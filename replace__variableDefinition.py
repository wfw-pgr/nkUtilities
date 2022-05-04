import os, sys, re
import nkUtilities.resolve__typeOfString as tos

# ========================================================= #
# ===  replace__variableDefinition.py                   === #
# ========================================================= #

def replace__variableDefinition( inpFile=None, lines=None, priority=None, \
                                 replace_expression=True, comment_mark="#", outFile=None, \
                                 define_mark="<define>", variable_mark="@" ):

    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    if ( lines is None ):
        if ( inpFile is None ):
            sys.exit( "[replace__variableDefinition.py] lines, inpFile == ???? [ERROR] " )
        else:
            with open( inpFile, "r" ) as f:
                lines = f.readlines()
    if ( type( lines ) is str ):
        lines = [ lines ]
    if ( priority is None ):
        priority = ["None","int","float","logical","intarr","fltarr","strarr","string"]
        
    # ------------------------------------------------- #
    # --- [2] replace variables                     --- #
    # ------------------------------------------------- #
    vdict     = {}
    # expr_def  = comment_mark + "\s*" + define_mark +  "\s*@(\S*)\s*=\s*(.*)"
    expr_def  = "{0}\s*{1}\s*{2}(\S*)\s*=\s*(.*)".format( comment_mark, define_mark, \
                                                          variable_mark )
    
    for line in lines:   # 1-line, 1-argument.
        
        # ------------------------------------------------- #
        # ---     search variable notation              --- #
        # ------------------------------------------------- #
        ret = re.match( expr_def, line.lower() )
        if ( ret ):      # Found.

            # ------------------------------------------------- #
            # --- [2-1] Definition of the variable          --- #
            # ------------------------------------------------- #
            vname        = "@"+ret.group(1)
            if ( comment_mark in ret.group(2) ):
                value = ( ( ( ret.group(2) ).split(comment_mark) )[0] ).strip()
            else:
                value = ( ret.group(2) ).strip()
            # ------------------------------------------------- #
            # --- [2-2] replace variables in value          --- #
            # ------------------------------------------------- #
            for hname in list( vdict.keys() ):
                ret = re.search( hname, value )
                if ( ret ):
                    if   ( type( vdict[hname] ) in [int,float,bool] ):
                        hvalue = "{0}".format( vdict[hname] )
                        value  = value.replace( hname, hvalue )
                    else:
                        sys.exit( "[replace__variableDefinition.py] variables of evaluation must be (int,float,bool). [ERROR] " )
            # ------------------------------------------------- #
            # --- [2-3] evaluation and store                --- #
            # ------------------------------------------------- #
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
                    hline = hline.replace( vname, value.strip() )
            replaced.append( hline )

    # ------------------------------------------------- #
    # --- [4] return                                --- #
    # ------------------------------------------------- #
    if ( replace_expression ):
        if ( outFile is not None ):
            text = "".join( replaced )
            with open( outFile, "w" ) as f:
                f.write( text )
            print( "[replace__variableDefinition.py] output :: {}".format( outFile ) )
        print( "[replace__variableDefinition.py] replaced lines is returned." + "\n" )
        return( replaced )
    else:
        print( "[replace__variableDefinition.py] variables dictionary is returned. " )
        return( vdict    )


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):

    # ------------------------------------------------- #
    # --- [1] define parametres                     --- #
    # ------------------------------------------------- #
    inpFile = "test/replace_sample.conf"
    outFile = "test/replace_sample.out"
    
    # ------------------------------------------------- #
    # --- [2] input / output Files                  --- #
    # ------------------------------------------------- #
    import nkUtilities.parse__arguments as par
    args = par.parse__arguments()
    if ( args["inpFile"] is not None ):
        inpFile = args["inpFile"]
    if ( args["outFile"] is not None ):
        outFile = args["outFile"]

    # ------------------------------------------------- #
    # --- [3] call replace variableDefinition       --- #
    # ------------------------------------------------- #
    ret     = replace__variableDefinition( inpFile=inpFile, outFile=outFile )
    print( ret )
