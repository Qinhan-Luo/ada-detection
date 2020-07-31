# -*- encoding: utf-8 -*-
'''
@Time : 2020/6/9 16:14 
@Author : qinhanluo
@File : test.py 
@Software: PyCharm
@Description ： TODO
'''
import numpy as np
from sklearn import svm
import pickle
import cv2

def build_filters():
    filters = []
    ksize = [11]
    lamda=np.pi/2.0
    for theta in np.arange(0, np.pi, np.pi/8):
        for K in range(1):
            kern = cv2.getGaborKernel((ksize[K], ksize[K]), 1.0, theta, lamda, 0.5, 0, ktype= cv2.CV_32F)
            kern /= 1.5*kern.sum()
            filters.append(kern)
    # plt.figure(1)
    #
    # for temp in range(len(filters)):
    #     plt.subplot(8, 1, temp+1)
    #     plt.imshow(filters[temp])
    # plt.show()
    return filters

def getGabor(img, filters):
    res = []
    for i in range(len(filters)):
        accum = np.zeros_like(img)
        for kern in filters[i]:
            fimg = cv2.filter2D(img, cv2.CV_8UC1, kern)
            accum = np.maximum(accum, fimg, accum)
        res.append(np.asarray(accum))
    # plt.figure(2)
    # for temp in range(len(res)):
    #     plt.subplot(8, 1, temp + 1)
    #     plt.imshow(res[temp], cmap='gray')
    # plt.show()
    return res

def feature_export(img):
    feature_channels = getGabor(img, build_filters())
    return feature_channels

if __name__ == '__main__':
    f2 = open(r"data\water_cover_svm.model", 'rb')
    s2 = f2.read()
    model = pickle.loads(s2)
    img = cv2.imread(r"C:\Users\muchun\Desktop\02\01.tif")
    # img = cv2.imread(r"C:\Users\muchun\Desktop\xu\HZ_01_wgs84.tif")
    # img = cv2.imread(r"D:\DataSets\adaWaters\imgs\17.tif")
    scale = 3
    h, w = img.shape[:2]
    # print(img.shape)
    img = cv2.resize(img, (int(w / scale), int(h / scale)), interpolation=cv2.INTER_CUBIC)
    # print(img.shape)
    slic = cv2.ximgproc.createSuperpixelSLIC(img, region_size=7, ruler=20.0)
    slic.iterate(10)

    mask_slic = slic.getLabelContourMask()
    label_slic = slic.getLabels()
    number_slic = slic.getNumberOfSuperpixels()
    mask_inv_slic = cv2.bitwise_not(mask_slic)
    img_slic = cv2.bitwise_and(img, img, mask=mask_inv_slic)
    cv2.imwrite("res.jpg", img_slic) # save result

    channels = feature_export(img)
    color = ('b', 'g', 'r')

    prediction_imgs = np.zeros(img.shape[:2], dtype=np.uint8)
    # print(prediction_imgs.shape)
    for i in range(number_slic):
        e_feature = []
        e_mask = cv2.inRange(label_slic, i, i)
        e_pixels = (e_mask == 255).sum()

        for j in range(len(channels)):
            e_channels = channels[j]
            for k, _ in enumerate(color):
                hist = cv2.calcHist([e_channels], [k], e_mask, [16], [0, 256])
                e_feature.append(hist / (e_pixels + 1))  # simple avoid / zero
        e_feature = np.asarray(e_feature).flatten()
        e_feature = e_feature.reshape(1,-1)
        e_predection = model.predict(e_feature)
        if e_predection == 1:
            # print(e_mask.shape)
            prediction_imgs = cv2.add(prediction_imgs, e_mask)

    prediction_imgs = cv2.resize(prediction_imgs, (w, h))
    cv2.imwrite("prediction.jpg", prediction_imgs)
    pass