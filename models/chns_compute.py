# -*- encoding: utf-8 -*-
'''
@Time : 2020/6/29 10:16 
@Author : qinhanluo
@File : chns_compute.py 
@Software: PyCharm
@Description ： TODO
'''
import cv2
import numpy as np
import logging as log

from models.channels.edge import edge
from models.channels.gradient import gradientMag, gradientHist
from models.channels.gabor import getGabor
from models.channels.cnn import cnn
from models.channels.color import colorConvert

'''
TODO,
'''
func_dictory = {
    'Color': colorConvert,
    'Gabor': getGabor,
    'GradientMag': gradientMag,
    'GradientHist': gradientHist,
    'Cnn': cnn
}

'''
TODO, compute features based on config
'''
def chnsCompute(img, config):
    if not config.__contains__('features'):
        log.error('the config not contain features')
        return None

    features = config['features']
    chnns = None
    for k, v in features.items():
        wrapper_func = func_dictory.get(k, None)
        if wrapper_func is not None:
            img2 = wrapper_func(img, v)

            if img2 is not None:
                if img2.ndim == 2:
                    img2 = img2[:, :, np.newaxis]

                if chnns is None:
                    chnns = np.asarray(img2)
                else:
                    chnns = np.concatenate([chnns, np.asarray(img2)], axis=2)
    return chnns

'''
TODO, 
'''
def chnsAdd(img, chns):
    pass

if __name__ == '__main__':
    img = cv2.imread(r'C:\Users\muchun\Desktop\02\01.tif')
    c1 = edge(img)
    c2, c3 = gradientMag(img)
    cv2.imwrite("ttt.jpg", c2)
    pass