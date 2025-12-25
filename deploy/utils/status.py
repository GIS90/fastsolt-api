# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    the class of response, type json to use API

base_info:
    __author__ = PyGo
    __time__ = 2025/11/29 09:07
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api
    __file_name__ = status.py

usage:
    
design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
import json
from fastapi import status as fastapi_http_status
from fastapi.responses import JSONResponse
from typing import Union, Dict, List

from deploy.utils.status_value import StatusCode, StatusMsg
from deploy.utils.enumeration import MediaType


class Status(JSONResponse):
    """
    状态响应类，用于构建统一格式的JSON响应，继承FastAPI的JSONResponse

    Args:
        code (int): 状态码
        message (str): 响应消息，如果为空则根据状态码ID获取默认消息
        data (Union[List, Dict], optional): 响应数据，默认为None

    Returns:
        Status: 状态响应对象
    """

    def __init__(self, code: int, message: str, data: Union[List, Dict] = None):
        if data is None:
            data = {}
        self.status_body = {
            "code": code,
            "message": message if message else StatusMsg.get(code),
            "data": data,
        }
        super().__init__(
            content=self.status_body,
            status_code=fastapi_http_status.HTTP_200_OK,
            media_type=MediaType.APPJson.value
        )

    def json(self):
        return json.dumps(self.status_body)

    def dict(self):
        return self.status_body


class SuccessStatus(Status):
    """
    成功
    """

    def __init__(self,
                 code: int = StatusCode.CODE_100_SUCCESS.value,
                 message: str = None,
                 data: Union[List, Dict] = None
                 ):

        super().__init__(code, message, data)


class FailureStatus(Status):
    """
    失败
    """

    def __init__(self,
                 code: int = StatusCode.CODE_900_SERVER_API_EXCEPTION.value,
                 message: str = None,
                 data: Union[List, Dict] = None
                 ):

        super().__init__(code, message, data)

