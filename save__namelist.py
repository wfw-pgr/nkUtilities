import os, sys, copy
import numpy                               as np
import nkBasicAlgs.group__keys             as grk
import nkUtilities.convert__constantString as ccs


# ========================================================= #
# ===  save const Dictionary as namelist                === #
# ========================================================= #

def save__namelist( outFile=None, const =None, keys=None, append=False, \
                    skipkeys=[] , groups=None, NotGrouped=None, indent=4 ):

    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    if ( outFile is None ): sys.exit( "[save__namelist] outFile == ???" )
    if ( const   is None ): sys.exit( "[save__namelist] const   == ???" )
    if ( keys    is None ):
        print( "[save__namelist.py] no keys is designated. place alphabetical order." )
        keys = sorted( list( const.keys() ) )
    if ( NotGrouped is None   ): NotGrouped = "parameters"
    if ( NotGrouped == "skip" ): print( "[save__namelist.py] NotGrouped == skip :: " )
    
    writeDescriptor = ( [ "w", "a" ] )[ int( append ) ] #  append= True:"a", False:"w"

    # ------------------------------------------------- #
    # --- [2] grouping keys                         --- #
    # ------------------------------------------------- #
    grouped_keys, backforwards = grk.group__keys( keys=keys, NotGrouped=NotGrouped, \
                                                  returnType="list" )
    groupNames       = list( grouped_keys.keys() )
    grouped_contents = { grp:{} for grp in groupNames }
    for grp in groupNames:
        gkeys = grouped_keys[ grp ]
        for key in gkeys:
            orgkey   = backforwards[ grp+"."+key ]
            ( grouped_contents[ grp ] )[key] = const[ orgkey ]
    print( grouped_keys )
    print( grouped_contents )
    
    # ------------------------------------------------- #
    # --- [3] write in a file                       --- #
    # ------------------------------------------------- #
    if ( groups is None ): groups = groupNames
    
    with open ( outFile, writeDescriptor ) as f:

        for grp in groups:
            
            if ( not( grp in groupNames ) ):
                print( "[save__namelist.py] group cannot be found in groupNames... [ERROR]" )
                print( "[save__namelist.py] group             :: {} ".format( grp        ) )
                print( "[save__namelist.py] listed groupNames :: {} ".format( groupNames ) )
                sys.exit()
                
            f.write( "&{0}\n".format( grp ) )

            gkeys = grouped_keys[ grp ]
            for key in gkeys:
                orgkey = backforwards[ grp+"."+key ]
                value  = ( grouped_contents[grp] )[key]

                if ( orgkey in skipkeys ):
                    pass
                else:
                    expr, type_ = ccs.convert__constantString( value=value, brackets=["",""] )
                    if ( type_ is not None ):
                        f.write( " "*indent + "{0:<24} = {1}\n".format( key, expr ) )
            
            f.write( "/   ! -- End of {0}\n".format( grp ) )
            f.write( "\n" )
    
    
    # ------------------------------------------------- #
    # --- [4] return                                --- #
    # ------------------------------------------------- #
    print( "[save__namelist.py] const is saved in {0} ".format( outFile ) )
    return()


# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #

if ( __name__=="__main__" ):

    outFile = "test/test.conf"
    const   = { "ex1.some_int":1, "ex2.some_float":0.1, "ex1.some.string":"a", \
                "ex1.some_None":None, "ex2.some_bool":True, "ex1.some_array":[1.0,2.0] \
    }
    keys    = [ "ex1.some_int", "ex2.some_float", "ex1.some.string", \
                "ex1.some_array", "ex2.some_bool", "ex1.some_None" \
    ]
    save__namelist( outFile=outFile, const=const, keys=keys )


    # # ------------------------------------------------- #
    # # --- [3] save constants                        --- #
    # # ------------------------------------------------- #
        
    #     # -- [3-2] each parameters       -- # 
    #     for key in keys:
    #         type_ = type( const[key] )

    #         if   ( const[key] is None ):
    #             value = None
    #         elif ( key in skipkeys ):
    #             value = None
    #         elif ( type_ is int   ):
    #             value = const[key]
    #         elif ( type_ is float ):
    #             value = const[key]
    #         elif ( type_ is str   ):
    #             value = '"' + const[key] + '"'
    #         elif ( type_ is bool  ):
    #             if   ( const[key] is True  ):
    #                 value = "True"
    #             elif ( const[key] is False ):
    #                 value = "False"
    #         elif ( type_ is list ):
    #             value = [ str( val ) for val in const[key] ]
    #             value = ",".join( value )
    #         else:
    #             print( "[save__namelist.py] Unknown Object in const.... [ERROR] " )
    #             print( "[save__namelist.py]    key :: {0}".format( key   ) )
    #             print( "[save__namelist.py]  type_ :: {0}".format( type_ ) )
    #             print( const )
    #             sys.exit()

    #         if ( value is None ):
    #             pass    # -- nothing to do -- #
    #         else:
    #             f.write( "{0:<24} = {1}\n".format( key, value ) )

    #     # -- [3-3] end of namelist       -- # 

        
