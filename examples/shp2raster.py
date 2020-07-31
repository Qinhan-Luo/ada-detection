# -*- encoding: utf-8 -*-
'''
@Time : 2020/6/22 9:39 
@Author : qinhanluo
@File : shp2raster.py 
@Software: PyCharm
@Description ： TODO
'''
from osgeo import gdal
from osgeo import ogr, osr
import gdalconst

if __name__ == '__main__':
    input_shape_file = r'D:\project\Adaspace_seg_waters\tmp2.shp'
    output_shape_file = r'D:\project\Adaspace_seg_waters\tmp2.tif'
    templatefile = r'C:\Users\muchun\Desktop\02\01.tif'
    try:
        data = gdal.Open(templatefile, gdalconst.GA_ReadOnly)
        x_res = data.RasterXSize
        y_res = data.RasterYSize

        vector = ogr.Open(input_shape_file)
        layer = vector.GetLayer()
        targetDataSet = gdal.GetDriverByName('MEM').Create(output_shape_file, x_res, y_res, 1, gdal.GDT_Byte)
        targetDataSet.SetGeoTransform(data.GetGeoTransform())
        targetDataSet.SetProjection(data.GetProjection())
        band = targetDataSet.GetRasterBand(1)
        NoData_value = -999
        band.SetNoDataValue(NoData_value)
        band.FlushCache()
        gdal.RasterizeLayer(targetDataSet, [1], layer)

        png_driver = gdal.GetDriverByName('PNG')
        png_datasets  = png_driver.CreateCopy("123.PNG", targetDataSet)

    finally:
        targetDataSet = None
        layer = None
        data = None