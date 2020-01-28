import sys
import numpy as np

# ========================================================= #
# ===  fourier Filter ( LPF )                           === #
# ========================================================= #
def fourierFilter( Data=None, iCutoff=None, fCutoff=None ):
    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    if ( Data    is None ): sys.exit( "[fourierFilter] Data == ?? " )
    if ( fCutoff is None ): fCutoff = 0.50
    if ( iCutoff is None ): iCutoff = int( Data.shape[0]/2*( 1.0-fCutoff ) ) + 1
    # ------------------------------------------------- #
    # --- [2] Fourier Transform                     --- #
    # ------------------------------------------------- #
    FD        = np.fft.fft( Data )
    # ------------------------------------------------- #
    # --- [3] cut high frequency                    --- #
    # ------------------------------------------------- #
    i1        =                +iCutoff
    i2        = ( Data.shape[0]-iCutoff + 1 )
    FD[i1:i2] = 0.0
    ret       = ( np.fft.ifft( FD ) ).real
    return( ret )


# ======================================== #
# ===  実行部                          === #
# ======================================== #
if ( __name__=="__main__" ):
    nAmp  = 0.5
    Nx    = 1000
    noise = np.random.rand( Nx ) * nAmp - nAmp/2.0
    xAxis = np.linspace( 0.0, 6.28, Nx )
    yAxis = np.sin( xAxis * 2.0 )
    for i in range( Nx ):
        if ( i % 20 == 0 ):
            yAxis[i] = yAxis[i] + noise[i]
            
    import myStyle.plot1D as pl1
    med   = fourierFilter( Data=yAxis, iCutoff=None )
    fig   = pl1.plot1D( FigName="out.png" )
    fig.addPlot( xAxis=xAxis, yAxis=yAxis, label="Raw Data" )
    fig.addPlot( xAxis=xAxis, yAxis=med  , label="Filtered" )
    fig.setAxis()
    fig.addLegend()
    fig.writeFigure()
