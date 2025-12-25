# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    DingTalk Api
    用请求DingTalk openApi来操作DingDing进行发消息等操作。
    目前，只支持机器人推送消息操作
    类添加了is_avail对access token进行判断是否可用

base_info:
    __author__ = PyGo
    __time__ = 2025/12/6 16:36
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api
    __file_name__ = dingtalk_lib.py

usage:
    user = 'manager2730'
    dapi = DingApi()
    res = dapi.robot2send(message=json_message, to_id=user)
    print(res)

design:
    DingDing官网开放平台

reference urls:
    官网发消息API：https://open.dingtalk.com/document/dingstart/robot-reply-and-send-messages

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
import json
import requests
from typing import Dict

from deploy.utils.status import Status, SuccessStatus, FailureStatus
from deploy.utils.status_value import StatusCode as status_code
from deploy.config import ding_base, ding_token_api
from deploy.utils.logger import logger as LOG

from alibabacloud_dingtalk.robot_1_0.client import Client as dingtalkrobot_1_0Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dingtalk.robot_1_0 import models as dingtalkrobot__1__0_models
from alibabacloud_tea_util import models as util_models
# from alibabacloud_tea_util.client import Client as UtilClient


_DINGTALK_BASE_URL = ding_base
_DINGTALK_TOKEN_API_URL = ding_token_api


class DingtalkLib:
    def __init__(self, app_key: str, app_secret: str) -> None:
        """
        初始化DingtalkLib工具，需要外部传入app-key、app-secret
        :param app_key: [str]
        :param app_secret:  [str]
        """
        self.app_key: str = app_key
        self.app_secret: str = app_secret
        self.base_api_url: str = _DINGTALK_BASE_URL
        self.token_api_url: str = _DINGTALK_TOKEN_API_URL
        self.msg_type: str = 'sampleMarkdown'   # 默认Markdown类型
        self.access_token = self.get_token()
        self.client = self.__create_client()

    def __str__(self) -> str:
        return f"DingtalkLib Class: [app-key: {self.app_key}]"

    def __repr__(self) -> str:
        return self.__str__()

    def check(self) -> bool:
        """
        检查是否有access token，如果没有token，则中止发信息请求
        建议用sys.exit()优雅的方式退出
        """
        return True if self.access_token else False

    def close(self) -> None:
        """
        关闭实例，清除access token
        """
        self.access_token = ''

    def get_token(self) -> str:
        """
        获取唯一access token，2h有效期
        this function is static method, it used to get access token code from dingTalk open api
        :return: access token
        result type is string
        """
        headers: Dict = {
            'Access-Control-Allow-Origin': '*'
        }
        params: Dict = {"appkey": self.app_key, "appsecret": self.app_secret}
        url: str = "%s%s" % (self.base_api_url, self.token_api_url)
        try:
            response = requests.get(url=url, headers=headers, params=params)
            if response.status_code == 200:
                json_res = response.json()
                if json_res and json_res.get("errcode") == 0:
                    return json_res.get("access_token")
        except Exception as e:
            LOG.error('[DingTalk] access token occur Exception: %s' % e)
        finally:
            LOG.error('[DingTalk]access token failure, please try again later.')
            return ''


    @staticmethod
    def __create_client() -> dingtalkrobot_1_0Client:
        """
        初始化账号Client
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config()
        config.protocol = 'https'
        config.region_id = 'central'
        return dingtalkrobot_1_0Client(config)

    def robot2send(self, message: dict, to_id: str) -> Status:
        """
        Use dingtalk openApi to send message
        :param message: DingDing消息体，为MarkDown语法
        :param to_id: 接收人ID
        :return: json type result
            code: 状态码,
            msg: 消息体
            data: 数据体

        message格式：
        {
            "title": "Hello World",
            "text": "Enjoy the good life every day！！!"
        }
        """
        if not self.access_token:
            return FailureStatus(
                code=status_code.CODE_903_OTHER_THREE_API_TOKEN_FAILURE.value,
                message="[DingTalk]Token初始化失败")

        batch_send_otoheaders = dingtalkrobot__1__0_models.BatchSendOTOHeaders()
        batch_send_otoheaders.x_acs_dingtalk_access_token = self.access_token
        batch_send_otorequest = dingtalkrobot__1__0_models.BatchSendOTORequest(
            robot_code=self.app_key,
            user_ids=[to_id],
            msg_key=self.msg_type,
            msg_param=json.dumps(message)
        )
        try:
            response = self.client.batch_send_otowith_options(
                batch_send_otorequest,
                batch_send_otoheaders,
                util_models.RuntimeOptions()
            )
            json_resp = {
                'process': response.body.process_query_key or '',
                'failure': response.body.invalid_staff_id_list or [],
                'control': response.body.flow_controlled_staff_id_list or []
            }
            return SuccessStatus(data=json_resp)
        except Exception as error:
            msg = '[DingTalk]发送信息 [%s] 异常: %s' % (to_id, error)
            LOG.error(msg)
            return FailureStatus(
                code=status_code.CODE_902_OTHER_THREE_API_SEND_FAILURE.value,
                message=msg)
