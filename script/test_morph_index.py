"""
@purpose: Morphometric characterization of river basins
@author: Kemeng Liu
@contact: kemeng.liu@stud-mail.uni-wuerzburg.de
@reference: GRASS GIS module 'r.basin' developed by Margherita Di Leo and Massimo Di Stefano
            (https://github.com/OSGeo/grass-addons/tree/master/grass7/raster/r.basin)
"""
import os
import shutil
import math
from glob import glob
#import sys
#import subprocess
#import json

import numpy as np
import geopandas as gpd
from shapely.geometry import Polygon, Point, MultiPolygon
import rioxarray as rio
import rasterio
#from rasterio.mask import mask

import grass_session
import grass.script as gs
import grass.script.setup as gsetup


# Global Variables (if in docker env)
#path_input = '/app/input'
#path_output = '/app/output'


def basinIndex(dem, basin, inpath, outpath):
    """Calculate hydromorphological parameters of each basin polygon
    of the input .shp file, and store the parameters in the attribute
    table of the output .shp file.
    Parameters
    ----------
    dem : string
        File name of the input DEM.
    basin : string
        File name of the input SHP-file of basin polygons.
    crs : string
        EPSG code of the basins, e.g. "32648".
    path_input : string (optional)
        The path to the directory containing all input files.
        If the function is running inside Docker container, this argument should stay as default.
    path_output : string
        The path to the directory containing the output SHP-file.
        If the function is running inside Docker container, this argument should stay as default.
    Returns
    -------
    A printed message indicating the location where the output SHP-file is stored
    """


    # Input DEM (Should be in WGS84)
    dem_input = dem
    path_dem = os.path.join(inpath, dem_input)
    dem = rio.open_rasterio(path_dem, masked=True)

    # Input Basin
    basin_input = basin
    path_basin = os.path.join(inpath, basin_input)
    basin = gpd.read_file(path_basin)

    # GRASS Database
    grass_dbase = os.path.join(outpath, 'grass_session')
    # if os.path.exists(grass_dbase):
    #     shutil.rmtree(grass_dbase)
    # os.makedirs(grass_dbase)

    # GRASS location
    grass_location = 'mylocation'
    
    
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
    ls_basin_length = []
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


    ###---------------------------Preprocessing--------------------------------------------------###

    # Define a polygon and multi-polygon for 'if' statement
    polygon = Polygon([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]])
    multipolygon = MultiPolygon([polygon, polygon])

    ls_crs = np.empty(len(basin))
    
    for i in range(len(basin)):
        basin_geom = basin['geometry'][i]

        ################################################################
        ### 1. Filter to Main Basin (largest piece of multipolygons) ###
        ################################################################
        if type(basin_geom) == type(multipolygon):
            # Calc area of all polygons of the multipolygon
            area = [basin_geom[k].area for k in range(len(basin_geom))]

            # Get the index of the largest polygon
            index = [j for j,k in enumerate(area) if k==max(area)] # i is the index of k
            index = index[0]

            # Select the largest piece of polygon and turn it into 'multipolygon' format
            basin_main = MultiPolygon([basin_geom[index]])
            #basin_main = MultiPolygon([basin_main])

        elif type(basin_geom) == type(polygon):
            basin_main = MultiPolygon([basin_geom])


        ############################
        ### 2. Clip DEM by Basin ###
        ############################
        dem_clip = dem.rio.clip(basin_main)


        ########################
        ### 3. Reproject DEM ###
        ########################
        dem_prj = dem_clip.rio.reproject(dem_clip.rio.estimate_utm_crs())


        ##########################
        ### 4. Reproject Basin ###
        ##########################
        crs = dem_prj.rio.crs
        basin_prj = basin.to_crs(crs)

        ls_crs[i] = int(str(crs).split(":")[-1])


        ############################
        ### 5. Export Masked DEM ###
        ############################

        # Export Masked DEM
        path_dem_output = os.path.join(outpath, dem_input.split(".")[0]+"_msk."+dem_input.split(".")[1])
        dem_prj.rio.to_raster(path_dem_output)
        print("Export masked and projected DEM", i, "done!")
        
        
        ###################################
        ### 0. Set up GRASS Environment ###
        ###################################
        
        # Define GRASS Database
        dbase = grass_dbase
        location = grass_location
    
        # Set GISBASE Environment Variable
        grass7bin = 'grass'
    
        # query GRASS GIS itself for its GISBASE
        print('start command')
        #startcmd = [grass7bin, '--config', 'path']
        #try:
        #    p = subprocess.Popen(startcmd, shell=False,
        #                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #    out, err = p.communicate()
        #except OSError as error:
        #    sys.exit("ERROR: Cannot find GRASS GIS start script"
        #             " {cmd}: {error}".format(cmd=startcmd[0], error=error))
        #if p.returncode != 0:
        #    sys.exit("ERROR: Issues running GRASS GIS start script"
        #             " {cmd}: {error}"
        #             .format(cmd=' '.join(startcmd), error=err))
    
    
        # Set GISBASE Environment Variable
        #gisbase = '/usr/local/grass'
        #os.environ['GISBASE'] = str(gisbase)
        os.environ['GRASS_ADDON_BASE'] = '/usr/local/grass/addons'
    
        # Initialize
        gsetup.init(os.environ['GISBASE'], dbase, location, 'PERMANENT')
        print('gsetup.init successful')
        
        # Create Init Location
        gs.create_location(dbase, location)
        print('gs.create_location successful')
        # os.environ['GRASS_ADDON_BASE'] = '/usr/local/grass/addons'
    
        # Create New Location in Target Projection
        gs.run_command('g.proj',
                       flags = "c",
                       #georef = dem_prj
                       georef = path_dem_output
                        )
        
        # Switch to Projected Location, Mapset "PERMANENT"
        gs.run_command('g.mapset',
                       location = grass_location,
                       mapset = "PERMANENT")
        print('grass location is: ', grass_location)
        
        # Install hydrology related GRASS Addons
        #gs.run_command('g.extension', extension='r.stream.basins', operation='add', quiet=True)
        #gs.run_command('g.extension', extension='r.stream.order', operation='add', quiet=True)
        #gs.run_command('g.extension', extension='r.stream.snap', operation='add', quiet=True)
        #gs.run_command('g.extension', extension='r.stream.stats', operation='add', quiet=True)
    



        ###-------------Calculate Hydromorph Parameters using GRASS-------------------###
        
        ##############################
        ### 0. Load DEM into GRASS ###
        ##############################
        
        ### Read DEM ###
        gs.run_command('r.in.gdal',
                       flags='e',
                       #input = dem_prj,
                       input = path_dem_output,
                       output='r_elevation',
                       quiet=True,
                       overwrite=True)
        #print('r_elevation is: ', r_elevation)
        print('start g.region command')
        
        ### Set Region ###
        gs.run_command('g.region',
                       flags="a",
                       raster='r_elevation',
                       quiet=True,
                       overwrite=True)
        print('end g.region command')
        
        ### Define Threshold ###
        # source: https://github.com/OSGeo/grass-addons/blob/master/grass7/raster/r.basin/r.basin.py
        #gs.run_command('r.proj',
        #                location = location,
        #                mapset = 'PERMANENT',
        #                input = 'r_elevation',
        #                flags = 'p',
        #                quiet = False,
        #                output = 'projection')
        #print('projection of current mapset: ', projection)

        resolution = gs.region()['nsres']
        #print('resolution from gs.region: ', resolution)
        #resolution = 50
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
        #r_accum = rio.open_rasterio(path_accumulation, masked=True)

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
                       stream_raster = 'r_stream_e', # output unique stream ids
                       direction = 'r_drainage_e',
                       quiet = False,
                       memory = 10000,
                       overwrite=True)
        #gs.run_command('r.out.gdal',
        #               input = 'r_stream_e',
        #               output = os.path.join(outpath, 'r_stream_e2.tif'),
        #               format='GTiff',
        #               type = 'Int32',
        #               flags='f',
        #               quiet = True,
        #               overwrite = True)
        gs.message("Stream Extraction done.")
        # Create stream order maps: strahler, horton, hack, shreeve
        gs.run_command('r.stream.order',
                       stream_rast = 'r_stream_e',
                       direction = 'r_drainage_e',
                       strahler = 'r_strahler', # output Strahler order
                       shreve = 'r_shreve', # output Shreve order
                       horton = 'r_horton', # output Horton order
                       hack = 'r_hack', # output Hack order
                       quiet = True,
                       overwrite = True)
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
        # Reference: GRASS GIS Tool

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
        ### Index 4a: Main Channel Length ###
        ####################################

        param_mainchannel = gs.read_command('v.what',
                                            map = 'v_mainchannel',
                                            coordinates='%s,%s' % (east_o, north_o),
                                            distance=5)
        MCL = float(param_mainchannel.split('\n')[7].split()[1])/1000 # km
        print("Basin-", i, " Main Channel Length = ", MCL, " km")
        
        
        ##############################
        ### Index 4b: Basin Length ###
        ##############################
        
        # Define a polygon and multi-polygon for 'if' statement
        polygon = Polygon([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]])
        multipolygon = MultiPolygon([polygon, polygon])
        
        basin_geom = basin_prj['geometry']
        
        # Get x, y coords of points consisting basin polygon
        # If basin[geometry] is of type 'Polygon'
        if type(basin_geom[i]) == type(polygon): 
            x, y = basin_geom[i].exterior.coords.xy     

        # If basin[geometry] is 'Multipolygon',
        # since function 'v.exterior.coords.xy' doesn't apply on 'Multipolygon'
        elif type(basin_geom[i]) == type(multipolygon):
            #x,y = basin_geom[i][0].exterior.coords.xy

            # In order to find out the largest piece of Polygon out of the Multipolygons,
            # Set empty array in same length as the 'Multipolygon' to store length of each polygon
            polyLen = np.empty(len(basin_geom[i]), dtype=float)
            for k in range(len(basin_geom[i])):
                # Calc x,y coords of points consisting each piece polygon 
                x,y = basin_geom[i][k].exterior.coords.xy
                # Use the number of polygon-consisting points to indicate the size of the polygon.
                polyLen[k] = len(x)
            # Get the index of the largest polygon piece in the 'Multipolygon'
            target_index = [k for k,w in enumerate(polyLen) if w==max(polyLen)]
            # Calc the x,y coords of the points consisting the largest piece Polygon
            x, y = basin_geom[i][target_index[0]].exterior.coords.xy

        # Create 'GeoSeries' of outlet coords
        outlet = gpd.GeoSeries([Point(float(east_o), float(north_o))])

        # Create 'Geoseries' of the coords
        edge_points = gpd.GeoSeries([Point(x[j], y[j]) for j in range(len(x))])

        # Calc distances between 'outlet' and each 'polygon-consisting point',
        distance_arr = np.array([outlet.distance(w) for w in edge_points])

        # Get the maximal distance (in km), take it as 'Basin Length'
        Lb = float(max(distance_arr)/1000)
        print("Basin-", i, " Basin Length = ", Lb, " km")


        #################################
        ### Index 5: Elongation Ratio ###
        #################################

        elon_ratio = (2*math.sqrt(basin_area/math.pi))/Lb
        print("Basin-", i, " Elongation Ratio = ", elon_ratio)


        ############################
        ### Index 6: Form Factor ###
        ############################

        form_factor = basin_area/(Lb**2)
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

        relief_ratio = relative_relief/Lb
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
        ### Index 18: Average Mainstream Slope ###
        ###########################################

        gs.run_command('v.to.points',
                       input = 'v_mainchannel_dim',
                       output = 'v_mainchannel_dim_point',
                       type = 'line',
                       quiet = True,
                       overwrite = True)
        vertex = gs.read_command('v.out.ascii',
                                 input = 'v_mainchannel_dim_point',
                                 quiet = True,
                                 overwrite = True).strip().split('\n')

        nodi = np.zeros((len(vertex), 4), float)
        pendenze = []

        for j in range(len(vertex)):
            x, y = float(vertex[j].split('|')[0]), float(vertex[j].split('|')[1])
            vertice1 = gs.read_command('r.what',
                                       map = 'r_elevation',
                                       coordinates = '%s,%s' % (x,y))
            vertice = vertice1.replace('\n', '').replace('||', '|').split('|')
            nodi[j, 0], nodi[j, 1], nodi[j, 2] = float(vertice[0]), float(vertice[1]), float(vertice[2])

        for j in range(0, len(vertex)-1, 2):
            dist = math.sqrt(math.fabs((nodi[j, 0] - nodi[j+1, 0]))**2 + math.fabs((nodi[j, 1] - nodi[j+1, 1]))**2)
            deltaz = math.fabs(nodi[j, 2] - nodi[j+1, 2])
            # Control to prevent float division by zero (dist=0)
            try:
                pendenza = deltaz / dist
                pendenze.append(pendenza)
                mainchannel_slope = float(sum(pendenze) / len(pendenze)*100)
            except:
                pass
        print("Basin-", i, " Average Mainchannel Slope = ", mainchannel_slope, "%")


        #############################
        ### Index 19: Slope Ratio ###
        #############################

        slope_ratio = mainchannel_slope / basin_slope
        #Slope_ratio = float(stream_stats_mom[3])
        print("Basin-", i, " Slope Ratio = ", slope_ratio)



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
        ls_basin_length.extend([Lb])
        ls_total_stream_length.extend([Len_streams])
        ls_avg_basin_slope.extend([basin_slope])
        ls_avg_mainchannel_slope.extend([mainchannel_slope])
        ls_circularity_ratio.extend([circularity_ratio])
        ls_elongation_ratio.extend([elon_ratio])
        ls_form_factor.extend([form_factor])
        ls_relief_ratio.extend([relief_ratio])
        ls_dissection_index.extend([dissection_index])
        ls_hypsometric_integral.extend([hypsom])
        ls_bifurcation_ratio.extend([Bif_ratio])
        ls_channel_gradient.extend([channel_gradient])
        ls_slope_ratio.extend([slope_ratio])




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
                                     basin_length_km = ls_basin_length,

                                     avg_basin_slope = ls_avg_basin_slope,
                                     avg_mainchannel_slope_percent = ls_avg_mainchannel_slope,

                                     circularity_ratio = ls_circularity_ratio,
                                     elongation_ratio = ls_elongation_ratio,
                                     form_factor = ls_form_factor,
                                     relief_ratio = ls_relief_ratio,
                                     dissection_index = ls_dissection_index,
                                     hypsometric_integral = ls_hypsometric_integral,
                                     bifurcation_ratio = ls_bifurcation_ratio,
                                     channel_gradient = ls_channel_gradient,
                                     slope_ratio = ls_slope_ratio
                                     )

    # Output
    path_basin_index = os.path.join(outpath, basin_input.split(".")[0]+"_index")
    basin_pop.to_file(path_basin_index)

    # Delete temp files
    os.remove(os.path.join(outpath, "accumulation.tif"))
    os.remove(os.path.join(outpath, "basin_area_perimeter"))
    os.remove(path_dem_output)
    shutil.rmtree(os.path.join(outpath, "grass_session"))

    return(print("The calculated Parameters are stored in ", path_basin_index))


# Local Env
dem_input = 'SRTM_V4_90m_Vietnam_larger.tif'
basin_input = "aoi_sub.gpkg"
path_output = "/home/shirobakaidou/EAGLE/Hiwi/BasinIndice/basinindices_don_github/output"
path_input = "/home/shirobakaidou/EAGLE/Hiwi/BasinIndice/basinindices_don_github/input"


# Docker Env
#dem_input = 'SRTM_V4_90m_Vietnam_larger.tif'
#basin_input = "aoi_sub.gpkg"

basinIndex(inpath=path_input, outpath=path_output, dem=dem_input, basin=basin_input)

