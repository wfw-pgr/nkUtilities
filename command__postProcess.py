import os, sys, re, subprocess

# ========================================================= #
# ===  command__postProcess.py                          === #
# ========================================================= #

def command__postProcess( inpFile=None, lines=None, comment_mark="#", execute=True, \
                          postProcess_mark="<postProcess>", escapeType ="UseEscapeSequence" ):

    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    if ( lines is None ):
        if ( inpFile is None ):
            sys.exit( "[command__postProcess.py] lines, inpFile == ???? [ERROR] " )
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
            expr_def = "{0}\s*{1}\s*(.*)".format( cmt, postProcess_mark )
            
        elif ( escapeType == "ReplaceCommentMark" ):
            original     = comment_mark
            comment_mark = "#"
            Flag__changeComment = True
            expr_def     = "{0}\s*{1}\s*(.*)".format( comment_mark, postProcess_mark )
            for ik,line in enumerate( lines ):
                lines[ik] = ( lines[ik] ).replace( original, comment_mark )

    else:
        expr_def     = "{0}\s*{1}\s*(.*)".format( comment_mark, postProcess_mark )

        
    # ------------------------------------------------- #
    # --- [3] parse variables                       --- #
    # ------------------------------------------------- #

    stack = []
    for ik,line in enumerate(lines):   # 1-line, 1-argument.

        # ------------------------------------------------- #
        # ---     search variable notation              --- #
        # ------------------------------------------------- #
        ret = re.match( expr_def, line )
        if ( ret ):      # Found.
            
            # ------------------------------------------------- #
            # --- [3-1] get file path                       --- #
            # ------------------------------------------------- #
            if ( comment_mark in [ "$", "*"] ):   # exception for "$" and "*"
                comment_mark_ = comment_mark*2
            else:
                comment_mark_ = comment_mark

            if ( comment_mark_ in ret.group(1) ):
                command = ( ( ( ret.group(1) ).split(comment_mark_) )[0] ).strip()
            else:
                command = ( ret.group(1) ).strip()

            # ------------------------------------------------- #
            # --- [3-2] stack commands                      --- #
            # ------------------------------------------------- #
            stack += [command]

    # ------------------------------------------------- #
    # --- [4] execute & return                      --- #
    # ------------------------------------------------- #
    for command in stack:
        print( command )
        subprocess.run( command, shell=True )
    print( "[command__postProcess.py] command list is returned." + "\n" )
    return( stack )


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):

    # ------------------------------------------------- #
    # --- [1] define parametres                     --- #
    # ------------------------------------------------- #
    inpFile = "test/replace_sample.conf"
    
    # ------------------------------------------------- #
    # --- [2] input / output Files                  --- #
    # ------------------------------------------------- #
    import nkUtilities.parse__arguments as par
    args = par.parse__arguments()
    if ( args["inpFile"] is not None ):
        inpFile = args["inpFile"]

    # ------------------------------------------------- #
    # --- [3] call replace variableDefinition       --- #
    # ------------------------------------------------- #
    ret   = command__postProcess( inpFile=inpFile, comment_mark="$" )
    print( "\n", ret )
