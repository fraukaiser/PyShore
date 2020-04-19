# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 17:20:49 2020

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

valid_data = pd.read_csv('/home/skaiser/Desktop/scatter/20200311_valid_data_mod_colored.csv')

#%%
flag_sub = valid_data[(valid_data)['validation'] == 'y']

#%%
#title = 'Water Surface Area [ha]'
#title = 'Water Surface Area Change [ha]'
title = 'Annual Shoreline Movement [m]'
#%%
#data = np.array(flag_sub[flag_sub.sm_correct == 'y']['mv_annual'])
data = np.array(flag_sub['mv_annual'])


#%% FIXED Linear Binning
nr_bins = 20

hist, bins, _ = plt.hist(data, color='darkred', rwidth=1.5, bins=nr_bins)
df = pd.DataFrame()

#df['bins'] = bins[:-1]
#df['frequency'] = hist
df['bins'] = bins[1:]
df['frequency'] = hist

#%% FIXED Logarithmic Binning

logbins = np.logspace(np.log10(bins[0]),np.log10(bins[-1]+1),len(bins))
log_hist, log_bins, _ = plt.hist(data, color='darkred', rwidth=1.5, bins=logbins)
plt.xscale('log')

#df['logbins'] = log_bins[:-1]
#df['log_frequency'] = log_hist

df['logbins'] = log_bins[1:]
df['log_frequency'] = log_hist

#%%
val_class1 = np.array(flag_sub[(flag_sub.sm_correct == 'y') & (flag_sub.klasse == 1)]['mv_annual'])
val_class2 = np.array(flag_sub[(flag_sub.sm_correct == 'y') & (flag_sub.klasse == 2)]['mv_annual'])
val_class3 = np.array(flag_sub[(flag_sub.sm_correct == 'y') & (flag_sub.klasse == 3)]['mv_annual'])
val_class4 = np.array(flag_sub[(flag_sub.sm_correct == 'y') & (flag_sub.klasse == 4)]['mv_annual'])

nval_class1 = np.array(flag_sub[(flag_sub.sm_correct == 'n') & (flag_sub.klasse == 1)]['mv_annual'])
nval_class2 = np.array(flag_sub[(flag_sub.sm_correct == 'n') & (flag_sub.klasse == 2)]['mv_annual'])
nval_class3 = np.array(flag_sub[(flag_sub.sm_correct == 'n') & (flag_sub.klasse == 3)]['mv_annual'])
nval_class4 = np.array(flag_sub[(flag_sub.sm_correct == 'n') & (flag_sub.klasse == 4)]['mv_annual'])

hist_list = [val_class1, val_class2, val_class3, val_class4, nval_class1, nval_class2, nval_class3, nval_class4]
#%% 
names = ['val_class1', 'val_class2', 'val_class3', 'val_class4', 'nval_class1', 'nval_class2', 'nval_class3', 'nval_class4']
count = 0


for i in hist_list:
    hist_data = plt.hist(i, color='darkred', rwidth=1.5, bins=log_bins)
    df[names[count]] = hist_data[0]
    count += 1

#%% Since I couldn't solve the ZeroDivisionError I exported the data to .csv file

#  Workaround for ZeroDivision Error

def percent(w, G):
    array = []
    for i, j in zip(w, G):
        try:
            p = i/ j * 100
        except:
            p = np.nan
        array.append(p)
    return array
    

