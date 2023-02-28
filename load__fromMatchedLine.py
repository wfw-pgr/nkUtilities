import os, sys, re
import numpy as np


# ========================================================= #
# ===  load__fromMatchedLine.py                         === #
# ========================================================= #

def load__fromMatchedLine( inpFile=None, outFile=None, midFile="data.mid",  \
                           startLine=None, endLine=None, endLineType="empty" ):

    # ------------------------------------------------- #
    # --- [1] arguments                             --- #
    # ------------------------------------------------- #
    if ( startLine   is None ): sys.exit( "[load__fromMatchedLine.py] startLine == ???" )
    if ( inpFile     is None ): sys.exit( "[load__fromMatchedLine.py] inpFile   == ???" )
    if ( endLine is not None ):
        endLineType = "endLine"
    else:
        if ( endLineType.lower() in [ "empty", "eof" ] ):
            pass
        else:
            print( "[load__fromMatchedLineLine.py] endLineType == {} ??? ".format( endLineType ) )
            sys.exit()

    # ------------------------------------------------- #
    # --- [2] find start Line                       --- #
    # ------------------------------------------------- #
    with open( inpFile, "r" ) as f:
        lines = f.readlines()
        
    matched = False
    for ik,line in enumerate( lines ):
        if ( re.search( startLine, line ) ):
            lfrom   = ik+1
            matched = True
            break
        
    if ( not( matched ) ):
        print( "[load__fromMatchedLine.py] startLine does not matched.... " )
        return( None )

    # ------------------------------------------------- #
    # --- [3] find  end Line                        --- #
    # ------------------------------------------------- #
    matched = False
    if ( endLineType.lower() == "endline" ):
        for ik,line in enumerate( lines[lfrom:] ):
            if ( re.match( endLine, line ) ):
                lupto   = lfrom + ik
                matched = True
                break
        if ( not( matched ) ):
            print( "[load__fromMatchedLine.py] endLine does not matched.... " )
            sys.exit()

    if ( endLineType.lower() == "empty" ):
        for ik,line in enumerate( lines[lfrom:] ):
            if ( len( line.strip() ) == 0 ):
                lupto   = lfrom + ik
                matched = True
                break
        if ( not( matched ) ):
            lupto = len( lines )
            matched = True

    if ( endLineType.lower() == "eof" ):
        lupto   = len( lines )
        matched = True

    # ------------------------------------------------- #
    # --- [4] return fetched data                   --- #
    # ------------------------------------------------- #
    lines   = "".join( lines[ lfrom:lupto ] )
    with open( midFile, "w" ) as f:
        f.write( lines )
    with open( midFile, "r" ) as f:
        Data  = np.loadtxt( f )
    os.remove( midFile )

    # ------------------------------------------------- #
    # --- [5] save in a file                        --- #
    # ------------------------------------------------- #
    if ( outFile is not None ):
        import nkUtilities.save__pointFile as spf
        spf.save__pointFile( outFile=outFile, Data=Data )
    return( Data )


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):

    inpFile   = "dat/test.dat"
    startLine = r"# read from this line"
    endLine   = r"# read upto this line"

    test_generate = False
    
    if ( test_generate ):
        import nkUtilities.equiSpaceGrid as esg
        x1MinMaxNum = [ 0.0, 1.0, 11 ]
        x2MinMaxNum = [ 0.0, 1.0, 11 ]
        x3MinMaxNum = [ 0.0, 1.0, 11 ]
        coord       = esg.equiSpaceGrid( x1MinMaxNum=x1MinMaxNum, x2MinMaxNum=x2MinMaxNum, \
                                         x3MinMaxNum=x3MinMaxNum, returnType = "point" )
        import nkUtilities.save__pointFile as spf
        spf.save__pointFile( outFile=inpFile, Data=coord )


    # ------------------------------------------------- #
    # --- [2] test                                  --- #
    # ------------------------------------------------- #
    ret = load__fromMatchedLine( inpFile=inpFile, startLine=startLine )
    if ( ret is not None ):
        print( ret.shape )
        
    ret = load__fromMatchedLine( inpFile=inpFile, startLine=startLine, endLine=endLine )
    if ( ret is not None ):
        print( ret.shape )

    ret = load__fromMatchedLine( inpFile=inpFile, startLine=startLine, endLineType="empty" )
    if ( ret is not None ):
        print( ret.shape )

    ret = load__fromMatchedLine( inpFile=inpFile, startLine=startLine, endLineType="EOF" )
    if ( ret is not None ):
        print( ret.shape )
