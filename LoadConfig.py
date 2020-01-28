import os, sys

# ========================================================= #
# ===  Load default.conf                                === #
# ========================================================= #
def LoadConfig( config=None ):
    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    if ( config is None ):
        if ( "PYCONFIGFILE" in os.environ ):
            config = os.environ["PYCONFIGFILE"]
        else:
            print( "[LoadConfig] No Config File !! " )
            print( "[LoadConfig]   -- 1. set environmental variable 'PYCONFIGFILE'." )
            print( "[LoadConfig]   -- 2. specify argument config. LoadConfig( config=xxx )" )
            print( "[LoadConfig] stop..." )
            sys.exit()
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
        if ( len(line) > 0 ):
            if ( ( line[0] != "#" ) and ( line[0] != "\n" )  ):
                # -- decomposition  -- #
                vname = ( line.split() )[0]
                vtype = ( line.split() )[1]
                value = ( line.split() )[2]
                # -- classification -- #
                if   ( value == 'None'    ):
                    ret[vname] = None
                elif ( vtype == 'float'   ):
                    ret[vname] = float( value )
                elif ( vtype == 'double'  ):
                    ret[vname] = float( value )
                elif ( vtype == 'long'    ):
                    ret[vname] = int( float(value) )
                elif ( vtype == 'string'  ):
                    ret[vname] = value
                elif ( vtype == 'logical' ):
                    if ( value == "True" ):
                        ret[vname] = True
                    else:
                        ret[vname] = False
                elif ( vtype == 'array'  ):
                    arr        = value.replace("[","").replace("]","").split(",")
                    lst        = [ float(s) for s in arr ]
                    ret[vname] = lst
                else:
                    print("[ERROR] Unknown Object in LoadConfig :: {0} [ERROR]".format(config) )
    return( ret )


# ======================================== #
# ===  実行部                          === #
# ======================================== #
if ( __name__=="__main__" ):
    config = LoadConfig()
    print( config )
