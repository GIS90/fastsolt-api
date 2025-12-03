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
    'fontForeColor',
    'fontBackColor',
    'fontStyle',
    'fontPrinter',
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
    BLACK = Fore.BLACK
    RED = Fore.RED
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    BLUE = Fore.BLUE
    MAGENTA = Fore.MAGENTA
    CYAN = Fore.CYAN
    WHITE = Fore.WHITE

    LIGHT_BLACK_EX = Fore.LIGHTBLACK_EX
    LIGHT_RED_EX = Fore.LIGHTRED_EX
    LIGHT_GREEN_EX = Fore.LIGHTGREEN_EX
    LIGHT_YELLOW_EX = Back.LIGHTYELLOW_EX
    LIGHT_BLUE_EX = Fore.LIGHTBLUE_EX
    LIGHT_MAGENTA_EX = Fore.LIGHTMAGENTA_EX
    LIGHT_CYAN_EX = Fore.LIGHTCYAN_EX
    LIGHT_WHITE_EX = Fore.LIGHTWHITE_EX

    RESET = Fore.RESET


@unique
class fontBackColor(Enum):
    """
    背景颜色
    """
    BLACK = Back.BLACK
    RED = Back.RED
    GREEN = Back.GREEN
    YELLOW = Back.YELLOW
    BLUE = Back.BLUE
    MAGENTA = Back.MAGENTA
    CYAN = Back.CYAN
    WHITE = Back.WHITE

    LIGHT_BLACK_EX = Back.LIGHTBLACK_EX
    LIGHT_RED_EX = Back.LIGHTRED_EX
    LIGHT_GREEN_EX = Back.LIGHTGREEN_EX
    LIGHT_YELLOW_EX = Back.LIGHTYELLOW_EX
    LIGHT_BLUE_EX = Back.LIGHTBLUE_EX
    LIGHT_MAGENTA_EX = Back.LIGHTMAGENTA_EX
    LIGHT_CYAN_EX = Back.LIGHTCYAN_EX
    LIGHT_WHITE_EX = Back.LIGHTWHITE_EX

    RESET = Back.RESET


@unique
class fontStyle(Enum):
    """
    字体样式
    """
    NORMAL = Style.NORMAL
    BRIGHT = Style.BRIGHT
    DIM = Style.DIM


@unique
class fontPrinter(Enum):
    """
    字体样式
    """
    info = fontForeColor.BLUE.value + fontStyle.NORMAL.value
    warn = fontForeColor.LIGHT_YELLOW_EX.value + fontBackColor.BLUE.value
    error = fontForeColor.LIGHT_RED_EX.value + fontBackColor.WHITE.value
