import os, sys, subprocess

# ========================================================= #
# ===  execute__commands.py                             === #
# ========================================================= #

def execute__commands( commands_list=[], shell=False ):

    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    if ( commands_list is None ): sys.exit( "[execute__commands.py] commands_list == ??? " )

    # ------------------------------------------------- #
    # --- [2] execution                             --- #
    # ------------------------------------------------- #

    if ( shell ):
        print()
        print( "-"*27 + "   execute  commands   " + "-"*27 )
        print()
        for command in commands_list:
            print( command )
            subprocess.call( command.split() )
        print()
        print( "-"*77 )
        print()
        print()

    else:
        print()
        print( "-"*27 + "   execute  commands   " + "-"*27 )
        print()
        for command in commands_list:
            print( command )
            subprocess.call( command, shell=True )
        print()
        print( "-"*77 )
        print()
        print()
        
    return()

# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #

if ( __name__=="__main__" ):

    commands_list = [ "ls", "pwd", "cd dat", "echo Hello", "cd ../", "pwd", "ls" ]
    execute__commands( commands_list=commands_list )
