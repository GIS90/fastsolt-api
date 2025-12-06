# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    public utils method
    任何项目、模块均都可以调用，均属于通用方法
    持续累计更新......

base_info:
    __author__ = PyGo
    __time__ = 2025/11/29 17:34
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api
    __file_name__ = utils.py

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
import random
import string
import hashlib
import time
import subprocess
import platform
from typing import List, Tuple, Set, Dict, Union, Optional, Any, Literal
from datetime import datetime, timedelta
from pathlib import Path, PurePath

""" - - - - - - - - - - - - - - - - - 加密类 - - - - - - - - - - - - - - - - -"""


def md5(v: str) -> str:
    """
    字符串md5加密

    :param v: string value
    :return: md5 string value
    """
    if not v: v = random_string(16)
    if isinstance(v, str):
        v = v.encode('utf-8')
    return hashlib.md5(v).hexdigest()


def filename2md5(rtx_id: str = None, file_name: str = None, _type: str = 'file') -> Tuple[str, str]:
    """[buildin method]
    根据文件名生成MD5值，用于本地存储文件命名

    :param rtx_id: rtx-id
    :param file_name: file name
    :param _type: file type, is file,image, and so on.
    :return:
        result is tuple
        param1: md5 value no suffix
        param2: md5 value have suffix
    """
    file_names = os.path.splitext(file_name)
    suffix = (file_names[1]).lower() if len(file_names) > 1 else ''
    _v = file_name + get_now() + _type + rtx_id if rtx_id \
        else file_name + get_now() + _type
    md5_v = md5(_v)
    return md5_v, md5_v + suffix if suffix else md5_v


""" - - - - - - - - - - - - - - - - - 时间、日期 - - - - - - - - - - - - - - - - -"""


def s2d(s, fmt="%Y-%m-%d %H:%M:%S") -> datetime:
    """
    字符串转日期

    :param s: string type time
    :param fmt: transfer to formatter
    :return: datetime type time
    """
    return datetime.strptime(s, fmt)


def d2s(d, fmt="%Y-%m-%d %H:%M:%S") -> str:
    """
    日期转字符串

    :param d: datetime type time
    :param fmt: transfer to formatter
    :return: string type time
    """
    return d.strftime(fmt)


def d2ts(d) -> float:
    """
    日期转ts

    :param d: datetime type parameter
    :return: timestamp type
    """
    return time.mktime(d.timetuple())


def s2ts(s, fmt="%Y-%m-%d %H:%M:%S") -> float:
    """
    字符串转ts

    :param s: sting type parameter
    :param fmt: transfer to formatter
    :return: time.time type
    """
    d = s2d(s, fmt)
    return d2ts(d)


def ts2d(st) -> datetime:
    """
    时间戳转日期

    :param st: timestamp
    :return: datetime type time
    """
    return datetime.fromtimestamp(st)


def dura_date(d1: Union[str, datetime], d2: Union[str, datetime], need_d: bool = False):
    """
    计算两个日期时间之间的差值

    :param d1: datetime parameter 1
    :param d2: datetime parameter 2
    :param need_d: is or not need hours, minutes, seconds
    :return: result 1: seconds
    result 2: hours, minutes, seconds
    """
    if type(d1) is str:
        d1 = s2d(d1)
    if type(d2) is str:
        d2 = s2d(d2)
    d = d2 - d1
    if need_d is False:
        seconds = d.seconds
        mins = seconds / 60.00
        hours = mins / 60.00
        return hours, mins, seconds
    return d


def get_now_time() -> datetime:
    """
    获取当前时间

    :return: to return the now of datetime type
    """
    return datetime.now()


def get_now_date():
    """
    获取当前日期

    :return: to return the now of date type
    """
    return datetime.now().date()


def get_now(format="%Y-%m-%d %H:%M:%S") -> str:
    """
    获取当前时间，字符串类型

    :return: to return the now of string type
    """
    return d2s(datetime.now(), format)


def get_week_day(date) -> str:
    """
    查询日期的星期

    :param date: date
    :return: week
    """
    weekday_list: Tuple = ('星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期天')
    weekday = weekday_list[date.weekday()]
    return weekday


