import sys

# ========================================================= #
# ===  Load Tabled Data from File                       === #
# ========================================================= #
def LoadConst( inpFile=None ):
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
        if ( line[0] != "#" ):
            # -- [3-1] vname, vtype, value  -- #
            vname = ( line.split() )[0]
            vtype = ( line.split() )[1]
            value = ( line.split() )[2]
            # -- [3-2] vtype check          -- #
            if   ( value == 'None'   ):
                vdict[vname] = None
            elif ( vtype == 'float'  ):
                vdict[vname] = float( value )
            elif ( vtype == 'double' ):
                vdict[vname] = float( value )
            elif ( vtype == 'long'   ):
                vdict[vname] = int( float(value) )
            elif ( vtype == 'string' ):
                vdict[vname] = value
            elif ( vtype == 'logical' ):
                if ( value == "True" ):
                    vdict[vname] = True
                else:
                    vdict[vname] = False
            elif ( vtype == 'array'  ):
                arr  = value.replace("[","").replace("]","").split(",")
                lst = [ float(s) for s in arr ]
                vdict[vname] = lst
            else:
                print("[ERROR] Unknown Object in LoadConst :: {0} [ERROR]".format(inpFile) )
    # ------------------------------------------------- #
    # --- [4] return                                --- #
    # ------------------------------------------------- #
    return( vdict )

