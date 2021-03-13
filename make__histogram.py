import os, sys, subprocess
import numpy                    as np
import nkUtilities.load__config as lcf
import nkUtilities.plot1D       as pl1

# ========================================================= #
# ===  make__histogram.py                               === #
# ========================================================= #

def make__histogram( Data=None, bins=None, range=None, \
                     color=None, alpha=None, width=None, \
                     pngFile=None, draw=True, config=None,  ):
    
    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #

    if ( Data    is None ): sys.exit( "[draw__histogram.py] Data == ???" )
    if ( config  is None ): config  = lcf.load__config()
    if ( bins    is None ): bins    = config["histo_bins"]
    
    # ------------------------------------------------- #
    # --- [2] make histogram                        --- #
    # ------------------------------------------------- #
    
    hist, bound = np.histogram( Data, bins=bins, range=range )
    axis        = 0.5 * ( bound[:-1] + bound[1:] )
    
    # ------------------------------------------------- #
    # --- [3] plotting                              --- #
    # ------------------------------------------------- #
    if ( draw ):
        if ( pngFile is None ):
            print( "[make__histogram.py] make__histogram.py :: None pngFile  .. --> out.png" )
            pngFile = "out.png"

        fig = pl1.plot1D( pngFile=pngFile, config=config )
        fig.add__bar( xAxis=axis, yAxis=hist, alpha=alpha, color=color,  )
        fig.set__axis()
        fig.save__figure()

    # ------------------------------------------------- #
    # --- [4] return                                --- #
    # ------------------------------------------------- #
    return( hist, axis )
    

# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #
if ( __name__=="__main__" ):
    sample_Data = np.random.normal( loc=0.2, scale=1.0, size=10001 )
    histo       = make__histogram( Data=sample_Data, pngFile = "out.png" )
