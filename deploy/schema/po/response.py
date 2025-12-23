# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    response

base_info:
    __author__ = PyGo
    __time__ = 2025/11/30 13:39
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api
    __file_name__ = response.py

usage:
    
design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
from deploy.schema._po_base_model import baseModel
from pydantic import EmailStr
from typing import Optional, Union


class UserIn(baseModel):
    username: str
    password: str
    email: EmailStr
    phone: Optional[str]
    full_name: Union[str, None] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "法外狂徒张三",
                "password": "123456",
                "email": "gaoming@example.com",
                "phone": "123456789000",
                "full_name": "法外狂徒张三"
            }
        }
    }


class UserOut(baseModel):
    username: str
    email: EmailStr
    phone: Optional[str]
    full_name: Union[str, None] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "法外狂徒张三",
                "email": "gaoming@example.com",
                "phone": "123456789000",
                "full_name": "法外狂徒张三"
            }
        }
    }
