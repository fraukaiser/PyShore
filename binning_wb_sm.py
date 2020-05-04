# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 16:03:16 2020

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
import collections
#%%
path_in = '/home/skaiser/permamount/staff/soraya_kaiser/git2/2_plots/median5'
figf_out = '/home/skaiser/permamount/staff/soraya_kaiser/git2/2_plots/'
today = datetime.date.today()

#duplicates = pd.read_csv('/home/skaiser/Desktop/scatter/20200311_valid_data_mod_colored.csv')
valid_data = pd.read_csv('/home/skaiser/permamount/staff/soraya_kaiser/git2/2_plots/20200417_valid_data_mod_no_duplicates.csv')
#valid_data = pd.read_csv('/home/skaiser/permamount/staff/soraya_kaiser/git2/2_plots/2020414_check_valid_data_again_no_duplicates.csv')
dir_data = pd.read_csv('/home/skaiser/permamount/staff/soraya_kaiser/git2/2_plots/202054_plotting_directions_mod.csv')
## MP 396:
gdf = gpd.read_file('/home/skaiser/permamount/staff/soraya_kaiser/git2/1_proc_data/median5/MP 396_ref_water_ni_noedge.shp')
gdf['area'] = gdf.area
#gdf.plot()
#%% DEFS

def percent_array(w, G):
    array = []
    for i, j in zip(w, G):
        try:
            p = float(i)/ float(j) * 100
        except:
            p = np.nan
        array.append(p)
    return array

def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

def percent(w, G):
    try:
        p = float(w)/ float(G) * 100
    except:
        p = np.nan
    return np.around(p, 1)
    
def CountFrequency(arr): 
    return collections.Counter(arr)


#%%
#x_text = 'Water Surface Area [ha]'
#x_text = 'Water Surface Area Change [ha]'
x_text = 'Annual Shoreline Movement [m]'

#%% Get overview

valid = len(valid_data[valid_data.validation == 'y'])
sm_correct = len(valid_data[valid_data.sm_correct == 'y'])
wb_exact = len(valid_data[valid_data.wb_exact == 'y'])

print valid, sm_correct, wb_exact

#%% Look at flagged data

flag_sub = valid_data[(valid_data)['validation'] == 'y']
#%% Which date should be looked at? Essnetial for binning!!

#data = [float(i)/10000 for i in np.array(flag_sub['area'])]
#data = [float(i)/10000 for i in np.array(flag_sub['diff'])]
#data = np.array(flag_sub['mv_annual'])
data = np.array(valid_data['mv_annual'])


#%% FIXED Linear Binning
#nr_bins = 20
bins = [0.0,
 4.4,
 8.7,
 13.0,
 17.3,
 21.6,
 25.9,
 30.2,
 34.4,
 38.7,
 43.0,
 47.3,
 51.6,
 55.9,
 60.2,
 64.5,
 68.7,
 73.0,
 77.3,
 81.6,
 85.9]
 
hist, bins, _ = plt.hist(data, color='darkred', rwidth=1.5, bins=bins)
df = pd.DataFrame()

#df['bins'] = bins[:-1]
#df['frequency'] = hist
df['bins'] = bins[1:]
df['frequency'] = hist

#%% FIXED Logarithmic Binning

#logbins = np.logspace(np.log10(bins[0]),np.log10(bins[-1]+1),len(bins))
logbins = [0.0,
 0.2,
 0.3,
 0.4,
 0.5,
 0.6,
 0.8,
 1.0,
 1.5,
 2.1,
 2.9,
 4.1,
 5.8,
 8.1,
 11.4,
 16.0,
 22.4,
 31.5,
 44.2,
 62.0,
 86.9]

log_hist, log_bins, _ = plt.hist(data, color='darkred', rwidth=1.5, bins=logbins)
plt.xscale('log')

#df['logbins'] = log_bins[:-1]
#df['log_frequency'] = log_hist

df['logbins'] = log_bins[1:]
df['log_frequency'] = log_hist

#%% LOG or LIN? Log doesn't work for area diff

typei = 'Logarithmic'
#typei = 'Linear'

#%% FIXED WB valid

yes_wb = [float(i)/10000 for i in np.array(valid_data[valid_data.wb_exact == 'y']['area'])]
no_wb = [float(i)/10000 for i in np.array(valid_data[valid_data.wb_exact == 'n']['area'])]

hist_yes_data = plt.hist(yes_wb, color='darkred', rwidth=1.5, bins=log_bins)
hist_no_data = plt.hist(no_wb, color='darkred', rwidth=1.5, bins=log_bins)

