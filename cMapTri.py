import sys
import nkUtilities.mpl_baseSettings
import nkUtilities.load__config     as lcf
import numpy                        as np
import matplotlib.pyplot            as plt
import matplotlib.tri               as tri
import matplotlib.ticker            as tic
import scipy.interpolate            as itp


# ========================================================= #
# ===  2次元 カラーマップ描画用クラス                   === #
# ========================================================= #
class cMapTri:
    # ------------------------------------------------- #
    # --- クラス初期化用ルーチン                    --- #
    # ------------------------------------------------- #
    def __init__( self, \
                  xAxis      = None, yAxis      = None, \
                  cMap       = None, Cntr       = None, \
                  xvec       = None, yvec       = None, \
                  pngFile    = None, config     = None ):
        # ------------------------------------------------- #
        # --- 引数の引き渡し                            --- #
        # ------------------------------------------------- #
        self.xAxis   = xAxis
        self.yAxis   = yAxis
        self.cMap    = cMap
        self.Cntr    = Cntr
        self.xvec    = xvec
        self.yvec    = yvec
        self.config  = config
        # ------------------------------------------------- #
        # --- コンフィグの設定                          --- #
        # ------------------------------------------------- #
        if ( self.config  is     None ): self.config            = lcf.load__config()
        if ( pngFile      is not None ): self.config["pngFile"] = pngFile
        # ------------------------------------------------- #
        # --- レベルの設定  ( カラー / コンター )       --- #
        # ------------------------------------------------- #
        self.cmpLevels  = np.linspace( self.config["cmp_MaxMin"][0], self.config["cmp_MaxMin"][1],
                                       self.config["cmp_nLevels"] )
        self.cntLevels  = np.linspace( self.config["cnt_MaxMin"][0], self.config["cnt_MaxMin"][1],
                                       self.config["cnt_nLevels"] )
        # ------------------------------------------------- #
        # --- 描画領域の作成                            --- #
        # ------------------------------------------------- #
        #  -- 描画領域                                  --  #
        cmppos     = self.config["cmp_position"]
        self.fig   = plt.figure( figsize=self.config["FigSize"] )
        self.ax1   = self.fig.add_axes( [ cmppos[0], cmppos[1], cmppos[2]-cmppos[0], cmppos[3]-cmppos[1] ] )
        #  -- 格子の描画 on/off                         --  #
        if ( self.config["grid_sw"] ): self.set__grid()
        # ------------------------------------------------- #
        # --- x軸 - y軸の作成                           --- #
        # ------------------------------------------------- #
        #  -- もし，引数に x,y 変数が渡されてない場合，インデックスで代用不可 -- #
        if ( ( self.xAxis is None ) and ( self.cMap is not None ) ):
            self.xAxis = np.arange( ( self.cMap.shape[0] ) )
        if ( ( self.yAxis is None ) and ( self.cMap is not None ) ):
            self.yAxis = np.arange( ( self.cMap.shape[1] ) )
        #  -- AutoRange (x)  --  #
        if ( ( self.config["cmp_xAutoRange"] ) and ( self.xAxis is not None ) ):
            self.config["cmp_xRange"] = [ np.min( self.xAxis ), np.max( self.xAxis ) ]
        #  -- AutoRange (y)  --  #
        if ( ( self.config["cmp_yAutoRange"] ) and ( self.yAxis is not None ) ):
            self.config["cmp_yRange"] = [ np.min( self.yAxis ), np.max( self.yAxis ) ]
        # ------------------------------------------------- #
        # --- 速攻描画                                  --- #
        # ------------------------------------------------- #
        instantOut = False
        #  -- もし cMap が渡されていたら，即，描く      --  #
        if ( self.cMap is not None ):
            self.add__cMap( xAxis   = self.xAxis, yAxis   = self.yAxis,     \
                            cMap    = self.cMap,  levels  = self.cmpLevels  )
            if ( self.config["clb_sw"]      ):
                self.set__colorBar()
            if ( self.config["cmp_pointSW"] ):
                self.add__point( xAxis=self.xAxis, yAxis=self.yAxis )
            instantOut = True
        #  -- もし Cntrが渡されていたら，即，描く       --  #
        if ( self.Cntr is not None ):
            self.add__contour( xAxis   = self.xAxis, yAxis   = self.yAxis,     \
                               Cntr    = self.Cntr,  levels  = self.cntLevels  )
            if ( self.config["cnt_Separatrix"] ): self.add__separatrix()
            instantOut = True
        # -- もし xvec, yvec が渡されていたら，即，描く --  #
        if ( ( self.xvec is not None ) and ( self.yvec is not None ) ):
            self.add__vector( xAxis = self.xAxis, yAxis = self.yAxis, \
                              uvec  = self.xvec,  vvec  = self.yvec,  )
        # -- もし 何かを描いてたら，出力する．          --  #
        if ( instantOut ):
            self.save__figure( pngFile=self.config["pngFile"] )

            
    # ========================================================= #
    # === カラーマップ 追加 ルーチン  ( add__cMap )         === #
    # ========================================================= #
    def add__cMap( self, xAxis=None, yAxis=None, cMap=None, levels=None, alpha=None ):
        # ------------------------------------------------- #
        # --- 引数情報 更新                             --- #
        # ------------------------------------------------- #
        self.xAxis, self.yAxis, self.cMap = xAxis, yAxis, cMap
        if ( levels is not None ): self.cmpLevels = levels
        if ( alpha  is     None ): alpha = self.config["cmp_alpha"]
        # ------------------------------------------------- #
        # --- コンター情報を設定する                    --- #
        # ------------------------------------------------- #
        if ( self.config["cmp_AutoLevel"] ):
            self.set__cmpLevels()
        else:
            self.set__cmpLevels( levels=self.cmpLevels )
        # ------------------------------------------------- #
        # --- 軸情報整形 : 1次元軸 を 各点情報へ変換    --- #
        # ------------------------------------------------- #
        xAxis_, yAxis_ = np.copy( xAxis ), np.copy( yAxis )
        # ------------------------------------------------- #
        # --- カラーマップを作図                        --- #
        # ------------------------------------------------- #
        eps = 1.e-10 * abs( self.cmpLevels[-1] - self.cmpLevels[0] )
        self.cMap[ np.where( self.cMap < float( self.cmpLevels[ 0] ) ) ] = self.cmpLevels[ 0] + eps
        self.cMap[ np.where( self.cMap > float( self.cmpLevels[-1] ) ) ] = self.cmpLevels[-1] - eps
        triangulated = tri.Triangulation( xAxis_, yAxis_ )
        self.cImage = self.ax1.tricontourf( triangulated, self.cMap, self.cmpLevels, alpha=alpha, \
                                            cmap = self.config["cmp_ColorTable"], zorder=0, extend="both" )
        # ------------------------------------------------- #
        # --- 軸調整 / 最大 / 最小 表示                 --- #
        # ------------------------------------------------- #
        print( "[cMapTri] :: size :: x, y, z    =  "\
               .format( xAxis_.shape, yAxis_.shape, self.cMap.shape ) )
        print( "[cMapTri] :: ( min(x), max(x) ) = ( {0}, {1} ) "\
               .format( np.min( self.xAxis ), np.max( self.xAxis ) ) )
        print( "[cMapTri] :: ( min(y), max(y) ) = ( {0}, {1} ) "\
               .format( np.min( self.yAxis ), np.max( self.yAxis ) ) )
        print( "[cMapTri] :: ( min(z), max(z) ) = ( {0}, {1} ) "\
               .format( np.min( self.cMap  ), np.max( self.cMap  ) ) )
        self.set__axis()

        
    # ========================================================= #
    # === 等高線 追加 ルーチン  ( add__contour )            === #
    # ========================================================= #
    def add__contour( self, xAxis=None, yAxis=None, Cntr=None, levels=None ):
        # ------------------------------------------------- #
        # --- 引数情報 更新                             --- #
        # ------------------------------------------------- #
        if ( xAxis  is not None ): self.xAxis = xAxis
        if ( yAxis  is not None ): self.yAxis = yAxis
        if ( levels is not None ): self.cntLevels = levels
        if ( Cntr   is None     ):
            sys.exit( "[add__contour] Cntr == ???" )
        else:
            self.Cntr = Cntr
        # ------------------------------------------------- #
        # --- コンター情報を設定する                    --- #
        # ------------------------------------------------- #
        if ( self.config["cnt_AutoLevel"] ):
            self.set__cntLevels()
        else:
            self.set__cntLevels( levels=self.cntLevels )
        # ------------------------------------------------- #
        # --- 軸情報整形 : 1次元軸 を 各点情報へ変換    --- #
        # ------------------------------------------------- #
        xAxis_, yAxis_ = np.copy( xAxis ), np.copy( yAxis )
        # ------------------------------------------------- #
        # --- カラーマップを作成                        --- #
        # ------------------------------------------------- #
        eps = 1.e-10 * abs( self.cntLevels[-1] - self.cntLevels[0] )
        self.Cntr[ np.where( self.Cntr < float( self.cntLevels[ 0] ) ) ] = self.cntLevels[ 0] + eps
        self.Cntr[ np.where( self.Cntr > float( self.cntLevels[-1] ) ) ] = self.cntLevels[-1] - eps
        triangulated = tri.Triangulation( xAxis_, yAxis_ )
        # ------------------------------------------------- #
        # --- 等高線をプロット                          --- #
        # ------------------------------------------------- #
        self.cImage = self.ax1.tricontour( triangulated, self.Cntr, self.cntLevels, \
                                           colors     = self.config["cnt_color"], \
                                           linewidths = self.config["cnt_linewidth"], \
                                           zorder=1 )
        if ( self.config["cnt.clabel.sw"] ):
            self.ax1.clabel( self.cImage, fontsize=self.config["cnt.clabel.fontsize"] )
        self.set__axis()

        
    # ========================================================= #
    # ===   ベクトル 追加  ルーチン                         === #
    # ========================================================= #
    def add__vector( self, xAxis=None, yAxis=None, uvec=None, vvec=None, color=None, order="ji" ):
        # ------------------------------------------------- #
        # --- 引数チェック                              --- #
        # ------------------------------------------------- #
        if ( uvec  is None ): sys.exit("[ERROR] No Information for uvec , vvec  --@add__vector [ERROR]")
        if ( vvec  is None ): sys.exit("[ERROR] No Information for uvec , vvec  --@add__vector [ERROR]")
        if ( xAxis is None ): sys.exit("[ERROR] No Information for xAxis, yAxis --@add__vector [ERROR]")
        if ( yAxis is None ): sys.exit("[ERROR] No Information for yAxis, yAxis --@add__vector [ERROR]")
        if ( color is None ): color = self.config["vec_color"]
        if ( order == "ji" ): uvec, vvec = np.transpose( uvec ), np.transpose( vvec )
        if ( self.config["vec_AutoRange"] ):
            self.config["vec_xRange"] = self.config["cmp_xRange"]
            self.config["vec_yRange"] = self.config["cmp_yRange"]
        # ------------------------------------------------- #
        # -- 座標系 及びプロット点                       -- #
        # ------------------------------------------------- #
        xa     = np.linspace( self.config["vec_xRange"][0], self.config["vec_xRange"][-1], self.config["vec_nvec_x"] )
        ya     = np.linspace( self.config["vec_yRange"][0], self.config["vec_yRange"][-1], self.config["vec_nvec_y"] )
        xg,yg  = np.meshgrid( xa, ya )
        pAxis  = np.concatenate( [ np.ravel( np.copy( xAxis ) )[:,None], np.ravel( np.copy( yAxis ) )[:,None] ], axis=1 )
        uxIntp = itp.griddata( pAxis, uvec, (xg,yg), method=self.config["vec_interpolation"] )
        vyIntp = itp.griddata( pAxis, vvec, (xg,yg), method=self.config["vec_interpolation"] )
        # ------------------------------------------------- #
        # --- プロット 設定                             --- #
        # ------------------------------------------------- #
        if ( self.config["vec_AutoScale"] ):
            self.config["vec_scale"] = np.sqrt( np.max( uxIntp**2 + vyIntp**2 ) )*self.config["vec_AutoScaleRef"]
        # ------------------------------------------------- #
        # -- ベクトルプロット                            -- #
        # ------------------------------------------------- #
        self.ax1.quiver( xg, yg, uxIntp, vyIntp, angles='uv', scale_units='xy', \
                         color     =color, \
                         pivot     =self.config["vec_pivot"], scale     =self.config["vec_scale"],     \
                         width     =self.config["vec_width"], headwidth =self.config["vec_headwidth"], \
                         headlength=self.config["vec_headlength"] )


    # ========================================================= #
    # ===  点 追加                                          === #
    # ========================================================= #
    def add__point( self, xAxis=None, yAxis=None, color=None, marker=None ):
        # ------------------------------------------------- #
        # --- 引数チェック                              --- #
        # ------------------------------------------------- #
        if ( xAxis      is None ): xAxis      = 0
        if ( yAxis      is None ): yAxis      = 0
        if ( color      is None ): color      = self.config["cmp_pointColor"]
        if ( marker     is None ): marker     = self.config["cmp_pointMarker"]
        # ------------------------------------------------- #
        # --- 点 描画                                   --- #
        # ------------------------------------------------- #
        self.ax1.plot( xAxis, yAxis, marker=marker, color=color, \
                       markersize     =self.config["cmp_pointSize"], \
                       markeredgewidth=self.config["cmp_pointWidth"], \
                       linewidth      =0.0 )


    # ========================================================= #
    # ===  プロット 追加                                    === #
    # ========================================================= #
    def add__plot( self, xAxis=None, yAxis=None, label=None, color=None, linestyle=None, linewidth=None, marker=None ):
        # ------------------------------------------------- #
        # --- 引数チェック                              --- #
        # ------------------------------------------------- #
        if ( yAxis     is None ): yAxis     = self.yAxis
        if ( xAxis     is None ): xAxis     = self.xAxis
        if ( yAxis     is None ): sys.exit( " [USAGE] add__plot( xAxis=xAxis, yAxis=yAxis ) [USAGE] " )
        if ( xAxis     is None ): xAxis     = np.arange( yAxis.size )   # - x は y サイズで代用可 - #
        if ( label     is None ): label     = ' '
        if ( linewidth is None ): linewidth = self.config["plt_linewidth"]
        if ( marker    is None ): marker    = self.config["plt_marker"]
        if ( color     is None ): color     = self.config["plt_color"]
        # ------------------------------------------------- #
        # --- プロット                                  --- #
        # ------------------------------------------------- #
        self.ax1.plot( xAxis, yAxis, \
                       alpha =0.95,  marker=marker, \
                       label =label, linewidth=linewidth, \
                       color =color, linestyle=linestyle, )
    

    # ========================================================= #
    # ===  セパラトリクス 描画                              === #
    # ========================================================= #
    def add__separatrix( self, mask=None, xAxis=None, yAxis=None, separatrix=None ):
        # ------------------------------------------------- #
        # --- 引数チェック                              --- #
        # ------------------------------------------------- #
        if ( xAxis      is None ): xAxis      = self.xAxis
        if ( yAxis      is None ): yAxis      = self.yAxis
        if ( mask       is None ): mask       = self.Cntr / np.max( self.Cntr )
        if ( separatrix is None ): separatrix = self.config["cnt_sepLevel"]
        # ------------------------------------------------- #
        #  -- レベル 作成                               --  #
        # ------------------------------------------------- #
        sepLevels = [ separatrix ]
        # ------------------------------------------------- #
        # --- 軸情報整形 : 1次元軸 を 各点情報へ変換    --- #
        # ------------------------------------------------- #
        if ( ( xAxis.ndim == 1 ) and ( yAxis.ndim == 1 ) ):
            xAxis_, yAxis_ = np.meshgrid( xAxis, yAxis, indexing='ij' )
        else:
            xAxis_, yAxis_ = xAxis, yAxis
        # ------------------------------------------------- #
        # --- セパラトリクス 描画                       --- #
        # ------------------------------------------------- #
        self.ax1.contour( xAxis_, yAxis_, mask, sepLevels, \
                          color     = self.config["cnt_sepColor"], \
                          linewidth = self.config["cnt_sepLineWidth"]  )

        
    # ========================================================= #
    # === 軸設定用ルーチン                                  === #
    # ========================================================= #
    def set__axis( self ):
        # ------------------------------------------------- #
        # --- AutoRange, AutoTicks モード (データ取得)  --- #
        # ------------------------------------------------- #
        if ( ( self.config["cmp_xAutoRange"] ) and ( self.xAxis is not None ) ):
            self.config["cmp_xRange"] = [ np.min(self.xAxis ), np.max( self.xAxis ) ]
        if ( ( self.config["cmp_yAutoRange"] ) and ( self.yAxis is not None ) ):
            self.config["cmp_yRange"] = [ np.min(self.yAxis ), np.max( self.yAxis ) ]
        # ------------------------------------------------- #
        # --- プロット範囲の指定 ( xlim, ylim 設定 )    --- #
        # ------------------------------------------------- #
        self.ax1.set_xlim( self.config["cmp_xRange"][0], self.config["cmp_xRange"][1] )
        self.ax1.set_ylim( self.config["cmp_yRange"][0], self.config["cmp_yRange"][1] )
        # ------------------------------------------------- #
        # ---  アスペクト比                             --- #
        # ------------------------------------------------- #
        if ( self.config["cmp_autoAspect"] ):
            xleft, xright                  = self.ax1.get_xlim()
            ybottom, ytop                  = self.ax1.get_ylim()
            self.config["cmp_aspectRatio"] = abs( (ytop-ybottom) / (xright-xleft) )
        self.ax1.set_aspect( self.config["cmp_aspectRatio"] )

        # ------------------------------------------------- #
        # --- 軸目盛 設定                               --- #
        # ------------------------------------------------- #
        #  -- 整数  軸目盛り                            --  #
        xtick_dtype               = np.int32 if ( self.config["xMajor_integer"] ) else np.float64
        ytick_dtype               = np.int32 if ( self.config["yMajor_integer"] ) else np.float64
        #  -- 自動 / 手動 軸目盛り (x)                  --  #
        if ( self.config["cmp_xAutoTicks"] ):
            xMin, xMax            = self.ax1.get_xlim()
            self.ax1.set_xticks( np.linspace( xMin, xMax, self.config["xMajor_Nticks"], dtype=xtick_dtype ) )
        else:
            self.ax1.set_xticks( np.array( self.config["xMajor_ticks"], dtype=xtick_dtype ) )
        #  -- 自動 / 手動 軸目盛り (y)                  --  #
        if ( self.config["cmp_yAutoTicks"] ):
            yMin, yMax            = self.ax1.get_ylim()
            self.ax1.set_yticks( np.linspace( yMin, yMax, self.config["yMajor_Nticks"], dtype=ytick_dtype ) )
        else:
            self.ax1.set_yticks( np.array( self.config["yMajor_ticks"], dtype=ytick_dtype ) )
        # ------------------------------------------------- #
        # --- 目盛 スタイル 設定                        --- #
        # ------------------------------------------------- #
        self.ax1.tick_params( axis  ="x"                         , labelsize=self.config["xMajor_FontSize"], \
                              length=self.config["xMajor_length"], width    =self.config["xMajor_width"   ]  )
        self.ax1.tick_params( axis  ="y"                         , labelsize=self.config["yMajor_FontSize"], \
                              length=self.config["yMajor_length"], width    =self.config["yMajor_width"   ]  )
        
        #  -- Minor 軸目盛                              --  #
        if ( self.config["xMinor_sw"] is False ): self.config["xMinor_nticks"] = 1
        if ( self.config["yMinor_sw"] is False ): self.config["yMinor_nticks"] = 1
        self.ax1.xaxis.set_minor_locator( tic.AutoMinorLocator( self.config["xMinor_nticks"] ) )
        self.ax1.yaxis.set_minor_locator( tic.AutoMinorLocator( self.config["yMinor_nticks"] ) )
        # ------------------------------------------------- #
        # --- 軸目盛 無し                               --- #
        # ------------------------------------------------- #
        if ( self.config["xMajor_off"] ): self.ax1.get_xaxis().set_ticks([])
        if ( self.config["yMajor_off"] ): self.ax1.get_yaxis().set_ticks([])
        # ------------------------------------------------- #
        # --- 軸目盛 ラベル 無し                        --- #
        # ------------------------------------------------- #
        if ( self.config["xMajor_NoLabel"] ):
            self.ax1.set_xticklabels( ['' for i in self.ax1.get_xaxis().get_ticklocs()])
        if ( self.config["yMajor_NoLabel"] ):
            self.ax1.set_yticklabels( ['' for i in self.ax1.get_yaxis().get_ticklocs()])
        # ------------------------------------------------- #
        # --- 軸タイトル 設定 ( xlabel, ylabel )        --- #
        # ------------------------------------------------- #
        self.ax1.set_xlabel( self.config["xTitle"], fontsize=self.config["xTitle_FontSize"] )
        self.ax1.set_ylabel( self.config["yTitle"], fontsize=self.config["yTitle_FontSize"] )
        # ------------------------------------------------- #
        # --- 軸タイトル 無し                           --- #
        # ------------------------------------------------- #            
        if ( self.config["xTitle_off"] ): self.ax1.set_xlabel('')
        if ( self.config["yTitle_off"] ): self.ax1.set_ylabel('')

        
    # ========================================================= #
    # ===  カラー レベル設定                                === #
    # ========================================================= #
    def set__cmpLevels( self, levels=None, nLevels=None ):
        # ------------------------------------------------- #
        # --- 引数チェック                              --- #
        # ------------------------------------------------- #
        if ( nLevels is None ): nLevels = self.config["cmp_nLevels"]
        if (  levels is None ):
            minVal, maxVal  = np.min( self.cMap ), np.max( self.cMap )
            eps             = 1.0e-12
            # -- レベルが一定値である例外処理 -- #
            if ( abs( maxVal - minVal ) < eps ):
                if ( abs( minVal ) > eps ):
                    minVal, maxVal =  0.0, 2.0*maxVal
                else:
                    minVal, maxVal = -1.0, 1.0
            levels = np.linspace( minVal, maxVal, nLevels )
        # ------------------------------------------------- #
        # --- cmpLevels を 設定                         --- #
        # ------------------------------------------------- #
        self.cmpLevels  = levels

        
    # ========================================================= #
    # ===  コンター レベル設定                              === #
    # ========================================================= #
    def set__cntLevels( self, levels=None, nLevels=None ):
        # ------------------------------------------------- #
        # --- 引数チェック                              --- #
        # ------------------------------------------------- #
        if ( nLevels is None ): nLevels = self.config["cnt_nLevels"]
        if (  levels is None ):
            minVal, maxVal  = np.min( self.Cntr ), np.max( self.Cntr )
            levels          = np.linspace( minVal, maxVal, nLevels )
        # ------------------------------------------------- #
        # --- cntLevels を 設定                         --- #
        # ------------------------------------------------- #
        self.cntLevels  = levels

        
    # ========================================================= #
    # ===  カラーバー 描画 ルーチン                         === #
    # ========================================================= #
    def set__colorBar( self ):
        # ------------------------------------------------- #
        # --- 準備                                      --- #
        # ------------------------------------------------- #
        #  -- color bar の 作成                         --  #
        clbdata         = np.array( [ np.copy( self.cmpLevels ), np.copy( self.cmpLevels ) ] )
        #  -- color bar の プロット領域                 --  #
        lbrt            = self.config["clb_position"]
        clbax           = self.fig.add_axes( [ lbrt[0], lbrt[1], lbrt[2]-lbrt[0], lbrt[3]-lbrt[1] ] )
        
        # ------------------------------------------------- #
        # --- 横向き カラーバーの描画                   --- #
        # ------------------------------------------------- #        
        if ( self.config["clb_orientation"] == "horizontal" ):
            clbax.set_xlim( self.cmpLevels[0] , self.cmpLevels[-1] )
            clbax.set_ylim( [0.0, 1.0] )
            clb_tickLabel = np.linspace( self.cmpLevels[0], self.cmpLevels[-1], \
                                         self.config["clb.xMajor.nTicks"] )
            #  -- color bar の 軸目盛  設定                 --  #
            clbax.tick_params( labelsize=self.config["clb_FontSize"], \
                               length=self.config["clb.xMajor.length"], \
                               width=self.config["clb.xMajor.width" ]  )
            clbax.xaxis.set_minor_locator( tic.AutoMinorLocator( self.config["clb.xMinor.nTicks"] ) )
            clbax.get_xaxis().set_ticks( clb_tickLabel )
            clbax.get_yaxis().set_ticks([])
            self.myCbl  = clbax.contourf( self.cmpLevels, [0.0,1.0], clbdata, \
                                          self.cmpLevels, zorder=0, \
                                          cmap = self.config["cmp_ColorTable"] )
        # ------------------------------------------------- #
        # --- 縦向き カラーバーの描画                   --- #
        # ------------------------------------------------- #        
        if ( self.config["clb_orientation"] == "vertical" ):
            clbax.set_xlim( [0.0, 1.0] )
            clbax.set_ylim( self.cmpLevels[0], self.cmpLevels[-1] )
            clbax.get_xaxis().set_ticks([])
            clb_tickLabel = np.linspace( self.cmpLevels[0], self.cmpLevels[-1], \
                                         self.config["clb.yMajor.nTicks"] )
            clbax.tick_params( labelsize=self.config["clb_FontSize"], \
                               length=self.config["clb.yMajor.length"], \
                               width=self.config["clb.yMajor.width" ]  )
            clbax.yaxis.set_minor_locator( tic.AutoMinorLocator( self.config["clb.yMinor.nTicks"] ) )
            clbax.get_yaxis().set_ticks( clb_tickLabel )
            clbax.yaxis.tick_right()
            self.myCbl  = clbax.contourf( [0.0,1.0], self.cmpLevels, np.transpose( clbdata ), \
                                          self.cmpLevels, zorder=0, \
                                          cmap = self.config["cmp_ColorTable"] )
        # ------------------------------------------------- #
        # --- カラーバー タイトル 追加                  --- #
        # ------------------------------------------------- #        
        if ( self.config["clb_title"] is not None ):
            textax = self.fig.add_axes( [0,0,1,1] )
            ctitle = r"{}".format( self.config["clb_title"] )
            textax.text( self.config["clb_title_pos"][0], self.config["clb_title_pos"][1], \
                         ctitle, fontsize=self.config["clb_title_size"] )
            textax.set_axis_off()


    # ========================================================= #
    # ===  グリッド / y=0 軸線 追加                         === #
    # ========================================================= #
    def set__grid( self ):
        
        # ------------------------------------------------- #
        # --- グリッド ( 主グリッド :: Major )          --- #
        # ------------------------------------------------- #
        if ( self.config["grid_sw"]      ):
            self.ax1.grid( visible  =self.config["grid_sw"]       , \
                           which    ='major'                      , \
                           color    =self.config["grid_color"]    , \
                           alpha    =self.config["grid_alpha"]    , \
                           linestyle=self.config["grid_linestyle"], \
                           linewidth=self.config["grid_linewidth"]  )
        # ------------------------------------------------- #
        # --- グリッド ( 副グリッド :: Minor )          --- #
        # ------------------------------------------------- #
        if ( self.config["grid_minor_sw"] ):
            self.ax1.grid( visible  =self.config["grid_minor_sw"]   , \
                           which    ='minor'                        , \
                           color    =self.config["grid_minor_color"], \
                           linestyle=self.config["grid_minor_style"], \
                           alpha    =self.config["grid_minor_alpha"], \
                           linewidth=self.config["grid_minor_width"]  )

            

            
    # ========================================================= #
    # ===  ファイル 保存                                    === #
    # ========================================================= #
    def save__figure( self, pngFile=None ):
        # ------------------------------------------------- #
        # --- 引数設定                                  --- #
        # ------------------------------------------------- #
        if ( pngFile is not None ): self.config["pngFile"] = pngFile
        # ------------------------------------------------- #
        # --- ファイル ( png ) 出力                     --- #
        # ------------------------------------------------- #
        if   ( self.config["MinimalOut"]   ):
            # -- 最小プロット (透明) -- #
            self.fig.savefig( self.config["pngFile"], dpi=self.config["densityPNG"], \
                              bbox_inches='tight'   , pad_inches=0, transparent=True )
        elif ( self.config["MinimalWhite"] ):
            # -- 最小プロット (白地) -- #
            self.fig.savefig( self.config["pngFile"], dpi=self.config["densityPNG"], \
                              bbox_inches="tight", pad_inches=0.0 )
        else:
            # -- 通常プロット        -- #
            self.fig.savefig( self.config["pngFile"], dpi=self.config["densityPNG"], \
                              pad_inches=0 )
        plt.close()
        print( "[ save__figure -@cMapTri- ] out :: {0}".format( self.config["pngFile"] ) )


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):

    x_, y_, z_ = 0, 1, 2

    # ------------------------------------------------- #
    # --- [1] load config                           --- #
    # ------------------------------------------------- #
    import nkUtilities.load__config as lcf
    config = lcf.load__config()
    
    # ------------------------------------------------- #
    # --- [2] generate profile 1                    --- #
    # ------------------------------------------------- #
    import nkUtilities.equiSpaceGrid as esg
    x1MinMaxNum = [ -1.0, 1.0, 21 ]
    x2MinMaxNum = [ -1.0, 1.0, 21 ]
    x3MinMaxNum = [  0.0, 0.0,  1 ]
    coord       = esg.equiSpaceGrid( x1MinMaxNum=x1MinMaxNum, x2MinMaxNum=x2MinMaxNum, \
                                     x3MinMaxNum=x3MinMaxNum, returnType = "point" )
    coord[:,z_] = np.sqrt( coord[:,x_]**2 + coord[:,y_]**2 )
    cMapTri( xAxis=coord[:,x_], yAxis=coord[:,y_], cMap=coord[:,z_], \
             config=config, pngFile="test/cMapTri.png" )

    # ------------------------------------------------- #
    # --- [3] generate profile 2                    --- #
    # ------------------------------------------------- #
    import nkUtilities.equiSpaceGrid as esg
    x1MinMaxNum = [ -1.0, 1.0, 21 ]
    x2MinMaxNum = [ -1.0, 1.0, 21 ]
    x3MinMaxNum = [  0.0, 0.0,  1 ]
    coord       = esg.equiSpaceGrid( x1MinMaxNum=x1MinMaxNum, x2MinMaxNum=x2MinMaxNum, \
                                     x3MinMaxNum=x3MinMaxNum, returnType = "point" )
    import nkBasicAlgs.robustInv as inv
    radii       = np.sqrt( coord[:,x_]**2 + coord[:,y_]**2 )
    uvec        = ( - coord[:,y_] * inv.robustInv( radii ) )
    vvec        = ( + coord[:,x_] * inv.robustInv( radii ) )
    
    fig         = cMapTri( pngFile="test/vector_map.png", config=config )
    fig.add__cMap   ( xAxis=coord[:,x_], yAxis=coord[:,y_], cMap=radii )
    fig.add__vector ( xAxis=coord[:,x_], yAxis=coord[:,y_], uvec=uvec, vvec=vvec )
    fig.add__contour( xAxis=coord[:,x_], yAxis=coord[:,y_], Cntr=radii )
    fig.save__figure()











    # # ========================================================= #
    # # ===   ベクトル 追加  ルーチン                         === #
    # # ========================================================= #
    # def add__vector( self, xAxis=None, yAxis=None, uvec=None, vvec=None, color=None, order="ji" ):
    #     # ------------------------------------------------- #
    #     # --- 引数チェック                              --- #
    #     # ------------------------------------------------- #
    #     if ( uvec  is None ): sys.exit("[ERROR] No Information for uvec, vvec --@add__vector [ERROR]")
    #     if ( vvec  is None ): sys.exit("[ERROR] No Information for uvec, vvec --@add__vector [ERROR]")
    #     if ( xAxis is None ): xAxis = np.linspace( 0.0, 1.0, len( uvec[:,0] ) )
    #     if ( yAxis is None ): yAxis = np.linspace( 0.0, 1.0, len( uvec[0,:] ) )
    #     if ( color is None ): color = self.config["vec_color"]
    #     if ( order == "ji" ): uvec, vvec = np.transpose( uvec ), np.transpose( vvec )
    #     # ------------------------------------------------- #
    #     # -- 座標系 及びプロット点                       -- #
    #     # ------------------------------------------------- #
    #     xAxis_ = np.linspace( self.config["cmp_xRange"][0], self.config["cmp_xRange"][-1], self.config["vec_nvec_x"] )
    #     yAxis_ = np.linspace( self.config["cmp_yRange"][0], self.config["cmp_yRange"][-1], self.config["vec_nvec_y"] )
    #     uxIntp = sit.interp2d( xAxis, yAxis, uvec )
    #     vyIntp = sit.interp2d( xAxis, yAxis, vvec )
    #     uvec_  = uxIntp( xAxis_, yAxis_ )
    #     vvec_  = vyIntp( xAxis_, yAxis_ )
    #     if ( self.config["vec_AutoScale"] ):
    #         self.config["vec_scale"] = np.sqrt( np.max( uvec_**2 + vvec_**2 ) )*8.0
    #     # ------------------------------------------------- #
    #     # -- ベクトルプロット                            -- #
    #     # ------------------------------------------------- #
    #     self.ax1.quiver( xAxis_, yAxis_, uvec_, vvec_, angles='uv', scale_units='xy', \
    #                      color     =color, \
    #                      pivot     =self.config["vec_pivot"], scale     =self.config["vec_scale"],     \
    #                      width     =self.config["vec_width"], headwidth =self.config["vec_headwidth"], \
    #                      headlength=self.config["vec_headlength"] )

