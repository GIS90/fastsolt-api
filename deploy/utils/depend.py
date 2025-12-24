# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    depend

base_info:
    __author__ = PyGo
    __time__ = 2025/12/6 10:47
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api
    __file_name__ = depend.py

usage:
    
design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
from fastapi import Header, Query
from typing import Optional, Dict

from deploy.utils.token import decode_access_token_rtx
from deploy.utils.exception import JwtCredentialsException
from deploy.delib.redis_lib import RedisClientLib
from deploy.config import redis_host, redis_port, redis_db, redis_password
from deploy.schema.po.x import PageListModel, DownloadFileModel
from deploy.schema.po.menu import MenuBaseModel, MenuEditModel


# redis-cli
redis_cli = RedisClientLib(host=redis_host, port=redis_port, db=redis_db, password=redis_password)
# parameters
MIN_LENGTH = 1
MAX_LENGTH = 299


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
"""
Token-Rtx-ID依赖
> depend_token_rtx：解码X-Token的Rtx-id
> depend_token_rtx_valid：解码X-Token的Rtx-id + 验证用户可用性（过滤数据不存在、已删除）
"""


def __get_token_rtx(token: str) -> str:
    token_rtx_id = None
    # >>>>> 优先redis
    try:
        if redis_cli.connection:
            token_rtx_id = redis_cli.get_key(key=token)
    except:
        ...

    # >>>>> jwt解码token
    if not token_rtx_id:
        token_rtx_id = decode_access_token_rtx(token)
        if not token_rtx_id:
            raise JwtCredentialsException("无效X-Token")

    return token_rtx_id


def depend_token_rtx(
    x_token: str = Header(..., min_length=MIN_LENGTH, max_length=MAX_LENGTH, convert_underscores=True, description="X-Token")
) -> str:
    return __get_token_rtx(token=x_token)


def depend_token_rtx_valid(
    x_token: str = Header(..., min_length=MIN_LENGTH, max_length=MAX_LENGTH, convert_underscores=True, description="X-Token")
) -> str:
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    token_rtx_id = __get_token_rtx(token=x_token)
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # TODO 用户数据验证
    # user_model = xtb_sysuser_bo.get_user_by_rtx_id(token_rtx_id)
    # # 数据不存在
    # if not user_model:
    #     raise UserInvalidException("用户不存在")
    # # 数据已删除
    # if getattr(user_model, "is_del"):
    #     raise UserInvalidException("用户已注销")
    ...

    return token_rtx_id


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
"""
Pageable-Params依赖
> pageable_params：分页参数
> pageable_query_params：分页参数 + 非模糊查询
> pageable_like_params：分页参数 + 模糊查询
> pageable_model_params：分页参数 + 条件数据模型（type：dict）
"""


def pageable_params(
    page: int = Query(default=1, ge=MIN_LENGTH, description="页码"),
    pageSize: int = Query(default=15, ge=MIN_LENGTH, description="条数"),
) -> Dict:
    return {"page": page, "limit": pageSize, "offset": (page - 1) * pageSize}


def pageable_query_params(
    page: int = Query(default=1, ge=MIN_LENGTH, description="页码"),
    pageSize: int = Query(default=15, ge=MIN_LENGTH, description="条数"),
    content: str | None = Query(default=None, max_length=MAX_LENGTH, description="非模糊查询"),
) -> Dict:
    return {"page": page, "limit": pageSize, "offset": (page - 1) * pageSize, "content": content}


def pageable_like_params(
    page: int = Query(default=1, ge=MIN_LENGTH, description="页码"),
    pageSize: int = Query(default=15, ge=MIN_LENGTH, description="条数"),
    content: Optional[str] = Query(default=None, max_length=MAX_LENGTH, description="模糊查询参数"),
) -> Dict:
    return {"page": page, "limit": pageSize, "offset": (page - 1) * pageSize, "content": f"%{content}%"}


def pageable_model_params(
    params: PageListModel
) -> Dict:
    page, pageSize, content = params.page, params.pageSize, params.content
    if content.get("content"):
        content["content"] = "%" + content.get("content") + "%"
    if content.get("dateRange"):
        content["start"] = content.get("dateRange")[0] + " 00:00:00"
        content["end"] = content.get("dateRange")[1] + " 23:59:59"
        content.pop("dateRange")
    return {"page": page, "limit": pageSize, "offset": (page - 1) * pageSize, "content": content}


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
"""
X->Download依赖
> download_params：下载数据请求参数
"""


def download_params(params: DownloadFileModel) -> Dict:
    # TODO 自定义处理
    file_name = params.name
    ...
    return {"api": params.api, "name": file_name, "md5": params.md5, "type": params.type}


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
"""
Menu菜单依赖
"""


def __menu_params(params: Dict) -> Dict:
    new_params: Dict = {}
    for key, value in params.items():
        if key == "isKeepAlive":
            new_params["cache"] = value
        elif key == "isAffix":
            new_params["affix"] = value
        elif key == "isFull":
            new_params["full"] = value
        elif key == "isBreadcrumb":
            new_params["breadcrumb"] = value
        else:
            new_params[key] = value
    return new_params


def menu_edit_params(params: MenuEditModel) -> Dict:
    return __menu_params(params=params.model_dump())


def menu_add_params(params: MenuBaseModel) -> Dict:
    return __menu_params(params=params.model_dump())