df['yes_wb_frequency'] = hist_yes_data[0]
df['no_wb_frequency'] = hist_no_data[0]

#%% FIXED WB yes/no percent

#yes_percent = []
#no_percent = []
#yes = np.array(df.yes_wb_frequency)
#no = np.array(df.no_wb_frequency)
#
#whole = np.array(df.log_frequency)
#count = 0
#for y in yes:
#    print count
#    z = y*100/whole[count]    
#    yes_percent.append(z)
#    count += 1
#count = 0
#for y in no:
#    print count
#    z = y*100/whole[count]    
#    no_percent.append(z)
#    count += 1
#        
#df['yes_wb_percent'] = yes_percent
#df['no_wb_percent'] = no_percent
#
#df.to_csv(figf_out + str(today.year) + str(today.month) + str(today.day) + '_' + x_text.replace(' ', '_') + '_lin_log_hist.csv')
#%% FIXED SM and WB valid

yes_wb = np.array(valid_data[valid_data.wb_exact == 'y']['mv_annual'])
no_wb = np.array(valid_data[valid_data.wb_exact == 'n']['mv_annual'])

yes_sm = np.array(valid_data[valid_data.sm_correct == 'y']['mv_annual'])
no_sm = np.array(valid_data[valid_data.sm_correct == 'n']['mv_annual'])

hist_yes_data = plt.hist(yes_wb, color='darkred', rwidth=1.5, bins=log_bins)
hist_no_data = plt.hist(no_wb, color='darkred', rwidth=1.5, bins=log_bins)

hist_yes_sm_data = plt.hist(yes_sm, color='darkred', rwidth=1.5, bins=log_bins)
hist_no_sm_data = plt.hist(no_sm, color='darkred', rwidth=1.5, bins=log_bins)

df['yes_wb_frequency'] = hist_yes_data[0]
df['no_wb_frequency'] = hist_no_data[0]

df['yes_sm_frequency'] = hist_yes_sm_data[0]
df['no_sm_frequency'] = hist_no_sm_data[0]

#%% EXAMPLE for double filtering

#y = np.array(flag_sub[(flag_sub.wb_exact == 'y') & (flag_sub.klasse == 1)]['mv_annual'])

#%% FIXED SM & WB yes/no 


#yes_sm_percent = []
#no_sm_percent = []
#yes = np.array(df.yes_sm_frequency)
#no = np.array(df.no_sm_frequency)
#
#whole = np.array(df.log_frequency)
#count = 0
#for y in yes:
#    print count
#    z = y*100/whole[count]    
#    yes_sm_percent.append(z)
#    count += 1
#count = 0
#for y in no:
#    print count
#    z = y*100/whole[count]    
#    no_sm_percent.append(z)
#    count += 1
#        
#df['yes_sm_percent'] = yes_sm_percent
#df['no_sm_percent'] = no_sm_percent
#
#yes_percent = []
#no_percent = []
#yes = np.array(df.yes_wb_frequency)
#no = np.array(df.no_wb_frequency)
#
#count = 0
#for y in yes:
#    print count
#    z = y*100/whole[count]    
#    yes_percent.append(z)
#    count += 1
#count = 0
#for y in no:
#    print count
#    z = y*100/whole[count]    
#    no_percent.append(z)
#    count += 1
#        
#df['yes_wb_percent'] = yes_percent
#df['no_wb_percent'] = no_percent
#
#df.to_csv(figf_out + str(today.year) + str(today.month) + str(today.day) + '_' + x_text.replace(' ', '_') + '_lin_log_hist.csv')
#%% FIXED Stack WB
#labels = [np.around(i, 2) for i in np.array(df.logbins)]
#yes_data = [np.around(i) for i in np.array(df.yes_wb_percent)]
#no_data = [np.around(i) for i in np.array(df.no_wb_percent)]
#
#x = np.arange(len(labels))  # the label locations
#width = 0.35  # the width of the bars
#
#fig, ax = plt.subplots(figsize = (16,8))
#rects1 = ax.bar(x - width/2, yes_data, width, label='Yes', color = 'darkgreen')
#rects2 = ax.bar(x + width/2, no_data, width, label='No', color = 'darkred')
#
## Add some text for labels, title and custom x-axis tick labels, etc.
#ax.set_ylabel('%')
#ax.set_xlabel(x_text)
#ax.set_title(typei + ' binning of ' + x_text)
#ax.set_xticks(x)
#ax.set_xticklabels(labels)
#ax.legend()
#
#def autolabel(rects):
#    """Attach a text label above each bar in *rects*, displaying its height."""
#    for rect in rects:
#        height = rect.get_height()
#        ax.annotate('{}'.format(height),
#                    xy=(rect.get_x() + rect.get_width() / 2, height),
#                    xytext=(0, 3),  # 3 points vertical offset
#                    textcoords="offset points",
#                    ha='center', va='bottom')
#
#
#autolabel(rects1)
#autolabel(rects2)
#plt.savefig(figf_out + str(today.year) + str(today.month) + str(today.day) + '_' + typei + '_Binning_of_' + x_text +'wb.pdf')

