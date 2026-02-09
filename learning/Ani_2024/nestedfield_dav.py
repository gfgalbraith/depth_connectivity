# -- coding utf-8 --
"""

This script simulates the trajectories of particles released every 3 minutes from 8:00pm to 11:00pm in 2D (depth-averaged velocities) within a reef cluster domain nested within the GBR1km grid.
Particle trajectories are simulated for 30 days and are output every 15 minutes.  

This code was based on example codes provided by OceanParcels on NestedFields. 

The latest Oceanparcels version was used for this simulation.

To run the script use the Syntax python nestedfield_dav.py [Cluster] [Year of release] [Day of release] [Cluster spatial data]

@author Chinenye Ani, AIMS 
"""

from parcels import Field, NestedField, FieldSet, ParticleSet, JITParticle, Variable, ParticleFile, StatusCode, AdvectionRK4
import numpy as np
import datetime
from datetime import datetime
import pandas as pd
from datetime import timedelta as delta
import netCDF4
from glob import glob
import argparse
import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
from shapely.geometry import Point
from warnings import simplefilter
# ignore all future warnings
simplefilter(action='ignore', category=FutureWarning)

parser = argparse.ArgumentParser()
parser.add_argument('cluster', type=str, help=cluster)  
parser.add_argument('year', type=str, help=year)
parser.add_argument('day', type=str, help=day)
parser.add_argument('spatial_data', type=str, help=spatial_data)
args = parser.parse_args()

num_release = 181      #total release time in minutes
int_release = 3        #time interval of particle release in minutes
num_particles = 61     #total number of released particles per site 
run_duration = 30      #duration of model run in days
out_dt = 0.25          #output timestep in hours
run_dt = 5             #run timestep in minutes
depth0 = -2.25         #depth at which particles are released

#create GBR1 fieldset
data_path = 'exportscratchcaniRRAPOceanparcels'
files = sorted(glob(args.cluster + 'velocity_data' + args.cluster + '_uv_' + args.year + '-.nc'))
filenames = {'U' {'lon' files[0], 'lat' files[0], 'depth' files[0], 'data' files},
             'V' {'lon' files[0], 'lat' files[0], 'depth' files[0], 'data' files}}
variables = {'U' 'u',
             'V' 'v'}
dimensions = {'U' {'lon' 'longitude', 'lat' 'latitude', 'depth' 'zc', 'time' 'time'},
              'V' {'lon' 'longitude', 'lat' 'latitude', 'depth' 'zc', 'time' 'time'}}
fieldset = FieldSet.from_netcdf(filenames, variables, dimensions, chunksize = 'auto', allow_time_extrapolation = True)

#create RECOM fieldset
data = args.cluster + '' + args.cluster + '_' + args.year +'_simple.nc'
dimensionsU={'lon''longitude', 'lat''latitude', 'depth' 'zc', 'time''time'}
dimensionsV={'lon''longitude', 'lat''latitude', 'depth' 'zc', 'time''time'}
U_recom=Field.from_netcdf(data, ('U_recom','uav'), dimensionsU, fieldtype='U', chunksize = 'auto', allow_time_extrapolation = True)
V_recom=Field.from_netcdf(data, ('V_recom','vav'), dimensionsV, fieldtype='V', chunksize = 'auto', allow_time_extrapolation = True)

#add RECOM fieldset to GBR fieldset
fieldset.add_field(U_recom)
fieldset.add_field(V_recom)


#create nested field
U=NestedField('U', [fieldset.U_recom, fieldset.U])
V=NestedField('V', [fieldset.V_recom, fieldset.V])
nest=FieldSet(U, V)

f = netCDF4.Dataset(data) #extract RECOM coordinates
lat = f.variables['latitude']
lon = f.variables['longitude']
latvals = lat[]; lonvals = lon[]

# a function to find the index of the point closest
# (in squared distance) to a given latlon value.
def getclosest_ij(lats,lons,latpt,lonpt)
  # find squared distance of every point on grid
  dist_sq = (lats-latpt)**2 + (lons-lonpt)**2
  # 1D index of minimum dist_sq element
  minindex_flattened = dist_sq.argmin()
  # Get 2D index for latvals and lonvals arrays from 1D index
  return np.unravel_index(minindex_flattened, lats.shape)


