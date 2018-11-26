import os
import sys
from os.path import dirname, join, abspath
#
import datetime
#
import json
#
#from Lib.efo import efo_fontinfo
#
from Lib.generic import generic_tools
#
#import os
# import io
import random
from math import sqrt, ceil, floor
#import datetime
import string
#
import itertools
#
import sys
from sys import argv
import re
#
import readline 
import rlcompleter 
from argparse import ArgumentParser
import atexit
#
import io
#
from shutil import copyfile
#
import copy
#
import difflib
import plistlib
#import json
#
import collections
from collections import Counter
#

plist_header = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>\n'''
#
#
plist_footer = '''\n</dict>\n</plist>'''
#
plist_string = '''		<key>{0}</key>
		<integer>{1}</integer>'''
#
plist_group = '''	<key>{0}</key>
	<dict>
{1}\n	</dict>\n'''
	#
#
fea_pos_line = '''pos {0} {1} {2};'''
do_fea_groups = ''
do_fea_kern = ''
#
flc_file_header = '''%%FONTLAB CLASSES\n\n'''
#
flc_content = '''%%CLASS _{0}
%%GLYPHS  {1}' {2}
%%KERNING {3} 0
%%END\n\n'''
#
fea_class_content = '''@{0} = [{1} {2}];\n'''
#
fea_prefix = '''# Languagesystems Start
# Prefix: Languagesystems
languagesystem DFLT dflt;
languagesystem grek dflt;
languagesystem latn dflt;
# Languagesystems End\n\n'''
#
class COMPRESS(object):
	#
	def __init__(self, _f_name, _temp_source, _temp_source_copy, _source_efo_similarity_kern_plist):
		#
		self._current_font_instance_weight = _f_name
		self._temp_source = _temp_source
		self._temp_source_copy = _temp_source_copy
		self._source_efo_similarity_kern_plist = _source_efo_similarity_kern_plist
		#
	#
	#
	def get_kern_name_and_dir(self, k):
		#
		ld = k.split('@MMK_')[1]
		ds = ld.split('_', 1)
		kd = ds[0]
		lt = ds[1]
		#
		return[lt, kd]
		#
	#
	def make_fea_class_lines(self,p_g):
		# #
		all_kern_flc = ''
		#
		for k,v in p_g.items():
			#
			k_spl = self.get_kern_name_and_dir(k)
			kern_name = k_spl[0]
			kern_dir = k_spl[1]
			#
			v.sort()
			#
			try:
				#
				v.remove(kern_name)
				v.insert(0, kern_name)
				#
			except Exception:
				#
				v.insert(0, kern_name)
				#
			#
			v.pop(0)
			#
			num_dir = ''
			#
			if kern_dir == 'R':
				#
				num_dir = '1'
				#
			#
			all_kern_flc = all_kern_flc + fea_class_content.format(kern_name+num_dir, kern_name, ' '.join(v), kern_dir)
			#
		#
		return all_kern_flc
	#
	def make_kern_lines_dict(self, f_kern_data):
		#
		all_kern_plist = ''
		plist_strings = ''
		#
		kern_dict = {}
		#
		for x in f_kern_data:
			#
			let_a = x[0]
			let_b = x[1]
			k_int = x[2]
			#
			if let_a in kern_dict:
				#
				kern_dict[let_a].update({let_b:k_int})
				#
			else:
				#
				kern_dict[let_a] = {let_b:k_int}
				#
			#
		#
		return kern_dict
	#
	#
	def make_kern_lines(f_kern_data):
		#
		all_kern_plist = ''
		plist_strings = ''
		#
		for x in f_kern_data:
			#
			let_a = x[0]
			let_b = x[1]
			k_int = x[2]
			#
			plist_strings = plist_string.format(let_b,k_int)
			#
			all_kern_plist = all_kern_plist + plist_group.format(let_a, plist_strings)
			#
			#
		#
		all_kern_plist = plist_header + all_kern_plist + plist_footer
		#
		return all_kern_plist
	#
	def get_kern_int(self, left, right, p_k):
		#
		found_int = 0
		#
		for k,v in p_k.items():
			#
			if k == left:
				#
				for x,y in v.items():
					#
					if x == right:
						#
						found_int = y
						#
						break
						#
					#
				#
			#
		#
		return found_int
		#
		#
	#
	def remove_redundant_kern_values(self, final_ckp, _dict):
		#
		tmpDict = _dict.copy()
		#
		for z in final_ckp:
			#
			left = z[0]
			right = z[1]
			#
			for k,v in tmpDict.items():
				#
				if k == left:
					#
					for x,y in v.items():
						#
						if x == right:
							#
							_dict = generic_tools.get_dict_wo_key(_dict, k)
							#
						#
					#
				#
			#
		return _dict
		#
	#
	def do_fea_kern_file(self, final_class_kern_pairs):
		#
		#do_fea_kern = 'feature kern {\n'
		#
		for y in final_class_kern_pairs:
			#
			k_dir = y[3]
			k_int = y[2]
			#
			let_a = self.get_kern_name_and_dir(y[0])
			let_b = self.get_kern_name_and_dir(y[1])
			#
			fea_line = fea_pos_line.format('@_'+let_a[0], '@_'+let_b[0]+'1', str(k_int))
			#
			#do_fea_kern = do_fea_kern +'    '+fea_line + '\n'
			#
			self.final_class_kerning.append(fea_line)
			#
		#
		#do_fea_kern = do_fea_kern + '} kern;'
		#
		#return final_class_kerning
		#
	#
	def fea_kern_list_to_file(self, final_kerning_list):
		#
		kern_strings = '''# Kerning Start
feature kern { # Kerning
# DEFAULT
lookup kern1 {\n'''
		#
		for y in final_kerning_list:
			#
			kern_strings = kern_strings +'    '+y + '\n'
			#
			#final_class_kerning.append(fea_line)
			#
		#
		kern_strings = kern_strings + '''}kern1;
script grek; # Greek
lookup kern1;
script latn; # Latin
lookup kern1;
} kern;
# Kerning End'''
		#
		return kern_strings
		#
	#
	def permut_plist_keys(self, g_plist_keys):
		#
		g_plist_permut = []
		#
		for o in g_plist_keys:
			#
			ltkd_a = self.get_kern_name_and_dir(o)
			#
			for p in g_plist_keys:
				#
				ltkd_b = self.get_kern_name_and_dir(p)
				#
				if ltkd_a[1] == 'R' and ltkd_b[1] == 'R':
					#
					pass
					#
				elif ltkd_a[1] == 'L' and ltkd_b[1] == 'L':
					#
					pass
					#
				else:
					#
					if ltkd_a[1] == 'R' and ltkd_b[1] == 'L':
						#
						g_plist_permut.append([p,o])
						#
					#
					elif ltkd_a[1] == 'L' and ltkd_b[1] == 'R':
						#
						g_plist_permut.append([o,p])
						#
					#
			#
		g_plist_permut.sort()

		result_permut = list(g_plist_permut for g_plist_permut,_ in itertools.groupby(g_plist_permut))

		return result_permut
		#
	#
	def remove_class_replace(self, p_k_clean, class_groups):
		#
		for x,j in class_groups.items():
			#
			if '@MMK_R_' in x:
				#
				first_letter = x.replace('@MMK_R_','')
				#
			else:
				#
				first_letter = x.replace('@MMK_L_','')
				#
			#
			j.append(first_letter)
			#
		#
		for k,v in p_k_clean.items():
			#
			wanted_list = []
			#
			for d,b in v.items():
				#
				wanted_list.append(d)
				#
			#
			this_num = 0
			#
			for f,g in class_groups.items():
				#
				match_list = []
				#
				for p in g:
					#
					if p in wanted_list:
						#
						if p not in match_list:
							#
							this_num = p_k_clean[k][p]
							#
							match_list.append(p)
							wanted_list.remove(p)
							#
							del p_k_clean[k][p]
						#
					#
					if match_list == g:
						#
						_right_f = f.replace('_L_','_R_')
						#
						p_k_clean[k][_right_f] = this_num
						#
					#
			#
		#
		return p_k_clean
		#
	#
	def do_fea_kern_file_additions(self, final_class_kern_pairs):
		#
		#do_fea_kern = 'feature kern {\n'
		#
		for k,y in final_class_kern_pairs.items():
			#
			for x,z in y.items():
				#
				k_int = z
				#
				let_a = k
				let_b = x
				#
				if '@MMK_L_' in let_a or '@MMK_R_' in let_a:
					#
					ltkd_a = self.get_kern_name_and_dir(let_a)
					#
					let_a = '@_'+ltkd_a[0]
					#
				if '@MMK_L_' in let_b or '@MMK_R_' in let_b:
					#
					ltkd_b = self.get_kern_name_and_dir(let_b)
					#
					let_b = '@_'+ltkd_b[0]+'1'
					#
				#
				fea_add_line = fea_pos_line.format(let_a, let_b, str(k_int))
				#
				#
				#do_fea_kern = do_fea_kern +'    '+fea_add_line + '\n'
				#
				self.final_class_kerning.append(fea_add_line)
			#
		#
		#do_fea_kern = do_fea_kern + '} kern;'
		#
		#return final_class_kerning
		#
	#
	def do_compress(self, p_groups, p_kerning, dir_to_comp_ufo_file):
		#
		p_g = plistlib.readPlist(p_groups)
		p_k = plistlib.readPlist(p_kerning)
		#
		all_kern_plist = ''
		#
		g_plist_keys = []
		all_affected_glyphs = []
		#
		for k,v in p_g.items():
			#
			g_plist_keys.append(k)
			all_affected_glyphs.append(k)
			all_affected_glyphs = all_affected_glyphs + v
			#
		#
		g_plist_permut = self.permut_plist_keys(g_plist_keys)
		#
		final_class_kern_pairs = []
		self.final_class_kerning = []
		#
		for pk in g_plist_permut:
			#
			ltkd_a = self.get_kern_name_and_dir(pk[0])
			ltkd_b = self.get_kern_name_and_dir(pk[1])
			#
			kern_int = self.get_kern_int(ltkd_a[0], ltkd_b[0], p_k)
			#
			#
			if kern_int == 0:
				pass
			else:
				#
				k_dir = ltkd_a[1]
				#
				if k_dir == "L":
					#
					kern_detail = [pk[0], pk[1], kern_int, k_dir]
					#
				else:
					#
					kern_detail = [pk[1], pk[0], kern_int, k_dir]
					#
				#
				final_class_kern_pairs.append(kern_detail)
				#
			#
		#
		all_affected_glyphs_permut = []
		#
		for x in all_affected_glyphs:
			#
			for y in all_affected_glyphs:
				#
				all_affected_glyphs_permut.append([x,y])
				#
			#
		#
		old_pg = generic_tools.copy_dict(p_g)
		old_p_k = generic_tools.copy_dict(p_k)
		#
		fea_classes = '# Classes Start\n'+self.make_fea_class_lines(old_pg)+'# Classes End\n\n'
		#
		p_k_clean = self.remove_redundant_kern_values(all_affected_glyphs_permut,old_p_k)
		p_k_class_replace = self.remove_class_replace(p_k_clean, old_pg)
		#
		self.do_fea_kern_file(final_class_kern_pairs)
		self.do_fea_kern_file_additions(p_k_class_replace)
		#
		#
		new_data = fea_prefix+fea_classes+self.fea_kern_list_to_file(sorted(self.final_class_kerning, key=lambda x: x.count('@_')))
		generic_tools.save_file(dir_to_comp_ufo_file, 'features'+'.fea', new_data)
		#
		#
		class_kerning_plist = self.make_kern_lines_dict(final_class_kern_pairs)
		total_kerning = class_kerning_plist.update(p_k_class_replace)
		k_c_temp = 'kerning'+'.plist'
		dstFile = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)),os.path.join(dir_to_comp_ufo_file,k_c_temp)))
		plistlib.writePlist(class_kerning_plist, dstFile)
		#
	#
	def do_class_kern_replacement(self):
		#
		dir_flat_ufo_file = self._temp_source
		dir_to_comp_ufo_file = self._temp_source_copy
		file_base_group = self._source_efo_similarity_kern_plist
		#
		dir_flat_ufo_file_kern=os.path.join(dir_flat_ufo_file,'kerning.plist')
		#
		copyfile(file_base_group, os.path.join(dir_to_comp_ufo_file,'groups.plist'))
		#
		print('Compressing:', self._current_font_instance_weight)
		#
		self.do_compress(file_base_group, dir_flat_ufo_file_kern, dir_to_comp_ufo_file)
		#
	#