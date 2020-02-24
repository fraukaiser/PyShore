import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import geopandas as gpd
import datetime
import fnmatch, os
from shapely import wkt

#%%
### Files for Testing

files_in = ['/home/skaiser/permamount/staff/soraya_kaiser/git2/2_plots/median5/gdf_ts0_lake138.csv', '/home/skaiser/permamount/staff/soraya_kaiser/git2/2_plots/median5/gdf_ts4_lake138.csv', '/home/skaiser/permamount/staff/soraya_kaiser/git2/2_plots/median5/gdf_ts8_lake138.csv']
files_in_cum = ['/home/skaiser/permamount/staff/soraya_kaiser/git2/2_plots/median5/gdf_ts0_lake138.csv', '/home/skaiser/permamount/staff/soraya_kaiser/git2/2_plots/median5/cum/gdf_tsref0_cum_tscomp8_lake138.csv', '/home/skaiser/permamount/staff/soraya_kaiser/git2/2_plots/median5/cum/gdf_tsref0_cum_tscomp12_lake138.csv']

#%%
path_in = '/home/skaiser/permamount/staff/soraya_kaiser/git2/2_plots/median5'
figf_out = '/home/skaiser/permamount/staff/soraya_kaiser/git2/2_plots/'
today = datetime.date.today()

files_2006 = []
files_2010 = []
files_2013 = []

for root, dirs, files in os.walk(path_in):
    for file in files:
        for i in range(0,4):
            if fnmatch.fnmatch(file, '*ts%s_*.csv' % i):
                filepath = root + '/' + file
                files_2006.append(filepath)
        for i in range(4,8):
            if fnmatch.fnmatch(file, '*ts%s_*.csv' % i):
                filepath = root + '/' + file
                files_2010.append(filepath)
        for i in range(8,12):
            if fnmatch.fnmatch(file, '*ts%s_*.csv' % i):
                filepath = root + '/' + file
                files_2013.append(filepath)

files_in = [files_2006, files_2010, files_2013]
#%%
path_in = '/home/skaiser/permamount/staff/soraya_kaiser/git2/2_plots/median5/cum'


files_2006_2013 = []
files_2006_2016 = []

for root, dirs, files in os.walk(path_in):
    for file in files:
        for i in range(8,12):
            if fnmatch.fnmatch(file, '*tscomp%s_*.csv' % i):
                filepath = root + '/' + file
                files_2006_2013.append(filepath)
        for i in range(12,16):
            if fnmatch.fnmatch(file, '*tscomp%s_*.csv' % i):
                filepath = root + '/' + file
                files_2006_2016.append(filepath)
                
files_in_cum = [files_2006, files_2006_2013, files_2006_2016]


#%% Create means of movement and direction and merge them into one dataframe
years = ['2006-2010', '2010-2013', '2013-2016']
dfs = []
count = 0
dirs = []
mean_dfs = []
empty = []

for i in files_in:
    print count
    for y in i:

        lake_id = y.rsplit('/')[-1][:-4]
        print lake_id
        try:
    
            df = pd.read_csv(y)
           
            direction = np.array(df['direction'])
            dir_mean = np.mean(df['direction'])
            mv_mean = np.mean(df['distance'])
            for i in direction:
                if 22.5 <= i < 67.5:
                    y = 'NE'
                elif 67.5 <= i < 112.5:
                    y = 'E'
                elif 112.5 <= i < 157.5:
                    y = 'SE'
                elif 157.5 <= i < 202.5:
                    y = 'S'
                elif 202.5 <= i < 247.5:   
                    y = 'SW'
                elif 247.5 <= i < 292.5:
                    y = 'W'
                elif 292.5 <= i < 337.5:
                    y = 'NW'
                else:
                    y = 'N'
                dirs.append(y)
            mean_df = pd.DataFrame({'lake': lake_id, 'dir': dir_mean, 'mv': mv_mean, 'years': years[count]}, index = [0])   
            mean_dfs.append(mean_df)       
            df['category'] = dirs
            df['year'] = [years[count]] * len(direction)
            df = df.drop(['Unnamed: 0', 'geometry', 'direction', 'min_dist_idy'], axis = 1)
            dfs.append(df)
        except:
            empty.append(lake_id)
    count += 1
    
    
data = pd.concat(mean_dfs)

#%% Convert mean directions in degree to string and save to dataframe
dirs = []

direction = np.array(data['dir'])
for i in direction:
    if 22.5 <= i < 67.5:
        y = 'NE'
    elif 67.5 <= i < 112.5:
        y = 'E'
    elif 112.5 <= i < 157.5:
        y = 'SE'
    elif 157.5 <= i < 202.5:
        y = 'S'
    elif 202.5 <= i < 247.5:   
        y = 'SW'
    elif 247.5 <= i < 292.5:
        y = 'W'
    elif 292.5 <= i < 337.5:
        y = 'NW'
    elif np.isnan(i) == True:
        y = np.nan
    else:
        y = 'N'
    dirs.append(y)
    
