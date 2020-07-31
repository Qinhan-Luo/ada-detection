# -*- encoding: utf-8 -*-
'''
@Time : 2020/6/28 9:33 
@Author : qinhanluo
@File : fileproc.py.py 
@Software: PyCharm
@Description ： TODO
'''
import os

def safeMakeDir(tdir):
    if not os.path.isdir(tdir):
        os.mkdir(tdir)

def safeMakeDirs(tdir):
    if not os.path.isdir(tdir):
        os.makedirs(tdir)