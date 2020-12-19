# ========================================================= #
# === matplotlib 共通 パラメータ セッティング           === #
# ========================================================= #
import matplotlib.pyplot        as plt
import nkUtilities.load__config as lcf

config = lcf.load__config()

# ------------------------------------------------- #
# --- 全体設定                                  --- #
# ------------------------------------------------- #
plt.style.use('seaborn-white')
plt.rcParams['figure.dpi']             = config["densityPNG"]

# ------------------------------------------------- #
# --- 画像 サイズ / 余白 設定                   --- #
# ------------------------------------------------- #
# -- 相対座標  --  #
plt.rcParams['figure.subplot.left']    = 0.0
plt.rcParams['figure.subplot.bottom']  = 0.0
plt.rcParams['figure.subplot.right']   = 1.0
plt.rcParams['figure.subplot.top']     = 1.0
plt.rcParams['figure.subplot.wspace']  = 0.0
plt.rcParams['figure.subplot.hspace']  = 0.0
# -- 余白設定  --  #
plt.rcParams['axes.xmargin']           = 0
plt.rcParams['axes.ymargin']           = 0

# ------------------------------------------------- #
# --- フォント 設定                             --- #
# ------------------------------------------------- #
# -- フォント 種類                          --  #
plt.rcParams['font.family']            = config["Font"]
plt.rcParams['font.serif']             = config["Font"]
plt.rcParams['mathtext.fontset']       = config["MathFont"]
# -- other settings                         --  #
#     :: 'dejavusans', 'cm', 'custom'       ::  #
#     :: 'stix', 'stixsans', 'dejavuserif'  ::  #
# --                                        --  #
# -- 通常 フォント                          --  #
plt.rcParams['font.size']              = config["chsize1"]
# -- 軸タイトル                             --  #
plt.rcParams['axes.labelsize']         = config["chsize2"]
plt.rcParams['axes.labelweight']       = 'regular'

# ------------------------------------------------- #
# --- 目盛 設定 ( xticks, yticks )              --- #
# ------------------------------------------------- #
# -- 目盛線向き :: 内向き('in'), 外向き('out')   -- #
# --            :: 双方向か('inout')             -- #
# -- xTicks -- #
plt.rcParams['xtick.direction']        = 'in'
plt.rcParams['xtick.bottom']           = True
plt.rcParams['xtick.top']              = True
plt.rcParams['xtick.major.size']       = config["xMajor_size"]
plt.rcParams['xtick.major.width']      = config["xMajor_width"]
plt.rcParams['xtick.minor.size']       = config["xMinor_size"]
plt.rcParams['xtick.minor.width']      = config["xMinor_width"]
plt.rcParams['xtick.minor.visible']    = config["xMinor_sw"]
# -- yTicks -- #
plt.rcParams['ytick.direction']        = 'in'
plt.rcParams['ytick.left']             = True
plt.rcParams['ytick.right']            = True
plt.rcParams['ytick.major.size']       = config["yMajor_size"]
plt.rcParams['ytick.major.width']      = config["yMajor_width"]
plt.rcParams['ytick.minor.visible']    = config["yMinor_sw"]
plt.rcParams['ytick.minor.size']       = config["yMinor_size"]
plt.rcParams['ytick.minor.width']      = config["yMinor_width"]

# ------------------------------------------------- #
# --- プロット線 / 軸 の線の太さ                --- #
# ------------------------------------------------- #
plt.rcParams['lines.linewidth']        = config["plt_linewidth"]
plt.rcParams['axes.linewidth']         = config["axes_linewidth"]
