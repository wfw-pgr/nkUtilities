import sys
import numpy                  as np
import nkUtilities.LoadConfig as lcf

# ========================================================= #
# ===  汎用 フィルタ 群                                 === #
# ========================================================= #
def generalFilter( xAxis=None, yAxis=None, config=None ):
    # ------------------------------------------------- #
    # --- Arguments                                 --- #
    # ------------------------------------------------- #
    if ( yAxis  is None ): sys.exit( "[generalFilter] None yAxis" )
    if ( config is None ): config = lcf.LoadConfig()
    if ( xAxis  is None ): xAxis  = np.arange( yAxis.size )    
    # ------------------------------------------------- #
    # --- メジアンフィルタリング                    --- #
    # ------------------------------------------------- #
    if ( config["flt_median" ] >=  3 ):
        import filters.medianFilter as med
        yAxis = med.medianFilter( Data=yAxis, width=config["flt_median"] )
    # ------------------------------------------------- #
    # --- フーリエフィルタリング                    --- #
    # ------------------------------------------------- #
    if ( config["flt_fourier"] > 0.0 ):
        import filters.fourierFilter as frf
        yAxis = frf.fourierFilter( Data=yAxis, fCutoff=config["flt_fourier"] )
    # ------------------------------------------------- #
    # --- ガウシアンフィルタリング                  --- #
    # ------------------------------------------------- #
    if ( config["flt_gaussian"] > 0.0 ):
        import scipy.ndimage.filters as gfl
        yAxis = gfl.gaussian_filter1d( yAxis, config["flt_gaussian"] )
    # ------------------------------------------------- #
    # --- スプライン 内挿                           --- #
    # ------------------------------------------------- #
    if ( config["flt_spline"  ] >   0 ):
        import scipy.interpolate
        splinefunc = scipy.interpolate.interp1d( xAxis, yAxis, kind='cubic')
        x_interp   = np.linspace( np.min( xAxis ), np.max( xAxis ), config["flt_spline"] )
        y_interp   = splinefunc( x_interp )
        xAxis      = x_interp
        yAxis      = y_interp
    # ------------------------------------------------- #
    # --- 線形フィルタリング                        --- #
    # ------------------------------------------------- #
    if ( config["flt_linear" ] > 0.0 ):
        import Filter.nxLinearFilter1D as lnf
        yAxis = lnf.nxLinearFilter1D( Data=yAxis, alpha=config["flt_linear"], nFilter=config["flt_ntimes"] )
    # ------------------------------------------------- #
    # --- 返却                                      --- #
    # ------------------------------------------------- #
    return( {"xAxis":xAxis, "yAxis":yAxis} )


# ======================================== #
# ===  実行部                          === #
# ======================================== #
if ( __name__=="__main__" ):
    xAxis  = np.linspace( 0.0, 2.0*2.0*np.pi, 101 )
    yAxis  = np.sin( xAxis )
    config = lcf.LoadConfig()
    # config["flt_median"] = 7
    config["flt_fourier"] = 0.5
    yAxis  = np.random.random( xAxis.shape ) * 0.05 + yAxis
    print( yAxis )
    ret    = generalFilter( xAxis=xAxis, yAxis=yAxis, config=config )
    import nkUtilities.plot1D as pl1
    pl1.plot1D( xAxis=ret["xAxis"], yAxis=ret["yAxis"] )
    
