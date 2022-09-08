import os, sys
import numpy as np
import nkUtilities.mpl_baseSettings
import matplotlib.pyplot        as plt
import nkUtilities.load__config as lcf


# ========================================================= #
# ===  make__colorbar.py                                === #
# ========================================================= #

def make__colorbar( cmap=None, nlevels=None, config=None, \
                    position=None, figsize=None, orientation=None, \
                    pngFile=None, dpi=300 ):

    # ------------------------------------------------- #
    # --- [1] arguments                             --- #
    # ------------------------------------------------- #
    if ( config      is None ): config      = lcf.load__config()
    if ( orientation is None ): orientation = config["colorbar.orientation"]
    if   ( orientation.lower() == "horizontal" ):
        if ( figsize   is None ): figsize  = (5,1)
        if ( position  is None ): position = [ 0.10, 0.10, 0.90, 0.90 ]
    elif ( orientation.lower() == "vertical" ):
        if ( figsize   is None ): figsize  = (1,5)
        if ( position  is None ): position = [ 0.10, 0.10, 0.90, 0.90 ]
    if ( nlevels  is None ): nlevels  = config["colorbar.nlevels"]
    if ( cmap     is None ): cmap     = config["colorbar.cmap"]
    if ( pngFile  is None ): pngFile  = config["colorbar.pngFile"]
    
        
    # ------------------------------------------------- #
    # --- [2] plot region                           --- #
    # ------------------------------------------------- #
    fig     = plt.figure( figsize=figsize )
    ax1     = fig.add_axes( [ position[0], position[1], \
                              position[2]-position[0], position[3]-position[1] ] )
    if   ( orientation.lower() == "horizontal" ):
        Data    = np.array( [ [ 0.0,1.0 ], [0.0,1.0] ]  )
    elif ( orientation.lower() == "vertical"   ):
        Data    = np.array( [ [ 0.0,0.0 ], [1.0,1.0] ]  )
    levels  = np.linspace( 0.0, 1.0, nlevels )
    
    # ------------------------------------------------- #
    # --- [3] axis settings                         --- #
    # ------------------------------------------------- #
    ax1.set_xlim( [ 0.0, 1.0] )
    ax1.set_ylim( [ 0.0, 1.0] )
    ax1.get_xaxis().set_ticks([])
    ax1.get_yaxis().set_ticks([])

    # ------------------------------------------------- #
    # --- [4] draw color bar                        --- #
    # ------------------------------------------------- #
    ax1.contourf( [ 0.0,1.0 ], [0.0,1.0], Data, levels, cmap=cmap )
        
    # ------------------------------------------------- #
    # --- [6] output .png file                      --- #
    # ------------------------------------------------- #
    fig.savefig( pngFile, dpi=dpi, pad_inches=0 )
    return()

# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    make__colorbar( pngFile="test/colorbar.png" )

