import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import geopandas as gpd
import datetime
import fnmatch, os
from shapely import wkt
import matplotlib.patches as mpatches
#%%
path_in = '/home/skaiser/permamount/staff/soraya_kaiser/git2/2_plots/median5'
figf_out = '/home/skaiser/permamount/staff/soraya_kaiser/git2/2_plots/'
today = datetime.date.today()
#%% FIXED Load .csv files for shoreline movement rates (for each point of each lake)

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

#%% FIXED Create means of movement and direction and merge them into one dataframe WITHOUT fliers
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
           
            dirs = []            
            direction = np.array(df['direction'])
            movement = np.array(df['distance'])
            
            dir_mean = np.mean(df['direction'])
            mv_mean = np.mean(df['distance'])
            
            
            q25, q50, q75 = np.percentile(movement, [25,50,75])
            iqr = q75-q25
            val_max = q75 + 1.5*iqr
            val_min = q25 - 1.5*iqr
            
            fliers = [val_min < x < val_max for x in movement] 
            print val_min, val_max, iqr           
            
            df['filter'] = fliers
            
            outliers = df['filter']
            filtered = []
            count_o = 0
            
            for y in outliers:
#                print count_o
                if y == True:
                    z = movement[count_o]
                else:
                    z = np.nan
                filtered.append(z)
                count_o += 1
                       
          
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
            mean_df = pd.DataFrame({'lake': lake_id, 'dir': dir_mean, 'mv': mv_mean, 'years': years[count], 'fliers': np.mean(outliers)}, index = [0])   
            mean_dfs.append(mean_df)       
            df['outliers'] = filtered             
            df['category'] = dirs
            df['year'] = [years[count]] * len(direction)
            df = df.drop(['Unnamed: 0', 'geometry', 'direction', 'min_dist_idy'], axis = 1)
            dfs.append(df)
        except:
            empty.append(lake_id)
    count += 1
    
    
data = pd.concat(mean_dfs)

####
# Should output dfs and mean_dfs of length 470 and an arrary empty of length 195 (makes a total of 665 lakes)


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
#data.to_csv(figf_out + 'median5/%s_mean_data.csv' % (str(today.year) + str(today.month) + str(today.day)))       

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
    

#%% loop through gdfs to calculate area diffs
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

### should output data_diff with length of 653 containing areas and area_diffs of polygon lakes
#%%

merged = data_diff.merge(data, on = 'lake')

### should output merged gdf with length of the smaller DataFrame (data = 470)

#merged.to_csv(figf_out + 'median5/%s_mean_diffs_data.csv' % (str(today.year) + str(today.month) + str(today.day)))
#%% FIXED tesing multiple datasets in one scatter


mat = np.random.randint(10, size=(6, 4))
df = pd.DataFrame(mat, columns=['A', 'B', 'C', 'D'])
x1, x2, y1, y2 = [df.A, df.B, df.C, df.D]

fig = plt.figure()
ax = fig.add_subplot(111)

ax.scatter(x1, y1, s=10, c='b', marker="s", label='first')
ax.scatter(x2, y2, s=10, c='r', marker="o", label='second')
plt.legend(loc='upper left');
plt.show()

#%% FIXED Scatter Plot for all timesteps
#plt.scatter(x, y)

x_s = [np.array(merged[merged.years == '2006-2010']['diff']), np.array(merged[merged.years == '2010-2013']['diff']), np.array(merged[merged.years == '2013-2016']['diff'])]
y_s = [np.array(merged[merged.years == '2006-2010']['mv']), np.array(merged[merged.years == '2010-2013']['mv']), np.array(merged[merged.years == '2013-2016']['mv'])]
types_s = [np.array(merged[merged.years == '2006-2010']['id_right']), np.array(merged[merged.years == '2010-2013']['id_right']), np.array(merged[merged.years == '2013-2016']['id_right'])]
colors = [i.upper() for i in ['#1b9e77','#d95f02','#7570b3']]
labels = ['2006-2010', '2010-2013', '2013-2016']

