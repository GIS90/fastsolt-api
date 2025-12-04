# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    printer

base_info:
    __author__ = PyGo
    __time__ = 2025/11/27 20:04
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api
    __file_name__ = printer.py

usage:
    
design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
import pprint
from colorama import init
from deploy.utils.enumeration import (fontForeColor as ffc,
                                      fontBackColor as fbc)
from deploy.utils.enumeration import fontPrinter as fp


init(autoreset=True)    # 自动重置颜色，避免影响后续输出

pp = pprint.PrettyPrinter(
    indent=4,           # 缩进空格数
    width=80,           # 每行最大宽度
    depth=None,         # 嵌套深度限制，None表示无限制
    compact=False,      # 是否紧凑显示
    sort_dicts=True     # 是否对字典键排序
)


def printer_json(content: dict) -> None:
    pp.pprint(content)


def printer_info(content: str, hr: bool = False) -> None:
    if hr:print(ffc.GREEN.value + "*" * 88)
    print(fp.info.value + content)
    if hr:print(ffc.GREEN.value + "*" * 88)


def printer_warn(content: str, hr: bool = False) -> None:
    if hr:print(ffc.YELLOW.value + "~" * 88)
    print(fp.warn.value + content)
    if hr:print(ffc.YELLOW.value + "~" * 88)


def printer_error(content: str, hr: bool = False) -> None:
    if hr:print(ffc.RED.value + "> " * 45)
    print(fp.error.value + content)
    if hr:print(ffc.RED.value + "< " * 45)
