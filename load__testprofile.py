import numpy as np

# ========================================================= #
# ===  load test profile for instant checking           === #
# ========================================================= #
def load__testprofile( mode="2D", LI=101, LJ=51, LK=11, sigma=1.0, \
                       x1Min=-1.0, x1Max=+1.0, x2Min=-1.0, x2Max=+1.0, x3Min=-1.0, x3Max=+1.0, \
                       x1MinMaxNum=None, x2MinMaxNum=None, x3MinMaxNum=None, \
                       x1Axis=None, x2Axis=None, x3Axis=None, profile=None, \
                       returnType="point" ):
    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    if ( x1MinMaxNum is None ): x1MinMaxNum = [ x1Min, x1Max, LI ]
    if ( x2MinMaxNum is None ): x2MinMaxNum = [ x2Min, x2Max, LJ ]
    if ( x3MinMaxNum is None ): x3MinMaxNum = [ x3Min, x3Max, LK ]
    coef = 0.5 / sigma
    # ------------------------------------------------- #
    # --- [2] 1D ver.                               --- #
    # ------------------------------------------------- #
    if ( mode == "1D" ):
        print( "[load__testprofile] mode == 1D, (LI)    = ({0})"        .format( x1MinMaxNum[2]         ) )
        x1Axis       = np.linspace( x1MinMaxNum[0], x1MinMaxNum[1], x1MinMaxNum[2] )
        profile      = np.exp( - coef * ( x1Axis )**2 )
    if ( mode == "2D" ):
        print( "[load__testprofile] mode == 2D, (LI,LJ) = ({0},{1})"    .format( x1MinMaxNum[2], x2MinMaxNum[2]     ) )
        x1Axis       = np.linspace( x1MinMaxNum[0], x1MinMaxNum[1], x1MinMaxNum[2] )
        x2Axis       = np.linspace( x2MinMaxNum[0], x2MinMaxNum[1], x2MinMaxNum[2] )
        x1g,x2g      = np.meshgrid( x1Axis, x2Axis, indexing='ij' )
        profile      = np.exp( -coef * ( x1g**2 + x2g**2 ) )
    if ( mode == "3D" ):
        print( "[load__testprofile] mode == 3D, (LI,LJ) = ({0},{1},{2})".format( x1MinMaxNum[2], x2MinMaxNum[2], x3MinMaxNum[2] ) )
        x1Axis       = np.linspace( x1MinMaxNum[0], x1MinMaxNum[1], x1MinMaxNum[2] )
        x2Axis       = np.linspace( x2MinMaxNum[0], x2MinMaxNum[1], x2MinMaxNum[2] )
        x3Axis       = np.linspace( x3MinMaxNum[0], x3MinMaxNum[1], x3MinMaxNum[2] )
        x1g,x2g,x3g  = np.meshgrid( x1Axis, x2Axis, x3Axis, indexing='ij' )
        profile      = np.exp( -coef * ( x1g**2 + x2g**2 + x3g**2 ) )
    # ------------------------------------------------- #
    # --- [5] Return Results (point)                --- #
    # ------------------------------------------------- #
    if ( returnType.lower() == "point" ):
        if ( mode == "1D" ):
            ret      = np.zeros( (profile.size,2) )
            ret[:,0] = x1Axis
            ret[:,1] = profile
        if ( mode == "2D" ):
            ret      = np.zeros( (profile.size,3) )
            ret[:,0] =     x1g.reshape( (-1,) )
            ret[:,1] =     x2g.reshape( (-1,) )
            ret[:,2] = profile.reshape( (-1,) )
        if ( mode == "3D" ):
            ret      = np.zeros( (profile.size,4) )
            ret[:,0] =     x1g.reshape( (-1,) )
            ret[:,1] =     x2g.reshape( (-1,) )
            ret[:,2] =     x3g.reshape( (-1,) )
            ret[:,3] = profile.reshape( (-1,) )
    # ------------------------------------------------- #
    # --- [6] Return Results (dictionary)           --- #
    # ------------------------------------------------- #            
    if ( returnType.lower() == "dictionary" ):
        ret = { "x1Axis":x1Axis, "x2Axis":x2Axis, "x3Axis":x3Axis, "profile":profile }
    return( ret )

        
# ======================================== #
# ===  実行部                          === #
# ======================================== #
if ( __name__=="__main__" ):
    import myUtils.genArgs as gar
    args    = gar.genArgs()
    Data    = load__testprofile( mode="3D" )
    print( Data )
