# Overview: a script for use in paraview that reads vtk files and creates an appropriate visualization
# 
# Desired functionality:
#  - Function to read in a directory of visualizations and process them automatically
#  - Function for complete "photographic" analysis of all open and visible visualizations
#   - Input a view orientation, get images of [everything] from that view
#    - Orientation, camera position, etc
#   - Here everything means...
#    - Opaque STL geometry images from each view
#    - The following with transparent geometry:
#     - For all files in a desired folder
#      - If binary image, images from each view
#       - Color appropriately based on name
#       - core_x red, core_y green, core_z blue
#       - cts purple, thin_wall_cavity cyan, thin_wall_mold magenta
#       - ihs orange, fill_distance purple
#      - If both IHS and Fill_distance present (specialization), repeat with the two combined
#      - If segmentation image, images from each view
#       - If Feeder, STL geo should be opaque
#      - If EDT (specialization)
#       - Analyze as scalar field
#       - Determine where each hotspot is
#       - For each hotspot
#        - Create x, y, z axial planes intersecting the hotspot
#        - Images from each view
#      - If STL
#       - Color appropriately based on name
#       - core_x red, core_y green, core_z blue

from paraview.simple import *
import os
from os import path
from inspect import getsourcefile
import sys
print os.path.abspath( os.path.dirname( getsourcefile( lambda:0 ) ) )
sys.path.insert( 0, os.path.abspath( os.path.dirname( getsourcefile( lambda:0 ) ) ) )
from DataLoader import *
from GlobalProperties import *

test_path = 'D://dev//repos//casting_segmentation//test_output//Autoriser//base_plate.stl'

( stl_path, stl_file_name ) = os.path.split( test_path )
stl_name = os.path.splitext( stl_file_name )[ 0 ]

renderView = GetActiveViewOrCreate( 'RenderView' )
initializeglobalproperties( renderView )

files = [ f for f in os.listdir( stl_path ) if os.path.isfile( os.path.join( stl_path, f ) ) and f.startswith( stl_name ) ]
for f in files:
    fpath = os.path.join( stl_path, f )
    name = os.path.splitext( f )[ 0 ]
    suffix = name[ len( stl_name ) : ]
    if suffix.startswith( '_' ):
        suffix = suffix.strip( '_' )
    print suffix
    if not suffix:
        loadstl( fpath, name, renderView )
        
    elif suffix.startswith( 'core' ):
        if suffix.endswith( 'x' ):
            color = [ 1.0, 0.0, 0.0 ]
        elif suffix.endswith( 'y' ):
            color = [ 0.0, 1.0, 0.0 ]
        elif suffix.endswith( 'z' ):
            color = [ 0.0, 0.0, 1.0 ]
        else:
            color = [ 0.0, 0.0, 0.0 ]
        loadbinaryimage( fpath, name, color, renderView )

    elif suffix.startswith( 'cts' ):
        color = [ 0.5, 0.0, 0.5 ]
        loadbinaryimage( fpath, name, color, renderView )
        
    elif suffix.startswith( 'edt' ):
        color_map_name = 'Black-Body Radiation'
        desired_extent = [ 0, None ]
        loadscalarimage( fpath, name, color_map_name, renderView, desired_extent )

        """
    elif suffix.startswith( 'feeder' ):
        color_map_name = 'hue_L60'
        desired_extent = [ 1, None ]
        loadsegmentimage( fpath, name, color_map_name, renderView, desired_extent )
        """

    elif suffix.startswith( 'fill_distance' ):
        color = [ 0.0, 0.5, 0.5 ]
        loadbinaryimage( fpath, name, color, renderView )

        """
    elif suffix.startswith( 'interior' ):
        color = [ 0.5, 0.5, 0.5 ]
        loadbinaryimage( fpath, name, color, renderView )
        """

    elif suffix.startswith( 'merged_segmentation' ):
        color_map_name = 'hue_L60'
        desired_extent = [ 1, None ]
        loadsegmentimage( fpath, name, color_map_name, renderView, desired_extent )

        """
    elif suffix.startswith( 'segmentation' ):
        color_map_name = 'hue_L60'
        desired_extent = [ 1, None ]
        loadsegmentimage( fpath, name, color_map_name, renderView, desired_extent )
        """

        """
    elif suffix.startswith( 'surface' ):
        color = [ 0.5, 0.5, 0.5 ]
        loadbinaryimage( fpath, name, color, renderView )
        """

    elif suffix.startswith( 'thin_wall' ):
        if suffix.endswith( 'cavity' ):
            color = [ 0.0, 1.0, 1.0 ]
        elif suffix.endswith( 'mold' ):
            color = [ 1.0, 0.0, 1.0 ]
        else:
            color = [ 0.0, 0.0, 0.0 ]
        loadbinaryimage( fpath, name, color, renderView )



def assemble_path( dirname, filename, ext ):
    return os.path.join( dirname, filename + ext )