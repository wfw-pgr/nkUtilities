#!/usr/bin/env python3
import os, sys, json5, argparse, shutil
import nkUtilities.json__formulaParser as jso

# ========================================================= #
# ===  translate__json2html                             === #
# ========================================================= #

def translate__json2html( data ):

    # ------------------------------------------------- #
    # --- [1] recursive translation                 --- #
    # ------------------------------------------------- #
    if   isinstance( data, type(None) ):           #  -- None -- #
        return( '<div class="bool-true">None</div>' )
    
    elif isinstance( data, bool ):                 #  -- bool -- #
        sval = str(data)
        return( '<div class="bool-{0}">{1}</div>'.format( sval.lower(), sval ) )
        
    elif isinstance( data, str  ):                 #  -- str  -- #
        if ( len(data) == 0):
            return( '<span class="string empty">(Empty Text)</span>' )
        else:
            return( f'<span class="string">{data}</span>' )
        
    elif isinstance(data, (int, float)):
        # INT or FLOAT
        if isinstance(data, int):
            class_name = "int number"
        else:
            class_name = "float number"
        return f'<span class="{class_name}">{data}</span>'
    elif isinstance(data, list):
        # ARRAY
        if len(data) > 0:
            html = '<table class="array">'
            for i, item in enumerate(data):
                html += '<tr>'
                html += '<td class="value array-value">'
                html += translate__json2html( data=item )
                html += '</td></tr>'
            html += '</table>'
            return html
        else:
            return '<span class="array empty">(Empty List)</span>'
    elif isinstance( data, dict ):
        # OBJECT
        html = '<table class="object">'
        for key, value in data.items():
            html += '<tr>'
            html += f'<th class="key object-key">{key}</th>'
            html += '<td class="value object-value">'
            html += translate__json2html( data=value )
            html += '</td></tr>'
        html += '</table>'
        return html
    elif callable(data):
        # FUNCTION
        return f'<span class="function">{data}</span>'
    else:
        # UNKNOWN
        return f'<span class="unknown">{data}</span>'


# ========================================================= #
# ===  generate__html                                   === #
# ========================================================= #

def generate__html( html_lines=[],  html_config=None ):

    
    if ( html_config is None ): sys.exit( "[generate__html.py] html_config == ???" )
    title, paramsFile   = None, None
    cssFile, htmlFile   = None, None
    config              = jso.json__formulaParser( inpFile=html_config )
    settings, images    = config["settings"], config["images"]
    if ( "cssFile"    in settings ): cssFile    = settings[ "cssFile"    ]
    if ( "title"      in settings ): title      = settings[ "title"      ]
    if ( "paramsFile" in settings ): paramsFile = settings[ "paramsFile" ]
    if ( "htmlFile"   in settings ): htmlFile   = settings[ "htmlFile"   ]
    
    # ------------------------------------------------- #
    # --- [1] html header part                      --- #
    # ------------------------------------------------- #
    html_lines      += [ "<html>", "<head>" ]
    if ( title   ):
        html_lines  += [ f"<title>{title}</title>" ]
    if ( cssFile ):
        if ( htmlFile ):
            css_filepath = os.path.basename( cssFile )
            out_dirpath  = os.path.dirname ( htmlFile )
            css_copypath = os.path.join( out_dirpath, css_filepath )
            shutil.copy( cssFile, css_copypath )
        html_lines  += [ f'<link rel="stylesheet" type="text/css" href="{css_filepath}"/>' ] 
    html_lines      += [ "</head>", "<body>" ]
   
    # ------------------------------------------------- #
    # --- [2] html body part                        --- #
    # ------------------------------------------------- #
    if ( title ):
        html_lines += [ f'<h1>{title}</h1>' ]
    if ( paramsFile ):
        if ( os.path.exists( paramsFile ) ):
            data  = jso.json__formulaParser( inpFile=paramsFile )
        else:
            print( "[generate__html.py] cannot find paramsFile... {} ".format( paramsFile ) )
            sys.exit()
        translation  = translate__json2html( data )
        html_lines  += [ translation ]

    # ------------------------------------------------- #
    # --- [3] html image file                       --- #
    # ------------------------------------------------- #
    imgtag = '<img src="../{0}" width="{1}">'
    for key,obj in images.items():
        html_lines += [ imgtag.format( obj["filepath"], obj["width"] ) ]
        
    # ------------------------------------------------- #
    # --- [3] html closing part / save html file    --- #
    # ------------------------------------------------- #
    html_lines  += [ "</body>", "</html>" ]
    html_strings = "\n".join( html_lines )

    if ( htmlFile ):
        with open( htmlFile, "w" ) as f:
            f.write( html_strings )
    return( html_strings )
            
    
# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):

    default_html_config = "dat/html_config.json"
    
    # ------------------------------------------------- #
    # --- [1] arguments                             --- #
    # ------------------------------------------------- #
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument( "--html_config", help="system config file for html." )
    args   = parser.parse_args()

    if args.html_config:
        html_config = args.html_config
    else:
        html_config = default_html_config

    # ------------------------------------------------- #
    # --- [2] call arguments                        --- #
    # ------------------------------------------------- #
    generate__html( html_config=html_config )
    
