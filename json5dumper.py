import os, sys, re, json5
import numpy as np

# ========================================================= #
# ===  json5dumper.py                                   === #
# ========================================================= #

class json5dumper():

    # ========================================================= #
    # ===  initialize                                       === #
    # ========================================================= #
    def __init__( self, Data=None, jsonFile=None, numpyMark="numpyArrayPath::", indent=True, silent=False ):
        self.Data      = Data
        self.jsonFile  = jsonFile
        self.numpyMark = numpyMark
        self.silent    = silent
        self.indent    = indent
        if not( self.silent ):
            print( "[json5dumper.py] Class Defined. USE json5dumper.dump() / json5dumper.recall()" )
        

    # ========================================================= #
    # ===  dump command  ( save )                           === #
    # ========================================================= #
    def dump( self, Data=None, jsonFile=None, silent=None, indent=None ):
    
        # ------------------------------------------------- #
        # --- [1] arguments                             --- #
        # ------------------------------------------------- #
        if ( jsonFile is not None ): self.jsonFile = jsonFile
        if ( Data     is not None ): self.Data     = Data
        if ( silent   is not None ): self.silent   = silent
        if ( indent   is not None ): self.indent   = indent
        
        # ------------------------------------------------- #
        # --- [2] detect numpy array                    --- #
        # ------------------------------------------------- #
        basename   = os.path.splitext( os.path.basename( self.jsonFile ) )[0]
        dirname    = os.path.join( os.path.dirname( self.jsonFile ), basename+"_npy" )
        nameformat = os.path.join( dirname, "{}.npy" )
        textables  = {}
        numpyvars  = {}
        for key,var in self.Data.items():
            if ( type(var) in [ np.ndarray ] ):
                numpyvars[key] = var
                textables[key] = self.numpyMark + nameformat.format( key )
            else:
                textables[key] = var
        if ( len( numpyvars ) > 0 ):
            ret    = os.makedirs( dirname, exist_ok=True )
            
        # ------------------------------------------------- #
        # --- [3] dump json5                            --- #
        # ------------------------------------------------- #
        with open( self.jsonFile, "w" ) as f:
            json5.dump( textables, f, indent=self.indent )

        # ------------------------------------------------- #
        # --- [4] save numpy array in file separately   --- #
        # ------------------------------------------------- #
        for key,var in numpyvars.items():
            np.save( nameformat.format( key ), var )

        # ------------------------------------------------- #
        # --- [5] return                                --- #
        # ------------------------------------------------- #
        if not( self.silent ):
            print( "[json5dumper.py] save in :: {}".format( self.jsonFile ) )
        return( self )

    
    # ========================================================= #
    # ===  recall command ( load )                          === #
    # ========================================================= #
    def recall( self, jsonFile=None ):
        
        # ------------------------------------------------- #
        # --- [1] arguments                             --- #
        # ------------------------------------------------- #
        if ( jsonFile is not None ): self.jsonFile = jsonFile
        
        # ------------------------------------------------- #
        # --- [2] load json file                        --- #
        # ------------------------------------------------- #
        with open( self.jsonFile, "r" ) as f:
            Data = json5.load( f )
            
        # ------------------------------------------------- #
        # --- [3] detect numpy array mark               --- #
        # ------------------------------------------------- #
        expr = self.numpyMark + "(.+)"
        for key,var in Data.items():
            if ( type( var ) is str ):
                ret = re.match( expr, var )
                if ( ret ):
                    Data[key] = np.load( ret.group(1) )

        # ------------------------------------------------- #
        # --- [4] return                                --- #
        # ------------------------------------------------- #
        self.Data = { **Data }
        return( Data )


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):

    jsonFile  = "dat/output.json"

    # ------------------------------------------------- #
    # --- [1] define sample data                    --- #
    # ------------------------------------------------- #
    arr1     = np.linspace( 0.0, 1.0, 5 )
    arr2     = np.reshape( np.arange( 30 ), ( 5,3,2 ) )
    arr3     = np.reshape( np.arange( 2000 ), ( 2, 1000 ) )
    
    Data     = { "float1":0.0, "int1":10, "str1":"string", "list1":[ 0.0, 1.0 ], \
                 "list2":[ "a1", "b2", "c2", 3 ], "arr1": arr1, "arr2":arr2, "arr3":arr3, \
                 "dict1":{ "a":0.0, "b":1.0, "c":"ok" } }

    # ------------------------------------------------- #
    # --- [2] dump & recall                         --- #
    # ------------------------------------------------- #
    dumper   = ( json5dumper() ).dump( Data=Data, jsonFile=jsonFile )
    recalled = ( json5dumper() ).recall( jsonFile=jsonFile )
    print()
    print( "[Data]" )
    print( Data )
    print()
    print( "[recalled]" )
    print( recalled )
    print()
    
