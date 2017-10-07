#!-*-coding:utf8-*-
import hashlib
import os
import datetime

def sum_md5(filename):
    """function:计算输入文件的md5信息"""
    if not os.path.isfile(filename):
        return ""
    if not os.path.exists(filename):
        return ""
    myhash = hashlib.md5()
    f = file(filename,'rb')
    while True:
        b = f.read(4096)
        if not b:
            break
        myhash.update(b)
    f.close()

    return myhash.hexdigest()

def sum_md5_version_2(filename):
    """function:计算输入文件的md5信息"""
    if not os.path.isfile(filename):
        return ""
    if not os.path.exists(filename):
        return ""
    myhash = hashlib.md5()
    with open(filename,'rb') as f:
        while 1:
            b = f.read(4096)
            if not b:
                break
            myhash.update(b)

    return myhash.hexdigest()

if __name__ == '__main__':
    filename = './utils.py'
    print sum_md5(filename)
    print sum_md5_version_2(filename)
