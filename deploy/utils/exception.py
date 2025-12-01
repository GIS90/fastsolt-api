# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    custom exception class

base_info:
    __author__ = PyGo
    __time__ = 2025/11/29 09:26
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api
    __file_name__ = exception.py

usage:
    
design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""

__all__ = [
    "JwtCredentialsException",
    "UserInValidateException"
]


class JwtCredentialsException(Exception):
    """
    jwt验证异常类
    """
    def __init__(self, detail):
        self.detail = detail

    def __str__(self):
        return "JwtCredentialsException Class."

    def __repr__(self):
        return self.__str__()

    def report(self):
        return f"JwtCredentialsException: {self.detail}"


class UserInValidateException(Exception):
    """
    user不可用异常类
    - 不存在
    - 已注销
    """
    def __init__(self, detail):
        self.detail = detail

    def __str__(self):
        return "UserInValidateException Class."

    def __repr__(self):
        return self.__str__()

    def report(self):
        return f"UserInValidateException: {self.detail}"
