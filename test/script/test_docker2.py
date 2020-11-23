#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 22 23:44:59 2020

@author: shirobakaidou
"""
import os
import sys
import subprocess
import shutil
import json
import math

import numpy as np
import geopandas as gpd

import rasterio
from rasterio.mask import mask
#from rasterio.transform import TransformMethodsMixin as TMM



def basinIndex(#wd, 
               path_input, path_output, dem, basin, crs):
    
    # Set working directory
    #os.chdir(wd)
    
    # Input path
    inpath = path_input
    
    # Output path
    outpath = path_output
    if os.path.exists(outpath):
        shutil.rmtree(outpath)
    os.makedirs(outpath)
    
    
    # Input DEM
    dem_input = dem
    
    # Input Basin
    basin_input = basin
    
    # Target CRS
    dst_crs = crs
    
    # GRASS Database
    grass_dbase = os.path.join(outpath, 'grass_session')
    if os.path.exists(grass_dbase):
        shutil.rmtree(grass_dbase)
    os.makedirs(grass_dbase)
    
    # GRASS location
    grass_location = 'mylocation'
    
    
    ###---------------------------Preprocessing--------------------------------------------------###
    
    ########################
    ### 1. Reproject DEM ###
    ########################
    
    path_dem = os.path.join(inpath, dem_input)
    path_dem_prj = os.path.join(outpath, dem_input.split(".")[0]+"_prj."+dem_input.split(".")[1])
    
    with rasterio.open(path_dem) as src:
        transform, width, height = rasterio.warp.calculate_default_transform(
            src.crs, dst_crs, src.width, src.height, *src.bounds)
        kwargs = src.meta.copy()
        kwargs.update({
            'crs': dst_crs,
            'transform': transform,
            'width': width,
            'height': height
            })
        
        with rasterio.open(path_dem_prj, 'w', **kwargs) as dst:
            for i in range(1, src.count + 1):
                rasterio.warp.reproject(
                    source = rasterio.band(src, i),
                    destination = rasterio.band(dst, i),
                    src_transform = src.transform,
                    src_crs = src.crs,
                    dst_transform = transform,
                    dst_crs = dst_crs,
                    resampling = rasterio.warp.Resampling.nearest)
    print("Reproject DEM done!")
    
    
    ##########################
    ### 2. Reproject Basin ###
    ##########################
    # Input Basin
    path_basin = os.path.join(inpath, basin_input)
    basin = gpd.read_file(path_basin)
    
    # Reproject
    basin_prj = basin.to_crs(dst_crs)
    print("Reproject Basin done!")
    
    
    ###################################
    ### 3. Set up GRASS Environment ###
    ###################################
    
    # Define GRASS Database
    dbase = grass_dbase
    location = grass_location
    
    # Set GISBASE Environment Variable
    grass7bin = 'grass'
    
    # query GRASS GIS itself for its GISBASE
    startcmd = [grass7bin, '--config', 'path']
    try:
        p = subprocess.Popen(startcmd, shell=False,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
    except OSError as error:
        sys.exit("ERROR: Cannot find GRASS GIS start script"
                 " {cmd}: {error}".format(cmd=startcmd[0], error=error))
    if p.returncode != 0:
        sys.exit("ERROR: Issues running GRASS GIS start script"
                 " {cmd}: {error}"
                 .format(cmd=' '.join(startcmd), error=err))
        
    # Set GISBASE Environment Variable
    gisbase = '/usr/local/grass'
    #gisbase = '/usr/lib/grass78'
    os.environ['GISBASE'] = str(gisbase)

    # Import GRASS Modules
    from grass_session import Session
    import grass.script as gs
    import grass.script.setup as gsetup
    
    # Initialize
    gsetup.init(os.environ['GISBASE'], dbase, location, 'PERMANENT')

    # Create Init Location
    gs.create_location(dbase, location)

    # Create New Location in Target Projection
    gs.run_command('g.proj', 
                   flags = "c",
                   georef = path_dem_prj)
    
    # Switch to Projected Location, Mapset "PERMANENT"
    gs.run_command('g.mapset', 
                   location = grass_location,
                   mapset = "PERMANENT")
    
    # Install hydrology related GRASS Addons
    gs.run_command('g.extension', extension='r.stream.basins', operation='add', quiet=True)
    gs.run_command('g.extension', extension='r.stream.order', operation='add', quiet=True)
    gs.run_command('g.extension', extension='r.stream.snap', operation='add', quiet=True)
    gs.run_command('g.extension', extension='r.stream.stats', operation='add', quiet=True)
    
    # Set empty list for every Index
    ls_perimeter = []
    ls_area = []
    ls_outlet_east = []
    ls_outlet_north = []
    ls_elevation_max = []
    ls_elevation_min = []
    ls_relative_relief = []
    ls_elevation_mean = []
    ls_mainchannel_length = []
    ls_total_stream_length = []
    ls_avg_basin_slope = []
    ls_avg_mainchannel_slope = []
    ls_circularity_ratio = []
    ls_elongation_ratio = []
    ls_form_factor = []
    ls_relief_ratio = []
    ls_dissection_index = []
    ls_hypsometric_integral = []
    ls_bifurcation_ratio = []
    ls_channel_gradient = []
    ls_slope_ratio = []
    print("Set GRASS Environment done!")
    
    
    # LOOP OVER ALL POLYGONS 
    for i in range(len(basin_prj)):
        
        ############################
        ### 4. Mask DEM by Basin ###
        ############################
        def getFeatures(gdf):
            return [json.loads(gdf.to_json())['features'][0]['geometry']]
        
        basin_geom = getFeatures(basin_prj[i:i+1])    
        
        # Load Projected DEM
        dem_prj = rasterio.open(path_dem_prj)
    
        # Mask DEM by Basin
        dem_msk, out_transform = mask(dataset=dem_prj, shapes=basin_geom, crop=True)
        
        # Mask out NA
        dem_msk = np.ma.masked_array(dem_msk, mask=(dem_msk < 0))
        print("Mask DEM by Basin", i, "done!")
        
        
        ############################
        ### 5. Export Masked DEM ###
        ############################
        
        # Copy Metadata of projected DEM before masking
        out_meta = dem_prj.meta.copy()
        out_meta.update({
            "driver": "GTiff",
            "count": dem_msk.shape[0],
            "height": dem_msk.shape[1],
            "width": dem_msk.shape[2],
            "transform": out_transform,
            "crs": dem_prj.crs
        })
        
        # Export Masked DEM
        path_dem_msk = os.path.join(outpath, dem_input.split(".")[0]+"_msk."+dem_input.split(".")[1])
        with rasterio.open(path_dem_msk, "w", **out_meta) as dest:
            dest.write(dem_msk)
        print("Export Masked DEM", i, "done!")
        
        
        
        ###-------------Calculate Hydromorph Parameters using GRASS-------------------###
        
        ### Read DEM ###
        gs.run_command('r.in.gdal', 
                       flags='e', 
                       input = path_dem_msk,
                       output='r_elevation',
                       quiet=True,
                       overwrite=True)
        
        ### Set Region ###
        gs.run_command('g.region', 
                       flags="a",
                       raster='r_elevation',
                       quiet=True,
                       overwrite=True)
        
        ### Define Threshold ###
        # source: https://github.com/OSGeo/grass-addons/blob/master/grass7/raster/r.basin/r.basin.py
        resolution = gs.region()['nsres']
        th = 1000000 / (resolution**2)
        #gs.message( "threshold : %s" % th )
        print("Threshold of Basin", i, "is: ", th)
        
        
        #########################################################
        ### 1. Watershed (Flow Direction & Flow Accumulation) ###
        #########################################################
        
        # Watershed SFD (single flow direction)
        gs.run_command('r.watershed',
                       flags='ams',
                       elevation='r_elevation',
                       accumulation='r_accumulation', # output accumulation
                       drainage='r_drainage', # output flow direction
                       convergence=5,
                       quiet=True,
                       overwrite=True)
        #gs.message("Flow Direction map and Flow Accumulation map done.")
        # Export Accumulation Map
        gs.run_command('r.out.gdal',
                       input = 'r_accumulation',
                       output = os.path.join(outpath, 'accumulation.tif'),
                       format='GTiff',
                       type = 'Int32',
                       flags='f',
                       quiet = True,
                       overwrite = True)
        print("Extract Watershed of Basin", i, "done!")
        
        
        #####################################
        ### 2. Outlet = max(Accumulation) ###
        #####################################
        
        path_accumulation = os.path.join(outpath, 'accumulation.tif')
        with rasterio.open(path_accumulation) as src:
            r_accum = src.read()
            
        # Get the index (row, col) of the pixel of maximal accumulation
        index_outlet=np.transpose(np.nonzero(r_accum[0]==r_accum.max()))
        
        # Get the coordinate of the pixel corresponding to the index
        coord_outlet = [src.xy(col, row) for col, row in index_outlet]
        east_o = coord_outlet[0][0]
        north_o = coord_outlet[0][1]
        print("The East and North  Outlet Coordinates of Basin", i, "is: ", east_o, ",", north_o)
        
        
        ################################
        ### 3. Stream & Stream Order ###
        ################################
        
        # Stream Extraction
        gs.run_command('r.stream.extract', 
                       elevation = 'r_elevation',
                       accumulation = 'r_accumulation',
                       threshold = th,
                       #d8cut =  1000000000,
                       mexp = 0,
                       stream_rast = 'r_stream_e', # output unique stream ids
                       direction = 'r_drainage_e',
                       quiet=True,
                       overwrite=True)
        #gs.message("Stream Extraction done.")
        # Create stream order maps: strahler, horton, hack, shreeve
        gs.run_command('r.stream.order',
                       stream_rast = 'r_stream_e',
                       direction = 'r_drainage_e',
                       strahler = 'r_strahler', # output Strahler order
                       shreve = 'r_shreve', # output Shreve order
                       horton = 'r_horton', # output Horton order
                       hack = 'r_hack', # output Hack order
                       quiet=True,
                       overwrite=True)
        #gs.message("Stream order maps of Strahler, Horton, Hack and Shreeve are created.")
        print("Extract Stream and Stream Order of Basin", i, "done!")
        
        
        ##########################
        ### 4. Delineate Basin ###
        ##########################
        
        # Delineation of basin: Create outlet
        gs.write_command('v.in.ascii',
                         input='-',
                         output='v_outlet',
                         sep=",",
                         stdin="%s,9999" % (str(east_o)+","+str(north_o)), # <modify coordinates>
                         quiet=True,
                         overwrite=True)
        
        # The point is snapped to the nearest point which lies on the streamline
        gs.run_command('r.stream.snap',
                       input='v_outlet', 
                       stream_rast='r_stream_e', # Input stream network
                       output='v_outlet_snap', # output vector points map
                       quiet=True,
                       overwrite=True)
        gs.run_command('v.to.rast',
                       input='v_outlet_snap',
                       output='r_outlet',
                       use='cat',
                       type='point',
                       layer=1,
                       value=1,
                       quiet=True,
                       overwrite=True)
        
        # Delineate Basin
        gs.run_command('r.stream.basins',
                       direction='r_drainage_e', # Input flow direction
                       points='v_outlet_snap', # Input vector points
                       basins='r_basin', # Output basin
                       quiet=True,
                       overwrite=True)
        
        # Create Basin Mask (Vector)
        gs.run_command('r.to.vect',
                       input='r_basin',
                       output='v_basin',
                       type='area',
                       flags='sv',
                       quiet=True,
                       overwrite=True)
        #gs.message("Delineation of basin done!")
        print("Delineation of Basin", i, "done!")
        
        
        ######################
        ### 5. Mainchannel ###
        ######################
        gs.mapcalc ("$r_mainchannel = if($r_hack==1,1,null())",
                    r_hack = 'r_hack', # input
                    r_mainchannel = 'r_mainchannel', # output
                    quiet=True,
                    overwrite=True) 
        gs.run_command("r.thin", 
                       input = 'r_mainchannel',
                       output = 'r_mainchannel'+'_thin',
                       quiet=True,
                       overwrite=True)
        gs.run_command('r.to.vect',
                       input='r_mainchannel'+'_thin',
                       output='v_mainchannel',
                       type='line',
                       #verbose=True,
                       quiet=True,
                       overwrite=True)
        #gs.message("Main Channel is extracted.")
        print("Extract Main Channel of Basin", i, "done!")
        
        
        #########################
        ### 6. Slope & Aspect ###
        #########################
        # Creation of Slope and Aspect maps
        gs.run_command('r.slope.aspect',
                       elevation='r_elevation',
                       slope='r_slope',
                       aspect = 'r_aspect',
                       quiet=True,
                       overwrite=True)
        #gs.message("Slope and Aspect maps done.")
        print("Slope and Aspect Map of Basin", i, "done!")
        
        
        ###############################
        ### 7. Topological Diameter ###
        ###############################
        gs.mapcalc("$r_mainchannel_dim = -($r_mainchannel - $r_shreve) + 1",
                   r_mainchannel_dim = 'r_mainchannel_dim',
                   r_shreve = 'r_shreve',
                   r_mainchannel = 'r_mainchannel',
                   quiet = True,
                   overwrite = True)
        gs.run_command('r.thin',
                       input = 'r_mainchannel_dim',
                       output = 'r_mainchannel_dim_thin',
                       quiet = True,
                       overwrite = True)
        gs.run_command('r.to.vect',
                       input = 'r_mainchannel_dim_thin',
                       output = 'v_mainchannel_dim',
                       type = 'line',
                       flags = 'v',
                       quiet = True,
                       overwrite = True)
        print("Calc Topological Diameter of Basin", i, "done!")
        
        
        ###------------------Hydromophorlogical Indices-----------------###
        
        #########################################
        ### Index 1-2: Basin Area & Perimeter ###
        #########################################
        
        # Add two columns to the table 'basin': Area and Perimeter
        gs.run_command('v.db.addcolumn',
                       map='v_basin',
                       columns='area double precision') # name & type
        gs.run_command('v.db.addcolumn',
                       map='v_basin',
                       columns='perimeter double precision')
        
        # Populate Perimeter Column
        gs.run_command('v.to.db',
                       map='v_basin',
                       type='line,boundary',
                       layer=1,
                       qlayer=1,
                       option='perimeter',
                       units='kilometers',
                       columns='perimeter',
                       quiet=True,
                       overwrite=True)
        gs.run_command('v.to.db',
                       map='v_basin',
                       type='line,boundary',
                       layer=1,
                       qlayer=1,
                       option='area',
                       units='kilometers',
                       columns='area',
                       #flags='c',
                       quiet=True,
                       overwrite=True)
        #gs.message("Column 'Area' and 'Perimeter' are populated!")
        
        # Export Selected Attributes
        gs.run_command('v.db.select',
                       map='v_basin',
                       column='perimeter, area',
                       file=os.path.join(outpath,'basin_area_perimeter'),
                       overwrite=True)
        
        # Read Perimeter and Area from the text file
        tmp = open(os.path.join(outpath,"basin_area_perimeter"), "r")
        tmp = tmp.read()
        
        # Extract Perimeter and Area
        basin_perimeter = float(tmp.split('\n')[1].split('|')[0])
        basin_area = float(tmp.split('\n')[1].split('|')[1])
        print("Basin-", i, " Basin Perimeter = " , basin_perimeter, " km")
        print("Basin-", i, " Basin Area = " , basin_area, " km2")
        
        
        ##################################
        ### Index 3: Circularity Ratio ###
        ##################################
        
        circularity_ratio = (4*math.pi*basin_area)/(basin_perimeter**2)
        print("Basin-", i, " Circularity Ratio = ", circularity_ratio)
        
        
        ####################################
        ### Index 4: Main Channel Length ###
        ####################################
        
        param_mainchannel = gs.read_command('v.what',
                                            map = 'v_mainchannel',
                                            coordinates='%s,%s' % (east_o, north_o),
                                            distance=5)
        MCL = float(param_mainchannel.split('\n')[7].split()[1])/1000 # km
        print("Basin-", i, " Main Channel Length = ", MCL, " km")
        
        
        #################################
        ### Index 5: Elongation Ratio ###
        #################################
        
        elon_ratio = (2*math.sqrt(basin_area/math.pi))/MCL
        print("Basin-", i, " Elongation Ratio = ", elon_ratio)
        
        
        ############################
        ### Index 6: Form Factor ###
        ############################
        
        form_factor = basin_area/(MCL**2)
        print("Basin-", i, " Form Factor = ", form_factor)
        
        
        #############################
        ### Index 7-10: Elevation ###
        #############################
        
        # Relative Relief (Hmax - Hmin)
        height_attr = gs.read_command('r.info', 
                        flags='r',
                        map='r_elevation')
        height_min = float(height_attr.strip().split('\n')[0].split('=')[-1])
        height_max = float(height_attr.strip().split('\n')[1].split('=')[-1])
        relative_relief = height_max - height_min
        
        # Mean Elevation
        gs.run_command("r.stats.zonal",
                       base = 'r_basin',
                       cover = 'r_elevation',
                       method = 'average',
                       output = 'r_height_average',
                       quiet = True,
                       overwrite = True)
        mean_elev = float(gs.read_command('r.info',
                                          flags = 'r',
                                          map = 'r_height_average').split('\n')[0].split('=')[1])
        
        print("Basin-", i, " Elevation MAX = ", height_max, " m")
        print("Basin-", i, " Elevation MIN = ", height_min, " m")
        print("Basin-", i, " Elevation Range = ", relative_relief, " m")
        print("Basin-", i, " Elevation Mean = ", mean_elev, " m")
        
        
        ##############################
        ### Index 11: Relief Ratio ###
        ##############################
        
        relief_ratio = (relative_relief/1000)/MCL
        print("Basin-", i, " Relief Ratio = ", relief_ratio)
        
        
        ##################################
        ### Index 12: Dissection Index ###
        ##################################
        
        dissection_index = relative_relief/height_max
        print("Basin-", i, " Dissection Index = ", dissection_index)
        
        
        ######################################
        ### Index 13: Hypsometric Integral ###
        ######################################
        
        hypsom = (mean_elev-height_min)/relative_relief
        print("Basin-", i, " Hypsometric Integral = ", hypsom)
        
        
        #####################################
        ### Index 14: Average Basin Slope ###
        #####################################
        
        slope_baricenter = gs.read_command("r.volume", 
                                           input = 'r_slope',
                                           clump = 'r_basin',
                                           quiet = True).split()
        basin_slope = float(slope_baricenter[30])
        print("Basin-", i, " Average Basin Slope = ", basin_slope)
        
        
        #####################################
        ### Index 15-17: Channel Gradient ###
        #####################################
        
        stream_stats = gs.read_command('r.stream.stats',
                                       stream_rast = 'r_strahler', # NOT Horton???
                                       direction = 'r_drainage_e',
                                       elevation = 'r_elevation',
                                       quiet = True)
        
        stream_stats_summary = stream_stats.split('\n')[4].split('|')
        stream_stats_mom = stream_stats.split('\n')[8].split('|')
        
        Len_streams = float(stream_stats_summary[2])
        Bif_ratio = float(stream_stats_mom[0])
        channel_gradient = relative_relief / ((math.pi/2) * ((Len_streams/(Len_streams-1)) / Bif_ratio))
        print("Basin-", i, " Total Stream Length = ", Len_streams, "km")
        print("Basin-", i, " Bifurcation Ratio = ", Bif_ratio)
        print("Basin-", i, " Channel Gradient = ", channel_gradient)
        
        
        ###########################################
        ### Index 18: Average Mainchannel Slope ###
        ###########################################
        
#        gs.run_command('v.to.points',
#                       input = 'v_mainchannel_dim',
#                       output = 'v_mainchannel_dim_point',
#                       type = 'line',
#                       quiet = True,
#                       overwrite = True)
#        vertex = gs.read_command('v.out.ascii',
#                                 input = 'v_mainchannel_dim_point',
#                                 quiet = True,
#                                 overwrite = True).strip().split('\n')
        
#        nodi = np.zeros((len(vertex), 4), float)
#        pendenze = []
        
#        for i in range(len(vertex)):
#            x, y = float(vertex[i].split('|')[0]), float(vertex[i].split('|')[1])
#            vertice1 = gs.read_command('r.what',
#                                       map = 'r_elevation',
#                                       coordinates = '%s,%s' % (x,y))
#            vertice = vertice1.replace('\n', '').replace('||', '|').split('|')
#            nodi[i, 0], nodi[i, 1], nodi[i, 2] = float(vertice[0]), float(vertice[1]), float(vertice[2])
            
#        for i in range(0, len(vertex)-1, 2):
#            dist = math.sqrt(math.fabs((nodi[i, 0] - nodi[i+1, 0]))**2 + math.fabs((nodi[i, 1] - nodi[i+1, 1]))**2)
#            deltaz = math.fabs(nodi[i, 2] - nodi[i+1, 2])  
#            # Control to prevent float division by zero (dist=0)
#            try:
#                pendenza = deltaz / dist
#                pendenze.append(pendenza)
#                mainchannel_slope = float(sum(pendenze) / len(pendenze)*100)
#            except:
#                pass


        ##########################
        ### Index: Slope Ratio ###
        ##########################
        
#        slope_ratio = mainchannel_slope / basin_slope
        #Slope_ratio = float(stream_stats_mom[3])
        
        
        
        # Fill parameter lists
        ls_perimeter.extend([basin_perimeter])
        ls_area.extend([basin_area])
        ls_outlet_east.extend([east_o])
        ls_outlet_north.extend([north_o])
        ls_elevation_max.extend([height_max])
        ls_elevation_min.extend([height_min])
        ls_relative_relief.extend([relative_relief])
        ls_elevation_mean.extend([mean_elev])
        ls_mainchannel_length.extend([MCL])
        ls_total_stream_length.extend([Len_streams])
        ls_avg_basin_slope.extend([basin_slope])
#        ls_avg_mainchannel_slope.extend([mainchannel_slope])
        ls_circularity_ratio.extend([circularity_ratio])
        ls_elongation_ratio.extend([elon_ratio])
        ls_form_factor.extend([form_factor])
        ls_relief_ratio.extend([relief_ratio])
        ls_dissection_index.extend([dissection_index])
        ls_hypsometric_integral.extend([hypsom])
        ls_bifurcation_ratio.extend([Bif_ratio])
        ls_channel_gradient.extend([channel_gradient])
#        ls_slope_ratio.extend([slope_ratio])
        
        
        
    ###----------Write Indices as Attribute into Basin Shapefile------------###
    basin_pop = basin_prj.assign(perimeter_km = ls_perimeter,
                                     area_km = ls_area,
                                     outlet_east = ls_outlet_east,
                                     outlet_north = ls_outlet_north,
                                     
                                     elevation_max_m = ls_elevation_max,
                                     elevation_min_m = ls_elevation_min,
                                     relative_relief_m = ls_relative_relief,
                                     elevation_mean_m = ls_elevation_mean,
                                     
                                     mainchannel_length_km = ls_mainchannel_length,
                                     total_stream_length_km = ls_total_stream_length,
                                     
                                     avg_basin_slope = ls_avg_basin_slope,
#                                     avg_mainchannel_slope_percent = ls_avg_mainchannel_slope,
                                     
                                     circularity_ratio = ls_circularity_ratio,
                                     elongation_ratio = ls_elongation_ratio,
                                     form_factor = ls_form_factor,
                                     relief_ratio = ls_relief_ratio,
                                     dissection_index = ls_dissection_index,
                                     hypsometric_integral = ls_hypsometric_integral,
                                     bifurcation_ratio = ls_bifurcation_ratio,
                                     channel_gradient = ls_channel_gradient,
#                                     slope_ratio = ls_slope_ratio
                                     )
        
    # Output
    path_basin_index = os.path.join(outpath, basin_input.split(".")[0]+"_index")
    basin_pop.to_file(path_basin_index)
    
    # Delete temp files
    os.remove(os.path.join(outpath, "accumulation.tif"))
    os.remove(os.path.join(outpath, "basin_area_perimeter"))
    os.remove(path_dem_prj)
    os.remove(path_dem_msk)
    shutil.rmtree(os.path.join(outpath, "grass_session"))
    
    return(print("The calculated Parameters are stored in ", path_basin_index))





#wd = '/home/shirobakaidou/docker_lab/morph_index/test/'
#path_input = '/home/shirobakaidou/docker_lab/morph_index/test/input'
#path_output = '/home/shirobakaidou/docker_lab/morph_index/test/output'    
#wd = '.'
path_input = '/app/input'
path_output = '/app/output'
dem_input = 'hydrosheds_90m.tif'
basin_input = 'Hydrosheds_level8_centralVN.shp'
dst_crs = 'EPSG:32648'

basinIndex(#wd=wd, 
           path_input=path_input, path_output=path_output, dem=dem_input, basin=basin_input, crs=dst_crs)
