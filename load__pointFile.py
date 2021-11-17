import os, sys
import numpy as np


# ========================================================= #
# ===  load point file with prescribed header           === #
# ========================================================= #

def load__pointFile( inpFile=None, returnType="point", shape=None, order="C", readHeader=True ):

    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    names, size = None, None
    if ( inpFile is None ): sys.exit( "[load__pointFile] inpFile   == ??? " )

    # ------------------------------------------------- #
    # --- [2] load Data with header                 --- #
    # ------------------------------------------------- #
    with open( inpFile, "r" ) as f:
        line1 = f.readline()
        line2 = f.readline()
        line3 = f.readline()
    with open( inpFile, "r" ) as f:
        Data  = np.loadtxt( f )

    # ------------------------------------------------- #
    # --- [3] names & size                          --- #
    # ------------------------------------------------- #
    if ( readHeader ):
        if ( ( ( line1.strip() )[0] == "#" ) and ( ( line2.strip() )[0] == "#" ) and \
             ( ( line3.strip() )[0] == "#" ) ):
            ext1  = ( ( ( line1.strip() ).strip( "#" ) ).strip() ).split()
            ext2  = ( ( ( line2.strip() ).strip( "#" ) ).strip() ).split()
            ext3  = ( ( ( line3.strip() ).strip( "#" ) ).strip() ).split()

            try:
                names = [ str(s) for s in ext1 ]
            except:
                names = [ "x{0}".format(ik) for ik in range( nComponents ) ]

            try:
                size  = [ int(i) for i in ext2 ]
            except:
                size  = Data.shape
                    
            try:
                shape = [ int(i) for i in ext3 ]
            except:
                if ( returnType.lower() == "structured" ):
                    print( "[load__pointFile.py] [WARNING] returnType == structured , but, specification is wrong. " )
                shape = Data.shape
    else:
        size        = Data.shape
        shape       = Data.shape
        if ( Data.ndim == 1 ):
            nComponents = 1
        else:
            nComponents = Data.shape[1]
        names = [ "x{0}".format(ik) for ik in range( nComponents ) ]
            
    # ------------------------------------------------- #
    # --- [4] return                                --- #
    # ------------------------------------------------- #
    if   ( returnType.lower() == "point" ):
        ret   = Data
    elif ( returnType.lower() == "dict"  ):
        ret   = {}
        ret["size"] = size
        for ik,name in enumerate( names ):
            ret[name] = np.ravel( Data[:,ik] )
    elif ( returnType.lower() == "structured"  ):
        if ( shape is None ):
            sys.exit( "[load__pointFile] returnType == structured :: but No Shape information [Error]" )
        if ( np.prod( shape ) != np.size( Data ) ):
            print( "[save__pointFile] shape and size are inconsistent [ERROR] " )
            print( "[save__pointFile] shape :: {0} ".format( shape      ) )
            print( "[save__pointFile] size  :: {0} ".format( Data.shape ) )
            sys.exit()
        ret   = np.reshape( Data, shape, order=order )
    elif ( returnType.lower() == "info" ):
        ret = { "names":names, "shape":shape, "size":size }
    else:
        sys.exit( "[load__pointFile] returnType = ( point, dict )" )
    return( ret )


# ======================================== #
# ===  実行部                          === #
# ======================================== #
if ( __name__=="__main__" ):

    inpFile = "output.dat"
    
    Data = load__pointFile( inpFile=inpFile, returnType="structured" )
    print( Data.shape )
    print( Data[0,0,:,0] )
