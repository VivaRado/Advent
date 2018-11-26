# from __future__ import absolute_import
# from fontTools.misc.py23 import *
# import gzip
# import tempfile
# from xml.etree.ElementTree import ElementTree, Element
#
import os
import sys
from os.path import dirname, join, abspath
from pathlib import Path
import copy
import json
#
from .efo_features import combine_fea
from .efo_features import split_fea
from .efo_fontinfo import read_efo_json_fontinfo
from .efo_fontinfo import get_font_file_array
from .efo_fontinfo import get_font_info_for_weight
from .efo_fontinfo import generate_fontinfo
from .efo_fontinfo import get_shared_info
from .efo_fontinfo import update_font_info
from .efo_groups import copy_groups_class_kerning
from .efo_groups import remove_groups_class_kerning
from .efo_kerning import copy_kerning
from .efo_lib import generate_lib
from .efo_metainfo import copy_metainfo
from .efo_glif import generate_contents_plist
from .efo_glif import copy_glif_files
#
#sys.path.insert(0, abspath(join(dirname("generic"), '..')))
#
from Lib.generic import generic_tools
from Lib.generic import lib_to_glyphlib
from Lib.components import comp_tools
#
#REMOVE
from pprint import pprint
#
import ufoLib
from distutils.dir_util import copy_tree
# from .glyphs import writeMissingGlyph, writeGlyphPath
# from .kerning import writeHKernElements
# from .tools import valueToString
#
'''default_fontinfo = [
	{
		"shared_info": {
			"familyName":"advent pro fmm"
		}
	},{
		"font_files":[
			"thn",
			"reg",
			"bld",
			"thn_it",
			"reg_it",
			"bld_it"
		]
	},{
		"font_info":[]
	},{
		"font_kerning_settings":[]
	}

]'''
#
class EFO(object):
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
		self.EFO_vectors = "vectors"
		#
		#
		if Path(self._in).name == "fontinfo.json":
			#
			print('BUILD')
			read_efo_json_fontinfo(self, "Upstream")
			#

			self.font_files = get_font_file_array(self)
			#
			if _out:
				#
				self._out = _out
				#
			else:
				#
				self._out = "Current"
				#
		else:
			#
			read_efo_json_fontinfo(self, "Downstream")
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
	def _efo_to_ufos(self, _fonts='', _flatten=False, _kerning_type="class"):
		#
		'''
		Export UFOs from EFO:
			
			Read /EFO/font_info.json

				For Every weight/font:

					Actions: 
						features.fea:
							combine all .fea files in /features folder
						fontinfo.plist
							read /font_info.json
							generate combined "shared" and per weight fontinfo.plist
						groups.plist
							copy /groups/kerning.plist to every UFO renamed as groups.plist
						kerning.plist
							copy /kerning/class/weight.plist to every UFO renamed as kerning.plist
						lib.plist
							read /glyphlib.xml and create lib.plist for every UFO
						metainfo.plist
							copy metainfo.plist to every UFO
						metainfo.plist
							read /glyphlib.xml and create glyphs/contents.plist for every UFO
						glyphs
							copy EFO glyphs to UFO glyphs for every UFO
							

		'''
		#
		#
		if _fonts != '':
			
			self._fonts = _fonts
			self.font_files = self._fonts.split(',')
			faults = generic_tools.check_given_fonts_exist(_fonts, self.font_files)
			_font_files = self.font_files

		else:

			faults = False
			_font_files = self.font_files
		#
		#
		#
		if faults == False:
			#
			print('\tGIVEN FONTS EXIST CONTINUING')
			#
			self.all_exported_ufo_dst = []
			#
			for f in _font_files:
				#
				self.current_font_file_name = f
				self.current_font_instance_name = generic_tools.sanitize_string(self.current_font_family_name+' '+self.current_font_file_name)
				self.current_font_instance_directory = os.path.join(self.current_font_family_directory,self.current_font_instance_name+'.ufo')
				self.current_fontinfo = get_font_info_for_weight(self)
				#
				generic_tools.make_dir(self.current_font_family_directory)
				generic_tools.make_dir(self.current_font_instance_directory)
				#
				self.all_exported_ufo_dst.append({f:self.current_font_instance_directory})
				#
				print('______________________________\n')
				print(self.current_font_instance_name)
				print('\n')
				#
				generate_fontinfo(self)
				combine_fea(self)
				#
				kerning_to_copy = _kerning_type # class / flat
				#
				if kerning_to_copy == "class":
					#
					copy_kerning(self, "class", "Downstream")
					copy_groups_class_kerning(self, "Downstream")
					#
				else:
					#
					copy_kerning(self, "flat", "Downstream")
					remove_groups_class_kerning(self)
					#
				#
				generate_lib(self)
				copy_metainfo(self, "Downstream")
				#
				generate_contents_plist(self)
				copy_glif_files(self, "Downstream")
				#
				if _flatten == True:
					#
					comp_tools.flatten_components(self.current_font_instance_directory)
					#
				#
			#
		else:
			#
			print('\tGIVEN FONTS INCONSISTENT ABORTING')
			#
		#
	#
	def _ufos_to_efo(self, _to_copy=["metainfo","features","glyphs","fontinfo","kerning","lib"], _ufos_to_temp=True, _from_compress=False):
		#
		read_efo_json_fontinfo(self, "Upstream")
		#
		self.font_files = get_font_file_array(self)
		#
		print('UFOs to EFO')
		#
		self.current_font_family_name = generic_tools.sanitize_string(self.fontinfo[0]["shared_info"]["familyName"])
		#
		if self._out != "Current":
			#
			self.new_efo_dir = self._out#os.path.join(*Path(self._in).parts[:-1])
			#
		else:
			#
			self.new_efo_dir = os.path.join(*Path(self._in).parts[:-1])
			#
		#
		temp_dir = os.path.join(self.new_efo_dir, self.EFO_temp)
		vectors_dir = os.path.join(self.new_efo_dir, self.EFO_vectors)
		features_dir = os.path.join(self.new_efo_dir, self.EFO_features_dir)
		#
		EFO_fontinfo_data = {}
		#
		new_info = copy.deepcopy(self.fontinfo)
		#
		x = 0
		#
		for f in self.font_files:
			#
			self.current_font_file_name = f
			self.current_font_instance_name = generic_tools.sanitize_string(self.current_font_family_name+' '+self.current_font_file_name)
			#
			if _from_compress:
				#
				self.current_source_ufo = os.path.join( self.current_source_ufo_family,self.current_font_instance_name+'.ufo' )
				#
			else:
				#
				self.current_source_ufo_family = os.path.join( self.new_efo_dir,self.current_font_family_name )
				#
			#
			self.current_source_ufo = os.path.join( self.current_source_ufo_family,self.current_font_instance_name+'.ufo' )
			#
			self.current_source_ufo_glyphs_dir = os.path.join(self.current_source_ufo,'glyphs')
			self.current_source_efo_features_dir = os.path.join(self.new_efo_dir,'features')
			
			self.current_source_ufo_lib = os.path.join(*(self.new_efo_dir,self.current_font_family_name,self.current_font_instance_name+'.ufo', 'lib.plist'))
			EFO_glyphlib_xml = os.path.join(self.new_efo_dir,'glyphlib.xml')
			#
			#
			if x == 0: # once
				#
				if "metainfo" in _to_copy:
					#
					copy_metainfo(self, "Upstream")
					#
				#
				if "lib" in _to_copy:
					#
					lib_to_glyphlib.lib_to_glyphlib(self.current_source_ufo_lib, EFO_glyphlib_xml)
					#
				#
				generic_tools.make_dir(temp_dir)
				generic_tools.make_dir(vectors_dir)
				#
				if "features" in _to_copy:
					#
					generic_tools.make_dir(features_dir)
					#
				#
			#
			if "glyphs" in _to_copy:
				#
				copy_glif_files(self, "Upstream")
				#
			#
			if "fontinfo" in _to_copy:
				#
				update_font_info(self, new_info, f)
				#
			#
			if "features" in _to_copy:
				#
				generic_tools.make_dir(os.path.join(self.current_source_efo_features_dir,"kern_fea"))
				#
				#
				split_fea(self, _from_compress)
				#
			#
			has_groups = generic_tools.determine_kerning_type_ufo(self.current_source_ufo)
			#
			if has_groups:
				#
				if "kerning" in _to_copy:
					#
					copy_kerning(self, "class","Upstream")
					copy_groups_class_kerning(self, "Upstream")
					#
				#
			else:
				#
				if "kerning" in _to_copy:
					#
					copy_kerning(self, "flat","Upstream")
					#
				#
			#
			x = x + 1
			#
		if "fontinfo" in _to_copy:
			# Save updated font info
			EFO_json_fontinfo = os.path.join(self.new_efo_dir,'fontinfo.json')
			#
			with open(EFO_json_fontinfo, "w") as fi:
				#
				json.dump(new_info, fi, indent=4, sort_keys=True)
				#
			#
		#
		if _ufos_to_temp:
			#Move UFO Source font family to EFO temp
			copy_tree(self.current_source_ufo_family, os.path.join(temp_dir,self.current_font_family_name))
			#
			#Remove UFO Source font family from root EFO dir
			generic_tools.rm_dir(self.current_source_ufo_family)
			#
			print("UFO Family Transfered To EFO/temp: ", self.current_source_ufo_family)
			#
		#
	#