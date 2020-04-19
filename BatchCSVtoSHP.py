# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 11:34:02 2020

@author: skaiser
"""

import os
import fnmatch
import geopandas as gpd
import pandas as pd
from shapely import wkt

path_in = '/home/skaiser/permamount/staff/soraya_kaiser/git2/2_plots/median5'

files_in = []
for root, dirs, files in os.walk(path_in):
    for file in files:
        if fnmatch.fnmatch(file, 'ts*.csv'):
            filepath = root + '/' + file
            files_in.append(filepath)

for i in files_in:
    df = pd.read_csv(i)
    df['geometry'] = df['geometry'].apply(wkt.loads)
    gdf = gpd.GeoDataFrame(df, geometry = 'geometry') # geometry=[Point(xy) for xy in zip(df.x, df.y)])
    file_out = '%s.shp' % (i[:-4])
    print file_out
    gdf.to_file(file_out, driver = 'ESRI Shapefile')
