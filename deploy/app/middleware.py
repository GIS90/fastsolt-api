# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    middleware

base_info:
    __author__ = PyGo
    __time__ = 2025/11/25 21:52
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api
    __file_name__ = middleware.py

usage:
    
design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
import time
from typing import List
from fastapi import FastAPI, Request, status as fastapi_http_status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.sessions import SessionMiddleware

from deploy.utils.status_value import StatusMsg as status_msg, \
    StatusCode as status_code
from deploy.utils.status import FailureStatus
from deploy.utils.enumeration import MediaType
from deploy.utils.logger import logger as LOG
from deploy.config import (app_secret_key, app_allow_host, app_cors_origin, app_ban_router,
                           app_session_max_age, app_request_method, app_gzip_size, app_gzip_level)
from deploy.utils.token import verify_access_token_expire


#- - - - - - - - - - - - - - - - - - - - - - - - - - - -
__APP_SECRET_KEY: str = app_secret_key
__APP_ALLOW_HOST: List[str] = app_allow_host
__APP_CORS_ORIGIN: List[str] = app_cors_origin or ["*"]  # 全部：["*"]
__APP_BAN_ROUTER: List[str] = app_ban_router
__APP_SESSION_MAX_AGE: int = app_session_max_age or 24 * 60 * 60    # 单位：秒
__APP_REQUEST_METHOD: List[str] = app_request_method
__APP_GZIP_SIZE: int = app_gzip_size
__APP_GZIP_LEVEL: int = app_gzip_level
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -


def register_app_middleware(app: FastAPI, app_headers: dict):
    """
    App中间件
    """

    # app middleware
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
    """
    自定义中间件C-Middleware:
        - 访问IP检查
        - 资源请求地址检查
        - 请求方法检查
        - Jwt Token验证
    """
    @app.middleware("http")
    async def cmAccess(request: Request, call_next):
        LOG.debug(">>>>> App middleware C-Middleware request")
        __is_verify_token = True  # 是否验证Jwt Token有效性[默认验证]，设置False跳过jwt token验证
        __token_rtx_id = None     # 用户token-rtx-id

        # - - - - - - - - - - - - - - - - 请求代码块 - - - - - - - - - - - - - - - -
        # [** 访问IP检查 **]
        if __APP_ALLOW_HOST and \
                request.client.host not in __APP_ALLOW_HOST:
            content = FailureStatus(
                status_id=status_code.CODE_10001_BAN_REQUEST.value,
                message=f"IP not allow access: {request.client.host}"
            ).status_body
            headers = {"X-App-CM-Request-Webhook": "CM-IP"}
            headers.update(app_headers)
            return JSONResponse(
                content=content,
                status_code=fastapi_http_status.HTTP_200_OK,
                headers=headers,
                media_type=MediaType.APPJson.value
            )

        # [** 资源请求地址检查 **]
        if __APP_BAN_ROUTER and \
                request.url.path in __APP_BAN_ROUTER:
            content = FailureStatus(
                status_id=status_code.CODE_10001_BAN_REQUEST.value,
                message=f"Request resource is forbid: {request.url.path}"
            ).status_body
            headers = {"X-App-CM-Request-Webhook": "CM-ROUTE"}
            headers.update(app_headers)
            return JSONResponse(
                content=content,
                status_code=fastapi_http_status.HTTP_200_OK,
                headers=headers,
                media_type=MediaType.APPJson.value
            )

        # [** 请求方法 **]
        if __APP_REQUEST_METHOD and \
                str(request.method).upper() not in __APP_REQUEST_METHOD:
            content = FailureStatus(
                status_id=status_code.CODE_300_REQUEST_METHOD_ERROR.value,
                message=f"Request method is error: {request.url.path}"
            ).status_body
            headers = {"X-App-CM-Request-Webhook": "CM-METHOD"}
            headers.update(app_headers)
            return JSONResponse(
                content=content,
                status_code=fastapi_http_status.HTTP_200_OK,
                headers=headers,
                media_type=MediaType.APPJson.value
            )

        # [** Jwt Token验证 **]
        # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
        """
        通过请求Headers获取X-Token、X-Rtx-Id信息，验证用户是否Token有效性
        注意：Header请求参数KEY需要采用[驼峰+中划线]方法命令
        """
        """
        no check jwt token request condition
          - api: rest open apis, special api for blueprints
          - access: login in and login out APIs
        """
        if request.url.path == "/" or \
                request.url.path.startswith("/api/") or \
                request.url.path.startswith("/access/"):
            __is_verify_token = False

        if __is_verify_token:
            request_token = request.headers.get('X-Token')
            headers = {"X-App-CM-Request-Webhook": "CM-TOKEN"}
            headers.update(app_headers)
            # NO Token
            if not request_token:
                content = FailureStatus(
                    status_id=status_code.CODE_250_TOKEN_NOT_FOUND.value,
                    message=status_msg.get(250)
                ).status_body
                return JSONResponse(
                    content=content,
                    status_code=fastapi_http_status.HTTP_200_OK,
                    headers=headers,
                    media_type=MediaType.APPJson.value
                )
            # Token expire
            expire, __token_rtx_id = verify_access_token_expire(x_token=request_token)
            if expire:
                content = FailureStatus(
                    status_id=status_code.CODE_253_TOKEN_EXPIRE.value,
                    message=status_msg.get(253)
                ).status_body
                return JSONResponse(
                    content=content,
                    status_code=fastapi_http_status.HTTP_200_OK,
                    headers=headers,
                    media_type=MediaType.APPJson.value
                )
        # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

        LOG.debug(">>>>> App middleware C-Middleware response")
        # + + + + + + + + + + + + + + + + 响应代码块 + + + + + + + + + + + + + + + +
        # [API Watcher执行时间]
        start = time.time()
        response = await call_next(request)
        end = time.time()
        cost = end - start

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
        """ 
        [watcher]
        > [ 在CM中对有Token请求的进行了watcher request ]
        > access在方法中直接调用user_service.request
        > APIs做成装饰器进行watcher request
        """
        if __is_verify_token:
            pass
            # 验证用户可用性
            '''
            from deploy.service.user import UserService
            user_service = UserService()
            await user_service.request(rtx_id=__token_rtx_id, request_body=request, cost=cost)
            '''
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

        response.headers["X-App-CM-Timer"] = str(cost)
        response.headers["X-App-CM-Response-Webhook"] = "C-Middleware-Timer"
        for _k, _v in app_headers.items():
            if not _k: continue
            response.headers[_k] = _v

        LOG.debug("<<<<< App middleware C-Middleware response")
        LOG.debug("<<<<< App middleware C-Middleware request")

        return response

    # 中间件 > CORS跨域
    app.add_middleware(
        CORSMiddleware,
        allow_origins=__APP_CORS_ORIGIN,
        allow_credentials=True,  # 认证
        allow_methods=__APP_REQUEST_METHOD,     # 方法
        allow_headers=["*"]      # Headers信息
    )

    # 中间件 > SESSION会话管理
    app.add_middleware(
        SessionMiddleware,
        secret_key=__APP_SECRET_KEY,
        session_cookie="session",
        max_age=__APP_SESSION_MAX_AGE
    )

    # 中间件 > HTTPSRedirectMiddleware(强制所有传入请求必须是 https 或 wss)
    """
    self.app.add_middleware(HTTPSRedirectMiddleware)
    """

    # 中间件 > GZip
    app.add_middleware(
        GZipMiddleware,
        minimum_size=__APP_GZIP_SIZE,   # default 500byte
        compresslevel=__APP_GZIP_LEVEL  # default 9
    )
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