#%% FIXED Stack WB and SM part I
#labels = [np.around(i, 2) for i in np.array(df.logbins)]
#yes_data = [np.around(i) for i in np.array(df.yes_wb_percent)]
#no_data = [np.around(i) for i in np.array(df.no_wb_percent)]
#
#x = np.arange(len(labels))  # the label locations
#width = 0.35  # the width of the bars
#
#fig, ax = plt.subplots(figsize = (16,8))
#rects1 = ax.bar(x - width/2, yes_data, width, label='Yes', color = 'darkgreen')
#rects2 = ax.bar(x + width/2, no_data, width, label='No', color = 'darkred')
#
## Add some text for labels, title and custom x-axis tick labels, etc.
#ax.set_ylabel('%')
#ax.set_xlabel(x_text)
#ax.set_title(typei + ' binning of ' + x_text)
#ax.set_xticks(x)
#ax.set_xticklabels(labels)
#ax.legend()
#
#def autolabel(rects):
#    """Attach a text label above each bar in *rects*, displaying its height."""
#    for rect in rects:
#        height = rect.get_height()
#        ax.annotate('{}'.format(height),
#                    xy=(rect.get_x() + rect.get_width() / 2, height),
#                    xytext=(0, 3),  # 3 points vertical offset
#                    textcoords="offset points",
#                    ha='center', va='bottom')
#
#
#autolabel(rects1)
#autolabel(rects2)
#plt.savefig(figf_out + str(today.year) + str(today.month) + str(today.day) + '_' + typei + '_Binning of_' + x_text.replace(' ', '_') +'wb.pdf')

#%% FIXED Stack WB and SM part II CUMULATIVE
labels = [np.around(i, 2) for i in np.array(df.logbins)]
#labels = [np.around(i, 2) for i in np.array(df.bins)]

#yes_data = [np.around(i) for i in np.array(df.yes_sm_percent)]
#no_data = [np.around(i) for i in np.array(df.no_sm_percent)]

# Cumulative 
yes_data = [int(i) for i in np.array(np.cumsum(df.yes_sm_frequency))]
no_data = [int(i) for i in np.array(np.cumsum(df.no_sm_frequency))]
#data = [int(i) for i in np.array(df.log_frequency)]


x = np.arange(len(labels))  # the label locations
width = 0.40  # the width of the bars

fig, ax = plt.subplots(figsize = (18,8))
rects1 = ax.bar(x - width/2, yes_data, width, label='correct', color = 'darkgreen')
rects2 = ax.bar(x + width/2, no_data, width, label='false', color = 'darkred')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Number of Lakes')
ax.set_xlabel(x_text)
title = 'Cumulative histogram of ' + x_text
ax.set_title(title)
ax.set_xticks(x)
ax.set_xticklabels(labels)
plt.rcParams.update({'font.size': 15})

ax.legend()


autolabel(rects1)
autolabel(rects2)
plt.savefig(figf_out + str(today.year) + str(today.month) + str(today.day) + '_' + title.replace(' ', '_') +'_cum_labeled_sm.pdf')

#%% part I: now do histogram yes/ no for each lake size category 

## sizes now logarithmic as well: 30 x 30, 60 x 60, 120 x 120, 240 x 240
area_cats = []

for i in valid_data.area:
    if i < 3600:
        y = 1
    elif 3600 <= i < 14400:
        y = 2
    elif 1440 <= i < 57600:
        y = 3
    elif 57600 <= i < 230400:
        y = 4
    elif i >= 230400:
        y = 5
    area_cats.append(y)
    
valid_data['area_cats'] = area_cats


#%% part II for WB exact sizes now logarithmic as well: 30 x 30, 60 x 60, 120 x 120, 240 x 240

#### HERE
######

