# -*- encoding: utf-8 -*-
'''
@Time : 2020/6/29 10:23 
@Author : qinhanluo
@File : gradient.py
@Software: PyCharm
@Description ： TODO
'''
import cv2

'''
TODO
'''
def gradientMag(img, config):
    enabled = config.get('enabled', False)
    if not enabled:
        return None
    h, w, c = img.shape
    if c > 1:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    gradient_values_x = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
    gradient_values_y = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)

    absX = cv2.convertScaleAbs(gradient_values_x)
    absY = cv2.convertScaleAbs(gradient_values_y)

    ret = cv2.addWeighted(absX, 0.5, absY, 0.5, 0)
    return ret

'''
TODO
'''
def gradientHist(img, config):
    enabled = config.get('enabled', False)
    if not enabled:
        return None
    h, w, c = img.shape
    if c>1:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    gradient_value_x = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
    gradient_value_y = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)

    gradient_magnitude = cv2.addWeighted(cv2.convertScaleAbs(gradient_value_x), 0.5, cv2.convertScaleAbs(gradient_value_y), 0.5, 0)
    gradient_angle = cv2.phase(gradient_value_x, gradient_value_y, angleInDegrees=True)

    num_channels = config.get('num_orients', 6)

    for i in range(num_channels):
        pass