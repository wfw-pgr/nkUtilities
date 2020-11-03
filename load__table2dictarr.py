import numpy as np

# ========================================================= #
# ===  load__table2dictarr                              === #
# ========================================================= #

def load__table2dictarr( inpFile=None, datatype="string" ):

    if ( inpFile is None ): sys.exit( "[load__table2dictarr] inpFile == ???" )

    with open( inpFile, "r" ) as f:
        header = f.readline()
        items  = ( ( header.strip() ).strip( "#" ) ).split()
        lines  = f.readlines()
    dicts  = []
    for line in lines:
        if ( ( line.strip() )[0] == "#" ):
            pass
        elif ( len( line.strip() ) == 0 ):
            pass
        else:
            contents = ( line.strip() ).split()
            if ( datatype=="string" ):
                dicts.append( { item:str(contents[ik]) for ik,item in enumerate( items ) } )
            if ( datatype=="float" ):
                dicts.append( { item:float(contents[ik]) for ik,item in enumerate( items ) } )
            
    return( dicts )
