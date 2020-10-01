#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 01:18:48 2020

@author: shirobakaidou
"""

# Function to Calc Indices
def calcIndices(wd, roi, dem):
    
    import os 
    import numpy as np
    import geopandas as gpd
    import rasterio
    from rasterio.mask import mask
    import json
    
    # Set Working Directory
    os.chdir(wd)
    
    # Read Vector File
    path_vector = os.path.join(os.getcwd(), roi)
    path_raster = os.path.join(os.getcwd(), dem)
    
    gdf = gpd.read_file(path_vector)
    r = rasterio.open(path_raster)
    
    # Convert Geometry of Shapefile to JSON Format to be readable by 'rasterio'
    coords = [json.loads(gdf.to_json())['features'][0]['geometry']]
    
    # Clip Raster with Vector Mask
    out_img, out_transform = mask(dataset = r, shapes = coords, crop = True)
    
    # Mask No Data Values
    dem_clip = np.ma.masked_array(out_img, mask = (out_img < 0))
    
    # Calculate Relative Relief
    relative_relief = dem_clip.max() - dem_clip.min()
    
    return print("Relative Relief is ", relative_relief, "m.")



output_test = calcIndices(wd = './sample_data', roi = "aoi.shp", dem = "srtm30.tif")        
