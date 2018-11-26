import xml.etree.ElementTree as ET
import os
import re
from io import BytesIO
import tempfile

from .tools import *
from .glyphs import writeGlyphPath
from .simple_path import *

from .svg2glif import *

from Lib.generic import generic_tools

header = """<?xml version="1.0" encoding="utf-8"?>
"""
#
flush_space = '                                     '
#

def convertUFOToSVGFiles(self, _f, item_name, ignoreGlyphs=[] ):
	#
	destinationPathOrFile = self.current_font_instance_vectors_directory
	#
	font = _f
	#
	all_keys_sorted = sorted(font.keys())
	#
	x = 0
	#
	all_ignored = []
	#
	print('UFO2SVG: Converting : '+ item_name)
	#
	for glyphName in all_keys_sorted:
		#
		glifname = generic_tools.glyphNameToFileName(glyphName).split('.glif')[0]
		#
		if glyphName in ignoreGlyphs:
			#
			pass
			#
		else:
			#
			glyph = font[glyphName]
			#
			glyph_box = ''
			#
			if glyph.box:
				#
				glyph_box = " ".join(map(str,glyph.box))
				#
			#
			the_path = writeGlyphPath(glyph)
			#
			if glyph.box:
				#			
				svg = ET.Element("svg", attrib=dict(version="1.0", xmlns="http://www.w3.org/2000/svg", width="0px", height="0px", x="0px", y="0px", viewBox="0 0 0 0"))
				#
			else:
				#			
				svg = ET.Element("svg", attrib=dict(version="1.0", xmlns="http://www.w3.org/2000/svg", x="0px", y="0px", viewbox="0 0 0 0"))
				#
			#
			svg.append(the_path)
			#
			#
			dest_folder = destinationPathOrFile
			#
			f = open(dest_folder+'/'+glifname+'.svg', "wb")
			#
			temp = BytesIO()
			temp.write(bytes(header, 'utf-8'))
			tree = ET.ElementTree(svg)
			#
			tree.write(temp)
			data = temp.getvalue()
			#
			temp.close()
			#
			f.write(data)
			#
			f.close()
			#
			if glyph.box:
				#
				pass
				#
			x = x + 1
			#
			if x == len(all_keys_sorted):

				print('\r\t'+'CONVERTED ALL '+str(len(all_keys_sorted))+' GLIFs to SVGs'+flush_space,end='')
				
			else:

				print('\r\t'+'CONVERTING: '+glifname+flush_space,end='')
			#
	#
	print('\n\tIGNORED: '+str(','.join(ignoreGlyphs+['contents.plist'])))
	#
def convertSVGFilesToEFO(self, _f, item_name, ignoreGlyphs=[] ):
	#
	current_font_dir = self.current_font_instance_vectors_directory
	#
	font = _f
	#
	x = 0
	#
	all_ignored = []
	#
	print('SVG2UFO: Converting : '+ item_name)
	#
	all_keys_sorted = sorted(os.listdir(current_font_dir))
	#
	for file in all_keys_sorted:
		#
		if file.endswith(".svg"):
			#
			glifname = file.split('.svg')[0]
			#
			glyphName = generic_tools.GLIFFileNametoglyphName(glifname)
			#
			svg_file = os.path.join(current_font_dir,file)
			#
			if glyphName in ignoreGlyphs:
				#
				pass
				#
			else:
				#
				tree = ET.parse(svg_file)
				#
				svg_data = tree.getroot()
				svg_string = ET.tostring(svg_data, encoding='utf8', method='xml').decode()
				#
				#
				if 'd' in svg_data[0].attrib:
					#
					path_d = svg_data[0].attrib['d']
					
					#
					if len(path_d) > 1:
						#
						flip_path = formatPath(flipPath(parsePath(path_d), horizontal=True, vertical=False))
						svg_data[0].attrib['d'] = flip_path
						svg_string = ET.tostring(svg_data, encoding='utf8', method='xml').decode()
						#
					#
				#
				glif = svg2glif(svg_string, glyphName)
				#
				EFO_glyphs_dir = os.path.join(self._in, self.EFO_glyphs_dir)
				EFO_current_font_item = os.path.join(EFO_glyphs_dir, item_name)
				outfile = os.path.join(EFO_current_font_item, glifname+'.glif')
				#
				with open(outfile, 'w', encoding='utf-8') as f:
					#
					f.write(glif)
					#pass
					#
				x = x + 1
				#
				if x == len(all_keys_sorted):

					print('\r\t'+'CONVERTED ALL '+str(len(all_keys_sorted))+' SVGs to GLIFs'+flush_space,end='')
					
				else:

					print('\r\t'+'CONVERTING: '+glifname+flush_space,end='')
				#
	#
	print('\n\tIGNORED: '+str(','.join(ignoreGlyphs)))
	#
#