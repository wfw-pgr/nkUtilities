import os, sys


# ========================================================= #
# ===  color print function                             === #
# ========================================================= #

def cprint( statement=None, color=None, return__color_dict=False, end="\n", display=True ):

    # ------------------------------------------------- #
    # --- [1] color dictionary                      --- #
    # ------------------------------------------------- #
    color_dict = { "black"     : "\033[30m",\
                   "red"       : "\033[31m",\
                   "green"     : "\033[32m",\
                   "yellow"    : "\033[33m",\
                   "blue"      : "\033[34m",\
                   "magenta"   : "\033[35m",\
                   "cyan"      : "\033[36m",\
                   "white"     : "\033[37m",\
                   "default"   : "\033[39m",\
                   "bold"      : "\033[1m" ,\
                   "underline" : "\033[4m" ,\
                   "invisible" : "\033[08m",\
                   "reverce"   : "\033[07m",\
                   "bg_black"  : "\033[40m",\
                   "bg_red"    : "\033[41m",\
                   "bg_green"  : "\033[42m",\
                   "bg_yellow" : "\033[43m",\
                   "bg_blue"   : "\033[44m",\
                   "bg_magenta": "\033[45m",\
                   "bg_cyan"   : "\033[46m",\
                   "bg_white"  : "\033[47m",\
                   "bg_default": "\033[49m",\
                   "reset"     : "\033[0m"    }
    
    # ------------------------------------------------- #
    # --- [2] return color dictionary               --- #
    # ------------------------------------------------- #
    if ( return__color_dict ):
        return( color_dict )

    # ------------------------------------------------- #
    # --- [3] return color expression               --- #
    # ------------------------------------------------- #
    if   ( color is not None ):
        color = color.lower()
        if ( not( color in color_dict ) ):
            print( "\033[31m",end="" )
            print( "[cprint.py]     color is not included in color_dict.. [ERROR] " )
            print( "[cprint.py]     color_dict == {0} ".format( list( color_dict.keys() ) ) )
            print("\033[0m", end=""  )
            return()
        if ( statement is None ):
            return( color_dict[color] )
    else:
        color = "red"
        
    # ------------------------------------------------- #
    # --- [4] print statement / return expression   --- #
    # ------------------------------------------------- #
    if ( statement is not None ):
        ret = color_dict[color] + statement + color_dict["reset"]
        if ( display ):
            print( ret, end=end )
        return( ret )
    else:
        print()
        return( color_dict )


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #
if ( __name__=="__main__" ):
    
    ret = cprint( "Hello World!!" )
    ret = cprint( "I am cprint.", color="blue" )
    ret = cprint( statement="A procedure to print colorfully.", color="Yellow" )
    ret = cprint()
    ret = cprint( statement="as a variable.", color="blue", display=False )
    print( ret )
