import configparser
import yaml
import sys
import os


def get_yaml_conf(f_path):
    data = {}
    if os.path.exists(f_path):
        with open(f_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
    return data

def conf_dict(conf_obj, key):
    if conf_obj:
        if conf_obj.get(key):
            return conf_obj.get(key).copy()
    return {}

# conf ini 文件读取
def get_conf(path) -> dict:
    """获取配置文件信息

    Args:
        path (string): 配置文件路径

    Returns:
        dict: 配置文件数据
    """
    conf = configparser.ConfigParser()
    conf.read(path, encoding='utf-8-sig')
    return dict(conf._sections)
