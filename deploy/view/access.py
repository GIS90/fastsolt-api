# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    access view
    
base_info:
    __author__ = PyGo
    __time__ = 2025/11/30 14:47
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api
    __file_name__ = access.py

usage:
    
design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
from fastapi import (APIRouter,
                     Depends, Query, Header,
                     HTTPException as FASTAPI_HTTPException,
                     status as fastapi_http_status)
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from deploy.schema.po.access import TokenBody as Token, O2LUserLogin
from deploy.utils.status import Status, SuccessStatus, FailureStatus
from deploy.utils.status_value import (StatusCode as status_code,
                                       StatusMsg as status_msg)
from deploy.utils.token import encode_access_token, decode_access_token_rtx
from deploy.delib.redis_lib import RedisClientLib
from deploy.config import redis_host, redis_port, redis_db, redis_password
from deploy.utils.exception import JwtCredentialsException


# router
router: APIRouter = APIRouter(prefix="/access", tags=["JWT Token系统验证"])


# ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ *
"""
JWT Token地址配置
    > 方式一：OAuth2PasswordRequestForm组件表单：token_request_o_form
    > 方式二：From表单：token_request_form
    > 方式三：Request请求体：token 

线上API采用第三种方式设置oauth2_schema对象的token-url
如果是Docs API文档验证模式，需要采用OAuth2PasswordRequestForm组件表单认证
"""
# 配置API oauth2_schema认证
oauth2_schema = OAuth2PasswordBearer(
    tokenUrl="/access/token_request_o_form"
)

credentials_exception = FASTAPI_HTTPException(
    fastapi_http_status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


@router.post("/token_request_o_form",
             response_model=Token,
             summary="用户Token API[OAuth2PasswordRequestForm组件表单] > Demo代码",
             description="依据用户[OAuth2PasswordRequestForm组件表单]提供的username，password参数（KEY不可更改），获取用户登录Token"
             )
async def access_token_request_o_form(
        form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm)
) -> Status:
    """
    用户Token API
    :param form_data: OAuth2PasswordRequestForm组件表单
    :return: dict
    """
    username = getattr(form_data, "username", None)
    password = getattr(form_data, "password", None)
    if not username or not password:
        return FailureStatus(
            code=status_code.CODE_204_LOGIN_USER_PASSWORD_ERROR.value
        )

    # TODO 用户校验 密码校验
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # = = = = = = = = = = = = = = = = start token = = = = = = = = = = = = = = = =
    token = encode_access_token(rtx_id=username)
    # = = = = = = = = = = = = == = = = end token = = = = = == = = = = = = = = = =
    return SuccessStatus(
        data={"access_token": token, "token_type": "Bearer"}
    )


@router.post("/token_request_form",
             response_model=Token,
             summary="用户Token API[Form表单] > Demo代码",
             description="依据用户[Form表单]提供的username，password参数（KEY不可更改），获取用户登录Token"
             )
async def access_token_request_from(
        username: str = Query(..., min_length=1, max_length=25, description="用户名称"),
        password: str = Query(..., min_length=1, max_length=30, description="用户密码")
) -> Status:
    """
    用户Token API
    :param username: Form表单对象
    :param password: Form表单对象
    :return: dict
    """
    if not username \
            or not password:
        return FailureStatus(
            code=status_code.CODE_204_LOGIN_USER_PASSWORD_ERROR.value
        )

    # TODO 用户校验 密码校验
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # = = = = = = = = = = = = = = = = start token = = = = = = = = = = = = = = = =
    token = encode_access_token(rtx_id=username)
    # = = = = = = = = = = = = == = = = end token = = = = = == = = = = = = = = = =
    return SuccessStatus(
        data={"access_token": token, "token_type": "Bearer"}
    )


@router.post("/token_request_body",
             response_model=Token,
             summary="用户Token API[Request Body] > Demo代码",
             description="依据用户[Request Body]提供的username，password参数（KEY不可更改），获取用户登录Token"
             )
async def access_token_request_body(body_data: O2LUserLogin) -> Status:
    """
    用户Token API
    :param body_data: Request Body
    :return: dict
    """
    username = getattr(body_data, "username", None)
    password = getattr(body_data, "password", None)
    # 缺少登录参数
    if not username or not password:
        return FailureStatus(
            code=status_code.CODE_204_LOGIN_USER_PASSWORD_ERROR.value
        )

    # TODO 用户校验 密码校验
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # = = = = = = = = = = = = = = = = start token = = = = = = = = = = = = = = = =
    token = encode_access_token(rtx_id=username)
    # = = = = = = = = = = = = == = = = end token = = = = = == = = = = = = = = = =
    return SuccessStatus(
        data={"access_token": token, "token_type": "Bearer"}
    )


# ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ *
redis_cli = RedisClientLib(host=redis_host, port=redis_port, db=redis_db, password=redis_password)


async def __get_token_rtx(token: str) -> str:
    token_rtx_id = None
    # >>>>> 优先redis
    if redis_cli.connection:
        token_rtx_id = redis_cli.get_key(key=token)

    # >>>>> jwt解码token
    if not token_rtx_id:
        token_rtx_id = decode_access_token_rtx(token)
        if not token_rtx_id:
            raise JwtCredentialsException("无效X-Token")

    return token_rtx_id


@router.get('/logout',
            summary="[ACCESS]Logout退出",
            description="后端APIs的logout退出API"
            )
async def logout(
        x_token: str = Header(..., min_length=1, max_length=299, convert_underscores=True, description="X-Token")
) -> Status:
    """
    [ACCESS]Logout退出
    :return: JSONResponse
    """
    try:
        x_token_rtx = await __get_token_rtx(token=x_token)
    except:
        return FailureStatus(
            code=status_code.CODE_250_TOKEN_NOT_FOUND.value,
            message=status_msg.get(250)
        )

    if x_token_rtx:
        # 销毁x-token
        if redis_cli.connection and x_token:
            redis_cli.delete_key(x_token)
        return SuccessStatus()
    else:
        return FailureStatus(
            code=status_code.CODE_251_TOKEN_VERIFY_FAILURE.value,
            message=status_msg.get(251)
        )

# ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ *
