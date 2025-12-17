# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 

base_info:
    __author__ = PyGo
    __time__ = 2025/12/17 22:04
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api
    __file_name__ = converter.py

usage:
    
design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
import datetime
from typing import Any, List, Dict, Optional


async def converter(
        model: Any,
        fields: List[Dict] = None,
        default_value: Any = "-"
) -> Optional[Dict[str, Any]]:
    """
    异步函数：将模型对象根据字段定义转换为字典格式。

    参数:
        model (Any): 要转换的模型对象，通常是一个包含属性的对象实例。
        fields (List[Dict], optional): 字段配置列表，每个元素是包含 'key'、'type' 和 'name' 键的字典。
                                       - 'key': 模型中的属性名；
                                       - 'type': 属性的数据类型（如 "str", "int", "datetime" 等）；
                                       - 'name': 输出字典中对应的键名。
        demo：
            xtb_user_list_fields = [
                {"key": "id", "type": "int", "name": "id"},
                {"key": "rtx_id", "type": "str", "name": "rtxId"},
                {"key": "md5_id", "type": "str", "name": "md5Id"},
            ]
        default_value (Any, optional): 当模型属性为空时使用的默认值，默认为 "-".

    返回:
        Dict[str, Any]: 转换后的字典，键为字段定义中的 name，值为对应类型的转换结果。
    """
    if not model or not fields:
        return None


    # 验证字段有效性
    valid_fields: List = []
    for field in fields:
        key: str = field.get("key")
        type_: str = field.get("type")
        name: str = field.get("name")

        if not key: continue  # 忽略无效字段定义
        __name: str = key if not name else name  # 为空默认取key
        __type: str = type_ if type_ else "str"  # 为空默认为字符串格式
        valid_fields.append((key, __type, __name))

    model_dict: Dict = {}
    for field_key, field_type, field_name in valid_fields:
        raw_value = getattr(model, field_key, None)
        # 显式判断 None 来决定是否使用默认值
        field_value = raw_value if raw_value is not None else default_value

        try:
            match field_type:
                case "str":
                    model_dict[field_name] = str(field_value)
                case "int":
                    model_dict[field_name] = int(field_value)
                case "float":
                    model_dict[field_name] = float(field_value)
                case "bool":
                    model_dict[field_name] = bool(field_value)
                case "bool_text":
                    model_dict[field_name] = "是" if bool(field_value) else "否"
                case "datetime" | "date" | "time" if isinstance(field_value, (datetime.datetime, datetime.date)):
                    fmt_map = {
                        "datetime": "%Y-%m-%d %H:%M:%S",
                        "date": "%Y-%m-%d",
                        "time": "%H:%M:%S"
                    }
                    model_dict[field_name] = field_value.strftime(fmt_map[field_type])
                case "timestamp" if hasattr(field_value, 'timestamp'):
                    model_dict[field_name] = field_value.timestamp()
                case "list":
                    model_dict[field_name] = list(field_value)
                case "dict":
                    model_dict[field_name] = dict(field_value)
                case _:
                    model_dict[field_name] = str(field_value)
        except:
            model_dict[field_name] = str(field_value)

    return model_dict
