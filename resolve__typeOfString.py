import os,sys,re

# ========================================================= #
# ===  resolve__typeOfString.py                         === #
# ========================================================= #
def resolve__typeOfString( word=None, priority=["None","int","float","logical",\
                                                "intarr","fltarr","string"] ):

    # ------------------------------------------------- #
    # --- [1] arguments check                       --- #
    # ------------------------------------------------- #
    if ( word is None ):
        sys.exit( "[resolve__typeOfString.py] word == ??? :: word is None [ERROR] " )
    if ( len( priority ) == 0 ):
        sys.exit( "[resolve__typeOfString.py] priority == ??? [ERROR] " )

    # ------------------------------------------------- #
    # --- [2] for each priority word                --- #
    # ------------------------------------------------- #
    ret = None
    for prior in priority:

        # ------------------------------------------------- #
        # --- [2-1] None type                           --- #
        # ------------------------------------------------- #
        if ( prior == "None" ):
            if ( word.lower() == "none" ):
                ret = None
                break
        # ------------------------------------------------- #
        # --- [2-2] integer type                        --- #
        # ------------------------------------------------- #
        if ( prior == "int" ):
            if ( word.isdecimal() ):
                ret = int( word )
                break
        # ------------------------------------------------- #
        # --- [2-3] float type                          --- #
        # ------------------------------------------------- #
        if ( prior == "float" ):
            flag = False
            try:
                ret  = float( word )
                flag = True
            except ValueError:
                pass
            if ( flag ): break
        # ------------------------------------------------- #
        # --- [2-4] logical type                        --- #
        # ------------------------------------------------- #
        if ( prior == "logical" ):
            if ( word.lower() in [ "true", "t" ] ):
                ret  = True
                break
            if ( word.lower() in [ "false", "f" ] ):
                ret  = False
                break
        # ------------------------------------------------- #
        # --- [2-5] fltarr type                         --- #
        # ------------------------------------------------- #
        if ( prior == "fltarr" ):
            pattern      = r"\[(.*)\]"
            ret          = re.search( pattern, word )
            failed       = False
            if ( ret is not None ):
                arrcontent   = ( ret.group(1) ).split(",")
                lst          = []
                for s in arrcontent:
                    try:
                        lst   += [ float( s ) ]
                    except ValueError:
                        failed = True
                        break
            else:
                failed = True
            if ( failed ):
                pass
            else:
                ret = lst
                break
        # ------------------------------------------------- #
        # --- [2-6] intarr type                         --- #
        # ------------------------------------------------- #
        if ( prior == "intarr" ):
            pattern      = r"\[(.*)\]"
            ret          = re.search( pattern, word )
            failed       = False
            if ( ret is not None ):
                arrcontent   = ( ret.group(1) ).split(",")
                lst          = []
                for s in arrcontent:
                    try:
                        lst   += [ int( s ) ]
                    except ValueError:
                        failed = True
                        break
            else:
                failed = True
            if ( failed ):
                pass
            else:
                ret = lst
                break
        # ------------------------------------------------- #
        # --- [2-7] string type                         --- #
        # ------------------------------------------------- #
        if ( prior == "string" ):
            ret = word.strip()

    # ------------------------------------------------- #
    # --- [3] return value                          --- #
    # ------------------------------------------------- #
    return( ret )


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #
if ( __name__=="__main__" ):
    
    ret = resolve__typeOfString( "0.1" )
    print( type(ret) )

    ret = resolve__typeOfString( "None" )
    print( type(ret) )

    ret = resolve__typeOfString( "1" )
    print( type(ret) )

    ret = resolve__typeOfString( "1.1" )
    print( type(ret) )

    ret = resolve__typeOfString( "aaa" )
    print( type(ret) )

    ret = resolve__typeOfString( "True" )
    print( type(ret) )

    ret = resolve__typeOfString( "False" )
    print( type(ret) )

    ret = resolve__typeOfString( "[0.1,0.2]" )
    print( type(ret) )
    print( type(ret[0]) )

    ret = resolve__typeOfString( "[1,2,3]" )
    print( type(ret) )
    print( type(ret[0]) )
