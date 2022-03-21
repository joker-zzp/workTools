import os
import sys
import timeit
from lib.conf import get_conf
from lib.log import Log_Json, Log_Txt


global CONF_PATH, CONF

CONF_PATH = 'configs/server.ini'
CONF = get_conf(CONF_PATH)
RUN_ENV = CONF.get('run').get('env')

base_run_text = \
'''

def main():
    print('hello world')

def __main__():main()
'''

def create_project(name:str, template = None):
    """创建脚本项目

    Args:
        name (string): 项目名称
    """
    global CONF, RUN_ENV
    # 非开发环境 不能创建项目
    if RUN_ENV != 'dev': return
    # 配置文件
    project_path = None
    if CONF := CONF.get('run'):
        project_path = CONF.get('project_path')
    else: raise Exception(f'Error: 缺少配置 "project_path".')
    # 检查设置文件夹是否存在 或者不是文件夹
    if not os.path.isdir(project_path):
        raise Exception(f'Error: 文件夹 "{project_path}" 不存在')
    root = f'{project_path}/{name}'
    # 判断项目是否存在
    if os.path.isdir(root):
        raise Exception('Error: 项目以存在')
    else:
        # 创建 项目文件夹
        os.mkdir(root)
    if not template:
        template = {
            'project': [
                {'dir': 'configs'},
                # {'dir': 'lib'},
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
        # 创建链接
        if i.get('link'):
            if os.path.isdir(project_dir):
                # 定义链接地址
                link_path = '../' * i.get('link').count('/') + project_dir
                # 创建链接
                os.symlink(link_path, i['link'])
            else:
                print('文件夹创建失败')
            # print(link_path)

    # 创建运行文件
    with open(f'{root}/run.py', 'w') as f:
        f.write(base_run_text)
            
def run_project(name, run_file = 'run'):
    global CONF

    LOG_CONF = CONF.get('log')
    # 载入日志配置
    log = Log_Txt(**LOG_CONF)
    # 打印 日志信息
    log.print(title='run_project', type='INFO', msg=f'run {name} start.')


    project_path = CONF.get('run').get('project_path')
    root = f'{project_path}/{name}'
    my_path = os.getcwd()

    new_path = os.path.join(my_path, root)

    if os.path.isdir(new_path):
        import importlib
        os.chdir(new_path)
        sys.path[0] = new_path
        # if RUN_ENV != 'dev':
        #     sys.path[0] = new_path
        pack = importlib.import_module(run_file)
        start_time = timeit.default_timer()
        pack.__main__()
        use_time = str(timeit.default_timer() - start_time)
        log.print(title='run_project', type='INFO', msg=f'run {name} over. use_time: {use_time} s')
    else:
        raise Exception(f'Error: path not exits "{new_path}"')

__all__ = [
    'RUN_ENV',
    'create_project',
    'run_project'
]
