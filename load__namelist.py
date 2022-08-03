import re, os, sys, copy
import nkUtilities.resolve__typeOfString as rts

# ========================================================= #
# ===  load__nameList.py                                === #
# ========================================================= #

def load__nameList( inpFile=None ):

    # ------------------------------------------------- #
    # --- [1] argument check                        --- #
    # ------------------------------------------------- #
    if ( inpFile is None ): sys.exit( "[load__nameList.py] inpFile == ???" )

    # ------------------------------------------------- #
    # --- [2] read file                             --- #
    # ------------------------------------------------- #
    with open( inpFile, "r" ) as f:
        contents = f.read()

    # ------------------------------------------------- #
    # --- [3] detect blocks                         --- #
    # ------------------------------------------------- #
    pattern1 = r"&.*?\/"
    matches1 = list( re.finditer( pattern1, contents, re.S ) )
    if ( len(matches1) == 0 ):
        print( "[load__nameList.py] no namelist block are detected..... [END] " )
        sys.exit()
    else:
        matches2   = [ match.group(0) for match in matches1 ]

    # ------------------------------------------------- #
    # --- [4] recognize block's name & items        --- #
    # ------------------------------------------------- #
    pattern2 = r"&\s*(\S+)((.|\s)*)\/"
    matches3   = [ re.match( pattern2, match ) for match in matches2 ]
    blockNames = [ match.group(1) for match in matches3 ]
    parameters = [ match.group(2) for match in matches3 ]
    parameters = [ param.strip().split( "\n" ) for param in parameters ]
    parameters = [ [ ( ( line.strip() ).split( "!" ) )[0] for line in param ] \
                   for param in parameters ]
    parameters = [ [ line.strip() for line in param if ( len(line) > 0 ) ]
                   for param in parameters ]

    # ------------------------------------------------- #
    # --- [5] arange items                          --- #
    # ------------------------------------------------- #
    pattern3   = r"(.*)=(.*)"
    blockItems = {}
    for ik,param in enumerate( parameters ):
        vdict = {}
        for hl in param:
            ret    = re.match( pattern3, hl )
            if ( ret ):
                key,value  = ( ret.group(1) ).strip(), ( ret.group(2) ).strip()
                vdict[key] = rts.resolve__typeOfString( word=value )
            else:
                print( "[load__nameList.py] wrong line @ line {0} in block {1}."\
                       .format( ik, blockNames[ik] ) )
                sys.exit()
        blockItems[blockNames[ik]] = copy.copy( vdict )
    return( blockItems )

    
# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    inpFile = "test/namelist.lst"
    load__nameList( inpFile=inpFile )
