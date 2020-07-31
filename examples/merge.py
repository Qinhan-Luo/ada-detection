# -*- encoding: utf-8 -*-
'''
@Time : 2020/6/18 17:39 
@Author : qinhanluo
@File : merge.py 
@Software: PyCharm
@Description ： TODO
'''
import  cv2


if __name__ == '__main__':
    # img1 = cv2.imread('ceshi_HZ_01_wgs84.jpg')
    # img2 = cv2.imread('prediction.jpg')
    #
    #
    # img_add = cv2.bitwise_and(img1, img2)
    # img_or = cv2.bitwise_or(img1, img2)
    #
    # cv2.imwrite("and.jpg", img_add)
    # cv2.imwrite("or.jpg", img_or)

    img  = cv2.imread('./tmp2.tif')

    cv2.imwrite("1.jpg", img)

    pass