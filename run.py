from lib.conf import get_conf
import importlib
# import getopt
# import sys
import os

global CONF_PATH, CONF

CONF_PATH = 'configs/server.ini'
CONF = get_conf(CONF_PATH)

def create_project(name):
    """创建脚本项目

    Args:
        name (string): 项目名称
    """
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
        pass
        # raise Exception('Error: 项目以存在')
    else:
        # 创建 项目文件夹
        os.mkdir(root)
    template = {
        'server': [
            {'dir': 'configs', 'link': f'configs/{name}'},
            {'dir': 'doc', 'link': f'doc/{name}'},
            {'dir': 'lib', 'link': f'lib/{name}'},
            {'dir': 'log', 'link': f'log/{name}'},
            {'dir': 'src', 'link': f'src/{name}'},
            {'dir': 'tmp', 'link': f'tmp/{name}'},
        ]
    }
    
    for i in template.get('server'):
        if os.path.isdir(i['link']):
            # 文件夹存在 跳过
            print(f"Folder exists: {i['link']}")
            continue
        else:
            # 创建真实文件夹
            os.makedirs()
        # 判断文件夹是否存在
        if os.path.isdir(i['link']):
            dst_path =  f"{root}/{i['dir']}"
            src_path = '../'*dst_path.count('/')+i['link']
            print(src_path)
            os.symlink(src_path, dst_path)
        print(f"{root}/{i['dir']} -> {i['link']}")
        # 创建 项目下子文件夹
        # 创建 链接 到项目下对应文件夹
    # os.mkair()

def run_project(name, run_file = 'run'):
    global CONF
    if CONF := CONF.get('run'):
        project_path = CONF.get('project_path')
    else: raise Exception(f'Error: 缺少配置 "project_path".')
    root = f'{project_path}/{name}'
    my_path = os.getcwd()
    new_path = os.path.join(my_path, root)
    if os.path.isdir(new_path):
        # 路径存在
        print(f'run: {name} -> {run_file}\n')
        # 进入项目目录
        os.chdir(new_path)
        # 执行包 __main__ 方法
        pack = importlib.import_module(run_file)
        print(dir(pack))

        pack.__main__()
        print('\nrun: over.')
        pass
    else:
        # 路径不存在
        raise Exception(f'Error: path not exits "{new_path}"')


if __name__ == "__main__":
    # 创建项目
    # create_project('test')
    # 运行项目
    # run_project('test')
    # print(sys.argv)
    pass