# -*- coding: utf-8 -*-
"""

This script creates consistent source and sink plots

@author: Chinenye Ani, AIMS
"""

import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
from glob import glob
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset


files = sorted(glob('outputs/Mortality_40/'Moore_*transfer_probability_matrix_wide_3d.csv'))
coord = gpd.read_file(spatial_data)
connect, sink, source = {}, {}, {}
sink_all = pd.Series(0, index=range(len(coord)))
source_all = pd.Series(0, index=range(len(coord)))
for i in range(len(files)):
    connect[i]= pd.read_csv(files[i], header = None, skiprows=4)
    sink[i] = connect[i].sum(axis=0,numeric_only=True) #sum the probalities of all sink sites
    sink[i].index = sink[i].index-1
    source[i] = connect[i].sum(axis=1,numeric_only=True)  #sum the probalities of all source sites
    for j in range(len(coord)):
        if (sink[i][j] > 0.0):
            sink_all[j] += 1.0
        if (source[i][j]> 0.0):
            source_all[j] += 1.0

fig1, ax1 = plt.subplots()
fig1.set_size_inches(15.5, 8.5)
axins1 = zoomed_inset_axes(ax1, 2, loc= 'center right')
minx,maxx,miny,maxy = 146.28, 146.31,-16.925,-16.910
axins1.set_xlim(minx, maxx)
axins1.set_ylim(miny, maxy)
mark_inset(ax1, axins1, loc1=3, loc2=4, fc="none", ec="0.5")
coord.plot(source_all, ax = ax1, legend = True, cmap='viridis_r', legend_kwds = {'shrink': 0.5}, edgecolor='black', linewidth =0.45)
coord.plot(source_all, ax= axins1, legend = False, cmap= 'viridis_r', edgecolor='black', linewidth =0.45)
plt.setp(axins1.get_xticklabels(), visible=False)
plt.setp(axins1.get_yticklabels(), visible=False)
ax1.set_xlabel("Longitude", fontsize = 18)
ax1.set_ylabel("Latitude", fontsize = 18)
ax1.tick_params(labelsize=18)
ax1.figure.axes[2].set_title("                   Number of spawning" + "\n" + "     nights" + "\n", fontsize=18)
ax1.figure.axes[2].tick_params(labelsize=18)
fig1.savefig('outputs/Mortality_40/' + cluster + '_union_source_' + dimension + 'd.png',bbox_inches='tight')

fig2, ax2 = plt.subplots()
fig2.set_size_inches(15.5, 8.5)
axins2 = zoomed_inset_axes(ax2, 2, loc= 'center right')
axins2.set_xlim(minx, maxx)
axins2.set_ylim(miny, maxy)
mark_inset(ax2, axins2, loc1=3, loc2=4, fc="none", ec="0.5")    
coord.plot(sink_all, ax = ax2, legend = True, cmap='viridis_r', legend_kwds = {'shrink': 0.5}, edgecolor='black', linewidth =0.45)
coord.plot(sink_all, ax= axins2, legend = False, cmap= 'viridis_r', edgecolor='black', linewidth =0.45)
plt.setp(axins2.get_xticklabels(), visible=False)
plt.setp(axins2.get_yticklabels(), visible=False)
ax2.set_xlabel("Longitude", fontsize = 18)
ax2.set_ylabel("Latitude", fontsize = 18)
ax2.tick_params(labelsize=18)
ax2.figure.axes[2].set_title("                   Number of spawning" + "\n" + "     nights" + "\n", fontsize=18)
ax2.figure.axes[2].tick_params(labelsize=18)
fig2.savefig('outputs/Mortality_40/' + cluster + '_union_sink_' + dimension + 'd.png',bbox_inches='tight')
