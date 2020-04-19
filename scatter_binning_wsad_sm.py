# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 15:20:30 2020

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

#title = 'Annual Shoreline Movement vs Water Surface Differences (sm_correct=y)'
title = 'Annual Shoreline Movement vs Water Surface Differences (sm_correct=n)'


#%% Get overview

valid = valid_data[valid_data.validation == 'y']
#sm_correct = valid_data[valid_data.sm_correct == 'y']
#wb_exact = valid_data[valid_data.wb_exact == 'y']

sm_correct = valid_data[valid_data.sm_correct == 'n']
wb_exact = valid_data[valid_data.wb_exact == 'n']

print len(valid), len(sm_correct), len(wb_exact)

#%% Look at flagged data

flag_sub = valid

#%% A - FIXED Scatter Plot for all timesteps in CLASSES

classes = range(1,5)
#types_s = [np.array(merged[merged.klasse == 1]['id_right']), np.array(merged[merged.klasse == 2]['id_right']), np.array(merged[merged.klasse == 3]['id_right']), np.array(merged[merged.klasse == 4]['id_right'])]
colors = ['#1b9e77','#d95f02','#7570b3','#e7298a']
#x_s = [np.array(sm_correct[sm_correct.klasse == 1]['diff']), np.array(sm_correct[sm_correct.klasse == 2]['diff']), np.array(sm_correct[sm_correct.klasse == 3]['diff']), np.array(sm_correct[sm_correct.klasse == 4]['diff'])]
y_s = [np.array(sm_correct[sm_correct.klasse == 1]['mv_annual']), np.array(sm_correct[sm_correct.klasse == 2]['mv_annual']), np.array(sm_correct[sm_correct.klasse == 3]['mv_annual']), np.array(sm_correct[sm_correct.klasse == 4]['mv_annual'])]
x_s = [np.array(sm_correct[sm_correct.klasse == 1]['diff']), np.array(sm_correct[sm_correct.klasse == 2]['diff']), np.array(sm_correct[sm_correct.klasse == 3]['diff']), np.array(sm_correct[sm_correct.klasse == 4]['diff'])]

#%% B - FIXED Scatter Plot for all timesteps in CLASSES

fig = plt.figure(figsize = (12, 12))
ax = fig.add_subplot(111)

for j in range(len(classes)):
    x_val = x_s[j]/ float(10000) 
    y_val = y_s[j]
#    types = types_s[j]
    color = colors[j]    
    #label = labels[j]
    klasse = str(classes[j])

    ax.scatter(x_val, y_val, marker='x', color = color, label=klasse)   # , alpha=0.5
#    for i,type in enumerate(types):                         # uncomment these lines to turn off labeling
#        x = x_val[i]                                        #
#        y = y_val[i]                                        #
#        plt.text(x+0.02, y+0.02, type, fontsize=6)            #
plt.title(title)
plt.xlabel('Water Surface Area Difference[ha]')
plt.ylabel('Shoreline Movement [m]')
plt.yscale('log')
plt.xscale('symlog')
#plt.xlim(x_min -1, x_max +1)
#plt.ylim(0, y_max +1)


#plt.axhline(y_max,linewidth=1, color='k', linestyle = '--')
#plt.axvline(x_min,linewidth=1, color='k', linestyle = '--')
#plt.axvline(x_max,linewidth=1, color='k', linestyle = '--')
plt.legend(loc = 'upper right')
#plt.show()
plt.savefig(figf_out + "%s_%s.pdf" % (str(today.year) + str(today.month) + str(today.day), title.replace(' ', '_')), dpi=300, orientation='landscape', format='pdf')

#%% A - FIXED Scatter Plot for all timesteps in YES/NO

title = 'Annual Shoreline Movement vs Water Surface Differences yes-no'


classes = ['yes', 'no']
types_s = [np.array(valid_data[valid_data.sm_correct == 'y']['lake']), np.array(valid_data[valid_data.sm_correct == 'n']['lake'])]
colors = ['#1b9e77','#d95f02','#7570b3','#e7298a']
#x_s = [np.array(sm_correct[sm_correct.klasse == 1]['diff']), np.array(sm_correct[sm_correct.klasse == 2]['diff']), np.array(sm_correct[sm_correct.klasse == 3]['diff']), np.array(sm_correct[sm_correct.klasse == 4]['diff'])]
y_s = [np.array(valid_data[valid_data.sm_correct == 'y']['mv_annual']), np.array(valid_data[valid_data.sm_correct == 'n']['mv_annual'])]
x_s = [np.array(valid_data[valid_data.sm_correct == 'y']['diff']), np.array(valid_data[valid_data.sm_correct == 'n']['diff'])]

#%% B - FIXED Scatter Plot for all timesteps in CLASSES

fig = plt.figure(figsize = (12, 12))
ax = fig.add_subplot(111)

for j in range(len(classes)):
    x_val = x_s[j]/ float(10000) 
    y_val = y_s[j]
#    types = types_s[j]
    color = colors[j]    
    #label = labels[j]
    klasse = str(classes[j])

    ax.scatter(x_val, y_val, marker='x', color = color, label=klasse)   # , alpha=0.5
#    for i,type in enumerate(types):                         # uncomment these lines to turn off labeling
#        x = x_val[i]                                        #
#        y = y_val[i]                                        #
#        plt.text(x+0.02, y+0.02, type, fontsize=6)            #
plt.title(title)
plt.xlabel('Water Surface Area Difference[ha]')
plt.ylabel('Shoreline Movement [m]')
plt.yscale('log')
plt.xscale('symlog')
#plt.xlim(x_min -1, x_max +1)
#plt.ylim(0, y_max +1)


#plt.axhline(y_max,linewidth=1, color='k', linestyle = '--')
#plt.axvline(x_min,linewidth=1, color='k', linestyle = '--')
#plt.axvline(x_max,linewidth=1, color='k', linestyle = '--')
plt.legend(loc = 'upper right')
#plt.show()
plt.savefig(figf_out + "%s_%s.pdf" % (str(today.year) + str(today.month) + str(today.day), title.replace(' ', '_')), dpi=300, orientation='landscape', format='pdf')

