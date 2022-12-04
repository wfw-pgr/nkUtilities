import numpy as np
import os, sys

# ========================================================= #
# ===  write__variableDefinition.py                     === #
# ========================================================= #

def write__variableDefinition( table=None, keys=None, outFile=None, comment_mark="#", \
                               define_mark="<define>", variable_mark="@" ):

    # ------------------------------------------------- #
    # --- [1]  Arguments                            --- #
    # ------------------------------------------------- #
    if ( table is None ): sys.exit( "[write__variableDefinition.py] table == ???" )

    # ------------------------------------------------- #
    # --- [2]  for loop to write out table          --- #
    # ------------------------------------------------- #
    if ( keys is None ): keys = table.keys()
    nMaxLen    = np.max( np.array( [ len(key) for key in keys ] ) )
    name_expr  = "{0:" + str(nMaxLen) + "}"
    value_expr = "{1}"
    expression = "{0} {1} {2}{3} = {4}\n".format( comment_mark, define_mark, variable_mark, \
                                                  name_expr, value_expr )
    stack      = []
    for key in keys:
        stack += [ expression.format( key, table[key] ) ]
    contents = "".join( stack )

    # ------------------------------------------------- #
    # --- [3] write out                             --- #
    # ------------------------------------------------- #
    if ( outFile is not None ):
        with open( outFile, "w" ) as f:
            f.write( contents )
    return( contents )

# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    
    table   = { "theta1":-90.0, \
                "theta2":+90.0, \
                "pole.r0":"flag", \
                "pole.flag":True, \
    }
    keys    = ["theta2", "theta1"]
    outFile = "test/example.conf"
    ret     = write__variableDefinition( outFile=outFile, table=table, keys=keys )
    print( ret )
