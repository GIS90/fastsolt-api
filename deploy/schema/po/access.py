# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    access

base_info:
    __author__ = PyGo
    __time__ = 2025/11/30 20:50
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api
    __file_name__ = access.py

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
from pydantic import Field, field_validator


class O2LUserLogin(baseModel):
    username: str = Field(..., min_length=1, max_length=25, description="用户名称")
    password: str = Field(..., min_length=1, max_length=30, description="用户密码")

    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "adc",
                "password": "123456"
            }
        }
    }
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    """
    字段特殊验证：字母+数字
    """
    @field_validator("username")
    def name_is_alnum(cls, value: str):
        assert str(value).isalnum(), "Field username field is isalnum."
        return value
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class TokenBody(baseModel):
    """
    Token body
    """
    access_token: str
    token_type: str
