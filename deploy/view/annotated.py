# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    annotated view

base_info:
    __author__ = PyGo
    __time__ = 2025/12/22 22:02
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api
    __file_name__ = annotated.py

usage:
    
design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
from typing import Annotated, Dict, Literal, Union
from fastapi import APIRouter, Path, Query, Body, Cookie, Header
from pydantic import BaseModel, Field, HttpUrl


annotated: APIRouter = APIRouter(prefix="/annotated", tags=["官网最新参数声明Annotated写法"])


@annotated.get("/q/{item_id}",
               summary="[查询参数模型]直接在路径、请求参数定义在方法上")
async def query_path(
    item_id: Annotated[int, Path(description="路径参数Item-id")],
    q: Annotated[str | None, Query(description="查询参数Item-q", alias="item-query")] = None,
) -> Dict:
    return {"item-id": item_id, "item-q": q}

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
class FilterParams(BaseModel):
    limit: int = Field(default=100, alias="limit", gt=0, le=100, description="分页参数limit")
    offset: int = Field(default=0, alias="offset", ge=0, description="分页参数offset")
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []


@annotated.get("/model/items/",
               summary="[查询参数模型]使用pydantic.BaseModel定义查询参数模型")
async def query_model(filter_query: Annotated[FilterParams, Query(description="查询参数")]) -> Dict:
    return filter_query.model_dump()


class User(BaseModel):
    username: str
    full_name: str | None = None


@annotated.put("/model/{item_id}",
                summary="[查询参数模型]路径请求参数 + Query查询参数 + Body请求体参数模型（pydantic.BaseModel）")
async def query_models(
        item_id: Annotated[int, Path(description="路径参数Item-id")],
        q: Annotated[FilterParams, Query(description="分页查询请求参数")],
        user: Annotated[User, Body(description="用户信息")]
) -> Dict:
    results = {"item_id": item_id, "filter_query": q, "user": user}
    return results

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
class GOODS(BaseModel):
    name: str = Field(..., description="货物名称")
    description: str | None = Field(
        default=None, description="货物描述内容。。。。。。。", max_length=300
    )
    price: float = Field(gt=0, description="货物价格")
    tax: float | None = Field(default=None, description="货物税")
    url: Union[HttpUrl, None] = Field(default=None, description="货物地址")

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "电风扇",
                "description": "格力牌子的电风扇",
                "price": 35.4,
                "tax": 3.2,
                "url": "http://www.pygo2.top",
            }
        }
    }


@annotated.put("/field/{item_id}",
               summary="[查询参数模型]采用Pydantic.Field定义请求体参数，其中embed=True只有一个请求体")
async def query_field(
        item_id: int,
        goods: Annotated[GOODS, Body(embed=True)]
) -> Dict:
    results = {"item_id": item_id, "goods": goods}
    return results

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
class CookieModel(BaseModel):
    cookie_id: str = Field(..., description="会话ID")
    host: str | None = Field(default=None, description="主机地址")
    port: int | None = Field(default=None, description="端口号")

    model_config = {
        "json_schema_extra": {
            "example": {
                "cookie_id": "cookie-id",
                "host": "111.222.333.444",
                "port": 22222
            }
        }
    }


@annotated.get("/cookie/",
               summary="[查询参数模型]Cookie示例")
async def query_cookie(cookies: Annotated[CookieModel, Cookie()]):
    return cookies

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
class HeaderModel(BaseModel):
    header_id: str = Field(..., description="请求头ID")
    host: Union[str, None] = Field(default=None, description="主机地址")
    port: Union[int, None]  = Field(default=None, description="端口号")

    model_config = {
        "json_schema_extra": {
            "example": {
                "header_id": "header-id",
                "host": "111.222.333.444",
                "port": 22222
            }
        }
    }

@annotated.get("/header/",
               summary="[查询参数模型]Header示例")
async def query_header(headers: Annotated[HeaderModel, Header()]):
    return headers
