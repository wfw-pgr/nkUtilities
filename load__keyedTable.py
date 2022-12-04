import re, sys
import nkUtilities.resolve__typeOfString       as tos
import nkUtilities.replace__variableDefinition as rvd
import nkUtilities.include__dividedFile        as inc


# ========================================================= #
# ===  Load Tabled with key from File                   === #
# ========================================================= #
def load__keyedTable( inpFile=None, returnType="dict-dict", \
                      priority=["None","int","float","logical","intarr",\
                                "fltarr","strarr","string"], \
                      datatype=None, comment_mark="#" ):
    
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
    # --- [3] replace variables                     --- #
    # ------------------------------------------------- #
    lines = inc.include__dividedFile       ( lines=lines, comment_mark=comment_mark )
    lines = rvd.replace__variableDefinition( lines=lines, replace_expression=True, \
                                             comment_mark=comment_mark )
    
    # ------------------------------------------------- #
    # --- [4] load header                           --- #
    # ------------------------------------------------- #
    names  = search__namesTags( lines=lines )

    # ------------------------------------------------- #
    # --- [5] generate Dictionary                   --- #
    # ------------------------------------------------- #
    vdict   = {}
    keys    = []
    nWords  = len( names )
    for il,line in enumerate( lines ):

        # -- empty line skip          -- #
        if ( len( line.strip() ) == 0   ):
            continue
        # -- new names is defined     -- #
        pattern = "\s*#\s*<names>\s*(.*)"
        ret     = re.match( pattern, line.strip() )
        if ( ret is not None ):
            names  = search__namesTags( lines=lines[il:] )
            nWords = len( names )
            continue
        if ( ( line.strip() )[0] == "#" ):
            continue
        # -- value until comment mark -- #
        pattern = "(.*?)#.*"
        ret     = re.match( pattern, line.strip() )
        if ( ret is     None ):
            words  = ( line.strip() ).split()
        else:
            words  = ( ( ret.group(1) ).strip() ).split()
        # -- grouping of array :: []  -- #
        jword   = " ".join( words )
        words   = []
        pattern = "\[(.*?)\]"
        while( len( jword.strip() ) > 0 ):
            ret = re.match( pattern, jword )
            if ( ret is None ):
                split  = jword.split()
                words += [ split.pop(0) ]
                jword  = ( " ".join( split ) ).strip()
            else:
                words += [ "[" + "".join( ( ret.group(1) ).split() ) + "]" ]
                jword  = ( jword[(ret.end()):] ).strip()
        # -- resolve variable type    -- # 
        if ( len(words) == nWords ):
            try:
                key = str( words[0] )
            except:
                key = "key{0:03}".format( len(keys)+1 )
            vdict[key] = { names[ik]:tos.resolve__typeOfString(word=words[ik],priority=priority)\
                           for ik in range(nWords) }
            keys      += [ key ]
        else:
            print( "[load__keyedTable.py] incompatible line... @Line={}".format(il) )
            print( "[load__keyedTable.py] line  == {0}".format( " ".join( words ) ) )
            print( "[load__keyedTable.py] names == {0}".format( " ".join( names ) ) )
            sys.exit()

    # ------------------------------------------------- #
    # --- [6] return                                --- #
    # ------------------------------------------------- #
    if   ( returnType == "dict-dict" ):
        return( vdict )
    elif ( returnType == "keys" ):
        return( keys  )
    else:
        print( "[load__keyedTable.py] unknown returnType :: {0} ".format( returnType ) )



# ========================================================= #
# ===  search names tag                                 === #
# ========================================================= #

def search__namesTags( lines=None ):

    # ------------------------------------------------- #
    # --- [1] arguments                             --- #
    # ------------------------------------------------- #
    if ( lines is None ): sys.exit( "[load__header] lines == ???" )
    
    # ------------------------------------------------- #
    # --- [2] read header                           --- #
    # ------------------------------------------------- #
    irows   = -1
    names   = [""]
    pattern = "\s*#\s*<names>\s*(.*)"
    for ik,line in enumerate( lines ):
        # -- empty line skip          -- #
        if ( len( line.strip() ) == 0 ):
            continue
        # -- header mark              -- #
        ret     = re.match( pattern, line.strip() )
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

    # ------------------------------------------------- #
    # --- [3] cannot find any header :: default tag --- #
    # ------------------------------------------------- #
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
        
    return( names )


# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #

if ( __name__=="__main__" ):
    const = load__keyedTable( inpFile="test/keyedTable.conf" )
    print( const )







    # else:
    #     if ( (irows+1) <= len( lines ) ):
    #         lines = lines[(irows+1):]
    #     else:
    #         print( "[load__keyedTable.py] names is {0}".format( "".join( names ) ) )
    #         print( "[load__keyedTable.py] but empty table.... [ERROR]" )
    #         sys.exit()
