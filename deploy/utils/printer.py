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
from typing import Dict
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

def printer_json(content: Dict) -> None:
    """
    格式化打印JSON内容
    """
    pp.pprint(content)


def __printer(content: str,
              content_color: str,
              hr: bool,
              hr_symbol: str,
              hr_color: str,
              hr_length: int) -> None:
    """
    打印带有颜色和分隔线的内容

    参数:
        content (str): 要打印的主要内容
        content_color (str): 内容的颜色代码
        hr (bool): 是否显示分隔线
        hr_symbol (str): 分隔线使用的符号
        hr_color (str): 分隔线的颜色代码
        hr_length (int): 分隔线的长度

    返回值:
        None
    """
    __hr = hr_symbol * hr_length
    if hr: print(f"{hr_color}{__hr}")
    print(f"{content_color}{content}")
    if hr: print(f"{hr_color}{__hr}")


def printer_info(content: str, hr: bool = False) -> None:
    """
    信息级别内容
    """
    __printer(content=content, content_color=fp.info.value, hr=hr, hr_symbol="* ", hr_color=ffc.GREEN.value, hr_length=55)


def printer_warn(content: str, hr: bool = False) -> None:
    """
    警告级别内容
    """
    __printer(content=content, content_color=fp.warn.value, hr=hr, hr_symbol="~ ", hr_color=ffc.YELLOW.value, hr_length=55)


def printer_error(content: str, hr: bool = False) -> None:
    """
    错误级别内容
    """
    __printer(content=content, content_color=fp.error.value, hr=hr, hr_symbol="✘ ", hr_color=ffc.RED.value, hr_length=55)