#%% FIXED For paper (labels must be turned on and changed in title) with fliers

fig = plt.figure(figsize = (8, 8))
ax = fig.add_subplot(111)
title = 'Scatter ALL timesteps with fliers no labeling'
 
for j in range(0,3):
    x_val = x_s[j]/ float(10000) 
    y_val = y_s[j]
    types = types_s[j]
    color = colors[j]    
    label = labels[j]

    ax.scatter(x_val, y_val, marker='x', color = color, label=label, alpha = 0.7)
#    for i,type in enumerate(types):                         # uncomment these lines to turn off labeling
#        x = x_val[i]                                        #
#        y = y_val[i]                                        #
#        plt.text(x+0.3, y+0.3, type, fontsize=9)            #
plt.title(title)
plt.xlabel('Area Change [ha]')
plt.ylabel('Shoreline Movement [m]')
plt.legend(loc = 'upper left')
#plt.show()
plt.savefig(figf_out + "%s_%s.pdf" % (str(today.year) + str(today.month) + str(today.day), title.replace(' ', '_')), dpi=300, orientation='landscape', format='pdf')

#%% EXP Batch Scatter Plotting NO FLIERS
files_in = ['/home/skaiser/Desktop/scatter/2020226_mean_diffs_data_2006-2010.csv', 
            '/home/skaiser/Desktop/scatter/2020226_mean_diffs_data_2010-2013.csv', 
            '/home/skaiser/Desktop/scatter/2020226_mean_diffs_data_2013-2016.csv'
            ]

for i in files_in:
    
    df = pd.read_csv(i)
#    df = df.drop(['Unnamed: 0', 'Unnamed: 0.1', 'geometry'], axis = 1)
    x_val = np.array(df['diff'])/ float(10000) 
    y_val = np.array(df['mv'])
    types = np.array(df['id_right'])
    title = i.rsplit('/')[-1][8:-4] + '_no_fliers'

    q75, q25 = np.percentile(x_val, [75 ,25])
    iqr = q75 - q25
    data_max = q75 + 1.5*iqr
    data_min = q25 - 1.5*iqr

    fig, ax = plt.subplots(figsize = (6,6)) 
    for i,type in enumerate(types):
        x = x_val[i]                    # diff is not found since it is not joined with area yet
        y = y_val[i]
        ax.scatter(x, y, marker='x', color='red')
        if title == 'mean_data_2013-2016_no_fliers':
            plt.text(x+0.05, y+0.03, type, fontsize=8)
        else:
            plt.text(x+0.5, y+0.3, type, fontsize=8)

    plt.title(title)
    plt.xlabel('Area Change [ha]')
    plt.ylabel('Shoreline Movement [m]')
#    plt.show()
    plt.savefig(figf_out + "%s_%s.pdf" % (str(today.year) + str(today.month) + str(today.day), title), dpi=300, orientation='landscape', format='pdf')

#%% FIXED Batch Scatter Plotting without outliers
files_in = ['/home/skaiser/Desktop/scatter/2020224_mean_diffs_data_2006-2010.csv', 
            '/home/skaiser/Desktop/scatter/2020224_mean_diffs_data_2010-2013.csv', 
            '/home/skaiser/Desktop/scatter/2020224_mean_diffs_data_2013-2016.csv'
            ]

for i in files_in:
    
    df = pd.read_csv(i)
    df = df.drop(['Unnamed: 0', 'Unnamed: 0.1', 'geometry'], axis = 1)
    x_val = np.array(df['diff'])/ float(10000) 
    y_val = np.array(df['mv'])
    types = np.array(df['id_right'])
    title = i.rsplit('/')[-1][8:-4]

    q75, q25 = np.percentile(x_val, [75 ,25])
    iqr = q75 - q25
    data_max = q75 + 1.5*iqr
    data_min = q25 - 1.5*iqr

    fig, ax = plt.subplots(figsize = (6,6)) 
    for i,type in enumerate(types):
        x = x_val[i]
        y = y_val[i]
        ax.scatter(x, y, marker='x', color='red')
        if title == 'mean_diffs_data_2013-2016':
            plt.text(x+0.05, y+0.03, type, fontsize=8)
        else:
            plt.text(x+0.5, y+0.3, type, fontsize=8)

    plt.title(title)
    plt.xlabel('Area Change [ha]')
    plt.ylabel('Shoreline Movement [m]')
