import configparser

def get_ini_conf(path:str) -> dict:
    """获取配置信息

    Args:
        path (str): 配置文件路径

    Returns:
        dict: 配置文件数据
    """
    conf = configparser.ConfigParser()
    conf.read(path, encoding='utf-8-sig')
    return dict(conf._sections)

def get_yaml_conf(path:str):
    """获取yaml配置

    Args:
        path (str): 文件路径

    Returns:
        dict: 配置结果
    """
    import yaml
    import os
    data = {}
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
    return data
