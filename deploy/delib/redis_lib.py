# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe:
    redis lib

base_info:
    __author__ = PyGo
    __time__ = 2025/11/29 18:02
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api
    __file_name__ = redis_lib.py

usage:
    
design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
import redis
from typing import Optional
from contextlib import contextmanager


class RedisClientLib:
    """
    Redis客户端库类

    用于创建和管理Redis数据库连接的客户端库

    Args:
        host (str): Redis服务器主机地址
        port (int): Redis服务器端口号
        db (int): 要连接的数据库编号
        password (Optional[str]): Redis服务器密码，如果不需要密码则传入None
        decode_responses (bool): 是否自动解码响应数据，默认为True

    Returns:
        None
    """
    def __init__(self, host: str, port: int, db: int, password: Optional[str], decode_responses=True):
        self.HOST: str = host
        self.PORT: int = port
        self.DB: int = db
        self.PASSWORD: Optional[str] = password
        self.decode_responses: bool = decode_responses
        self._connection = None

    def __str__(self):
        return "RedisClientLib Class "

    def __repr__(self):
        return self.__str__()

    @property
    def connection(self):
        if not self._connection:
            try:
                self._connection = redis.StrictRedis(
                    host=self.HOST,
                    port=self.PORT,
                    db=self.DB,
                    password=self.PASSWORD,
                    decode_responses=self.decode_responses
                )
            except redis.RedisError as e:
                print(f"RedisClientLib create connect failed: {e}")

        return self._connection

    def close(self):
        if self._connection:
            self._connection.close()
            self._connection = None

    @contextmanager
    def get_connection(self):
        try:
            yield self.connection
        finally:
            # 如果需要，可以在这里进行清理工作，不过对于 Redis 连接通常不需要
            pass

    def set_key(self, key, value, ex=None, px=None, nx=False, xx=False):
        """Set the value at key ``name`` to ``value``"""
        with self.get_connection() as conn:
            return conn.set(key, value, ex, px, nx, xx)

    def get_key(self, key):
        """Return the value at key ``name``, or None if the key doesn't exist"""
        with self.get_connection() as conn:
            return conn.get(key)

    def delete_key(self, *keys):
        """Delete one or more keys specified by ``keys``"""
        with self.get_connection() as conn:
            return conn.delete(*keys)

    def expire_key(self, key, time):
        """Set an expiration on key ``name``. ``time`` can be repr'd as an int."""
        with self.get_connection() as conn:
            return conn.expire(key, time)

    def ttl_key(self, key):
        """Returns the remaining time to live of a key that has a timeout"""
        with self.get_connection() as conn:
            return conn.ttl(key)
