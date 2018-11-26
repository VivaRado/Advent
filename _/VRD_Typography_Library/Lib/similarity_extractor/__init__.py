import os
import sys
from os.path import dirname, join, abspath
#
import datetime
#
import json
#
from Lib.efo import efo_fontinfo
#
this_path = os.path.dirname(os.path.realpath(__file__))
scripts_path = os.path.abspath(os.path.join(os.path.join(this_path, '..', '')))
#
tfs_path = os.path.join(scripts_path,'tfs3/common')
#
sys.path.append(tfs_path)
#
from fontParts.world import *
from Lib.tfs3.common.TFSFont import *
#from TFSSvg import *
#

from Lib.generic import generic_tools
#
from .simex_tools import *
from .simex_permut import *
from .simex_plist_comp import *
from .simex_plist_kern import *
#
#
#REMOVE
from pprint import pprint
#
checking = ['A', 'Alphatonos', 'Abreve', 'Deltagreek', 'Omicron', 'Theta', 'O', 'E', 'F', 'P', 'R', 'L', 'Lacute', 'J', 'Eng', 'V', 'W']
#checking = ['A', 'Alphatonos', 'Abreve', 'Deltagreek', 'Omicron', 'Theta', 'O']
check_list = False
#
# SIMILARITY PURPOSE VARIABLES
# left, center, right
max_diff_kern = [0.8, 0.8, 0.8] # loose for kern groups
max_diff_comp = [1, 1, 1] 		# tight for components
#
class SIMEX(object):
	#
	def __init__(self, _in, _purpose, _compress="Yes", _font=''):
		#
		self._in = _in
		self._purpose = _purpose
		self._compress = _compress
		self.EFO_fontinfo = "fontinfo.json"
		self.SIMEX_temp = "temp_simex"
		#self.EFO_vectors_dir = "vectors"
		#self.EFO_glyphs_dir = "glyphs"
		self.EFO_temp = "temp"
		self.EFO_groups = "groups"

		efo_fontinfo.read_efo_json_fontinfo(self)
		
		self.current_font_family_directory = os.path.join(self._in,self.current_font_family_name)
		#
		if len(_font) > 0:
			#
			self._font = _font
			#
	#
	#def compress_similarity_to_plist(self, udir):
		#
		#udir = input("component class loc json file: ")
		#
		#if len(udir) > 0:
			#
		#build_group_plist_data_test(udir)
			#
		#
		#
	#
	def extract_similarity(self):
		#
		efo_fontinfo.read_efo_json_fontinfo(self)
		#
		print('SIMEX: Started Similarity Extraction')
		#
		self.font_files = efo_fontinfo.get_font_file_array(self)
		self.given_fonts = self._font.split(',')
		#self.current_font_family_glyphs_directory = os.path.join(self._in,self.EFO_glyphs_dir)
		#self.current_font_family_vectors_directory = os.path.join(self._in,self.EFO_vectors_dir)
		#
		faults = generic_tools.check_given_fonts_exist(self._font, self.font_files)
		#
		#
		if faults == False:
			#
			print('\tGIVEN FONTS EXIST CONTINUING')
			#
			all_dst = []
			#
			for gf in self.given_fonts:
				#
				print('\tSIMEX: Extracting Similarity from:', gf)
				#
				self.return_self_dirs(gf)
				#
				ufo_src_path = self.current_font_instance_directory
				#
				srcUfoFont = TFSFontFromFile(ufo_src_path)
				#
				glyph_nums = get_glyphs(srcUfoFont, check_list, checking)
				#
				if self._purpose == "comp":
					max_diff = max_diff_comp
					print('\tExtracting Similarity for Components (1 to 1)')
				else:
					max_diff = max_diff_kern
					print('\tExtracting Similarity for Kerning '+str(max_diff_kern)+'[left, center, right]'+' edit : max_diff_kern in SIMEX init for custom diff values.')
				#
				in_mils = init_permut(glyph_nums, 'right', max_diff)
				#
				mil_dict = in_mils[0]
				all_mils = in_mils[1]
				#
				#
				uni_groups = unique_groups(all_mils)
				#
				r = json.dumps(uni_groups)
				#
				parsed = json.loads(r)
				parse_dumped = json.dumps(parsed, indent=4, sort_keys=False)
				#

				#
				time_now = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
				filename = gf+'.json'
				#
				init_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), self.SIMEX_temp)
				#
				generic_tools.make_dir(init_path)
				#
				dst_dir = os.path.abspath(os.path.join(init_path, filename))
				#
				all_dst.append(dst_dir)
				#
				with open(dst_dir, 'w') as the_file:
					#
					the_file.write(parse_dumped)
					the_file.close()
					#
				#
				print('\n\tSIMEX: Done Extracting Similarity and Saved:', dst_dir)
				#
			#
			if self._compress == "Yes":
				#
				for x in all_dst:
					#
					if self._purpose == "comp":
						#
						print('\tCOMPRESSING to COMPONENTS PLIST: ',x)
						#
						build_component_group_plist(x, self.EFO_groups_dir)
					else:
						#
						print('\tCOMPRESSING to KERNING PLIST: ',x)
						#
						build_kerning_group_plist(x, self.EFO_groups_dir)
					#
				#
			#
			generic_tools.empty_dir(os.path.join(self._in, self.EFO_temp))
			#
		else:
			#
			print('\tGIVEN FONTS INCONSISTENT ABORTING')
			#
		#
	#
	def return_self_dirs(self, gf):
		#
		self.current_font_file_name = gf
		self.current_font_family_directory = os.path.join(os.path.join(self._in, self.EFO_temp),self.current_font_family_name)
		self.current_font_instance_name = generic_tools.sanitize_string(self.current_font_family_name+' '+self.current_font_file_name)
		self.current_font_instance_directory = os.path.join(self.current_font_family_directory,self.current_font_instance_name+'.ufo')
		self.current_fontinfo = efo_fontinfo.get_font_info_for_weight(self)
		#
		self.EFO_groups_dir = os.path.join(self._in, self.EFO_groups)
		#