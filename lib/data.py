""" 数据处理常用方法
"""

############ json 数据处理 ############
import json
import jsonpath

# dict -> json
def dict_json(dict_data, json_file=None) -> str:
    """dict -> json

    Args:
        dict_data (dict): 字典数据
        json_file (str, optional): json文件路径. Defaults to None.

    Returns:
        json: json格式数据
    """
    data = json.dumps(dict_data, indent=2, ensure_ascii=False)
    if json_file and dict_data:
        with open(json_file, 'w') as jf:
            json.dump(dict_data, jf, indent=2, ensure_ascii=False)
    return data

# json -> dict
def json_dict(data:str=None, file_path:str=None) -> dict:
    """json -> dict

    Args:
        data (str, optional): json 数据. Defaults to None.
        file_path (str, optional): json file path. Defaults to None.

    Returns:
        dict: 数据
    """
    if bool(data) ^ bool(file_path):
        if data:
            return json.loads(data)
        else:
            data = {}
            with open(file_path, 'r', encoding='utf8') as f:
                data = json.load(f)
            return data
    else:
        raise Exception('Select one of the paramss')

############ json 数据处理 ############

############ dict 字典处理 ############
import jsonpath

# dict find json path
def dict_find_key(data:dict, json_path:str) -> list|bool:
    """字典 根据jsonpath 找值

    Args:
        data (dict): 数据
        json_path (str): json path

    Returns:
        list|bool: 返回数据集 或 false 没找到
    """
    # jsonpath $ 不会返回所有
    if json_path == '$': return data
    return jsonpath.jsonpath(data, json_path)

############ dict 字典处理 ############

############ re ############
import re

def re_get_str(_r:str, data:str) -> str|None:
    """re 获取字符串

    Args:
        _r (str): 正则表达式
        data (str): 要查找的数据

    Returns:
        str|None: 查找结果
    """
    res = re.search(_r, data)
    return res.group() if res else None

def re_up(_r:str, data:str, new_data:str) -> str:
    """re 更换数据

    Args:
        _r (str): 正则表达式
        data (str): 数据
        new_data (str): 替换的数据

    Returns:
        str: 更新后结果
    """
    return re.sub(_r, new_data, data)

############ re ############

############ check ############

# 检查数据 v2
def check_exist_type(data: dict, not_null_list: list, data_type_dict: dict) -> dict:
    """数据检查 存在 & 类型

    Args:
        data (dict): 数据体
        not_null_list (list): 不能为空列表
        data_type_dict (dict): 数据值类型

    Raises:
        PermissionError: 缺少参数 code: fail_data_params_miss
        TypeError: 类型错误 code: fail_data_params_type

    Returns:
        dict: 检查结果 code: success_data_check
    """
    res = {
        'code': None
    }
    # 非空数据检查
    if set(not_null_list) > set(data):
        res.update({
            'code': 'fail_data_params_miss',
            'params_miss': set(not_null_list) - set(data)
        })
    if res.get('code'): raise PermissionError(res)
    # 数据类型检查
    for k, v in data.items():
        if k in data_type_dict.keys():
            # 类型不正确时
            if not isinstance(v, data_type_dict.get(k)):
                try:
                    data[k] = data_type_dict.get(k)(v)
                except:
                    res.update({
                        'code': 'fail_data_params_type',
                        'params': k
                    })
                    raise TypeError(res)
        else:...
    if not res.get('code'): res.update({'code': 'success_data_check'})
    return res

# 检查 key 是否存在 不存在抛出异常
def check_key_isexit_strict(data: dict, key_list:list) -> None:
    """检查 key 是否存在

    Args:
        data (dict): 要检查数据
        key_list (list): 数据key列表

    Raises:
        PermissionError: 哪些 key (list) 不存在
    """
    res = set(key_list) & set(data)
    if res != set(key_list):
        raise PermissionError(list(set(key_list) - res))

############ check ############

#################### [base64 加密解密] ####################
import base64

# txt -> base64
def txt_base64(txt: str) -> str:
    """ txt -> base64
    param:
        txt: 要编码数据
    return: 编码后文本
    """
    return base64.b64encode(txt.encode('utf-8')).decode("utf-8")

# base64 -> txt
def base64_txt(txt: str) -> str:
    """ base64 -> txt
    param:
        txt: 要解码的数据
    return: 解码后文本
    """
    return base64.b64decode(txt.encode('utf-8')).decode("utf-8")

#################### [base64 加密解密] ####################

#################### [url 编码解码] ####################
from urllib import parse

def urldecode(txt: str) -> str:
    return parse.unquote(txt)

def urlencode(txt: str) -> str:
    return parse.quote(txt)

#################### [url 编码解码] ####################
