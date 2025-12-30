# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe:
    MVS：view layer

base_info:
    __author__ = PyGo
    __time__ = 2025/11/25 21:44
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
from deploy.view.root import router as root_router
from deploy.view.api import router as api_router
from deploy.view.access import router as access_router

from deploy.view.base import router as base_router
from deploy.view.annotated import router as annotated_router
from deploy.view.method import router as method_router
from deploy.view.response import router as response_router
from deploy.view.depend import router as depend_router
from deploy.view.upload import router as upload_router
from deploy.view.error import router as error_router

from deploy.view.xtb_sysuser import router as xtb_sysuser_router


"""
View根据系统设计的api进行模块划分，其中有3个比较特殊（不为系统模块设计API）
- root：路径为/，系统首页
- api：为对外开发的API集合 [不走token验证]
- access：JWT Token系统验证 [不走token验证]


功能模块
- base：基础参数请求模块 [Path Query Body Form Cookie Header]
- base：官网最新参数声明Annotated写法
- method：请求方式模块 [GET POST PUT DELETE PATCH OPTIONS HEAD]
- response：Response对象类返回测试示例 [Response, PlainTextResponse, HTMLResponse, 
                                    JSONResponse, StreamingResponse, RedirectResponse]
- depend：依赖注入，包含依赖方法与依赖类
- upload：文件上传模块 [File UploadFile]
- error：自定义FastAPI-HTTPException异常处理


实例模块
- xtb_sysuser：系统用户增删改查
"""
__all__ = ["add_routers"]


add_routers = [
    root_router,
    base_router,
    annotated_router,
    method_router,
    response_router,
    upload_router,
    error_router,
    api_router,
    access_router,
    xtb_sysuser_router,
]
