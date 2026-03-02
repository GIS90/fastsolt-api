# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    base curd class

base_info:
    __author__ = PyGo
    __time__ = 2026/3/2 22:09
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api
    __file_name__ = base_curd.py

usage:
    
design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
from abc import ABC, abstractmethod
from typing import Optional, List, Any
from sqlalchemy.ext.asyncio import AsyncSession


class BaseCurd(ABC):

    @staticmethod
    @abstractmethod
    async def new_model():
        ...

    @classmethod
    @abstractmethod
    async def get_count(cls, db: AsyncSession) -> int:
        ...

    @classmethod
    @abstractmethod
    async def get_pagination(
        cls, db: AsyncSession, offset: int = 0, limit: int = 15
    ) -> Optional[List]:
        ...

    @classmethod
    @abstractmethod
    async def add(
            cls, db: AsyncSession, model: Any
    ) -> None:
        ...

    @classmethod
    @abstractmethod
    async def update(
            cls, db: AsyncSession, model: Any
    ) -> None:
        ...

    @classmethod
    @abstractmethod
    async def delete(
            cls, db: AsyncSession, model: Any
    ) -> None:
        ...