data['category'] = dirs
data.to_csv(figf_out + 'median5/%s_mean_data.csv' % (str(today.year) + str(today.month) + str(today.day)))       

#%%
##
####    Calculate difference in areas for each lake of polygon files 
####
####    Load polygon files, calculate area for each lake 


lake_ids = []       
gdfs = []      

for i in range(0, 16):
    lake_ids = []
    path = figf_out + 'median5/ts%s.csv' % str(i) 
    df = pd.read_csv(path)

    if i < 4:
        df = df.drop(['area', 'DN', 'id'], axis = 1)
    else:
        df = df.drop(['geometry_x'], axis = 1)
    df['geometry'] = df['geometry'].apply(wkt.loads)
    y = np.array(df.id_right)
    for x in y:
        z = 'gdf_ts%s_lake%s' % (str(i), str(int(x)))
        print z
        lake_ids.append(z)
    df['lake'] = lake_ids
    gdf = gpd.GeoDataFrame(df, geometry = 'geometry')
    gdf['area'] = gdf.area.astype(int)
    gdfs.append(gdf)
    

#%% loop through gdfs to calculate area 
#diffs = []
diff_gdfs = []

for y in range(len(gdfs)-4):  # 
    diffs = []

    df1 = gdfs[y]
    df2 = gdfs[y+4]

    lake_ids1 = df1.id_right.unique()
    ####
    lake_ids = lake_ids1.astype(int)
    print len(lake_ids), y
    for lake_id in lake_ids:
#        print lake_id

        area2 = df2[(df2['id_right']==lake_id)]
        area1 = df1[(df1['id_right']==lake_id)]
        diff = np.asarray(area2.area) - np.asarray(area1.area)
        if diff.size == 0:
#            print 'Yes'
            y = -999
#            print y
        else:
            y = diff[0]
#            print y
        diffs.append(np.int(y))
    print len(diffs)    
    df1['diff'] = diffs
    df1.head()
        
data_diff = pd.concat(gdfs[0:12])
#%%

merged = data_diff.merge(data, on = 'lake')

merged.to_csv(figf_out + 'median5/%s_mean_diffs_data.csv' % (str(today.year) + str(today.month) + str(today.day)))

#%% Minimize data

df = pd.read_csv(figf_out + 'median5/%s_mean_diffs_data.csv' % (str(today.year) + str(today.month) + str(today.day)))
df.columns
df = df.drop(['Unnamed: 0', 'Unnamed: 0.1', 'geometry'], axis = 1)

#%% Scatter Plot

x_val = np.array(df.area) # neeeee, HIER DIE DIFFS
y_val = np.array(df.mv)

#plt.scatter(x, y)

types = np.array(df.id_right)
 
for i,type in enumerate(types):
    x = x_val[i]
    y = y_val[i]
    plt.scatter(x, y, marker='x', color='red')
    plt.text(x+0.3, y+0.3, type, fontsize=9)
plt.xlim(0, 150000)
plt.ylim(0, 70)
plt.show()


#%%
years = ['2006-2010', '2010-2013', '2013-2016']
dfs = []
count = 0

mean_dfs = []
for i in files_in:
    print count
    for y in i:
        lake_id = y.rsplit('/')[-1][:-4]
    
        try: 
            df = pd.read_csv(y)
            print y
        
            direction = np.array(df['direction'])
            dir_mean = np.mean(df['direction'])
            mv_mean = np.mean(df['distance'])
            for i in direction:
                if 22.5 <= i < 67.5:
                    y = 'NE'
                elif 67.5 <= i < 112.5:
                    y = 'E'
                elif 112.5 <= i < 157.5:
                    y = 'SE'
                elif 157.5 <= i < 202.5:
                    y = 'S'
                elif 202.5 <= i < 247.5:   
                    y = 'SW'
                elif 247.5 <= i < 292.5:
                    y = 'W'
                elif 292.5 <= i < 337.5:
                    y = 'NW'
                else:
                    y = 'N'
                dirs.append(y)
        
                        
            df['category'] = dirs
            df['year'] = [years[count]] * len(direction)
            df = df.drop(['Unnamed: 0', 'geometry', 'direction', 'min_dist_idy'], axis = 1)
            dfs.append(df)
        except: 
            print 'empty sequence'
            
    count += 1

#%%

cum_years = ['2006-2010', '2006-2013', '2006-2016']
cum_dfs = []
count = 0

for i in files_in_cum:
    print count
    for y in i:
        try: 
            df = pd.read_csv(y)
            print y
        
            direction = np.array(df['direction'])
            dirs = []
            for i in direction:
                if 22.5 <= i < 67.5:
                    y = 'NE'
                elif 67.5 <= i < 112.5:
                    y = 'E'
                elif 112.5 <= i < 157.5:
                    y = 'SE'
                elif 157.5 <= i < 202.5:
                    y = 'S'
                elif 202.5 <= i < 247.5:   
                    y = 'SW'
                elif 247.5 <= i < 292.5:
                    y = 'W'
                elif 292.5 <= i < 337.5:
                    y = 'NW'
                else:
                    y = 'N'
                dirs.append(y)
        
            df['category'] = dirs
            df['year'] = [cum_years[count]] * len(direction)
            df = df.drop(['Unnamed: 0', 'geometry', 'direction', 'min_dist_idy'], axis = 1)
            cum_dfs.append(df)
        except: 
            print 'empty sequence'
            
    count += 1
