# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    X

base_info:
    __author__ = PyGo
    __time__ = 2025/12/6 15:29
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api
    __file_name__ = x.py

usage:
    
design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
from fastapi import Header, Query

from deploy.schema._po_base_model import baseModel
from pydantic import Field, validator, field_validator
from typing import List, Tuple, Dict, Set, Optional, Union, Text


# parameters
MIN_LENGTH = 1
MAX_LENGTH = 299


class RequestMd5Model(baseModel):
    """
    Md5通用参数请求体
    单条数据：str类型
    """
    md5: str = Query(..., min_length=MIN_LENGTH, max_length=MAX_LENGTH, description="数据MD5")

    model_config = {
        "json_schema_extra": {
            "example": {
                "md5": "A"
            }
        }
    }


class RequestMd5Models(baseModel):
    """
    Md5通用参数请求体
    多条数据：List类型
    """
    md5: List[str] = Query(..., min_length=MIN_LENGTH, description="数据MD5列表")

    model_config = {
        "json_schema_extra": {
            "example": {
                "md5": ["A", "B", "C"]
            }
        }
    }


class RequestIDModels(baseModel):
    """
    ID通用参数请求体
    多条数据：List类型
    """
    id: List[Union[int, str]] = Query(..., description="数据ID列表")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": [1, "B", "C"]
            }
        }
    }


class DownloadFileModel(baseModel):
    """
    下载数据请求参数
    """
    api: str = Query(..., min_length=MIN_LENGTH, max_length=55, description="API-ID"),
    type: str = Query(..., min_length=MIN_LENGTH, max_length=35, description="下载数据类型"),
    name: str = Query(..., min_length=MIN_LENGTH, max_length=55, description="下载文件名称"),
    md5: Optional[List[str]] = Query(..., description="数据MD5列表")

    model_config = {
        "json_schema_extra": {
            "example": {
                "api": "api",
                "type": "ALL",
                "name": "下载.xlsx",
                "md5": ["A", "B", "C"]
            }
        }
    }


class PageListModel(baseModel):
    """
    List数据查询：分页参数 + 条件数据模型（type：dict）
    """
    page: int = Field(..., ge=MIN_LENGTH, description="页码"),
    pageSize: int = Field(..., ge=MIN_LENGTH, description="条数"),
    content: Optional[dict] = Field(..., description="非模糊查询")

    model_config = {
        "json_schema_extra": {
            "example": {
                "page": 1,
                "pageSize": 10,
                "content": {
                    "name": "PyGo"
                }
            }
        }
    }

