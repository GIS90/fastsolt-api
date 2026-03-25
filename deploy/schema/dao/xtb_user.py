# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    xtb_user modal

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
from .common_field import RtxIdField, Md5Field, CUDField, StatusField
from typing import Optional


__all__ = ["XtbUserModel"]


class XtbUserModel(baseModel, RtxIdField, Md5Field, CUDField, StatusField):
    __tablename__ = 'xtb_user'
    __table_args__ = ({'comment': '系统表-用户表'})

    id: Mapped[int] = mapped_column(Integer, name="id", autoincrement="auto", primary_key=True, comment="主键，自增ID")
    name: Mapped[str] = mapped_column(String(30), name="name", nullable=False, comment="名称")
    password: Mapped[str] = mapped_column(String(120), name="password", nullable=False, comment="密码[md5加密]")
    salt: Mapped[Optional[str]] = mapped_column(String(55), name="salt", comment="密码盐值，随机MD5-ID")
    sex: Mapped[str] = mapped_column(String(2), name="sex", nullable=False, comment="性别")
    email: Mapped[Optional[str]] = mapped_column(String(55), name="email", comment="邮箱")
    phone: Mapped[Optional[str]] = mapped_column(String(15), name="phone", comment="电话")
    avatar: Mapped[str] = mapped_column(String(120), name="avatar", nullable=False, comment="头像地址")
    introduction: Mapped[Optional[str]] = mapped_column(Text, name="introduction", comment="描述")
    role: Mapped[Optional[str]] = mapped_column(String(255), name="role", nullable=False, comment="角色RTX-ID值（大写），关联role表，多角色用;分割")
    department: Mapped[Optional[str]] = mapped_column(String(55), name="department", comment="部门MD5-ID值，关联department表")

    def __str__(self):
        return f"XtbUserModel Class[DB table: {self.__tablename__}], id: {self.id}, rtx_id: {self.rtx_id}, name: {self.name}."

    def __repr__(self):
        return self.__str__()
