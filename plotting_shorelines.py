# -*- coding: utf-8 -*-
"""
Edited on Mon Jul  6 11:07:27 2020

@author: fraukaiser


Calculating shoreline movement of multitemporal dataset

Usage: python plotting_shorelines.py <path_in> <sitename>

"""
#%%

####
## Imports
####

import os, json, fnmatch, sys
import numpy as np
from osgeo import gdal, ogr
import geopandas as gpd
from shapely.geometry import Point
from shapely.wkt import loads
import datetime, time
from scipy.spatial import distance

#%% Functions

def createFolder(directory):  # from https://gist.github.com/keithweaver/562d3caa8650eefe7f84fa074e9ca949
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)
        
        
        
def segmentize(geom):
    wkt = geom.wkt  # shapely Polygon to wkt
    geom = ogr.CreateGeometryFromWkt(wkt)  # create ogr geometry
    geom.Segmentize(resolution)  # densify geometry
    wkt2 = geom.ExportToWkt()  # ogr geometry to wkt
    new = loads(wkt2)  # wkt to shapely Polygon
    return new 

#%%

start = datetime.datetime.now()
start_time = time.time()


# In[2]:



#path_in = '/your/path/to/your/input/data'
path_in = sys.argv[1]
sitename = sys.argv[2]


#### Load satellite images and infrastructure data
files_in = []
infrastructure_in = []
tif_in = []

for root, dirs, files in os.walk(path_in):
    for file in files:
        if fnmatch.fnmatch(file, '*1.shp'):
            filepath = root + '/' + file
            infrastructure_in.append(filepath)
        elif fnmatch.fnmatch(file, '*otsu_ordershp.shp'):
            filepath = root + '/' + file
            files_in.append(filepath)
        elif fnmatch.fnmatch(file, '*.TIF'):
            filepath = root + '/' + file
            tif_in.append(filepath)
            
            
files_in.sort()
tif_in.sort()
#print files_in, tif_in, infrastructure_in

gtif = gdal.Open(tif_in[0])
gtif_info = gtif.GetGeoTransform()
resolution = gtif_info[1]


site = tif_in[0].rsplit('/')[-1][:-4]
print "The spatial resolution is %s m" %(str(resolution))
print 'files_in length: ', len(files_in)


#%% Create Folders for Output
data_out = path_in.rsplit('/', 1)[0] + '/1_PyShore_ProcData/'
figf_out = path_in.rsplit('/', 1)[0] + '/2_PyShore_Output/'
createFolder(data_out)
createFolder(figf_out)

#%% Check for Line Geometries in infrastructure data, buffer and merge

gdfs = []
for i in infrastructure_in:
    gdf = gpd.read_file(i)

    for y in gdf.type[:1]:
        if y == 'LineString':
            print 'yes'
            buffered = gdf.buffer(0.0003)
            gdf['geometry'] = buffered
            print 'buffered'
        else:
            print 'no'     

    gdfs.append(gdf)
    
osm = gdfs[0].append(gdfs[1:])
osm.to_file(path_in.rsplit('/', 1)[0] + '/1_PyShore_ProcData/' + 'infrastructuremap.shp')


### To Do: Clip Infrastructure map to site extent: %s_infrastructuremap.shp % sitename

#%% convert multi-temporal shapefiles to gdfs

reference = gpd.read_file(files_in[0]) # set reference for shoreline change
print "The reference file is " + files_in[0]

shapes = files_in[1:len(files_in)]

timestep_names = [str(i) for i in range(0, len(files_in))]

storage = [reference]
for i in shapes:
    y = gpd.read_file(i)
    storage.append(y)

print 'storage length: ', len(storage)

#%% Remove non-water features


## DN = 1: feature is waterbody
storage_water = []
for i in storage:
    y = i.loc[i['DN'] == 1].copy()
    y['id'] = np.array(range(len(y)))
    storage_water.append(y)

    
#%% Drop features containing infrastructure (osm data) and filter for features > 0.1 ha


storage_infrastructure = []
count = 0
for i in storage_water:
    print count
    i.crs = reference.crs
    fname = timestep_names[count]
    i.to_file(data_out + "%s_%s.shp" %(fname, sitename), driver = 'ESRI Shapefile')
    print "%s_%s written to file" %(fname, sitename)
    print "overlay infrastructure"
    x = gpd.overlay(i, osm, how = 'intersection')
    y = np.ndarray.tolist(np.array(x.id))
    z = i[~i['id'].isin(y)]
    print "Filter feature > 0.1 ha"
    xyz = z.loc[z.area > 1000].copy()
    xyz.to_file(data_out + "%s_%s_water_ni.shp" %(fname, sitename), driver = 'ESRI Shapefile')
    print "%s_%s_water_ni written to file" %(fname, sitename)
    storage_infrastructure.append(xyz)
    count = count + 1


