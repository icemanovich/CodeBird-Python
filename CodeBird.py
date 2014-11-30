# coding=utf-8

__author__ = 'ignat'
__date__ = '01.12.14 0:04'


class CodeBird:

    instance = None

    # make singletone instance




    pass




class OnlyOne:
    class __OnlyOne:
        def __init__(self, arg):
            self.val = arg
        def __str__(self):
            return repr(self) + self.val
    instance = None
    def __init__(self, arg):
        if not OnlyOne.instance:
            OnlyOne.instance = OnlyOne.__OnlyOne(arg)
        else:
            OnlyOne.instance.val = arg
    def __getattr__(self, name):
        return getattr(self.instance, name)








# 1) Prepare global CONSTANTS
# 2) Make class

if __name__ == '__main__':
    print("Start")

    x = OnlyOne('sausage')
    print(x)
    y = OnlyOne('eggs')
    print(y)
    z = OnlyOne('spam')
    print(z)
    print(x)
    print(y)
    print('x')
    print('y')
    print('z')