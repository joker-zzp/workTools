import os
import sys
import time
from utils.conf import Conf_InI as InI
from utils.Jlog import Log_Json, Log_Txt

global CONF_PATH, CONF

CONF_PATH = 'configs/server.ini'
CONF = InI.get_conf(CONF_PATH)
RUN_ENV = CONF.get('run').get('env')

base_run_text = \
'''# 在此 导入 main 方法替换此main方法 使用 from src.main import main

def main():
    print('hello world')

def __main__(): main()

# 项目独立运行时
if __name__ == "__main__":
    __main__()
'''

__all__ = [
    'RUN_ENV',
    'create_project',
    'run_project',
]

def project_info(name: str) -> dict:
    """项目信息

    Args:
        name (str): 项目名称

    Returns:
        dict: 项目信息
    """
    global CONF
    project_conf = CONF.get('project')
    # 存放项目的路径 过滤 末尾 路径符合 / 和 \
    project_conf_path = project_conf.get('path')[-1] if project_conf.get('path')[-1] in ['/', '\\'] else project_conf.get('path')
    # 项目相对路径
    project_root_path = name if project_conf_path in name else f'{project_conf_path}/{name}'
    # 项目名称
    project_name = project_root_path[len(project_conf_path) + 1:]

    res = {
        'project_name': project_name,
        'project_root_path': project_root_path,
        'project_conf_path': project_conf_path,
        'project_conf_print': project_conf.get('print_name'),
    }
    # print(res)
    return res

def _logout(o:Log_Txt, log_info:dict, msg: str = None):
    if msg:
        log_info.update({'msg': msg})
    o.output(**log_info)

# 创建 项目
def create_project(name:str, template = None):
    """创建脚本项目

    Args:
        name (string): 项目名称
    """
    global RUN_ENV, CONF
    # log 设置
    LOG_CONF = CONF.get('log')
    # 载入日志配置
    log = Log_Txt(**LOG_CONF)
    
    # 非开发环境 不能创建项目
    if RUN_ENV != 'dev': return
    # 项目信息
    p_info = project_info(name)
    # 项目名称
    p_name = p_info.get('project_name')

    # 打印 日志信息
    log_info = {
        'title': 'create_project',
        'type': 'INFO',
        'msg': f'create {p_name} start.'
    }
    _logout(log, log_info)
    # 配置文件
    project_conf_path = p_info.get('project_conf_path')
    if not project_conf_path: raise Exception(f'Error: 缺少配置 "project_path".')
    # 检查设置文件夹是否存在 或者不是文件夹
    if not os.path.isdir(project_conf_path): raise Exception(f'Error: 文件夹 "{project_conf_path}" 不存在')
    root = p_info.get('project_root_path')
    # 判断项目是否存在
    if os.path.isdir(root):
        _logout(log, log_info, msg = f'Error: {p_name} 项目以存在')
        raise Exception('Error: 项目以存在')
    else:
        # 创建 项目文件夹
        os.mkdir(root)
        _logout(log, log_info, msg = f'mkdir {root} is ok!')

    if not template:
        template = {
            'project': [
                {'dir': 'configs'},
                {'dir': 'src'},
            ]
        }

    # 根据模板创建文件目录
    for i in template.get('project'):
        # 创建项目文件夹
        project_dir = os.path.join(root, i.get('dir'))
        if os.path.exists(project_dir):
            continue
        else:
            os.makedirs(project_dir)
            _logout(log, log_info, msg = f'mkdir {project_dir} is ok!')
    # 创建运行文件
    with open(f'{root}/run.py', 'w') as f:
        f.write(base_run_text)
        _logout(log, log_info, msg = f'touch run.py is ok!')
    _logout(log, log_info, msg = f'create {p_name} over.')

# 运行 项目
def run_project(name: str, run_file: str = 'run'):
    """运行项目

    Args:
        name (str): 项目名称
        run_file (str, optional): 运行项目文件. Defaults to 'run'.
    """
    global CONF

    LOG_CONF = CONF.get('log')
    # 载入日志配置
    log = Log_Txt(**LOG_CONF)
    # 项目信息
    p_info = project_info(name)
    # 项目名称
    p_name = p_info.get('project_name')

    # 打印 日志信息
    log_info = {
        'title': 'run_project',
        'type': 'INFO',
        'msg': f'run {p_name} start.'
    }

    _logout(log, log_info)    
    # 当前目录
    current_path = os.getcwd()
    # 项目绝对路径
    p_abs_path = os.path.join(current_path, p_info.get('project_root_path'))
    # 打印项目名
    if p_info.get('project_conf_print'):
        # 运行项目的真正名称
        __symbol = '#'
        __ps = __symbol * (len(p_name) + 10)
        __space = ' ' * 4
        print(f'{__ps} \n{__symbol + __space + p_name + __space + __symbol} \n{__ps} \n>>>')

    # 运行脚本
    if os.path.isdir(p_abs_path):
        import importlib
        # 改变当前工作目录
        os.chdir(p_abs_path)
        sys.path[0] = p_abs_path
        # 导入 运行包
        pack = importlib.import_module(run_file)
        # 运行 主文件 的 __main__ 方法
        start_time = time.time_ns()
        pack.__main__()
        run_time = time.time_ns() - start_time
        # 写入日志
        _logout(log, log_info, msg = f'run {p_name} over. run_time: {run_time} ns.')
        # 回到 当前项目目录
        os.chdir(current_path)
    else:
        log_info.update({'type': 'ERROR', 'msg': f'path not exits "{p_abs_path}"'})
        # 输出结果 写入日志
        _logout(log, log_info)

# 打包 项目
def pack_project(name: str):
    global CONF

    LOG_CONF = CONF.get('log')
    # 项目信息
    p_info = project_info(name)
    pass
