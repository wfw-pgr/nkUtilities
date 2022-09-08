import os, sys
import numpy as np
import matplotlib.pyplot        as plt
import nkUtilities.load__config as lcf
import nkUtilities.mpl_baseSettings
import matplotlib.ticker        as tic


# ========================================================= #
# ===  draw__heatmap.py                                 === #
# ========================================================= #

def draw__heatmap( Data=None  , vmin=None, vmax=None, \
                   xlabels=None, ylabels=None, xtitle="", ytitle="", \
                   cmap="jet", textFormat="{0:.3f}", fontsize=10, pngFile=None, \
                   config=None, figsize=None, position=None, dpi=300, \
                   xMinor_Nticks=1, yMinor_Nticks=1, keep_aspect=True ):
    
    # ------------------------------------------------- #
    # --- [1] arguments                             --- #
    # ------------------------------------------------- #
    if ( Data       is None ): sys.exit( "[draw__heatmap.py] Data == ???" )
    if ( config     is None ): config     = lcf.load__config()
    if ( figsize    is None ): figsize    = config["FigSize"]
    if ( position   is None ): position   = config["plt_position"]
    if ( xlabels    is None ):
        xlabels  = [ str(ik+1) for ik in range( Data.shape[0] ) ]
    if ( ylabels    is None ):
        ylabels  = [ str(ik+1) for ik in range( Data.shape[1] ) ]

    xExtent, yExtent = 1.0, 1.0
    if ( keep_aspect ): yExtent  = xExtent * ( Data.shape[1] / Data.shape[0] )
    if ( vmin is None ): vmin = np.min( Data )
    if ( vmax is None ): vmax = np.max( Data )
    
    # ------------------------------------------------- #
    # --- [2] draw heatmap                          --- #
    # ------------------------------------------------- #
    fig = plt.figure( figsize=figsize )
    ax1 = fig.add_axes( [ position[0], position[1], \
                          position[2]-position[0], position[3]-position[1] ] )

    # ------------------------------------------------- #
    # --- [3] grid settings                         --- #
    # ------------------------------------------------- #
    xlabels_values = np.linspace( 0.0, xExtent, len(xlabels)+1 )
    ylabels_values = np.linspace( 0.0, yExtent, len(ylabels)+1 )
    xlabels_values = 0.5 * ( xlabels_values + np.roll( xlabels_values, -1 ) )[:-1]
    ylabels_values = 0.5 * ( ylabels_values + np.roll( ylabels_values, -1 ) )[:-1]
    ax1.set_xticks     ( xlabels_values )
    ax1.set_yticks     ( ylabels_values )
    ax1.set_xticklabels( xlabels, fontsize=config["xMajor_FontSize"] )
    ax1.set_yticklabels( ylabels, fontsize=config["yMajor_FontSize"] )
    ax1.set_xlabel     (  xtitle, fontsize=config["xTitle_FontSize"] )
    ax1.set_ylabel     (  ytitle, fontsize=config["yTitle_FontSize"] )
    ax1.xaxis.set_minor_locator( tic.AutoMinorLocator( xMinor_Nticks ) )
    ax1.yaxis.set_minor_locator( tic.AutoMinorLocator( yMinor_Nticks ) )

    # ------------------------------------------------- #
    # --- [4] make heatmap                          --- #
    # ------------------------------------------------- #
    ax1.imshow( np.transpose( Data[:,::-1] ), cmap=cmap, \
                extent=[0,xExtent,0,yExtent], vmin=vmin, vmax=vmax )
    
    # ------------------------------------------------- #
    # --- [5] make annotation map                   --- #
    # ------------------------------------------------- #
    for ik in range( Data.shape[0] ):
        for jk in range( Data.shape[1] ):
            ax1.text( xlabels_values[ik], ylabels_values[jk], \
                      textFormat.format( Data[ik,jk] ) ,\
                      horizontalalignment="center", verticalalignment  ="center", \
                      fontsize=fontsize )
            
    # ------------------------------------------------- #
    # --- [6] return                                --- #
    # ------------------------------------------------- #
    if ( pngFile is None ):
        fig.show()
        plt.show()
    else:
        fig.savefig( pngFile, dpi=dpi )


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):

    # ------------------------------------------------- #
    # --- [1] sample Data ( :: wine )               --- #
    # ------------------------------------------------- #
    import sklearn.datasets as ds
    wines      = ds.load_wine()
    avgs_      = np.average( wines.data, axis=0  )
    stds_      = np.std    ( wines.data, axis=0, ddof=True  )
    uniform    = np.ones(  ( wines.data.shape[0] ) )
    wines.avgs = np.outer( uniform, avgs_ )
    wines.stds = np.outer( uniform, stds_ )
    wines.norm = ( wines.data - wines.avgs ) /wines.stds
    wines.covs = np.cov( wines.norm, rowvar=False )
    Data       = np.copy( wines.covs )
    print( Data.shape )

    xlabels = [ "x{}".format( i+1 ) for i in range( Data.shape[0] ) ]
    ylabels = [ "y{}".format( i+1 ) for i in range( Data.shape[1] ) ]
    draw__heatmap( Data=Data, xlabels=xlabels, ylabels=ylabels, \
                   xtitle="x value", ytitle="y value", \
                   pngFile="test/heatmap.png" )
    
