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
    """
    单例模式+ABC

    基于单例模式和抽象基类的Web基础类，确保全局只有一个实例，并提供抽象的入口点方法供子类实现。
    """
    _instance = None
    _instance_lock = threading.Lock()

    def __init__(self) -> None:
        super(WebBaseClass, self).__init__()
        # 使用标志位确保entry_point只执行一次
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self.entry_point()

    def __str__(self) -> str:
        return "WebBaseClass Class."

    def __repr__(self) -> str:
        return self.__str__()

    def __new__(cls, *args, **kwargs):
        # 双重检查锁定模式确保线程安全
        if cls._instance is None:
            with cls._instance_lock:
                if cls._instance is None:
                    cls._instance = object.__new__(cls)
        return cls._instance

    @abstractmethod
    def entry_point(self):
        """
        entry method
        """
        ...
