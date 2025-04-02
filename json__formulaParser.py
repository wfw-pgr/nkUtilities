import json5, re, math, sys, decimal
import numpy as np

# ========================================================= #
# ===  json__formulaParser.py                           === #
# ========================================================= #

def json__formulaParser( inpFile=None, stop__error=False, verbose=False, table=None, \
                         expr_fml=None, formula_mark="", variable_mark="$", iterMax=10 ):
    
    if ( expr_fml is None ):
        if   ( formula_mark == "`" ):
            expr_fml = r"\s*`([\s\S]+)`\s*"
        elif ( formula_mark == "" ):
            expr_fml = r"([\s\S]+)"
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
    for iloop in range( iterMax ):
        updated = False
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
                        updated = True
                    except SyntaxError:
                        if ( verbose ):
                            print()
                            print( "[json__wformula.py] Cannot evaluate [ERROR]" )
                            print( "[json__wformula.py] key     :: {}".format( key     ) )
                            print( "[json__wformula.py] formula :: {}".format( val     ) )
                            print( "[json__wformula.py]         :: {}".format( formula ) )
                            print()
                    except:
                        if ( verbose ):
                            print()
                            print( "[json__wformula.py] Cannot evaluate [ERROR]" )
                            print( "[json__wformula.py] key     :: {}".format( key     ) )
                            print( "[json__wformula.py] formula :: {}".format( val     ) )
                            print( "[json__wformula.py]         :: {}".format( formula ) )
                            print()
                            raise
        if not( updated ): break

    # ------------------------------------------------- #
    # --- [3] align__digits                         --- #
    # ------------------------------------------------- #
    for key,val in varDict.items():
        if ( type(val) in [ int, np.int32 ] ):
            varDict[key] = int( return__digitsAligned( val ) )
        if ( type(val) in [ float, np.float64 ] ):
            varDict[key] = float( return__digitsAligned( val ) )
        if ( type(val) in [ list ] ):
            stack = []
            for vh in val:
                if   ( type(vh) in [   int, np.int32   ] ):
                    stack += [   int( return__digitsAligned( vh ) ) ]
                elif ( type(vh) in [ float, np.float64 ] ):
                    stack += [ float( return__digitsAligned( vh ) ) ]
                else:
                    stack += [ vh ]
            varDict[key] = stack
    
    # ------------------------------------------------- #
    # --- [4] print parsed items                    --- #
    # ------------------------------------------------- #
    return( varDict )


def return__digitsAligned( value, maxDigit=8, precision=12 ):

    if ( type( value ) in [ int, float, np.float64, np.int32 ] ):
        decimal.getcontext().prec     = precision
        decimal.getcontext().rounding = decimal.ROUND_HALF_UP
        exp = math.floor( math.log10( abs( value ) ) ) if ( value != 0 ) else 0.0
        if ( abs( exp ) >= maxDigit ):
            ret = ( "{:15." + str(maxDigit) + "e}" ).format( value )
        else:
            lowest = int( exp - maxDigit )
            quant  = decimal.Decimal( "1e{0}".format( lowest ) )
            dval   = decimal.Decimal.from_float( value ).quantize( quant )
            ret   = format(dval, "f").rstrip("0").rstrip(".")
        return( ret )
    else:
        return( value )



# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
        
    # ------------------------------------------------- #
    # --- [1] declare regexp and file name          --- #
    # ------------------------------------------------- #
    inpFile  = "test/json__formulaParser/sample1.json"
    ret      = json__formulaParser( inpFile=inpFile, variable_mark="$" )
    print()
    print( ret )
    print()
    
    # ------------------------------------------------- #
    # --- [2] variable mark is "@" case             --- #
    # ------------------------------------------------- #
    inpFile  = "test/json__formulaParser/sample2.json"
    ret      = json__formulaParser( inpFile=inpFile, variable_mark="@" )
    print()
    print( ret )
    print()


    # ------------------------------------------------- #
    # --- [2] variable mark is "@" case             --- #
    # ------------------------------------------------- #
    inpFile  = "test/json__formulaParser/sample3.json"
    ret      = json__formulaParser( inpFile=inpFile, variable_mark="@" )
    print()
    print( ret )
    print()

