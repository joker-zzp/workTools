from src import test

def Eng():

    def __fux(func):

        def f(self, *args, **kwargs):
            print(self)
            return func(self, *args, **kwargs)
        return f()

    class TmpEng(*[getattr(test, i) for i in test.__all__]):

        def __init__(self):...

        def test(func):

            def f(self, *args, **kwargs):
                print(f'--> {self.func}')
                pack = getattr(test, self.func)
                print(func.__name__)
                return getattr(pack, func.__name__)(self, *args, **kwargs)
            return f

        def a(self):
            test.A.__init__(self)
            self.func = 'A'
        
        def b(self):
            test.B.__init__(self)
            self.func = 'B'

        def c(self):
            test.C.__init__(self)
            self.func = 'C'

        @test
        def get_t(self):...

    return TmpEng()

def main():
    a = Eng()
    a.a()
    a.get_t()
    pass
