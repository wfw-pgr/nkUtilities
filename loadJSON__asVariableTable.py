import os, sys, re, json5
import numpy as np
import nkUtilities.json__formulaParser as jso

# ========================================================= #
# ===  loadJSON__asVariableTable.py                     === #
# ========================================================= #

def loadJSON__asVariableTable( inpFile=None, outFile=None, lines=None, table=None, \
                               loadJSON_mark="<loadJSON>", comment_mark="#", \
                               escapeType="UseEscapeSequence" ):
    
    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    if ( lines is None ):
        if ( inpFile is None ):
            sys.exit( "[loadJSON__asVariableTable.py] lines, inpFile == ???? [ERROR] " )
        else:
            with open( inpFile, "r" ) as f:
                lines = f.readlines()
    if ( type( lines ) is str ):
        lines = [ lines ]
        
    # ------------------------------------------------- #
    # --- [2] expression of definition              --- #
    # ------------------------------------------------- #
    vdict = {}
    if ( table is not None ):
        vdict = { **table, **vdict }
        
    if ( comment_mark in [ "$", "*" ] ):  # --:: Need - Escape-Sequence ... ::-- #
        if   ( escapeType == "UseEscapeSequence" ):
            cmt      = "\\" + comment_mark
            expr_def = "{0}\s*{1}\s*filepath\s=\s*(.*)".format( cmt, loadJSON_mark )
            
        elif ( escapeType == "ReplaceCommentMark" ):
            original     = comment_mark
            comment_mark = "#"
            Flag__changeComment = True
            expr_def     = "{0}\s*{1}\s*filepath\s*=\s*(.*)".format( comment_mark, loadJSON_mark )
            for ik,line in enumerate( lines ):
                lines[ik] = ( lines[ik] ).replace( original, comment_mark )

    else:
        expr_def     = "{0}\s*{1}\s*filepath\s*=\s*(.*)".format( comment_mark, loadJSON_mark )

        
    # ------------------------------------------------- #
    # --- [3] parse variables                       --- #
    # ------------------------------------------------- #
    for line in lines:
        
        # ------------------------------------------------- #
        # ---     search <loadJSON> notation            --- #
        # ------------------------------------------------- #
        ret = re.match( expr_def, line )
        if ( ret ):         # Found
            
            # ------------------------------------------------- #
            # --- [3-1] get file path                       --- #
            # ------------------------------------------------- #
            if ( comment_mark in ret.group(1) ):
                filepath = ( ( ( ret.group(1) ).split(comment_mark) )[0] ).strip()
            else:
                filepath = ( ret.group(1) ).strip()
            filepath = filepath.strip( " "+'"'+"'" )

            # ------------------------------------------------- #
            # --- [3-2] file existing check & load          --- #
            # ------------------------------------------------- #
            if ( os.path.exists( filepath ) ):
                vdict = jso.json__formulaParser( inpFile=filepath, table=vdict )
            else:
                print( "[loadJSON__asVariableTable.py] Cannot Find such a file.... [ERROR] " )
                print( "[loadJSON__asVariableTable.py] filepath :: {} ".format( filepath   ) )
                sys.exit()

    # ------------------------------------------------- #
    # --- [4] return                                --- #
    # ------------------------------------------------- #
    if ( outFile is not None ):
        with open( outFile, "w" ) as g:
            json5.dump( vdict, g )
            print( "[loadJSON__asVariableTable.py] output :: {}".format( outFile ) )
    return( vdict )


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    inpFile       = "cnf/sample_parameter.inp"
    comment_mark  = "$"
    ret           = loadJSON__asVariableTable( inpFile=inpFile, comment_mark=comment_mark )
    print( ret )
