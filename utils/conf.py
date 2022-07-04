from lib import conf


__doc__ = \
"""
配置文件读取模块
"""

class Base:

    def __init_subclass__(cls):
        name = str(cls.__name__).split('_')[-1].upper()
        if name == 'INI':
            cls.get_conf = conf.get_ini_conf
            cls.get_conf.__doc__ = conf.get_ini_conf.__doc__
        if name == 'YAML':
            cls.get_conf = conf.get_yaml_conf
            cls.get_conf.__doc__ = conf.get_ini_conf.__doc__

    def get_conf():...

class Conf_InI(Base):...
class Conf_Yaml(Base):...


__all__ = [
    'Conf_InI',
    'Conf_Yaml'
]