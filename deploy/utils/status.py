# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    the class of response, type json to use api

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
    def __init__(self, status_id: int, message: str, data: Union[List, Dict] = None):
        if data is None:
            data = {}
        self.status_body = {
            "status_id": status_id,
            "message": message if message else StatusMsg.get(status_id),
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
                 status_id: int = StatusCode.CODE_100_SUCCESS.value,
                 message: str = None,
                 data: Union[List, Dict] = None
                 ):

        super().__init__(status_id, message, data)


class FailureStatus(Status):
    """
    失败
    """

    def __init__(self,
                 status_id: int = StatusCode.CODE_900_SERVER_API_EXCEPTION.value,
                 message: str = None,
                 data: Union[List, Dict] = None
                 ):

        super().__init__(status_id, message, data)

