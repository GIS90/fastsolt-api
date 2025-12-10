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


class XtbUserService:

    user_fields: Dict = [
        "id",
        "rtx_id",
        "md5_id",
        "fullname",
        "password",
        "sex",
        "email",
        "phone",
        "avatar",
        "introduction"
    ]

    def __init__(self):
        """
        UserService class initialize
        """
        self.xtb_user_bo = XtbUserBo()

    def __str__(self):
        print("UserService class.")

    def __repr__(self):
        self.__str__()

    async def __format_user_model(self, model) -> Dict:
        """
        format user model to dict
        :param model: db model
        :return: dict
        """
        _data: Dict = dict()
        if not model:
            return _data

        for field in self.user_fields:
            if not field: continue
            _data[field] = getattr(model, field)
        else:
            return _data

    async def user_list(self, db: AsyncSession, rtx_id: str, params: Dict) -> Status:
        users = await self.xtb_user_bo.get_all(db=db, offset=params.get("offset"), limit=params.get("limit"))
        data: List = list()
        data.extend(
            filter(
                lambda x: x is not None,
                [await self.__format_user_model(u) for u in users if u]
            )
        )
        result: Dict = {
            "list": data,
            "total": len(users)
        }
        return SuccessStatus(data=data)

