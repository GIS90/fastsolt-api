# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    api view

base_info:
    __author__ = PyGo
    __time__ = 2025/11/30 14:35
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api
    __file_name__ = api.py

usage:
    
design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
from fastapi import APIRouter

from deploy.service.api import ApiService
from deploy.utils.decorator import watch_except


# router
router: APIRouter = APIRouter(prefix="/api", tags=["APIs集合"])
# service
api_service: ApiService = ApiService()


@router.get('/m1/case',
            summary="[M1模块]CASE",
            description="[M1模块]测试用例")
@watch_except
async def m1_case() -> dict:
    """
    [M1模块]CASE
    :return: json
    """
    return await api_service.m1_case()
