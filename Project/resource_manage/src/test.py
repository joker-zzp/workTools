class Base():

    def __init__(self):
        self.t = None

    def get_t(self):
        print(self.t)


class A(Base):

    def __init__(self):
        self.t = 'A'

class B(Base):

    def __init__(self):
        self.t = 'B'

    def get_t(self):
        print('haha')

class C(Base):

    def __init__(self):
        self.t = 'C'

__all__ = [
    'A',
    'B',
    'C',
]