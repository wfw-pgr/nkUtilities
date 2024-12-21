import math, decimal

def return__digitsAligned( value, maxDigit=10, precision=12 ):

    decimal.getcontext().prec = precision

    exp = math.floor( math.log10( abs( value ) ) ) if ( value != 0 ) else 0.0
    if ( abs( exp ) >= maxDigit ):
        ret = "{:15.8e}".format( value )
    else:
        ret = str( decimal.Decimal( round( value, maxDigit ) ).normalize() )
    return( ret )

# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    print( return__digitsAligned( 1.602e-19 ) )
    print( return__digitsAligned( 1.602e-6 ) )
    print( return__digitsAligned( 0.92229 ) )
    print( return__digitsAligned( 1.02e+8 ) )
