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
#path_in = sys.argv[1]
path_in = "/home/skaiser/Desktop/Code_Subs_Soraya/HERE/0_preproc_data"
fig_out = "/home/skaiser/permamount/staff/soraya_kaiser/git2/2_plots"

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
    #os.system(cmd)
    filenames.append("%s_8B.TIF" %i[:-4])

#%%    user defined t- value 

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
#    
    # perform inverse binary thresholding
    mask = blur < t
    
    #output np array as GeoTiff
    file_out = '%s/%s_mask_t%s_otsu.TIF'% (path_in, i.rsplit('/')[-1][:-4], str(t)[0:4])
    dst_ds = gdal.GetDriverByName('GTiff').Create(file_out, x, y, 1, gdal.GDT_Float32)   
    dst_ds.GetRasterBand(1).WriteArray(mask)
    dst_ds.SetGeoTransform(geotransform)
    dst_ds.SetProjection(sourceSR) 
    dst_ds.FlushCache()
    dst_ds = None
    
    #polygonize and write to Shapefile
    cmd = 'gdal_polygonize.py %s -f "ESRI Shapefile" %s.shp' %(file_out, file_out[:-4])
    os.system(cmd)    
#%% Ab hier nur plotting 
plot_hist = []
legend = []
   
for i in filenames:
    image = skimage.io.imread(fname=i)   # image[rows, columns, dimensions]-> image[:,:,3] is near Infrared
    legend.append((i.rsplit('/')[-1][:-4]).rsplit('-')[0])

    nir = image[:,:,3]
#    gtif = gdal.Open(i)
#    geotransform = gtif.GetGeoTransform()
#    sourceSR = gtif.GetProjection()
#    
#    x = np.shape(image)[1]
#    y = np.shape(image)[0]
#    bands = np.shape(image)[2]
    
    ## create the histogram
#    histogram, bin_edges = np.histogram(nir, bins=256, range=(0, 1))
    hist_data, bins = np.histogram(nir, bins = np.max(nir))
    plot_hist.append(hist_data)    
    

#%% Random HEX Color Code Generator (source: https://stackoverflow.com/questions/28999287/generate-random-colors-rgb)
import random

number_of_colors = len(filenames)

color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
             for i in range(number_of_colors)]
print(color)

colors = [i.upper() for i in ['#1b9e77','#d95f02','#7570b3','#e7298a']]
linesytles = [':', '-.', '-', '--']

#%% For Visualization

"""
Broken axis example, where the y-axis will have a portion cut out.
"""

f, (ax, ax2) = plt.subplots(2, 1, sharex=True, figsize = (16, 8))

# zoom-in / limit the view to different portions of the data
ax.set_ylim(350, 1000)  # outliers only
ax2.set_ylim(0, 130)  # most of the data

# hide the spines between ax and ax2
ax.spines['bottom'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax.xaxis.tick_top()
ax.tick_params(labeltop='off')  # don't put tick labels at the top
ax2.xaxis.tick_bottom()

count = 0
for i in plot_hist:
    print count
    i = [float(i) / 10000 for i in i]
    print i
    ax.plot(bins[0:-1], i, label = legend[count], color = colors[count], linestyle = linesytles[count])
    ax2.plot(bins[0:-1], i, label = legend[count], color = colors[count], linestyle = linesytles[count])
    count = count + 1
ax.legend(loc='upper left')

#blur_hist, bins = np.histogram(blur, bins = 50, range= (0.0,1.0))
#f, ax = plt.subplots(1, figsize = (12, 8))
#ax.plot(bins[0:-1], blur_hist)
