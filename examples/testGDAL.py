# -*- encoding: utf-8 -*-
'''
@Time : 2020/6/15 14:26 
@Author : qinhanluo
@File : testGDAL.py 
@Software: PyCharm
@Description ： TODO
'''
import os
from osgeo import gdal
from osgeo import ogr, osr
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy import FLOAT, Integer, BIGINT, text
import pandas as pd
from datetime import datetime
import geopandas as gpd
from  shapely import wkt
import time
import numpy as np
from shapely.geometry import Polygon
from shapely.wkb import dumps, loads
from geoalchemy2 import Geometry, WKTElement
import cv2

def geo2imagexy(dataset, x, y):
    '''
    根据GDAL的六 参数模型将给定的投影或地理坐标转为影像图上坐标（行列号）
    :param dataset: GDAL地理数据
    :param x: 投影或地理坐标x
    :param y: 投影或地理坐标y
    :return: 影坐标或地理坐标(x, y)对应的影像图上行列号(row, col)
    '''
    trans = dataset.GetGeoTransform()
    a = np.array([[trans[1], trans[2]], [trans[4], trans[5]]])
    b = np.array([x - trans[0], y - trans[3]])
    return np.linalg.solve(a, b)  # 使用numpy的linalg.solve进行二元一次方程的求解

def read_img(filename):
    dataset=gdal.Open(filename)

    im_width = dataset.RasterXSize
    im_height = dataset.RasterYSize

    im_geotrans = dataset.GetGeoTransform()
    im_proj = dataset.GetProjection()
    im_data = dataset.ReadAsArray(0,0,im_width,im_height)

    return im_width,im_height,im_proj,im_geotrans,im_data,dataset

def get_mask(img_path,out_shp, proj=4326):
    im_width,im_height,im_proj,im_geotrans,im_data, dataset = read_img(img_path)
    xleft = im_geotrans[0]
    yleft = im_geotrans[3]
    xright = im_geotrans[0] + im_width*im_geotrans[1] + im_height*im_geotrans[2]
    yright = im_geotrans[3] + im_width*im_geotrans[4] + im_height*im_geotrans[5]
    driver = ogr.GetDriverByName("ESRI Shapefile")
    data_source = driver.CreateDataSource(out_shp)

    srs = osr.SpatialReference(wkt=dataset.GetProjection())
    layer = data_source.CreateLayer("polygon", srs, ogr.wkbPolygon)
    feature = ogr.Feature(layer.GetLayerDefn())
    wa = xleft
    ha = yright
    wa1 = xleft
    ha1 = yleft
    wa2 = xright
    ha2 = yleft
    wa3 = xright
    ha3 = yright
    wkt = "POLYGON((" + str(wa)+ " " +str(ha)+ "," + str(wa1) + " " + str(ha1) + "," + str(wa2)+ " " +str(ha2)+ "," + str(wa3)+ " " +str(ha3) + "))"
    point = ogr.CreateGeometryFromWkt(wkt)
    point.CloseRings()  #这个必须要有，不然创建出来的矢量面有问题
    feature.SetGeometry(point)
    layer.CreateFeature(feature)
    feature = None
    data_source = None

