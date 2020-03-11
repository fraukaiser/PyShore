# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 11:35:30 2020

@author: skaiser
"""

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import geopandas as gpd
import datetime
import fnmatch, os
from shapely import wkt
from matplotlib import patches as ptch
#%%
path_in = '/home/skaiser/permamount/staff/soraya_kaiser/git2/2_plots/median5'
figf_out = '/home/skaiser/permamount/staff/soraya_kaiser/git2/2_plots/'
today = datetime.date.today()

merged = pd.read_csv('/home/skaiser/Desktop/scatter/2020227_mean_diffs_data.csv')
#%% FIXED Calculate Stats for whole dataset

x_val = np.array(merged['diff'])/ float(10000) 
x_val_max = np.max(x_val)
x_q75, x_q25 = np.percentile(x_val, [75 ,25])
x_iqr = x_q75 - x_q25
x_max = x_q75 + 1.5*x_iqr
x_min = x_q25 - 1.5*x_iqr

print x_min, x_max, x_iqr
whiskers = 0
fliers = 0
for j in x_val:
    if x_min < j < x_max:
        whiskers += 1
    else:
        fliers += 1
print whiskers, (whiskers*100)/ (whiskers+fliers) ,fliers

y_val = np.array(merged['mv'])
y_val_max = np.max(y_val)
y_q75, y_q25 = np.percentile(y_val, [75 ,25])
y_iqr = y_q75 - y_q25
y_max = y_q75 + 1.5*y_iqr
y_min = y_q25 - 1.5*y_iqr

print y_min, y_max, y_iqr
whiskers = 0
fliers = 0
for j in y_val:
    if y_min < j < y_max:
        whiskers += 1
    else:
        fliers += 1
print whiskers, (whiskers*100)/ (whiskers+fliers) ,fliers


#%% A - FIXED Scatter Plot for all timesteps in CLASSES

classes = range(1,5)
types_s = [np.array(merged[merged.klasse == 1]['id_right']), np.array(merged[merged.klasse == 2]['id_right']), np.array(merged[merged.klasse == 3]['id_right']), np.array(merged[merged.klasse == 4]['id_right'])]
colors = ['#1b9e77','#d95f02','#7570b3','#e7298a']
x_s = [np.array(merged[merged.klasse == 1]['diff']), np.array(merged[merged.klasse == 2]['diff']), np.array(merged[merged.klasse == 3]['diff']), np.array(merged[merged.klasse == 4]['diff'])]
y_s = [np.array(merged[merged.klasse == 1]['mv']), np.array(merged[merged.klasse == 2]['mv']), np.array(merged[merged.klasse == 3]['mv']), np.array(merged[merged.klasse == 4]['mv'])]

#%% B - FIXED Scatter Plot for all timesteps in CLASSES

fig = plt.figure(figsize = (8, 8))
ax = fig.add_subplot(111)
title = 'Scatter ALL timesteps with fliers with labeling in classes' # zoomed min max, zoomed

for j in range(0,4):
    x_val = x_s[j]/ float(10000) 
    y_val = y_s[j]
    types = types_s[j]
    color = colors[j]    
    #label = labels[j]
    klasse = str(classes[j])

    ax.scatter(x_val, y_val, marker='.', color = color, label=klasse, alpha=0.5)
    for i,type in enumerate(types):                         # uncomment these lines to turn off labeling
        x = x_val[i]                                        #
        y = y_val[i]                                        #
        plt.text(x+0.02, y+0.02, type, fontsize=6)            #
ptch.Rectangle((-20, 0), 40, 40, fill=False, edgecolor='black', linewidth=2.5)
plt.title(title)
plt.xlabel('Area Change [ha]')
plt.ylabel('Shoreline Movement [m]')
#plt.xlim(x_min -1, x_max +1)
#plt.ylim(0, y_max +1)


plt.axhline(y_max,linewidth=1, color='k', linestyle = '--')
plt.axvline(x_min,linewidth=1, color='k', linestyle = '--')
plt.axvline(x_max,linewidth=1, color='k', linestyle = '--')
plt.legend(loc = 'upper left')
#plt.show()
plt.savefig(figf_out + "%s_%s.pdf" % (str(today.year) + str(today.month) + str(today.day), title.replace(' ', '_')), dpi=300, orientation='landscape', format='pdf')


#%% FIXED Calculate Stats for each size category dataset
for i in x_s:
    x_val = i/ float(10000) 
    x_val_max = np.max(x_val)
    x_q75, x_q25 = np.percentile(x_val, [75 ,25])
    x_iqr = x_q75 - x_q25
    x_max = x_q75 + 1.5*x_iqr
    x_min = x_q25 - 1.5*x_iqr
    print x_min, x_max
    whiskers = 0
    fliers = 0
    for j in i:
        j = j/ float(10000)
        if x_min < j < x_max:
            whiskers += 1
        else:
            fliers += 1
    print whiskers, fliers
    
for i in y_s:
    y_val = i
    y_val_max = np.max(y_val)
    y_q75, y_q25 = np.percentile(y_val, [75 ,25])
    y_iqr = y_q75 - y_q25
    y_max = y_q75 + 1.5*y_iqr
    y_min = y_q25 - 1.5*y_iqr
    print y_min, y_max
    whiskers = 0
    fliers = 0
    for j in i:
        j = j/ float(10000)
        if y_min < j < x_max:
            whiskers += 1
        else:
            fliers += 1
    print whiskers, fliers
    
#%% FIXED Calculate Stats for each timestep dataset
x_s = [np.array(merged[merged.years == '2006-2010']['diff']), np.array(merged[merged.years == '2010-2013']['diff']), np.array(merged[merged.years == '2013-2016']['diff'])]
y_s = [np.array(merged[merged.years == '2006-2010']['mv']), np.array(merged[merged.years == '2010-2013']['mv']), np.array(merged[merged.years == '2013-2016']['mv'])]

x_min = []
x_mins = []
x_maxs = []
x_iqrs = []
for i in x_s:
    x_val = i/ float(10000) 
    x_val_max = np.max(x_val)
    x_q75, x_q25 = np.percentile(x_val, [75 ,25])
    x_iqr = x_q75 - x_q25
    x_max = x_q75 + 1.5*x_iqr
    x_min = x_q25 - 1.5*x_iqr
    x_mins.append(x_min)
    x_maxs.append(x_max)
    x_iqrs.append(x_iqr)
    

y_min = []
y_mins = []
y_maxs = []
y_iqrs = []
for i in y_s:
    y_val = i
    y_val_max = np.max(y_val)
    y_q75, y_q25 = np.percentile(y_val, [75 ,25])
    y_iqr = y_q75 - y_q25
    y_max = y_q75 + 1.5*y_iqr
    y_min = y_q25 - 1.5*y_iqr
    y_mins.append(y_min)
    y_maxs.append(y_max)
    y_iqrs.append(y_iqr)
    
#%% FIXED Stats: which lakes are lying within/ outside whiskers. Just change print comment -> output to .csv file
hectars = np.array(merged['diff'])/ float(10000)
merged['hectars'] = hectars
    
diff_ha = merged['hectars']
lake = merged['lake']
count_o = 0
count = 0
for y in diff_ha:
#    print count_o
    if (x_min < y < x_max) & (y < y_max):
        z = lake[count_o]
        print z
        count += 1
    else:
        z = lake[count_o]
#        print z
#        count += 1
    count_o += 1
    print count

