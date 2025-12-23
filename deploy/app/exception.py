# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    App exception handler

base_info:
    __author__ = PyGo
    __time__ = 2025/11/25 21:52
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api
    __file_name__ = exception.py

usage:
    
design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
from typing import Dict
from fastapi import (FastAPI, Request,
                     status as fastapi_http_status,
                     HTTPException as FastAPI_HTTPException)
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from deploy.utils.status_value import (StatusMsg as status_msg,
                                       StatusCode as status_code)
from deploy.utils.status import FailureStatus
from deploy.utils.exception import (JwtCredentialsException,
                                    UserInvalidException,
                                    SQLDBHandleException)
from deploy.utils.enumeration import MediaType
from deploy.utils.logger import logger as LOG


def register_app_exception(app: FastAPI, app_headers: Dict):
    """
    注册应用程序中的全局异常处理器，用于捕获并统一处理不同类型的异常。

    :param app: FastAPI 应用实例，用于注册异常处理器。
    :param app_headers: 字典类型，包含需要在响应中附加的公共头部信息。
    """

    # RequestValidationError[请求参数验证错误]
    @app.exception_handler(RequestValidationError)
    async def request_validation_handle(request: Request, exec: RequestValidationError):
        """
        :param request: Request
        :param exec: RequestValidationError
        :return: JSONResponse
        """
        LOG.error(f"请求地址{request.url.__str__()}，[request_validation_handle]: {exec.errors()}")

        # rewrite response >>> 加入请求体body
        content = FailureStatus(
            status_id=status_code.CODE_404_REQUEST_PARAMETER_VALUE_ERROR.value,
            message="请求参数错误" or status_msg.get(404),
            data=jsonable_encoder(exec.errors())  # jsonable_encoder({"error": exec.errors(), "body": exec.body})   # 返回请求体参数 + errors
        ).status_body
        headers = {"app-cm-exception-webhook": "RequestValidationError"}
        headers.update(app_headers)
        return JSONResponse(
            content=content,
            status_code=fastapi_http_status.HTTP_200_OK,
            headers=headers,
            media_type=MediaType.APPJson.value
        )

    # JwtCredentialsException[Jwt Token验证异常]
    @app.exception_handler(JwtCredentialsException)
    async def jwt_exception_handler(request: Request, exec: JwtCredentialsException):
        """
        :param request: Request
        :param exec: JwtCredentialsException
        :return: JSONResponse
        """
        LOG.error(f"请求地址{request.url.__str__()}，[jwt_exception_handler]: {exec.__str__()}")

        # rewrite response
        content = FailureStatus(
            status_id=status_code.CODE_251_TOKEN_VERIFY_FAILURE.value,
            message=status_msg.get(251),
            data={"error": exec.detail}
        ).status_body
        headers = {"app-cm-exception-webhook": "JwtCredentialsException"}
        headers.update(app_headers)
        return JSONResponse(
            content=content,
            status_code=fastapi_http_status.HTTP_200_OK,
            headers=headers,
            media_type=MediaType.APPJson.value
        )

    # UserInvalidException[用户不可用验证异常]
    @app.exception_handler(UserInvalidException)
    async def user_invalid_exception_handler(request: Request, exec: UserInvalidException):
        """
        :param request: Request
        :param exec: UserInvalidException
        :return: JSONResponse
        """
        LOG.error(f"请求地址{request.url.__str__()}，[user_invalid_exception_handler]: {exec.__str__()}")

        # rewrite response
        content = FailureStatus(
            status_id=status_code.CODE_207_USER_INVALID.value,
            message=status_msg.get(207),
            data={"error": exec.detail}
        ).status_body
        headers = {"app-cm-exception-webhook": "UserInvalidException"}
        headers.update(app_headers)
        return JSONResponse(
            content=content,
            status_code=fastapi_http_status.HTTP_200_OK,
            headers=headers,
            media_type=MediaType.APPJson.value
        )

    # SQLDBHandleException[数据库操作异常]
    @app.exception_handler(SQLDBHandleException)
    async def db_exception_handler(request: Request, exec: SQLDBHandleException):
        """
        :param request: Request
        :param exec: SQLDBHandleException
        :return: JSONResponse
        """
        LOG.error(f"请求地址{request.url.__str__()}，[db_exception_handler]: {exec.__str__()}")

        # rewrite response
        content = FailureStatus(
            status_id=status_code.CODE_600_DB_EXCEPTION.value,
            message=status_msg.get(600),
            data={"error": exec.detail}
        ).status_body
        headers = {"app-cm-exception-webhook": "SQLDBHandleException"}
        headers.update(app_headers)
        return JSONResponse(
            content=content,
            status_code=fastapi_http_status.HTTP_200_OK,
            headers=headers,
            media_type=MediaType.APPJson.value
        )

    # FastAPI-HTTPException[HTTP异常]
    @app.exception_handler(FastAPI_HTTPException)
    async def fastapi_http_exception_handler(request: Request, exec: FastAPI_HTTPException):
        """
        :param request: Request
        :param exec: FastAPI HTTPException
        :return: JSONResponse
        """
        LOG.error(f"请求地址{request.url.__str__()}，[fastapi_http_exception_handler]: {exec.__str__()}")

        # rewrite response
        content = FailureStatus(
            status_id=status_code.CODE_901_HTTP_EXCEPTION.value,
            message=status_msg.get(901),
            data={"error": exec.__str__()}
        ).status_body
        headers = {"app-cm-exception-webhook": "FastAPI-HTTPException"}
        headers.update(app_headers)
        return JSONResponse(
            content=content,
            status_code=fastapi_http_status.HTTP_200_OK,
            headers=headers,
            media_type=MediaType.APPJson.value
        )

    # [Exception验证异常]
    @app.exception_handler(Exception)
    async def all_exception_handler(request: Request, exec: Exception):
        """
        :param request: Request
        :param exec: Exception
        :return: JSONResponse
        """
        LOG.error(f"请求地址{request.url.__str__()}，[all_exception_handler]: {exec.__str__()}")

        # rewrite response
        content = FailureStatus(
            status_id=status_code.CODE_900_SERVER_API_EXCEPTION.value,
            message=status_msg.get(900),
            data={"error": exec.__str__()}
        ).status_body
        headers = {"app-cm-exception-webhook": "Exception"}
        headers.update(app_headers)
        return JSONResponse(
            content=content,
            status_code=fastapi_http_status.HTTP_200_OK,
            headers=headers,
            media_type=MediaType.APPJson.value
        )
