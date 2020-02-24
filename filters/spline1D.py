import sys
import numpy as np
from   scipy.interpolate import interp1d

# ========================================================= #
# ===  spline 1D wrapper                                === #
# ========================================================= #
def spline1D( xAxis=None, yAxis=None, xInterp=None, Nx=1000, kind="cubic" ):
    # ------------------------------------------------- #
    # --- [1] 引数チェック                          --- #
    # ------------------------------------------------- #
    if ( yAxis   is None ): sys.exit( "[ERROR] yAxis ??? [ERROR]" )
    if ( xAxis   is None ): xAxis   = np.arange( yAxis.size )
    if ( xInterp is None ): xInterp = np.linspace( xAxis[0], xAxis[-1], Nx )
    # ------------------------------------------------- #
    # --- [2] spline 1D ラッパ                      --- #
    # ------------------------------------------------- #
    f       = interp1d( xAxis, yAxis, kind='cubic')
    yInterp = f( xInterp )
    return( ( xInterp, yInterp ) )
