#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 14:00:25 2020

@author: shirobakaidou
"""
# Import Modules
import os
import math
import csv
import json
import numpy as np
import geopandas as gpd
import matplotlib

import rasterio
from rasterio.plot import show, plotting_extent
from rasterio.mask import mask
from rasterio.merge import merge

from grass_session import Session
import grass.script as gs
import grass.script.setup as gsetup




def basinIndex(wd):
    
    # Set working directory
    os.chdir(wd)
    
    
    ###########################
    ## Set GRASS Environment ##
    ###########################

    # Define GRASS Database
    dbase = os.getcwd()
    location = 'mylocation'
    
    # Set GISBASE environment variable
    gisbase = '/usr/lib/grass78'
    os.environ['GISBASE'] = str(gisbase)
    
    # Initialize
    gsetup.init(os.environ['GISBASE'], dbase, location, 'PERMANENT')
    #print(gs.gisenv())
    
    # Create Location
    gs.create_location(dbase, location)
    
    # Create a new location, using a georeferenced file
    gs.run_command('g.proj', flags="c",
                   georef="/home/shirobakaidou/eagle/MET_Spatial_Python/data/hydroDEM_clip.tif",
                   location="rbasin_reproduce")
    
    # Switch to the location_vietnam, mapset "PERMANENT"
    gs.run_command('g.mapset', 
                   #location="mylocation",
                   location="rbasin_reproduce",
                   mapset="PERMANENT")
    
    


# Set working directory
os.chdir('/home/shirobakaidou/eagle/MET_Spatial_Python/grass')


###########################
## Set GRASS Environment ##
###########################

# Define GRASS Database
dbase = os.getcwd()
location = 'mylocation'

# Set GISBASE environment variable
gisbase = '/usr/lib/grass78'
os.environ['GISBASE'] = str(gisbase)

# Initialize
gsetup.init(os.environ['GISBASE'], dbase, location, 'PERMANENT')
print(gs.gisenv())

# Create Location
gs.create_location(dbase, location)

# Create a new location, using a georeferenced file
gs.run_command('g.proj', flags="c",
               georef="/home/shirobakaidou/eagle/MET_Spatial_Python/data/hydroDEM_clip.tif",
               location="rbasin_reproduce")

# Switch to the location_vietnam, mapset "PERMANENT"
gs.run_command('g.mapset', 
               #location="mylocation",
               location="rbasin_reproduce",
               mapset="PERMANENT")


#################
## Import Data ##
#################

# Read GeoTiFF as GRASS Raster (Import Raster)
gs.run_command('r.in.gdal', 
               #flags='e', # update the default region
               input='/home/shirobakaidou/eagle/MET_Spatial_Python/data/hydroDEM_clip.tif',
               output='r_elevation',
               quiet=True,
               overwrite=True)

# Set Region
gs.run_command('g.region', 
               flags="pa",
               raster='r_elevation')





