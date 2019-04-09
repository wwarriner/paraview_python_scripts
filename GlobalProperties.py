from paraview.simple import *

# Initialization of global properties:
#  - Set orientation axes visibility to off
#  - Set background color to white
#  - Set parallel projection on
#  - Edit Axes Grid:
#   - Set visibility to on
#   - Set X Title Font Properties color to black (Y, Z)
#   - Set Face Properties color to black
#   - Set X Axis Label Font Properties color to black (Y, Z)
def initializeglobalproperties( renderView ):    
    paraview.simple._DisableFirstRenderCameraReset()
    renderView.OrientationAxesVisibility = 0
    renderView.CameraParallelProjection = True
    renderView.Background = [ 1.0, 1.0, 1.0 ]
    axes = renderView.AxesGrid
    axes.XTitleColor = [ 0.0, 0.0, 0.0 ]
    axes.YTitleColor = [ 0.0, 0.0, 0.0 ]
    axes.ZTitleColor = [ 0.0, 0.0, 0.0 ]
    axes.GridColor = [ 0.0, 0.0, 0.0 ]
    axes.XLabelColor = [ 0.0, 0.0, 0.0 ]
    axes.YLabelColor = [ 0.0, 0.0, 0.0 ]
    axes.ZLabelColor = [ 0.0, 0.0, 0.0 ]
    axes.Visibility = True