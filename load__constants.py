import sys

# ========================================================= #
# ===  Load Tabled Data from File                       === #
# ========================================================= #
def load__constants( inpFile=None ):
    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    if ( inpFile is None ): sys.exit(" [LoadConst] inpFile == ?? ")
    
    # ------------------------------------------------- #
    # --- [2] Data Load                             --- #
    # ------------------------------------------------- #
    with open( inpFile ) as f:
        lines = f.readlines()
        
    # ------------------------------------------------- #
    # --- [3] generate Dictionary                   --- #
    # ------------------------------------------------- #
    vdict = {}
    for line in lines:
        if ( len( line.strip() ) == 0 ):
            continue
        if ( ( line[0] != "#" ) ):
            # -- [3-1] vname, vtype, value  -- #
            vname = ( line.split() )[0]
            vtype = ( line.split() )[1]
            value = ( line.split() )[2]
            
            # -- [3-2] vtype check          -- #
            if   ( value.lower() == 'none'   ):
                vdict[vname] = None
                
            elif ( vtype.lower() in [ 'float', 'double', 'real' ]  ):
                vdict[vname] = float( value )
                                
            elif ( vtype.lower() in [ 'long' , 'integer'] ):
                vdict[vname] = int( float(value) )

            elif ( vtype.lower() == 'string' ):
                vdict[vname] = value

            elif ( vtype.lower() == 'logical' ):
                if ( value == "True" ):
                    vdict[vname] = True
                else:
                    vdict[vname] = False

            elif ( vtype.lower() == 'array'  ):
                value = "".join( ( line.split() )[2:] )
                varr  = ( ( ( ( value.split( "#" )[0] ).strip() ).strip( "[" ) ).strip( "]" ) ).split(",")
                lst   = [ float(s) for s in varr ]
                vdict[vname] = lst
            else:
                print("[ERROR] Unknown Object in LoadConst :: {0} [ERROR]".format(inpFile) )

    # ------------------------------------------------- #
    # --- [4] return                                --- #
    # ------------------------------------------------- #
    return( vdict )

