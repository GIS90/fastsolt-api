# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    request service

base_info:
    __author__ = PyGo
    __time__ = 2026/3/30 22:12
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api
    __file_name__ = request.py

usage:

design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request

from deploy.curd.xtb_request import XtbRequestCurd
from deploy.utils.utils import md5 as md5_func


class XtbRequestService:

    def __init__(self, db_connection: AsyncSession):
        """
        XtbRequestService class initialize
        """
        self.db: AsyncSession = db_connection
        self.xtb_request_curd = XtbRequestCurd()

    def __str__(self):
        print("XtbRequestService class.")

    def __repr__(self):
        self.__str__()

    async def add(self, rtx_id: str, request_body: Request, *args, **kwargs) -> None:
        """
        request record store to database
        :param rtx_id: [str]rtx_id
        :param request_body: [Request]Request object
        :return: None
        """
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        cost = 0  # API请求用时，默认0
        for _k, _v in kwargs.items():
            if _k == "cost":
                cost = _v
        now = datetime.now()
        now_date = now.date()
        path = request_body.url.path
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

        # 基本信息
        new_model = await self.xtb_request_curd.new_model()
        new_model.md5_id = md5_func(
            "%s-%s-%s-%s-%s" % (now, rtx_id, request_body.client.host, path, request_body.method)
        )  # md5
        new_model.rtx_id = rtx_id
        new_model.ip = request_body.client.host
        new_model.params = request_body.query_params
        new_model.method = request_body.method
        new_model.path = path
        new_model.full_path = f"{path}{request_body.url.query}"
        new_model.host_url = f"{request_body.url.scheme}//{request_body.url.netloc}"
        new_model.url = request_body.url
        new_model.cost = cost
        # 其他信息
        new_model.create_time = now
        new_model.create_date = now_date
        new_model.status = False
        # 新增到数据库
        await self.xtb_request_curd.add(db=self.db, model=new_model)


