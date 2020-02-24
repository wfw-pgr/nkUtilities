import os, sys
import numpy                       as np
import nkUtilities.equiSpaceGrid3D as esg

# ***************************************************************************** #
# *****  class Type                                                       ***** #
# ***************************************************************************** #
#
# ========================================================= #
# ===  generate Sample Profile                          === #
# ========================================================= #
class sampleProfile_Generator():
    # ========================================================= #
    # ===  initializer of the class                         === #
    # ========================================================= #
    def __init__( self, outFile=None, returnType ="point", nData      =1, \
                  x1MinMaxNum  =None, x2MinMaxNum=None   , x3MinMaxNum=None,
                  x1Min        =None, x2Min      =None   , x3Min      =None, \
                  LI           =None, LJ         =None   , LK         =None ):
        # ------------------------------------------------- #
        # --- [1] Arguments                             --- #
        # ------------------------------------------------- #
        if ( outFile is None ): outFile = "out.dat"
        if ( not( returnType.lower() in ["point","dictionary","tuple"] ) ):
            print( "[genSampleProfile] Arguments returnType == { 'point', 'dictionary', 'tuple' } " )
            return()
        if ( x1MinMaxNum is None ):
            if ( ( x1Min is not None ) and ( x1Max is not None ) and ( LI is not None ) ):
                x1MinMaxNum = [ x1Min, x1Max, LI ]
            else:
                sys.exit( "[genSampleProfile] x1MinMax==??? ( x1MinMaxNum ) or ( x1Min, x1Max, LI)" )
        if ( x2MinMaxNum is None ):
            if ( ( x2Min is not None ) and ( x2Max is not None ) and ( LJ is not None ) ):
                x2MinMaxNum = [ x2Min, x2Max, LJ ]
            else:
                sys.exit( "[genSampleProfile] x2MinMax==??? ( x2MinMaxNum ) or ( x2Min, x2Max, LJ)" )
        if ( x3MinMaxNum is None ):
            if ( ( x3Min is not None ) and ( x3Max is not None ) and ( LK is not None ) ):
                x3MinMaxNum = [ x3Min, x3Max, LK ]
            else:
                sys.exit( "[genSampleProfile] x3MinMax==??? ( x3MinMaxNum ) or ( x3Min, x3Max, LK)" )
        # ------------------------------------------------- #
        # --- [2] Arguments ==> self.variables          --- #
        # ------------------------------------------------- #
        self.outFile     = outFile
        self.returnType  = returnType
        self.nData       = nData
        self.x1MinMaxNum = x1MinMaxNum
        self.x2MinMaxNum = x2MinMaxNum
        self.x3MinMaxNum = x3MinMaxNum
        # ------------------------------------------------- #
        # --- [3] call generate Function                --- #
        # ------------------------------------------------- #
        self.generate__sampleProfile()
        
    # ========================================================= #
    # ===  function of the sample profile                   === #
    # ========================================================= #
    def sampleFunction( self, xyz=None, alpha=0.5 ):
        ret = np.exp( - 0.5 * alpha * ( xyz[:,0]**2 + xyz[:,1]**2 + xyz[:,2]**2 ) )
        return( ret )

    # ========================================================= #
    # ===  generate Sample Profile                          === #
    # ========================================================= #
    def generate__sampleProfile( self ):
        # ------------------------------------------------- #
        # --- [1] Sample Data Making                    --- #
        # ------------------------------------------------- #
        grid             = esg.equiSpaceGrid3D( x1MinMaxNum=self.x1MinMaxNum, x2MinMaxNum=self.x2MinMaxNum, \
                                                x3MinMaxNum=self.x3MinMaxNum, returnType =self.returnType   )
        nSize            = self.x1MinMaxNum[2] * self.x2MinMaxNum[2] * self.x3MinMaxNum[2]
        ret              = np.zeros( ( nSize, 3+self.nData ) )
        ret[:,0:3]       = grid[:,:]
        ret[:,  3]       = self.sampleFunction( xyz=grid )
        with open( self.outFile, "w") as f:
            f.write( "# xp yp zp phi\n" )
            f.write( "# {0} {1} {2} {3}\n".format( self.nData         , self.x1MinMaxNum[2], \
                                                   self.x2MinMaxNum[2], self.x3MinMaxNum[2] ) )
            np.savetxt( f, ret )


            
