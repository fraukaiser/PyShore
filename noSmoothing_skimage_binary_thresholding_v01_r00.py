# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 13:53:47 2020

@author: skaiser
"""

"""
 * Python3 script to delineate waterbodies based on simple thresholding of the NIR channel.
 *
 * usage: python Threshold.py <path_in> <threshold>
"""
import sys, os, fnmatch
import numpy as np
import skimage.color
import skimage.filters
import skimage.io
import skimage.viewer
from matplotlib import pyplot as plt
from osgeo import gdal



#%%

# get filename, sigma, and threshold value from command line
#path_in = sys.argv[0]
path_in = "/home/fraukaiser/Documents/PermaRisk/git/0_preproc_data"
#t = sys.argv[1]
t = 0.8

#%%

filenames = []
input = []
for root, dirs, files in os.walk(path_in):
    for file in files:
        if fnmatch.fnmatch(file, '*sub.TIF'):
            filepath = root + '/' + file
            input.append(filepath)
            
for i in input:
    cmd = "gdal_translate -ot Byte -of GTiff %s %s_8B.TIF" %(i, i[:-4])
    os.system(cmd)
    filenames.append("%s_8B.TIF" %i[:-4])

#%%    

for i in filenames:
    image = skimage.io.imread(fname=i)   # image[rows, columns, dimensions]-> image[:,:,3] is near Infrared

    nir = image[:,:,3]
    gtif = gdal.Open(i)
    geotransform = gtif.GetGeoTransform()
    sourceSR = gtif.GetProjection()
    
    x = np.shape(image)[1]
    y = np.shape(image)[0]
    bands = np.shape(image)[2]
    
    ## create the histogram
    histogram, bin_edges = np.histogram(nir, bins=256, range=(0, 1))
    
    #
    # configure and draw the histogram figure
    plt.figure()
    plt.title("Grayscale Histogram")
    plt.xlabel("grayscale value")
    plt.ylabel("pixels")
    plt.xlim([0.0, 1.0])  # <- named arguments do not work here
    
    plt.plot(bin_edges[0:-1], histogram)  # <- or here
    plt.show()
    
    # blur and grayscale before thresholding
    blur = skimage.color.rgb2gray(nir)
    blur = skimage.filters.gaussian(blur, sigma=2.0)
    
    # perform inverse binary thresholding
    mask = blur < t
    
    #output np array as GeoTiff
    file_out = '%s/%s_mask_t%s.TIF'% (path_in, i.rsplit('/')[-1][:-4], str(t))
    dst_ds = gdal.GetDriverByName('GTiff').Create(file_out, x, y, 1, gdal.GDT_Float32)   
    dst_ds.GetRasterBand(1).WriteArray(mask)
    dst_ds.SetGeoTransform(geotransform)
    dst_ds.SetProjection(sourceSR) 
    dst_ds.FlushCache()
    dst_ds = None
    
    #polygonize and write to Shapefile
    cmd = 'gdal_polygonize.py %s -f "ESRI Shapefile" %s.shp' %(file_out, file_out[:-4])
    os.system(cmd)
    
    
