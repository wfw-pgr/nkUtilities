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
    if ( configType.lower() in [ "plot.def", "plot_def", "plot1d_def" ] ):
        config["FigSize"]         = (6,6)
        config["plt_position"]    = [0.12,0.12,0.92,0.92]
        config["plt_linewidth"]   = 1.0
        config["plt_linestyle"]   = "--"
        config["plt_marker"]      = None
        config["plt_markersize"]  = 4.0
        config["plt_markerwidth"] = 1.0
        config["xTitle"]          = "x"
        config["yTitle"]          = "y"
        config["grid_sw"]         = True
        config["xMajor_Nticks"]   = 5
        config["yMajor_Nticks"]   = 5
        config["xTitle_FontSize"] = 16
        config["yTitle_FontSize"] = 16
        config["xMajor_FontSize"] = 10
        config["yMajor_FontSize"] = 10
        config["leg_location"]    = "best"
        config["leg_FontSize"]    = 12

    # ------------------------------------------------- #
    # --- [3] マーカープロット設定                  --- #
    # ------------------------------------------------- #
    if ( configType.lower() in [ "plot.marker", "plot_marker", "plot1d_mark" ] ):
        config["plt_marker"]      = "o"
        config["plt_markersize"]  = 4.0
        config["plt_markerwidth"] = 1.0
        
    # ------------------------------------------------- #
    # --- [4] 対数プロット用設定                    --- #
    # ------------------------------------------------- #
    if ( configType.lower() in [ "plot.log", "plot_log", "plot1D_log" ] ):
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
    if ( configType.lower() in [ "cmap.def", "cmap_def", "cmap2d_def" ] ):
        config["FigSize"]          = (6,6)
        config["xMajor_FontSize"]  = 14   # it is better to set bigger than plot1d
        config["yMajor_FontSize"]  = 14
        config["xTitle_FontSize"]  = 20
        config["yTitle_FontSize"]  = 20
        config["cmp_position"]     = [0.14,0.14,0.84,0.84]
        config["cmp_AutoLevel"]    = True
        config["cmp_xAutoRange"]   = True
        config["cmp_yAutoRange"]   = True
        config["cmp_xAutoTicks"]   = True
        config["cmp_yAutoTicks"]   = True
        config["cmp_nLevels"]      = 255
        config["cmp_ColorTable"]   = "jet"
        config["clb_position"]     = [0.50,0.89,0.88,0.91]
        config["clb_title"]        = None
        config["clb_FontSize"]     = 14
        config["clb_title_pos"]    = [0.65,0.935]
        config["grid_sw"]          = True
        config["grid_minor_sw"]    = True
        config["grid_alpha"]       = 0.9
        config["grid_color"]       = "darkgrey"
        config["grid_linestyle"]   = ":"
        config["grid_linewidth"]   = 0.8
        config["grid_minor_color"] = "darkgrey"
        config["grid_minor_style"] = ":"
        config["grid_minor_width"] = 0.6
        config["grid_minor_alpha"] = 0.9

        
    # ------------------------------------------------- #
    # --- [6] 2次元コンターマップ用設定             --- #
    # ------------------------------------------------- #
    if ( configType.lower() in [ "contour.def", "contour_def" ] ):
        config["cnt_nLevels"]     = 30
        config["cnt_AutoLevel"]   = True
        config["cnt_color"]       = "grey"
        config["cnt_linewidth"]   = 1.0

    # ------------------------------------------------- #
    # --- [7] ベクトルプロット用標準設定            --- #
    # ------------------------------------------------- #
    if ( configType.lower() in [ "vector.def", "vector_def" ] ):
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
    if ( configType.lower() in [ "noaxis" ] ):
        config["xTitle"]          = ""
        config["yTitle"]          = ""
        config["xMajor_NoLabel"]  = True
        config["yMajor_NoLabel"]  = True
        config["MinimalOut"]      = True
        config["clb_nLabel"]      = 0
        config["clb_sw"]          = False

    # ------------------------------------------------- #
    # --- [9] 2nd Axis Settings                     --- #
    # ------------------------------------------------- #
    if ( configType.lower() in ["plot.ax2"] ):
        config["FigSize"]             = (6,6)
        config["plt_position"]        = [ 0.14,0.14,0.86, 0.86 ]
        config["grid_sw"]             = True
        config["xTitle_FontSize"]     = 16
        config["yTitle_FontSize"]     = 16
        config["xMajor_FontSize"]     = 10
        config["yMajor_FontSize"]     = 10
        config["leg_location"]        = "best"
        config["leg_FontSize"]        = 12
        config["ax2.yMajor.nticks"]   = 7
        config["ax2.yAutoRange"]      = True
        config["ax2.yMinor.sw"]	      = False
        config["ax2.yMinor.ntikcs"]   = 2
        config["ax2.legend.position"] = [0.65,0.75]
        
    return( config )



# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):

    x_, y_, z_ = 0, 1, 2

    # ------------------------------------------------- #
    # --- [1] plot config settings sample           --- #
    # ------------------------------------------------- #
    import numpy as np
    import nkUtilities.plot1D       as pl1
    import nkUtilities.load__config as lcf
    
    pngFile  = "test/configSettings_sample_plot.png"
    config   = lcf.load__config()
    config   = configSettings( configType="plot.def"   , config=config )
    config   = configSettings( configType="plot.marker", config=config )
    xAxis    = np.linspace( 0.0, 1.0, 101 )
    yAxis1   = np.sin( xAxis * 2.0*np.pi )
    yAxis2   = np.cos( xAxis * 2.0*np.pi )

    fig     = pl1.plot1D( config=config, pngFile=pngFile )
    fig.add__plot( xAxis=xAxis, yAxis=yAxis1, label="sin(x)" )
    fig.add__plot( xAxis=xAxis, yAxis=yAxis2, label="cos(x)" )
    fig.add__legend()
    fig.set__axis()
    fig.save__figure()

    # ------------------------------------------------- #
    # --- [2] cmap config settings sample           --- #
    # ------------------------------------------------- #
    import nkUtilities.load__config   as lcf
    import nkUtilities.cMapTri        as cmt
    config   = lcf.load__config()
    config   = configSettings( configType="cMap_def", config=config )
    pngFile  = "test/configSettings_sample_cMap.png"
    
    import nkUtilities.equiSpaceGrid as esg
    x1MinMaxNum = [ -1.0, 1.0, 21 ]
    x2MinMaxNum = [ -1.0, 1.0, 21 ]
    x3MinMaxNum = [  0.0, 0.0,  1 ]
    coord       = esg.equiSpaceGrid( x1MinMaxNum=x1MinMaxNum, x2MinMaxNum=x2MinMaxNum, \
                                     x3MinMaxNum=x3MinMaxNum, returnType = "point" )
    coord[:,z_] = np.sqrt( coord[:,x_]**2 + coord[:,y_]**2 )
    
    cmt.cMapTri( xAxis=coord[:,x_], yAxis=coord[:,y_], cMap=coord[:,z_], \
    	         pngFile=pngFile, config=config )

