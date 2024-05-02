import json5, re, math, sys
import numpy as np

# ========================================================= #
# ===  json__formulaParser.py                           === #
# ========================================================= #

def json__formulaParser( inpFile=None, stop__error=False, table=None ):

    expr_fml    = r"\s*`([\s\S]+)`\s*"
    expr_var    = r"\$\{(\S+)\}"

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
                match_var = re.findall( expr_var, formula )
                for var in match_var:
                    if ( var in varDict ):
                        expr_from = "${"+var+"}"
                        expr_into = "{}".format( varDict[var] )
                        formula   = formula.replace( expr_from, expr_into )
                    else:
                        print( "\n[json__wformula.py] Cannot find variable [ERROR] :: {}\n".format( var ) )
                        if ( stop__error ): sys.exit()
                try:
                    varDict[key] = eval( formula )
                except SyntaxError:
                    print()
                    print( "[json__wformula.py] Cannot evaluate [ERROR]" )
                    print( "[json__wformula.py] key     :: {}".format( key ) )
                    print( "[json__wformula.py] formula :: {}".format( val ) )
                    print()
                except:
                    print()
                    print( "[json__wformula.py] Cannot evaluate [ERROR]" )
                    print( "[json__wformula.py] key     :: {}".format( key ) )
                    print( "[json__wformula.py] formula :: {}".format( val ) )
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
    inpFile  = "test/sample.json"
    ret      = json__formulaParser( inpFile=inpFile )
    print( ret )



