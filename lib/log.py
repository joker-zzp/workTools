import time
import json
import os
import re

class Log_Base:

    LOG_TYPE = None
    LOG_SETTING = 1
    Attribute = {
        'ERROR': -1,
        'UNKNOWN': 0,
        'INFO': 1,
    }
    Log_Format_T = {
        'T': '时间戳',
        'PID': '进程ID'
    }

    def __init__(self, path, lvlup, template, error_path=None, **kwargs):
        """日志初始化配置

        Args:
            path (str): 日志文件输出路径.
            lvlup (int): 日志输出等级.
            template (str): 日志模板.
            error_path (str, None): 异常日志输出路径. Defaults to None.
            kwargs (str): 可选配置
                size (str): 单个日志文件大小
        """
        self.path:str = path
        self.lvlup:int = lvlup
        self.template:str = template
        self.error_path:str = error_path
        # self.__dict__(kwargs)
        for k, v in kwargs.items():
            setattr(self, k, v)
        pass

    def __init_subclass__(cls):
        # 定义日志类型
        cls.LOG_TYPE = str(cls.__name__).split('_')[-1].upper()

    def print(self, **kwargs) -> None:
        """打印日志

        kwargs: 自定义内容

        Return:
        """
        if self.LOG_TYPE == 'TXT':
            # print(self.template)
            print(self._txt_format(self.template, **kwargs))
        if self.LOG_TYPE == 'JSON':
            print(self._josn_format(self.template, **kwargs))

    def output(self, **kwargs) -> None:
        root_dir = os.getcwd()
        doc = None
        # 文件处理
        if self.LOG_TYPE == 'TXT':
            doc = self._txt_format(self.template, **kwargs)
        if self.LOG_TYPE == 'JSON':
            doc = self._josn_format(self.template, **kwargs)
        # print(doc)
        
        if os.path.isfile(self.path):
            # 文件存在写入
            pass
        else:
            # 文件不存在 创建写入
            if self.path:
                # 判断是否是绝对路径
                is_abs = os.path.isabs(self.path)
                if is_abs:
                    # 创建文件夹
                    path = self.path.split('/')[0:-1]
                    # print(path)
                    os.makedirs(self)
                else:
                    # 创建文件夹
                    path = os.path.join(*self.path.split('/')[0:-1])
                    if not os.path.isdir(path):
                        os.makedirs(path)
                    # 创建文件
                    
            else: raise Exception('Error: 不可能出现的错误.')

    def _txt_format(self, t, **kwargs):
        fstr = t
        doc = self._args_format_(**kwargs)
        fsr = r'\{(.*?)\}'
        fs_keys = re.compile(fsr).findall(fstr)
        for i in fs_keys:
            if i not in doc.keys():
                doc.update({i: None})
        return fstr.format(**doc)
    
    def _josn_format(self, t, **kwargs):
        fdict = json.loads(t)
        fj_keys = fdict.keys()
        doc = self._args_format_(**kwargs)
        for k, v in fdict.items():
            if k not in doc.keys():
                doc.update({k: None})
        return json.dumps(self._up_keys_(fdict, doc))

    @classmethod
    def _up_keys_(cls, t, obj):
        return {v:obj.get(k) for k, v in t.items()}
    @classmethod
    def _args_format_(cls, **kwargs):
        doc = {
            'T': time.time(),
            'PID': os.getpid(),
        }
        if kwargs:
            doc.update(kwargs)
        return doc

class Log_Txt(Log_Base):...
class Log_Json(Log_Base):...
