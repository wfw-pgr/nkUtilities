import sys
import numpy                     as np

# ========================================================= #
# ===  equi-partitioned Grid                            === #
# ========================================================= #
def equiSpaceGrid( dim=None, x1MinMaxNum=None, x2MinMaxNum=None, x3MinMaxNum=None, \
                   returnType="dictionary", DataOrder="ijk", silent=False ):
    
    # ------------------------------------------------- #
    # --- [1] Preparation of axis range             --- #
    # ------------------------------------------------- #
    
    if   ( x1MinMaxNum is None ):
        if ( not( silent ) ):
            print( "[equiSpaceGrid] x1MinMaxNum is not specified :: default :: [ 0.0, 1.0, 11 ] ")
            print( "[equiSpaceGrid] x2MinMaxNum is not specified :: default :: [ 0.0, 1.0, 11 ] ")
            print( "[equiSpaceGrid] x3MinMaxNum is not specified :: default :: [ 0.0, 1.0, 11 ] ")
            print( "[equiSpaceGrid] 3D grid will be returned...")
        dim         = 3
        
    elif ( x2MinMaxNum is None ):
        if ( not( silent ) ):
            print( "[equiSpaceGrid] dim == 1D " )
            print( "[equiSpaceGrid] x1MinMaxNum :: [ {0}, {1}, {2} ] ".format( x1MinMaxNum[0], x1MinMaxNum[1], x1MinMaxNum[2] ) )
        dim         = 1
        
    elif ( x3MinMaxNum is None ):
        if ( not( silent ) ):
            print( "[equiSpaceGrid] dim == 2D " )
            print( "[equiSpaceGrid] x1MinMaxNum :: [ {0}, {1}, {2} ] ".format( x1MinMaxNum[0], x1MinMaxNum[1], x1MinMaxNum[2] ) )
            print( "[equiSpaceGrid] x2MinMaxNum :: [ {0}, {1}, {2} ] ".format( x2MinMaxNum[0], x2MinMaxNum[1], x2MinMaxNum[2] ) )
        dim         = 2
        
    else:
        if ( not( silent ) ):
            print( "[equiSpaceGrid] dim == 3D " )
            print( "[equiSpaceGrid] x1MinMaxNum :: [ {0}, {1}, {2} ] ".format( x1MinMaxNum[0], x1MinMaxNum[1], x1MinMaxNum[2] ) )
            print( "[equiSpaceGrid] x2MinMaxNum :: [ {0}, {1}, {2} ] ".format( x2MinMaxNum[0], x2MinMaxNum[1], x2MinMaxNum[2] ) )
            print( "[equiSpaceGrid] x3MinMaxNum :: [ {0}, {1}, {2} ] ".format( x3MinMaxNum[0], x3MinMaxNum[1], x3MinMaxNum[2] ) )
        dim         = 3
        
    if ( x1MinMaxNum is None ): x1MinMaxNum = np.array( [ 0.0, 1.0, 11 ] )
    if ( x2MinMaxNum is None ): x2MinMaxNum = np.array( [ 0.0, 1.0, 11 ] )
    if ( x3MinMaxNum is None ): x3MinMaxNum = np.array( [ 0.0, 1.0, 11 ] )
        
    # ------------------------------------------------- #
    # --- [2] Axis Making                           --- #
    # ------------------------------------------------- #
    
    x1          = np.linspace( x1MinMaxNum[0], x1MinMaxNum[1], int( x1MinMaxNum[2] ) )
    x2          = np.linspace( x2MinMaxNum[0], x2MinMaxNum[1], int( x2MinMaxNum[2] ) )
    x3          = np.linspace( x3MinMaxNum[0], x3MinMaxNum[1], int( x3MinMaxNum[2] ) )
    
    if ( DataOrder == "kji" ):
        if ( dim == 1 ): xg1           = x1
        if ( dim == 2 ): xg1, xg2      = np.meshgrid( x1, x2,     indexing="ij" )
        if ( dim == 3 ): xg1, xg2, xg3 = np.meshgrid( x1, x2, x3, indexing="ij" )

    if ( DataOrder == "ijk" ):
        if ( dim == 1 ): xg1           = x1
        if ( dim == 2 ): xg2, xg1      = np.meshgrid( x2, x1,     indexing="ij" )
        if ( dim == 3 ): xg3, xg2, xg1 = np.meshgrid( x3, x2, x1, indexing="ij" )

    # ------------------------------------------------- #
    # --- [3] Return                                --- #
    # ------------------------------------------------- #
    
    if   ( returnType.lower() == "tuple"      ):
        if ( dim == 1 ): return(  xg1          )
        if ( dim == 2 ): return( (xg1,xg2    ) )
        if ( dim == 3 ): return( (xg1,xg2,xg3) )
        
    elif ( returnType.lower() == "dictionary" ):
        if ( dim == 1 ): return( { "xg1":xg1                       } )
        if ( dim == 2 ): return( { "xg1":xg1, "xg2":xg2            } )
        if ( dim == 3 ): return( { "xg1":xg1, "xg2":xg2, "xg3":xg3 } )
        
    elif ( returnType.lower() == "point"      ):
        if ( dim == 1 ):
            return( xg1 )
        if ( dim == 2 ):
            ret      = np.zeros( ( np.size( xg1 ), 2 ) )
            ret[:,0] = np.copy( xg1.reshape( -1, ) )
            ret[:,1] = np.copy( xg2.reshape( -1, ) )
            return( ret )
        if ( dim == 3 ):
            ret      = np.zeros( ( np.size( xg1 ), 3 ) )
            ret[:,0] = np.copy( xg1.reshape( -1, ) )
            ret[:,1] = np.copy( xg2.reshape( -1, ) )
            ret[:,2] = np.copy( xg3.reshape( -1, ) )
            return( ret )

    elif ( returnType.lower() == "structured" ):
        if ( DataOrder == "ijk" ):
            if ( dim == 1 ): arrs = np.array( [ xg1,          ] )
            if ( dim == 2 ): arrs = np.array( [ xg1, xg2,     ] )
            if ( dim == 3 ): arrs = np.array( [ xg1, xg2, xg3 ] )
            ret  = np.concatenate( [ arr[...,np.newaxis] for arr in arrs ], axis=-1  )
            return( ret )
        if ( DataOrder == "kji" ):
            if ( dim == 1 ): arrs = np.array( [ xg1,          ] )
            if ( dim == 2 ): arrs = np.array( [ xg1, xg2,     ] )
            if ( dim == 3 ): arrs = np.array( [ xg1, xg2, xg3 ] )
            ret  = np.concatenate( [ arr[np.newaxis,...] for arr in arrs ], axis= 0 )
            return( ret )


        
