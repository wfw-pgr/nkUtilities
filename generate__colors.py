import numpy         as np
import matplotlib.cm as cm
import seaborn       as sns


# ========================================================= #
# ===  generate colors for plot                         === #
# ========================================================= #
def generate__colors( colorType="default", nColors=10, seaborn=True, howto=False ):

    if ( howto == True ):
        print( "[generate__colors.py] generate__colors( colorType=, nColors=, seaborn=T/F, howto=T/F )")
        print( "[generate__colors.py] colorType = [ \ \n"\
               "default, bright, deep, muted, colorblind, pastel, \n"\
               "jet, tab10, tab20, hsv, accent, pastel1, pastel2, set1, set2, set3 \n"\
               " ] ")
        return()
    
    # ------------------------------------------------- #
    # --- [1] generate colors                       --- #
    # ------------------------------------------------- #

    if ( not( seaborn ) ):
        
        if   ( colorType.lower()=="jet"   ):
            colors = [ cm.jet( ik / float( nColors ) ) for ik in range( nColors ) ]
            
        elif ( colorType.lower()=="tab10" ):
            colors = [ cm.tab10( ik / float( nColors ) ) for ik in range( nColors ) ]
            
        elif ( colorType.lower()=="tab20" ):
            colors = [ cm.tab20( ik / float( nColors ) ) for ik in range( nColors ) ]
            
        elif ( colorType.lower()=="hsv" ):
            colors = [ cm.hsv( ik / float( nColors ) ) for ik in range( nColors ) ]
            
        elif ( colorType.lower()=="accent" ):
            colors = [ cm.Accent( ik / float( nColors ) ) for ik in range( nColors ) ]
            
        elif ( colorType.lower()=="pastel1" ):
            colors = [ cm.Pastel1( ik / float( nColors ) ) for ik in range( nColors ) ]
            
        elif ( colorType.lower()=="pastel2" ):
            colors = [ cm.Pastel2( ik / float( nColors ) ) for ik in range( nColors ) ]
            
        elif ( colorType.lower()=="set1" ):
            colors = [ cm.Set1( ik / float( nColors ) ) for ik in range( nColors ) ]
            
        elif ( colorType.lower()=="set2" ):
            colors = [ cm.Set2( ik / float( nColors ) ) for ik in range( nColors ) ]
            
        elif ( colorType.lower()=="set3" ):
            colors = [ cm.Set3( ik / float( nColors ) ) for ik in range( nColors ) ]
            
        else:
            print( "[generate__colors.py] colorType  == ?? " )
            sys.exit()

    else:
        
        if   ( colorType.lower()=="jet"  ):
            print( "[generate__colors.py]  no jet palette for seaborn" )
            sys.exit()

        elif ( colorType.lower()=="default" ):
            colors = sns.color_palette( n_colors=nColors )
            
        elif ( colorType.lower()=="deep" ):
            colors = sns.color_palette( palette="deep", n_colors=nColors )

        elif ( colorType.lower()=="colorblind" ):
            colors = sns.color_palette( palette="colorblind", n_colors=nColors )

        elif ( colorType.lower()=="dark" ):
            colors = sns.color_palette( palette="dark", n_colors=nColors )

        elif ( colorType.lower()=="bright" ):
            colors = sns.color_palette( palette="bright", n_colors=nColors )

        elif ( colorType.lower()=="muted" ):
            colors = sns.color_palette( palette="muted", n_colors=nColors )

        elif ( colorType.lower()=="pastel" ):
            colors = sns.color_palette( palette="pastel", n_colors=nColors )

        elif ( colorType.lower()=="hsv" ):
            colors = sns.color_palette( palette="hsv", n_colors=nColors )

        elif ( colorType.lower()=="accent" ):
            colors = sns.color_palette( palette="Accent", n_colors=nColors )

        elif ( colorType.lower()=="pastel1" ):
            colors = sns.color_palette( palette="Pastel1", n_colors=nColors )

        elif ( colorType.lower()=="pastel2" ):
            colors = sns.color_palette( palette="Pastel2", n_colors=nColors )

        elif ( colorType.lower()=="tab10" ):
            colors = sns.color_palette( palette="tab10", n_colors=nColors )

        elif ( colorType.lower()=="tab20" ):
            colors = sns.color_palette( palette="tab20", n_colors=nColors )

        elif ( colorType.lower()=="set1" ):
            colors = sns.color_palette( palette="Set1", n_colors=nColors )

        elif ( colorType.lower()=="set2" ):
            colors = sns.color_palette( palette="Set2", n_colors=nColors )

        elif ( colorType.lower()=="set3" ):
            colors = sns.color_palette( palette="Set3", n_colors=nColors )

        else:
            colors = sns.color_palette( palette=colorType, n_colors=nColors )
            

    # ------------------------------------------------- #
    # --- [2] return                                --- #
    # ------------------------------------------------- #
    return( colors )



# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #

if ( __name__=="__main__" ):
    
    generate__colors( howto=True )
    
    wnum_max = 5
    xAxis    = np.linspace( 0.0, 1.0, 101 ) * 2.0*np.pi
    
    colors   = generate__colors( colorType="default", nColors=wnum_max )
    print( colors )
    
    import nkUtilities.plot1D as pl1
    pngFile  = "out.png"
    fig = pl1.plot1D( pngFile=pngFile )
    for ik in range( wnum_max ):
        yAxis    = np.sin( xAxis*(ik+1)/float(wnum_max)*2.0 )
        fig.add__plot( xAxis=xAxis, yAxis=yAxis, color=colors[ik] )
    fig.set__axis()
    fig.save__figure()


