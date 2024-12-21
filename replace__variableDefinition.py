import os, sys, re, decimal, math
import numpy as np
import nkUtilities.resolve__typeOfString as tos

# ========================================================= #
# ===  replace__variableDefinition.py                   === #
# ========================================================= #

def replace__variableDefinition( inpFile=None, lines=None, priority=None, table=None, \
                                 replace_expression=True, comment_mark="#", outFile=None, \
                                 define_mark="<define>", variable_mark="@", \
                                 escapeType ="UseEscapeSequence", silent=True, \
                                 append__variableList=True, precision=12, maxDigit=10 ):

    decimal.getcontext().prec = precision
    
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
    # --- [2] expression of definition              --- #
    # ------------------------------------------------- #
    vdict      = {}
    if ( table is not None ):
        vdict  = { **vdict, **table }
    Flag__changeComment = False
    
    if ( comment_mark in [ "$", "*" ] ):  # --:: Need - Escape-Sequence ... ::-- #
        if   ( escapeType == "UseEscapeSequence" ):
            cmt      = "\\" + comment_mark
            expr_def = "{0}\s*{1}\s*{2}(\S*)\s*=\s*(.*)".format( cmt, define_mark, variable_mark )
            
        elif ( escapeType == "ReplaceCommentMark" ):
            original     = comment_mark
            comment_mark = "#"
            Flag__changeComment = True
            expr_def     = "{0}\s*{1}\s*{2}(\S*)\s*=\s*(.*)".format( comment_mark, define_mark,\
                                                                     variable_mark )
            for ik,line in enumerate( lines ):
                lines[ik] = ( lines[ik] ).replace( original, comment_mark )

        else:
            print( "[replace__variableDefinition.py] Unknown escapeType :: {} ".format( escapeType ) )
            sys.exit()

    else:
        expr_def     = "{0}\s*{1}\s*{2}(\S*)\s*=\s*(.*)".format( comment_mark, define_mark, \
                                                                 variable_mark ) 

    # ------------------------------------------------- #
    # --- [3] parse variables                       --- #
    # ------------------------------------------------- #
    
    for iL,line in enumerate(lines):   # 1-line, 1-argument.

        # ------------------------------------------------- #
        # ---     search variable notation              --- #
        # ------------------------------------------------- #
        ret = re.match( expr_def, line )     # use match here.
        if ( ret ):      # Found.

            # ------------------------------------------------- #
            # --- [3-1] Definition of the variable          --- #
            # ------------------------------------------------- #
            vname        = "@"+ret.group(1)
            if ( comment_mark in ret.group(2) ):
                value = ( ( ( ret.group(2) ).split(comment_mark) )[0] ).strip()
            else:
                value = ( ret.group(2) ).strip()
            # ------------------------------------------------- #
            # --- [3-2] replace variables in value          --- #
            # ------------------------------------------------- #
            for hname in list( vdict.keys() ):
                ret = re.search( hname, value )
                if ( ret ):
                    if   ( type( vdict[hname] ) in [int,float,bool] ):
                        hvalue = "{0}".format( vdict[hname] )
                        value  = value.replace( hname, hvalue )
                    else:
                        print( "[replace__variableDefinition.py] ERROR @ line {}, ".format(iL) )
                        print( line )
                        sys.exit( "[replace__variableDefinition.py] variables of evaluation must be (int,float,bool). [ERROR] " )
            # ------------------------------------------------- #
            # --- [3-3] evaluation and store                --- #
            # ------------------------------------------------- #
            try:
                value    = "{0}".format( eval( value ) )
            except:
                value    = "{0}".format(       value   )
            value        = tos.resolve__typeOfString( word=value, priority=priority )
            vdict[vname] = value

    # ------------------------------------------------- #
    # --- [4] check variable mark                   --- #
    # ------------------------------------------------- #
    vdict_ = {}
    for key,val in vdict.items():
        if ( not( variable_mark in ["@"] ) ):
            print( "[replace__variableDefinition.py] variable_mark ??? :: {} "\
                   .format( variable_mark ) )
        check_expr = "{}\S+".format( variable_mark )
        ret        = re.match( check_expr, key )
        if ( ret ):
            vdict_[key] = val
        else:
            key_ = "{0}{1}".format( variable_mark, key )
            vdict_[key_] = val
    vdict = vdict_


    # ------------------------------------------------- #
    # --- [5] decimal expression                    --- #
    # ------------------------------------------------- #
    for key,value in vdict.items():
        if ( type(value) in [float] ):
            exp = math.floor( np.log10( abs( value ) ) ) if ( value != 0 ) else 0.0
            if ( abs( exp ) >= maxDigit ):
                vdict[key] = "{:15.8e}".format( value )
            else:
                vdict[key] = str( decimal.Decimal( round( value, maxDigit ) ).normalize() )
        if ( type(value) in [list]  ):
            if ( type( value[0] ) in [float] ):
                stack = []
                for val in value:
                    exp = math.floor( np.log10( abs( value ) ) ) if ( value != 0 ) else 0.0
                    if ( abs( exp ) >= maxDigit ):
                        stack += [ "{:15.8e}".format( val ) ]
                    else:
                        stack += str( decimal.Decimal( round( val, maxDigit ) ).normalize() )
                vdict[key] = "[" + ",".join( stack ) + "]"
    
    # ------------------------------------------------- #
    # --- [4] replace expression                    --- #
    # ------------------------------------------------- #
    if ( replace_expression ):
        replaced  = []
        vnames    = list( vdict.keys() )
        for line in lines:
            hline = ( line )
            if ( len( hline.strip() ) == 0 ):
                replaced.append( hline )
                continue
            if ( ( hline.strip() )[0] == comment_mark ):
                replaced.append( hline )
                continue
            for vname in vnames:
                ret = re.search( vname, hline )     # use search here.
                if ( ret ):
                    if   ( type( vdict[vname] ) in [None,int,bool,str] ):
                        value = "{0}".format( vdict[vname] )
                    elif ( type( vdict[vname] ) in [float] ):
                        value = str( decimal.Decimal( vdict[vname] ).normalize() )
                    elif ( type( vdict[vname] ) in [list] ):
                        if   ( type( vdict[vname][0] ) in [int] ):
                            value = [ "{}".format( val ) for val in vdict[vname] ]
                            value = "[" + ",".join( value ) + "]"
                        elif ( type( vdict[vname][0] ) in [float] ):
                            value = [ str( decimal.Decimal( vdict[vname] ).normalize() )
                                      for val in vdict[vname] ]
                            value = "[" + ",".join( value ) + "]"
                        else:
                            value = "[" + ",".join( vdict[vname] ) + "]"
                    hline = hline.replace( vname, value.strip() )
            replaced.append( hline )
            
        if ( Flag__changeComment ):
            for ik,line in enumerate( replaced ):
                replaced[ik] = ( line.replace( comment_mark, original ) )

    # ------------------------------------------------- #
    # --- [5] append variable List                  --- #
    # ------------------------------------------------- #
    if ( append__variableList ):
        lwidth     = 90
        cm, dcm    = comment_mark, 2*comment_mark
        leftside   = "{} === ".format(dcm) 
        bar1       = "{} ".format(dcm) + "="*(lwidth-(1+len(dcm))*2) + " {}".format(dcm)
        bar2       = leftside + "variables List".center(lwidth-2*(len(leftside))) + leftside[::-1]
        stack      = "\n\n\n" + bar1 + "\n" + bar2 + "\n" + bar1 + "\n{}\n".format(dcm)
        stack     += "{0}  {1} :   {2}\n".format( dcm, "name".ljust(30), "value".ljust(50) )
        stack     += dcm + " " + "-"*(lwidth-3) + "\n"
        for key,val in vdict.items():
            stack += "{0} {1:>30} : {2:>50}\n".format( dcm, key, val )
        stack     += dcm + " " + "-"*(lwidth-3) + "\n"
        replaced  += [ stack ]
        
        
    # ------------------------------------------------- #
    # --- [6] return                                --- #
    # ------------------------------------------------- #
    if ( replace_expression ):
        if ( outFile is not None ):
            text = "".join( replaced )
            with open( outFile, "w" ) as f:
                f.write( text )
            print( "[replace__variableDefinition.py] output :: {}".format( outFile ) )
        if ( not( silent ) ):
            print( "[replace__variableDefinition.py] replaced lines is returned." )
        return( replaced )
    else:
        if ( not( silent ) ):
            print( "[replace__variableDefinition.py] variables dictionary is returned. " )
        return( vdict    )


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):

    # ------------------------------------------------- #
    # --- [1] define parametres                     --- #
    # ------------------------------------------------- #
    inpFile = "test/replace_sample_2.conf"
    outFile = "test/replace_sample_2.out"
    table   = { "@val_frm_tbl":"value_from_table" }
    
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
    append__variableList=True 
    ret   = replace__variableDefinition( inpFile=inpFile, outFile=outFile, \
                                         table=table, comment_mark="$", \
                                         append__variableList=append__variableList )
    text  = "".join( ret )
    print( text )
