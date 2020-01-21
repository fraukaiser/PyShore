# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 12:06:40 2019

Batch loading .csv results from PyShore into QGIS 

@author: fraukaiser
"""

import glob
layers=[] # makes an empty list
path_in = '/home/skaiser/permamount/staff/soraya_kaiser/git2/2_plots'

for file in glob.glob('%s/gdf*.csv' % path_in):
    uri = "file://" + file + "?delimiter={}&crs={}&wktField={}".format(",", "epsg:32606", "geometry") # put here the text delimiter, epsg code & name of field containing wkt geometry, e.g. POINT (442918.5 7789310)
    vlayer = QgsVectorLayer(uri,file.rsplit('/')[-1][:-4] , "delimitedtext")
    layers.append(vlayer)
    QgsMapLayerRegistry.instance().addMapLayers(layers)
