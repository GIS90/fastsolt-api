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


pp = pprint.PrettyPrinter(
    indent=4,           # 缩进空格数
    width=80,           # 每行最大宽度
    depth=None,         # 嵌套深度限制，None表示无限制
    compact=False,      # 是否紧凑显示
    sort_dicts=True     # 是否对字典键排序
)


def __printer(data):
    pp.pprint(data)


def printer_scan(data):
    print("*" * 88)
    __printer(data)
    print("*" * 88)


def printer_die(data):
    print("> " * 55)
    __printer(data)
    print("< " * 55)
