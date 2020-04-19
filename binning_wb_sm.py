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
#%%
path_in = '/home/skaiser/permamount/staff/soraya_kaiser/git2/2_plots/median5'
figf_out = '/home/skaiser/permamount/staff/soraya_kaiser/git2/2_plots/'
today = datetime.date.today()

#valid_data = pd.read_csv('/home/skaiser/Desktop/scatter/20200311_valid_data_mod_colored.csv')
valid_data = pd.read_csv('/home/skaiser/permamount/staff/soraya_kaiser/git2/2_plots/20200417_valid_data_mod_no_duplicates.csv')
#valid_data = pd.read_csv('/home/skaiser/permamount/staff/soraya_kaiser/git2/2_plots/2020414_check_valid_data_again_no_duplicates.csv')
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
 1.1,
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
#ax.set_title('Cumulative histogram of ' + x_text)
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

yes_data = [np.around(i) for i in percent(plt.hist(yes_sm, bins = nr_bins)[0], plt.hist(all_wb, bins = nr_bins)[0])]
no_data = [np.around(i) for i in percent(plt.hist(no_sm, bins = nr_bins)[0], plt.hist(all_wb, bins = nr_bins)[0])]

x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots(figsize = (8,8))
rects1 = ax.bar(x - width/2, yes_data, width, label='Yes', color = 'darkgreen')
rects2 = ax.bar(x + width/2, no_data, width, label='No', color = 'darkred')

ax.set_ylabel('%')
ax.set_xlabel('Lake Size [ha]')
title = 'Quality of Shoreline Derivation per Lake Size Category (sm_correct)'
ax.set_title(title)
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

autolabel(rects1)
autolabel(rects2)

plt.savefig(figf_out + str(today.year) + str(today.month) + str(today.day) + '_' + title.replace(' ', '_') +'.pdf')


#%% what about the old sizes? for WB
nr_bins = len(np.unique(valid_data.klasse))
#labels = np.arange(1, 5, 1)
labels = ['< 0.1 - 1.0', '1.0 - 10.0', '10.0 - 40.0', '> 40.0']
yes_wb = np.array(valid_data[valid_data.wb_exact == 'y']['klasse'])
no_wb = np.array(valid_data[valid_data.wb_exact == 'n']['klasse'])
all_wb = np.array(valid_data[valid_data.validation == 'y']['klasse'])

yes_data = [np.around(i) for i in percent(plt.hist(yes_wb, bins = nr_bins)[0], plt.hist(all_wb, bins = nr_bins)[0])]
no_data = [np.around(i) for i in percent(plt.hist(no_wb, bins = nr_bins)[0], plt.hist(all_wb, bins = nr_bins)[0])]
x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots(figsize = (8,8))
rects1 = ax.bar(x - width/2, yes_data, width, label='Yes', color = 'darkgreen')
rects2 = ax.bar(x + width/2, no_data, width, label='No', color = 'darkred')

ax.set_ylabel('%')
ax.set_xlabel('Lake Size [ha]')
title = 'Quality of Shoreline Derivation per Lake Size Category (wb_exact)'
ax.set_title(title)
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

autolabel(rects1)
autolabel(rects2)

plt.savefig(figf_out + str(today.year) + str(today.month) + str(today.day) + '_' + title.replace(' ', '_') +'old_classes.pdf')


#%% what about the old sizes? for SM
nr_bins = len(np.unique(valid_data.klasse))
#labels = np.arange(1, 5, 1)
labels = ['< 0.1 - 1.0', '1.0 - 10.0', '10.0 - 40.0', '> 40.0']
yes_sm = np.array(valid_data[valid_data.sm_correct == 'y']['klasse'])
no_sm = np.array(valid_data[valid_data.sm_correct == 'n']['klasse'])
all_wb = np.array(valid_data[valid_data.validation == 'y']['klasse'])

yes_data = [np.around(i) for i in percent(plt.hist(yes_sm, bins = nr_bins)[0], plt.hist(all_wb, bins = nr_bins)[0])]
no_data = [np.around(i) for i in percent(plt.hist(no_sm, bins = nr_bins)[0], plt.hist(all_wb, bins = nr_bins)[0])]
x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots(figsize = (8,8))
rects1 = ax.bar(x - width/2, yes_data, width, label='Yes', color = 'darkgreen')
rects2 = ax.bar(x + width/2, no_data, width, label='No', color = 'darkred')

ax.set_ylabel('%')
ax.set_xlabel('Lake Size [ha]')
title = 'Quality of Shoreline Derivation per Lake Size Category (sm_correct)'
ax.set_title(title)
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

autolabel(rects1)
autolabel(rects2)

plt.savefig(figf_out + str(today.year) + str(today.month) + str(today.day) + '_' + title.replace(' ', '_') +'old_classes.pdf')
#%%
flag_sub = valid_data[(valid_data)['validation'] == 'y']
flag_sub.to_csv(figf_out + str(today.year) + str(today.month) + str(today.day) + 'check_valid_data_again.csv')

#%% Plot SM histogram for the whole dataset
labels = [np.around(i, 2) for i in np.array(df.logbins)]
#data = [int(i) for i in np.array(df.log_frequency)] # plots total number of whole dataset for each bin
data = [int(i) for i in np.cumsum(np.array(df.log_frequency))] # plots cum total number of whole dataset for each bin

#data = [percent(i, 463) for i in np.array(df.log_frequency)] # plots percentage of whole dataset for each bin
#data = [percent(i, 463) for i in np.cumsum(np.array(df.log_frequency))] # plots cum percentage of whole dataset for each bin

x = np.arange(len(labels))  # the label locations
width = 0.5  # the width of the bars

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

plt.savefig(figf_out + str(today.year) + str(today.month) + str(today.day) + '_' + '_Binning of_' + x_text.replace(' ', '_') +'_all_lakes_cumnumber.pdf')
