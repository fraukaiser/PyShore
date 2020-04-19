# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 16:15:59 2020

@author: skaiser
"""
import numpy as np
from matplotlib import pyplot as plt

def percent(w, G):
    array = []
    for i, j in zip(w, G):
        try:
            p = float(i)/ float(j) * 100
        except:
            p = np.nan
        array.append(p)
    return array

fig, ax = plt.subplots(figsize = (16,8))    
def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')
