# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    common field

base_info:
    __author__ = PyGo
    __time__ = 2025/12/28 14:57
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api
    __file_name__ = common_field.py

usage:
    
design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import (
    String,
    Integer,
    Boolean,
    DateTime,
    Text
)


class RtxIdField:
    rtx_id: Mapped[str] = mapped_column(String(35), name="rtx_id", nullable=False, comment="用户RTX-ID唯一标识")


class Md5Field:
    md5_id: Mapped[str] = mapped_column(String(55), name="md5_id", nullable=False, comment="数据唯一标识：MD5-ID")


class CUDField:
    create_time: Mapped[datetime] = mapped_column(DateTime(), name="create_time", nullable=False, comment="创建时间")
    create_rtx: Mapped[Optional[str]] = mapped_column(String(35), name="create_rtx", nullable=False, comment="创建用户")
    update_time: Mapped[Optional[datetime]] = mapped_column(DateTime(), name="update_time", comment="更新时间")
    update_rtx: Mapped[Optional[str]] = mapped_column(String(35), name="update_rtx", comment="更新用户")
    delete_time: Mapped[Optional[datetime]] = mapped_column(DateTime(), name="delete_time", comment="删除时间")
    delete_rtx: Mapped[Optional[str]] = mapped_column(String(35), name="delete_rtx", comment="删除用户")


class StatusField:
    status: Mapped[bool] = mapped_column(Boolean(), name="status", default=False, comment="状态：1注销/删除；0启用/正常（默认）")

