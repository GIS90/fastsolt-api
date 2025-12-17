# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    图片处理

base_info:
    __author__ = PyGo
    __time__ = 2025/12/7 22:04
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api
    __file_name__ = image_lib.py

usage:
    
design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
import os
from PIL import Image
from typing import Dict, List, Optional

from deploy.utils.utils import filename2md5, \
    get_now, mk_dirs
from deploy.config import store_cache, image_quality, image_width
from deploy.utils.status_value import StatusMsg as status_msg, StatusEnum as status_enum


_STORE_CACHE: str = store_cache
_IMAGE_QUALITY: int = image_quality or 100
_IMAGE_WIDTH: int = image_width or 700


class ImageLib:

    ALLOWED_EXTENSIONS = [
            '.png',
            '.jpg',
            '.bmp',
            '.jpeg',
            '.gif',
            '.tif',
            '.psd'
        ]

    def __init__(self, quality: int = _IMAGE_QUALITY, width: int = _IMAGE_WIDTH) -> None:
        """
        初始化参数
        暂无实例化参数，都从配置文件中进行获取
        """
        self.cache = _STORE_CACHE
        self.quality = quality
        self.width = width

    def __str__(self) -> str:
        return f"ImageLib Class: quality[{self.quality}] width[{self.width}]"

    def __repr__(self) -> str:
        return self.__str__()

    @staticmethod
    def visual_value(status_id: int, message: str, data: Optional[List, Dict]) -> Dict:
        """
        方法请求结果格式化
        """
        if data is None: data = []
        return {
            'status_id': status_id,
            'message': message if message else status_msg.get(status_id),
            'data': data
        }

    def allow_format_img(self, name: str) -> bool:
        """
        image格式判断
        :param name: image name
        """
        names = os.path.splitext(name)
        if len(names) < 2:
            return False
        return True if (names[1]).lower() in self.ALLOWED_EXTENSIONS \
            else False

    @staticmethod
    def scan(image_file: str) -> Dict:
        """
        查看图片的基础信息
        image_file: image file
        """
        if (not image_file
                or not os.path.exists(image_file)):
            return {}

        img = Image.open(image_file)
        res = {
            'size': img.size,  # 大小
            'width': img.width,  # 图片的宽
            'height': img.height,  # 图片的高
            'format': img.format  # 图像格式
        }
        return res

    def store_local(self, image_file: str, compress: bool = False) -> Dict:
        """
        图片本地化存储
        :param image_file: image file stream
        :param compress: image 是否进行压缩
        """
        if not image_file:
            return self.visual_value(
                450, '缺少上传文件')

        try:
            # ================= 文件存储初始化 =================
            now_date = get_now(format="%Y%m%d")
            real_store_dir = os.path.join(self.cache, now_date)
            if not os.path.exists(real_store_dir):
                mk_dirs(real_store_dir)
            # <<<<<<<<<<<<<<<<<< save image >>>>>>>>>>>>>>>>>>
            image_name = image_file.filename
            _, store_name_md5 = filename2md5(file_name=image_name, _type='image')
            image_real_file = os.path.join(real_store_dir, store_name_md5)
            image_file.save(image_real_file)
            # 是否进行图片压缩
            if compress:
                small_img = Image.open(image_real_file)
                w_percent = self.width / float(small_img.size[0])   # 宽缩放比例
                h_size = int(float(small_img.size[1]) * float(w_percent))
                small_img = small_img.resize((self.width, h_size), Image.ANTIALIAS)
                small_img.save(image_real_file, quality=self.quality)
            return self.visual_value(
                    status_id=100,
                    message=status_enum.SUCCESS.value,
                    data={'name': store_name_md5, 'file': os.path.join(real_store_dir, store_name_md5)}
                   )
        except Exception as error:
            return self.visual_value(456, '图片存储失败：%s' % str(error))

    def update_size(self, image_file: str, length: int = 280, width: int = 280) -> Dict:
        """
        update image size: length with
        """
        if (not image_file or
                not os.path.exists(image_file)):
            return self.visual_value(
                451, '文件不存在')

        try:
            image_dir, image_name = os.path.split(image_file)
            out_file_md5, out_file_name = \
                filename2md5(file_name=image_name, _type='image')
            im = Image.open(image_file)
            out_image_file = os.path.join(image_dir, out_file_name)
            upsize_image = im.resize((length, width), Image.ANTIALIAS)
            upsize_image.save(out_image_file)
            return self.visual_value(
                status_id=100,
                message=status_enum.SUCCESS.value,
                data={'md5': out_file_md5, 'name': out_file_name})
        except Exception as error:
            return self.visual_value(
                999, '图片更新大小失败：%s' % str(error))

