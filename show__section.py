import os, sys


# ========================================================= #
# ===  show__section                                    === #
# ========================================================= #

def show__section( section=None, length=71, bar_mark="-", comment_mark="#", sidebarLen=3, sideSpaceLen=1, \
                   newLine=True ):

    # ------------------------------------------------- #
    # --- [1] arguments                             --- #
    # ------------------------------------------------- #
    if ( section is None ): sys.exit( "[show__section.py] section == ???" )

    # ------------------------------------------------- #
    # --- [2] Length determination                  --- #
    # ------------------------------------------------- #
    sectLen        = len(section)
    uprlwrbar_Len  = length - ( len( comment_mark ) + sideSpaceLen )*2
    space_t_Len    = ( length - len(section) - 2*( len( comment_mark ) + sideSpaceLen*2 + sidebarLen ) )
    space_f_Len    = space_t_Len // 2
    space_r_Len    = space_t_Len - space_f_Len

    # ------------------------------------------------- #
    # --- [3] preparation                           --- #
    # ------------------------------------------------- #
    space_f        = " "*space_f_Len
    space_r        = " "*space_r_Len
    side1          = comment_mark + " "*sideSpaceLen
    side2          = comment_mark + " "*sideSpaceLen + bar_mark*sidebarLen + " "*sideSpaceLen

    # ------------------------------------------------- #
    # --- [4] section contents                      --- #
    # ------------------------------------------------- #
    line1          = side1 + bar_mark*uprlwrbar_Len + side1[::-1] + "\n"
    line2          = side2 + space_f + section + space_r + side2[::-1] + "\n"
    if ( newLine ):
        lines = "\n" + line1 + line2 + line1 + "\n"
    print( lines )
    return( lines )


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    show__section( section="sample execution" )