def get_month_list() -> List[str]:
    """
    获取月份列表

    :return: list data
    """
    return ['1月', '2月', '3月', '4月', '5月', '6月',
            '7月', '8月', '9月', '10月', '11月', '12月']


def get_day_week_date(query_date) -> Dict:
    """
    获取指定日期所在周的日期信息

    :param query_date: 查询日期
    :return: 包含本周起始日期、结束日期和每日日期的字典
        - start_week_date: 本周开始日期 (周一)
        - end_week_date: 本周结束日期 (周日)
        - week_date: 包含周一到周日日期的列表
    """
    if not query_date:
        query_date = get_now_date()
    if isinstance(query_date, str):
        query_date = s2d(query_date, fmt="%Y-%m-%d")
    current_week = query_date.isoweekday()  # 当前时间所在本周第几天
    start_week_date = (query_date - timedelta(days=current_week - 1))
    end_week_date = (query_date + timedelta(days=7 - current_week))
    _week = list()
    for day_num in range(0, 7, 1):
        _week.append(d2s(start_week_date + timedelta(days=day_num), fmt="%Y-%m-%d"))
    _res = {
        "start_week_date": d2s(start_week_date, fmt="%Y-%m-%d"),  # 本周起始日期
        "end_week_date": d2s(end_week_date, fmt="%Y-%m-%d"),  # 本周结束日期
        "week_date": _week  # 本周日期列表

    }
    return _res


""" - - - - - - - - - - - - - - - - - 用户类 - - - - - - - - - - - - - - - - -"""


def get_real_ip(request) -> str:
    """
    获取请求的真实IP地址
    优先从HTTP头部的X-Forwarded-For字段获取客户端IP，
    如果不存在该字段则使用remote_addr获取

    :param request: Flask API请求对象
    :return: 客户端IP地址字符串
    """
    if not request.headers.getlist("X-Forwarded-For"):
        ip = request.remote_addr
    else:
        ip = request.headers.getlist("X-Forwarded-For")[0]
    return ip


def get_rtx_id(request) -> str:
    """
    获取请求用户的RTX-ID
    从HTTP头部的X-Rtx-Id字段获取用户标识信息

    :param request: Flask API请求对象
    :return: 用户RTX-ID字符串，如果不存在则返回空字符串
    """
    return request.headers.get("X-Rtx-Id") \
        if request.headers.get("X-Rtx-Id") else ''


""" - - - - - - - - - - - - - - - - - 文件、目录 - - - - - - - - - - - - - - - - -"""


def mk_dirs(path: str) -> str:
    """
    递归创建文件夹

    :param path: to make folder
    :return: path
    """
    os.makedirs(path, exist_ok=True)
    return path


def __get_cur_folder() -> Path:
    """
    获取当前脚本所在的文件夹路径，解决脚本是否被冻结的问题

    :return: 当前脚本所在的文件夹路径
    :rtype: Path
    """
    # config file absolute path
    current_abspath_file = Path(__file__).resolve()
    if not current_abspath_file.is_absolute():
        _os_path = os.path.dirname(os.path.abspath(__file__))
        current_abspath_file = Path(_os_path)

    return current_abspath_file.parent


def get_deploy_folder() -> Optional[Path]:
    """
    获取项目deploy目录

    :return: abs deploy path
    """
    if not __get_cur_folder().is_absolute() \
            or not __get_cur_folder().exists():
        return None

    return __get_cur_folder().parent


def get_root_folder() -> Optional[Path]:
    """
    获取项目root目录

    :return: project root directory
    """
    if not get_deploy_folder().is_absolute() \
            or not get_deploy_folder().exists():
        return None

    return get_deploy_folder().parent


""" - - - - - - - - - - - - - - - - - 参数校验类 - - - - - - - - - - - - - - - - -"""


def v2decimal(x: str, y: int) -> Optional[float]:
    """
    将字符串数值转换为指定小数位数的数值

    :param x: 字符串类型的数值
    :param y: 保留的小数位数
    :return: 转换后的数值，如果输入为空则返回None
    """
    if not x: return None

    try:
        return round(float(x), y)
    except ValueError:
        return None


