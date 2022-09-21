from src.project import create_project, run_project, RUN_ENV
import getopt
import sys


def main():
    """ 用于工程 开发/调试
    """
    
    name = 'hello_world'
    # 本地测试
    name = 'test'
    # name = 'yangyang'
    name = 'mediatrack_bug'

    """项目目录模板
        项目基本 目录介绍 
            configs 脚本配置文件
            lib     公共代码库 通用代码或定制代码存放位置
            log     脚本日志
            src     主体代码 按功能需求进行 逻辑 流程 编写
            tmp     临时存放路径
            run.py  运行 / 调试/ 打包 / 入口文件
    """
    template = {
        'project': [
            {'dir': 'configs', 'link': 0},
            # {'dir': 'doc', 'link': 0},
            {'dir': 'data', 'link': 0},
            {'dir': 'src', 'link': 0},
        ]
    }
    # 创建项目 根据模板 创建项目
    # create_project(name, template)
    # 运行 / 调试 项目
    run_project(name)
    pass

if __name__ == "__main__":
    opts, args = getopt.getopt(sys.argv[1:], 'c:r:', ['create','run'])
    if opts:
        # print(opts)
        if len(opts) == 1:
            if opts[0][0] in ['-c', '--create']:
                if opts[0][0] == '-c':
                    if RUN_ENV == 'online':
                        raise Exception(f'线上环境禁止创建项目.')
                    name = opts[0][1]
                    create_project(name)
                if opts[0][0] == '--create':
                    if RUN_ENV == 'online':
                        raise Exception(f'线上环境禁止创建项目.')
                    name = args[0]
                    create_project(name)
            if opts[0][0] in ['-r', '--run']:
                if opts[0][0] == '-r':
                    name = opts[0][1]
                    run_project(name)
                if opts[0][0] == '--run':
                    name = args[0]
                    run_project(name)
        else:
            print('error: 参数过多')
    else:
        # 直接运行脚本
        if RUN_ENV == 'dev':
            main()
