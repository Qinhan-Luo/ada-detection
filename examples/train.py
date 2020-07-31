# -*- encoding: utf-8 -*-
'''
@Time : 2020/6/9 15:15 
@Author : qinhanluo
@File : train.py 
@Software: PyCharm
@Description ： TODO
'''
import numpy as np
from sklearn import svm
import pickle

if __name__ == '__main__':
    npz = np.load('../weights/water_cover.npz')
    features_list = npz['features']
    labels_list = npz['labels']

    train_samples = np.array(features_list[0])
    train_labels = np.array(labels_list[0])

    for i in range(1, 12):
        train_samples = np.concatenate((train_samples, features_list[i]), axis=0)
        train_labels = np.concatenate((train_labels, labels_list[i]), axis=0)

    C = 1.0
    models = svm.SVC(kernel='rbf', gamma=0.7, C=C)

    Model = models.fit(train_samples, train_labels)

    s = pickle.dumps(Model)
    f = open('water_cover_svm.model', 'wb+')
    f.write(s)
    f.close()
    print("Done")