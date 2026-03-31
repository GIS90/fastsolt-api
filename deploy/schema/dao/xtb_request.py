# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    xtb_request model

base_info:
    __author__ = PyGo
    __time__ = 2026/3/25 23:11
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api
    __file_name__ = xtb_request.py

usage:
    
design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
from datetime import datetime
from sqlalchemy import (
    String,
    Integer,
    Boolean,
    DateTime,
    Date,
    Text,
    DECIMAL
)
from sqlalchemy.orm import Mapped, mapped_column
from deploy.schema._dao_base_model import baseModel
from .common_field import IDField, RtxIdField, Md5Field, StatusField
from typing import Optional


__all__ = ["XtbRequestModel"]


class XtbRequestModel(baseModel, IDField, RtxIdField, Md5Field, StatusField):
    __tablename__ = 'xtb_request'
    __table_args__ = ({'comment': '系统表-请求表'})

    ip: Mapped[str] = mapped_column(name="ip", type_=String(15), comment="用户IP")
    method: Mapped[str] = mapped_column(name="method", type_=String(10), comment="请求方法")
    params: Mapped[str] = mapped_column(name="params", type_=String(100), comment="请求参数")
    path: Mapped[str] = mapped_column(name="path", type_=String(55), comment="请求路径")
    full_path: Mapped[str] = mapped_column(name="full_path", type_=String(155), comment="请求路径+参数")
    host_url: Mapped[str] = mapped_column(name="host_url", type_=String(100), comment="请求HOST")
    url: Mapped[str] = mapped_column(name="url", type_=String(255), comment="请求全路径")
    cost: Mapped[float] = mapped_column(name="cost", type_=DECIMAL(10, 4), comment="运行时间")
    create_time: Mapped[datetime] = mapped_column(name="create_time", type_=DateTime(), nullable=False, comment="创建时间")
    create_date = mapped_column(name="create_date", type_=Date(), comment="创建日期")
    delete_rtx: Mapped[Optional[str]] = mapped_column(name="delete_rtx", type_=String(35), comment="删除用户RTX-ID")
    delete_time: Mapped[Optional[datetime]] = mapped_column(name="delete_time", type_=DateTime(), comment="删除时间")

    def __str__(self):
        return f"XtbRequestModel Class[DB table: {self.__tablename__}], id: {self.id}, rtx_id: {self.rtx_id}, [{self.ip}]-{self.url}."

    def __repr__(self):
        return self.__str__()
