#!/usr/bin/env python
import os
#
#from Lib.ufo2svg import convertUFOToSVGFont 
from Lib.ufo2svg import convertUFOToSVGFiles 
#
from fontParts.world import *
#
from ufoLib import *
#
#
#
#
#
# python startup file 
import readline 
import rlcompleter 
import atexit
# tab completion 
readline.parse_and_bind('tab: complete') 
# history file 
histfile = os.path.join(os.environ['HOME'], '.pythonhistory') 
try: 
    readline.read_history_file(histfile) 
except IOError: 
    pass 
atexit.register(readline.write_history_file, histfile) 
del histfile, readline, rlcompleter
#
#
#
#
#
#
#
#

#
ufo_src_path = input("UFO file: ")
#
#srcUfoFont = OpenFont(ufo_src_path)
f = OpenFont(ufo_src_path)
print(f)
print('____')
print(f.info.familyName)
#f = UFOReader(ufo_src_path, validate=True)
## get the current font
#cf = f['CurrentFont']

## create a layer name based on the familyName and styleName of the opend font
#layerName = "%s_%s" %(f.info.familyName, f.info.styleName)
#
dest = '/media/root/Malysh1/winshm/advent_repo/Advent/font_source/source_svg/font_conv'
#

# loop over all glyphs in the font

## if the glyph doenst exist in the current font, create a new glyph
convertUFOToSVGFiles(f, dest)


# ## we are done :)
# print(f)
