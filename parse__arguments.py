import argparse

# ========================================================= #
# ===  general arguments parser ver.2                   === #
# ========================================================= #

def parse__arguments( silent=False ):
    
    # ---------------------------------------- #
    # --- [1] 引数パーサー 定義 / リスト   --- #
    # ---------------------------------------- #
    parser = argparse.ArgumentParser()

    # ------------------------------------------------- #
    # --- [2] 引数 リスト                           --- #
    # ------------------------------------------------- #
    parser.add_argument("--job"      , help="Job Name. "             )
    parser.add_argument("--id"       , help="ID  Name. "             )
    parser.add_argument("--dir"      , help="directory name"         )
    parser.add_argument("--mode"     , help="mode select."           )
    parser.add_argument("--key"      , help="key variables."         )
    parser.add_argument("--file"     , help="file name"              ) 
    parser.add_argument("--inpFile"  , help="input file name"        ) 
    parser.add_argument("--outFile"  , help="output file name"       ) 
    parser.add_argument("--MinMaxNum", help="Min / Max / Num"        )
    parser.add_argument("--size"     , help="Size of Array."         )
    parser.add_argument("--integer"  , help="General arg for int"    )
    parser.add_argument("--float"    , help="General arg for float"  )
    parser.add_argument("--string"   , help="General arg for string" )
    parser.add_argument("--array"    , help="General arg for array"  )

    # ------------------------------------------------- #
    # --- [3] 引数をセット                          --- #
    # ------------------------------------------------- #
    args = parser.parse_args()

    # ------------------------------------------------- #
    # --- [4] 返却用辞書 キー 準備 / 初期化         --- #
    # ------------------------------------------------- #
    rets  = {}
    items = [ "job", "id", "dir", "mode", "key", "MinMaxNum", "size", "file", \
              "integer", "float", "string", "array", "inpFile", "outFile" ]
    for item in items: rets[item] = None

    # ------------------------------------------------- #
    # --- [5] 引数定義 ( 文字列引数群 )             --- #
    # ------------------------------------------------- #
    #  -- [5-1] job                                 --  #
    if ( args.job     ): rets["job"]     = str(args.job)
    #  -- [5-2] id                                  --  #
    if ( args.id      ): rets["id"]      = str(args.id )
    #  -- [5-3] dir                                  --  #
    if ( args.dir     ): rets["dir"]     = str(args.dir)
    #  -- [5-4] mode                                 --  #
    if ( args.mode    ): rets["mode"]    = str(args.mode)
    #  -- [5-5] key                                  --  #
    if ( args.key     ): rets["key"]     = str(args.key)
    #  -- [5-6] file                                 --  #
    if ( args.file    ): rets["file"]    = str(args.file)
    #  -- [5-7] file                                 --  #
    if ( args.inpFile ): rets["inpFile"] = str(args.inpFile)
    #  -- [5-8] file                                 --  #
    if ( args.outFile ): rets["outFile"] = str(args.outFile)
    

    # ------------------------------------------------- #
    # --- [6] 引数定義 ( 配列  引数群 )             --- #
    # ------------------------------------------------- #
    #  -- [6-1] MinMaxNum                           --  #
    if ( args.MinMaxNum  ):
        strlst            = ( args.MinMaxNum.replace( "[","" ) ).replace( "]","" )   # - "[,]" 消去 - #
        fltarr            = [ float(s) for s in strlst.split( "," ) ]
        rets["MinMaxNum"] = [ fltarr[0], fltarr[1], int( fltarr[2] ) ]
    #  -- [6-2] size                                --  #
    if ( args.size       ):
        strlst            = ( args.size     .replace( "[","" ) ).replace( "]","" )   # - "[,]" 消去 - #
        rets["size"]      = [ int(s) for s in strlst.split( "," ) ]

    # ------------------------------------------------- #
    # --- [7] 代表的引数定義                        --- #
    # ------------------------------------------------- #
    #  -- [7-1] integer                             --  #
    if ( args.integer):
        rets["integer"] =   int( args.integer )
    #  -- [7-2] float                               --  #
    if ( args.float  ):
        rets["float"]   = float( args.float   )
    #  -- [7-3] string                              --  #
    if ( args.string ):
        rets["string"]  =   str( args.string  )
    #  -- [7-4] array                               --  #
    if ( args.array  ):
        strlst          = ( args.array.replace( "[","" ) ).replace( "]","" )   # - "[,]" 消去 - #
        rets["array"]   = [ int(s) for s in strlst.split( "," ) ]
        
    # ---------------------------------------- #
    # --- [8] 返却                         --- #
    # ---------------------------------------- #
    return( rets )
