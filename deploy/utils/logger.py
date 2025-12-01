# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    record system information
    level: debug, info, warning, error, critical

    CRITICAL 50
    ERROR 40
    WARNING 30
    INFO 20
    DEBUG 10

base_info:
    __author__ = PyGo
    __time__ = 2025/11/26 22:19
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api
    __file_name__ = logger.py

usage:
    logger.debug('message')
    logger.info('message')
    logger.warning('message')
    logger.error('message')
    logger.critical('message')

formatter：
    属性名	    格式	            描述
    name	    %(name)s	    Logger名称
    levelno	    %(levelno)s	    数字日志级别
    levelname	%(levelname)s	文本日志级别
    pathname	%(pathname)s	完整路径名
    filename	%(filename)s	文件名
    module	    %(module)s	    模块名
    lineno	    %(lineno)d	    行号
    funcName	%(funcName)s	函数名
    created	    %(created)f	    创建时间（UNIX时间戳）
    asctime	    %(asctime)s	    可读时间
    msecs	    %(msecs)d	    毫秒部分
    message	    %(message)s	    日志消息

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

remarks:
    everyone file allow to import and to use
------------------------------------------------
"""
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from pathlib import Path
from deploy.config import (log_folder, log_prefix, log_format,
                           log_level, log_count, log_max_size)


level: str = log_level
formatter: str = log_format
filename_prefix: str = log_prefix
__max_size: int = log_max_size or 10 * 1024 * 1024  # 无配置默认10M
__count: int = log_count or 10
__log_encode: str = "utf-8"     # 日志编码

LEVEL = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}

logger = logging.getLogger(__name__)


def __current_folder() -> Path:
    return Path(__file__).parent.resolve()


def __deploy_folder() -> Path:
    return __current_folder().parent.resolve()


def __root_folder() -> Path:
    return __deploy_folder().parent.resolve()


def __get_now(__format="%Y-%m-%d %H:%M:%S") -> str:
    return datetime.strftime(datetime.now(), __format)


## 目录
__log_folder_path: Path = Path(log_folder)
__log_folder_abs: Path = __root_folder().joinpath(log_folder) if not __log_folder_path.is_absolute() \
    else __log_folder_path.resolve()
if not __log_folder_abs.exists():
    # If log folder not exists, create it
    __log_folder_abs.mkdir(parents=True)

# 格式
if not log_format:
    formatter = '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s - %(message)s'
__log_formatter = logging.Formatter(formatter,
                                    datefmt='%Y/%m/%d %H:%M:%S')

# 级别
__log_level = LEVEL.get(level or 'info')
logger.setLevel(level=__log_level)

# 定义一个RotatingFileHandler，最多备份10个日志文件，每个日志文件最大10M
__log_name: str = filename_prefix + '-' + __get_now(__format="%Y-%m-%d") \
    if filename_prefix and filename_prefix != '-' else __get_now(__format="%Y-%m-%d")
__log_file = __log_folder_abs.joinpath(f"{__log_name}.log")
file_handler = RotatingFileHandler(__log_file,
                                   mode='a',
                                   maxBytes=__max_size,
                                   backupCount=__count,
                                   encoding=__log_encode)
file_handler.setLevel(__log_level)
file_handler.setFormatter(__log_formatter)
logger.addHandler(file_handler)
# 控制台
stream_handler = logging.StreamHandler()
stream_handler.setLevel(__log_level)
stream_handler.setFormatter(__log_formatter)
logger.addHandler(stream_handler)
