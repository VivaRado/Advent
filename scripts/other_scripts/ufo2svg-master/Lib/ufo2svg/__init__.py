from __future__ import absolute_import
from fontTools.misc.py23 import *
import os
import tempfile
from xml.etree.ElementTree import ElementTree, Element

from .glyphs import writeGlyphPath
from .tools import valueToString


header = """<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd" >
"""

def convertUFOToSVGFiles(font, destinationPathOrFile=None, ignoreGlyphs=[] ):

	for glyphName in sorted(font.keys()):
		#
		if glyphName == ".notdef" or glyphName in ignoreGlyphs:
			continue
		glyph = font[glyphName]
		
		the_svg = writeGlyphPath(glyph)
		#
		svg = Element("svg", attrib=dict(version="1.1", xmlns="http://www.w3.org/2000/svg", width=valueToString(glyph.width)))
		svgDefs = Element("defs")
		#
		svg.append(svgDefs)
		svg.append(the_svg)

		print(glyphName)
		#
		dest_folder = '/media/root/Malysh1/winshm/advent_repo/Advent/font_source/source_svg/crap'
		#
		f = open(dest_folder+'/'+glyphName+'.svg', "wb")
		#
		temp = BytesIO()
		tree = ElementTree(svg)
		#
		tree.write(temp)
		data = temp.getvalue()
		#
		temp.close()
		print(str(data))
		#
		f.write(data)
		#
		f.close()
		#
	#