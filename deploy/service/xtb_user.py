# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    xtb_user service

base_info:
    __author__ = PyGo
    __time__ = 2025/12/9 22:22
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
from typing import Dict, List
from sqlalchemy.ext.asyncio import AsyncSession
from deploy.curd.xtb_user import XtbUserBo
from deploy.utils.status import Status, SuccessStatus, FailureStatus
from deploy.utils.status_value import (StatusCode as status_code,
                                       StatusMsg as status_msg)
from deploy.utils.converter import model_converter_dict
from deploy.schema.dto.xtb_user import xtb_user_list_fields, xtb_user_detail_fields


class XtbUserService:

    def __init__(self):
        """
        UserService class initialize
        """
        self.xtb_user_bo = XtbUserBo()

    def __str__(self):
        print("UserService class.")

    def __repr__(self):
        self.__str__()

    async def user_list(self, db: AsyncSession, rtx_id: str, params: Dict) -> Status:
        users = await self.xtb_user_bo.get_all(
            db=db,
            offset=params.get("offset"),
            limit=params.get("limit")
        )
        if not users:
            return FailureStatus(code=status_code.CODE_101_SUCCESS_NO_DATA)

        data: List = list()
        data.extend(
            filter(
                lambda x: x is not None and x is not {},
                [await model_converter_dict(model=u, fields=xtb_user_list_fields) for u in users if u]
            )
        )
        result: Dict = {
            "rtxId": rtx_id,
            "list": data,
            "total": len(users)
        }
        return SuccessStatus(data=result)

    async def get_user_by_md5_id(self, db: AsyncSession, rtx_id: str, md5_id: str) -> Status:
        model = await self.xtb_user_bo.get_by_md5_id(db=db, md5_id=md5_id)
        return SuccessStatus(data=await model_converter_dict(
            model=model,
            fields=xtb_user_detail_fields,
            default_value="****")
        ) if model \
            else FailureStatus(code=status_code.CODE_501_DATA_NOT_EXIST)