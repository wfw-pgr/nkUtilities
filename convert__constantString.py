import os, sys
import numpy as np

# ========================================================= #
# ===  convert__constantString                          === #
# ========================================================= #

def convert__constantString( value=None, float_fmt="{:15.8e}", integer_fmt="{:}", \
                             returnType="list", brackets=["[","]"] ):

    # ------------------------------------------------- #
    # --- [1] convert into constants notation       --- #
    # ------------------------------------------------- #
    type_ = type( value )
    if   ( value is None  ):
        expr   = "None"
        type_  = None
        
    elif ( type_ is int   ):
        expr   = integer_fmt.format( value )
        
    elif ( type_ is float ):
        expr   = float_fmt.format( value )
        
    elif ( type_ is str   ):
        expr   = '"' + value + '"'
        
    elif ( type_ is bool  ):
        expr   = "True" if ( value ) else "False"
        
    elif ( type_ in [ list, tuple ]  ):
        expr = [ str( val ) for val in list( value ) ]
        expr = brackets[0] + ",".join( expr ) + brackets[1]
        
    elif ( type_ in [ np.ndarray  ]  ):
        expr = [ str( val ) for val in np.reshape( value, (-1,) ) ]
        expr = brackets[0] + ",".join( expr ) + brackets[1]
        
    else:
        print( "[save__namelist.py] Unknown Object in const.... [ERROR] " )
        print( "[save__namelist.py]    key :: {0}".format( key   ) )
        print( "[save__namelist.py]  type_ :: {0}".format( type_ ) )
        print( value )
        sys.exit()
        
    # ------------------------------------------------- #
    # --- [2] return                                --- #
    # ------------------------------------------------- #
    if   ( returnType.lower() == "list" ):
        return( [ expr, type_ ] )
    elif ( returnType.lower() == "expr" ): 
        return( expr  )
    elif ( returnType.lower() == "type" ): 
        return( type_ )


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    
    values = [ 1, 2.0, "Book", True, False, None, \
               list(range(5)), np.linspace( 0, 1, 5 ), ["a","bb","ccc"] ]

    for value in values:
        expr, type_ = convert__constantString( value=value )
        print()
        print( "[convert__constantString.py] value :: {} ".format( value ) )
        print( "[convert__constantString.py] expr  :: {} ".format( expr  ) )
        print( "[convert__constantString.py] type_ :: {} ".format( type_ ) )