if __name__ == '__main__':
    # dataset = gdal.Open(r"C:\Users\muchun\Desktop\02\01.tif")
    # im_width = dataset.RasterXSize
    # im_height = dataset.RasterYSize
    # im_bands = dataset.RasterCount
    # im_geotrans = dataset.GetGeoTransform()
    # im_proj = dataset.GetProjection()
    # img_path = r"D:\DataSets\测试20200602\GF6_E113.8_N22.4_20200131.tif"
    img_path = r"C:\Users\muchun\Desktop\02\9.tif"
    # img_path = r"C:\Users\muchun\Desktop\xu\HZ_01_wgs84.tif"
    name = "ceshi_" + img_path.split('\\')[-1].split('.')[0] + ".jpg"
    print(name)
    im_width, im_height, im_proj, im_geotrans, im_data, dataset = read_img(img_path)

    xleft = im_geotrans[0]
    yleft = im_geotrans[3]
    xright = im_geotrans[0] + im_width*im_geotrans[1] + im_height*im_geotrans[2]
    yright = im_geotrans[3] + im_width*im_geotrans[4] + im_height*im_geotrans[5]

    wa = xleft
    ha = yright
    wa1 = xleft
    ha1 = yleft
    wa2 = xright
    ha2 = yleft
    wa3 = xright
    ha3 = yright

    pnts = [(wa, ha), (wa1, ha1), (wa2, ha2), (wa3, ha3),(wa, ha)]
    wkts = "SRID=4326;" + " POLYGON((" + str(wa) + " " + str(ha) + "," + str(wa1) + " " + str(ha1) + "," + str(wa2) + " " + str(ha2) + "," + str(wa3) + " " + str(ha3) + "," + str(wa) + " " + str(ha) + "))"

    enginge = create_engine('postgresql+psycopg2://postgres:123456@localhost:5432/test')
    # con = enginge.connect()
    sql = 'SELECT * from public."WATER_POLYGON_2" WHERE ST_Intersects(geometry, \'{}\')'.format(wkts)
    # result = con.execute(sql)
    conver_polygon = wkt.loads(wkts.split(';')[-1])
    results = gpd.read_postgis(sql, enginge, geom_col='geometry', crs="epsg:4326")
    cover_region = Polygon()

    conver_img = np.zeros([im_height, im_width])

    for i in range(len(results)):
        tmp = conver_polygon.intersection(results['geometry'][i])
        # points = tmp.convex_hull.wkt.split(',')
        points = tmp.exterior.coords.xy
        t_x = np.array(points[0])
        t_x = t_x[:-1]
        t_y = np.array(points[1])
        t_y = t_y[:-1]
        assert len(t_x) == len(t_y)
        img_coor = []
        for j in range(len(t_x)):
            img_x, img_y = geo2imagexy(dataset, t_x[j], t_y[j])
            img_coor.append([int(img_x), int(img_y)])
        # cover_region = cover_region.union(tmp)
        conver_img = cv2.fillConvexPoly(conver_img, np.array(img_coor), 255)

    cv2.imwrite(name, conver_img)
    print("Done")



    # save to shp
    # driver = ogr.GetDriverByName("ESRI Shapefile")
    # data_source = driver.CreateDataSource("tmp2.shp")
    #
    # srs = osr.SpatialReference(wkt=dataset.GetProjection())
    # layer = data_source.CreateLayer("multipolygon", srs, ogr.wkbPolygon)
    # feature = ogr.Feature(layer.GetLayerDefn())
    # point = ogr.CreateGeometryFromWkt(cover_region.wkt)
    # point.CloseRings()
    # feature.SetGeometry(point)
    # layer.CreateFeature(feature)
    #
    # feature = None
    # layer = None

    # print(type(ss))
    # results.crs = {'init': 'epsg:4326'}
    # results.to_file("test.shp", encoding="utf-8")
    # driver = ogr.GetDriverByName('ESRI Shapefile')
    #
    # source_ds = driver.Open(r'D:\project\CrawlingGeoData-master\data\厦门市商务住宅边界_gcj02_wgs84.shp', 0)
    # source_layer = source_ds.GetLayer()
    #
    # x_min, x_max, y_min, y_max = source_layer.GetExtent()
    #
    #
    # x_res = im_geotrans[2]
    # y_res = im_geotrans[5]
    #
    #
    # tifDriver = gdal.GetDriverByName('GTiff')
    #
    # target_ds = tifDriver.Create('test.tif', dataset.RasterXSize, dataset.RasterYSize, 1, gdal.GDT_Byte)
    # # target_ds.SetGeoTransform(dataset.GetGeoTransform())
    # # target_ds.SetProjection(dataset.GetProjection())
    #
    # # gdal.RasterizeLayer(target_ds, [1], source_layer, None)
    # #
    # # dataset,target_ds = None, None
    #
    # target_ds.SetGeoTransform(dataset.GetGeoTransform())
    # target_ds.SetProjection(source_layer.GetSpatialRef().ExportToWkt())
    # band = target_ds.GetRasterBand(1)
    # gdal.RasterizeLayer(target_ds, [1], source_layer, None,None,burn_values=[1])
    #
    #
    # target_ds = None  # flushes data from memory.  Without this you often get an empty raster.
    # dataset = None
    # source_layer = None
    # source_ds = None
    pass