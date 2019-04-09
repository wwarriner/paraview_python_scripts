from paraview.simple import *
from math import floor, ceil
from sys import stdout
from copy import deepcopy

# STL, monochromatic triangular data
def loadstl( filePath, name, renderView, color=None ):
    stl = STLReader( FileNames=[ filePath ] )
    RenameSource( name, stl )
    #lut = GetColorTransferFunction( 'STLSolidLabeling' )
    stlDisplay = Show( stl, renderView )
    #stlDisplay.LookupTable = lut
    ColorBy( stlDisplay, None )
    if color is not None:
        stlDisplay.DiffuseColor = color
    #stlDisplay.SetScalarBarVisibility( renderView, False )
    Render()
    renderView.ResetCamera()

    

# Binary images, monochromatic categorical data
def loadbinaryimage( filePath, arrayName, color, renderView ):
    binaryImage = LegacyVTKReader( FileNames=[ filePath ] )
    RenameSource( arrayName, binaryImage )
    binaryContour = Contour( Input=binaryImage )
    binaryContour.ContourBy = [ 'POINTS', arrayName ]
    binaryContour.Isosurfaces = [ 0.5 ]
    binaryContour.PointMergeMethod = 'Uniform Binning'
    binaryContourDisplay = Show( binaryContour, renderView )
    binaryContourDisplay.SetRepresentationType( 'Surface' )
    #ColorBy( binaryContourDisplay, None )
    binaryContourDisplay.DiffuseColor = color
    binaryContourDisplay.SetScalarBarVisibility( renderView, False )
    Render()



# Scalar field images, color-mapped continuous data
def loadscalarimage( filePath, arrayName, colorMapName, renderView, desiredExtent=[ None, None ] ):
    scalarImage = LegacyVTKReader( FileNames=[ filePath ] )
    RenameSource( arrayName, scalarImage )
    actualExtent = getExtent( desiredExtent, scalarImage, arrayName )
    scalarThreshold = Threshold( Input=scalarImage )
    scalarThreshold.Scalars = [ 'POINTS', arrayName ]
    scalarThreshold.ThresholdRange = actualExtent
    scalarThresholdDisplay = Show( scalarThreshold, renderView )
    scalarThresholdDisplay.SetScalarBarVisibility( renderView, False )
    setLut( arrayName, colorMapName, actualExtent )
    Render()



# Segment images, multichromatic categorical data
def loadsegmentimage( filePath, arrayName, colorMapName, renderView, desiredExtent=[ None, None ] ):
    segmentImage = LegacyVTKReader( FileNames=[ filePath ] )
    RenameSource( arrayName, segmentImage )
    actualExtent = getExtent( desiredExtent, segmentImage, arrayName )
    lutExtent = deepcopy( actualExtent )
    lutExtent[ 0 ] = lutExtent[ 0 ] - 1
    setLut( arrayName, colorMapName, lutExtent )
    segments = range( int( floor( actualExtent[ 0 ] ) ), int( ceil( actualExtent[ 1 ] ) ) + 1, 1 )
    for segment in segments:
        stdout.write( str( segment ) + ' ' )
        threshold = Threshold( Input=segmentImage )
        RenameSource( 'segment ' + str( segment ), threshold )
        threshold.Scalars = [ 'POINTS', arrayName ]
        threshold.ThresholdRange = [ segment - 0.5, segment + 0.5 ]
        isoVolumeDisplay = Show( threshold, renderView )
        #ColorBy( isoVolumeDisplay, arrayName )
        isoVolumeDisplay.SetScalarBarVisibility( renderView, False )
    Render()



def getExtent( desiredExtent, imageProxy, arrayName ):
    imageData = servermanager.Fetch( imageProxy )
    pointData = imageData.GetPointData()
    actualExtent = desiredExtent
    dataExtent = pointData.GetScalars().GetRange()
    if desiredExtent[ 0 ] is None:
        actualExtent[ 0 ] = dataExtent[ 0 ]
    if desiredExtent[ 1 ] is None:
        actualExtent[ 1 ] = dataExtent[ 1 ]
    return actualExtent



def setLut( arrayName, colorMapName, actualExtent ):
    lut = GetColorTransferFunction( arrayName )
    lut.ApplyPreset( colorMapName, True )
    lut.RescaleTransferFunction( actualExtent[ 0 ], actualExtent[ 1 ] )
    segmentImagePwf = GetOpacityTransferFunction( arrayName )
    segmentImagePwf.Points[ 1 ] = 1.0