#!/usr/bin/evn python
# coding=utf-8

import os
import sys


def datailtrace():
    '''获取程序当前运行的堆栈信息'''
    retStr = ''
    f = sys._getframe()
    f = f.f_back  # first frame is detailtrace,ignore it
    while hasattr(f, 'f_code'):
        co = f.f_code
        retStr = '%s(%s:%s)->' % (os.path.basename(co.co_filename), co.co_name, f.f_lineno) + retStr
        f = f.f_back
    return retStr

def get_cur_info():
    print(sys._getframe().f_code)
    print(sys._getframe().f_code.co_filename)
    print(os.path.basename(sys._getframe().f_code.co_filename))
    print(sys._getframe().f_code.co_name)
    print(sys._getframe().f_lineno)


if __name__ == '__main__':
    get_cur_info()

