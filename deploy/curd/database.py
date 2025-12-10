# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    db session

base_info:
    __author__ = PyGo
    __time__ = 2025/12/9 22:07
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api
    __file_name__ = _database.py

usage:
    
design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
import sys
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from deploy.config import env, db_link
from deploy.utils.printer import printer_error
from deploy.utils.logger import logger as LOG


# 数据库连接地址
_DB_LINK: str = db_link
if not _DB_LINK:
    printer_error(content="数据库连接地址空，系统退出！", hr=True)
    sys.exit(1)

# 根据环境决定是否开启SQL日志
_ECHO_SQL = True if env == "dev" else False

# 异步引擎
engine = create_async_engine(
    url=_DB_LINK,
    echo=_ECHO_SQL,
    future=True
)

# 异步会话工厂
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)

# 依赖注入：获取数据库会话
async def get_db():
    """
    异步获取数据库会话的依赖注入函数

    该函数用于FastAPI的依赖注入系统，提供数据库会话管理。
    它确保每次请求都能获得独立的数据库会话，并在操作完成后正确处理事务提交、回滚和会话关闭。

    Yields:
        AsyncSession: 异步数据库会话对象，用于执行数据库操作

    Raises:
        Exception: 当数据库操作过程中发生异常时，会自动回滚事务并重新抛出异常
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as exec:
            await session.rollback()
            LOG.error(f"{'=' * 10}数据库操作异常：{exec.__str__()}{'=' * 10}")
            raise
        finally:
            await session.close()

