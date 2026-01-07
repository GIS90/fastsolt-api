# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    xtb_sysuser

base_info:
    __author__ = PyGo
    __time__ = 2025/12/17 22:37
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api
    __file_name__ = xtb_sysuser.py

usage:
  
design:
    字段含义：
       - 'key': 模型中的属性名；
       - 'type': 属性的数据类型（如 "str", "int", "datetime" 等），具体含义参考FieldTypeEnum
       - 'name': 输出字典中对应的键名。
    完全体：
        [
            {"key": "id", "type": "int", "name": "id"},
            {"key": "rtx_id", "type": ft.STRING, "name": "rtxId"},
            {"key": "md5_id", "type": ft.STRING, "name": "md5Id"},
        ]
        
    简版本：
        [
            {"key": "id"},
            {"key": "rtx_id"},
            {"key": "md5_id"},
        ]
        
        
reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
from deploy.utils.enumeration import FieldTypeEnum as ft


xtb_sysuser_list_fields = [
    {"key": "id", "type": ft.INT, "name": "id"},
    {"key": "rtx_id", "type": ft.STR, "name": "rtxId"},
    {"key": "md5_id", "type": ft.STR, "name": "md5Id"},
    {"key": "name", "type": ft.STR, "name": "name"},
    {"key": "sex", "type": ft.STR, "name": "sex"},
    {"key": "email", "type": ft.STR, "name": "email"},
    {"key": "phone", "type": ft.STR, "name": "phone"},
    {"key": "avatar", "type": ft.STR, "name": "avatar"},
    {"key": "introduction", "type": ft.STR, "name": "introduction"},
    {"key": "status", "type": ft.BOOLTEXT, "name": "status"},
    {"key": "create_rtx", "type": ft.STR, "name": "createRtx"},
    {"key": "create_time", "type": ft.DATETIME, "name": "createTime"},
    {"key": "update_rtx", "type": ft.STR, "name": "updateRtx"},
    {"key": "update_time", "type": ft.DATETIME, "name": "updateTime"},
]


xtb_sysuser_detail_fields = [
    {"key": "id"},
    {"key": "rtx_id", "type": ft.STR, "name": "rtxId"},
    {"key": "name"},
    {"key": "sex"},
    {"key": "email"},
    {"key": "phone"},
    {"key": "avatar"},
    {"key": "introduction"},
    {"key": "status", "type": ft.BOOLTEXT, "name": "status"},
]