def CheckOutOfBounds(particle, fieldset, time):  #delete particles that are out of bounds
    if particle.state == StatusCode.ErrorOutOfBounds:
        particle.delete()

#read geospatial data 
coord = gpd.read_file(data_path + args.cluster +'' + args.spatial_data)
np.random.seed(10)

#a function to get random points in a polygon
def random_point_in_poly(poly)
        within = False
        while not within
            x = np.random.uniform(poly.bounds[0], poly.bounds[2])
            y = np.random.uniform(poly.bounds[1], poly.bounds[3])
            within = poly.contains(Point(x, y))
        return Point(x,y)

Lat, Lon = [], []
for i in range(num_particles)
    coord['Point' + str(i)] = coord['geometry'].apply(random_point_in_poly)
    Lat = [Lat,list(coord['Point'+str(i)].y)]
    Lon = [Lon,list(coord['Point'+str(i)].x)]

"""
Timing of annual coral spawning for 2015, 2016, 2017, 2018, 2019 and 2020 in the GBR 
Coral mass spawning by Acropora corals usually occurs around the spring-summer transition 
and peaks 4-6 days after the full moon
Year 2015: full moon on 26/11/2015
Year 2016: full moon on 12/11/2016
Year 2017: full moon on 4/11/2017 and 4/12/2017
Year 2018: full moon on 23/11/2018
Year 2019: full moon on 12/11/2019
Year 2020: full moon on 1/11/2020 and 30/11/2020

"""
releases = {
# particle releases at 800 pm
    2011 {
        1 datetime(2011, 11, 15, 20, 0),
        2 datetime(2011, 11, 16, 20, 0),
        3 datetime(2011, 11, 17, 20, 0),
    },
    2015 {
        1 datetime(2015, 11, 30, 20, 0),
        2 datetime(2015, 12, 1, 20, 0),
        3 datetime(2015, 12, 2, 20, 0),
    },
    2016 {
        1 datetime(2016, 11, 18, 20, 0),
        2 datetime(2016, 11, 19, 20, 0),
        3 datetime(2016, 11, 20, 20, 0),
    },
    2017 {
        1 datetime(2017, 11, 8, 20, 0),
        2 datetime(2017, 11, 9, 20, 0),
        3 datetime(2017, 11, 10, 20, 0),
        4 datetime(2017, 12, 8, 20, 0),
        5 datetime(2017, 12, 9, 20, 0),
        6 datetime(2017, 12, 10, 20, 0),
    },
    2018 {
        1 datetime(2018, 11, 27, 20, 0),
        2 datetime(2018, 11, 28, 20, 0),
        3 datetime(2018, 11, 29, 20, 0),
    },
    2019 {
        1 datetime(2019, 11, 16, 20, 0),
        2 datetime(2019, 11, 17, 20, 0),
        3 datetime(2019, 11, 18, 20, 0),
    },
    2020 {
        1 datetime(2020, 11, 5, 20, 0),
        2 datetime(2020, 11, 6, 20, 0),
        3 datetime(2020, 11, 7, 20, 0),
        4 datetime(2020, 12, 4, 20, 0),
        5 datetime(2020, 12, 5, 20, 0),
        6 datetime(2020, 12, 6, 20, 0),
    }
}

t0 = releases[args.year][args.day]
res = [t0 + delta(minutes=idx) for idx in range(0,num_release,int_release)] 
release_time = [i for i in res for n in range(0,len(coord))]  #list containing the initial conditions of all released particles
depth = [depth0] * len(Lat)


#create a particle set with the nested field
pset = ParticleSet.from_list(nest, pclass=JITParticle,
                             lon = Lon,
                             lat = Lat,
                             depth = depth,
                             time = release_time)
for p in pset
    yi, xi = getclosest_ij(latvals, lonvals, p.lat, p.lon)
    p.xi = np.array([xi], dtype=np.int32)
    p.yi = np.array([yi], dtype=np.int32)

output_file = pset.ParticleFile(name= args.cluster + 'outputs' + args.year + '' + args.cluster + '_trajectory_' + args.year + '_d' + args.day + 'dav.zarr', 
                                outputdt=delta(hours=out_dt))
pset.execute([AdvectionRK4,CheckOutOfBounds], runtime=delta(days=run_duration), dt=delta(minutes=run_dt), output_file=output_file)

             