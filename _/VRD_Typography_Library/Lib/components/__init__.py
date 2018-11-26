# from __future__ import absolute_import
# from fontTools.misc.py23 import *
# import gzip
# import tempfile
# from xml.etree.ElementTree import ElementTree, Element
#
import os
import sys
from os.path import dirname, join, abspath
#
#
#sys.path.insert(0, abspath(join(dirname("generic"), '..')))
#
from Lib.generic import generic_tools
#
#REMOVE
from pprint import pprint
#
import ufoLib
# from .glyphs import writeMissingGlyph, writeGlyphPath
# from .kerning import writeHKernElements
# from .tools import valueToString
#
#
class COMPS(object):
	#
	read_efo_json_fontinfo = ""
	#
	def __init__(self, _in, _out=None):
		#
		self._in = _in
		#
		#
		self.EFO_fontinfo = "fontinfo.json"
		self.EFO_features_dir = "features"
		self.EFO_groups_dir = "groups"
		self.EFO_kerning_dir = "kerning"
		self.EFO_glyphs_dir = "glyphs"
		self.EFO_temp = "temp"
		#
		read_efo_json_fontinfo(self)
		#
		self.font_files = get_font_file_array(self)
		#
		if _out:
			#
			self._out = _out
			#
			self.current_font_family_directory = os.path.join(self._out,self.current_font_family_name)
			#
			print(self.current_font_family_directory)
			print(self._in, self._out)
			#
		#
	#
	def components_flatten(self, _fonts=''):
		#
		pass
		#