#df.to_csv(figf_out + str(today.year) + str(today.month) + str(today.day) + '_lin_log_classes_hist.csv')
#%%
#df = pd.read_csv(figf_out + '202043_lin_log_classes_hist.csv')
#%%
# Data
r = np.arange(len(df.log_frequency))
names = [np.around(i, 2) for i in np.array(df.logbins)]
colors = ['#1b9e77','#d95f02','#7570b3','#e7298a']
# From raw value to percentage
#greenBars = [i / j * 100 for i,j in zip(df['greenBars'], totals)]
#greenBars = [float(i) / float(j) * 100 for i,j in zip(df.val_class1, df.log_frequency) if j >= 0]
greenBars = percent(df.val_class1, df.log_frequency)
greenBarsYes = percent(df.val_class1, df.log_frequency)
greenBarsNo = percent(df.nval_class1, df.log_frequency)
#orangeBars = [i / j * 100 for i,j in zip(df.val_class2,  df.log_frequency) if j > 0]
orangeBars = percent(df.val_class2, df.log_frequency)
orangeBarsYes = percent(df.val_class2, df.log_frequency)
orangeBarsNo = percent(df.nval_class2, df.log_frequency)
#blueBars = [i / j * 100 for i,j in zip(df.val_class3,  df.log_frequency) if j > 0]
purpleBars = percent(df.val_class3, df.log_frequency)
purpleBarsYes = percent(df.val_class3, df.log_frequency)
purpleBarsNo = percent(df.nval_class3, df.log_frequency)
#redBars = [i / j * 100 for i,j in zip(df.val_class4,  df.log_frequency) if j > 0]
pinkBars = percent(df.val_class4, df.log_frequency)
pinkBarsYes = percent(df.val_class4, df.log_frequency)
pinkBarsNo = percent(df.nval_class4, df.log_frequency)
#%% 
# plot
barWidth = 0.35

# Create green Bars
plt.subplots(figsize = (16,8))
#plt.bar(r, greenBars, color=colors[0], edgecolor='white', width=barWidth)
plt.bar(r - barWidth/2, greenBarsYes, color=colors[0], edgecolor='white', width=barWidth, label = '1')
plt.bar(r + barWidth/2, greenBarsNo, color=colors[0], edgecolor='white', width=barWidth)

# Create orange Bars
#plt.bar(r, orangeBars, bottom=greenBars, color = colors[1], edgecolor='white', width=barWidth)
plt.bar(r - barWidth/2, orangeBarsYes, bottom=greenBarsYes, color=colors[1], edgecolor='white', width=barWidth, label = '2')
plt.bar(r + barWidth/2, orangeBarsNo, bottom= greenBarsNo, color=colors[1], edgecolor='white', width=barWidth)

# Create blue Bars
#plt.bar(r, purpleBars, bottom=[i+j for i,j in zip(greenBars, orangeBars)], color=colors[2], edgecolor='white', width=barWidth)
plt.bar(r - barWidth/2, purpleBarsYes, bottom=[i+j for i,j in zip(greenBarsYes, orangeBarsYes)], color=colors[2], edgecolor='white', width=barWidth, label = '3')
plt.bar(r + barWidth/2, purpleBarsNo, bottom=[i+j for i,j in zip(greenBarsNo, orangeBarsNo)], color=colors[2], edgecolor='white', width=barWidth)

# Create red Bars
#plt.bar(r, pinkBars, bottom=[i+j+k for i,j,k in zip(greenBars, orangeBars, purpleBars)], color=colors[3], edgecolor='white', width=barWidth)
plt.bar(r - barWidth/2, pinkBarsYes, bottom=[i+j+k for i,j,k in zip(greenBarsYes, orangeBarsYes, purpleBarsYes)], color=colors[3], edgecolor='white', width=barWidth, label = '4')
plt.bar(r + barWidth/2, pinkBarsNo, bottom=[i+j+k for i,j,k in zip(greenBarsNo, orangeBarsNo, purpleBarsNo)], color=colors[3], edgecolor='white', width=barWidth)

# Custom x axis
plt.xticks(r, names)
plt.xlabel(title)
plt.legend()


# Show/Save graphic
plt.savefig(figf_out + str(today.year) + str(today.month) + str(today.day) + '_Binning of_' + title.replace(' ', '_') +'_classes.pdf')
#plt.show()
#rects1 = ax.bar(r - width/2, yes_data, width, label='Yes', color = 'darkgreen')
#rects2 = ax.bar(r + width/2, no_data, width, label='No', color = 'darkred')
#%%