#nr_bins = len(np.unique(valid_data.area_cats))
##labels = np.arange(1, nr_bins + 1, 1)
#
#labels = ['< 0.36', '0.36 - 1.44', '1.44 - 5.76', '5.76 - 23.04', '> 23.04']
#yes_wb = np.array(valid_data[valid_data.wb_exact == 'y']['area_cats'])
#no_wb = np.array(valid_data[valid_data.wb_exact == 'n']['area_cats'])
#all_wb = np.array(valid_data[valid_data.validation == 'y']['area_cats'])
#
#yes_data = [np.around(i) for i in percent_array(plt.hist(yes_wb, bins = nr_bins)[0], plt.hist(all_wb, bins = nr_bins)[0])]
#no_data = [np.around(i) for i in percent_array(plt.hist(no_wb, bins = nr_bins)[0], plt.hist(all_wb, bins = nr_bins)[0])]
#
#x = np.arange(len(labels))  # the label locations
#width = 0.35  # the width of the bars
#
#fig, ax = plt.subplots(figsize = (8,8))
#rects1 = ax.bar(x - width/2, yes_data, width, label='Yes', color = 'darkgreen')
#rects2 = ax.bar(x + width/2, no_data, width, label='No', color = 'darkred')
#
#ax.set_ylabel('%')
#ax.set_xlabel('Lake Size [ha]')
#title = 'Quality of Shoreline Derivation per Lake Size Category (wb_exact)'
#ax.set_title(title)
#ax.set_xticks(x)
#ax.set_xticklabels(labels)
#ax.legend()
#
#autolabel(rects1)
#autolabel(rects2)

#plt.savefig(figf_out + str(today.year) + str(today.month) + str(today.day) + '_' + title.replace(' ', '_') +'.pdf')


#%% part II for SM correct sizes now logarithmic as well: 30 x 30, 60 x 60, 120 x 120, 240 x 240

#### HERE
######

nr_bins = len(np.unique(valid_data.area_cats))
#labels = np.arange(1, nr_bins + 1, 1)

labels = ['< 0.36', '0.36 - 1.44', '1.44 - 5.76', '5.76 - 23.04', '> 23.04']
yes_sm = np.array(valid_data[valid_data.sm_correct == 'y']['area_cats'])
no_sm = np.array(valid_data[valid_data.sm_correct == 'n']['area_cats'])
all_wb = np.array(valid_data[valid_data.validation == 'y']['area_cats'])

yes_data = [np.around(i) for i in percent_array(plt.hist(yes_sm, bins = nr_bins)[0], plt.hist(all_wb, bins = nr_bins)[0])]
no_data = [np.around(i) for i in percent_array(plt.hist(no_sm, bins = nr_bins)[0], plt.hist(all_wb, bins = nr_bins)[0])]

x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots(figsize = (8,8))
rects1 = ax.bar(x - width/2, yes_data, width, label='Yes', color = 'darkgreen')
rects2 = ax.bar(x + width/2, no_data, width, label='No', color = 'darkred')

ax.set_ylabel('%')
ax.set_xlabel('Lake Size [ha]')
title = 'Quality of Shoreline Derivation per Lake Size Category (sm_correct new classes)'
ax.set_title(title)
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

autolabel(rects1)
autolabel(rects2)

plt.savefig(figf_out + str(today.year) + str(today.month) + str(today.day) + '_' + title.replace(' ', '_') +'.pdf')

#%% what about the old sizes? for WB
#nr_bins = len(np.unique(valid_data.klasse))
##labels = np.arange(1, 5, 1)
#labels = ['< 0.1 - 1.0', '1.0 - 10.0', '10.0 - 40.0', '> 40.0']
#yes_wb = np.array(valid_data[valid_data.wb_exact == 'y']['klasse'])
#no_wb = np.array(valid_data[valid_data.wb_exact == 'n']['klasse'])
#all_wb = np.array(valid_data[valid_data.validation == 'y']['klasse'])
#
#yes_data = [np.around(i) for i in percent_array(plt.hist(yes_wb, bins = nr_bins)[0], plt.hist(all_wb, bins = nr_bins)[0])]
#no_data = [np.around(i) for i in percent_array(plt.hist(no_wb, bins = nr_bins)[0], plt.hist(all_wb, bins = nr_bins)[0])]
#x = np.arange(len(labels))  # the label locations
#width = 0.35  # the width of the bars
#
#fig, ax = plt.subplots(figsize = (8,8))
#rects1 = ax.bar(x - width/2, yes_data, width, label='Yes', color = 'darkgreen')
#rects2 = ax.bar(x + width/2, no_data, width, label='No', color = 'darkred')
#
#ax.set_ylabel('%')
#ax.set_xlabel('Lake Size [ha]')
#title = 'Quality of Shoreline Derivation per Lake Size Category (wb_exact old classes)'
#ax.set_title(title)
#ax.set_xticks(x)
#ax.set_xticklabels(labels)
#ax.legend()
#
#autolabel(rects1)
#autolabel(rects2)
#
#plt.savefig(figf_out + str(today.year) + str(today.month) + str(today.day) + '_' + title.replace(' ', '_') +'.pdf')


