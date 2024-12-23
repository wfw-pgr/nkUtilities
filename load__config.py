import os, sys, re, json5
import nkUtilities.load__constants as lcn

# ========================================================= #
# ===  load default.conf to plot settings               === #
# ========================================================= #

def load__config( config=None, new=True, synonym=None ):

    dirname = os.path.dirname( os.path.abspath( __file__ ) )

    # ------------------------------------------------- #
    # --- [1] load config file                      --- #
    # ------------------------------------------------- #
    if ( config is None ):
        if ( new ):
            config  = os.path.join( dirname, "config.json" )
            with open( config, "r" ) as f:
                const = json5.load( f )
        else:
            config  = os.path.join( dirname, "default.conf" )
            const   = lcn.load__constants( inpFile=config )

    # ------------------------------------------------- #
    # --- [2] synonymize keywords                   --- #
    # ------------------------------------------------- #
    if ( synonym is None ):
        synonym = os.path.join( dirname, "synonym.json" )
    import nkUtilities.synonymize__keywords as syn
    const     = syn.synonymize__keywords( dictionary=const, synonym=synonym )
    return( const )
    

# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #
if ( __name__=="__main__" ):

    config = load__config()
    print( config )




















# import os, sys, re
# # ========================================================= #
# # ===  Load default.conf                                === #
# # ========================================================= #
# def load__config( config=None ):
    
#     # ------------------------------------------------- #
#     # --- [1] Arguments                             --- #
#     # ------------------------------------------------- #
#     if ( config is None ):
#         dirname = os.path.dirname( os.path.abspath( __file__ ) )
#         config  = os.path.join( dirname, "default.conf" )
            
#     # ------------------------------------------------- #
#     # --- [2] Load Config File                      --- #
#     # ------------------------------------------------- #
#     with open( config ) as f:
#         lines = f.readlines()
        
#     # ------------------------------------------------- #
#     # --- [3] generate config Dictionary            --- #
#     # ------------------------------------------------- #
#     ret = {}
#     for line in lines:
        
#         # -- empty line skip    -- #
#         if   ( len( line.strip() ) == 0 ):
#             continue
        
#         # -- comment line skip  -- #
#         if ( line.strip()[0] == "#"   ):
#             continue
        
#         # -- decomposition  -- #
#         vname =   ( line.split() )[0]
#         vtype = ( ( line.split() )[1] ).lower()
#         value =   ( line.split() )[2]
        
#         # -- classification -- #
#         if   ( value.lower() == "none" ):
#             ret[vname] = None
#         elif ( vtype.lower() in ["float","double", "real"] ):
#             ret[vname] = float( value )
#         elif ( vtype.lower() in ["long","integer"]         ):
#             ret[vname] = int( float(value) )
#         elif ( vtype == "string"  ):
#             ret[vname] = str( value )
#         elif ( vtype == "logical" ):
#             if   ( value.lower() in ["true","t"] ):
#                 ret[vname] = True
#             elif ( value.lower() in ["false","f"] ):
#                 ret[vname] = False
#         elif ( vtype == "array"  ):
#             value      = "".join( line.split()[2:] )
#             pattern    = r"\[(.+)\]"
#             sarr       = re.search( pattern, value )
#             arrcontent = ( sarr.group(1) ).split(",")
#             lst        = [ float(s) for s in arrcontent ]
#             ret[vname] = lst
#         else:
#             print()
#             print("[load__config.py] Unknown Object in load__config [WARNING]" )
#             print("[load__config.py] config file  :: {0} ".format( config ) )
#             print("[load__config.py] illegal line :: {0} ".format( line   ) )
#             print()
            
#     # ------------------------------------------------- #
#     # --- [4] return                                --- #
#     # ------------------------------------------------- #
#     return( ret )


# # ======================================== #
# # ===  実行部                          === #
# # ======================================== #
# if ( __name__=="__main__" ):
#     config = load__config()
#     print( config )





    
# # if ( config is None ):
# #     if ( "PYCONFIGFILE" in os.environ ):
# #         config = os.environ["PYCONFIGFILE"]
# #     else:
# #         print( "[load__config] No Config File !! " )
# #         print( "[load__config]   -- 1. set environmental variable 'PYCONFIGFILE'." )
# #         print( "[load__config]   -- 2. specify argument config. load__config( config=xxx )" )
# #         print( "[load__config] stop..." )
# #         sys.exit()
