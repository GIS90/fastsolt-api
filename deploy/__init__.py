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
from typing import Any
from fastapi import FastAPI, APIRouter
from starlette.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html

from deploy.view import add_routers
from deploy.app.exception import register_app_exception    # app exception handle
from deploy.app.middleware import register_app_middleware  # app middleware
from deploy.app.tip import tip_color_startup, tip_color_shutdown    # app startup and shutdown tip

from deploy.utils.base_class import WebBaseClass
from deploy.utils.logger import logger as LOG
from deploy.config import (app_openapi_url, app_docs_url,
                           app_static_url, app_static_folder,
                           APPProfile, _author_contact)


# FastAPI App instance
__app: FastAPI = FastAPI(
    openapi_url=app_openapi_url,
    # Docs配置[str类型，设置None为禁用状态]
    docs_url=None,  # 重定向
    redoc_url=None  # 禁用redoc_url
)


class FSWebAppClass(WebBaseClass):

    def __init__(self, app: Any):
        """
        class initialize
        :param app: FastAPI App instance
        """
        self.app = app
        self.headers = {"app": "FSWebAppClass"}     # 初始化Headers
        if not self.app:
            LOG.critical('Web App server initialize is failure, exit......')
            sys.exit(1)

        # APP configuration
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
        # ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ -
        self.app.mount(path=app_static_url, app=StaticFiles(directory=app_static_folder), name="static")

        # 配置本地Swagger UI资源
        @self.app.get(app_docs_url, include_in_schema=False)
        async def __swagger_ui_html():
            return get_swagger_ui_html(
                openapi_url=app_openapi_url,
                title=f"{APPProfile.title}-{APPProfile.version}-接口说明手册",
                swagger_js_url=f"{app_static_url}/swagger-ui-bundle.js",
                swagger_css_url=f"{app_static_url}/swagger-ui.css",
                swagger_favicon_url=f"{app_static_url}/favicon.ico"
            )
        # ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ - ~ -

        # app middleware
        # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
        register_app_middleware(app=self.app, app_headers=self.headers)
        # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

        # app webhook: exception_handler
        # -----------------------------------------------------------------------------------------------
        register_app_exception(app=self.app, app_headers=self.headers)
        # -----------------------------------------------------------------------------------------------

        # FSWebAppClass initialize
        super(FSWebAppClass, self).__init__()

        @self.app.on_event("startup")
        async def startup_event():
            LOG.info('>>>>> Web app startup success......')
            tip_color_startup()

        @self.app.on_event("shutdown")
        async def shutdown_event():
            LOG.info('>>>>> Web app shutdown success......')
            tip_color_shutdown()

    def __str__(self) -> str:
        return """
        FSWebAppClass instance.
        WebApp project class, use to run APIs.
        contain middleware, exceptions, and tips for the app.
        """

    def __repr__(self) -> str:
        return self.__str__()

    def register_router(self, router: APIRouter):
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

    def __auto_register_router(self):
        for route in add_routers:
            if not route: continue
            self.register_router(router=route)

    def entry_point(self) -> None:
        """
        Web app initialize, parent class method
        :return: None
        """
        LOG.info('Web app server start initialize......')
        self.__auto_register_router()
        LOG.info('Web app server end initialize......')


def __create_app():
    return FSWebAppClass(__app).app


app = __create_app()
