import re, sys


# ========================================================= #
# ===  Load Tabled Data from File                       === #
# ========================================================= #
def load__constants( inpFile=None, returnKeys=False ):
    
    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    if ( inpFile is None ):
        sys.exit(" [LoadConst] inpFile == ?? ")
    
    # ------------------------------------------------- #
    # --- [2] Data Load                             --- #
    # ------------------------------------------------- #
    with open( inpFile ) as f:
        lines = f.readlines()
        
    # ------------------------------------------------- #
    # --- [3] generate Dictionary                   --- #
    # ------------------------------------------------- #
    vdict = {}
    keys  = []
    for line in lines:

        # -- empty line skip       -- #
        if ( len( line.strip() ) == 0 ):
            continue

        # -- comment line skip     -- #
        if ( line.strip()[0] == "#"   ):
            continue
        
        # -- decomposition         -- #
        vname = ( line.split() )[0]
        vtype = ( line.split() )[1]
        value = ( line.split() )[2]

        # -- classification        -- #
        if   ( value.lower() == 'none'   ):
            vdict[vname] = None
                
        elif ( vtype.lower() in [ 'float', 'double', 'real' ]  ):
            vdict[vname] = float( value )
                                
        elif ( vtype.lower() in [ 'long' , 'integer'] ):
            vdict[vname] = int( float(value) )
            
        elif ( vtype.lower() == 'string' ):
            vdict[vname] = value

        elif ( vtype.lower() in ['logical',"bool"] ):
            if   ( value.lower() in ["true","t" ] ):
                vdict[vname] = True
            elif ( value.lower() in ["false","f"] ):
                vdict[vname] = False
                
        elif ( vtype.lower() in [ "array", "fltarr" ] ):
            value        = "".join( ( line.split() )[2:] )
            pattern      = r"\[(.+)\]"
            sarr         = re.search( pattern, value )
            arrcontent   = ( sarr.group(1) ).split(",")
            lst          = [ float(s) for s in arrcontent ]
            vdict[vname] = lst

        elif ( vtype.lower() in [ "intarr", "intarray" ] ):
            value        = "".join( ( line.split() )[2:] )
            pattern      = r"\[(.+)\]"
            sarr         = re.search( pattern, value )
            arrcontent   = ( sarr.group(1) ).split(",")
            lst          = [ str(s) for s in arrcontent ]
            pattern      = r"(.+)-(.+)"
            ilst         = []
            for val in lst:
                reval = re.search( pattern, val )
                if ( reval ):
                    imin = min( int( reval.group(1) ), int( reval.group(2) ) )
                    imax = max( int( reval.group(1) ), int( reval.group(2) ) )
                    ival = list( range( imin, imax+1 ) )
                else:
                    ival = [ int( val ) ]
                ilst += ival
            vdict[vname] = ilst
            
        else:
            print("[ERROR] Unknown Object in load__constants :: {0} [ERROR]".format(inpFile) )
        keys.append( vname )

    # ------------------------------------------------- #
    # --- [4] return                                --- #
    # ------------------------------------------------- #
    if ( returnKeys is True ):
        return( keys  )
    else:
        return( vdict )




# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #

if ( __name__=="__main__" ):
    const = load__constants( inpFile="test/parameter.conf" )
    print( const )
