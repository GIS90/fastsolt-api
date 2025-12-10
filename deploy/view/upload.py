# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    upload view

base_info:
    __author__ = PyGo
    __time__ = 2025/11/30 14:07
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api
    __file_name__ = upload.py

usage:
    
design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
from fastapi import APIRouter, File, UploadFile
from typing import  List

from deploy.service.upload import UploadService
from deploy.utils.status import Status, SuccessStatus


# route
upload: APIRouter = APIRouter(prefix='/upload', tags=["文件上传"])
# service
upload_service: UploadService = UploadService()


@upload.post('/file',
             summary="File单个小文件上传",
             description="单个小文件上传，File也有很多参数，目前来说通过file对象获取不到文件的名称等属性，具体查看源码，不推荐使用"
             )
async def file_api(
        file: bytes = File(...)
) -> Status:
    """
    File单个小文件上传
    :param file: [File]File文件对象
    :return: json
    """
    return upload_service.file_api(file)


@upload.post('/files',
             summary="File多个小文件上传",
             description="多个小文件上传，使用的就是List，其中元素都是File对象，不推荐使用")
async def files_api(
        files: List[bytes] = File(...)
) -> Status:
    """
    File单个多文件上传
    :param files: [list]File文件对象列表
    :return: json
    """
    result = list()
    for f in files:
        if not f: continue
        res = upload_service.file_api(file=f)
        if res.get('status_id'):
            result.append(res.get('data').get('file'))

    return SuccessStatus()


@upload.post('/upload_file',
             summary="UploadFile单个大文件上传",
             description="单个大文件上传，UploadFile对象可以获取文件属性，具体参数请查看UploadFile源码，推荐使用")
async def upload_file(
        file: UploadFile = File(...)
) -> Status:
    """
    UploadFile单个大文件上传
    :param file: [UploadFile]UploadFile上传文件对象
    :return: json
    """
    return await upload_service.upload_file_api(file)


@upload.post('/upload_files',
             summary="UploadFile多个大文件上传",
             description="多个大文件上传，UploadFile对象可以获取文件属性，具体参数请查看UploadFile源码，推荐使用")
async def upload_files(
        files: List[UploadFile] = File(...)
) -> Status:
    """
    UploadFile多个大文件上传
    :param files: [UploadFile]UploadFile上传文件对象集合
    :return: json
    """
    result = list()
    for f in files:
        if not f: continue
        res = await upload_service.upload_file_api(file=f)
        if res.get('status_id'):
            result.append(res.get('data').get('file'))
    return SuccessStatus()

# * * * * * * * * * * * * * * * * * * * * * * * * * * [ END ] * * * * * * * * * * * * * * * * * * * * * * * * * * *
