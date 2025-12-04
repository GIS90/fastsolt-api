# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe:
    App startup and shutdown tip
    Python Package：pyfiglet

base_info:
    __author__ = PyGo
    __time__ = 2025/11/28 23:02
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api
    __file_name__ = tip.py

usage:
    
design:
    第三方网站：https://patorjk.com/
    模块：Text to ASCII Art Generator

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
import pyfiglet
from deploy.utils.enumeration import (fontForeColor as ffc,
                                      fontBackColor as fbc)
from colorama import init
init(autoreset=True)


__all__ = [
    "tip_color_startup",
    "tip_color_shutdown"
]


# 显示的字符
__STARTUP_ASCII : str= """Server Run"""
__SHUTDOWN_ASCII : str= """Shutdown"""


# 字体配置
__FONT = "Slant"        # 字体
__JUSTIFY = "center"    # 对齐方式：auto left center right
___DIRECTION = "auto"   # 方向：auto left-to-right right-to-left

def __print_colored_ascii_art(text: str, color: str) -> None:
    """
    打印彩色ASCII艺术字

    参数:
        text (str): 要转换为ASCII艺术字的文本内容
        color (str): 应用于ASCII艺术字的颜色代码

    返回值:
        None: 该函数不返回任何值，仅执行打印操作
    """
    try:
        ascii_art = pyfiglet.figlet_format(
            text,
            font=__FONT,
            direction=___DIRECTION,
            justify=__JUSTIFY
        )
        print(color + ascii_art)
    except:
        pass


def tip_color_startup() -> None:
    __print_colored_ascii_art(__STARTUP_ASCII, ffc.LIGHT_CYAN_EX.value)


def tip_color_shutdown() -> None:
    __print_colored_ascii_art(__SHUTDOWN_ASCII, ffc.LIGHT_RED_EX.value)