#%% Exit script when no multi-temporal files are inserted

if len(files) == 1:
    sys.exit()


#%% Merge smaller moist feature to one lake by setting the ref dataset as basis

print len(storage_infrastructure[0])
for i in storage_infrastructure[1:]:
    x = gpd.sjoin(i, storage_infrastructure[0], op ='intersects', how = 'left')
    y = x.dissolve(by = 'id_right')
    print len(y)
    storage_merged.append(y)

    
# #### ref id needs to be transformed to id_right
storage_merged[0]['id_right'] = storage_merged[0]['id']   

# In[12]:


count = 1
storage_joined = []
for i in storage_merged[1:]:
    joined = i.merge(storage_merged[0], on = 'id_right')
    fname = "%s_water_ni_joined" %(timestep_names[count])
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


fname = "%s_water_ni_joined" %(timestep_names[0])
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
        classname = "%s_class_0%s" %(fname, str(j))
        class_names.append(classname)
        y = i.loc[(minimum[min_max_count] <= i.area) & (i.area < maximum[min_max_count])].copy()
        try: 
            y.to_file(data_out + classname + '.shp', driver = 'ESRI Shapefile') # uncommenting this solved the issue of "is empty" for classes from first_01! How? Why?
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
names_out = range(0,16)
count = 0 
for i in class_features:
    lake_id = []
    class_array = []
    ####
    i.to_csv(figf_out + 'ts%s.csv' % str(names_out[count]))
    count += 1
    ####
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
            fi = open(figf_out + 'gdf_tsref%s_tscomp%s_lake%s.txt' % (str(ts_ref), str(ts_comp), str(lake_id)), "w")
            fi.write("empty sequence")
            fi.close()


#%% Nearest Points for cumulative results:

figf_out = '/permarisk/staff/soraya_kaiser/git2/2_plots/median5/cum/'


for y in range(8, 16):  # 
    if y < 12:
        df1 = class_features_new[y-8]
        ts_ref = int(y-8)
    else: 
        df1 = class_features_new[y-12]
        ts_ref = int(y-12)

    df2 = class_features_new[y]     # is new

    lake_ids1 = df1.lake_id.unique()
    lake_ids2 = df2.lake_id.unique()
    lake_ids = np.unique(np.append(lake_ids1,lake_ids2))

    lake_ids = lake_ids.astype(int)
    ts_comp = int(y)
    
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
            print figf_out + 'gdf_tsref%s_cum_tscomp%s_lake%s.csv' % (str(ts_ref), str(ts_comp), str(lake_id))
            gdf_ref.to_csv(figf_out + 'gdf_tsref%s_cum_tscomp%s_lake%s.csv' % (str(ts_ref), str(ts_comp), str(lake_id)))
#            gdf_ref.to_file(figf_out + 'gdf_ts%s_lake%s.shp' % (str(ts_ref), str(lake_id)), driver = 'ESRI Shapefile')
            
#            # write comp to file
#            gdf_comp = gpd.GeoDataFrame(
#                crs = {'init': 'epsg:32606'},
#                geometry=[Point(xy) for xy in zip(xy_comp[:, 0], xy_comp[:, 1])])
#            print figf_out + 'gdf_ts%s_lake%s.csv' % (str(ts_comp), str(lake_id))
#            gdf_comp.to_csv(figf_out + 'gdf_ts%s_lake%s.csv' % (str(ts_comp), str(lake_id)))
##            gdf_comp.to_file(figf_out + 'gdf_ts%s_lake%s.shp' % (str(ts_comp), str(lake_id)), driver = 'ESRI Shapefile')
        
        except:
            fi = open(figf_out + 'gdf_tsref%s_tscomp%s_lake%s.txt' % (str(ts_ref), str(ts_comp), str(lake_id)), "w")
            fi.write("empty sequence")
            fi.close()


#%%

now = datetime.datetime.now()
print 'started at %s,  finished at %s' % (str(start), str(now))  
print 'Total computing time: --------------- %s seconds -----------------' % (time.time() - start_time)
