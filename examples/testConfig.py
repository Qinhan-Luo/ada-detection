# -*- encoding: utf-8 -*-
'''
@Time : 2020/6/29 11:15 
@Author : qinhanluo
@File : testConfig.py 
@Software: PyCharm
@Description ： TODO
'''
import os
import cv2
import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import logging as log
from pprint import pformat
from torch.utils.data import DataLoader
from torchsummary import summary

from utils.envs import initEnv
from models.chns_compute import chnsCompute
from models.data.dataset import BasicDataset
from models.unet.unet_model import UNet

import sys
sys.path.insert(0, '.')

if __name__ == '__main__':
    train_flag = 1
    model_name = 'acf'
    config = initEnv(train_flag=train_flag, model_name=model_name)
    log.info('Config\n\n%s\n' % pformat(config))

    net = UNet(n_channels=3, n_classes=1, bilinear=True)
    device = 'cuda'
    net = net.to(device)
    summary(net, (3,244,244))

    dir_root = config.get('data_root_dir', None)
    dataset = config.get('dataset', None)

    if dir_root is not None and dataset is not None:
        img_dir = os.path.join(dir_root, dataset, 'image')
        mask_dir = os.path.join(dir_root, dataset, 'label')
        dataset = BasicDataset(img_dir, mask_dir, 1.0)
        log.info('Load images from %s, labels from %s\n', img_dir, mask_dir)

    train_loader = DataLoader(dataset, batch_size=1, shuffle=True, num_workers=2)

    img = cv2.imread(r'C:\Users\muchun\Desktop\02\01.tif')

    height, width = img.shape[:2]
    scale = 20
    img = cv2.resize(img, (int(height/scale), int(width/scale)), interpolation=cv2.INTER_CUBIC)
    chnns = chnsCompute(img, config)
    _, _, c = chnns.shape

    features = chnns.reshape(-1, c)

    labels = cv2.imread(r"C:\Users\muchun\Desktop\02\01.jpg")
    labels = cv2.cvtColor(labels, cv2.COLOR_BGR2GRAY)
    labels = cv2.resize(labels, (int(height / scale), int(width / scale)))
    test = labels == 255
    test = test.reshape(-1, 1)
    # labels = cv2.bitwise_and(labels == 255, np.ones_like(labels))
    labels = labels.reshape(-1, 1)
    labels = np.squeeze(labels)
    labels[labels>0] = 1

    tsne = TSNE(n_components=2, init="pca", random_state=0)

    X_tsne = tsne.fit_transform(features)
    plt.figure()
    plt.scatter(X_tsne[:, 0], X_tsne[:, 1], c=labels)
    plt.colorbar()
    plt.show()