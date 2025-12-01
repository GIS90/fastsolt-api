# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    base class

base_info:
    __author__ = PyGo
    __time__ = 2025/11/25 21:48
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api
    __file_name__ = base_class.py

usage:
    
design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
import threading
from abc import ABC, abstractmethod


class WebBaseClass(ABC):
    """单例模式+ABC"""
    _instance = None
    _instance_lock = threading.Lock()

    def __init__(self):
        super(WebBaseClass, self).__init__()
        self.entry_point()

    def __str__(self):
        return "WebBaseClass Class."

    def __repr__(self):
        return self.__str__()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with WebBaseClass._instance_lock:
                cls._instance = object.__new__(cls)
        return cls._instance

    @abstractmethod
    def entry_point(self):
        pass
