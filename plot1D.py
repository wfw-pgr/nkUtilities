import sys, math
import nkUtilities.mpl_baseSettings
import nkUtilities.load__config     as lcf
import numpy                        as np
import matplotlib.pyplot            as plt
import matplotlib.ticker            as tic


# ========================================================= #
# === 1次元プロット描画用クラス                         === #
# ========================================================= #
class plot1D:
    
    # ------------------------------------------------- #
    # --- クラス初期化用ルーチン                    --- #
    # ------------------------------------------------- #
    def __init__( self, xAxis=None, yAxis=None, label=None, pngFile=None, config=None, window=False ):
        # ------------------------------------------------- #
        # --- 引数の引き渡し                            --- #
        # ------------------------------------------------- #
        self.xAxis     = xAxis
        self.yAxis     = yAxis
        self.label     = []
        self.DataRange = None
        self.xticks    = None
        self.yticks    = None
        self.config    = config
        # ------------------------------------------------- #
        # --- コンフィグの設定                          --- #
        # ------------------------------------------------- #
        if ( self.config is     None ): self.config                = lcf.load__config()
        if ( label       is not None ): self.label.append( label )
        if ( pngFile     is not None ): self.config["pngFile"]     = pngFile
        # ------------------------------------------------- #
        # --- 描画領域の作成                            --- #
        # ------------------------------------------------- #
        #  -- 描画領域                                  --  #
        pos      = self.config["plt_position"]
        self.fig = plt.figure( figsize=self.config["FigSize"]  )
        self.ax1 = self.fig.add_axes( [ pos[0], pos[1], pos[2]-pos[0], pos[3]-pos[1] ] )
        self.set__axis()
        self.set__grid()
        # ------------------------------------------------- #
        # --- 2nd Axis settings                         --- #
        # ------------------------------------------------- #
        self.ax2           = None
        self.DataRange_ax2 = None
        # ------------------------------------------------- #
        # --- 速攻描画                                  --- #
        # ------------------------------------------------- #
        instantOut = False
        #  -- もし yAxis が渡されていたら，即，描く      --  #
        if ( self.yAxis is not None ):
            #   - xAxis がなければインデックスで代用    -   #
            if ( self.xAxis is None ):       
                self.xAxis = np.arange( float( self.yAxis.size ) )
            instantOut = True
            #   - プロット描きだし                      -   #
            self.add__plot( self.xAxis, self.yAxis, label=label )
            self.set__axis()
            if ( self.config["leg_sw"] ): self.add__legend()
        #  -- カーソル (x) がある時．                   --  #
        if ( self.config["cursor_x"] is not None ):
            self.add__cursor( xAxis=self.config["cursor_x"] )
            instantOut = True
        #  -- カーソル (y) がある時．                   --  #
        if ( self.config["cursor_y"] is not None ):
            self.add__cursor( yAxis=self.config["cursor_y"] )
            instantOut = True
        #  -- もし 何かを描いてたら，出力する．         --  #
        if ( instantOut ):
            self.save__figure( pngFile=self.config["pngFile"] )
        # -- それ以外の場合は，外部から直接関数を読んでもらう． -- #
        #  -- window に表示する．                       --  #
        if ( window ):
            self.display__window()
        
    # ========================================================= #
    # ===  プロット 追加                                    === #
    # ========================================================= #
    def add__plot( self, xAxis=None, yAxis=None, label=None, color=None, alpha=None, \
                   linestyle=None, linewidth=None, \
                   marker=None, markersize=None, markerwidth=None ):
        # ------------------------------------------------- #
        # --- 引数チェック                              --- #
        # ------------------------------------------------- #
        if ( yAxis       is None ): yAxis       = self.yAxis
        if ( xAxis       is None ): xAxis       = self.xAxis
        if ( yAxis       is None ): sys.exit( " [add__plot] yAxis == ?? " )
        if ( xAxis       is None ): xAxis       = np.arange( yAxis.size ) # - インデックス代用 - #
        if ( label       is None ): label       = ' '*self.config["leg_labelLength"]
        if ( color       is None ): color       = self.config["plt_color"]
        if ( alpha       is None ): alpha       = self.config["plt_alpha"]
        if ( linestyle   is None ): linestyle   = self.config["plt_linestyle"]
        if ( linewidth   is None ): linewidth   = self.config["plt_linewidth"]
        if ( marker      is None ): marker      = self.config["plt_marker"]
        if ( markersize  is None ): markersize  = self.config["plt_markersize"]
        if ( markerwidth is None ): markerwidth = self.config["plt_markerwidth"]
        # ------------------------------------------------- #
        # --- フィルタリング                            --- #
        # ------------------------------------------------- #
        # xAxis, yAxis = gfl.generalFilter( xAxis=xAxis, yAxis=yAxis, config=self.config )
        # ------------------------------------------------- #
        # --- 軸設定                                    --- #
        # ------------------------------------------------- #
        self.xAxis   = xAxis
        self.yAxis   = yAxis
        self.update__DataRange( xAxis=xAxis, yAxis=yAxis )
        self.set__axis()
        if ( self.config["plt_colorStack"] is not None ):
            color    = ( self.config["plt_colorStack"] ).pop(0)
        # ------------------------------------------------- #
        # --- プロット 追加                             --- #
        # ------------------------------------------------- #
        self.ax1.plot( xAxis, yAxis , \
                       color =color , linestyle =linestyle , \
                       label =label , linewidth =linewidth , \
                       marker=marker, markersize=markersize, \
                       markeredgewidth=markerwidth, alpha =alpha   )
        

    # ========================================================= #
    # ===  プロット 追加                                    === #
    # ========================================================= #
    def add__errorbar( self, xAxis=None, yAxis=None, xerr=None, yerr=None, \
                       capsize=None, capthick=None, fmt="none", \
                       label=None, color=None, alpha=None, \
                       linestyle=None, linewidth=None, marker=None, markersize=None ):
        # ------------------------------------------------- #
        # --- 引数チェック                              --- #
        # ------------------------------------------------- #
        if ( yAxis       is None ): yAxis       = self.yAxis
        if ( xAxis       is None ): xAxis       = self.xAxis
        if ( yAxis       is None ): sys.exit( " [add__errorbar] yAxis == ?? " )
        if ( xAxis       is None ): xAxis       = np.arange( yAxis.size ) # - インデックス代用 - #
        if ( color       is None ): color       = self.config["plt_color"]
        if ( alpha       is None ): alpha       = self.config["plt_alpha"]
        if ( linewidth   is None ): linewidth   = self.config["plt_linewidth"] * 0.8
        if ( linestyle   is None ): linestyle   = self.config["plt_linestyle"]
        if ( marker      is None ): marker      = self.config["plt_marker"]
        if ( markersize  is None ): markersize  = self.config["plt_markersize"]
        if ( capthick    is None ): capthick    = self.config["plt_error_capthick"]
        if ( capsize     is None ): capsize     = self.config["plt_error_capsize"]
        if ( ( xerr is None ) and ( yerr is None ) ):
            sys.exit("[add__errorbar] xerr=None & yerr=None ")
        if ( self.config["plt_colorStack"] is not None ):
            color    = ( self.config["plt_colorStack"] ).pop(0)
        # ------------------------------------------------- #
        # --- フィルタリング                            --- #
        # ------------------------------------------------- #
        # xAxis, yAxis = gfl.generalFilter( xAxis=xAxis, yAxis=yAxis, config=self.config )
        # ------------------------------------------------- #
        # --- プロット 追加                             --- #
        # ------------------------------------------------- #
        self.ax1.errorbar( xAxis, yAxis, xerr=xerr, yerr=yerr, \
                           fmt=fmt, capsize=capsize, capthick=capthick, \
                           ecolor=color , elinestyle=linestyle, elinewidth=linewidth , \
                           marker=marker, markersize=markersize,  \
                           alpha=alpha )


    # ========================================================= #
    # ===  軸 レンジ 自動調整用 ルーチン                    === #
    # ========================================================= #
    def set__axis( self, xRange=None, yRange=None ):
        # ------------------------------------------------- #
        # --- 自動レンジ調整   ( 優先順位 2 )           --- #
        # ------------------------------------------------- #
        #  -- オートレンジ (x)                          --  #
        if ( ( self.config["plt_xAutoRange"] ) and ( self.DataRange is not None ) ):
            ret = self.auto__griding( vMin=self.DataRange[0], vMax=self.DataRange[1], \
                                      nGrid=self.config["xMajor_Nticks"] )
            self.config["plt_xRange"] = [ ret[0], ret[1] ]
        #  -- オートレンジ (y)                          --  #
        if ( ( self.config["plt_yAutoRange"] ) and ( self.DataRange is not None ) ):
            ret = self.auto__griding( vMin=self.DataRange[2], vMax=self.DataRange[3], \
                                      nGrid=self.config["yMajor_Nticks"] )
            self.config["plt_yRange"] = [ ret[0], ret[1] ]
        # ------------------------------------------------- #
        # --- 軸範囲 直接設定  ( 優先順位 1 )           --- #
        # ------------------------------------------------- #
        if ( xRange is not None ): self.config["plt_xRange"] = xRange
        if ( yRange is not None ): self.config["plt_yRange"] = yRange
        self.ax1.set_xlim( self.config["plt_xRange"][0], self.config["plt_xRange"][1] )
        self.ax1.set_ylim( self.config["plt_yRange"][0], self.config["plt_yRange"][1] )
        # ------------------------------------------------- #
        # --- 軸タイトル 設定                           --- #
        # ------------------------------------------------- #
        self.ax1.set_xlabel( self.config["xTitle"], fontsize=self.config["xTitle_FontSize"] )
        self.ax1.set_ylabel( self.config["yTitle"], fontsize=self.config["yTitle_FontSize"] )
        # ------------------------------------------------- #
        # --- 目盛を調整する                            --- #
        # ------------------------------------------------- #
        self.set__ticks()


        
    # ========================================================= #
    # ===  軸 レンジ 自動調整用 ルーチン for axis2          === #
    # ========================================================= #
    def set__axis2( self, xRange=None, yRange=None ):
        # ------------------------------------------------- #
        # --- 自動レンジ調整   ( 優先順位 2 )           --- #
        # ------------------------------------------------- #
        #  -- オートレンジ (y)                          --  #
        if ( ( self.config["ax2.yAutoRange"] ) and ( self.DataRange_ax2 is not None ) ):
            ret = self.auto__griding( vMin=self.DataRange_ax2[2], vMax=self.DataRange_ax2[3], \
                                      nGrid=self.config["ax2.yMajor.nticks"] )
            self.config["ax2.yRange"] = [ ret[0], ret[1] ]
        # ------------------------------------------------- #
        # --- 軸範囲 直接設定  ( 優先順位 1 )           --- #
        # ------------------------------------------------- #
        if ( yRange is not None ): self.config["ax2.yRange"] = yRange
        self.ax2.set_ylim( self.config["ax2.yRange"][0], self.config["ax2.yRange"][1] )
        # ------------------------------------------------- #
        # --- 軸タイトル 設定                           --- #
        # ------------------------------------------------- #
        self.ax2.set_ylabel( self.config["ax2.yTitle"], fontsize=self.config["ax2.yTitle.fontsize"] )
        # ------------------------------------------------- #
        # --- 目盛を調整する                            --- #
        # ------------------------------------------------- #
        self.set__ticks2()

    # ========================================================= #
    # ===  軸目盛 設定 ルーチン for axis2                   === #
    # ========================================================= #
    def set__ticks2( self ):
        # ------------------------------------------------- #
        # --- 軸目盛 自動調整                           --- #
        # ------------------------------------------------- #
        #  -- 軸目盛 整数設定                           --  #
        ytick_dtype      = np.int32 if ( self.config["ax2.yMajor.integer"] ) else np.float64
        #  -- 軸目盛 自動調整 (y)                       --  #
        if ( self.config["ax2.yMajor.auto"] ):
            yMin, yMax   = self.ax2.get_ylim()
            self.yticks2 = np.linspace( yMin, yMax, self.config["ax2.yMajor.nticks"], dtype=ytick_dtype  )
        else:
            self.yticks2 = np.array( self.config["ax2.yMajor.ticks"], dtype=ytick_dtype )
        #  -- Minor 軸目盛                              --  #
        if ( self.config["ax2.yMinor.sw"] is False ):
            self.config["ax2.yMinor.nticks"] = 1
        self.ax2.yaxis.set_minor_locator( tic.AutoMinorLocator( self.config["ax2.yMinor.nticks"] ) )
        #  -- 軸目盛 調整結果 反映                      --  #
        self.ax2.set_yticks( self.yticks2 )
        # ------------------------------------------------- #
        # --- 軸目盛 スタイル                           --- #
        # ------------------------------------------------- #
        #  -- 対数表示 ( x,y )                          --  #
        if ( self.config["ax2.ylog"] ): self.ax2.set_yscale("log")
        #  -- 軸スタイル (y)                            --  #
        self.ax2.tick_params( axis     ="y", \
                              labelsize=self.config["ax2.yMajor.fontsize"], \
                              length   =self.config["ax2.yMajor.length"  ], \
                              width    =self.config["ax2.yMajor.width"   ]  )
        # ------------------------------------------------- #
        # --- 軸目盛  オフ                              --- #
        # ------------------------------------------------- #
        if ( self.config["ax2.yMajor.noLabel"] ):
            self.ax2.set_yticklabels( [ "" for i in self.ax2.get_yaxis().get_ticklocs() ] )

        

    # ========================================================= #
    # ===  軸の値 自動算出ルーチン                          === #
    # ========================================================= #
    def auto__griding( self, vMin=None, vMax=None, nGrid=5 ):

        eps = 1.e-8

        # ------------------------------------------------- #
        # --- check Arguments                           --- #
        # ------------------------------------------------- #
        if ( vMax  <  vMin ):
            sys.exit( "[auto__griding] ( vMin,vMax ) == ( {0},{1} ) ??? ".format( vMin, vMax ) )
        if ( nGrid <= 0 ):
            sys.exit( "[auto__griding] nGrid == {0} ??? ".format( nGrid ) )
        if ( vMin == vMax  ):
            return( [ vMin-eps, vMax+eps] )
            
        # ------------------------------------------------- #
        # --- auto grid making                          --- #
        # ------------------------------------------------- #
        minimum_tick = ( vMax - vMin ) / float( nGrid )
        magnitude    = 10**( math.floor( math.log( minimum_tick, 10 ) ) )
        significand  = minimum_tick / magnitude
        if   ( significand > 5    ):
            grid_size = 10 * magnitude
        elif ( significand > 2    ):
            grid_size =  5 * magnitude
        elif ( significand > 1    ):
            grid_size =  2 * magnitude
        else:
            grid_size =  1 * magnitude
        tick_below   = grid_size * math.floor( vMin / grid_size ) 
        tick_above   = grid_size * math.ceil ( vMax / grid_size )
        
        return( [tick_below,tick_above] )
        
        
    # ========================================================= #
    # ===  軸目盛 設定 ルーチン                             === #
    # ========================================================= #
    def set__ticks( self ):
        # ------------------------------------------------- #
        # --- 軸目盛 自動調整                           --- #
        # ------------------------------------------------- #
        #  -- 軸目盛 整数設定                           --  #
        xtick_dtype     = np.int32 if ( self.config["xMajor_integer"] ) else np.float64
        ytick_dtype     = np.int32 if ( self.config["yMajor_integer"] ) else np.float64
        #  -- 軸目盛 自動調整 (x)                       --  #
        if ( self.config["xMajor_auto"] ):
            xMin, xMax  = self.ax1.get_xlim()
            self.xticks = np.linspace( xMin, xMax, self.config["xMajor_Nticks"], dtype=xtick_dtype  )
        else:
            self.xticks = np.array( self.config["xMajor_ticks"], dtype=xtick_dtype )
        #  -- 軸目盛 自動調整 (y)                       --  #
        if ( self.config["yMajor_auto"] ):
            yMin, yMax  = self.ax1.get_ylim()
            self.yticks = np.linspace( yMin, yMax, self.config["yMajor_Nticks"], dtype=ytick_dtype  )

        else:
            self.yticks = np.array( self.config["yMajor_ticks"], dtype=ytick_dtype )
        #  -- Minor 軸目盛                              --  #
        if ( self.config["xMinor_sw"] is False ): self.config["xMinor_nticks"] = 1
        if ( self.config["yMinor_sw"] is False ): self.config["yMinor_nticks"] = 1
        self.ax1.xaxis.set_minor_locator( tic.AutoMinorLocator( self.config["xMinor_nticks"] ) )
        self.ax1.yaxis.set_minor_locator( tic.AutoMinorLocator( self.config["yMinor_nticks"] ) )
        #  -- 軸目盛 調整結果 反映                      --  #
        self.ax1.set_xticks( self.xticks )
        self.ax1.set_yticks( self.yticks )
        # ------------------------------------------------- #
        # --- 軸目盛 スタイル                           --- #
        # ------------------------------------------------- #
        #  -- 対数表示 ( x,y )                          --  #
        if ( self.config["plt_xlog"] ): self.ax1.set_xscale("log")
        if ( self.config["plt_ylog"] ): self.ax1.set_yscale("log")
        #  -- 軸スタイル (x)                            --  #
        self.ax1.tick_params( axis  ="x"                         , labelsize=self.config["xMajor_FontSize"], \
                              length=self.config["xMajor_length"], width    =self.config["xMajor_width"   ]  )
        #  -- 軸スタイル (y)                            --  #
        self.ax1.tick_params( axis  ="y"                         , labelsize=self.config["yMajor_FontSize"], \
                              length=self.config["yMajor_length"], width    =self.config["yMajor_width"   ]  )
        # ------------------------------------------------- #
        # --- 軸目盛  オフ                              --- #
        # ------------------------------------------------- #
        if ( self.config["xMajor_NoLabel"] ):
            self.ax1.set_xticklabels( ['' for i in self.ax1.get_xaxis().get_ticklocs()])
        if ( self.config["yMajor_NoLabel"] ):
            self.ax1.set_yticklabels( ['' for i in self.ax1.get_yaxis().get_ticklocs()])


    # =================================================== #
    # === データレンジ更新 for 複数プロット自動範囲用 === #
    # =================================================== #
    def update__DataRange( self, xAxis=None, yAxis=None, ax2=False ):
        # ------------------------------------------------- #
        # --- 引数チェック                              --- #
        # ------------------------------------------------- #
        if ( ( xAxis is None ) or ( yAxis is None ) ):
            sys.exit(  "[ERROR] [@update__DataRange] xAxis or yAxis is None [ERROR]" )

        if ( ax2 ):
            if ( self.DataRange_ax2 is None ):
                # -- DataRange_ax2 未定義のとき -- #
                self.DataRange_ax2    = np.array( [ np.min( xAxis ), np.max( xAxis ),
                                                    np.min( yAxis ), np.max( yAxis ) ] )
            else:
                # -- DataRange_ax2 を更新する -- #
                self.DataRange_ax2 = np.array( [ min( self.DataRange_ax2[0], np.min( xAxis ) ), \
                                                 max( self.DataRange_ax2[1], np.max( xAxis ) ), \
                                                 min( self.DataRange_ax2[2], np.min( yAxis ) ), \
                                                 max( self.DataRange_ax2[3], np.max( yAxis ) ), ] )
            return()
        # ------------------------------------------------- #
        # --- update DataRange for ax1                  --- #
        # ------------------------------------------------- #
        if ( self.DataRange is None ):
            # -- DataRange 未定義のとき -- #
            self.DataRange    = np.zeros( (4,) )
            self.DataRange[0] = np.min( xAxis )
            self.DataRange[1] = np.max( xAxis )
            self.DataRange[2] = np.min( yAxis )
            self.DataRange[3] = np.max( yAxis )
        else:
            # -- DataRange を更新する -- #
            if( self.DataRange[0] > np.min( xAxis ) ): self.DataRange[0] = np.min( xAxis )
            if( self.DataRange[1] < np.max( xAxis ) ): self.DataRange[1] = np.max( xAxis )
            if( self.DataRange[2] > np.min( yAxis ) ): self.DataRange[2] = np.min( yAxis )
            if( self.DataRange[3] < np.max( yAxis ) ): self.DataRange[3] = np.max( yAxis )

        
    # ========================================================= #
    # ===  グリッド / y=0 軸線 追加                         === #
    # ========================================================= #
    def set__grid( self ):
        # ------------------------------------------------- #
        # --- y=0 軸線 描画                             --- #
        # ------------------------------------------------- #
        if ( self.config["plt_y=0_sw"] ):
            self.ax1.axhline( y        = 0.0, \
                              linestyle=self.config["plt_y=0_linestyle"], \
                              color    =self.config["plt_y=0_color"]    , \
                              linewidth=self.config["plt_y=0_linewidth"] )
        # ------------------------------------------------- #
        # --- グリッド ( 主グリッド :: Major )          --- #
        # ------------------------------------------------- #
        if ( self.config["grid_sw"]      ):
            self.ax1.grid( b        =self.config["grid_sw"]       , \
                           which    ='major'                      , \
                           color    =self.config["grid_color"]    , \
                           alpha    =self.config["grid_alpha"]    , \
                           linestyle=self.config["grid_linestyle"], \
                           linewidth=self.config["grid_linewidth"]  )
        # ------------------------------------------------- #
        # --- グリッド ( 副グリッド :: Minor )          --- #
        # ------------------------------------------------- #
        if ( self.config["grid_minor_sw"] ):
            self.ax1.grid( b        =self.config["grid_minor_sw"]   , \
                           which    ='minor'                        , \
                           color    =self.config["grid_minor_color"], \
                           linestyle=self.config["grid_minor_style"], \
                           alpha    =self.config["grid_minor_alpha"], \
                           linewidth=self.config["grid_minor_width"]  )

            
    # ========================================================= #
    # ===  凡例を表示                                       === #
    # ========================================================= #
    def add__legend( self, loc=None, FontSize=None ):
        # ------------------------------------------------- #
        # --- 引数チェック                              --- #
        # ------------------------------------------------- #
        if ( loc      is not None ): self.config["leg_location"] = loc
        if ( FontSize is not None ): self.config["leg_FontSize"] = FontSize
        loc_interpretted = self.config["leg_location"].replace( "=", " " )
        # ------------------------------------------------- #
        # --- 凡例 描画                                 --- #
        # ------------------------------------------------- #
        if ( self.config["ax1.legend.position"] is not None ):
            bbox_to_anchor   = tuple( self.config["ax1.legend.position"] )
            loc_interpretted = "lower left"
        else:
            bbox_to_anchor = None
        self.ax1.legend( loc           =loc_interpretted, \
                         fontsize      =self.config["leg_FontSize"]     , \
                         ncol          =self.config["leg_nColumn" ]     , \
                         frameon       =self.config["leg_FrameOn" ]     , \
                         labelspacing  =self.config["leg_labelGap"]     , \
                         columnspacing =self.config["leg_columnGap"]    , \
                         handlelength  =self.config["leg_handleLength" ], \
                         bbox_to_anchor=bbox_to_anchor )
        
        if ( self.ax2 is not None ):
            if ( self.config["ax2.legend.position"] is not None ):
                bbox_to_anchor   = tuple( self.config["ax2.legend.position"] )
                loc_interpretted = "lower left"
            else:
                bbox_to_anchor = None
            self.ax2.legend( loc           =loc_interpretted, \
                             fontsize      =self.config["leg_FontSize"]     , \
                             ncol          =self.config["leg_nColumn" ]     , \
                             frameon       =self.config["leg_FrameOn" ]     , \
                             labelspacing  =self.config["leg_labelGap"]     , \
                             columnspacing =self.config["leg_columnGap"]    , \
                             handlelength  =self.config["leg_handleLength" ], \
                             bbox_to_anchor=bbox_to_anchor )

        

    # ========================================================= #
    # ===  カーソル 描画                                    === #
    # ========================================================= #
    def add__cursor( self, xAxis=None, yAxis=None, color=None, linestyle=None, linewidth=None ):
        # ------------------------------------------------- #
        # --- 引数チェック                              --- #
        # ------------------------------------------------- #
        if ( color     is not None ): self.config["cursor_color"] = color
        if ( linestyle is not None ): self.config["cursor_linestyle"] = linestyle
        if ( linewidth is not None ): self.config["cursor_linewidth"] = linewidth
        # ------------------------------------------------- #
        # --- カーソル ( x ) 追加                       --- #
        # ------------------------------------------------- #
        if ( xAxis is not None ):
            MinMax = self.ax1.get_ylim()
            self.ax1.vlines( xAxis, MinMax[0], MinMax[1], \
                             colors    =self.config["cursor_color"], \
                             linestyles=self.config["cursor_linestyle"],
                             linewidth =self.config["cursor_linewidth"] )
        # ------------------------------------------------- #
        # --- カーソル ( y ) 追加                       --- #
        # ------------------------------------------------- #
        if ( yAxis is not None ):
            MinMax = self.ax1.get_xlim()
            self.ax1.hlines( yAxis, MinMax[0], MinMax[1], \
                             colors    =self.config["cursor_color"], \
                             linestyles=self.config["cursor_linestyle"], \
                             linewidth =self.config["cursor_linewidth"] )

            
    # =================================================== #
    # === 2軸目 プロット用 ルーチン                   === #
    # =================================================== #
    def add__plot2( self, xAxis=None, yAxis=None, label=None, color=None, alpha=None, \
                    linestyle=None, linewidth=None, \
                    marker=None, markersize=None, markerwidth=None ):
        # ------------------------------------------------- #
        # --- 引数チェック                              --- #
        # ------------------------------------------------- #
        if ( yAxis       is None ): sys.exit( " [add__plot2] yAxis for axis 2 == ?? " )
        if ( xAxis       is None ): xAxis       = np.arange( yAxis.size ) # - インデックス代用 - #
        if ( label       is None ): label       = ' '*self.config["leg_labelLength"]
        if ( color       is None ): color       = self.config["plt_color"]
        if ( alpha       is None ): alpha       = self.config["plt_alpha"]
        if ( linestyle   is None ): linestyle   = self.config["plt_linestyle"]
        if ( linewidth   is None ): linewidth   = self.config["plt_linewidth"]
        if ( marker      is None ): marker      = self.config["plt_marker"]
        if ( markersize  is None ): markersize  = self.config["plt_markersize"]
        if ( markerwidth is None ): markerwidth = self.config["plt_markerwidth"]
        # ------------------------------------------------- #
        # --- 軸設定                                    --- #
        # ------------------------------------------------- #
        if ( self.ax2    is None ): self.ax2 = self.ax1.twinx()
        self.update__DataRange( xAxis=xAxis, yAxis=yAxis, ax2=True )
        self.set__axis2()
        # ------------------------------------------------- #
        # --- プロット 追加                             --- #
        # ------------------------------------------------- #
        self.ax2.plot( xAxis, yAxis , \
                       color =color , linestyle =linestyle , \
                       label =label , linewidth =linewidth , \
                       marker=marker, markersize=markersize, \
                       markeredgewidth=markerwidth, alpha =alpha   )


    # ========================================================= #
    # ===  bar 追加                                         === #
    # ========================================================= #
    def add__bar( self, xAxis=None, yAxis=None, color=None, alpha=None, width=None, \
                  label=None, align="center" ):
        # ------------------------------------------------- #
        # --- 引数チェック                              --- #
        # ------------------------------------------------- #
        if ( yAxis is None ): yAxis      = self.yAxis
        if ( xAxis is None ): xAxis      = self.xAxis
        if ( yAxis is None ): sys.exit( " [add__plot] yAxis == ?? " )
        if ( xAxis is None ): xAxis      = np.arange( yAxis.size ) # - インデックス代用 - #
        if ( label is None ): label      = ' '*self.config["leg_labelLength"]
        if ( width is None ): width      = self.config["bar_width"]
        if ( color is None ): color      = self.config["plt_color"]
        if ( alpha is None ): alpha      = self.config["plt_alpha"]
        # ------------------------------------------------- #
        # --- 軸設定                                    --- #
        # ------------------------------------------------- #
        bar_width    = ( xAxis[1]-xAxis[0] ) * width
        self.xAxis   = xAxis
        self.yAxis   = yAxis
        self.update__DataRange( xAxis=xAxis, yAxis=yAxis )
        self.set__axis()
        # ------------------------------------------------- #
        # --- プロット 追加                             --- #
        # ------------------------------------------------- #
        self.ax1.bar( xAxis, yAxis, label =label, \
                      color =color, alpha =alpha, width=bar_width, \
                      align =align )


    # ========================================================= #
    # ===  vector 追加                                      === #
    # ========================================================= #
    def add__arrow( self, xAxis=None, yAxis=None, uvec=None, vvec=None, color=None, width=None, \
                    scale=1.0, nvec=10 ):
    
        # ------------------------------------------------- #
        # --- 引数チェック                              --- #
        # ------------------------------------------------- #
        if ( yAxis      is None ): yAxis      = self.yAxis
        if ( xAxis      is None ): xAxis      = self.xAxis
        if ( yAxis      is None ): sys.exit( " [add__plot] yAxis == ?? " )
        if ( xAxis      is None ): xAxis      = np.arange( yAxis.size ) # - インデックス代用 - #
        if ( width      is None ): width      = 1.0
        if ( color      is None ): color      = "blue"
        
        # ------------------------------------------------- #
        # --- 軸設定                                    --- #
        # ------------------------------------------------- #
        self.xAxis   = xAxis
        self.yAxis   = yAxis
        self.update__DataRange( xAxis=xAxis, yAxis=yAxis )
        self.set__axis()
        nData = self.yAxis.shape[0]
        uvec_ = scale * uvec
        vvec_ = scale * vvec
        index = np.linspace( 0.0, nData-1, nvec, dtype=np.int64 )
        index = np.array( index, dtype=np.int64 )
        
        # ------------------------------------------------- #
        # --- プロット 追加                             --- #
        # ------------------------------------------------- #
        for ik in index:
            self.ax1.arrow( xAxis[ik], yAxis[ik] , uvec_[ik], vvec_[ik], \
                            color =color , width=width  )
    
        
    # ========================================================= #
    # ===  色付きライン                                     === #
    # ========================================================= #
    def add__colorline( self, xAxis=None, yAxis    =None , label =None, alpha     =None, \
                        linestyle  =None, linewidth=None , marker=None, markersize=None, \
                        color      =None, cmap     ="jet", norm  =plt.Normalize(0.0, 1.0) ):

        # ------------------------------------------------- #
        # --- 引数チェック                              --- #
        # ------------------------------------------------- #
        if ( yAxis      is None ): yAxis      = self.yAxis
        if ( xAxis      is None ): xAxis      = self.xAxis
        if ( yAxis      is None ): sys.exit( " [add__colorline] yAxis == ?? " )
        if ( xAxis      is None ): xAxis      = np.arange( yAxis.size ) # - インデックス代用 - #
        if ( label      is None ): label      = " "*self.config["leg_labelLength"]
        if ( alpha      is None ): alpha      = self.config["plt_alpha"]
        if ( linestyle  is None ): linestyle  = self.config["plt_linestyle"]
        if ( linewidth  is None ): linewidth  = self.config["plt_linewidth"]
        if ( marker     is None ): marker     = self.config["plt_marker"]
        if ( markersize is None ): markersize = self.config["plt_markersize"]
        
        # ------------------------------------------------- #
        # --- フィルタリング                            --- #
        # ------------------------------------------------- #
        # xAxis, yAxis = gfl.generalFilter( xAxis=xAxis, yAxis=yAxis, config=self.config )
        
        # ------------------------------------------------- #
        # --- make & check color_array                  --- #
        # ------------------------------------------------- #
        if ( color is None ):
            color  = np.linspace(0.0, 1.0, len(xAxis) )
        if ( not( hasattr( color, "__iter__" ) ) ):
            color  = np.array( [ color ] )
        if ( ( np.min( color ) < 0.0 ) or ( np.max( color ) > 1.0 ) ):
            print( "[add__colorline @ plot1D.py] color range exceeds [0,1] :: Normalize.... " )
            color  = ( color - np.min( color ) ) / ( np.max( color ) - np.min( color ) )
            
        # ------------------------------------------------- #
        # --- 軸設定                                    --- #
        # ------------------------------------------------- #
        self.xAxis   = xAxis
        self.yAxis   = yAxis
        color        = np.asarray( color )
        points       = np.array( [xAxis, yAxis] ).T.reshape( -1,1,2 )
        segments     = np.concatenate( [points[:-1], points[1:]], axis=1)
        self.update__DataRange( xAxis=xAxis, yAxis=yAxis )
        self.set__axis()
        # ------------------------------------------------- #
        # --- プロット 追加                             --- #
        # ------------------------------------------------- #
        import matplotlib.collections as mcoll
        lc           = mcoll.LineCollection( segments, array=color, cmap=cmap, norm=norm,
                                             linewidth=linewidth, alpha=alpha )
        self.ax1.add_collection( lc )
        
    
    # ========================================================= #
    # ===  scatter プロット 追加                            === #
    # ========================================================= #
    def add__scatter( self, xAxis=None, yAxis=None, cAxis=None, color=None, cmap=None, \
                      label=None, alpha=None, marker=None, markersize=None, markerwidth=None ):
        # ------------------------------------------------- #
        # --- 引数チェック                              --- #
        # ------------------------------------------------- #
        if ( yAxis       is None ): yAxis       = self.yAxis
        if ( xAxis       is None ): xAxis       = self.xAxis
        if ( yAxis       is None ): sys.exit( " [add__plot] yAxis == ?? " )
        if ( xAxis       is None ): xAxis       = np.arange( yAxis.size ) # - インデックス代用 - #
        if ( color       is None ): color       = self.config["plt_color"]
        if ( label       is None ): label       = ' '*self.config["leg_labelLength"]
        if ( alpha       is None ): alpha       = self.config["plt_alpha"]
        if ( marker      is None ): marker      = self.config["plt_marker"]
        # ------------------------------------------------- #
        # --- 軸設定                                    --- #
        # ------------------------------------------------- #
        self.xAxis   = xAxis
        self.yAxis   = yAxis
        self.update__DataRange( xAxis=xAxis, yAxis=yAxis )
        self.set__axis()
        if ( cmap is None ):
            cmap = "jet"
        if ( type( cmap ) is list ):
            if ( type( cmap[0] ) == str ):
                import matplotlib.colors as mcl
                cmap = mcl.ListedColormap( cmap )
            
        # ------------------------------------------------- #
        # --- プロット 追加                             --- #
        # ------------------------------------------------- #
        self.ax1.scatter( xAxis, yAxis , c=cAxis, cmap=cmap, label=label, \
                          marker=marker, alpha =alpha   )
        
        
    # ========================================================= #
    # ===  ファイル 保存                                    === #
    # ========================================================= #
    def save__figure( self, pngFile=None, dpi=None ):
        # ------------------------------------------------- #
        # --- 引数設定                                  --- #
        # ------------------------------------------------- #
        if ( pngFile is None ): pngFile = self.config["pngFile"]
        if ( dpi     is None ): dpi     = self.config["densityPNG"]
        # ------------------------------------------------- #
        # --- ファイル ( png ) 出力                     --- #
        # ------------------------------------------------- #
        if ( self.config["MinimalOut"] ):
            # -- 最小プロット (透明) -- #
            self.fig.savefig( pngFile, dpi=dpi, bbox_inches='tight', pad_inches=0, transparent=True )
        elif ( self.config["MinimalWhite"] ):
            # -- 最小プロット (白地) -- #
            self.fig.savefig( pngFile, dpi=dpi, bbox_inches="tight", pad_inches=0.0 )
        else:
            # -- 通常プロット        -- #
            self.fig.savefig( pngFile, dpi=dpi, pad_inches=0 )
        # plt.close()
        print( "[ save__figure -@plot1d- ] out :: {0}".format( pngFile ) )
        

    # ========================================================= #
    # ===  Display window                                   === #
    # ========================================================= #
    def display__window( self ):
        
        # ------------------------------------------------- #
        # --- Window へ出力                             --- #
        # ------------------------------------------------- #
        print( "\n" + "[ display__window -@plot1d- ]" + "\n" )
        self.fig.show()
               
        

