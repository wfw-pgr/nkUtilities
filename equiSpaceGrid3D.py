import numpy                     as np

# ========================================================= #
# ===  equiSpaceGrid3D                                  === #
# ========================================================= #
def equiSpaceGrid3D( LI   =None, LJ   =None, LK   =None, size =None, x1Range=None, x2Range=None, x3Range=None, \
                     x1Min=None, x1Max=None, x2Min=None, x2Max=None, x3Min  =None, x3Max  =None, \
                     x1MinMaxNum=None, x2MinMaxNum=None, x3MinMaxNum=None, \
                     returnType="Dictionary", DataOrder="ijk" ):
    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    if ( size  is not None ): LI, LJ, LK = size
    if ( LI        is None ): LI         = 11
    if ( LJ        is None ): LJ         = 11
    if ( LK        is None ): LK         = 11
    if ( x1Range   is None ): x1Range    = [0.,1.]
    if ( x2Range   is None ): x2Range    = [0.,1.]
    if ( x3Range   is None ): x3Range    = [0.,1.]
    if ( x1Min is not None ): x1Range[0] = x1Min
    if ( x2Min is not None ): x2Range[0] = x2Min
    if ( x3Min is not None ): x3Range[0] = x3Min
    if ( x1Max is not None ): x1Range[1] = x1Max
    if ( x2Max is not None ): x2Range[1] = x2Max
    if ( x3Max is not None ): x3Range[1] = x3Max
    if ( x1MinMaxNum is None ):
        x1MinMaxNum = np.array( [ x1Range[0], x1Range[1], LI ] )
    if ( x2MinMaxNum is None ):
        x2MinMaxNum = np.array( [ x2Range[0], x2Range[1], LJ ] )
    if ( x3MinMaxNum is None ):
        x3MinMaxNum = np.array( [ x3Range[0], x3Range[1], LK ] )
    # ------------------------------------------------- #
    # --- [2] Axis                                  --- #
    # ------------------------------------------------- #
    x1          = np.linspace( x1MinMaxNum[0], x1MinMaxNum[1], int( x1MinMaxNum[2] ) )
    x2          = np.linspace( x2MinMaxNum[0], x2MinMaxNum[1], int( x2MinMaxNum[2] ) )
    x3          = np.linspace( x3MinMaxNum[0], x3MinMaxNum[1], int( x3MinMaxNum[2] ) )
    if ( DataOrder == "kji" ):
        xg1,xg2,xg3 = np.meshgrid( x1, x2, x3, indexing="ij" )
    if ( DataOrder == "ijk" ):
        xg3,xg2,xg1 = np.meshgrid( x3, x2, x1, indexing="ij" )
    # ------------------------------------------------- #
    # --- [3] Return                                --- #
    # ------------------------------------------------- #
    if   ( returnType.lower() == "tuple"      ):
        return( (xg1,xg2,xg3) )
    elif ( returnType.lower() == "dictionary" ):
        return( { "xg1":xg1, "xg2":xg2, "xg3":xg3 } )
    elif ( returnType.lower() == "point"      ):
        ret      = np.zeros( ( np.size( xg1 ), 3 ) )
        ret[:,0] = np.copy( xg1.reshape( -1, ) )
        ret[:,1] = np.copy( xg2.reshape( -1, ) )
        ret[:,2] = np.copy( xg3.reshape( -1, ) )
        return( ret )


# ======================================== #
# ===  実行部                          === #
# ======================================== #
if ( __name__=="__main__" ):
    ret = equiSpaceGrid3D( x1Range=[-1.0,1.0], x2Range=[0.0,1.0], x3Range=[0.0,1.0], LI=201, LJ=101, LK=11, \
                           returnType="dictionary" )
    print( ret["xg1"].shape )
    print( ret["xg2"].shape )
    print( ret["xg3"].shape )
