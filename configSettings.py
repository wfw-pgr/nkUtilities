import nkUtilities.load__config as lcf

# ========================================================= #
# ===  コンフィグの設定用 ルーチン                      === #
# ========================================================= #
def configSettings( configType=None, config=None ):
    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    if ( configType is None ): configType = "cMap2D_def"
    if ( config     is None ): config     = lcf.load__config()
    
    # ------------------------------------------------- #
    # --- [2] 1次元プロット用 デフォルト設定        --- #
    # ------------------------------------------------- #
    if ( configType == "plot1D_def" ):
        config["FigSize"]         = (3.5,3.5)
        config["grid_sw"]         = True
        config["plt_position"]    = [0.24,0.24,0.93,0.93]
        config["xTitle_FontSize"] = 16
        config["yTitle_FontSize"] = 16
        config["xMajor_Nticks"]   = 5
        config["yMajor_Nticks"]   = 5
        config["xMajor_FontSize"] = 10
        config["yMajor_FontSize"] = 10
        config["leg_location"]    = "best"
        config["leg_FontSize"]    = 12

    # ------------------------------------------------- #
    # --- [3] マーカープロット設定                  --- #
    # ------------------------------------------------- #
    if ( configType == "plot1D_mark" ):
        config["plt_marker"]      = "D"
        config["plt_markersize"]  = 4.0
        config["plt_linewidth"]	  = 0.0
        
    # ------------------------------------------------- #
    # --- [4] 対数プロット用設定                    --- #
    # ------------------------------------------------- #
    if ( configType == "plot1D_log" ):
        config["plt_xlog"]        = True
        config["plt_ylog"]        = True
        config["grid_sw"]         = True
        config["grid_color"]      = "dimgray"
        config["grid_width"]      = 0.6
        config["grid_style"]      = "-"
        config["MinorGrid_sw"]    = True
        config["MinorGrid_color"] = "gray"
        config["MinorGrid_width"] = 0.3
        config["MinorGrid_style"] = "-"
    
    # ------------------------------------------------- #
    # --- [5] 2次元カラーマップ用設定               --- #
    # ------------------------------------------------- #
    if ( configType == "cMap2D_def" ):
        config["FigSize"]         = (5,5)
        config["xMajor_FontSize"] = 12
        config["yMajor_FontSize"] = 12
        config["xTitle_FontSize"] = 16
        config["yTitle_FontSize"] = 16
        config["cmp_Position"]    = [0.22,0.22,0.82,0.82]
        config["cmp_AutoLevel"]   = True
        config["cmp_xAutoRange"]  = True
        config["cmp_yAutoRange"]  = True
        config["cmp_xAutoTicks"]  = True
        config["cmp_yAutoTicks"]  = True
        config["cmp_nLevels"]     = 255
        config["cmp_ColorTable"]  = "jet"
        config["clb_Title"]       = None
        config["clb_FontSize"]    = 12
        config["clb_Title_pos"]   = [0.70,0.95]

    # ------------------------------------------------- #
    # --- [6] 2次元コンターマップ用設定             --- #
    # ------------------------------------------------- #
    if ( configType == "contour_def" ):
        config["cnt_nLevels"]     = 30
        config["cnt_AutoLevel"]   = True
        config["cnt_color"]       = "grey"
        config["cnt_linewidth"]   = 1.0

    # ------------------------------------------------- #
    # --- [7] ベクトルプロット用標準設定            --- #
    # ------------------------------------------------- #
    if ( configType == "vector_def" ):
        config["vec_nvec_x"]      = 12
        config["vec_nvec_y"]      = 12
        config["vec_color"]       = "springgreen"
        config["vec_AutoScale"]   = True
        config["vec_scale"]       = 1.0
        config["vec_width"]       = 0.01
        config["vec_headwidth"]   = 2.5
        config["vec_headlength"]  = 4.5
        config["vec_pivot"]       = "mid"

    # ------------------------------------------------- #
    # --- [8] 軸 消去設定                           --- #
    # ------------------------------------------------- #
    if ( configType == "NoAxis" ):
        config["xTitle"]          = ""
        config["yTitle"]          = ""
        config["xMajor_NoLabel"]  = True
        config["yMajor_NoLabel"]  = True
        config["MinimalOut"]      = True
        config["clb_nLabel"]      = 0
        config["clb_sw"]          = False

    # ------------------------------------------------- #
    # --- [9] Filter Clear ( フィルタ初期化 )       --- #
    # ------------------------------------------------- #
    if ( configType == "FilterClear" ):
        config["flt_median"]   = 0.0
        config["flt_fourier"]  = 0.0
        config["flt_gaussian"] = 0.0
        config["flt_spline"]   = 0.0
        config["flt_linear"]   = 0.0
        config["flt_ntimes"]   = 0
        
