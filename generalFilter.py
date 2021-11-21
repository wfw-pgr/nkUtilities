import sys
import numpy                    as np
import nkUtilities.load__config as lcf

# ========================================================= #
# ===  汎用 フィルタ 群                                 === #
# ========================================================= #

def generalFilter( xAxis=None, yAxis=None, config=None, returnType="list" ):
    
    # ------------------------------------------------- #
    # --- Arguments                                 --- #
    # ------------------------------------------------- #
    if ( yAxis  is None ): sys.exit( "[generalFilter] None yAxis" )
    if ( config is None ): config = lcf.load__config()
    if ( xAxis  is None ): xAxis  = np.arange( yAxis.size )
    
    # ------------------------------------------------- #
    # --- メジアンフィルタリング                    --- #
    # ------------------------------------------------- #
    if ( config["filter.median"] is not None ):
        if ( config["filter.median" ] >= 3 ):
            import filters.medianFilter as med
            yAxis = med.medianFilter( Data=yAxis, width=config["filter.median"] )
        
    # ------------------------------------------------- #
    # --- フーリエフィルタリング                    --- #
    # ------------------------------------------------- #
    if ( config["filter.fourier"] is not None ):
        if ( config["filter.fourier"] > 0.0 ):
            import filters.fourierFilter as frf
            yAxis = frf.fourierFilter( Data=yAxis, fCutoff=config["filter.fourier"] )
        
    # ------------------------------------------------- #
    # --- ガウシアンフィルタリング                  --- #
    # ------------------------------------------------- #
    if ( config["filter.gaussian"] is not None ):
        if ( config["filter.gaussian"] > 0.0 ):
            import scipy.ndimage.filters as gfl
            yAxis = gfl.gaussian_filter1d( yAxis, config["filter.gaussian"] )
            
    # ------------------------------------------------- #
    # --- スプライン 内挿                           --- #
    # ------------------------------------------------- #
    if ( config["filter.spline"] is not None ):
        if ( config["filter.spline"] > 0 ):
            import scipy.interpolate
            splinefunc = scipy.interpolate.interp1d( xAxis, yAxis, kind='cubic')
            x_interp   = np.linspace( np.min( xAxis ), np.max( xAxis ), \
                                      config["filter.spline"] )
            y_interp   = splinefunc( x_interp )
            xAxis      = x_interp
            yAxis      = y_interp
            
    # ------------------------------------------------- #
    # --- 線形フィルタリング                        --- #
    # ------------------------------------------------- #
    if ( config["filter.linear"] is not None ):
        if ( config["filter.linear"] > 0.0 ):
            import Filter.nxLinearFilter1D as lnf
            yAxis = lnf.nxLinearFilter1D( Data=yAxis, alpha=config["filter.linear"], \
                                          nFilter=config["filter.ntimes"] )
        
    # ------------------------------------------------- #
    # --- 返却                                      --- #
    # ------------------------------------------------- #
    if   ( returnType.lower() == "dict" ):
        ret = { "xAxis":xAxis, "yAxis":yAxis }
    elif ( returnType.lower() == "list" ):
        ret = [ xAxis, yAxis ]
    elif ( returnType.lower() == "array" ):
        ret = np.cocatenate( [ xAxis[:,None], yAxis[:,None] ] )
    return( ret )


# ======================================== #
# ===  実行部                          === #
# ======================================== #

if ( __name__=="__main__" ):
    
    xAxis  = np.linspace( 0.0, 2.0*2.0*np.pi, 101 )
    yAxis  = 1.0 * np.sin(xAxis) + np.random.random( xAxis.shape ) * 0.05

    import nkUtilities.plot1D         as pl1
    import nkUtilities.configSettings as cfs
    x_,y_                    = 0, 1
    pngFile                  = "test/filter.png"
    config                   = lcf.load__config()
    config                   = cfs.configSettings( configType="plot.def", config=config )
    # config["filter.linear"]  = 0.5
    # config["filter.median"]  = 3
    config["filter.fourier"] = 0.5

    print( yAxis )
    xAxis_, yAxis_ = generalFilter( xAxis=xAxis, yAxis=yAxis, config=config )
    print( yAxis_ )
    
    fig     = pl1.plot1D( config=config, pngFile=pngFile )
    fig.add__plot( xAxis=xAxis_, yAxis=yAxis_, label="w/" , linestyle="-"  )
    fig.add__plot( xAxis=xAxis , yAxis=yAxis , label="w/o", linestyle="--" )
    fig.add__legend()
    fig.set__axis()
    fig.save__figure()


