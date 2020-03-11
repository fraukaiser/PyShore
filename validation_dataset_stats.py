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

valid_data = pd.read_csv('/home/skaiser/Desktop/scatter/20200311_valid_data_mod.csv')
#%%

for row in valid_data:
    wb_valid_count = 0
    sm_valid_count = 0
    data_count = 0
    
    sm_correct = valid_data['sm correct']
    wb_exact = valid_data['wb exact']
    valid = valid_data['validation']
    
    for i in valid:
        if i == 'y':
            data_count += 1    
    
    for i in sm_correct:
        if i == 'y':
            sm_valid_count += 1
            
    for i in wb_exact:
        if i == 'y':
            wb_valid_count += 1
   
print wb_valid_count, sm_valid_count, data_count
    
    
