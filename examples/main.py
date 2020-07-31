# -*- encoding: utf-8 -*-
'''
@Time : 2020/6/7 10:43 
@Author : qinhanluo
@File : main.py 
@Software: PyCharm
@Description ： TODO
'''
import os
from skimage import io
from skimage.segmentation import slic, mark_boundaries
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    img = io.imread(r'C:\Users\muchun\Desktop\8bit\1_8bit.tif')
    segments = slic(img, n_segments=1000, compactness=20, enforce_connectivity=True, convert2lab=True)
    print(segments.shape)

    area = np.bincount(segments.flat)
    w, h = segments.shape

    out = mark_boundaries(img, segments)

    plt.subplot(111)
    plt.imshow(out)
    plt.show()