import re, sys
import nkUtilities.resolve__typeOfString as tos


# ========================================================= #
# ===  Load Tabled with key from File                   === #
# ========================================================= #
def load__keyedTable( inpFile=None, returnType="dict-dict", comment="#", \
                      priority=["None","int","float","logical","intarr","fltarr","string"], \
                      datatype=None ):
    
    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    if ( inpFile  is None  ):
        sys.exit(" [load__keyedTable.py] inpFile == ??? [ERROR]" )
    if ( datatype is not None ):
        priority = [ datatype, "string" ]
        
    # ------------------------------------------------- #
    # --- [2] Data Load                             --- #
    # ------------------------------------------------- #
    with open( inpFile ) as f:
        lines = f.readlines()

    # ------------------------------------------------- #
    # --- [3] read header                           --- #
    # ------------------------------------------------- #
    irows   = -1
    names   = [""]
    pattern = "#\s*<names>\s*(.*)"
    for ik,line in enumerate( lines ):
        # -- empty line skip          -- #
        if ( len( line.strip() ) == 0 ):
            continue
        # -- header mark              -- #
        ret     = re.match( pattern, line )
        if ( ret is None ):
            continue
        else:
            comment_pat = "(.*?)#.*"
            strings     = ret.group(1)
            ret         = re.match( comment_pat, strings )
            if ( ret is None ):
                names = ( strings.strip() ).split()
            else:
                names = ( ( ret.group(1) ).strip() ).split()
            irows = ik
            break
        
    if ( irows == -1 ):
        irows = 0
        for ik,line in enumerate( lines ):
            # -- empty line skip          -- #
            if ( len( line.strip() ) == 0 ):
                continue
            # -- skip comment line        -- #
            if ( line.strip()[0] == "#"   ):
                continue
            # -- search max column number -- #
            length = len( ( line.strip() ).split() )
            if ( irows < length ):
                irows = length
        names = [ "data{0:03}".format( ik+1 ) for ik in range( irows ) ]
        
    else:
        if ( (irows+1) <= len( lines ) ):
            lines = lines[(irows+1):]
        else:
            print( "[load__keyedTable.py] names is {0}".format( "".join( names ) ) )
            print( "[load__keyedTable.py] but empty table.... [ERROR]" )
            sys.exit()
        
    nWords = len( names )
    
    # ------------------------------------------------- #
    # --- [4] generate Dictionary                   --- #
    # ------------------------------------------------- #
    vdict = {}
    keys  = []
    for line in lines:

        # -- empty line skip          -- #
        if ( len( line.strip() ) == 0 ):
            continue
        # -- value until comment mark -- #
        pattern = "(.*?)#.*"
        ret     = re.match( pattern, line )
        if   ( ret is None ):
            words = ( line.strip() ).split()
        else:
            words = ( ( ret.group(1) ).strip() ).split()
        if ( len(words) == nWords ):
            try:
                key = str( words[0] )
            except:
                key = "key{0:03}".format( len(keys)+1 )
            vdict[key] = { names[ik]:tos.resolve__typeOfString(word=words[ik],priority=priority)\
                           for ik in range(nWords) }
            keys      += [ key ]
        else:
            print( "[load__keyedTable.py] incompatible line... " )
            print( "[load__keyedTable.py] line  == {0}".format( " ".join( words ) ) )
            print( "[load__keyedTable.py] names == {0}".format( " ".join( names ) ) )
            sys.exit()

    # ------------------------------------------------- #
    # --- [4] return                                --- #
    # ------------------------------------------------- #
    if   ( returnType == "dict-dict" ):
        return( vdict )
    elif ( returnType == "keys" ):
        return( keys  )
    else:
        print( "[load__keyedTable.py] unknown returnType :: {0} ".format( returnType ) )



# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #

if ( __name__=="__main__" ):
    const = load__keyedTable( inpFile="test/keyedTable.conf" )
    const = load__keyedTable( inpFile="test/keyedTable.conf", datatype="float" )
    print( const )
