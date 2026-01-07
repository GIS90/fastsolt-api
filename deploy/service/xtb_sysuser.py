# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    xtb_sysuser service

base_info:
    __author__ = PyGo
    __time__ = 2025/12/9 22:22
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
from typing import Dict, List, Tuple, Literal, Any
from sqlalchemy.ext.asyncio import AsyncSession
from deploy.curd.xtb_sysuser import XtbSysUserBo
from deploy.utils.status import Status, SuccessStatus, FailureStatus
from deploy.utils.status_value import (StatusCode as status_code,
                                       StatusMsg as status_msg)
from deploy.utils.converter import model_converter_dict
from deploy.schema.dto.xtb_sysuser import xtb_sysuser_list_fields, xtb_sysuser_detail_fields
from deploy.utils.utils import get_now, random_string, md5


class XtbSysUserService:
    DEFAULT_AVATAR = "http://pygo2.top/images/article_github.jpg"

    def __init__(self):
        """
        XtbSysUserService class initialize
        """
        self.xtb_sysuser_bo = XtbSysUserBo()

    def __str__(self):
        print("XtbSysUserService class.")

    def __repr__(self):
        self.__str__()

    async def __valid_user_by_md5_id(
            self,
            db: AsyncSession,
            md5_id: str,
            status_check: bool = True,
            response_type: Literal["dict", "model"] = "model"
    ) -> Tuple[bool, Any]:
        if not md5_id:
            return False, FailureStatus(code=status_code.CODE_4002_REQUEST_PARAMETER_MISS_MD5)

        user = await self.xtb_sysuser_bo.get_by_md5_id(db=db, md5_id=md5_id)
        if not user:
            return False, FailureStatus(code=status_code.CODE_501_DATA_NOT_EXIST)
        if status_check and getattr(user, "status", None):
            return False, FailureStatus(code=status_code.CODE_503_DATA_DELETE_NOT_EDIT)

        return (True, user if response_type == "model"
                        else await model_converter_dict(model=user, fields=xtb_sysuser_detail_fields, default_value="****"))

    async def user_list(self, db: AsyncSession, rtx_id: str, params: Dict) -> Status:
        users = await self.xtb_sysuser_bo.get_pagination(
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
                [await model_converter_dict(model=u, fields=xtb_sysuser_list_fields) for u in users if u]
            )
        )
        result: Dict = {
            "list": data,
            "total": await self.xtb_sysuser_bo.get_count(db)
        }
        return SuccessStatus(data=result)

    async def get_user_by_md5_id(self, db: AsyncSession, rtx_id: str, md5_id: str) -> Status:
        _, data = await self.__valid_user_by_md5_id(
            db=db, md5_id=md5_id, status_check=False, response_type="dict"
        )
        return data

    async def user_add(self, db: AsyncSession, rtx_id: str, model: Dict) -> Status:
        new_user = await self.xtb_sysuser_bo.new_model()
        __now = get_now()
        __password = random_string()
        # TODO 用户默认的头像、密码可以放在数据库中
        new_user.md5_id = md5(v=f"{model.get('rtx_id')}-{__now}-{__password}")
        new_user.avatar = self.DEFAULT_AVATAR
        new_user.status = False
        new_user.create_time = __now
        new_user.create_rtx = rtx_id
        new_user.password = md5(v=__password)
        for k, v in model.items():
            setattr(new_user, k, v)
        await self.xtb_sysuser_bo.add(db=db, model=new_user)
        return SuccessStatus(data={"password": __password})

    async def user_update(self, db: AsyncSession, rtx_id: str, model: Dict) -> Status:
        _md5 = model.get("md5_id")
        flag, data = await self.__valid_user_by_md5_id(
            db=db, md5_id=_md5, status_check=True, response_type="model"
        )
        if not flag: return data
        if model.get("rtx_id"):
            del model["rtx_id"]
        del model["md5_id"]
        model["update_rtx"] = rtx_id
        model["update_time"] = get_now()
        for k, v in model.items():
            setattr(data, k, v)
        await self.xtb_sysuser_bo.update(db=db, model=data)
        return SuccessStatus()

    async def user_delete_hard(self, db: AsyncSession, rtx_id: str, md5_id: str) -> Status:
        flag, data = await self.__valid_user_by_md5_id(
            db=db, md5_id=md5_id, status_check=True, response_type="model"
        )
        if not flag: return data

        await self.xtb_sysuser_bo.delete(db=db, model=data)
        return SuccessStatus()


    async def user_delete_soft(self, db: AsyncSession, rtx_id: str, md5_id: str) -> Status:
        flag, data = await self.__valid_user_by_md5_id(
            db=db, md5_id=md5_id, status_check=True, response_type="model"
        )
        if not flag: return data

        setattr(data, "status", True)
        setattr(data, "delete_rtx", rtx_id)
        setattr(data, "delete_time", get_now())
        await self.xtb_sysuser_bo.update(db=db, model=data)
        return SuccessStatus()

    async def user_batch_delete_hard(self, db: AsyncSession, rtx_id: str, md5_id: List) -> Status:
        await self.xtb_sysuser_bo.batch_delete(db=db, md5_id=md5_id)
        return SuccessStatus()


    async def user_batch_delete_soft(self, db: AsyncSession, rtx_id: str, md5_id: List) -> Status:
        await self.xtb_sysuser_bo.batch_soft_delete_update(db=db, md5_id=md5_id, rtx_id=rtx_id)
        return SuccessStatus()