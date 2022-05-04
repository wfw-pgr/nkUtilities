import numpy as np
import matplotlib.pyplot as plt


# ========================================================= #
# ===  draw__heatmap.py                                 === #
# ========================================================= #

def draw__heatmap( Data=None, cmap="jet", textFormat="{0:.3f}", fontsize=5 ):

    
    # ------------------------------------------------- #
    # --- [1] arguments                             --- #
    # ------------------------------------------------- #
    if ( Data is None ): sys.exit( "[draw__heatmap.py] Data == ???" )

    # ------------------------------------------------- #
    # --- [2] draw heatmap                          --- #
    # ------------------------------------------------- #
    fig = plt.figure()
    ax  = fig.add_axes( [0.16,0.16,0.74, 0.74] )
    ax.imshow( Data[:,:], cmap=cmap )
    for ik in range( Data.shape[0] ):
        for jk in range( Data.shape[1] ):
            ax.text( ik, jk, textFormat.format( Data[ik,jk] ) ,\
                     horizontalalignment="center", \
                     verticalalignment  ="center", fontsize=fontsize )
    fig.show()
    plt.show()


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):

    # ------------------------------------------------- #
    # --- [1] sample Data ( :: wine )               --- #
    # ------------------------------------------------- #
    import sklearn.datasets as ds
    wines      = ds.load_wine()
    avgs_      = np.average( wines.data, axis=0  )
    stds_      = np.std    ( wines.data, axis=0, ddof=True  )
    uniform    = np.ones(  ( wines.data.shape[0] ) )
    wines.avgs = np.outer( uniform, avgs_ )
    wines.stds = np.outer( uniform, stds_ )
    wines.norm = ( wines.data - wines.avgs ) /wines.stds
    wines.covs = np.cov( wines.norm, rowvar=False )
    print( wines.covs.shape )
    
    draw__heatmap( Data=wines.covs )
