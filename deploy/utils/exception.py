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
from sqlalchemy.exc import SQLAlchemyError


__all__ = [
    "JwtCredentialsException",
    "UserInvalidException",
    "SQLDBHandleException"
]


class JwtCredentialsException(Exception):
    """
    Jwt验证异常类
    """
    def __init__(self, detail):
        super().__init__(detail)
        self.detail = detail

    def __str__(self):
        return self.report()

    def __repr__(self):
        return self.report()

    def report(self):
        return f"JwtCredentialsException: {self.detail}"


class UserInvalidException(Exception):
    """
    用户不可用异常类
    - 不存在
    - 已注销
    """
    def __init__(self, detail):
        self.detail = detail

    def __str__(self):
        return self.report()

    def __repr__(self):
        return self.report()

    def report(self):
        return f"UserInvalidException: {self.detail}"


class SQLDBHandleException(SQLAlchemyError):
    """
    Sqlalchemy数据库操作异常类
    """
    def __init__(self, detail):
        self.detail = detail

    def __str__(self):
        return self.report()

    def __repr__(self):
        return self.report()

    def report(self):
        return f"SQLDBHandleException: {self.detail}"
