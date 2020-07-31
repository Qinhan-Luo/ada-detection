# -*- encoding: utf-8 -*-
'''
@Time : 2020/6/8 9:36 
@Author : qinhanluo
@File : CVseg.py 
@Software: PyCharm
@Description ： TODO
'''
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

def get_images(input_path):
    img_paths = []
    for (path, dirs, files) in os.walk(input_path):
        for filename in files:
            if filename.endswith('.tif'):
                img_paths.append(path + r'/' + filename)
    return img_paths

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

# TODO some more features may need
def feature_export(img):
    feature_channels = getGabor(img, build_filters())
    return feature_channels

def process_images(img_path):
    scale = 6
    img = cv2.imread(img_path)
    h, w = img.shape[:2]
    img = cv2.resize(img, (int(h / scale), int(w / scale)), interpolation=cv2.INTER_CUBIC)

    # convers the img into superpixels
    # TODO: the slic params need to consider
    slic = cv2.ximgproc.createSuperpixelSLIC(img, region_size=7, ruler=20.0)
    slic.iterate(10)

    mask_slic = slic.getLabelContourMask()
    label_slic = slic.getLabels()
    number_slic = slic.getNumberOfSuperpixels()
    mask_inv_slic = cv2.bitwise_not(mask_slic)
    # img_slic = cv2.bitwise_and(img, img, mask=mask_inv_slic)

    features = []
    channels = feature_export(img)
    color = ('b', 'g', 'r')

    for i in range(number_slic):
        e_feature = []
        e_mask = cv2.inRange(label_slic, i, i)
        e_pixels = (e_mask == 255).sum()

        for j in range(len(channels)):
            e_channels = channels[j]
            for k, _ in enumerate(color):
                hist = cv2.calcHist([e_channels], [k], e_mask, [16], [0, 256])
                e_feature.append(hist / (e_pixels + 1))  # simple avoid / zero
        features.append(np.asarray(e_feature).flatten())

    # get features and labels to start train the images
    label_img_paths = img_path.replace('imgs', 'masks')
    label_img_paths = label_img_paths.replace('tif', 'jpg')
    print(label_img_paths)
    image_labels = cv2.imread(label_img_paths)

    label_h, label_w = image_labels.shape[:2]
    convert_labels = cv2.resize(image_labels, (int(label_h / scale), int(label_w / scale)),
                                interpolation=cv2.INTER_CUBIC)

    convert_labels = cv2.cvtColor(convert_labels, cv2.COLOR_RGB2GRAY)
    labels = []

    for m in range(number_slic):
        e_label = cv2.inRange(label_slic, m, m)
        t_label = cv2.bitwise_and(convert_labels, convert_labels, mask=e_label)

        t_sum = (t_label == 255).sum()
        e_sum = (e_label == 255).sum()
        if t_sum >= 0.5 * e_sum:
            labels.append(1)
        else:
            labels.append(0)
    return features, labels

if __name__ == "__main__":
    paths = get_images(r"D:\DataSets\adaWaters\imgs")

    t_features = []
    t_labels = []
    for images in paths:
        i_features, i_labels = process_images(images)
        t_features.append(i_features)
        t_labels.append(i_labels)
        # t_features = np.concatenate((t_features, i_features), axis=0)
        # t_labels = np.concatenate((t_labels, i_labels), axis=0)
    np.savez("water_cover", features=t_features, labels=t_labels)
    print("process success.")