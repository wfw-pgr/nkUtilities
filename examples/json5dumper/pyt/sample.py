import numpy as np
na_      = np.newaxis
tcoord   = np.linspace( 0.0, 1.0, 11 )
xcoord   = np.cos( 0.5*np.pi * tcoord )
ycoord   = np.sin( 0.5*np.pi * tcoord )
xycoord  = np.concatenate( [ xcoord[:,na_], ycoord[:,na_] ], axis=1 )

Data     = { "Title":"Data_A", "Date":"2024/07/13", "Data":xycoord } 

import nkUtilities.json5dumper as j5d
jsonFile = "dat/sample.json"
dumper   = j5d.json5dumper().dump  ( jsonFile=jsonFile, Data=Data )
recalled = j5d.json5dumper().recall( jsonFile=jsonFile )

print( "Data" )
print( Data )

print( "recalled" )
print( recalled )
