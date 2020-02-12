import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


file_in = '/home/skaiser/permamount/staff/soraya_kaiser/git2/2_plots/median5/gdf_ts1_lake483.csv'
df = pd.read_csv(file_in)

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

df.head()
direction

#ax = df.plot.bar(x = 'category', y = 'distance')
plt.bar(df.category, df.distance)