# ======================================== #
# ===  実行部                          === #
# ======================================== #
if ( __name__=="__main__" ):

    # ------------------------------------------------- #
    # --- [1] no argument                           --- #
    # ------------------------------------------------- #
    ret = equiSpaceGrid()
    print( ret["xg1"].shape )
    print( ret["xg2"].shape )
    print( ret["xg3"].shape )

    # ------------------------------------------------- #
    # --- [2] 1D test                               --- #
    # ------------------------------------------------- #
    returnType = "dictionary"
    x1MinMaxNum = [ 0.0, 1.0, 11 ]
    ret = equiSpaceGrid( x1MinMaxNum=x1MinMaxNum,  \
    	      		 returnType=returnType )
    print( ret["xg1"].shape )

    # ------------------------------------------------- #
    # --- [3] 2D test                               --- #
    # ------------------------------------------------- #
    returnType = "point"
    x1MinMaxNum = [ 0.0, 1.0, 11 ]
    x2MinMaxNum = [ 0.0, 1.0, 11 ]
    ret = equiSpaceGrid( x1MinMaxNum=x1MinMaxNum, x2MinMaxNum=x2MinMaxNum, \
    	      		 returnType=returnType )
    print( ret.shape )
    
    # ------------------------------------------------- #
    # --- [4] 3D test                               --- #
    # ------------------------------------------------- #
    returnType  = "tuple"
    x1MinMaxNum = [ 0.0, 1.0, 11 ]
    x2MinMaxNum = [ 0.0, 1.0, 11 ]
    x3MinMaxNum = [ 0.0, 1.0, 11 ]
    x1g,x2g,x3g = equiSpaceGrid( x1MinMaxNum=x1MinMaxNum, x2MinMaxNum=x2MinMaxNum, \
    	      		         x3MinMaxNum=x3MinMaxNum, returnType=returnType )
    print( x1g.shape )
    print( x2g.shape )
    print( x3g.shape )