def check_length(data: str, limit: int = 10) -> bool:
    """
    检查数据长度是否符合限制要求

    :param data: check data
    :param limit: length limit, default value is 10
    return True or False
    """
    if not data:
        return True
    return True if len(data) <= limit else False


""" - - - - - - - - - - - - - - - - - 信息类、通讯类 - - - - - - - - - - - - - - - - -"""


def ping(ip: str, **kwargs):
    """
    Ping

    :param ip: the target ip or 域名
    :param kwargs: the ping other parameters
    :return: bool

    **kwargs:
        -a             将地址解析为主机名。
        -n count       要发送的回显请求数。
        -l size        发送缓冲区大小。
        -w timeout     等待每次回复的超时时间(毫秒)。

    usage:
        ping(ip='www.baidu.com', n=4, w=2000, l=32)
        or
        ping(ip='127.0.0.1', n=4, w=2000, l=32)

    param default value:
        - count: 4
        - size: 32
        - timeout: 2000
    """
    cmd = ['ping']
    # **kwargs > ping > a
    if kwargs.get('a'):
        cmd.append('-a')
    # **kwargs > ping > n
    if kwargs.get('n') or kwargs.get('count'):
        count = kwargs.get('n') or kwargs.get('count') or 4
        if not isinstance(count, int):
            count = 4
        if count > 0:
            cmd.append('-n %s' % count)
    # **kwargs > ping > l
    if kwargs.get('l') or kwargs.get('size'):
        size = kwargs.get('l') or kwargs.get('size') or 32
        if not isinstance(size, int):
            size = 0
        if size > 0:
            cmd.append('-l %s' % size)
    # **kwargs > ping > w
    if kwargs.get('w') or kwargs.get('timeout'):
        timeout = kwargs.get('w') or kwargs.get('timeout') or 2000
        if not isinstance(timeout, int):
            timeout = 0
        if timeout > 0:
            cmd.append('-w %s' % timeout)
    cmd.append(ip)
    cmd_str = ' '.join(cmd)
    ret_res = subprocess.call(cmd_str, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
    return True if ret_res == 0 else False


def host_os():
    """
    获取当前运行的操作系统类型和架构信息，并返回对应的编码和详细信息字典。
    Windows: 1
    Linux: 2
    Darwin: 3

    :return: int, detail information
    """
    _host_os = platform.system()
    _host_bit = platform.architecture()
    if _host_os == 'Windows':
        os_code = 1
    elif _host_os == 'Linux':
        os_code = 2
    elif _host_os == 'Darwin':
        os_code = 3
    else:
        os_code = 4

    _detail = {
        'os': _host_os,
        'os_code': os_code,
        'bit': _host_bit[0] if len(_host_bit) > 1 else _host_bit
    }
    return os_code, _detail


""" - - - - - - - - - - - - - - - - - 权限类 - - - - - - - - - - - - - - - - -"""


def api_inspect_rtx() -> Dict:
    """
    检查请求的API是否包含RTX-ID参数，不包含则中止请求
    POST请求：
        get_json()
    GET请求：
        args
    其他：
        no check
    """
    pass


""" - - - - - - - - - - - - - - - - - 数据类 - - - - - - - - - - - - - - - - -"""


def get_file_size(path: str, unit: str = 'KB') -> float:
    """
    获取传入的文件大小，以默认KB大小返回
    """
    # not found file
    if not path \
            or not os.path.isfile(path) \
            or not os.path.exists(path):
        return 0

    # get the real file size
    size = os.path.getsize(path)
    if size == 0:
        return 0

    # return file size, default is KB
    __unit = str(unit).upper() if unit else 'KB'
    b = 1024
    if __unit == 'B':
        return size
    elif __unit == 'KB':
        return size / b
    elif __unit == 'MB':
        return size / b ** 2
    elif __unit == 'GB':
        return size / b ** 3
    elif __unit == 'TB':
        return size / b ** 4
    else:
        return size


def random_string(length: int = 16) -> str:
    """
    生成随机字符串
    :param length: 字符串长度
    """
    return ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=length))


