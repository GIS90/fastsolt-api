# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    xtb_sysuser view

base_info:
    __author__ = PyGo
    __time__ = 2025/12/9 21:58
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api
    __file_name__ = xtb_sysuser.py

usage:
    
design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
from typing import Annotated
from fastapi import APIRouter, Depends, Query, Body
from sqlalchemy.ext.asyncio import AsyncSession

from deploy.curd.database import get_db
from deploy.service.xtb_sysuser import XtbSysUserService
from deploy.utils.status import Status
from deploy.utils.depend import pageable_params, depend_token_rtx
from deploy.schema.po.xtb_user import XtbUserBaseModel, XtbUserUpdateModel


# router
router: APIRouter = APIRouter(prefix="/user", tags=["实例代码：系统用户增删改查"])
# service
xtb_sysuser_service: XtbSysUserService = XtbSysUserService()


@router.get("/list", summary="用户列表")
async def user_list(
    params: dict = Depends(pageable_params),
    token_rtx_id: str = Depends(depend_token_rtx),
    db: AsyncSession = Depends(get_db)
) -> Status:
    return await xtb_sysuser_service.user_list(db=db, rtx_id=token_rtx_id, params=params)


@router.get("", summary="单条用户")
async def get_user_by_md5_id(
    md5_id: str = Query(..., description="用户md5-id"),
    token_rtx_id: str = Depends(depend_token_rtx),
    db: AsyncSession = Depends(get_db)
) -> Status:
    return await xtb_sysuser_service.get_user_by_md5_id(db=db, rtx_id=token_rtx_id, md5_id=md5_id)


@router.post("", summary="新增用户")
async def user_add(
    params: Annotated[XtbUserBaseModel, Body()],
    token_rtx_id: str = Depends(depend_token_rtx),
    db: AsyncSession = Depends(get_db)
) -> Status:
    return await xtb_sysuser_service.user_add(db=db, rtx_id=token_rtx_id, model=params.model_dump())


@router.put("", summary="更新用户")
async def user_update(
    params: Annotated[XtbUserUpdateModel, Body()],
    token_rtx_id: str = Depends(depend_token_rtx),
    db: AsyncSession = Depends(get_db)
) -> Status:
    return await xtb_sysuser_service.user_update(db=db, rtx_id=token_rtx_id, model=params.model_dump())


@router.delete("/hard", summary="【硬删除】用户")
async def user_delete(
    md5_id: str = Query(..., description="用户md5-id"),
    token_rtx_id: str = Depends(depend_token_rtx),
    db: AsyncSession = Depends(get_db)
) -> Status:
    return await xtb_sysuser_service.user_delete_hard(db=db, rtx_id=token_rtx_id, md5_id=md5_id)


@router.delete("/soft", summary="【软删除】用户")
async def user_delete(
    md5_id: str = Query(..., description="用户md5-id"),
    token_rtx_id: str = Depends(depend_token_rtx),
    db: AsyncSession = Depends(get_db)
) -> Status:
    return await xtb_sysuser_service.user_delete_soft(db=db, rtx_id=token_rtx_id, md5_id=md5_id)
