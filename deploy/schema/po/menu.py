# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe:
    menu

base_info:
    __author__ = PyGo
    __time__ = 2025/12/6 16:01
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api
    __file_name__ = menu.py

usage:
    
design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
from deploy.schema._base import baseModel
from pydantic import Field
from typing import Optional


class MenuBaseModel(baseModel):
    pid: int = Field(..., description="菜单父ID")
    name: str = Field(..., min_length=1, max_length=55, description="名称")
    path: str = Field(..., min_length=1, max_length=255, description="路由地址")
    title: str = Field(..., min_length=1, max_length=35, description="菜单标题")
    level: int = Field(..., description="级别")
    type: str = Field(..., min_length=1, max_length=35, description="类型")
    component: str = Field(..., min_length=1, max_length=255, description="组件路径")
    redirect: Optional[str] = Field(..., max_length=255, description="重定向地址")
    icon: Optional[str] = Field(..., max_length=35, description="图标")
    isKeepAlive: bool = Field(..., description="缓存")
    isAffix: bool = Field(..., description="固定标签")
    isFull: bool = Field(..., description="全屏")
    isBreadcrumb: bool = Field(..., description="面包屑菜单")
    tag: str = Field(..., max_length=10, description="TAG")
    order_id: int = Field(..., description="级别")


class MenuEditModel(MenuBaseModel):
    id: int = Field(..., description="菜单ID")
    md5: str = Field(..., min_length=1, max_length=55, description="数据MD5")