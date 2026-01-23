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
import time
from typing import Dict
from fastapi import APIRouter, Depends, Header, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from deploy.curd.database import get_session
from deploy.schema.po.access import O2LUserLogin
from deploy.utils.status import Status, SuccessStatus, FailureStatus
from deploy.utils.status_value import StatusCode as Status_code
from deploy.config import redis_host, redis_port, redis_db, redis_password, jwt_expire
from deploy.utils.token import encode_access_token
from deploy.delib.redis_lib import RedisClientLib
from deploy.utils.depend import __get_token_rtx
from deploy.service.xtb_sysuser import XtbSysUserService


# view
router = APIRouter(prefix="/access", tags=["系统登录、退出"])
# service
def get_xtb_sysuser_service(db: AsyncSession = Depends(get_session)):
    return XtbSysUserService(db_connection=db)
# redis-cli
redis_cli = RedisClientLib(host=redis_host, port=redis_port, db=redis_db, password=redis_password)
__JWT_TOKEN_EXPIRE_MINUTES = jwt_expire

# * * * * * * * * * * * * * * * * * * * * * * * * * * [ APIs] * * * * * * * * * * * * * * * * * * * * * * * * * * *
"""
APIs：
    > /access/login：登录
    > /access/logout：退出
"""


@router.post('/login',
             summary="[ACCESS]Login登录",
             description="后端APIs的login登录API，参数位username、password，用来登录获取用户信息、JWT-Token"
             )
async def login(
        body_data: O2LUserLogin,
        request: Request,
        xtb_sysuser_service: XtbSysUserService = Depends(get_xtb_sysuser_service)
) -> Status:
    """
    [ACCESS]Login登录
    :param db: 数据库DB
    :param body_data: [dict]查询请求参数
    :param request: Request
    :return: JSONResponse
    """
    username = getattr(body_data, "username", None)
    password = getattr(body_data, "password", None)
    t24 = getattr(body_data, "t24", False)  # 默认不支持24hToken
    # 缺少登录参数
    if not username \
            or not password:
        return FailureStatus(
            code=Status_code.CODE_209_MISS_USER_PASSWORD.value)

    # 用户信息核对
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    username = username.strip()     # 去空格
    user: Dict = await xtb_sysuser_service.get_login_by_rtx_id(rtx_id=username)
    # >>> 不用不存在
    if not user:
        return FailureStatus(
            code=Status_code.CODE_202_LOGIN_USER_NO_REGISTER.value)
    # >>> 用户注销状态
    if user.get('status'):
        return FailureStatus(
            code=Status_code.CODE_203_LOGIN_USER_OFF.value)

    # >>> check password[前端md5加密 数据库md5加密]
    password_md5_hash = user.get('password')
    if password != password_md5_hash:
        return FailureStatus(
            code=Status_code.CODE_204_LOGIN_USER_PASSWORD_ERROR.value)

    # >>> user is not admin && role is null
    if user.get("rtx_id") != 'admin' and not user.get("role"):
        return FailureStatus(
            code=Status_code.CODE_208_USER_MENU_INVALID.value)
    # 删除密码
    if user.get('password'):
        del user['password']
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # = = = = = = = = = = = = = = = = start token = = = = = = = = = = = = = = = =
    token = encode_access_token(
        rtx_id=username,
        token_time=24 * 60 if t24 else __JWT_TOKEN_EXPIRE_MINUTES
    )
    if not token:
        return FailureStatus(
            code=Status_code.CODE_254_TOKEN_GENERATE_FAILURE.value)
    # = = = = = = = = = = = = == = = = end token = = = = = == = = = = = = = = = =

    data = {
            "token": token,
            "userInfo": {
                "userId": user.get("rtx_id"),
                "userName": user.get("name"),
                "avatar": user.get("avatar"),
                "sex": user.get("sex"),
                "roles": user.get("role"),
            }
        }
    return SuccessStatus(data=data)


@router.get('/logout',
            summary="[ACCESS]Logout退出",
            description="后端APIs的logout退出API"
            )
async def logout(
        x_token: str = Header(..., min_length=1, convert_underscores=True, description="X-Token"),
        request: Request = None
) -> Status:
    """
    [ACCESS]Logout退出
    :return: JSONResponse
    """
    try:
        x_token_rtx = __get_token_rtx(token=x_token)
    except:
        return FailureStatus(
            code=Status_code.CODE_250_TOKEN_NOT_FOUND.value)

    if x_token_rtx:
        # 销毁x-token
        if redis_cli.connection and x_token:
            redis_cli.delete_key(x_token)
        return SuccessStatus()
    else:
        return FailureStatus(
            code=Status_code.CODE_251_TOKEN_VERIFY_FAILURE.value)


# * * * * * * * * * * * * * * * * * * * * * * * * * * [ END ] * * * * * * * * * * * * * * * * * * * * * * * * * * *

