# -*- encoding: utf-8 -*-
'''
@Time : 2020/6/30 14:25 
@Author : qinhanluo
@File : color.py 
@Software: PyCharm
@Description ： TODO
'''
import cv2

color_transform = {
    'hsv': cv2.COLOR_BGR2HSV,
    'luv': cv2.COLOR_BGR2LUV,
    'gray': cv2.COLOR_BGR2GRAY
}

def colorConvert(img, config):
    enabled = config.get('enabled', False)
    _, _, c = img.shape
    if not enabled:
        return None
    if c != 3:
        return None
    ret = None
    color_space = config.get('color_space', None)
    if color_space is not None:
        ret = cv2.cvtColor(img, color_transform[color_space])
    return ret