# ======================================== #
# ===  実行部                          === #
# ======================================== #
if ( __name__=="__main__" ):

    import numpy as np
    xAxis  = np.linspace( 0.0, 2.0*np.pi, 101 )
    yAxis1 = np.sin( xAxis )
    yAxis2 = np.cos( xAxis ) * 100.0
    
    import nkUtilities.load__config   as lcf
    import nkUtilities.configSettings as cfs
    
    pngFile = "test/plot_sample.png"
    config  = lcf.load__config()
    config  = cfs.configSettings( configType="plot.def"   , config=config)
    config  = cfs.configSettings( configType="plot.marker", config=config )
    config  = cfs.configSettings( configType="plot.ax2"   , config=config )
    config["plt_xAutoRange"]    = False
    config["plt_xRange"]        = [0.0,6.0]
    config["ax2.yMajor.nticks"] = 7
    config["ax2.yAutoRange"]    = False
    config["ax2.yRange"]        = [-120.0,+120.0]
    fig     = plot1D( config=config, pngFile=pngFile )
    fig.add__plot ( xAxis=xAxis, yAxis=yAxis1, label="sin(x)", color="Orange" )
    fig.add__plot2( xAxis=xAxis, yAxis=yAxis2, label="cos(x)", color="RoyalBlue" )
    fig.add__legend()
    fig.set__axis()
    fig.save__figure()


    
