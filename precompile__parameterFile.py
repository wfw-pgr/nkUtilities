import numpy as np
import nkUtilities.include__dividedFile        as inc
import nkUtilities.replace__variableDefinition as rvd

# ========================================================= #
# ===  precompile__parameterFile.py                     === #
# ========================================================= #

def precompile__parameterFile( inpFile=None, outFile=None, lines=None, table=None, \
                               priority=None, replace_expression=True, comment_mark="#", \
                               define_mark="<define>", include_mark="<include>", \
                               escapeType ="UseEscapeSequence", variable_mark="@" ):

    # ------------------------------------------------- #
    # --- [1] call routines                         --- #
    # ------------------------------------------------- #
    ret1 = inc.include__dividedFile( inpFile=inpFile, lines=lines, \
                                     comment_mark=comment_mark, include_mark=include_mark, \
                                     escapeType=escapeType )
    ret2 = rvd.replace__variableDefinition( outFile=outFile, lines=ret1, \
                                            table=table, comment_mark=comment_mark,\
                                            priority=priority, \
                                            replace_expression=replace_expression, \
                                            variable_mark=variable_mark, \
                                            escapeType=escapeType )
    return( ret2 )


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    inpFile = "test/replace_sample.conf"
    outFile = "test/replace_sample.out"
    table   = { "@val_frm_tbl":"import_from_table::SUCCESS"  }
    precompile__parameterFile( inpFile=inpFile, outFile=outFile, table=table, comment_mark="$" )
    
    
