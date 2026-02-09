# -*- coding: utf-8 -*-
"""

This script creates reef connectivity network plots

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

connect = pd.read_csv('Moore_2015_d1transfer_probability_matrix_wide_3d.csv', header = None, skiprows=3)  # read connectivity matrix
coord = gpd.read_file('MooreCluster_SpatialPolygons.gpkg') # read spatial data 
coord['centroid'] = coord.centroid
coord['Lon'] = coord.centroid.x
coord['Lat'] = coord.centroid.y
lat = coord.Lat
lon = coord.Lon

connect_mat = []
points = []
for i in range(0, len(lat)):  # loop through reef sites' coordinates
    points.append([lon[i],lat[i]])
    connect_index = np.where(connect.iloc[i+1,1:len(lat)+1].astype(float) != 0.0)  # find index of connections (i.e., nonzero values)
    if (np.size(connect_index) != 0):
        for k in range(len(connect_index[0])): # loop through the index of connections
            connect_mat.append((i,connect_index[0][k]))
            prob_str.append(connect.iloc[i+1,connect_index[0][k]+1]) # get the probabilities of connections

#create the graph
graph = nx.Graph()

#add nodes/connections to the graph
for node in range(len(points)):
    graph.add_node(node)
graph.add_edges_from(connect_mat)

fig, ax = plt.subplots()
nx.draw_networkx_nodes(graph,[(x,y) for x,y in points], node_color = 'grey', node_size=10, ax = ax) # draw nodes
arcs = nx.draw_networkx_edges(graph, [(x,y) for x,y in points], edge_color = 'red', node_size=10, ax = ax, alpha = 0.5)  # draw edges
   
plt.axis("on")
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
fig.savefig("connectivity_network_2015_1.png",bbox_inches='tight')
plt.show()
