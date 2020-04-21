import sys
import numpy as np


# ========================================================= #
# ===  save point File with prescribed header           === #
# ========================================================= #

def save__pointFile( outFile=None, Data=None, names=None, size=None, ndim=None, \
                     shape=None ):
    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    if ( Data    is None ): sys.exit( "[save__pointFile] Data    == ???" )
    if ( outFile is None ): outFile = "out.dat"
    if ( ndim    is None ): ndim    = Data.ndim
    if ( size    is None ): size    = Data.shape
    if ( ndim > 2        ): sys.exit( "[save__pointFile] Data.ndim > 2"  )
    if ( names   is None ):
        if   ( ndim == 1 ):
            names   = [ "x1" ]
        elif ( ndim == 2 ):
            names   = [ "x{0}".format(i+1) for i in range( size[1] ) ]
    if ( shape is not None ):
        prod = 1
        for i in shape:
            prod = prod * i
        if ( prod != np.size( Data ) ):
            print( "[save__pointFile] shape and size are inconsistent [ERROR] " )
            print( "[save__pointFile] shape :: {0} ".format( shape )  )
            print( "[save__pointFile] size  :: {0} ".format( size  )  )
            sys.exit()
            
    # ------------------------------------------------- #
    # --- [2] save Data with header                 --- #
    # ------------------------------------------------- #
    with open( outFile, "w" ) as f:
        f.write( "# " + " ".join( names ) + "\n" )
        f.write( "# " + " ".join( [ str(i) for i in size ] ) + "\n" )
        if ( shape is not None ):
            f.write( "# " + " ".join( [str(i) for i in shape] ) + "\n" )
        np.savetxt( f, Data )
    print( "[save__pointFile] output :: {0} ".format( outFile ) )
    return()




# ======================================== #
# ===  実行部                          === #
# ======================================== #
if ( __name__=="__main__" ):

    outFile ="output.dat"
    import nkUtilities.equiSpaceGrid3D as esg
    LI, LJ, LK  = 11, 11, 11
    x1MinMaxNum = [0.0,   1.0, LI]
    x2MinMaxNum = [0.0,  10.0, LJ]
    x3MinMaxNum = [0.0, 100.0, LK]
    Data        = esg.equiSpaceGrid3D( x1MinMaxNum=x1MinMaxNum, x2MinMaxNum=x2MinMaxNum, \
                                       x3MinMaxNum=x3MinMaxNum, returnType="point" )
    
    save__pointFile( outFile=outFile, Data=Data, shape=[LK,LJ,LI,3] )
