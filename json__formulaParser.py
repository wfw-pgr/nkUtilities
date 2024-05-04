import json5, re, math, sys
import numpy as np

# ========================================================= #
# ===  json__formulaParser.py                           === #
# ========================================================= #

def json__formulaParser( inpFile=None, stop__error=False, table=None, \
                         expr_fml=None, formula_mark="`", variable_mark="$" ):
    
    if ( expr_fml is None ):
        if   ( formula_mark == "`" ):
            expr_fml = r"\s*`([\s\S]+)`\s*"
        else:
            print( "[json__formulaParser.py] formula_mark == {} ??? ".format( variable_mark ) )
            sys.exit()

    if ( variable_mark in [ "$" ] ):
        variable_mark = "\{}".format( variable_mark )
            
    # ------------------------------------------------- #
    # --- [1] load json file as json5               --- #
    # ------------------------------------------------- #
    with open( inpFile, "r" ) as f:
        varDict = json5.load( f )
    if ( table is not None ):
        varDict = { **table, **varDict }

    # ------------------------------------------------- #
    # --- [2] convert formula string into value     --- #
    # ------------------------------------------------- #
    for key,val in varDict.items():
        if ( type(val) is str ):
            match_fml = re.match( expr_fml, val )
            if ( match_fml ):
                formula   = match_fml.group(1)
                for var_,val_ in varDict.items():
                    expr_from = variable_mark+"\{*"+var_+"\}*\s*"
                    expr_into = "{}".format( val_ )
                    formula = re.sub( expr_from, expr_into, formula )
                try:
                    varDict[key] = eval( formula )
                except SyntaxError:
                    print()
                    print( "[json__wformula.py] Cannot evaluate [ERROR]" )
                    print( "[json__wformula.py] key     :: {}".format( key     ) )
                    print( "[json__wformula.py] formula :: {}".format( val     ) )
                    print( "[json__wformula.py]         :: {}".format( formula ) )
                    print()
                except:
                    print()
                    print( "[json__wformula.py] Cannot evaluate [ERROR]" )
                    print( "[json__wformula.py] key     :: {}".format( key     ) )
                    print( "[json__wformula.py] formula :: {}".format( val     ) )
                    print( "[json__wformula.py]         :: {}".format( formula ) )
                    print()
                    raise
                
    # ------------------------------------------------- #
    # --- [4] print parsed items                    --- #
    # ------------------------------------------------- #
    return( varDict )

# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    
    # ------------------------------------------------- #
    # --- [1] declare regexp and file name          --- #
    # ------------------------------------------------- #
    inpFile  = "test/json__formulaParser/sample1.json"
    ret      = json__formulaParser( inpFile=inpFile, variable_mark="$" )
    print( ret )

    # ------------------------------------------------- #
    # --- [2] variable mark is "@" case             --- #
    # ------------------------------------------------- #
    inpFile  = "test/json__formulaParser/sample2.json"
    ret      = json__formulaParser( inpFile=inpFile, variable_mark="@" )
    print( ret )