#    plt.show()
    plt.savefig(figf_out + "%s_%s.pdf" % (str(today.year) + str(today.month) + str(today.day), title), dpi=300, orientation='landscape', format='pdf')

#%% FIXED Batch Scatter Plotting for most of the data
files_in = ['/home/skaiser/Desktop/scatter/2020224_mean_diffs_data_2006-2010.csv', 
            '/home/skaiser/Desktop/scatter/2020224_mean_diffs_data_2010-2013.csv', 
            '/home/skaiser/Desktop/scatter/2020224_mean_diffs_data_2013-2016.csv'
            ]
stats = []
for i in files_in:
    df = pd.read_csv(i)
    df = df.drop(['Unnamed: 0', 'Unnamed: 0.1', 'geometry'], axis = 1)
    x_val = np.array(df['diff'])/ float(10000) 
    y_val = np.array(df['mv'])
    types = np.array(df['id_right'])
    title = i.rsplit('/')[-1][8:-4]
    
    x_val_max = np.max(x_val)
    x_q75, x_q25 = np.percentile(x_val, [75 ,25])
    x_iqr = x_q75 - x_q25
    x_max = x_q75 + 1.5*x_iqr
    x_min = x_q25 - 1.5*x_iqr

    y_val_max = np.max(y_val)  
    y_q75, y_q25 = np.percentile(y_val, [75 ,25])
    y_iqr = y_q75 - y_q25
    y_max = y_q75 + 1.5*y_iqr
    y_min = y_q25 - 1.5*y_iqr    
    stats.append([title, x_min, x_max, x_iqr, y_min, y_max, y_iqr])      
    ###
    
    fig, ax = plt.subplots(figsize = (6,6)) 
    for i,type in enumerate(types):
        x = x_val[i]
        y = y_val[i]
        ax.scatter(x, y, marker='x', color='orange')
        if title == 'mean_diffs_data_2006-2010':
            plt.xlim(-0.5, 2)
            plt.ylim(0, 10)
        elif title == 'mean_diffs_data_2010-2013':
            plt.xlim(-5, 5)
            plt.ylim(0, 45)
        else:
            plt.xlim(-2, 2)
            plt.ylim(0, 50)
            
        plt.text(x+0.02, y+0.05, type, fontsize=7)    
    plt.title(title)
    plt.xlabel('Area Change [ha]')
    plt.ylabel('Shoreline Movement [m]')
    plt.show()
#    fig.savefig(figf_out + "%s_%s_whiskers.pdf" % (str(today.year) + str(today.month) + str(today.day), title), dpi=300, orientation='landscape', format='pdf')
    




#%% FIXED Plot pivot table

n123 = pd.concat(dfs)

n123.pivot_table(columns = "year", index = "category", values = "outliers", aggfunc = np.mean).plot.bar(figsize = (10,6), color = colors)
title = 'Direction and Magnitude of Shoreline Movement (without outliers)'
plt.title(title)
plt.xlabel('Direction')
plt.ylabel('[m]')
#plt.show() # in order for plt.savefig to work you need to uncomment this line
plt.savefig(figf_out + "%s_%s.pdf" % (str(today.year) + str(today.month) + str(today.day), title.replace(' ', '_')))
#%%

cum_n123 = pd.concat(cum_dfs)

cum_n123.pivot_table(columns = "year", index = "category", values = "distance", aggfunc = np.mean).plot.bar(figsize = (10,6), color = colors)
title = 'Direction and Magnitude of Shoreline Movement Cumulative'
plt.title(title)
plt.xlabel('Direction')
plt.ylabel('[m]')
plt.show()
#plt.savefig(figf_out + "%s_%s.pdf" % (str(today.year) + str(today.month) + str(today.day), title))

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
    

