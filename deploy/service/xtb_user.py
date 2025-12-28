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
from deploy.utils.utils import get_now, random_string, md5


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
        users = await self.xtb_user_bo.get_pagination(
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
            "list": data,
            "total": await self.xtb_user_bo.get_count(db)
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

    async def add_user(self, db: AsyncSession, rtx_id: str, model: Dict):
        new_user = await self.xtb_user_bo.new_model()
        __now = get_now()
        __password = random_string()
        new_user.md5_id = md5(v=f"{model.get('rtx_id')}-{__now}-{__password}")
        new_user.avatar = "http://pygo2.top/images/article_github.jpg"
        new_user.status = False
        new_user.create_time = __now
        new_user.create_rtx = rtx_id
        new_user.password = __password
        new_user.role = ""
        for k, v in model.items():
            setattr(new_user, k, v)
        await self.xtb_user_bo.add(db=db, model=new_user)
        return SuccessStatus()