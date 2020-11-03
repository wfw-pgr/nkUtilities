import numpy as np

# ========================================================= #
# ===  pileup Arr ( join multiple arrays into 1 )       === #
# ========================================================= #
def pileupArr( arrs, NoNewAxis=False, axis=0, hint=False ):
    if ( hint is True ):
        print( "pileupArr( (v1,v2,v3,...), NoNewAxis=(True/False), axis=0 )" )
    if ( NoNewAxis ):
        return( np.concatenate( [ arr for arr in arrs], axis=axis ) )
    else:
        return( np.concatenate( [ arr[np.newaxis,:] for arr in arrs ], axis=0 ) )

    