# ***************************************************************************** #
# *****  Function Type                                                    ***** #
# ***************************************************************************** #
#
# ========================================================= #
# ===  function of the sample profile                   === #
# ========================================================= #
def sampleFunction( xyz=None, alpha=0.5 ):
    ret = np.exp( - 0.5 * alpha * ( xyz[:,0]**2 + xyz[:,1]**2 + xyz[:,2]**2 ) )
    return( ret )

# ========================================================= #
# ===  generate Sample Profile                          === #
# ========================================================= #
def generate__sampleProfile( outFile    =None, returnType ="point", nData=1, \
                             x1MinMaxNum=None, x2MinMaxNum=None, x3MinMaxNum=None,
                             x1Min      =None, x2Min      =None, x3Min      =None, \
                             LI         =None, LJ         =None, LK         =None  ):
    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    if ( outFile is None ): outFile = "out.dat"
    if ( not( returnType.lower() in ["point","dictionary","tuple"] ) ):
        print( "[genSampleProfile] Arguments returnType == { 'point', 'dictionary', 'tuple' } " )
        return()
    if ( x1MinMaxNum is None ):
        if ( ( x1Min is not None ) and ( x1Max is not None ) and ( LI is not None ) ):
            x1MinMaxNum = [ x1Min, x1Max, LI ]
        else:
            sys.exit( "[genSampleProfile] x1MinMax==??? ( x1MinMaxNum ) or ( x1Min, x1Max, LI)" )
    if ( x2MinMaxNum is None ):
        if ( ( x2Min is not None ) and ( x2Max is not None ) and ( LJ is not None ) ):
            x2MinMaxNum = [ x2Min, x2Max, LJ ]
        else:
            sys.exit( "[genSampleProfile] x2MinMax==??? ( x2MinMaxNum ) or ( x2Min, x2Max, LJ)" )
    if ( x3MinMaxNum is None ):
        if ( ( x3Min is not None ) and ( x3Max is not None ) and ( LK is not None ) ):
            x3MinMaxNum = [ x3Min, x3Max, LK ]
        else:
            sys.exit( "[genSampleProfile] x3MinMax==??? ( x3MinMaxNum ) or ( x3Min, x3Max, LK)" )
    # ------------------------------------------------- #
    # --- [2] Sample Data Making                    --- #
    # ------------------------------------------------- #
    grid         = esg.equiSpaceGrid3D( x1MinMaxNum=x1MinMaxNum, x2MinMaxNum=x2MinMaxNum, \
                                        x3MinMaxNum=x3MinMaxNum, returnType ="point"      )
    nSize        = x1MinMaxNum[2] * x2MinMaxNum[2] * x3MinMaxNum[2]
    ret          = np.zeros( ( nSize, 3+nData ) )
    ret[:,0:3]   = grid[:,:]
    ret[:,  3]   = sampleFunction( xyz=grid )
    with open( outFile, "w") as f:
        f.write( "# xp yp zp phi\n" )
        f.write( "# {0} {1} {2} {3}\n".format( nData         , x1MinMaxNum[2], \
                                               x2MinMaxNum[2], x3MinMaxNum[2] ) )
        np.savetxt( f, ret )

    
# ======================================== #
# ===  実行部                          === #
# ======================================== #
if ( __name__=="__main__" ):

    run = "Function"
    
    # ------------------------------------------------- #
    # --- [1] Function Type Test                    --- #
    # ------------------------------------------------- #
    if ( run == "Function" ):
        x1MinMaxNum = [ 0.0, 1.0, 21 ]
        x2MinMaxNum = [ 0.0, 1.0, 21 ]
        x3MinMaxNum = [ 0.0, 1.0, 21 ]
        generate__sampleProfile( x1MinMaxNum=x1MinMaxNum, x2MinMaxNum=x2MinMaxNum, \
                                 x3MinMaxNum=x3MinMaxNum )

    # ------------------------------------------------- #
    # --- [2] Class Type Test                       --- #
    # ------------------------------------------------- #
    if ( run == "Class" ):
        x1MinMaxNum = [ 0.0, 1.0, 21 ]
        x2MinMaxNum = [ 0.0, 1.0, 21 ]
        x3MinMaxNum = [ 0.0, 1.0, 21 ]
        sampleProfile_Generator( x1MinMaxNum=x1MinMaxNum, x2MinMaxNum=x2MinMaxNum, \
                                 x3MinMaxNum=x3MinMaxNum )
