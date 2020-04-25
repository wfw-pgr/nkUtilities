import numpy                     as np
import nkUtilities.equiSpaceGrid as esg

# ========================================================= #
# ===  generate test profile for instant checking       === #
# ========================================================= #
def generate__testprofile( dim=None, x1MinMaxNum=None, x2MinMaxNum=None, x3MinMaxNum=None, \
                           vMin=0.0, vMax=1.0, returnType="point", profileType="cos**2" ):
    
    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    if   ( x1MinMaxNum is None ):
        print( "[generate__testprofile] no (x1,x2,x3)MinMaxNum is specified " )
        print( "                        :: Default => dim = 2D, [ 0.0, 1.0, 11 ] " )
        dim         = 2
        x1MinMaxNum = [ 0.0, 1.0, 21 ]
        x2MinMaxNum = [ 0.0, 1.0, 21 ]
    elif ( x2MinMaxNum is None ):
        dim         = 1
    elif ( x3MinMaxNum is None ):
        dim         = 2
    else:
        dim         = 3

    if ( dim == 1 ):
        MaxLength = max( abs(x1MinMaxNum[0]), abs(x1MinMaxNum[1])  )
    if ( dim == 2 ):
        MaxLength = max( abs(x1MinMaxNum[0]), abs(x1MinMaxNum[1]), \
                         abs(x2MinMaxNum[0]), abs(x2MinMaxNum[1])  )
    if ( dim == 3 ):
        MaxLength = max( abs(x1MinMaxNum[0]), abs(x1MinMaxNum[1]), \
                         abs(x2MinMaxNum[0]), abs(x2MinMaxNum[1]), \
                         abs(x3MinMaxNum[0]), abs(x3MinMaxNum[1])  )
        
    # ------------------------------------------------- #
    # --- [2] 1D ver.                               --- #
    # ------------------------------------------------- #
    if ( dim == 1 ):
        print( "[generate__testprofile]  dim == 1D, (LI)    = ({0})"           .format( x1MinMaxNum[2]                                 ) )
        x1g          = esg.equiSpaceGrid( x1MinMaxNum=x1MinMaxNum, returnType="tuple" )
        rhat         = x1g / MaxLength * 0.5 * np.pi
        if ( profileType == "cos**2" ):
            profile      = ( vMax-vMin ) * ( np.cos( rhat ) )**2 + vMin
    if ( dim == 2 ):
        print( "[generate__testprofile]  dim == 2D, (LI,LJ) = ({0},{1})"       .format( x1MinMaxNum[2], x2MinMaxNum[2]                 ) )
        x1g,x2g      = esg.equiSpaceGrid( x1MinMaxNum=x1MinMaxNum, x2MinMaxNum=x2MinMaxNum, returnType="tuple" )
        rhat         = np.sqrt( x1g**2 + x2g**2 ) / MaxLength * 0.5 * np.pi 
        if ( profileType == "cos**2" ):
            profile      = ( vMax-vMin ) * ( np.cos( rhat ) )**2 + vMin
    if ( dim == 3 ):
        print( "[generate__testprofile]  dim == 3D, (LI,LJ,LK) = ({0},{1},{2})".format( x1MinMaxNum[2], x2MinMaxNum[2], x3MinMaxNum[2] ) )
        x1g,x2g,x3g  = esg.equiSpaceGrid( x1MinMaxNum=x1MinMaxNum, x2MinMaxNum=x2MinMaxNum, x3MinMaxNum=x3MinMaxNum, returnType="tuple" )
        rhat         = np.sqrt( x1g**2 + x2g**2 + x3g**2 ) / MaxLength * 0.5 * np.pi 
        if ( profileType == "cos**2" ):
            profile      = ( vMax-vMin ) * ( np.cos( rhat ) )**2 + vMin
        
    # ------------------------------------------------- #
    # --- [5] Return Results (point)                --- #
    # ------------------------------------------------- #
    if ( returnType.lower() == "point" ):
        if ( dim == 1 ):
            ret      = np.zeros( (profile.size,2) )
            ret[:,0] = x1g
            ret[:,1] = profile
        if ( dim == 2 ):
            ret      = np.zeros( (profile.size,3) )
            ret[:,0] =     x1g.reshape( (-1,) )
            ret[:,1] =     x2g.reshape( (-1,) )
            ret[:,2] = profile.reshape( (-1,) )
        if ( dim == 3 ):
            ret      = np.zeros( (profile.size,4) )
            ret[:,0] =     x1g.reshape( (-1,) )
            ret[:,1] =     x2g.reshape( (-1,) )
            ret[:,2] =     x3g.reshape( (-1,) )
            ret[:,3] = profile.reshape( (-1,) )

    # ------------------------------------------------- #
    # --- [6] Return Results (dictionary)           --- #
    # ------------------------------------------------- #            
    if ( returnType.lower() == "dictionary" ):
        if ( dim == 1 ):
            ret = { "x1g":x1g,                       "profile":profile }
        if ( dim == 2 ):
            ret = { "x1g":x1g, "x2g":x2g,            "profile":profile }
        if ( dim == 3 ):
            ret = { "x1g":x1g, "x2g":x2g, "x3g":x3g, "profile":profile }

    # ------------------------------------------------- #
    # --- [7] Return Results (structured)           --- #
    # ------------------------------------------------- #
    if ( returnType.lower() == "structured" ):
        if ( dim == 1 ): arrs = np.array( [ x1g,           profile ] )
        if ( dim == 2 ): arrs = np.array( [ x1g, x2g,      profile ] )
        if ( dim == 3 ): arrs = np.array( [ x1g, x2g, x3g, profile ] )
        ret  = np.concatenate( [ arr[...,np.newaxis] for arr in arrs ], axis=-1 )

    # ------------------------------------------------- #
    # --- [8] Return Results (tuple)                --- #
    # ------------------------------------------------- #
    if ( returnType.lower() == "tuple"      ):
        if ( dim == 1 ): ret  = (x1g,        profile)
        if ( dim == 2 ): ret  = (x1g,x2g,    profile)
        if ( dim == 3 ): ret  = (x1g,x2g,x3g,profile)
        
    return( ret )

        
# ======================================== #
# ===  実行部                          === #
# ======================================== #
if ( __name__=="__main__" ):
    returnType  = "structured"
    x1MinMaxNum = [ -2.0, 2.0, 21 ]
    x2MinMaxNum = [ -2.0, 2.0, 31 ]
    x3MinMaxNum = [ -2.0, 2.0, 41 ]
    Data        = generate__testprofile( x1MinMaxNum=x1MinMaxNum, x2MinMaxNum=x2MinMaxNum, \
                                         x3MinMaxNum=x3MinMaxNum, returnType=returnType )
    import nkUtilities.save__pointFile as spf
    spf.save__pointFile( outFile="out.dat", Data=Data )
    # import nkUtilities.cMapTri as cmt
    # cmt.cMapTri( xAxis=Data[:,0], yAxis=Data[:,1], cMap=Data[:,2], pngFile="out.png" )
