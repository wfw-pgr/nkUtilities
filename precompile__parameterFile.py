#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-

import os, sys, argparse
import numpy                                   as np
import nkUtilities.include__dividedFile        as inc
import nkUtilities.replace__variableDefinition as rvd
import nkUtilities.json__formulaParser         as jfp
import nkUtilities.loadJSON__asVariableTable   as lja

# ========================================================= #
# ===  precompile__parameterFile.py                     === #
# ========================================================= #

def precompile__parameterFile( inpFile=None, outFile=None, lines=None, table=None, silent=True, \
                               priority=None, replace_expression=True, comment_mark="#", \
                               define_mark="<define>", include_mark="<include>",
                               loadJSON_mark="<loadJSON>", expr_var=None, \
                               escapeType ="UseEscapeSequence", variable_mark="@", \
                               append__variableList=True ):

    # ------------------------------------------------- #
    # --- [1] include divided Files                 --- #
    # ------------------------------------------------- #
    lines = inc.include__dividedFile( inpFile=inpFile, lines=lines, \
                                      comment_mark=comment_mark, include_mark=include_mark, \
                                      escapeType=escapeType, silent=silent )
    
    # ------------------------------------------------- #
    # --- [2] load json file                        --- #
    # ------------------------------------------------- #
    table = lja.loadJSON__asVariableTable( inpFile=inpFile, lines=lines, table=table, \
                                           loadJSON_mark=loadJSON_mark, \
                                           variable_mark=variable_mark, \
                                           comment_mark=comment_mark, escapeType=escapeType )
    
    # ------------------------------------------------- #
    # --- [3] include divided Files                 --- #
    # ------------------------------------------------- #
    lines = rvd.replace__variableDefinition( outFile=outFile, lines=lines, table=table,
                                             replace_expression=replace_expression, \
                                             comment_mark=comment_mark, \
                                             variable_mark=variable_mark, priority=priority, \
                                             escapeType=escapeType, silent=silent, \
                                             append__variableList=append__variableList )
    return( lines )


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):

    mode = "normal"
    
    if ( mode == "test" ):
        table   = { "title":"TEST01" }
        inpFile = "test/precompile__parameterFile/sample_parameter.inp"
        outFile = "test/precompile__parameterFile/sample_parameter.out"
        ret     = precompile__parameterFile( inpFile=inpFile, outFile=outFile, \
                                             comment_mark="$", table=table )
        print()
        print( "".join( ret ) )
        print()
        sys.exit()

    elif ( mode == "normal" ):

        parser = argparse.ArgumentParser()
        parser.add_argument( "inpFile"       , help="input  file name." )
        parser.add_argument( "--outFile"     , help="output file name." )
        parser.add_argument( "--comment_mark", help="comment mark.", default="#" )
        args   = parser.parse_args()
        if ( args.inpFile is None ):
            print( "[precompile__parameterFile.py]  inpFile  must be given ..." )
            print( "precompile__parameterFile.py inpFile --outFile xxx --comment_mark X")

        ret = precompile__parameterFile( inpFile=args.inpFile, outFile=args.outFile,\
                                         comment_mark=args.comment_mark )
        print( "".join( ret ) )
