import functools

# 异常捕获
def error_capture(func):
    @functools.wraps(func)
    def f(*args, **kwargs):
        res = {}
        try:
            res = {
                'code': 1,
                'return': func(*args, **kwargs)
            }
        except Exception as e:
            res = {
                'code': -1,
                'type': type(e),
                'func': func.__name__,
                'args': args,
                'kwargs': kwargs,
                'error_info': e
            }
        finally:
            return res
    return f
