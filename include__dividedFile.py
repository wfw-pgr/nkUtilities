import os, sys, re

# use "<include> filepath = dat/xxx.conf" to include some file.


# ========================================================= #
# ===  include__dividedFile.py                          === #
# ========================================================= #

def include__dividedFile( inpFile=None, outFile=None, lines=None, \
                          comment_mark="#", include_mark="<include>", \
                          escapeType ="UseEscapeSequence" ):

    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    if ( lines is None ):
        if ( inpFile is None ):
            sys.exit( "[include__dividedFile.py] lines, inpFile == ???? [ERROR] " )
        else:
            with open( inpFile, "r" ) as f:
                lines = f.readlines()
    if ( type( lines ) is str ):
        lines = [ lines ]
        
    # ------------------------------------------------- #
    # --- [2] expression of definition              --- #
    # ------------------------------------------------- #
    vdict               = {}
    Flag__changeComment = False
    
    if ( comment_mark in [ "$", "*" ] ):  # --:: Need - Escape-Sequence ... ::-- #
        if   ( escapeType == "UseEscapeSequence" ):
            cmt      = "\\" + comment_mark
            expr_def = "{0}\s*{1}\s*filepath\s*=\s*(.*)".format( cmt, include_mark )
            
        elif ( escapeType == "ReplaceCommentMark" ):
            original     = comment_mark
            comment_mark = "#"
            Flag__changeComment = True
            expr_def     = "{0}\s*{1}\s*filepath\s*=\s*(.*)".format( comment_mark, include_mark )
            for ik,line in enumerate( lines ):
                lines[ik] = ( lines[ik] ).replace( original, comment_mark )

    else:
        expr_def     = "{0}\s*{1}\s*filepath\s*=\s*(.*)".format( comment_mark, include_mark )

        
    # ------------------------------------------------- #
    # --- [3] parse variables                       --- #
    # ------------------------------------------------- #

    stack = []
    while( True ):    # infinite loop

        if ( len(lines) == 0 ):
            break
        else:
            line   = lines.pop(0)
        stack += [line]
        
        # ------------------------------------------------- #
        # ---     search variable notation              --- #
        # ------------------------------------------------- #
        ret = re.search( expr_def, line )
        if ( ret ):      # Found.

            # ------------------------------------------------- #
            # --- [3-1] get file path                       --- #
            # ------------------------------------------------- #
            if ( comment_mark in ret.group(1) ):
                filepath = ( ( ( ret.group(1) ).split(comment_mark) )[0] ).strip()
            else:
                filepath = ( ret.group(1) ).strip()

            # ------------------------------------------------- #
            # --- [3-2] file existing check & load          --- #
            # ------------------------------------------------- #
            if ( os.path.exists( filepath ) ):
                with open( filepath, "r" ) as g:
                    inc = g.readlines()
                lines = inc + lines
            else:
                print( "[include__dividedFile.py] Cannot Find such a file.... [ERROR] " )
                print( "[include__dividedFile.py] filepath :: {} ".format( filepath   ) )

    # ------------------------------------------------- #
    # --- [4] return                                --- #
    # ------------------------------------------------- #
    if ( outFile is not None ):
        text = "".join( stack )
        with open( outFile, "w" ) as f:
            f.write( text )
        print( "[include__dividedFile.py] output :: {}".format( outFile ) )
    print( "[include__dividedFile.py] inserted lines is returned." + "\n" )
    return( stack )


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):

    # ------------------------------------------------- #
    # --- [1] define parametres                     --- #
    # ------------------------------------------------- #
    inpFile = "test/replace_sample.conf"
    outFile = "test/replace_sample.out"
    
    # ------------------------------------------------- #
    # --- [2] input / output Files                  --- #
    # ------------------------------------------------- #
    import nkUtilities.parse__arguments as par
    args = par.parse__arguments()
    if ( args["inpFile"] is not None ):
        inpFile = args["inpFile"]
    if ( args["outFile"] is not None ):
        outFile = args["outFile"]

    # ------------------------------------------------- #
    # --- [3] call replace variableDefinition       --- #
    # ------------------------------------------------- #
    ret   = include__dividedFile( inpFile=inpFile, outFile=outFile, comment_mark="$" )
    text  = "".join( ret )
    print( text )
