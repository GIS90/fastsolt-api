# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    api service

base_info:
    __author__ = PyGo
    __time__ = 2025/11/30 14:40
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api
    __file_name__ = api.py

usage:
    
design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""

class ApiService:
    """
    API Service
    """
    COLOR_ENUM = [
        'red'.upper(),
        'yellow'.lower(),
        'blue'.title(),
        'green'.capitalize()
    ]

    def __init__(self):
        """
        ApiService class initialize
        """
        super(ApiService, self).__init__()

    def __str__(self):
        print("ApiService class.")

    def __repr__(self):
        self.__str__()

    async def m1_case(self) -> dict:
        return {
            "route": "api",
            "module": "M1",
            "name": "m1>case",
            "data": self.COLOR_ENUM
        }

