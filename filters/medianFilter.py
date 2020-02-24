import sys
import numpy        as np
import scipy.signal as sig

# ========================================================= #
# ===  median filter                                    === #
# ========================================================= #
def medianFilter( Data=None, width=3 ):
    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    if ( Data  is None ): sys.exit( "[medianFilter] Data == ?? " )
    if ( width is None ): width = 3
    # ------------------------------------------------- #
    # --- [2] call median filter                    --- #
    # ------------------------------------------------- #
    Data = sig.medfilt( Data, kernel_size=width )
    return( Data )


# ======================================== #
# ===  実行部                          === #
# ======================================== #
if ( __name__=="__main__" ):
    nAmp  = 0.5
    Nx    = 1000
    noise = np.random.rand( Nx ) * nAmp - nAmp/2.0
    xAxis = np.linspace( 0.0, 6.28, Nx )
    yAxis = np.sin( xAxis * 2.0 )
    for i in range( Nx ):
        if ( i % 20 == 0 ):
            yAxis[i] = yAxis[i] + noise[i]
    import nkUtilities.plot1D as pl1
    med   = medianFilter( Data=yAxis, width=7 )
    fig   = pl1.plot1D( FigName="out.png" )
    fig.addPlot( xAxis=xAxis, yAxis=yAxis, label="Raw Data" )
    fig.addPlot( xAxis=xAxis, yAxis=med  , label="Filtered" )
    fig.setAxis()
    fig.addLegend()
    fig.writeFigure()
