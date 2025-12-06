# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    App

base_info:
    __author__ = PyGo
    __time__ = 2025/11/25 21:46
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api
    __file_name__ = __init__.py

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

from fastapi import FastAPI, APIRouter
from starlette.staticfiles import StaticFiles

from deploy.view import add_routers
from deploy.app.exception import register_app_exception    # app exception handle
from deploy.app.middleware import register_app_middleware  # app middleware
from deploy.app.tip import tip_color_startup, tip_color_shutdown    # app startup and shutdown tip

from deploy.utils.base_class import WebBaseClass
from deploy.utils.logger import logger as LOG
from deploy.config import (server_name, server_version,
                           app_openapi_url, app_docs_url,
                           app_static_url, app_static_folder,
                           APPProfile, _author_contact)


# FastAPI App instance
__app: FastAPI = FastAPI(
    # Docs配置[str类型，设置None为禁用状态]
    openapi_url=app_openapi_url,
    docs_url=app_docs_url,
    redoc_url=None  # 禁用redoc_url
)


class FSWebAppClass(WebBaseClass):
    app = None

    def __init__(self, app):
        """
        class initialize
        :param app: FastAPI App instance
        """
        self.app = app
        self.headers = {"app": "FSWebAppClass"}     # 初始化Headers
        if not self.app:
            LOG.critical('Web App server initialize is failure, exit......')
            sys.exit(1)

        # APP object configuration
        # ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ -
        # APP简介
        self.app.title = APPProfile.title
        self.app.version = APPProfile.version
        self.app.summary = APPProfile.summary
        self.app.description = APPProfile.description
        # 作者
        if _author_contact:
            self.app.contact = _author_contact

        # 静态资源
        self.app.mount(path=app_static_url, app=StaticFiles(directory=app_static_folder), name="static")
        # ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ -

        # app middleware
        # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
        register_app_middleware(app=app, app_headers=self.headers)
        # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

        # app webhook: exception_handler
        # -----------------------------------------------------------------------------------------------
        register_app_exception(app=app, app_headers=self.headers)
        # -----------------------------------------------------------------------------------------------

        # FSWebAppClass initialize
        super(FSWebAppClass, self).__init__()

        @app.on_event("startup")
        async def startup_event():
            LOG.info('>>>>> Web app startup success......')
            tip_color_startup()

        @app.on_event("shutdown")
        async def shutdown_event():
            LOG.info('>>>>> Web app shutdown success......')
            tip_color_shutdown()

    def __str__(self):
        return "FSWebAppClass instance."

    def register_blueprint(self, router: APIRouter):
        """
        register router
        :param router: route object
            contain prefix, tags, response and so on...
        :return: None
        """
        if router:
            __route_prefix = "/root" if router.prefix == "" else router.prefix
            LOG.info(f'Blueprint [{__route_prefix}] is register')
            self.app.include_router(router)

    def __auto_register_blueprint(self):
        for route in add_routers:
            if not route: continue
            self.register_blueprint(router=route)

    def entry_point(self):
        """
        web app initialize
        :return: None
        """
        LOG.info('Web app server start initialize......')
        self.__auto_register_blueprint()
        LOG.info('Web app server end initialize......')


def __create_app():
    return FSWebAppClass(__app).app


app = __create_app()
