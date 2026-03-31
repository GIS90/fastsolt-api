# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    xtb_user model

base_info:
    __author__ = PyGo
    __time__ = 2025/12/8 22:23
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo.space
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
from sqlalchemy import (
    String,
    Integer,
    Boolean,
    DateTime,
    Text
)
from sqlalchemy.orm import Mapped, mapped_column
from deploy.schema._dao_base_model import baseModel
from .common_field import IDField, RtxIdField, Md5Field, CUDField, StatusField
from typing import Optional

__all__ = ["XtbUserModel"]


class XtbUserModel(baseModel, IDField, RtxIdField, Md5Field, CUDField, StatusField):
    __tablename__ = 'xtb_user'
    __table_args__ = ({'comment': '系统表-用户表'})

    name: Mapped[str] = mapped_column(name="name", type_=String(30), nullable=False, comment="名称")
    password: Mapped[str] = mapped_column(name="password", type_=String(120), nullable=False, comment="密码[md5加密]")
    salt: Mapped[Optional[str]] = mapped_column(name="salt", type_=String(32), comment="密码盐值，随机MD5-ID[32位]")
    sex: Mapped[str] = mapped_column(name="sex", type_=String(2), nullable=False, comment="性别")
    email: Mapped[Optional[str]] = mapped_column(name="email", type_=String(80), comment="邮箱")
    phone: Mapped[Optional[str]] = mapped_column(name="phone", type_=String(15), comment="电话")
    avatar: Mapped[str] = mapped_column(name="avatar", type_=String(120), nullable=False, comment="头像地址")
    introduction: Mapped[Optional[str]] = mapped_column(name="introduction", type_=Text, comment="描述")
    role: Mapped[Optional[str]] = mapped_column(name="role", type_=String(255), nullable=False, comment="角色RTX-ID值（大写），关联role表，多角色用;分割")
    department: Mapped[Optional[str]] = mapped_column(name="department", type_=String(55), comment="部门MD5-ID值，关联department表")

    def __str__(self):
        return f"XtbUserModel Class[DB table: {self.__tablename__}], id: {self.id}, rtx_id: {self.rtx_id}, name: {self.name}."

    def __repr__(self):
        return self.__str__()
