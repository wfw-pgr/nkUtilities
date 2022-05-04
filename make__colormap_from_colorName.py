import matplotlib.colors as mcl


# ========================================================= #
# ===  make colormap from designated color name         === #
# ========================================================= #
def make__colormap_from_colorName( colorNames=None ):

    # ------------------------------------------------- #
    # --- [1] arguments                             --- #
    # ------------------------------------------------- #
    if (      colorNames     is None     ):
        sys.exit( "[make__colormap_from_colorName.py] colorNames == ???" )
    if ( type(colorNames)    is not list ):
        sys.exit( "[make__colormap_from_colorName.py] colorNames is not list type... [ERROR]" )
    if ( type(colorNames[0]) is not str  ):
        sys.exit( "[make__colormap_from_colorName.py] colorNames is not list of string.. [ERROR]")
        
    cmap       = mcl.ListedColormap( colorNames )
    return( cmap )


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    colorNames = [ "green", "blue", "red" ]
    cmap       = make__colormap_from_colorName( colorNames=colorNames )
    print( cmap )
