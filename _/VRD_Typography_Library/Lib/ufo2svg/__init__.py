from __future__ import absolute_import
from fontTools.misc.py23 import *
import os
import re
import tempfile
from xml.etree import ElementTree
#from xml.etree.ElementTree import ElementTree, Element

from Lib.efo import efo_fontinfo
from Lib.efo import efo_metainfo
from Lib.generic import generic_tools
from .tools import *

from .glyphs import writeGlyphPath
from .glif2svg import convertUFOToSVGFiles
from .glif2svg import convertSVGFilesToEFO

#
from fontParts.world import *
#
from ufoLib import *
from .svg2glif import *
#
import svgutils as su

# from .efo_fontinfo import read_efo_json_fontinfo
# from .efo_fontinfo import get_font_file_array

class UFO2SVG(object):
	#
	read_efo_json_fontinfo = ""
	#
	def __init__(self, _in, _fonts=''):
		#
		self._in = _in
		self.EFO_fontinfo = "fontinfo.json"
		self.EFO_vectors_dir = "vectors"
		self.EFO_glyphs_dir = "glyphs"
		self.EFO_temp = "temp"
		#
		if len(_fonts) > 0:
			#
			self._fonts = _fonts
			#
	#
	
	def efo_to_svgs(self):
		#
		efo_fontinfo.read_efo_json_fontinfo(self)
		#
		print('UFO2SVG: Started Conversion of EFO to SVGs')
		#
		self.font_files = efo_fontinfo.get_font_file_array(self)
		self.given_fonts = self._fonts.split(',')
		self.current_font_family_glyphs_directory = os.path.join(self._in,self.EFO_glyphs_dir)
		self.current_font_family_vectors_directory = os.path.join(self._in,self.EFO_vectors_dir)
		#
		generic_tools.empty_dir(self.current_font_family_vectors_directory)
		#
		faults = generic_tools.check_given_fonts_exist(self._fonts, self.font_files)
		#
		if faults == False:
			#
			print('\tGIVEN FONTS EXIST CONTINUING')
			#
			for gf in self.given_fonts:
				#
				self.return_temp_and_vector_dirs(gf)
				#
				generic_tools.make_dir(self.current_font_family_vectors_directory)
				generic_tools.make_dir(self.current_font_instance_vectors_directory)
				#
				f = OpenFont(self.current_font_instance_temp_directory)
				#
				UFO_to_SVG = UFO2SVG(f)
				#
				convertUFOToSVGFiles(self, f, self.current_font_instance_name)
				#
			#
		else:
			#
			print('\tGIVEN FONTS INCONSISTENT ABORTING')
			#
		#
	#
	def svgs_to_efo(self):
		#
		efo_fontinfo.read_efo_json_fontinfo(self)
		#
		print('UFO2SVG: Started Conversion of SVGs to EFO')
		#
		self.font_files = efo_fontinfo.get_font_file_array(self)
		self.given_fonts = self._fonts.split(',')
		self.current_font_family_glyphs_directory = os.path.join(self._in,self.EFO_glyphs_dir)
		self.current_font_family_vectors_directory = os.path.join(self._in,self.EFO_vectors_dir)
		#
		print(self._fonts, self.font_files)
		#
		faults = generic_tools.check_given_fonts_exist(self._fonts, self.font_files)
		#
		if faults == False:
			#
			print('\tGIVEN FONTS EXIST CONTINUING')
			#
			for gf in self.given_fonts:
				#
				self.return_temp_and_vector_dirs(gf)
				#
				if os.path.isdir(self.current_font_instance_vectors_directory):
					#
					print('\tGIVEN FONT VECTORS EXIST CONTINUING')
					#
					f = OpenFont(self._in)
					#
					UFO_to_SVG = UFO2SVG(f)
					#
					convertSVGFilesToEFO(self, f, gf)
					#
				else:
					#
					print('\tGIVEN FONT VECTORS DONT EXIST IGNORING')
					#
			#
		else:
			#
			print('\tGIVEN FONTS INCONSISTENT ABORTING')
			#
		#
	#
	def return_temp_and_vector_dirs(self, gf):
		#
		self.current_font_file_name = gf
		self.current_font_family_directory = os.path.join(self._in,self.EFO_temp)
		self.current_font_family_vectors_directory = os.path.join(self._in,self.EFO_vectors_dir)
		self.current_font_instance_name = generic_tools.sanitize_string(self.current_font_family_name+' '+self.current_font_file_name)
		#
		self.current_font_family_temp_directory = os.path.join(self.current_font_family_directory,self.current_font_family_name)
		self.current_font_instance_temp_directory = os.path.join(self.current_font_family_temp_directory,self.current_font_instance_name+'.ufo')
		#
		self.current_font_family_vectors_directory = os.path.join(self.current_font_family_vectors_directory,self.current_font_family_name)
		self.current_font_instance_vectors_directory = os.path.join(self.current_font_family_vectors_directory,self.current_font_instance_name)