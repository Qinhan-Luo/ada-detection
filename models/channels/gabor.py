# -*- encoding: utf-8 -*-
'''
@Time : 2020/6/29 10:23 
@Author : qinhanluo
@File : gabor.py 
@Software: PyCharm
@Description ： TODO
'''
import cv2
import numpy as np

'''
TODO, add the kernel size
'''
def buildFilters():
    filters = []
    ksize = [11]
    lamda = np.pi/2.0
    for theta in np.arange(0, np.pi, np.pi/8):
        for K in range(1):
            kern = cv2.getGaborKernel((ksize[K], ksize[K]), 1.0, theta, lamda, 0.5, 0, ktype=cv2.CV_32F)
            kern /= 1.5*kern.sum()
            filters.append(kern)
    return filters

'''
TODO, modify
'''
def getGabor(img, config):
    ret = None
    enabled = config.get('enabled', False)
    if not enabled:
        return ret

    res = None
    filters = buildFilters()

    for i in range(len(filters)):
        accum = np.zeros_like(img)
        for kern in filters[i]:
            fimg = cv2.filter2D(img, cv2.CV_8UC1, kern)
            accum = np.maximum(accum, fimg, accum)

        if res is None:
            res = np.asarray(accum)
        else:
            res = np.concatenate([np.asarray(accum), res], axis=2)

    return res

if __name__ == '__main__':
    #TODO, add some tests and visuals the filters.
    pass