# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    method view

base_info:
    __author__ = PyGo
    __time__ = 2025/11/29 18:50
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api
    __file_name__ = method.py

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
from deploy.utils.status import Status, SuccessStatus


# router
router: APIRouter = APIRouter(prefix="/method", tags=["METHOD请求方法"])


@router.get('/get',
            summary="GET请求请求示例",
            description="GET请求请求示例")
async def method_get(rtx_id: str) -> Status:
    """
    GET请求请求示例
    :param rtx_id: [str]查询请求参数
    :return: json
    """
    return SuccessStatus(
        data={'rtx_id': rtx_id, 'method': 'get'}
    )


@router.post('/post',
             summary="POST请求请求示例",
             description="POST请求请求示例")
async def method_post(rtx_id: str) -> Status:
    """
    POST请求请求示例
    :param rtx_id: [str]查询请求参数
    :return: json
    """
    return SuccessStatus(
        data={'rtx_id': rtx_id, 'method': 'post'}
    )


@router.put('/put',
            summary="PUT请求请求示例",
            description="PUT请求请求示例")
async def method_put(rtx_id: str) -> Status:
    """
    PUT请求请求示例
    :param rtx_id: [str]查询请求参数
    :return: json
    """
    return SuccessStatus(
        data={'rtx_id': rtx_id, 'method': 'put'}
    )


@router.delete('/delete',
               summary="DELETE请求请求示例",
               description="DELETE请求请求示例")
async def method_delete(rtx_id: str) -> Status:
    """
    DELETE请求请求示例
    :param rtx_id: [str]查询请求参数
    :return: json
    """
    return SuccessStatus(
        data={'rtx_id': rtx_id, 'method': 'delete'}
    )


@router.head('/head',
             summary="HEAD请求请求示例",
             description="HEAD请求请求示例")
async def method_head(rtx_id: str) -> Status:
    """
    HEAD请求请求示例
    :param rtx_id: [str]查询请求参数
    :return: json
    """
    return SuccessStatus(
        data={'rtx_id': rtx_id, 'method': 'head'}
    )


@router.options('/options',
                summary="OPTIONS请求请求示例",
                description="OPTIONS请求请求示例")
async def method_options(rtx_id: str) -> Status:
    """
    OPTIONS请求请求示例
    :param rtx_id: [str]查询请求参数
    :return: json
    """
    return SuccessStatus(
        data={'rtx_id': rtx_id, 'method': 'options'}
    )


@router.patch('/patch',
              summary="PATCH请求请求示例",
              description="PATCH请求请求示例")
async def method_patch(rtx_id: str) -> Status:
    """
    PATCH请求请求示例
    :param rtx_id: [str]查询请求参数
    :return: json
    """
    return SuccessStatus(
        data={'rtx_id': rtx_id, 'method': 'patch'}
    )

# * * * * * * * * * * * * * * * * * * * * * * * * * * [ END ] * * * * * * * * * * * * * * * * * * * * * * * * * * *
