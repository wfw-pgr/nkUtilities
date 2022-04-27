import numpy as np
import os, sys
import matplotlib.pyplot as plt

# ========================================================= #
# ===  adjust__plot.py                                  === #
# ========================================================= #

def adjust__plot( ax=None, params=None ):

    # ------------------------------------------------- #
    # --- [1] arguments                             --- #
    # ------------------------------------------------- #
    if ( ax     is None ): sys.exit( "[adjust__plot.py] ax == ???" )
    if ( params is None ): sys.exit( "[adjust__plot.py] params == ???" )
    
    # ------------------------------------------------- #
    # --- [2] for every params                      --- #
    # ------------------------------------------------- #

    keys, vals = list( params.keys() ), list( params.values() )

    for key,val in zip( keys, vals ):

        key               = key.lower()
        category, subject = key.split( "." )
        
        if ( key.lower() == "xMajor.range" ):
