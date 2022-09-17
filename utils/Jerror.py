"""
自建异常类

继承 BaseError 即可
"""


class BaseError(Exception):

    def __init__(self, *args):
        self.res = Exception(*args)
        self.__str__()
    
    def __str__(self):
        return f'[{self.__class__.__name__}]: {self.res}'
