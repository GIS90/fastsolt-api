# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    xtb_user

base_info:
    __author__ = PyGo
    __time__ = 2025/12/25 22:51
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api
    __file_name__ = xtb_user.py

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
from pydantic import Field
from typing import Optional



class XtbUserBaseModel(baseModel):
    rtx_id: str = Field(..., min_length=1, max_length=35, description="用户RTX-ID", alias="rtxId")
    name: str = Field(..., min_length=1, max_length=30, description="用户昵称")
    sex: str = Field(..., min_length=1, max_length=2, description="用户性别")
    email: str = Field(..., min_length=1, max_length=55, description="用户邮箱")
    phone: str = Field(..., min_length=11, max_length=11, description="用户电话")
    introduction: Optional[str] = Field(..., max_length=255, description="个性签名")

    model_config = {
        "json_schema_extra": {
            "example": {
                "rtxId": "ADC",
                "name": "abcd木头人",
                "sex": "M",
                "email": "gaoming971366@163.com",
                "phone": "13051355646",
                "introduction": "哈哈哈哈哈"
            }
        }
    }


class XtbUserUpdateModel(XtbUserBaseModel):
    md5_id: str = Field(..., min_length=1, max_length=55, description="数据MD5", alias="md5Id")

    model_config = {
        "json_schema_extra": {
            "example": {
                "rtxId": "adc",
                "md5Id": "AAAAAAAAAA",
                "name": "adc",
                "sex": "M",
                "email": "gaoming971366@163.com",
                "phone": "13051355646",
                "introduction": "哈哈哈哈哈"
            }
        }
    }


