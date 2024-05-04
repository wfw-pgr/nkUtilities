#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-

import os, sys, re, subprocess

# ========================================================= #
# ===  command__postProcess.py                          === #
# ========================================================= #

def command__postProcess( inpFile=None, lines=None, comment_mark="#", execute=True, \
                          verbose__command=True, silent=True, \
                          postProcess_mark="<postProcess>", escapeType ="UseEscapeSequence" ):

    replace__mark = "#"

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
    if ( comment_mark in [ "$", "*"] ):   # exception for "$" and "*"
        comment_mark_ = comment_mark*2
    else:
        comment_mark_ = comment_mark
        
    # ------------------------------------------------- #
    # --- [2] expression of definition              --- #
    # ------------------------------------------------- #
    vdict               = {}
    if ( comment_mark in [ "$", "*" ] ):  # --:: Need - Escape-Sequence ... ::-- #
        if   ( escapeType == "UseEscapeSequence" ):
            cmt      = "\\" + comment_mark
            expr_def = "{0}\s*{1}\s*(.*)".format( cmt, postProcess_mark )
            
        elif ( escapeType == "ReplaceCommentMark" ):
            original      = comment_mark
            expr_def      = "{0}\s*{1}\s*(.*)".format( replace_mark, postProcess_mark )
            for ik,line in enumerate( lines ):
                lines[ik] = ( lines[ik] ).replace( original, replace_mark )
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
            # --- [3-1] get command                         --- #
            # ------------------------------------------------- #
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
    #  -- [4-1] print & execute command             --  #
    for command in stack:
        if ( verbose__command ):
            print( command )
        if ( execute ):
            subprocess.run( command, shell=True )
    #  -- [4-2] return                              --  #
    if ( not( silent ) ):
        print( "[command__postProcess.py] command list is returned." + "\n" )
    return( stack )


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):

    # ------------------------------------------------- #
    # --- [1] arguments                             --- #
    # ------------------------------------------------- #
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument( "inpFile"        , help="input  file name."       , default=None )
    parser.add_argument( "--comment_mark" , help="comment mark like # or $", default="#"  ) 
    parser.add_argument( "-c", "--command", help="display command only", \
                         default=False, action="store_true" )
    args   = parser.parse_args()
    if ( args.inpFile is None ):
        print( "[command__postProcess.py] inpFile == ???" )
        print( "  ( e.g. )  $ command__postProcess.py inpFile -c --comment_mark $" )
        sys.exit()
    
    # ------------------------------------------------- #
    # --- [3] call replace variableDefinition       --- #
    # ------------------------------------------------- #
    execute = not( args.command )
    print( "\n" + "[commands]"  )
    ret     = command__postProcess( inpFile=args.inpFile, comment_mark=args.comment_mark, \
                                    execute=execute )
    print( "\n" + "[return]"       )
    print( "\n".join( ret ) + "\n" )
    
