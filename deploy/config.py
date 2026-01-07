# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    config parameter

base_info:
    __author__ = PyGo
    __time__ = 2025/11/26 22:37
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api
    __file_name__ = config.py

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
import tomllib
from pathlib import Path
from dotenv import dotenv_values
from typing import List, Dict
from dataclasses import dataclass, field
from deploy.utils.printer import printer_error, printer_info, printer_warn


# 指定 .env 文件路径
deploy_folder: Path = Path(__file__).parent.resolve()  # deploy abs path
root_folder = deploy_folder.parent
env_file = root_folder.joinpath(".env")
env: str = "dev" if not env_file.exists() \
    else dotenv_values(env_file).get("ENV") or "dev"  # 默认dev环境

# 配置文件
etc_file = root_folder.joinpath("etc", f"{env}.toml")
if (not etc_file.exists()
        or not etc_file.is_file()):
    printer_error(content=f"配置文件[{env_file}]不存在，系统自动退出......", hr=True)
    sys.exit(1)

try:
    with open(etc_file, "rb") as f:
        data = tomllib.load(f)
except:
    printer_error(content=f"配置文件解析失败，请检查配置：{env_file}", hr=True)
    sys.exit(1)

printer_info(content=f"当前环境：{env}，配置文件：{etc_file}", hr=True)


# server
server_name: str = data["server"].get("name") or "Fastslot-API"
server_version: str = data["server"].get("version")

# app
# ---------- middleware ------------
app_secret_key: str = data["app"].get("secret_key")
app_allow_host: List[str] = data["app"].get("allow_host")
app_cors_origin: List[str] = data["app"].get("cors_origin")
app_ban_router: List[str] = data["app"].get("ban_router")
app_session_max_age: int = data["app"].get("session_max_age")
app_request_method: List[str] = data["app"].get("request_method")
app_gzip_size: int = data["app"].get("gzip_size")
app_gzip_level: int = data["app"].get("gzip_level")
# ----------- docs ------------
app_openapi_url: str = data["app"].get("openapi_url")
app_docs_url: str = data["app"].get("docs_url")
# ----------- static resource ------------
__app_static_folder: str = data["app"].get("static")
app_static_url: str = f"/{__app_static_folder}"
app_static_folder = deploy_folder.joinpath(__app_static_folder)
if not app_static_folder.exists():
    # if not exist, create it
    app_static_folder.mkdir(parents=True)
    printer_warn(content=f"静态资源目录[{app_static_folder}]不存在，系统自动创建", hr=True)

# db
db_link: str = data["db"].get("link")
if not db_link:
    printer_error(content="配置文件[db->link]数据库连接地址空，系统退出！", hr=True)
    sys.exit(1)

# redis
redis_host: str = data["redis"].get("host")
redis_port: int = data["redis"].get("port")
redis_db: int = data["redis"].get("db")
redis_password: str = data["redis"].get("password")

# jwt
jwt_token_verify: bool = data["jwt"].get("verify")
jwt_secret_key: str = data["jwt"].get("secret_key")
jwt_algorithm: str = data["jwt"].get("algorithm")
jwt_expire: int = data["jwt"].get("expire")

# log
log_folder: str = data["log"].get("folder")
log_level: str = data["log"].get("level")
log_format: str = data["log"].get("format")
log_prefix: str = data["log"].get("prefix")
log_max_size: int = data["log"].get("max_size")
log_count: int = data["log"].get("count")

# dingtalk
ding_base: str = data["dingtalk"].get("base")
ding_token_api: str = data["dingtalk"].get("token_api")

# qywx
qywx_base: str = data["qywx"].get("base")
qywx_token_api: str = data["qywx"].get("token_api")
qywx_send_api: str = data["qywx"].get("send_api")
qywx_recall_api: str = data["qywx"].get("recall_api")
qywx_upload_api: str = data["qywx"].get("upload_api")
qywx_temp_api: str = data["qywx"].get("temp_api")

# store
store_cache: str = data["store"].get("cache")
store_yun_access: str = data["store"].get("yun_access")
store_yun_secret: str = data["store"].get("yun_secret")
store_yun_base: str = data["store"].get("yun_base")
store_yun_space: str = data["store"].get("yun_space")

# image
image_quality: int = data["image"].get("quality")
image_width: int = data["image"].get("width")



# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# APP简介
@dataclass(frozen=True, order=True)
class APPProfile:
    title: str = server_name
    version: str = server_version
    summary: str = "作者：高明亮"
    description: str = "基于Python语言研发，使用FastAPI、Pydantic、异步数据库搭建的后端APIs脚手架，Github地址：https://github.com/GIS90/fastsolt-api"     # 支持Markdown语法


# 作者
_author_contact: Dict[str, str] = {
    "name": "Pygo2",
    "url": "http://www.pygo2.top",
    "email": "gaoming971366@163.com"
}
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -