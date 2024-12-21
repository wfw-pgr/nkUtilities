import os, sys, re, json5

# ========================================================= #
# ===  synonymize__keywords.py                          === #
# ========================================================= #

def synonymize__keywords( dictionary=None, synonym=None ):

    # ------------------------------------------------- #
    # --- [1] load dictionary & synonym             --- #
    # ------------------------------------------------- #
    if ( dictionary is None ):
        print( "[synonymize__keywords.py] dictionary == ??? " )
    else:
        if ( type( dictionary ) is str ):
            if ( os.path.exists( dictionary ) ):
                with open( dictionary, "r" ) as f:
                    dictionary = json5.load( f )
            else:
                print( "[synonymize__keywords.py] cannnot find {} ".format( dictionary ) )
                sys.exit()
    
    if ( synonym is None ):
        print( "[synonymize__keywords.py] synonym == ??? " )
    else:
        if ( type( synonym ) is str ):
            if ( os.path.exists( synonym ) ):
                with open( synonym, "r" ) as f:
                    synonym = json5.load( f )
            else:
                print( "[synonymize__keywords.py] cannnot find {} ".format( synonym ) )
                sys.exit()
                
    # ------------------------------------------------- #
    # --- [2] replace synonym                       --- #
    # ------------------------------------------------- #
    ret = { **dictionary }
    for key in dictionary.keys():
        if ( key in synonym ):
            ret[ synonym[key] ] = ret.pop( key )
        else:
            ret[ key ]            = ret.pop( key )
    return( ret )


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):

    dictionary = "test/synonymize__keywords.json"
    synonym    = "test/synonym.json"
    ret        = synonymize__keywords( dictionary=dictionary, synonym=synonym )
    print( ret )