#%% what about the old sizes? for SM
nr_bins = len(np.unique(valid_data.klasse))
#labels = np.arange(1, 5, 1)
labels = ['< 0.1 - 1.0', '1.0 - 10.0', '10.0 - 40.0', '> 40.0']
yes_sm = np.array(valid_data[valid_data.sm_correct == 'y']['klasse'])
no_sm = np.array(valid_data[valid_data.sm_correct == 'n']['klasse'])
all_wb = np.array(valid_data[valid_data.validation == 'y']['klasse'])

yes_data = [np.around(i) for i in percent_array(plt.hist(yes_sm, bins = nr_bins)[0], plt.hist(all_wb, bins = nr_bins)[0])]
no_data = [np.around(i) for i in percent_array(plt.hist(no_sm, bins = nr_bins)[0], plt.hist(all_wb, bins = nr_bins)[0])]
x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots(figsize = (8,8))
rects1 = ax.bar(x - width/2, yes_data, width, label='Yes', color = 'darkgreen')
rects2 = ax.bar(x + width/2, no_data, width, label='No', color = 'darkred')

ax.set_ylabel('%')
ax.set_xlabel('Lake Size [ha]')
title = 'Quality of Shoreline Derivation per Lake Size Category (sm_correct old classes)'
ax.set_title(title)
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

autolabel(rects1)
autolabel(rects2)

plt.savefig(figf_out + str(today.year) + str(today.month) + str(today.day) + '_' + title.replace(' ', '_') +'.pdf')
#%%
flag_sub = valid_data[(valid_data)['validation'] == 'y']
flag_sub.to_csv(figf_out + str(today.year) + str(today.month) + str(today.day) + 'check_valid_data_again.csv')

#%% Plot SM histogram for the whole dataset
labels = [np.around(i, 2) for i in np.array(df.logbins)]
#data = [int(i) for i in np.array(df.log_frequency)] # plots total number of whole dataset for each bin
#data = [int(i) for i in np.cumsum(np.array(df.log_frequency))] # plots cum total number of whole dataset for each bin

#data = [percent(i, 463) for i in np.array(df.log_frequency)] # plots percentage of whole dataset for each bin
data = [percent(i, 463) for i in np.cumsum(np.array(df.log_frequency))] # plots cum percentage of whole dataset for each bin



fig, ax = plt.subplots(figsize = (18,8))
rects1 = ax.bar(x, data, width, color = 'orange')


# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Number of Lakes')
#ax.set_ylabel('Percentage of Whole Dataset')

ax.set_xlabel(x_text)
#ax.set_title(typei + ' binning of ' + x_text)
ax.set_xticks(x)
ax.set_xticklabels(labels)
plt.rcParams.update({'font.size': 15})
#ax.legend()

def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

autolabel(rects1)

plt.savefig(figf_out + str(today.year) + str(today.month) + str(today.day) + '_' + '_Binning of_' + x_text.replace(' ', '_') +'_all_lakes_cumpercentage.pdf')

#%% Plot mean annual shoreline movement & direction for every size category


# 1. Identify distribution of shoreline movement direction

labels = ['NE', 'E', 'SE', 'S', 'SW', 'W', 'NW', 'N']
Counter(valid_data.category)
## OUTPUT
Counter({'E': 95, 'NE': 1, 'S': 137, 'SE': 155, 'SW': 73, 'W': 2})

#%%
x = np.arange(1, len(labels) +1, 1)  # the label locations
width = 0.5  # the width of the bars
data = [1, 95, 155, 137, 73, 2, 0, 0]
total = np.cumsum(data)[-1] # for calculation of percentages
totals = [total] * len(data)

percent_array(data, totals)
# OUTPUT     [0.0, 21.0, 33.0, 30.0, 16.0, 0.0, 0.0, 0.0]


fig, ax = plt.subplots(figsize = (8,8))
rects = ax.bar(x, data, width, color = '#59B18C')
#ax.hist(np.array(valid_data.direction), bins = len(labels))
ax.set_ylabel('number of lakes')
ax.set_xlabel('Direction of shoreline movement')
title = 'Spatial Pattern of Shoreline Movement'
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.set_title(title)
autolabel(rects)

