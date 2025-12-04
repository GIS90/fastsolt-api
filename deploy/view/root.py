# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    root view

base_info:
    __author__ = PyGo
    __time__ = 2025/11/25 21:54
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api
    __file_name__ = root.py

usage:
    
design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
from fastapi import APIRouter, status as fastapi_http_status
from fastapi.responses import HTMLResponse
from deploy.config import app_docs_url, server_name, server_version


# define view
root: APIRouter = APIRouter(prefix="", tags=["首页"])


@root.get('/',
          summary="Welcome to Fastslot-API脚手架",
          description="Hello Fastslot-API脚手架!",
          status_code=fastapi_http_status.HTTP_200_OK
          )
async def hi() -> HTMLResponse:
    """
    :return: HTMLResponse
    """
    return HTMLResponse(
        content='''
            <h1 style="color:red">欢迎访问%s脚手架🚀🚀🚀🚀🚀🚀</h1>
            <hr>
            <h2>版本：%s</h2>
            <h2>API文档说明请访问：<a href="%s">%s</a></h2>
            <h2>有问题请联系作者，邮箱：gaoming971366@163.com</h2>
            <hr>
            <h2 style="font-style: italic;color:blue">Enjoy the good life everyday！！!</h2>
        ''' % (server_name, server_version, app_docs_url, app_docs_url),
        status_code=fastapi_http_status.HTTP_200_OK,
        headers={'X-Token': "I'm is token%s" % ("." * 33)}
    )
