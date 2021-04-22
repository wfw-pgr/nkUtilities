import numpy as np

# ========================================================= #
# ===  load__table2dictarr                              === #
# ========================================================= #

def load__table2dictarr( inpFile=None, datatype="auto" ):

    if ( inpFile is None ): sys.exit( "[load__table2dictarr] inpFile == ???" )

    with open( inpFile, "r" ) as f:
        header = f.readline()
        items  = ( ( header.strip() ).strip( "#" ) ).split()
        lines  = f.readlines()
    dicts  = []
    for line in lines:
        if ( len( line.strip() ) == 0 ):
            continue
        if ( ( line.strip() )[0] == "#" ):
            continue
        
        contents = ( line.strip() ).split()
        if ( datatype=="string" ):
            dicts.append( { item:  str(contents[ik]) for ik,item in enumerate( items ) } )
        if ( datatype=="float" ):
            dicts.append( { item:float(contents[ik]) for ik,item in enumerate( items ) } )
            
        if ( datatype=="auto"  ):
            stack = []
            for ik,item in enumerate(items):
                content = contents[ik]
                if   ( content is None ):
                    stack.append( None )
                elif ( content.isdecimal() ):
                    stack.append(   int( content ) )
                elif ( isfloat( content ) ):
                    stack.append( float( content ) )
                else:
                    stack.append(   str( content ) )
            dicts.append( { items[ik]:stack[ik] for ik in range( len( items ) ) } )
        
    return( dicts )


# ========================================================= #
# ===  isfloat function                                 === #
# ========================================================= #
def isfloat( parameter ):
    if not( parameter.isdecimal() ):
        try:
            float( parameter )
            return True
        except ValueError:
            return False
    else:
        return False



# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #
if ( __name__=="__main__" ):

    inpFile = "test/sample.conf"
    ret = load__table2dictarr( inpFile=inpFile )
    print( ret )
