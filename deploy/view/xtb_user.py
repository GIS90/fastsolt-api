# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    xtb_user view

base_info:
    __author__ = PyGo
    __time__ = 2025/12/9 21:58
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api
    __file_name__ = user.py

usage:
    
design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from deploy.curd.database import get_db
from deploy.service.xtb_user import XtbUserService
from deploy.utils.status import Status
from deploy.utils.depend import pageable_params, depend_token_rtx


# define route
xtb_user: APIRouter = APIRouter(prefix="/user", tags=["实例代码：系统用户增删改查"])

# service
xtb_user_service: XtbUserService = XtbUserService()


@xtb_user.get("/", summary="列表")
async def user_list(
        # token_rtx_id: str = Depends(depend_token_rtx),
        params: dict = Depends(pageable_params),
        db: AsyncSession = Depends(get_db)
) -> Status:
    return await xtb_user_service.user_list(db=db, rtx_id="123", params=params)
    return await xtb_user_service.user_list(db=db, rtx_id=token_rtx_id, params=params)