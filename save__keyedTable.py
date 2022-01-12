import os, sys

# ========================================================= #
# ===  save__keyedTable.py                              === #
# ========================================================= #

def save__keyedTable( table=None, names=None, keys=None, outFile="test.table" ):

    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    if ( table is None ):
        sys.exit( "[save__keyedTable.py] table is None. [ERROR] " )
    if ( keys  is None ):
        keys = list( table.keys() )
    if ( len( keys ) == 0 ):
        sys.exit( "[save__keyedTable.py] table:: empty card. No key for table. [ERROR] " )
    if ( names is None ):
        names = list( table[keys[0]].keys() )
    if ( "key" in names ):
        names.remove( "key" )
        names = [ "key" ] + names
    else:
        for key in keys:
            table[key]["key"] = key
        names = [ "key" ] + names

    # ------------------------------------------------- #
    # --- [2] save__keyedTable                      --- #
    # ------------------------------------------------- #
    
    with open( outFile, "w" ) as f:
        
        # ------------------------------------------------- #
        # --- [2-1] write header                        --- #
        # ------------------------------------------------- #
        header = "# <names> " + " ".join( names ) + "\n"
        f.write( header )
        # ------------------------------------------------- #
        # --- [2-2] write cards                         --- #
        # ------------------------------------------------- #
        for key in keys:
            card   = table[key]
            slst   = []
            for name in names:
                if ( name in card ):
                    slst += [ str( card[name] ) ]
                else:
                    slst += [ "None" ]
            line   = " ".join( slst ) + "\n"
            f.write( line )

    return()


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):

    table   = { "key01":{ "r1":1, "r0":2, "r3":3 }, \
                "key02":{ "r1":1, "r0":2, "r3":3 }, \
                "key03":{ "r1":1, "r0":2, "r3":3 }  }
    outFile = "test/out.table"
    names   = [ "r1", "r2", "r3", "r0" ] 
    save__keyedTable( table=table, outFile=outFile, names=names )
