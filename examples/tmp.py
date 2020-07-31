# -*- encoding: utf-8 -*-
'''
@Time : 2020/6/8 18:59 
@Author : qinhanluo
@File : tmp.py 
@Software: PyCharm
@Description ： TODO
'''
import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from sklearn import  datasets
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn import metrics

if __name__ == "__main__":
    digits = datasets.load_digits(n_class=6)
    data = digits.data
    label = digits.target
    # features = np.load("d.npy")
    npz = np.load('../weights/water_cover.npz')

    xx = npz['features']
    yy = npz['labels']
    print(np.isnan(xx).any())
    for i in range(12):
        print(xx[i].shape)
        print(yy[i].shape)

    # idx = np.where(~np.isnan(features))
    # features[np.isnan(features)] = 0

    pass
    # # print(idx)
    # # features = features[:-10, :]
    # print(np.isnan(features).any())
    # print(features.shape)
    #
    # labels = np.load("label.npy")
    # # labels = labels[:-10]
    # print(np.isnan((features.any())))
    # print(labels.shape)
    #
    # # model = LogisticRegression()
    # # model.fit(features, labels)
    # # print(model)
    # #
    # # print("RESULT")
    # # expected = labels
    # # predicted = model.predict(features)
    # # print(metrics.classification_report(expected, predicted))
    # tsne = TSNE(n_components=2, init="pca", random_state=0)
    # X_tsne = tsne.fit_transform(features)
    # plt.figure()
    # plt.scatter(X_tsne[:,0], X_tsne[:,1], c=labels)
    # plt.colorbar()
    # plt.show()
    # # print(labels.sum())