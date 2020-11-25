import os, sys, re


# ========================================================= #
# ===  Load default.conf                                === #
# ========================================================= #
def load__config( config=None ):
    
    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    if ( config is None ):
        dirname = os.path.dirname( os.path.abspath( __file__ ) )
        config  = os.path.join( dirname, "default.conf" )
            
    # ------------------------------------------------- #
    # --- [2] Load Config File                      --- #
    # ------------------------------------------------- #
    with open( config ) as f:
        lines = f.readlines()
        
    # ------------------------------------------------- #
    # --- [3] generate config Dictionary            --- #
    # ------------------------------------------------- #
    ret = {}
    for line in lines:
        
        # -- empty line skip    -- #
        if   ( len( line.strip() ) == 0 ):
            continue
        
        # -- comment line skip  -- #
        if ( line.strip()[0] == "#"   ):
            continue
        
        # -- decomposition  -- #
        vname =   ( line.split() )[0]
        vtype = ( ( line.split() )[1] ).lower()
        value =   ( line.split() )[2]
        
        # -- classification -- #
        if   ( value.lower() == "none" ):
            ret[vname] = None
        elif ( vtype.lower() in ["float","double", "real"] ):
            ret[vname] = float( value )
        elif ( vtype.lower() in ["long","integer"]         ):
            ret[vname] = int( float(value) )
        elif ( vtype == "string"  ):
            ret[vname] = str( value )
        elif ( vtype == "logical" ):
            if   ( value.lower() in ["true","t"] ):
                ret[vname] = True
            elif ( value.lower() in ["false","f"] ):
                ret[vname] = False
        elif ( vtype == "array"  ):
            value      = "".join( line.split()[2:] )
            pattern    = r"\[(.+)\]"
            sarr       = re.search( pattern, value )
            arrcontent = ( sarr.group(1) ).split(",")
            lst        = [ float(s) for s in arrcontent ]
            ret[vname] = lst
        else:
            print("[ERROR] Unknown Object in load__config :: {0} [ERROR]".format(config) )
    # ------------------------------------------------- #
    # --- [4] return                                --- #
    # ------------------------------------------------- #
    return( ret )


# ======================================== #
# ===  実行部                          === #
# ======================================== #
if ( __name__=="__main__" ):
    config = load__config()
    print( config )





    
# if ( config is None ):
#     if ( "PYCONFIGFILE" in os.environ ):
#         config = os.environ["PYCONFIGFILE"]
#     else:
#         print( "[load__config] No Config File !! " )
#         print( "[load__config]   -- 1. set environmental variable 'PYCONFIGFILE'." )
#         print( "[load__config]   -- 2. specify argument config. load__config( config=xxx )" )
#         print( "[load__config] stop..." )
#         sys.exit()
