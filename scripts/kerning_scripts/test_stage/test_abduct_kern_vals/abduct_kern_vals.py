import os
# import io
import random
from math import sqrt, ceil, floor
import datetime
import string
#
import sys
from sys import argv
import re
#
import readline 
import rlcompleter 
import atexit
#
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
import difflib
import plistlib
import json
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
fea_pos_line = '''    pos {0} {1} {2};'''
do_fea_groups = ''
do_fea_kern = ''
#
#
flc_file_header = '''%%FONTLAB CLASSES\n\n'''
#
flc_content = '''%%CLASS _{0}
%%GLYPHS  {1}' {2}
%%KERNING {3} 0
%%END\n\n'''
#
#
def find_kern_int(left, right, kern_data):
	#
	found_int = 0
	#
	for k,v in kern_data.items():
		#
		current_items = {}
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
def get_kern_name_and_dir(k):
	#
	ld = k.split('@MMK_')[1]
	ds = ld.split('_', 1)
	kd = ds[0]
	lt = ds[1]
	#
	return[lt, kd]
	#
#
def make_flc_lines(p_g):
	# #
	all_kern_flc = ''
	#
	for k,v in p_g.items():
		#
		#flc_string = ''
		#
		k_spl = get_kern_name_and_dir(k)
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
		#flc_string = flc_string.format(let_b,k_int)
		#
		all_kern_flc = all_kern_flc + flc_content.format(kern_name+num_dir, kern_name, ' '.join(v), kern_dir)
		#
			
		#
	#
	# letter_and_dir = k.split('@MMK_')[1]
	# dir_kern_split = letter_and_dir.split('_', 1)
	# kern_dir = dir_kern_split[0]
	# letter = dir_kern_split[1]
	#
	print(all_kern_flc)
	#all_kern_flc = flc_file_header + all_kern_flc
	#
	return flc_file_header + all_kern_flc
#
def make_kern_lines(f_kern_data):
	# #
	# letter_and_dir = k.split('@MMK_')[1]
	# dir_kern_split = letter_and_dir.split('_', 1)
	# kern_dir = dir_kern_split[0]
	# letter = dir_kern_split[1]
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
def get_dict_wo_key(dictionary, key):
	"""Returns a **shallow** copy of the dictionary without a key."""
	_dict = dictionary.copy()
	_dict.pop(key, None)
	return _dict
#
def get_kern_int(left, right, p_k):
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
					#print('DELETING:', k)
					#
					#p_k = get_dict_wo_key(p_k, k)
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
def remove_redundant_kern_values(final_ckp, p_k):
	#
	tmpDict = p_k.copy()
	#
	for z in final_ckp:
		#
		left = z[0]
		right = z[1]
		#
		#print(left[0], right[0])
		#
		for k,v in tmpDict.items():
			#
			if k == left:
				#
				for x,y in v.items():
					#
					if x == right:
						#
						#print('DELETING:', k)
						#
						p_k = get_dict_wo_key(p_k, k)
						#
					#
				#
			#
		#
	return p_k
	#
#
def do_fea_kern_file(final_class_kern_pairs):
	#
	do_fea_kern = 'feature kern {\n'
	#
	for y in final_class_kern_pairs:
		#
		#print(y)
		#
		k_dir = y[3]
		k_int = y[2]
		#
		let_a = get_kern_name_and_dir(y[0])
		let_b = get_kern_name_and_dir(y[1])
		#
		do_fea_kern = do_fea_kern + fea_pos_line.format('@_'+let_a[0], '@_'+let_b[0]+'1', str(k_int)) + '\n'
		#
	#
	do_fea_kern = do_fea_kern + '} kern;'
	#
	return do_fea_kern
	#
#
def permut_plist_keys(g_plist_keys):
	#
	g_plist_permut = []
	#
	for o in g_plist_keys:
		#
		ltkd_a = get_kern_name_and_dir(o)
		#
		for p in g_plist_keys:
			#
			ltkd_b = get_kern_name_and_dir(p)
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
				print('-----')
				print(ltkd_a, ltkd_b)
				print('=====')
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
	return g_plist_permut
	#
#
def save_file(location, name, content):
	#
	time_now = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
	filename = time_now+name
	#
	dstFile = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)),os.path.join(location,filename)))
	#
	with open(dstFile, 'w') as the_file:
		the_file.write(content)
		the_file.close()
	#
	#
#
def do_adbuct(p_groups, p_kerning):
	#
	p_g = plistlib.readPlist(p_groups)
	#global p_k
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
	#
	g_plist_permut = permut_plist_keys(g_plist_keys)
	#
	print(len(g_plist_keys))
	print(len(g_plist_permut))
	#
	final_class_kern_pairs = []
	#
	for pk in g_plist_permut:
		#
		ltkd_a = get_kern_name_and_dir(pk[0])
		ltkd_b = get_kern_name_and_dir(pk[1])
		#
		kern_int = get_kern_int(ltkd_a[0], ltkd_b[0], p_k)
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
	print(len(final_class_kern_pairs))
	print(len(all_affected_glyphs))
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
	#
	#
	fea_file = do_fea_kern_file(final_class_kern_pairs)
	save_file('reducted_kerning/', '_features'+'.fea', fea_file)
	print(fea_file)
	#
	#
	#
	fl_class_file = make_flc_lines(p_g)
	save_file('reducted_kerning/', '_fl_class_file'+'.flc', fl_class_file)
	#
	#
	#
	class_kerning_plist = make_kern_lines(final_class_kern_pairs)
	save_file('reducted_kerning/', '_kern_class'+'.plist', class_kerning_plist)
	#
	#
	#
	p_k = remove_redundant_kern_values(all_affected_glyphs_permut,p_k)
	#
	time_now = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
	filename = time_now+'_kern_write'+'.plist'
	dstFile = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)),os.path.join('reducted_kerning/',filename)))
	plistlib.writePlist(p_k, dstFile)
	#
#
#
#
p_groups_src_path = input("groups plist file: ")
p_kerning_src_path = input("kerning plist file: ")
#
do_adbuct(p_groups_src_path, p_kerning_src_path)
#