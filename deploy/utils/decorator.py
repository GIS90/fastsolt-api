# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe:
    decorator, use to function

base_info:
    __author__ = PyGo
    __time__ = 2025/11/29 21:47
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api
    __file_name__ = decorator.py

usage:
    @decorator
    def function():
        pass

design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
from typing import Any
from datetime import datetime
from functools import wraps

from deploy.utils.status import FailureStatus
from deploy.utils.logger import logger as LOG
from deploy.utils.status_value import (StatusMsg as status_msg,
                                       StatusCode as status_code)
# ～ ～ ～ ～ ～ ～ ～ ～ ～ ～ ～ ～ ～ ～ ～ ～ ～ ～ ～ ～ ～ ～ ～ ～ ～ ～ ～ ～ ～ ～ ～ ～ ～ ～ ～
"""
装饰器模板
"""


def decorator(func):
    """
    装饰器功能描述
    """
    @wraps(func)
    async def __wrapper(*args: Any, **kwargs: Any):
        # 额外功能
        result = await func(*args, **kwargs)
        # 额外功能
        LOG.info("[Decorator] >>>>> %s." % func.__name__)
        return result
    return __wrapper
# ～ ～ ～ ～ ～ ～ ～ ～ ～ ～ ～ ～ ～ ～ ～ ～ ～ ～ ～ ～ ～ ～ ～ ～ ～ ～ ～ ～ ～ ～ ～ ～ ～ ～ ～


# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
def timer(func):
    """
    方法执行时间装饰器
    """
    @wraps(func)
    async def __wrapper(*args: Any, **kwargs: Any):
        start_time = datetime.now()
        result = await func(*args, **kwargs)
        end_time = datetime.now()
        cost = round((end_time - start_time).microseconds * pow(0.1, 6), 3)
        LOG.info("[Decorator>Timer] >>>>> %s cost %s seconds." % (func.__name__, cost))
        return result
    return __wrapper


# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
def debug(func):
    """
    debug装饰器
    """
    @wraps(func)
    async def __wrapper(*args: Any, **kwargs: Any):
        LOG.info("[Decorator>Debugging] >>>>> %s - args: %s, kwargs: %s" % (func.__name__, args, kwargs))
        return await func(*args, **kwargs)
    return __wrapper


# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
def deprecated(func):
    """
    方法过时提示
    """
    @wraps(func)
    async def __wrapper(*args: Any, **kwargs: Any):
        LOG.warn("[Decorator>deprecated] %s is deprecated and will be removed in future versions." % func.__name__, DeprecationWarning)
        return await func(*args, **kwargs)
    return __wrapper


# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
def watch_except(func):
    """
    异常处理
    """
    @wraps(func)
    async def __wrapper(*args: Any, **kwargs: Any):
        try:
            return await func(*args, **kwargs)
        except Exception as error:
            LOG.error(f"{func.__name__} is error: {error}")
            return FailureStatus(
                status_code.CODE_900_SERVER_API_EXCEPTION.value,
                status_msg.get(900),
                {"error": str(error)}
            ).status_body

    return __wrapper


# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *


