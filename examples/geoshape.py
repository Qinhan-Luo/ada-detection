# -*- encoding: utf-8 -*-
'''
@Time : 2020/6/11 15:19 
@Author : qinhanluo
@File : geoshape.py 
@Software: PyCharm
@Description ： TODO
'''

import geopandas as gpd
from sqlalchemy import create_engine
from geoalchemy2 import Geometry, WKTElement
from shapely.geometry import Polygon
from shapely.geometry import  MultiPolygon
from sqlalchemy import FLOAT, Integer, BIGINT, text
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import FLOAT, Integer, BIGINT, text
import pandas as pd
from datetime import datetime
import geopandas as gpd
import time
from shapely.geometry import Polygon
from geoalchemy2 import Geometry, WKTElement

def explode(indata):
    count_mp = 0
    indf = gpd.GeoDataFrame.from_file(indata)
    outdf = gpd.GeoDataFrame(columns=indf.columns)
    for idx, row in indf.iterrows():
        if type(row.geometry) == Polygon:
            outdf = outdf.append(row, ignore_index=True)
        if type(row.geometry) == MultiPolygon:
            print('test')
            count_mp = count_mp + 1
            multdf = gpd.GeoDataFrame(columns=indf.columns)
            recs = len(row.geometry)
            multdf = multdf.append([row]*recs, ignore_index=True)
            for geom in range(recs):
                multdf.loc[geom, 'geometry'] = row.geometry[geom]
            outdf = outdf.append(multdf, ignore_index= True)
    print("Thre were", count_mp, "Multipolygons found and exploded")
    return outdf


if __name__ == '__main__':
    # seg_path = r'C:\Users\muchun\Desktop\1\面状.shp'
    # shape = gpd.read_file(seg_path)
    shape = explode(r'C:\Users\muchun\Desktop\1\面状.shp')
    print(shape.columns)
    df = pd.DataFrame(shape.loc[:,['osm_id', 'code', 'fclass', 'name']])

    gem = shape['geometry']
    gdf = gpd.GeoDataFrame(df, geometry=gem)
    gdf.crs = {'init': 'espg:4326'}

    gdf['geom'] = gdf['geometry'].apply(lambda x:WKTElement(x.wkt, 4326))
    gdf.drop('geometry',1, inplace=True)
    gdf.rename(columns={'geom': 'geometry'}, inplace=True)

    enginge = create_engine('postgresql+psycopg2://postgres:123456@localhost:5432/test')
    con = enginge.connect()

    gdf.to_sql('WATER_POLYGON_2', enginge, if_exists='append', index=False,
               dtype={'geometry': Geometry('Polygon', 4326)})

    pass