# -*- coding: utf-8 -*-
"""

This script creates source and sink plots

@author: Chinenye Ani, AIMS
"""

import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd


num_release = 61 # number of particles released at a reef site
total_release = 20374 # total number of particles released in the cluster domain
connect = pd.read_csv('/outputs/Moore_2015_d1transfer_probability_matrix_wide_3d.csv', header = None, skiprows=4)
coord = gpd.read_file(spatial_data)
source = connect.sum(axis=1,numeric_only=True)
fig1, ax1 = plt.subplots()
fig1.set_size_inches(17.5, 8.5)
coord.plot(source, ax = ax1, legend = True, cmap= 'viridis_r', vmin= 0.0, legend_kwds = {'shrink': 0.5})
ax1.set_xlabel("Longitude", fontsize = 18)
ax1.set_ylabel("Latitude", fontsize = 18)
ax1.figure.axes[1].tick_params(labelsize=18)
ax1.figure.axes[0].tick_params(labelsize=18)
ax1.figure.axes[1].set_title("           Proportion settled",fontsize=18)     
fig1.savefig('/outputs/Moore_source_2015_1_3d.png',bbox_inches='tight')

#sum the probalities of all sink sites and find the proportion of the total released larvae that settle on a reef site
sink = connect.sum(axis=0,numeric_only=True) * 1000 * num_release / total_release  
sink.index = sink.index-1 
fig2, ax2= plt.subplots()
fig2.set_size_inches(17.5, 8.5)
coord.plot(sink, ax = ax2, legend = True, cmap = 'viridis_r', vmin= 0.0, legend_kwds = {'shrink': 0.5})
ax2.set_xlabel("Longitude", fontsize = 18)
ax2.set_ylabel("Latitude", fontsize = 18)
ax2.figure.axes[1].tick_params(labelsize=18)
ax2.figure.axes[0].tick_params(labelsize=18)
ax2.figure.axes[1].set_title("         Sum of settling" + "\n" + "          fractions (10$^{-3}$)",fontsize=18)    
fig2.savefig('/outputs/Moore_sink_2015_1_3d.png',bbox_inches='tight')