#%%
colors = [i.upper() for i in ['#1b9e77','#d95f02','#7570b3']]
#%%

n123 = pd.concat(dfs)

n123.pivot_table(columns = "year", index = "category", values = "distance", aggfunc = np.mean).plot.bar(figsize = (10,6), color = colors)
title = 'Direction and Magnitude of Shoreline Movement'
plt.title(title)
plt.xlabel('Direction')
plt.ylabel('[m]')
plt.savefig(figf_out + "%s_%s.pdf" % (str(today.year) + str(today.month) + str(today.day), title))
#%%

cum_n123 = pd.concat(cum_dfs)

cum_n123.pivot_table(columns = "year", index = "category", values = "distance", aggfunc = np.mean).plot.bar(figsize = (10,6), color = colors)
title = 'Direction and Magnitude of Shoreline Movement Cumulative'
plt.title(title)
plt.xlabel('Direction')
plt.ylabel('[m]')
plt.savefig(figf_out + "%s_%s.pdf" % (str(today.year) + str(today.month) + str(today.day), title))

#%%

######
## Plotting water surface areas & area differences
######
wsa = []
data = []
shapes_in = ['/home/skaiser/permamount/staff/soraya_kaiser/git2/1_proc_data/median5/Deadhorse_ref_water_ni.shp', '/home/skaiser/permamount/staff/soraya_kaiser/git2/1_proc_data/median5/Deadhorse_first_water_ni.shp',  '/home/skaiser/permamount/staff/soraya_kaiser/git2/1_proc_data/median5/Deadhorse_second_water_ni.shp',  '/home/skaiser/permamount/staff/soraya_kaiser/git2/1_proc_data/median5/Deadhorse_third_water_ni.shp']
for i in shapes_in:
    gdf = gpd.read_file(i)
    data.append(gdf.area/10000) # to get number in ha
    a = np.sum(np.array(gdf.area/10000))
    wsa.append(a)


wsa_diffs = []
for i in range(1, len(wsa), 1):
    y = wsa[i] - wsa[i-1]
    wsa_diffs.append(y)    
    
wsa_diffs_cum = []
for i in range(1, len(wsa), 1):
    y = wsa[i] - wsa[0]
    wsa_diffs_cum.append(y)

threshold = 0
#%%
wsa_diff_df = pd.DataFrame({'timesteps': years, 'difference': wsa_diffs})    
wsa_diff_df.plot.bar(x = 'timesteps', y = 'difference', rot = 0, figsize = (10,6), color = 'darkred', legend = None)
plt.axhline(y=threshold,linewidth=1, color='k', linestyle = '--')
title = 'Water Surface Area Changes [ha]'
plt.title(title)
plt.xlabel('Timesteps')
plt.ylabel('[ha]')
plt.ylim(min(wsa_diffs)-10 ,max(wsa_diffs) + 10)

count = 0
for i in range(len(years)):
    plt.text(i, max(wsa_diffs) + 5, str(np.around(wsa_diffs[count], decimals = 2)), horizontalalignment= 'center')
    count += 1
    
plt.savefig(figf_out + "%s_%s.pdf" % (str(today.year) + str(today.month) + str(today.day), title))
#%%
wsa_diff_cum_df = pd.DataFrame({'timesteps': cum_years, 'difference': wsa_diffs_cum})    
wsa_diff_cum_df.plot.bar(x = 'timesteps', y = 'difference', rot = 0, figsize = (10,6), color = 'darkred', legend = None)
plt.axhline(y=threshold,linewidth=1, color='k', linestyle = '--')
title = 'Cumulative Water Surface Area Changes [ha]'
plt.title(title)
plt.xlabel('Timesteps')
plt.ylabel('[ha]')
plt.ylim(min(wsa_diffs_cum)-10 ,max(wsa_diffs_cum) + 10)

count = 0
for i in range(len(cum_years)):
    plt.text(i, max(wsa_diffs_cum) + 5, str(np.around(wsa_diffs_cum[count], decimals = 2)), horizontalalignment= 'center')
    count += 1
    
plt.savefig(figf_out + "%s_%s.pdf" % (str(today.year) + str(today.month) + str(today.day), title))
#%%   
wsa_df = pd.DataFrame({'Water Surface Area [ha]': wsa, 'Year': year})
wsa_df.plot.bar(x = 'Year', y = 'Water Surface Area [ha]', rot = 0)
#%%

    
#%% In case of boxplots
   
   
fig, ax = plt.subplots()
ax.boxplot(data, 0, '')

plt.show()
    

