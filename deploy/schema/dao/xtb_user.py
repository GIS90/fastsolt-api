# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    sysuser model

base_info:
    __author__ = PyGo
    __time__ = 2025/12/8 22:23
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api
    __file_name__ = sysuser.py

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
from typing import Optional
from datetime import datetime


__all__ = ("XtbUserModel")


class XtbUserModel(baseModel):
    __tablename__ = 'xtb_user'
    __table_args__ = ({'comment': '系统表-系统用户表'})

    id: Mapped[int] = mapped_column(Integer, name="id",  autoincrement="auto", primary_key=True, comment="主键，自增ID")
    rtx_id: Mapped[str] = mapped_column(String(35), name="rtx_id", nullable=False, comment="用户rtx-id唯一标识")
    md5_id: Mapped[str] = mapped_column(String(55), name="md5_id", nullable=False, comment="唯一标识：MD5-ID")
    fullname: Mapped[str] = mapped_column(String(30), name="fullname", nullable=False, comment="用户名称")
    password: Mapped[str] = mapped_column(String(120), name="password", nullable=False, comment="用户密码[md5加密]")
    sex: Mapped[str] = mapped_column(String(2), name="sex", nullable=False, comment="用户性别")
    email: Mapped[Optional[str]] = mapped_column(String(55), name="email", comment="用户邮箱")
    phone: Mapped[Optional[str]] = mapped_column(String(15), name="phone", comment="用户电话")
    avatar: Mapped[str] = mapped_column(String(120), name="avatar", nullable=False, comment="用户头像地址")
    introduction: Mapped[Optional[str]] = mapped_column(Text, name="introduction", comment="用户描述")
    role: Mapped[Optional[str]] = mapped_column(String(120),name="role",  nullable=False, comment="用户角色engname值，关联role表，多角色用;分割")
    department: Mapped[Optional[str]] = mapped_column(String(55), name="department", comment="用户部门md5-id值，关联department表")
    create_time: Mapped[datetime] = mapped_column(DateTime(), name="create_time", nullable=False, comment="创建时间")
    create_rtx: Mapped[Optional[str]] = mapped_column(String(35), name="create_rtx", nullable=False, comment="创建用户")
    update_time: Mapped[Optional[datetime]] = mapped_column(DateTime(), name="update_time", comment="更新时间")
    update_rtx: Mapped[Optional[str]] = mapped_column(String(35), name="update_rtx", comment="更新用户")
    delete_time: Mapped[Optional[datetime]] = mapped_column(DateTime(), name="delete_time", comment="删除时间")
    delete_rtx: Mapped[Optional[str]] = mapped_column(String(35), name="delete_rtx", comment="删除用户")
    status: Mapped[bool] = mapped_column(Boolean(), name="status", default=False, comment="用户状态：True注销状态；False可用状态")

    def __str__(self):
        return f"XtbUserModel Class[DB table: xtb_user], id: {self.id}, rtx_id: {self.rtx_id}, fullname: {self.fullname}."

    def __repr__(self):
        return self.__str__()

