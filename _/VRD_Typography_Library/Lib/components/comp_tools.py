#
import os
import time
from shutil import copyfile
from distutils.dir_util import copy_tree
#
import ufoLib
#
from Lib.ufo2svg import tools
from Lib.generic import generic_tools
import xml.etree.cElementTree as ET
#
'''
Flattens but punctuation is missaligned.
Intended only for the rendering procedute where the punctuation is ignored and only the number 1 contour is considered.
'''
def flatten_components(ufo_dir):
	#
	print('COMP: Flatten UFO Components')
	#
	reader = ufoLib.UFOReader(ufo_dir, validate=True)
	#
	source_dir = os.path.join(ufo_dir,'glyphs')
	target_dir = os.path.join(ufo_dir,'glyphs_flat')
	generic_tools.make_dir(target_dir)
	#
	copy_tree(source_dir, target_dir)
	#
	t_dir = target_dir#/media/root/Malysh1/winshm/advent_repo/Advent/_/exp/advent_pro_fmm/test.ufo/glyphs'
	#print('INPUT', ufo_dir)
	#print('OUTPUT', t_dir)
	#
	ufoWriter = ufoLib.GlyphSet(t_dir)
	#
	inGlyphSet = reader.getGlyphSet()
	#
	for glyphName in inGlyphSet.keys():
		#
		g = inGlyphSet[glyphName]
		#
		text = inGlyphSet.getGLIF(glyphName)
		comp = ufoLib.glifLib._fetchComponentBases(text)
		#
		if len(comp):
			#
			new_outline = []
			#
			source_glyph = os.path.join(t_dir,generic_tools.glyphNameToFileName(glyphName))
			#
			target_elem = ET.parse(source_glyph)
			target_dest = target_elem.find('outline')
			#
			for co in comp:
				#
				comp_source = inGlyphSet.getGLIF(co)
				tree = ET.fromstring(comp_source)
				outl = tree.find('outline')
				#
				for x in outl:
					#
					contour = ET.Element("contour")
					#
					for point in x:
						#
						contour.append(point)
						#
					#
					if len(contour):
						#
						target_dest.append(contour)
						#
					#
				#
			#
			for elem in target_elem.iter():
				for child in list(elem):
					if child.tag == 'component':
						elem.remove(child)
					elif child.tag == 'contour':
						#
						for point in list(child):
							#	
							if "move" in str(point.attrib):
								elem.remove(child)
								break
			#
			
			xml_str = ET.tostring(target_elem.getroot(), method='xml').decode().replace("'", '"')
			#print(ElementTree.tostring(svgGlyph, method='xml'))
			#
			#data = ET.tostring(target_elem.getroot())
			f = open(source_glyph, "w")
			f.write('<?xml version="1.0" encoding="UTF-8"?>\n'+xml_str) 
			#target_elem.write(source_glyph, encoding='utf8')
			#
		else:
			g.drawPoints(None) 
			ufoWriter.writeGlyph(glyphName, g, g.drawPoints)
		#
	#
	ufoWriter.writeContents()
	#
	time.sleep(2)
	#
	generic_tools.empty_dir(source_dir)
	#
	generic_tools.rm_dir(source_dir)
	os.rename(target_dir, source_dir)