def list_dict_find(options: List[Dict], key: str, value: any) -> Union[Dict, None]:
    """
    字典列表查找
    """
    return next((item for item in options if item.get(key) == value), None)


def cut_string(content: str, length: Optional[int]) -> str:
    if not content: return content
    _max_len = 55 if not length else length
    return content[:_max_len] + "......详情" if len(content) >= length else content


""" - - - - - - - - - - - - - - - - - 菜单 - - - - - - - - - - - - - - - - -"""


def build_menu_tree_fci(flat_menus: List[Dict],
                        parent_id: Optional[int] = None,
                        id_key: str = "id",
                        parent_key: str = "pid",
                        children_key: str = "children"
                        ) -> List[Dict]:
    """
    递归构建菜单树
    :param flat_menus: [list]扁平化菜单列表
    :param parent_id: [int]当前层级的父节点ID
    :param id_key: [str]节点ID字段名
    :param parent_key: [str]父节点ID字段名
    :param children_key: [str]子节点列表字段名
    :return: [list]
    """
    tree = []
    for menu in flat_menus:
        if menu.get(parent_key) == parent_id:
            # 递归查找子节点
            children = build_menu_tree_fci(
                flat_menus,
                parent_id=menu[id_key],
                id_key=id_key,
                parent_key=parent_key,
                children_key=children_key
            )
            if children:
                menu[children_key] = children
            tree.append(menu)
    return tree


def build_menu_tree_iterative(
        flat_menus: List[Dict],
        root_id: Optional[int] = None,
        id_key: str = "id",
        parent_key: str = "pid",
        children_key: str = "children"
) -> List[Dict]:
    """
    迭代构建菜单树

    :param flat_menus: [list]扁平化菜单列表
    :param root_id: [int]跟节点ID
    :param id_key: [str]节点ID字段名
    :param parent_key: [str]父节点ID字段名
    :param children_key: [str]子节点列表字段名
    :return: [list]
    """
    # 创建ID到节点的映射
    menu_map = {menu[id_key]: menu for menu in flat_menus}

    # 初始化树
    tree = []

    for menu in flat_menus:
        parent_id = menu.get(parent_key)
        if parent_id == root_id:
            # 根节点
            tree.append(menu)
        else:
            # 子节点：添加到父节点的children中
            parent = menu_map.get(parent_id)
            if parent:
                if children_key not in parent:
                    parent[children_key] = []
                parent[children_key].append(menu)

    return tree


def flatten_tree_recursive(tree_data, parent_id=None, result=None):
    if result is None:
        result = []

    for node in tree_data:
        # 创建扁平化节点（可根据需要调整字段）
        flat_node = {
            'id': node['id'],
            'label': node['label'],
            'level': node['level'],
        }
        result.append(flat_node)

        # 如果有子节点，递归处理
        if node.get('children'):
            flatten_tree_recursive(node['children'], parent_id=node['id'], result=result)

    return result


def get_all_parent_ids_iterative(
        flat_menus: List[Dict],
        permission_ids: List[int],
        id_key: str = "id",
        parent_key: str = "pid"
) -> List[Union[int, Any]]:
    """
    获取权限菜单ID所有的父节点+权限节点集合

    :param flat_menus: [list]扁平化菜单列表
    :param permission_ids: [list]权限菜单列表
    :param id_key: [str]节点ID字段名
    :param parent_key: [str]父节点ID字段名
    :return: [list]
    """
    menu_dict: Dict = {item[id_key]: item for item in flat_menus}
    all_ids = set(permission_ids)

    # 使用队列进行广度优先搜索
    queue = list(permission_ids)

    while queue:
        current_id = queue.pop(0)
        current_item = menu_dict.get(current_id)
        if current_item and current_item[parent_key]:
            parent_id = current_item[parent_key]
            if parent_id not in all_ids:
                all_ids.add(parent_id)
                queue.append(parent_id)

    return list(all_ids)