plt.savefig(figf_out + str(today.year) + str(today.month) + str(today.day) + '_' + title.replace(' ', '_') +'number.pdf')

#%%
# 2. Plot SM for every size category/ timestep

# NEW classes
MV_area_cats_sm_c = [np.array(valid_data[(valid_data.sm_correct == 'y') & (valid_data.area_cats == 1)]['mv_annual']), 
                    np.array(valid_data[(valid_data.sm_correct == 'y') & (valid_data.area_cats == 2)]['mv_annual']), 
                    np.array(valid_data[(valid_data.sm_correct == 'y') & (valid_data.area_cats == 3)]['mv_annual']), 
                    np.array(valid_data[(valid_data.sm_correct == 'y') & (valid_data.area_cats == 4)]['mv_annual']),
                    np.array(valid_data[(valid_data.sm_correct == 'y') & (valid_data.area_cats == 5)]['mv_annual'])]
                    
## OLD classes              
#MV_area_cats_sm_c = [np.array(valid_data[(valid_data.sm_correct == 'y') & (valid_data.klasse == 1)]['mv_annual']), 
#                    np.array(valid_data[(valid_data.sm_correct == 'y') & (valid_data.klasse == 2)]['mv_annual']), 
#                    np.array(valid_data[(valid_data.sm_correct == 'y') & (valid_data.klasse == 3)]['mv_annual']), 
#                    np.array(valid_data[(valid_data.sm_correct == 'y') & (valid_data.klasse == 4)]['mv_annual'])]
#                    
#MV_years_sm_c = [np.array(valid_data[(valid_data.sm_correct == 'y') & (valid_data.years == '2006-2010')]['mv_annual']), 
#                    np.array(valid_data[(valid_data.sm_correct == 'y') & (valid_data.years == '2010-2013')]['mv_annual']), 
#                    np.array(valid_data[(valid_data.sm_correct == 'y') & (valid_data.years == '2013-2016')]['mv_annual'])]
#                    
labels = ['< 0.36', '0.36 - 1.44', '1.44 - 5.76', '5.76 - 23.04', '> 23.04']
#labels = ['< 0.1 - 1.0', '1.0 - 10.0', '10.0 - 40.0', '> 40.0']
#labels = ['2006-2010', '2010-2013', '2013-2016']


data = np.array([np.around(np.mean(i), 2) for i in MV_area_cats_sm_c])
x = np.arange(len(labels))  # the label locations

fig, ax = plt.subplots(figsize = (12,9))
rects1 = ax.bar(x, data, width, color = 'orange')


# Add some text for labels, title and custom x-axis tick labels, etc.
x_text = 'annual shoreline movement [m]'
y_text = 'time step'
title = 'Mean annual shoreline movement per time step (valid lakes)'
ax.set_ylabel(x_text)
ax.set_xlabel(y_text)
ax.set_title(title)


ax.set_xticks(x)
ax.set_xticklabels(labels)
plt.rcParams.update({'font.size': 15})
autolabel(rects1)
#ax.legend()

plt.savefig(figf_out + str(today.year) + str(today.month) + str(today.day) + '_' + title.replace(' ', '_') + '.pdf')

#%% 

# 3. Now directions per Sizes

## ALL DATA 
#new classes
#MDIR_area_cats_sm_c = [np.array(valid_data[valid_data.area_cats == 1]['category']), 
#                    np.array(valid_data[valid_data.area_cats == 2]['category']), 
#                    np.array(valid_data[valid_data.area_cats == 3]['category']), 
#                    np.array(valid_data[valid_data.area_cats == 4]['category']),
#                    np.array(valid_data[valid_data.area_cats == 5]['category'])]
# old classes
#MDIR_area_cats_sm_c = [np.array(valid_data[valid_data.klasse == 1]['category']), 
#                    np.array(valid_data[valid_data.klasse == 2]['category']), 
#                    np.array(valid_data[valid_data.klasse == 3]['category']), 
#                    np.array(valid_data[valid_data.klasse == 4]['category'])]

for i in MDIR_area_cats_sm_c:
    print Counter(i)

# OUTPUT new classes
Counter({'SE': 73, 'S': 62, 'E': 36, 'SW': 26})
Counter({'SE': 52, 'E': 42, 'S': 42, 'SW': 29, 'W': 2, 'NE': 1})
Counter({'S': 18, 'SE': 13, 'E': 12, 'SW': 10})
Counter({'S': 9, 'E': 3, 'SE': 3, 'SW': 1})
Counter({'SE': 14, 'SW': 7, 'S': 6, 'E': 2})

