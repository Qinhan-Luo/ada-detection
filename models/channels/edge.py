# -*- encoding: utf-8 -*-
'''
@Time : 2020/6/29 10:24 
@Author : qinhanluo
@File : edge.py 
@Software: PyCharm
@Description ： TODO
'''
import cv2
import numpy as np

'''
TODO
'''
def edge(img, config):
    h, w, c = img.shape
    if c > 1:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    #TODO, some params to set
    edge = cv2.Canny(img, 100, 200)
    return edge

if __name__ == '__main__':
    pass