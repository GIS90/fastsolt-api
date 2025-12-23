# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    base

base_info:
    __author__ = PyGo
    __time__ = 2025/11/30 14:21
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api
    __file_name__ = base.py

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
from pydantic import Field, validator, field_validator
from typing import List, Tuple, Dict, Set, Optional, Union, Text
from dataclasses import dataclass


@dataclass
class Address(baseModel):
    """
    request body: Address
    Base model class
    """
    province: str = Field(..., min_length=1, max_length=25, description="省份")
    city: str = Field(..., min_length=1, max_length=120, description="城市")
    address: Optional[Text] = Field(default=None, min_length=0, max_length=120, description="详情地址")

    model_config = {
        "json_schema_extra": {
            "example": {
                "province": "地球",
                "city": "中国",
                "address": "最牛逼的地方"
            }
        }
    }

class BaseUserBody(baseModel):
    """
    request body: User
    Base model class
    """
    name: str = Field(..., min_length=1, max_length=12, description="姓名")
    age: int = Field(..., ge=1, le=1000, description="年龄")
    sex: str = Field(..., min_length=1, max_length=1, description="性别")
    addr: Address

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "法外狂徒张三",
                "age": 32,
                "sex": "男",
                "addr": {
                    "province": "地球",
                    "city": "中国",
                    "address": "最牛逼的地方"
                }
            }
        }
    }
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    """
    字段特殊验证：字母+数字
    """
    @field_validator("name")
    def name_is_alnum(cls, value: str):
        assert str(value).isalnum(), "Field name field is isalnum."
        return value
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class UserBody(BaseUserBody):
    """
    request body: UserBody
    inherit BaseUser
    """
    phone: Optional[str] = Field(default=None, min_length=0, max_length=11, description="联系电话")

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "法外狂徒张三",
                "age": 32,
                "sex": "男",
                "addr": {
                    "province": "地球",
                    "city": "中国",
                    "address": "最牛逼的地方"
                },
                "phone": ""
            }
        }
    }

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    """
    字段特殊验证：字母+数字
    """
    @field_validator("name")
    def name_is_alnum(cls, value: str):
        assert str(value).isalnum(), "Field name field is isalnum."
        return value
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

