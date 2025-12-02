# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    enum module

base_info:
    __author__ = PyGo
    __time__ = 2025/11/29 09:11
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api
    __file_name__ = enum.py

usage:
    
design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
from enum import Enum, unique
from colorama import Fore, Back, Style


__all__ = [
    'MediaType',
]


@unique
class MediaType(Enum):
    """
    HTTP协议数据类型
    """
    TextPlain = "text/plain"
    TextHtml = "text/html"
    TextXml = "text/xml"
    TextMarkDown = "text/x-markdown"

    ImageGif = "image/gif"
    ImageJpg = "image/jpg"
    ImagePng = "image/png"

    APPXHtml = "application/xhtml"
    APPXml = "application/xml"
    APPJson = "application/json"
    APPPdf = "application/pdf"
    APPWord = "application/msword"
    APPStream = "application/octet-stream"
    APPForm = "application/x-www-form-urlencoded"

    MulForm = "multipart/form-data"


@unique
class fontForeColor(Enum):
    """
    字体颜色
    """
    black = Fore.BLACK
    red = Fore.RED
    green = Fore.GREEN
    yellow = Fore.YELLOW
    blue = Fore.BLUE
    magenta = Fore.MAGENTA
    cyan = Fore.CYAN
    white = Fore.WHITE

    light_black_ex = Fore.LIGHTBLACK_EX
    light_red_ex = Fore.LIGHTRED_EX
    light_green_ex = Fore.LIGHTGREEN_EX
    light_yellow_ex = Back.LIGHTYELLOW_EX
    light_blue_ex = Fore.LIGHTBLUE_EX
    magenta_ex = Fore.LIGHTMAGENTA_EX
    cyan_ex = Fore.LIGHTCYAN_EX
    white_ex = Fore.LIGHTWHITE_EX

    reset = Fore.RESET


@unique
class fontBackColor(Enum):
    """
    背景颜色
    """
    black = Back.BLACK
    red = Back.RED
    green = Back.GREEN
    yellow = Back.YELLOW
    blue = Back.BLUE
    magenta = Back.MAGENTA
    cyan = Back.CYAN
    white = Back.WHITE

    light_black_ex = Back.LIGHTBLACK_EX
    light_red_ex = Back.LIGHTRED_EX
    light_green_ex = Back.LIGHTGREEN_EX
    light_yellow_ex = Back.LIGHTYELLOW_EX
    light_blue_ex = Back.LIGHTBLUE_EX
    magenta_ex = Back.LIGHTMAGENTA_EX
    cyan_ex = Back.LIGHTCYAN_EX
    white_ex = Back.LIGHTWHITE_EX

    reset = Back.RESET


@unique
class fontStyle(Enum):
    """
    字体样式
    """
    normal = Style.NORMAL
    bright = Style.BRIGHT
    dim = Style.DIM


@unique
class fontPrinter(Enum):
    """
    字体样式
    """
    info = fontForeColor.blue.value + fontStyle.normal.value
    warn = fontForeColor.yellow.value + fontBackColor.cyan.value + fontStyle.bright.value
    error = fontForeColor.red.value + fontBackColor.white.value + fontStyle.bright.value
