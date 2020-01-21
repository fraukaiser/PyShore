#!/usr/bin/env python
# coding: utf-8

# In[1]:


####
## Imports
####

#import argparse
import os, json, fnmatch
import numpy as np
from osgeo import gdal, ogr
import geopandas as gpd
from shapely.geometry import Point
from shapely.wkt import loads
import datetime, time
from scipy.spatial import distance


#%%

start = datetime.datetime.now()
start_time = time.time()


# In[2]:

#### subs home directory
path_in = '/permarisk/data/remote_sensing/HighResImagery/DigitalGlobe/ftp2.digitalglobe.com/2_plots'
infrastructure = '/permarisk/staff/soraya_kaiser/git2/0_preproc_data/20190830_NorthSlope_infrastructure_polygon_32606.shp'
gtif_file = '/permarisk/staff/soraya_kaiser/git2/0_preproc_data/06AUG15222517-M2AS-058878563040_01_P001_GS_pansharpened_cubic_0.5_sub.TIF'
data_out = '/permarisk/staff/soraya_kaiser/git2/1_proc_data/'
figf_out = '/permarisk/staff/soraya_kaiser/git2/2_plots/'


files_in = []
for root, dirs, files in os.walk(path_in):
    for file in files:
        if fnmatch.fnmatch(file, '*.shp'):
            filepath = root + '/' + file
            files_in.append(filepath)

files_in.sort()
files_in.append(infrastructure)

gtif = gdal.Open(gtif_file)
gtif_info = gtif.GetGeoTransform()
resolution = gtif_info[1]
sitename = 'Deadhorse'
site = gtif_file.rsplit('/')[-1][:-4]
#sitename = site.rsplit('-')[-1]
print "The spatial resolution of the %s data is %s m" %(sitename, str(resolution))
print site 

print 'files_in length: ', len(files_in)



# In[3]:


## convert shapes to gdfs
reference = gpd.read_file(files_in[0])
osm = gpd.read_file(files_in[len(files_in)-1])
print "The reference file is " + files_in[0]
print "File %s contains the osm infrastructure" %str(files_in[len(files_in)-1])

shapes = files_in[:len(files_in)-1]

# in case of Deadhorse and CNSC: Four timesteps
timestep_names = ['ref', 'first', 'second', 'third', 'fourth'] # to access current set of data: until len(files_in)-1
storage = [reference]
for i in shapes[1:len(files_in)-1]:
    y = gpd.read_file(i)
    storage.append(y)

print 'storage length: ', len(storage)

# In[7]:


#####
## Functions
####

def segmentize(geom):
    wkt = geom.wkt  # shapely Polygon to wkt
    geom = ogr.CreateGeometryFromWkt(wkt)  # create ogr geometry
    geom.Segmentize(resolution)  # densify geometry
    wkt2 = geom.ExportToWkt()  # ogr geometry to wkt
    new = loads(wkt2)  # wkt to shapely Polygon
    return new 


# In[8]:


## DN = 1: feature is waterbody
storage_water = []
for i in storage:
    y = i.loc[i['DN'] == 1].copy()
    y['id'] = np.array(range(len(y)))
    storage_water.append(y)

    
osm['osm_id'] = np.array(range(len(osm)))


# ### Drop features containing infrastructure (osm data) and filter for features > 0.1 ha

# In[9]:


storage_infrastructure = []
count = 0
for i in storage_water:
    print count
    i.crs = reference.crs
    fname = timestep_names[count]
    i.to_file(data_out + "%s_%s.shp" %(sitename, fname), driver = 'ESRI Shapefile')
    print "%s_%s written to file" %(sitename, fname)
    print "overlay infrastructure"
    x = gpd.overlay(i, osm, how = 'intersection')
    y = np.ndarray.tolist(np.array(x.id))
    z = i[~i['id'].isin(y)]
    print "Filter feature > 0.1 ha"
    xyz = z.loc[z.area > 1000].copy()
    xyz.to_file(data_out + "%s_%s_water_ni.shp" %(sitename, fname), driver = 'ESRI Shapefile')
    print "%s_%s_water_ni written to file" %(sitename, fname)
    storage_infrastructure.append(xyz)
    count = count + 1


# 

# ## Merge smaller moist feature to one lake by setting the ref dataset as basis

# In[10]:


storage_merged = [storage_infrastructure[0]]
print len(storage_infrastructure[0])
for i in storage_infrastructure[1:]:
    x = gpd.sjoin(i, storage_infrastructure[0], op ='intersects', how = 'left')
    y = x.dissolve(by = 'id_right')
    print len(y)
    storage_merged.append(y)

    
