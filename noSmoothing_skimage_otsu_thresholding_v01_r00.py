# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 13:53:47 2020

@author: skaiser
"""

"""
 * Python script to demonstrate simple adaptive thresholding with Otsu.
 *
 * usage: python script.py <path_in>
"""
import os, fnmatch
import numpy as np
import skimage.color
import skimage.filters
import skimage.io
import skimage.viewer
from osgeo import gdal



#%%

# get path_in
#path_in = sys.argv[1]
#path_in = "/home/skaiser/Desktop/Code_Subs_Soraya/HERE/0_preproc_data"
path_in = "/home/skaiser/permamount/data/remote_sensing/HighResImagery/DigitalGlobe/ftp2.digitalglobe.com/0_preproc_data"
#fig_out = "/home/skaiser/permamount/staff/soraya_kaiser/git2/2_plots"
fig_out = "/home/skaiser/permamount/data/remote_sensing/HighResImagery/DigitalGlobe/ftp2.digitalglobe.com/2_plots"
nir_band = 3
#%%

filenames = []
input = []
for root, dirs, files in os.walk(path_in):
    for file in files:
        if fnmatch.fnmatch(file, '*.TIF'):
            filepath = root + '/' + file
            input.append(filepath)
            
for i in input:
    cmd = "gdal_translate -ot Byte -of GTiff %s %s_8B.TIF" %(i, i[:-4])
    print cmd
    os.system(cmd)
    filenames.append("%s_8B.TIF" %i[:-4])

    
#%%    Otsu

for i in filenames:
    image = skimage.io.imread(fname=i)   # image[rows, columns, dimensions]-> image[:,:,3] is near Infrared

    nir = image[:,:,3]
    gtif = gdal.Open(i)
    geotransform = gtif.GetGeoTransform()
    sourceSR = gtif.GetProjection()
    
    x = np.shape(image)[1]
    y = np.shape(image)[0]
    bands = np.shape(image)[2]
    
   
    # blur and grayscale before thresholding
    blur = skimage.color.rgb2gray(nir)
    blur = skimage.filters.gaussian(blur, sigma=2.0)
    
    t = skimage.filters.threshold_otsu(blur)
    
    # perform inverse binary thresholding
    mask = blur < t
    
    #output np array as GeoTiff
    file_out = '%s/%s_mask_t%s_otsu.TIF'% (fig_out, i.rsplit('/')[-1][:-4], str(t)[0:4])
    dst_ds = gdal.GetDriverByName('GTiff').Create(file_out, x, y, 1, gdal.GDT_Float32)   
    dst_ds.GetRasterBand(1).WriteArray(mask)
    dst_ds.SetGeoTransform(geotransform)
    dst_ds.SetProjection(sourceSR) 
    dst_ds.FlushCache()
    dst_ds = None
    
    #polygonize and write to Shapefile
    cmd = 'gdal_polygonize.py %s -f "ESRI Shapefile" %s.shp' %(file_out, file_out[:-4])
    os.system(cmd)    
    print cmd
