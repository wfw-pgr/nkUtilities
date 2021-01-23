import sys


# ========================================================= #
# ===  save Tabled Data into File                       === #
# ========================================================= #

def save__constants( outFile=None, const=None, keys=None ):

    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    if ( outFile is None ):
        sys.exit( "[save__constants] outFile == ???" )
    if ( const   is None ):
        sys.exit( "[save__constants] const   == ???" )
    if ( keys    is None ):
        print( "[save__constants.py] no keys is designated... alphabetical order..." )
        keys = sorted( list( const.keys() ) )

    # ------------------------------------------------- #
    # --- [2] save constants                        --- #
    # ------------------------------------------------- #

    with open ( outFile, "w" ) as f:
        for key in keys:
            type_ = type( const[key] )

            if   ( const[key] is None  ):
                vtype = "None"
                value = "None"

            elif ( type_ is int   ):
                vtype = "integer"
                value = const[key]

            elif ( type_ is float ):
                vtype = "float"
                value = const[key]

            elif ( type_ is str   ):
                vtype = "string"
                value = const[key]

            elif ( type_ is bool  ):
                vtype = "logical"
                if   ( const[key] is True  ):
                    value = "True"
                elif ( const[key] is False ):
                    value = "False"

            elif ( type_ is list ):
                vtype = "array"
                slist = [ "{0}".format( val ) for val in const[key] ]
                value = "[" + ",".join( slist ) + "]"
                
            else:
                print( "[save__constants.py] Unknown Object in const.... [ERROR] " )
                print( "[save__constants.py]    key :: {0}".format( key   ) )
                print( "[save__constants.py]  type_ :: {0}".format( type_ ) )
                print( const )
                sys.exit()

            f.write( "{0:<24} {1:<14} {2}\n".format( key, vtype, value ) )
        print( "[save__constants.py] const is saved in {0} ".format( outFile ) )

        
    # ------------------------------------------------- #
    # --- [3] return                                --- #
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
    save__constants( outFile=outFile, const=const, keys=keys )