# #### ref id needs to be transformed to id_right
storage_merged[0]['id_right'] = storage_merged[0]['id']   


# In[11]:


#for i in storage_merged:
#    i.plot(color='#FBFAF9', alpha= 0.3, edgecolor= 'darkred')


# In[12]:


count = 1
storage_joined = []
for i in storage_merged[1:]:
    joined = i.merge(storage_merged[0], on = 'id_right')
    fname = "%s_%s_water_ni_joined" %(sitename, timestep_names[count])
    print fname, ':', joined.crs, len(joined)
    df_new = gpd.GeoDataFrame(joined.geometry_x) # df1
    df_new['geometry'] = df_new['geometry_x']
    df_new['id_right'] = joined.id_right
    df_new['geometry'] = df_new['geometry'].map(segmentize)
    df_ref = gpd.GeoDataFrame(joined.geometry_y) # df2
    df_ref['geometry'] = df_ref['geometry_y']
    df_ref['id_right'] = joined.id_right
#    df_ref['geometry'] = df_ref['geometry'].map(segmentize)
    print len(df_new), len(df_ref)
    df_new['geometry'] = df_new['geometry'].map(segmentize)
##    df_new.plot(figsize= (16, 16))
    count += 1
    storage_joined.append(df_new)
    
storage_merged[0]['geometry'] = storage_merged[0]['geometry'].map(segmentize)
storage_joined.insert(0, storage_merged[0])


# In[13]:


fname = "%s_%s_water_ni_joined" %(sitename, timestep_names[0])
print fname, ':', storage_joined[0].crs, len(storage_joined[0])


# In[14]:

#
#for i in storage_joined:
#    i.plot(color='#FBFAF9', alpha= 0.3, edgecolor= 'darkblue')


# ### Define categories by waterbody size

# In[15]:


### do histograms for different size classes after Jones, B. M., Grosse, G., Arp, C. D., Jones, M. C., Walter Anthony, K. M., & Romanovsky, V. E. (2011). Modern thermokarst lake dynamics in the continuous permafrost zone, northern Seward Peninsula, Alaska. Journal of Geophysical Research: Biogeosciences, 116(3), 1–13. https://doi.org/10.1029/2011JG001666
### 0.1 to 1 ha (class_01), 1 to 10 ha (class_02), 10 to 40 ha (class_03), 40 to 400 ha (class_04)
count = 0 
sizes = [1, 2, 3, 4]   
minimum = [1000, 10000, 100000, 400000]
maximum = [10000, 100000, 400000, 4000000]
class_names = []
class_features = []
new_dict = {}

for i in storage_joined:
#    print count 
#    print i
    fname = timestep_names[count]
    min_max_count = 0
    for j in sizes:
        print min_max_count
        classname = "%s_%s_class_0%s" %(sitename, fname, str(j))
        class_names.append(classname)
        y = i.loc[(minimum[min_max_count] <= i.area) & (i.area < maximum[min_max_count])].copy()
        try: 
            #y.to_file(data_out + classname + '.shp', driver = 'ESRI Shapefile') # uncommenting this solved the issue of "is empty" for classes from first_01! How? Why?
            print classname, ':', len(y)
        except:
            print classname + ' is empty' # apparently after ref every class is empty, no output as shapefile
        class_features.append(y)
#        print y
        new_dict.update({classname: len(y)})
        min_max_count +=1 
    count += 1
    


# In[16]:

os.chdir(figf_out)
print new_dict

with open('new_dict.txt', 'w') as file:
    file.write(json.dumps(new_dict))


 ### Convert geometry to points

# In[17]:


#class_features
class_features_new = []

for i in class_features:
    lake_id = []
    class_array = []
    for index, row in i.iterrows():
        try:
            lakeid = row['id_right'] #### and index_right
        except:
            lakeid = row['index_right']
#        print type(row.geometry)
#        row.geometry.unary_union
#        print type(row.geometry)
        if row.geometry.type == 'Polygon':
            print "yes"
            for pt in list(row['geometry'].exterior.coords):    # for pt in list(row['geometry'].exterior.coords): AttributeError: 'MultiPolygon' object has no attribute 'exterior'
                class_array.append(pt)
                lake_id.append(lakeid)
        elif row.geometry.type == 'MultiPolygon':
            print "no"
            for pt in list(row.geometry.convex_hull.exterior.coords):    # for pt in list(row['geometry'].exterior.coords): AttributeError: 'MultiPolygon' object has no attribute 'exterior'
                class_array.append(pt)
                lake_id.append(lakeid)
