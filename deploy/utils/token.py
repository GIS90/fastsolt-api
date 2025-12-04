# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    token

base_info:
    __author__ = PyGo
    __time__ = 2025/11/29 16:52
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api
    __file_name__ = token.py

usage:
    
design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
from datetime import timedelta
from typing import Optional, Dict
from jose import JWTError, jwt, ExpiredSignatureError

from deploy.utils.utils import d2s, get_now_time, d2ts, ts2d
from deploy.utils.exception import JwtCredentialsException
from deploy.config import (jwt_secret_key, jwt_algorithm, jwt_expire,
                           redis_host, redis_port, redis_db, redis_password)
from deploy.delib.redis_lib import RedisClientLib


# ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ *
JWT_TOKEN_SECRET_KEY: str = jwt_secret_key
JWT_TOKEN_ALGORITHM: str = jwt_algorithm
# 访问令牌过期[默认时间]，单位：分
TOKEN_EXPIRE_MINUTE: int = 4 * 60
if jwt_expire:
    TOKEN_EXPIRE_MINUTE = jwt_expire

# redis-cli
redis_cli = RedisClientLib(
    host=redis_host,
    port=redis_port,
    db=redis_db,
    password=redis_password
)
# ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ * ～ *


# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
"""
JWT Token APIs[JWT]:
    > encode_access_token：生成Jwt Token
    > decode_access_token：解码Jwt Token
    > decode_access_token_rtx：解密Jwt Token的rtx-id
    > verify_access_token：验证Jwt Token
    > verify_access_token_expire：验证Jwt Token是否过期
    > read_token_header：读取Jwt Token HEADER信息

关键参数用户rtx-id
"""


def encode_access_token(
        rtx_id: str = None,
        token_time: int = TOKEN_EXPIRE_MINUTE
) -> Optional[str]:
    """
    生成Jwt Token
    :param rtx_id: [str]rtx-id
    :param token_time: [int]Token过期时间，系统默认4h，单位：分钟
    :return: [dict]jwt token
    """
    encoded_jwt_token = None
    if not rtx_id:
        return encoded_jwt_token

    to_encode_data: Dict = {"rtx_id": rtx_id}
    # 申请时间
    token_apply_time = get_now_time()
    to_encode_data['apply_time'] = d2s(token_apply_time, fmt="%Y-%m-%d %H:%M:%S")
    # 过期日期
    expire = token_apply_time + timedelta(minutes=token_time)     # 调试配置seconds=10
    expire_ts = d2ts(expire)
    to_encode_data['expire_time'] = d2s(expire, fmt="%Y-%m-%d %H:%M:%S")
    to_encode_data['expire_time_ts'] = expire_ts
    to_encode_data.update({"exp": expire_ts})    # jwt过期时间KEY：['exp', 'iat', 'nbf']
    # header
    HEADERS = {"alg": JWT_TOKEN_ALGORITHM, "typ": "JWT"}
    try:
        encoded_jwt_token = jwt.encode(
            claims=to_encode_data,
            key=JWT_TOKEN_SECRET_KEY,
            algorithm=JWT_TOKEN_ALGORITHM,
            headers=HEADERS)
        # 存储->Redis
        if redis_cli.connection:
            redis_cli.set_key(key=encoded_jwt_token, value=rtx_id, ex=token_time * 60)
    except Exception as e:
        raise JwtCredentialsException(f"Jwt Token [encode] error, [{e}].")
    """
    jwt.encode参数解析：
        claims: dict[str, Any],
        key: AllowedPrivateKeys | str | bytes,
        algorithm: str | None = "HS256",
        headers: dict[str, Any] | None = None,
        json_encoder: type[json.JSONEncoder] | None = None,
        sort_headers: bool = True,
    ----------------------------------------------------------------------
    返回值：
        str：加密形成的Token字符串
    """
    return encoded_jwt_token


def decode_access_token(
        token: str
) -> dict:
    """
    解码Jwt Token
    :param token: [str]Token
    :return: [dict]Token data
    """
    claims = dict()
    if not token:
        return claims

    try:
        claims = jwt.decode(token=token, key=JWT_TOKEN_SECRET_KEY, algorithms=[JWT_TOKEN_ALGORITHM])
        """jwt.decode
        参数解析：
            token (str): Token字符串
            key (str or dict): 定义Token时的密钥
            algorithms (str or list): 定义Token时的算法
        ----------------------------------------------------------------------
        返回值：
            dict: 解码加密后Token的data数据
        """
        return claims
    except (ExpiredSignatureError, JWTError):
        return claims
    except Exception as e:
        raise JwtCredentialsException(f"Jwt Token [decode] error, [{e}].")


def decode_access_token_rtx(
        token: str
) -> Optional[str]:
    """
    解密Jwt Token的rtx-id
    :param token: [str]token
    :return: [str]rtx-id
    """
    if not token:
        return None
    return decode_access_token(token).get('rtx_id')


def verify_access_token(
        token: str,
        x_rtx_id: str
) -> bool:
    """
    校验Token解码后的rtx-id与用户Header/Data/Params传入的rtx-id是否一样
    :param token: [str]Token
    :param x_rtx_id: [str]用户X-Rtx-Id
    :return: [bool]
    """
    if (not token or
            not x_rtx_id):
        return False

    try:
        claims = decode_access_token(token)
        return claims.get('rtx_id') == x_rtx_id if claims else False
    except:
        return False


def read_token_header(
        token: str
) -> dict:
    """
    读取Jwt Token HEADER信息
    :param token: [str]token
    :return: [dict]header
    """
    header = dict()
    if not token:
        return header

    try:
        header = jwt.get_unverified_header(token)
    except:
        pass
    return header


# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
"""
JWT Token APIs[Redis]:
    > verify_access_token_expire：验证Jwt Token是否过期

关键参数用户X-Token
"""


def __verify_access_token_expire_jwt(
        token: str
) -> str:
    """
    验证Jwt Token是否过期
    :param token: [str]token
    :return: [str]rtx-id
    """
    if not token:
        return None

    try:
        claims = decode_access_token(token)
        if not claims:
            return None

        rtx_id = claims.get("rtx_id")
        exp = claims.get("exp")
        if (not rtx_id
                or not exp):
            return None

        exp_datetime = ts2d(st=exp)
        now_datetime = get_now_time()
        return None if now_datetime < exp_datetime else rtx_id
    except JwtCredentialsException:
        return None
    except Exception as e:
        raise Exception(f"Jwt Token [expire] error, [{e}].")


def verify_access_token_expire(
        x_token: str
) -> (bool, Optional[str]):
    """
    验证Jwt Token是否过期Form Redis
    :param x_token: [str]token
    :return: [bool, str]bool, rtx-id
    """
    token_rtx_id = None
    if not x_token:
        return True, None

    try:
        if redis_cli.connection:
            token_rtx_id = redis_cli.get_key(key=x_token)
    except Exception as e:
        pass

    if not token_rtx_id:
        try:
            token_rtx_id = __verify_access_token_expire_jwt(x_token)
        except Exception as e:
            return True, None

    # 如果token_rtx_id存在，说明token有效未过期，返回False；否则返回True表示已过期
    return False if token_rtx_id else True, token_rtx_id

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
