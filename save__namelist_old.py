import os, sys, copy
import numpy as np
import nkBasicAlgs.group__keys as grp


# ========================================================= #
# ===  save const Dictionary as namelist                === #
# ========================================================= #

def save__namelist( outFile=None, const=None, keys=None, append=False, \
                    skipkeys=[] , group=None ):

    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    if ( outFile is None ): sys.exit( "[save__namelist] outFile == ???" )
    if ( const   is None ): sys.exit( "[save__namelist] const   == ???" )
    if ( keys    is None ):
        print( "[save__namelist.py] no keys is designated. place alphabetical order." )
        keys = sorted( list( const.keys() ) )

    # ------------------------------------------------- #
    # --- [2] grouping keys                         --- #
    # ------------------------------------------------- #
    # grouped_keys = grp.group__keys( keys=keys )

    # ------------------------------------------------- #
    # --- [3] save constants                        --- #
    # ------------------------------------------------- #
    with open ( outFile, "w" ) as f:
        # -- [3-1] namelist's group name -- # 
        f.write( "&{0}\n".format( group ) )
        
        # -- [3-2] each parameters       -- # 
        for key in keys:
            type_ = type( const[key] )

            if   ( const[key] is None ):
                value = None
            elif ( key in skipkeys ):
                value = None
            elif ( type_ is int   ):
                value = const[key]
            elif ( type_ is float ):
                value = const[key]
            elif ( type_ is str   ):
                value = '"' + const[key] + '"'
            elif ( type_ is bool  ):
                if   ( const[key] is True  ):
                    value = "True"
                elif ( const[key] is False ):
                    value = "False"
            elif ( type_ is list ):
                value = [ str( val ) for val in const[key] ]
                value = ",".join( value )
            else:
                print( "[save__namelist.py] Unknown Object in const.... [ERROR] " )
                print( "[save__namelist.py]    key :: {0}".format( key   ) )
                print( "[save__namelist.py]  type_ :: {0}".format( type_ ) )
                print( const )
                sys.exit()

            if ( value is None ):
                pass    # -- nothing to do -- #
            else:
                f.write( "{0:<24} = {1}\n".format( key, value ) )

        # -- [3-3] end of namelist       -- # 
        f.write( "/   ! -- End of {0}\n".format( group ) )
        f.write( "\n" )
        print( "[save__namelist.py] const is saved in {0} ".format( outFile ) )

        
    # ------------------------------------------------- #
    # --- [4] return                                --- #
    # ------------------------------------------------- #
    return()


# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #

if ( __name__=="__main__" ):

    outFile = "test.conf"
    const   = { "some_int":1, "some_float":0.1, "some_string":"a", \
                "some_None":None, "some_bool":True, "some_array":[1.0,2.0] \
    }
    keys    = ["some_int", "some_float", "some_string", \
               "some_array", "some_bool", "some_None" \
    ]
    save__namelist( outFile=outFile, const=const, keys=keys )

