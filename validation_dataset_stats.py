# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 11:57:03 2020

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
#%%
merged = pd.read_csv('/home/skaiser/Desktop/scatter/2020227_mean_diffs_data.csv')
flg_within = pd.read_csv('/home/skaiser/Desktop/scatter/20200303_stats_lakes_within_whiskers.csv')
flg_outside = pd.read_csv('/home/skaiser/Desktop/scatter/20200303_stats_lakes_outside_whiskers.csv')
#%%
merged = merged.drop(['Unnamed: 0', 'Unnamed: 0.1', 'id_right'], axis = 1)
flagged = pd.concat([flg_within, flg_outside])
flagged = flagged.drop(['Unnamed: 7'], axis = 1)

valid_data = merged.merge(flagged, on = 'lake')
valid_data.to_csv(figf_out + str(today.year) + str(today.month) + str(today.day) + '_valid_data.csv')
#%% START HERE

valid_data = pd.read_csv('/home/skaiser/Desktop/scatter/20200311_valid_data_mod_colored.csv')
#%%

for row in valid_data:
    wb_valid_count = 0
    sm_valid_count = 0
    data_count = 0
    both_count = 0
    
    sm_correct = valid_data['sm_correct']
    wb_exact = valid_data['wb_exact']
    valid = valid_data['validation']
    
    for i in valid:
        if i == 'y':
            data_count += 1    
    
    for i in sm_correct:
        if i == 'y':
            sm_valid_count += 1
        elif i == 'n':
            both_count += 1
            
    for i in wb_exact:
        if i == 'y':
            wb_valid_count += 1
        elif i == 'n':
            both_count += 1
            
print wb_valid_count, sm_valid_count, data_count, both_count
    
#%% Look at flagged data
flag_sub = valid_data[(valid_data)['validation'] == 'y']


#%% X and Y values for WB_EXACT
x_s = [np.array(valid_data[valid_data.wb_exact == 'y']['diff']), np.array(valid_data[valid_data.wb_exact == 'n']['diff'])]
y_s = [np.array(valid_data[valid_data.wb_exact == 'y']['mv']), np.array(valid_data[valid_data.wb_exact == 'n']['mv'])]
types_s = [np.array(valid_data[valid_data.wb_exact == 'y']['lake']), np.array(valid_data[valid_data.wb_exact == 'n']['lake'])]

#%% X and Y values for SM_CORRECT
x_s = [np.array(valid_data[valid_data.sm_correct == 'y']['diff']), np.array(valid_data[valid_data.sm_correct == 'n']['diff'])]
y_s = [np.array(valid_data[valid_data.sm_correct == 'y']['mv']), np.array(valid_data[valid_data.sm_correct == 'n']['mv'])]
types_s = [np.array(valid_data[valid_data.sm_correct == 'y']['lake']), np.array(valid_data[valid_data.sm_correct == 'n']['lake'])]

#%% scatter results
colors = ['#1b9e77','#d95f02','#7570b3','#e7298a']
classes = ['yes (%s)' % str(len(x_s[0])), 'no (%s)' % str(len(x_s[1]))]

#%% B - FIXED Scatter Plot for validated data 

fig = plt.figure(figsize = (8, 8))
ax = fig.add_subplot(111)
title = 'Shoreline Movement Correct, zoomed' # zoomed min max, zoomed
#title = 'Waterbody Derivation exact zoomed, labeled'

for j in range(0,2):
    x_val = x_s[j]/ float(10000) 
    y_val = y_s[j]
    types = types_s[j]
    color = colors[j]    
    klasse = str(classes[j])

    ax.scatter(x_val, y_val, marker='.', color = color, label=klasse, alpha=0.5)
    for i,type in enumerate(types):                         # uncomment these lines to turn off labeling
        x = x_val[i]                                        #
        y = y_val[i]                                        #
        plt.text(x+0.02, y+0.02, type, fontsize=6)          #
plt.title(title)
plt.xlabel('Area Change [ha]')
plt.ylabel('Shoreline Movement [m]')
plt.xlim(-10, 10)
plt.ylim(0, 70)

plt.legend(loc = 'upper left')
#plt.show()
plt.savefig(figf_out + "%s_%s.pdf" % (str(today.year) + str(today.month) + str(today.day), title.replace(' ', '_')), dpi=300, orientation='landscape', format='pdf')


#%% FIXED Binning min max

minimum = np.min(flag_sub['mv_annual'])
maximum = np.max(flag_sub['mv_annual'])
#%% FIXED extract mv_annual data

#data = np.array(flag_sub['mv_annual'])
data = [float(i)/10000 for i in np.array(flag_sub['diff'])]


#%%
plt.subplot(211)
hist, bins, _ = plt.hist(data, bins=10)
# histogram on log scale. 
# Use non-equal bin sizes, such that they look equal on log scale.
logbins = np.logspace(np.log2(bins[0]),np.log2(bins[-1]+1),len(bins))
plt.subplot(212)
plt.hist(data, bins=logbins)
plt.xscale('log')
plt.show()


#%% 

hist_log_data = plt.hist(data, color='darkred', rwidth=1.5, bins=logbins)
plt.xscale('log')

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

#%% FIXED Now extract only valid data
yes_wb = [float(i)/10000 for i in np.array(valid_data[valid_data.wb_exact == 'y']['diff'])]
no_wb = [float(i)/10000 for i in np.array(valid_data[valid_data.wb_exact == 'n']['diff'])]

