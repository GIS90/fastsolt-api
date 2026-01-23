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

    def __init__(self, db_connection: AsyncSession):
        """
        XtbSysUserService class initialize
        """
        self.db: AsyncSession = db_connection
        self.xtb_sysuser_bo = XtbSysUserBo()

    def __str__(self):
        print("XtbSysUserService class.")

    def __repr__(self):
        self.__str__()

    async def __valid_user_by_md5_or_rtx(
            self,
            user_id: str,
            status_check: bool = True,
            response_type: Literal["dict", "model"] = "model",
            user_type: Literal["md5", "rtx"] = "md5",
    ) -> Tuple[bool, Any]:
        if not user_id:
            return False, FailureStatus(
                code=status_code.CODE_400_REQUEST_PARAMETER_MISS,
                message="缺少md5参数" if user_type == "md5" else "缺少rtx参数")

        user = await self.xtb_sysuser_bo.get_by_md5_id(db=self.db, md5_id=user_id) if user_type == "md5" \
            else await self.xtb_sysuser_bo.get_by_rtx_id(db=self.db, rtx_id=user_id)
        if not user:
            return False, FailureStatus(code=status_code.CODE_501_DATA_NOT_EXIST)
        if status_check and getattr(user, "status", None):
            return False, FailureStatus(code=status_code.CODE_503_DATA_DELETE_NOT_EDIT)

        return (True, user if response_type == "model"
                        else await model_converter_dict(model=user, fields=xtb_sysuser_detail_fields, default_value="****"))

    async def user_list(self, rtx_id: str, params: Dict) -> Status:
        users = await self.xtb_sysuser_bo.get_pagination(
            db=self.db,
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
            "total": await self.xtb_sysuser_bo.get_count(self.db)
        }
        return SuccessStatus(data=result)

    async def get_login_by_rtx_id(self, rtx_id: str) -> Dict:
        __flag, data = await self.__valid_user_by_md5_or_rtx(
            user_id=rtx_id, status_check=False, response_type="dict", user_type="rtx"
        )
        return data if __flag else None

    async def get_user_by_md5_id(self, rtx_id: str, md5_id: str) -> Status:
        __flag, data = await self.__valid_user_by_md5_or_rtx(
            user_id=md5_id, status_check=False, response_type="dict", user_type="md5"
        )
        return SuccessStatus(data=data) if __flag else data

    async def user_add(self, rtx_id: str, model: Dict) -> Status:
        new_user = await self.xtb_sysuser_bo.new_model()
        __now = get_now()
        __password: str = random_string()
        __salt: str = random_string()
        # TODO 用户默认的头像、密码可以放在数据库中
        new_user.md5_id = md5(v=f"{model.get('rtx_id')}-{__now}-{__password}")
        new_user.avatar = self.DEFAULT_AVATAR
        new_user.status = False
        new_user.salt = __salt
        new_user.create_time = __now
        new_user.create_rtx = rtx_id
        new_user.password = md5(v=f"{__password}{__salt}")
        for k, v in model.items():
            setattr(new_user, k, v)
        await self.xtb_sysuser_bo.add(db=self.db, model=new_user)
        return SuccessStatus(data={"password": __password})

    async def user_update(self, rtx_id: str, model: Dict) -> Status:
        _md5 = model.get("md5_id")
        __flag, data = await self.__valid_user_by_md5_or_rtx(
            user_id=_md5, status_check=True, response_type="model"
        )
        if not __flag: return data

        if model.get("rtx_id"):
            del model["rtx_id"]
        del model["md5_id"]
        model["update_rtx"] = rtx_id
        model["update_time"] = get_now()
        for k, v in model.items():
            setattr(data, k, v)
        await self.xtb_sysuser_bo.update(db=self.db, model=data)
        return SuccessStatus()

    async def user_delete_hard(self, rtx_id: str, md5_id: str) -> Status:
        __flag, data = await self.__valid_user_by_md5_or_rtx(
            user_id=md5_id, status_check=True, response_type="model", user_type="md5"
        )
        if not __flag: return data

        await self.xtb_sysuser_bo.delete(db=self.db, model=data)
        return SuccessStatus()


    async def user_delete_soft(self, rtx_id: str, md5_id: str) -> Status:
        __flag, data = await self.__valid_user_by_md5_or_rtx(
            user_id=md5_id, status_check=True, response_type="model", user_type="md5"
        )
        if not __flag: return data

        setattr(data, "status", True)
        setattr(data, "delete_rtx", rtx_id)
        setattr(data, "delete_time", get_now())
        await self.xtb_sysuser_bo.update(db=self.db, model=data)
        return SuccessStatus()

    async def user_batch_delete_hard(self, rtx_id: str, md5_id: List) -> Status:
        await self.xtb_sysuser_bo.batch_delete(db=self.db, md5_id=md5_id)
        return SuccessStatus()


    async def user_batch_delete_soft(self, rtx_id: str, md5_id: List) -> Status:
        await self.xtb_sysuser_bo.batch_soft_delete_update(db=self.db, md5_id=md5_id, rtx_id=rtx_id)
        return SuccessStatus()