# OUTPUT new classes
Counter({'SE': 111, 'S': 98, 'E': 71, 'SW': 50, 'W': 2, 'NE': 1})
Counter({'S': 31, 'SE': 29, 'E': 20, 'SW': 15})
Counter({'SE': 4, 'S': 3, 'SW': 2, 'E': 2})
Counter({'SE': 11, 'SW': 6, 'S': 5, 'E': 2})

## VALIDATED DATA
#new classes
MDIR_area_cats_sm_c = [np.array(valid_data[(valid_data.sm_correct == 'y') & (valid_data.area_cats == 1)]['category']), 
                    np.array(valid_data[(valid_data.sm_correct == 'y') & (valid_data.area_cats == 2)]['category']), 
                    np.array(valid_data[(valid_data.sm_correct == 'y') & (valid_data.area_cats == 3)]['category']), 
                    np.array(valid_data[(valid_data.sm_correct == 'y') & (valid_data.area_cats == 4)]['category']),
                    np.array(valid_data[(valid_data.sm_correct == 'y') & (valid_data.area_cats == 5)]['category'])]
# old classes
#MDIR_area_cats_sm_c = [np.array(valid_data[(valid_data.sm_correct == 'y') & (valid_data.klasse == 1)]['category']), 
#                    np.array(valid_data[(valid_data.sm_correct == 'y') & (valid_data.klasse == 2)]['category']), 
#                    np.array(valid_data[(valid_data.sm_correct == 'y') & (valid_data.klasse == 3)]['category']), 
#                    np.array(valid_data[(valid_data.sm_correct == 'y') & (valid_data.klasse == 4)]['category'])]


for i in MDIR_area_cats_sm_c:
    print CountFrequency(i)
 
## OUTPUT old classes
#Counter({'S': 6, 'E': 4, 'SW': 4, 'SE': 4})
#Counter({'E': 3, 'SW': 3, 'SE': 1})
#Counter({'SE': 4, 'S': 3})
#Counter({'SE': 4, 'S': 2, 'SW': 1})
#
## OUTPUT new classes
#Counter({'S': 5, 'E': 3, 'SW': 2, 'SE': 2})
#Counter({'SW': 4, 'SE': 3, 'E': 2, 'S': 1})
#Counter({'E': 1, 'SW': 1})
#Counter({'S': 2, 'E': 1, 'SE': 1})
#Counter({'SE': 7, 'S': 3, 'SW': 1})

#%%   Now directions per years
                 
MDIR_years_sm_c = [np.array(valid_data[(valid_data.sm_correct == 'y') & (valid_data.years == '2006-2010')]['category']), 
                    np.array(valid_data[(valid_data.sm_correct == 'y') & (valid_data.years == '2010-2013')]['category']), 
                    np.array(valid_data[(valid_data.sm_correct == 'y') & (valid_data.years == '2013-2016')]['category'])]
                    
#for i in MDIR_years_sm_c:
#    print Counter(i)
    
### OUTPUT   new classes 
### {'SE': 9, 'S': 4, 'E': 2, 'SW': 1}
### {'SW': 7, 'S': 6, 'SE': 1}
### {'E': 5, 'SE': 3, 'S': 1}
    
MDIR_years_all_lakes = [np.array(valid_data[valid_data.years == '2006-2010']['category']), 
                    np.array(valid_data[valid_data.years == '2010-2013']['category']), 
                    np.array(valid_data[valid_data.years == '2013-2016']['category'])]
                    
for i in MDIR_years_all_lakes:
    print Counter(i) # .most_common(3)
    
### OUTPUT    
### {'SE': 89, 'E': 41, 'S': 38, 'SW': 5, 'W': 1}
### {'S': 79, 'SW': 64, 'SE': 11}
### {'SE': 55, 'E': 54, 'S': 20, 'SW': 4, 'NE': 1, 'W': 1}

#%%    
# 4. Plot directions per timestep

    
labels = ['2006-2010', '2010-2013', '2013-2016']
x = np.arange(1, len(labels) + 1, 1)  # the label locations
width = 0.15

fig, ax = plt.subplots(figsize = (12,9))

# ALL lakes 
#data_SW = [5, 64, 4]
#data_S = [38, 79, 20]
#data_SE = [89, 11, 55]
#data_E = [41, 0, 54]

# VALIDATED lakes
data_SW = [1, 7, 0]
data_S = [4, 6, 1]
data_SE = [9, 1, 3]
data_E = [2, 0, 5]


