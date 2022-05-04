import os, sys, re
import nkUtilities.resolve__typeOfString as tos

# ========================================================= #
# ===  replace__variableDefinition.py                   === #
# ========================================================= #

def replace__variableDefinition( inpFile=None, lines=None, priority=None, \
                                 replace_expression=True, comment_mark="#" ):

    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    if ( lines is None ):
        if ( inpFile is None ):
            sys.exit( "[replace__variableDefinition.py] lines, inpFile == ???? [ERROR] " )
        else:
            with open( inpFile, "r" ) as f:
                lines = f.readlines()
    if ( priority is None ):
        priority = ["None","int","float","logical","intarr","fltarr","strarr","string"]
        
    # ------------------------------------------------- #
    # --- [2] replace variables                     --- #
    # ------------------------------------------------- #
    vdict     = {}
    expr_def  = comment_mark + "\s*define\s*@(\S*)\s*=\s*(.*)"
    expr_eval = comment_mark + "\s*evaluate\s*@(\S*)\s*=\s*(.*)"
    for line in lines:
        # ------------------------------------------------- #
        # --- [2-1] define variable                     --- #
        # ------------------------------------------------- #
        ret = re.match( expr_def, line.lower() )
        if ( ret ):
            vname        = "@"+ret.group(1)
            if ( comment_mark in ret.group(2) ):
                value = ( ( ( ret.group(2) ).split(comment_mark) )[0] ).strip()
            else:
                value = ( ret.group(2) ).strip()
            value        = tos.resolve__typeOfString( word=value, priority=priority )
            vdict[vname] = value
        # ------------------------------------------------- #
        # --- [2-2] evaluate variable                   --- #
        # ------------------------------------------------- #
        ret = re.match( expr_eval, line.lower() )
        if ( ret ):
            # -- 
            vname        = "@"+ret.group(1)
            if ( comment_mark in ret.group(2) ):
                value = ( ( ( ret.group(2) ).split(comment_mark) )[0] ).strip()
            else:
                value = ( ret.group(2) ).strip()
            # -- 
            for hname in list( vdict.keys() ):
                ret = re.search( hname, value )
                if ( ret ):
                    if   ( type( vdict[hname] ) in [int,float] ):
                        hvalue = "{0}".format( vdict[hname] )
                        value  = value.replace( hname, hvalue )
                    else:
                        sys.exit( "[replace__variableDefinition.py] variables of evaluation must be (int,float). [ERROR] " )
            value        = "{0}".format( eval( value ) )
            value        = tos.resolve__typeOfString( word=value, priority=priority )
            vdict[vname] = value

    # ------------------------------------------------- #
    # --- [3] replace expression                    --- #
    # ------------------------------------------------- #
    if ( replace_expression ):
        replaced  = []
        vnames    = list( vdict.keys() )
        for line in lines:
            hline = line
            if ( len( hline.strip() ) == 0 ):
                replaced.append( hline )
                continue
            if ( ( hline.strip() )[0] == "#" ):
                replaced.append( hline )
                continue
            for vname in vnames:
                ret = re.search( vname, hline )
                if ( ret ):
                    if   ( type( vdict[vname] ) in [None,int,float,bool,str] ):
                        value = "{0}".format( vdict[vname] )
                    elif ( type( vdict[vname] ) in [list] ):
                        value = "[" + ",".join( vdict[vname] ) + "]"
                    hline = hline.replace( vname, value )
            replaced.append( hline )
        print( "[replace__variableDefinition.py] replaced lines is returned. " )
        return( replaced )
    else:
        print( "[replace__variableDefinition.py] variables dictionary is returned. " )
        return( vdict    )


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    ret = replace__variableDefinition( inpFile="test/replace_sample.conf" )
    print( ret )
    with open( "test/replace_sample.out", "w" ) as f:
        for line in ret:
            f.write(line)
        print( "output :: {}".format( "test/replace_sample.out" ) )
