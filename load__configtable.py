import os, sys, re
import numpy as np

# ========================================================= #
# ===  load config table                                === #
# ========================================================= #
def load__configtable( inpFile=None, returnType="dict-dict" ):

    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    if ( inpFile is None ): sys.exit( "[load__configtable.py] inpFile == ???" )
    
    # ------------------------------------------------- #
    # --- [2] Data Load                             --- #
    # ------------------------------------------------- #
    with open( inpFile ) as f:
        configtable = f.readlines()
    varNames = ( ( configtable[0] ).strip( " #" ) ).split()
    varTypes = ( ( configtable[1] ).strip( " #" ) ).split()
    
    if ( len( varNames ) != len( varTypes ) ):
        print( "[load__configtable.py] Incompatible number of columns between line1 & line2. [ERROR]" )
        print( "[load__configtable.py] line1 :  ".format( varNames ) )
        print( "[load__configtable.py] line2 :  ".format( varTypes ) )
        sys.exit()
    else:
        nColumns = len( varNames )

    # ------------------------------------------------- #
    # --- [3] generate Dictionary ( physical Num )  --- #
    # ------------------------------------------------- #
    table  = {}
    keys   = []

    for row in configtable:
        if   ( len( row.strip() ) == 0 ):
            continue
        elif ( (row.strip())[0] == "#" ):
            continue
        else:

            stacklist  = []
            rowsplit   = row.split()
            
            for ik,(hkey,htype) in enumerate( zip(varNames,varTypes) ):

                if   ( htype.lower() == "none" ):
                    stacklist += [ None ]
                    rowsplit.pop(0)
                elif ( htype.lower() in ["long", "integer"]      ):
                    stacklist += [   int(rowsplit.pop(0)) ]
                elif ( htype.lower() in ["float","double","real"]):
                    stacklist += [ float(rowsplit.pop(0)) ]
                elif ( htype.lower() in ["string"]               ):
                    stacklist += [   str(rowsplit.pop(0)) ]
                elif ( htype.lower() in ["logical", "bool"]      ):
                    value = str(rowsplit.pop(0))
                    if   ( value.lower() in [  "true", "t" ] ):
                        stacklist += [ True  ]
                    elif ( value.lower() in [ "false", "f" ] ):
                        stacklist += [ False ]
                    else:
                        print( "[load__configtable] type is logical, but the value is wrong. " )
                elif ( htype.lower() in ["array","fltarr"]       ):
                    value        = "".join( rowsplit )
                    pattern      = r"\[(.+)\]"
                    sarr         = re.search( pattern, value )
                    arrcontent   = ( sarr.group(1) ).split(",")
                    lst          = [ float(s) for s in arrcontent ]
                    stacklist   += [ lst ]
                    rowsplit     = " ".join( ( ( " ".join(rowsplit).split("]") )[1:] ) ).split()

                elif ( htype.lower() in [ "intarr", "intarray" ] ):
                    value        = "".join( rowsplit )
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
                    rowsplit     = " ".join( ( ( " ".join(rowsplit).split("]") )[1:] ) ).split()
                    stacklist   += [ ilst ]
                else:
                    print("[load__configtable.py] Unknown Object in load__configtable.py :: {0}"\
                          .format(inpFile) )
            key         = stacklist[0]
            table[key]  = { hkey:hval for hkey,hval in zip(varNames,stacklist) }
            keys.append( key )


    # ------------------------------------------------- #
    # --- [3] return Type                           --- #
    # ------------------------------------------------- #
    if   ( returnType.lower() == "dict-dict" ):
        return( table )
    
    elif ( returnType.lower() == "dict-list" ):
        return( { key:[ (table[key])[var] for var in varNames ] for key in keys } )
    
    elif ( returnType.lower() == "list-dict" ):
        return( [ table[key] for key in keys ] )
    
    elif ( returnType.lower() == "list-list" ):
        return( [ [ table[key][var] for var in varNames ] for key in keys ] )
    else:
        print( "[load__configtable.py] returnType == {0} ?? ".format( returnType ) )
        print( "[load__configtable.py] default type :: dict-dict will be returned." )
        return( table )
            
                    
# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #
if ( __name__=="__main__" ):
    inpFile = "dat/arbitral.conf"
    ret = load__configtable( inpFile=inpFile )
    print( ret )