rects1 = ax.bar(x - width/2 - width, data_SW, width, label = "SW", color = 'darkgreen')
rects2 = ax.bar(x - width/2, data_S, width, label = "S",  color = 'darkred')
rects3 = ax.bar(x + width/2, data_SE, width, label = "SE", color = 'darkorange')
rect42 = ax.bar(x + width/2 + width, data_E, width, label = "E", color = 'yellow')


# Add some text for labels, title and custom x-axis tick labels, etc.
x_text = 'magnitude'
y_text = 'time step'
title = 'Prevailing direction of shoreline movement per time step (validated lakes)'
ax.set_ylabel(x_text)
ax.set_xlabel(y_text)
ax.set_title(title)


ax.set_xticks(x)
ax.set_xticklabels(labels)
plt.rcParams.update({'font.size': 15})
#autolabel(rects1)
ax.legend()

plt.savefig(figf_out + str(today.year) + str(today.month) + str(today.day) + '_' + title.replace(' ', '_') + '.pdf')


#%%    
# 4. Plot directions per size category

# OUTPUT new classes (all lakes)
#Counter({'SE': 73, 'S': 62, 'E': 36, 'SW': 26})
#Counter({'SE': 52, 'E': 42, 'S': 42, 'SW': 29, 'W': 2, 'NE': 1})
#Counter({'S': 18, 'SE': 13, 'E': 12, 'SW': 10})
#Counter({'S': 9, 'E': 3, 'SE': 3, 'SW': 1})
#Counter({'SE': 14, 'SW': 7, 'S': 6, 'E': 2})

# OUTPUT new classes (validated lakes)
#Counter({'S': 5, 'E': 3, 'SW': 2, 'SE': 2})
#Counter({'SW': 4, 'SE': 3, 'E': 2, 'S': 1})
#Counter({'E': 1, 'SW': 1})
#Counter({'S': 2, 'E': 1, 'SE': 1})
#Counter({'SE': 7, 'S': 3, 'SW': 1})

# OUTPUT old classes
#Counter({'SE': 111, 'S': 98, 'E': 71, 'SW': 50, 'W': 2, 'NE': 1})
#Counter({'S': 31, 'SE': 29, 'E': 20, 'SW': 15})
#Counter({'SE': 4, 'S': 3, 'SW': 2, 'E': 2})
#Counter({'SE': 11, 'SW': 6, 'S': 5, 'E': 2})

#%%

   
labels = ['< 0.36', '0.36 - 1.44', '1.44 - 5.76', '5.76 - 23.04', '> 23.04']
#labels = ['< 0.1 - 1.0', '1.0 - 10.0', '10.0 - 40.0', '> 40.0']

x = np.arange(1, len(labels) + 1, 1)  # the label locations
width = 0.15

fig, ax = plt.subplots(figsize = (12,9))
 
## old classes 
#data_SW = [50, 15, 2, 6]
#data_S = [98, 31, 3, 5]
#data_SE = [111, 29, 4, 11]
#data_E = [71, 20, 2, 2]

## new classes (all lakes)
#data_SW = [26, 29, 10, 1, 7]
#data_S = [62, 42, 18, 9, 6]
#data_SE = [73, 52, 13, 3, 14]
#data_E = [36, 42, 12, 3, 2]

## new classes (validated lakes)
data_SW = [2, 4, 1, 0, 1]
data_S = [5, 1, 0, 2, 3]
data_SE = [2, 3, 0, 1, 7]
data_E = [3, 2, 1, 1, 0]

rects1 = ax.bar(x - width/2 - width, data_SW, width, label = "SW", color = 'darkgreen')
rects2 = ax.bar(x - width/2, data_S, width, label = "S",  color = 'darkred')
rects3 = ax.bar(x + width/2, data_SE, width, label = "SE", color = 'darkorange')
rect42 = ax.bar(x + width/2 + width, data_E, width, label = "E", color = 'yellow')


# Add some text for labels, title and custom x-axis tick labels, etc.
x_text = 'number of lakes'
y_text = 'lake sizes'
title = 'Prevailing direction of shoreline movement per lake size (validated lakes new classes)'
ax.set_ylabel(x_text)
ax.set_xlabel(y_text)
ax.set_title(title)


ax.set_xticks(x)
ax.set_xticklabels(labels)
plt.rcParams.update({'font.size': 15})
#autolabel(rects1)
ax.legend()

plt.savefig(figf_out + str(today.year) + str(today.month) + str(today.day) + '_' + title.replace(' ', '_') + '.pdf')


