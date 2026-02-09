# -*- coding: utf-8 -*-
"""

This script produces a csv file of the transfer probability matrix from simulated particle trajectories of a reef cluster with daily larval mortality considered.

Particle tracking ceased after the first settlement.

To run the script use the Syntax: python connectivity_matrix_with_mortality.py [Cluster] [Year of release] [Day of release] [Cluster spatial data]

@author: Chinenye Ani, AIMS
"""

import xarray as xr
import numpy as np
import pandas as pd
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import argparse
import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd

parser = argparse.ArgumentParser()
parser.add_argument('cluster', type=str, help="Cluster")
parser.add_argument('year', type=str, help="Year_of_release")
parser.add_argument('day', type=str, help="Day_of_release")
parser.add_argument('spatial_data', type=str, help="Cluster_spatial_data")

args = parser.parse_args()

num_release = 181  # number of particles released at a reef site
min_index = 384 # index of minimum competency time (4 days)
max_index = 2688 # index of maximum competency time (28 days)
last_index = 12 # index of the final realease time (3 hours)
mort_rate = 0.4   # daily mortality rate
num_obs = 96  # number of observations (time steps) in 1 day

# read particle tracks from file
data_path = '/export/scratch/cani/RRAP/Oceanparcels/'
data_path1 = '/export/scratch/cani/RRAP/Oceanparcels/' + args.cluster + '/outputs/' + args.year + '/'
data_xarray = xr.open_dataset(data_path1 + args.cluster + '_trajectory_' + args.year + '_d' + args.day + '_3d.zarr', engine = 'zarr')
time = data_xarray['time'].values
lon = data_xarray['lon'].values
lat = data_xarray['lat'].values

# read reef sites' coordinates and polygons
coord = gpd.read_file(data_path + args.cluster +'/' + args.spatial_data)

t = (time - time[0,0]) / 3.6e12    # convert time in nanoseconds to hours
connect_matrix = np.zeros([len(coord),len(coord)])
settle_array = np.zeros(len(lat))
competency = [x for x in range(min_index,max_index + 1)] # indices of competency period
random.seed(200)

for j in range(last_index, max_index + 1):  #loop through the dispersal period
    # remove particles after the last set of particles are released (i.e, 3 hours after the initial release) 
    if (j == last_index): 
        n = np.size(t[:,j]) 
        mort = random.sample(range(n), int(np.round(mort_rate * n * j / num_obs))) # indices of particles that are removed immediately after all particles have been released
        remaining_index = [x for x in range(n) if x not in mort] # indices of remaining particles after the removal of particles
    elif (j > last_index): # remove particles every 15 mins (output time step) during the dispersal period
        num_mort = int(np.round(mort_rate * len(remaining_index) / num_obs))  # number of particles to be removed every 15 mins
        num_alive = len(remaining_index) - num_mort  # number of particles that are left after removing some particles 
        alive = set(random.sample(remaining_index, num_alive))  # indices of remaining particles after the removal of particles
        alive = [y for y in remaining_index if y in alive]  # you need this to restore the order
        remaining_index = alive
    if (j in competency):
        for i in remaining_index:  # loop through the remaining particles
            if ((settle_array[i] == 0) & (np.isnan(lon[i,j]) == False)): # check if the particle had previously settled on a reef site
                pt = Point(lon[i,j],lat[i,j])
                for k in range(0,len(coord)): # loop through the site polygons
                    if (pt.within(coord.geometry[k]) == True):  # check if the particle is over a spatial polygon
                        connect_matrix[i%len(coord),k] += 1
                        settle_array[i] += 1
                        break

connect_matrix_prop = connect_matrix / num_particles   #calculate transfer probability matrix
c_matrix = pd.DataFrame(connect_matrix_prop) 
c_matrix.columns = coord.reef_siteid
c_matrix.index = coord.reef_siteid.rename()
f = open(data_path1 + args.cluster + '_' + args.year + '_d' + args.day  + 'transfer_probability_matrix_wide_3d.csv', mode='a')
f.write('# Transfer probability matrix generated for ' + args.cluster + ' on day '+ args.day +' of spawning in ' + args.year + '.\n')
f.write('# Row names indicate the SOURCE site_id. Column names indicate the RECEIVING site_id.\n')
f.write('# Refer to the associated cross-reference table for reef locations.\n')
f.close()
c_matrix.to_csv(data_path1 + args.cluster + '_' + args.year + '_d' + args.day  + 'transfer_probability_matrix_wide_3d.csv', mode='a')
