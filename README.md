# workTools

Python 工具脚本项目集

[wiki](https://github.com/joker-zzp/workTools/wiki)

项目结构

configs     - 配置代码
lib         - 公共代码
utils       - 封装工具
src         - 主业务代码
run.py      - 入口程序

## 项目运行

python run.py -r hello_world

## 创建项目

环境配置 dev 
```ini
[run]
project_path = Project
; 运行环境 dev / test / online
env = dev
```

使用 命令创建项目

修改 run.py
```python
def main():
    """ 用于工程 开发/调试
    """
    
    # name = 'hello_world'
    # 本地测试
    name = 'test'

    template = {
        'project': [
            {'dir': 'configs', 'link': 0},
            # {'dir': 'doc', 'link': 0},
            {'dir': 'data', 'link': 0},
            {'dir': 'src', 'link': 0},
        ]
    }
    # 创建项目 根据模板 创建项目
    create_project(name, template)
    # 运行 / 调试 项目
    # run_project(name)
    pass
```

`python run.py`