yes_sm = [float(i)/10000 for i in np.array(valid_data[valid_data.sm_correct == 'y']['diff'])]
no_sm = [float(i)/10000 for i in np.array(valid_data[valid_data.sm_correct == 'n']['diff'])]
#%% FIXED Now extract only valid data
yes_wb = np.array(valid_data[valid_data.wb_exact == 'y']['mv_annual'])
no_wb = np.array(valid_data[valid_data.wb_exact == 'n']['mv_annual'])

yes_sm = np.array(valid_data[valid_data.sm_correct == 'y']['mv_annual'])
no_sm = np.array(valid_data[valid_data.sm_correct == 'n']['mv_annual'])

#%%

y = np.array(flag_sub[(flag_sub.wb_exact == 'y') & (flag_sub.klasse == 1)]['mv_annual'])
#%% FIXED hist data
hist_yes_data = plt.hist(yes_wb, color='darkred', rwidth=1.5, bins=log_bins)
hist_no_data = plt.hist(no_wb, color='darkred', rwidth=1.5, bins=log_bins)

hist_yes_sm_data = plt.hist(yes_sm, color='darkred', rwidth=1.5, bins=log_bins)
hist_no_sm_data = plt.hist(no_sm, color='darkred', rwidth=1.5, bins=log_bins)

df['yes_wb_frequency'] = hist_yes_data[0]
df['no_wb_frequency'] = hist_no_data[0]

df['yes_sm_frequency'] = hist_yes_sm_data[0]
df['no_sm_frequency'] = hist_no_sm_data[0]

#%% FIXED Percentage, too wb_exact


yes_percent = []
no_percent = []
yes = np.array(df.yes_wb_frequency)
no = np.array(df.no_wb_frequency)

whole = np.array(df.log_frequency)
count = 0
for y in yes:
    print count
    z = y*100/whole[count]    
    yes_percent.append(z)
    count += 1
count = 0
for y in no:
    print count
    z = y*100/whole[count]    
    no_percent.append(z)
    count += 1
        
df['yes_wb_percent'] = yes_percent
df['no_wb_percent'] = no_percent


#%% FIXED Percentage, too sm_correct


yes_sm_percent = []
no_sm_percent = []
yes = np.array(df.yes_sm_frequency)
no = np.array(df.no_sm_frequency)

whole = np.array(df.log_frequency)
count = 0
for y in yes:
    print count
    z = y*100/whole[count]    
    yes_sm_percent.append(z)
    count += 1
count = 0
for y in no:
    print count
    z = y*100/whole[count]    
    no_sm_percent.append(z)
    count += 1
        
df['yes_sm_percent'] = yes_sm_percent
df['no_sm_percent'] = no_sm_percent

df.to_csv(figf_out + str(today.year) + str(today.month) + str(today.day) + '_lin_log_hist.csv')

#%% FIXED show linear and logarithmic histogram for whole dataset, yes only and no only
#nr_bins = 20
#
#fig = plt.figure(figsize = (8, 16))
# 
#plt.subplot(611)
#hist, bins, _ = plt.hist(data, color='darkred', rwidth=1.5, bins=nr_bins)
#logbins = np.logspace(np.log10(bins[0]),np.log10(bins[-1]),len(bins))
#plt.subplot(612)
#hist_log_data = plt.hist(data, color='darkred', rwidth=1.5, bins=logbins)
#plt.xscale('log')
## histogram on log scale. 
## Use non-equal bin sizes, such that they look equal on log scale.
#plt.subplot(613) 
#hist_yes_data = plt.hist(yes_wb, color='darkred', rwidth=1.5, bins=bins)
#plt.subplot(614)
#hist_yes_data = plt.hist(yes_wb, color='darkred', rwidth=1.5, bins=logbins)
#plt.xscale('log')
#
#
#plt.subplot(615)
#hist_no_data = plt.hist(no_wb, color='darkred', rwidth=1.5, bins=bins)
#plt.subplot(616)
#hist_no_data = plt.hist(no_wb, color='darkred', rwidth=1.5, bins=logbins)
#plt.xscale('log')
#plt.show()

#%% DO WATER SURFACE AREA HERE FIXED Stack it now LOG wb_exact
labels = [np.around(i, 2) for i in np.array(df.logbins)]
#labels = [np.around(i, 2) for i in np.array(log_bins)]

men_means = [np.around(i) for i in np.array(df.yes_wb_percent)]
women_means = [np.around(i) for i in np.array(df.no_wb_percent)]

x = np.arange(len(labels))  # the label locations
width = 0.40  # the width of the bars

fig, ax = plt.subplots(figsize = (16,8))
rects1 = ax.bar(x - width/2, men_means, width, label='Yes')
rects2 = ax.bar(x + width/2, women_means, width, label='No')

title = 'Logarithmic binning of identified waterbodies'
# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('%')
ax.set_xlabel('Annual shoreline movement [m]')
ax.set_title(title)
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

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
autolabel(rects2)

#%% FIXED Stack it now LOG sm_correct
labels = [np.around(i, 2) for i in np.array(df.bins)]
men_means = [np.around(i) for i in np.array(df.yes_sm_percent)]
women_means = [np.around(i) for i in np.array(df.no_sm_percent)]

x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots(figsize = (16,8))
rects1 = ax.bar(x - width/2, men_means, width, label='Yes', color = 'darkgreen')
rects2 = ax.bar(x + width/2, women_means, width, label='No', color = 'darkred')

title = 'Logarithmic binning of identified waterbodies'
# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('%')
ax.set_xlabel('Water Surface Area Change [ha]')
ax.set_title(title)
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

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
autolabel(rects2)