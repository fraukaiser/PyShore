import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import geopandas as gpd

#%%
#file_in = '/home/skaiser/permamount/staff/soraya_kaiser/git2/2_plots/median5/gdf_ts1_lake483.csv'
#file_in = '/home/skaiser/permamount/staff/soraya_kaiser/git2/2_plots/median5/gdf_ts5_lake483.csv'

files_in = ['/home/skaiser/permamount/staff/soraya_kaiser/git2/2_plots/median5/gdf_ts1_lake483.csv', '/home/skaiser/permamount/staff/soraya_kaiser/git2/2_plots/median5/gdf_ts5_lake483.csv', '/home/skaiser/permamount/staff/soraya_kaiser/git2/2_plots/median5/gdf_ts1_lake483.csv']
years = ['2006-2010', '2010-2013', '2013-2016']
dfs = []
count = 0
for i in files_in:
    
    df = pd.read_csv(i)

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
    df['year'] = [years[count]] * len(direction)
    df = df.drop(['Unnamed: 0', 'geometry', 'direction', 'min_dist_idy'], axis = 1)
    dfs.append(df)
    
    count += 1

#%%

#%%
colors = [i.upper() for i in ['#1b9e77','#d95f02','#7570b3']]
#%%
n1 = dfs[0]
n2 = dfs[1]
n3 = dfs[2]

n123 = pd.concat([n1, n2, n3])
n123.pivot_table(columns = "year", index = "category", values = "distance", aggfunc = np.mean).plot.bar(figsize = (10,10), color = colors)

#%%

######
## Plotting water surface areas
######
data = []
shapes_in = ['/home/skaiser/permamount/staff/soraya_kaiser/git2/1_proc_data/median5/Deadhorse_ref_water_ni.shp', '/home/skaiser/permamount/staff/soraya_kaiser/git2/1_proc_data/median5/Deadhorse_first_water_ni.shp',  '/home/skaiser/permamount/staff/soraya_kaiser/git2/1_proc_data/median5/Deadhorse_second_water_ni.shp',  '/home/skaiser/permamount/staff/soraya_kaiser/git2/1_proc_data/median5/Deadhorse_third_water_ni.shp']
for i in shapes_in:
    gdf = gpd.read_file(i)
    data.append(gdf.area/10000) # to get number in ha
    print np.sum(np.array(gdf.area))
#%%
   
   
fig, ax = plt.subplots()
ax.boxplot(data, 0, '')

plt.show()
    

