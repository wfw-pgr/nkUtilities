import numpy as np

# ========================================================= #
# ===  load fortran binary file                         === #
# ========================================================= #

def load__fortranBinary( inpFile=None, shape=(-1,), datatype="float" ):

    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    if ( inpFile is None ): sys.exit( "[load__fortranBinary.py] inpFile == ??? " )

    # ------------------------------------------------- #
    # --- [2] load fortran Binary file              --- #
    # ------------------------------------------------- #
    import scipy.io as io
    with io.FortranFile( inpFile, mode="r" ) as f:
        if   ( datatype.lower() in ["float","double","real"] ):
            data = f.read_reals( float )
        elif ( datatype.lower() in ["int","integer","long"] ):
            data = f.read_ints( np.int32 )

    # ------------------------------------------------- #
    # --- [3] reshape data                          --- #
    # ------------------------------------------------- #

    dshape = data.shape
    
    if   ( shape == (-1,) ):
        ret = data
    elif ( np.abs( np.prod( np.array( shape ) ) ) == data.shape[0]  ):
        ret = data.reshape( shape )
    else:
        print( "[load__fortranBinary.py] shape is incompatible with Data.shape !!! ERROR !!! " )
        print( "[load__fortranBinary.py] shape      == {0} ".format( shape      ) )
        print( "[load__fortranBinary.py] data.shape == {0} ".format( data.shape ) )
        print()
        sys.exit()

    # ------------------------------------------------- #
    # --- [4] return                                --- #
    # ------------------------------------------------- #
    return( ret )

# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #

if ( __name__=="__main__" ):
    inpFile = "dat/out.bin"
    shape   = (1,31,41,4)
    Data    = load__fortranBinary( inpFile=inpFile, shape=shape )

    Data    = Data.reshape( (-1,4) )
    
    import nkUtilities.load__config   as lcf
    import nkUtilities.cMapTri        as cmt
    config  = lcf.load__config()
    pngFile = "png/out.png"
    config["xTitle"]         = "X (m)"
    config["yTitle"]         = "Y (m)"
    config["cmp_xAutoRange"] = True
    config["cmp_yAutoRange"] = True

    cmt.cMapTri( xAxis=Data[:,0], yAxis=Data[:,1], cMap=Data[:,3], \
                 pngFile=pngFile, config=config )

