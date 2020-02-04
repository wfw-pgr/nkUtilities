import numpy                     as np

# ========================================================= #
# ===  equiSpaceGrid2D                                  === #
# ========================================================= #
def equiSpaceGrid2D( LI   =None, LJ=None, size=None, x1Range=None, x2Range=None, \
                     x1Min=None, x1Max=None, x2Min=None, x2Max=None, x1MinMaxNum=None, x2MinMaxNum=None, \
                     returnType="Dictionary" ):
    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    if ( size  is not None ): LI, LJ     = size
    if ( LI        is None ): LI         = 101
    if ( LJ        is None ): LJ         = 101
    if ( x1Range   is None ): x1Range    = [0.,1.]
    if ( x2Range   is None ): x2Range    = [0.,1.]
    if ( x1Min is not None ): x1Range[0] = x1Min
    if ( x2Min is not None ): x2Range[0] = x2Min
    if ( x1Max is not None ): x1Range[1] = x1Max
    if ( x2Max is not None ): x2Range[1] = x2Max
    if ( x1MinMaxNum is None ):
        x1MinMaxNum = np.array( [ x1Range[0], x1Range[1], LI ] )
    if ( x2MinMaxNum is None ):
        x2MinMaxNum = np.array( [ x2Range[0], x2Range[1], LJ ] )
    # ------------------------------------------------- #
    # --- [2] Axis                                  --- #
    # ------------------------------------------------- #
    x1      = np.linspace( x1MinMaxNum[0], x1MinMaxNum[1], int( x1MinMaxNum[2] ) )
    x2      = np.linspace( x2MinMaxNum[0], x2MinMaxNum[1], int( x2MinMaxNum[2] ) )
    xg1,xg2 = np.meshgrid( x1, x2, indexing="ij" )
    # ------------------------------------------------- #
    # --- [3] Return                                --- #
    # ------------------------------------------------- #
    if   ( returnType.lower() == "tuple"      ):
        return( (xg1,xg2) )
    elif ( returnType.lower() == "dictionary" ):
        return( { "xg1":xg1, "xg2":xg2 } )
    elif ( returnType.lower() == "point"      ):
        ret      = np.zeros( ( np.size( xg1 ), 2 ) )
        ret[:,0] = np.copy( xg1.reshape( -1, ) )
        ret[:,1] = np.copy( xg2.reshape( -1, ) )
        return( ret )


# ======================================== #
# ===  実行部                          === #
# ======================================== #
if ( __name__=="__main__" ):
    ret = equiSpaceGrid2D( x1Range=[-1.0,1.0], x2Range=[0.0,1.0], LI=201, LJ=101, returnType="dictionary" )
    print( ret["xg1"].shape )
    print( ret["xg2"].shape )
