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
import os, fnmatch, sys
import numpy as np
import skimage.color
import skimage.filters
import skimage.io
import skimage.viewer
from osgeo import gdal
import datetime, time
from skimage.morphology import disk
from matplotlib import pyplot as plt

start = datetime.datetime.now()
start_time = time.time()


#%%

# get path_in
#path_in = sys.argv[1]
#path_in = "/home/skaiser/Desktop/Code_Subs_Soraya/HERE/0_preproc_data"
#path_in = "/home/skaiser/permamount/data/remote_sensing/HighResImagery/DigitalGlobe/ftp2.digitalglobe.com/0_preproc_data"
#fig_out = "/home/skaiser/permamount/staff/soraya_kaiser/git2/2_plots"
path_out = "/permarisk/data/remote_sensing/HighResImagery/DigitalGlobe/ftp2.digitalglobe.com/1_proc_data"
nir_band = 3
#%%

filenames = []
#input = []
#for root, dirs, files in os.walk(path_in):
#    for file in files:
#        if fnmatch.fnmatch(file, '*.TIF'):
#            filepath = root + '/' + file
#            input.append(filepath)
input = ['/permarisk/data/remote_sensing/HighResImagery/DigitalGlobe/ftp2.digitalglobe.com/058878563050_01/058878563050_01_P001_MUL/16AUG27214538-M2AS-058878563050_01_P001_GS_pansharpened_cubic_0.5.TIF']            
#input = ['/permarisk/data/remote_sensing/HighResImagery/DigitalGlobe/ftp2.digitalglobe.com/058878563040_01/058878563040_01_P001_MUL/06AUG15222517-M2AS-058878563040_01_P001_GS_pansharpened_cubic_0.5.TIF', 
#         '/permarisk/data/remote_sensing/HighResImagery/DigitalGlobe/ftp2.digitalglobe.com/058878563030_01/058878563030_01_P001_MUL/10JUL09221426-M2AS-058878563030_01_P001_GS_pansharpened_cubic_0.5_1stpoly_warped_16tp.TIF', 
#         '/permarisk/data/remote_sensing/HighResImagery/DigitalGlobe/ftp2.digitalglobe.com/058878563020_01/058878563020_01_P001_MUL/13JUL16225401-M2AS-058878563020_01_P001_GS_pansharpened_cubic_0.5_1stpoly_warped_17tp.TIF', 
#         '/permarisk/data/remote_sensing/HighResImagery/DigitalGlobe/ftp2.digitalglobe.com/058878563010_01/058878563010_01_P001_MUL/16JUL10222531-M2AS-058878563010_01_P001_GS_pansharpened_cubic_0.5_1stpoly_warped_18tp.TIF']            

for i in input:
    cmd = "gdal_translate -ot Byte -of GTiff %s %s_8B.TIF" %(i, i[:-4])
    print cmd
#    os.system(cmd)
    filenames.append("%s_8B.TIF" %i[:-4])

#%% Bilateral Filtering
#
#value = range(1,20,2)
#   
#for i in value:
#    bilat_img = skimage.filters.rank.mean_bilateral(nir, disk(20), s0=10,s1=10)
#    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10, 10), sharex='row', sharey='row')
#
#    ax = axes.ravel()
#    
#    ax[0].imshow(nir, cmap=plt.cm.gray)
#    ax[0].set_title('Original')
#
#    ax[1].imshow(bilat_img, cmap=plt.cm.gray)
#    ax[1].set_title('Bilateral %s' % str(i))  
#
#    
#%% Median Filtering
#
#for i in value:
#    bilat_img = skimage.filters.rank.median(nir, disk(i))
#    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10, 10), sharex='row', sharey='row')
#
#    ax = axes.ravel()
#    
#    ax[0].imshow(nir, cmap=plt.cm.gray)
#    ax[0].set_title('Original')
#
#    ax[1].imshow(bilat_img, cmap=plt.cm.gray)
#    ax[1].set_title('Bilateral %s' % str(i))  
#
#  
#%% Median and Otsu
value = 5
clips = []
for i in filenames:
    image = skimage.io.imread(fname=i)   # image[rows, columns, dimensions]-> image[:,:,3] is near Infrared
    nir = image[:,:,nir_band]    
    
    bilat_img = skimage.filters.rank.median(nir, disk(value))
    
    gtif = gdal.Open(i)
    geotransform = gtif.GetGeoTransform()
    sourceSR = gtif.GetProjection()
    
    x = np.shape(image)[1]
    y = np.shape(image)[0]
    bands = np.shape(image)[2]
   
    # blur and grayscale before thresholding
    blur = skimage.color.rgb2gray(bilat_img)
    blur = skimage.filters.gaussian(blur, sigma=2.0)
    
    t = skimage.filters.threshold_otsu(blur)
    print t
    
    # perform inverse binary thresholding
    mask = blur < t
    
 
    #output np array as GeoTiff
    file_out = '%s/%s_t%s_median%s_otsu.TIF'% (path_out, i.rsplit('/')[-1][:-4], str(t)[0:4], str(value))
    clips.append(file_out)
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
	

    
#%%    Otsu

#for i in filenames:
#    image = skimage.io.imread(fname=i)   # image[rows, columns, dimensions]-> image[:,:,3] is near Infrared
#
#    nir = image[:,:,nir_band]
#    gtif = gdal.Open(i)
#    geotransform = gtif.GetGeoTransform()
#    sourceSR = gtif.GetProjection()
#    
#    x = np.shape(image)[1]
#    y = np.shape(image)[0]
#    bands = np.shape(image)[2]
#    
#   
#    # blur and grayscale before thresholding
#    blur = skimage.color.rgb2gray(nir)
#    blur = skimage.filters.gaussian(blur, sigma=2.0)
#    
#    t = skimage.filters.threshold_otsu(blur)
#    
#    # perform inverse binary thresholding
#    mask = blur < t
#    
#    #output np array as GeoTiff
#    file_out = '%s/%s_mask_t%s_otsu.TIF'% (path_out, i.rsplit('/')[-1][:-4], str(t)[0:4])
#    dst_ds = gdal.GetDriverByName('GTiff').Create(file_out, x, y, 1, gdal.GDT_Float32)   
#    dst_ds.GetRasterBand(1).WriteArray(mask)
#    dst_ds.SetGeoTransform(geotransform)
#    dst_ds.SetProjection(sourceSR) 
#    dst_ds.FlushCache()
#    dst_ds = None
#    
#    #polygonize and write to Shapefile
#    cmd = 'gdal_polygonize.py %s -f "ESRI Shapefile" %s.shp' %(file_out, file_out[:-4])
#    os.system(cmd)    
#    print cmd
#%%

order_shape = '/home/skaiser/permamount/data/remote_sensing/HighResImagery/DigitalGlobe/ftp2.digitalglobe.com/058878563050_01/GIS_FILES/058878563050_01_ORDER_SHAPE_32606.shp'

for i in clips:
    cmd = 'ogr2ogr -clipsrc %s -clipsrclayer %s %s_ordershp.shp %s %s -f "ESRI Shapefile"' % (order_shape, order_shape.rsplit('/')[-1][:-4], i[:-4], i, i.rsplit('/')[-1][:-4])
    print cmd
    os.system(cmd)
#%%

now = datetime.datetime.now()
print 'started at %s,  finished at %s' % (str(start), str(now))  
print 'Total computing time: --------------- %s seconds -----------------' % (time.time() - start_time)