#            row.geometry.convex_hull
    new = gpd.GeoDataFrame()
    new['geometry'] = class_array
    new['geometry'] = new['geometry'].apply(Point) 
    new['lake_id'] = lake_id
    new['point_id'] = np.arange(len(class_array))
    class_features_new.append(new)


# In[18]:


for i in class_features_new:
    print len(i)


# In[19]:


count = 0
class_names = []
sizes = [1, 2, 3, 4]   
min_max_count = 0
for i in class_features_new:
    if count == len(sizes):
        break
    fname = timestep_names[count]
    for j in sizes:
#        print min_max_count
        classname = fname + '_class_0%d_points' %j
        class_names.append(classname)
#        print classname, len(class_features_new[min_max_count])
        min_max_count += 1
    count += 1
   
    
class_lake_id = []   
count = 0
for i in class_features_new:
    try:
##        i.to_file(data_out + class_names[count] + '.shp', driver = 'ESRI Shapefile')
        lake_nr = i.lake_id.unique()
        print class_names[count] + ':  ', len(i), lake_nr   
        class_lake_id.append(lake_nr)
    except: 
        print class_names[count] + ' is empty'
    count += 1


# In[28]:

print len(class_features_new) # 12

#%% Nearest Point Analysis
for y in range(len(class_features_new)-4):  # 
    df1 = class_features_new[y]
    df2 = class_features_new[y+4]

    lake_ids1 = df1.lake_id.unique()
    lake_ids2 = df2.lake_id.unique()
    lake_ids = np.unique(np.append(lake_ids1,lake_ids2))

    lake_ids = lake_ids.astype(int)
    ts_ref = int(y)
    ts_comp = int(y+4)
    
    for lake_id in lake_ids:
        #get points as xy array from reference dataframe
        points = df1[(df1['lake_id']==lake_id)]
        x = np.asarray(points.geometry.x)
        y = np.asarray(points.geometry.y)
        xy_ref = np.transpose(np.vstack((x,y)))
        
        #get points as xy array from dataframe to which ref is compared
        points = df2[(df2['lake_id']==lake_id)]
        x = np.asarray(points.geometry.x)
        y = np.asarray(points.geometry.y)
        xy_comp = np.transpose(np.vstack((x,y)))
        
        #note that it is important to not use lists but to transfere them first in to arrays in order to benefit from vector calculation
        distances = distance.cdist(xy_ref, xy_comp)
        try:
            min_dist_idy = np.argmin(distances,axis=1)
            min_distances = np.min(distances,axis=1)
        
            #claculate direction between reference points and comp points
            p_n = xy_comp[min_dist_idy] - xy_ref 
            #get direction in degree clockwise from north
            direction = np.rad2deg(np.arctan2(p_n[:,0], p_n[:,1]))
            direction[(direction<0)] = 360 + direction[(direction<0)] 
            
            # write reference to file
            gdf_ref = gpd.GeoDataFrame(
                crs = {'init': 'epsg:32606'},
                geometry=[Point(xy) for xy in zip(xy_ref[:, 0], xy_ref[:, 1])])
            gdf_ref['distance'] = min_distances
            gdf_ref['direction'] = direction
            gdf_ref['min_dist_idy'] = min_dist_idy
            print figf_out + 'gdf_ts%s_lake%s.csv' % (str(ts_ref), str(lake_id))
            gdf_ref.to_csv(figf_out + 'gdf_ts%s_lake%s.csv' % (str(ts_ref), str(lake_id)))
#            gdf_ref.to_file(figf_out + 'gdf_ts%s_lake%s.shp' % (str(ts_ref), str(lake_id)), driver = 'ESRI Shapefile')
            
            # write comp to file
            gdf_comp = gpd.GeoDataFrame(
                crs = {'init': 'epsg:32606'},
                geometry=[Point(xy) for xy in zip(xy_comp[:, 0], xy_comp[:, 1])])
            print figf_out + 'gdf_ts%s_lake%s.csv' % (str(ts_comp), str(lake_id))
            gdf_comp.to_csv(figf_out + 'gdf_ts%s_lake%s.csv' % (str(ts_comp), str(lake_id)))
#            gdf_comp.to_file(figf_out + 'gdf_ts%s_lake%s.shp' % (str(ts_comp), str(lake_id)), driver = 'ESRI Shapefile')
        
        except:
            print 'empty sequence'

#%%
    
now = datetime.datetime.now()
print 'started at %s,  finished at %s' % (str(start), str(now))  
print 'Total computing time: --------------- %s seconds -----------------' % (time.time() - start_time)
