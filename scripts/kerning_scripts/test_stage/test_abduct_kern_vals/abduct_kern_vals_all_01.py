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
from argparse import ArgumentParser
import atexit
#
import io
#
from shutil import copyfile
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
fea_class_content = '''@_{0} = [{1} {2}];\n'''
#
fea_prefix = '''# Prefix: Languagesystems
languagesystem DFLT dflt;
languagesystem grek dflt;
languagesystem latn dflt;'''
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
def make_fea_class_lines(p_g):
	# #
	all_kern_flc = ''
	#
	for k,v in p_g.items():
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
		all_kern_flc = all_kern_flc + fea_class_content.format(kern_name+num_dir, kern_name, ' '.join(v), kern_dir)
		#
	#
	return all_kern_flc
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
	#time_now = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
	filename = name
	#
	dstFile = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)),os.path.join(location,filename)))
	#
	with open(dstFile, 'w') as the_file:
		the_file.write(content)
		the_file.close()
	#
	#
#
def remove_class_replace(p_k_clean, class_groups):
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
def do_fea_kern_file_additions(final_class_kern_pairs):
	#
	do_fea_kern = 'feature kern {\n'
	#
	for k,y in final_class_kern_pairs.items():
		#
		print(k,y)
		#
		for x,z in y.items():
			#pass
			#
			k_int = z
			#
			let_a = k
			let_b = x
			#
			if '@MMK_L_' in let_a or '@MMK_R_' in let_a:
				#
				ltkd_a = get_kern_name_and_dir(let_a)
				#
				let_a = '@_'+ltkd_a[0]
				#
			if '@MMK_L_' in let_b or '@MMK_R_' in let_b:
				#
				ltkd_b = get_kern_name_and_dir(let_b)
				#
				let_b = '@_'+ltkd_b[0]+'1'
				#
				#
			#
			do_fea_kern = do_fea_kern + fea_pos_line.format(let_a, let_b, str(k_int)) + '\n'
		#
	#
	do_fea_kern = do_fea_kern + '} kern;'
	#
	return do_fea_kern
	#
#
def merge_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z
#
def do_adbuct(p_groups, p_kerning, dir_to_comp_ufo_file):
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
	old_pg = p_g.copy()
	#
	fea_file = do_fea_kern_file(final_class_kern_pairs)
	#
	fea_classes = make_fea_class_lines(p_g)
	fea_class_file = fea_prefix+'\n\n#automatic\n'+fea_classes+'<!ADDITIONS>'+'\n\n'+fea_file
	save_file(dir_to_comp_ufo_file, 'features'+'.fea', fea_class_file)
	#
	class_kerning_plist = make_kern_lines(final_class_kern_pairs)
	#
	#
	out_start = '''<plist version="1.0">
<dict>'''
	out_end = '''</dict>
</plist>'''
	#
	result_ck_dicts=class_kerning_plist[class_kerning_plist.find(out_start)+len(out_start):class_kerning_plist.find(out_end)]
	#print mySubString
	p_k_clean = remove_redundant_kern_values(all_affected_glyphs_permut,p_k)
	p_k_class_replace = remove_class_replace(p_k_clean, old_pg)
	#
	fea_file_additions = do_fea_kern_file_additions(p_k_class_replace)
	#
	altered_fea = os.path.join(dir_to_comp_ufo_file,'features'+'.fea')
	#
# 	with open(altered_fea, 'r') as the_fea:
# 		#
# 		the_fea_data = the_fea.read()
# 		#
# 		new_data = the_fea_data.replace('<!ADDITIONS>', fea_file_additions)
# 		#
# 		clip_features = new_data.replace('''} kern;

# feature kern {''', '')
# 		#
# 		save_file(dir_to_comp_ufo_file, 'features'+'.fea', clip_features)
# 		#
# 	#
	filename = 'kerning'+'.plist'
	dstFile = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)),os.path.join(dir_to_comp_ufo_file,filename)))
	plistlib.writePlist(p_k_class_replace, dstFile)
	#
	with open(dstFile, 'r') as the_file:
		content = the_file.read()
		result_fk_dicts=content[content.find(out_start)+len(out_start):content.find(out_end)]
		#
		res_kerning = plist_header+result_ck_dicts + result_fk_dicts+plist_footer
		#
		save_file(dir_to_comp_ufo_file, filename, res_kerning)
		#
	#
	temp_class_plist = os.path.join(dir_to_comp_ufo_file, filename)
	#
	c_k = plistlib.readPlist(temp_class_plist).items()
	#
	#
	print('Initial Flat Pairs:',len(all_affected_glyphs))
	print('Resulting Class Pairs and Remaining Flat',len(c_k))
	#
#
parser = ArgumentParser()
parser.add_argument("-g", "--group", dest="group",
                    help="Base group.plist", metavar="FILE")
parser.add_argument("-k", "--flatkern", dest="flatkern", 
                    help="Directory of flat kerned UFOs to extract pairs")
parser.add_argument("-c", "--compkern", dest="compkern", 
                    help="Directory of component kerned UFOs to replace kerning and grouping")
parser.add_argument("-w", "--weights", dest="weights", 
                    help="The weights comma separated, example filename: fontname_bld (we assume underscore)")
parser.add_argument("-f", "--fontfile", dest="fontfile", 
                    help="The font filename of the UFOs without the weights, example filename: fontname_bld (we assume underscore)")

#
args = parser.parse_args()
#
dir_path = os.path.dirname(os.path.realpath(__file__))
#
def do_class_kern_replacement(dir_flat, dir_to_comp, file_base_group, fontfilename, weights_str):
	#
	x = 0
	#
	_dir = dir_path+'/'
	#
	weight_list = weights_str.split(',')
	#
	for w in weight_list:	
		#
		dir_flat_ufo_file = dir_flat+'/'+fontfilename+'_'+w+'.ufo'
		dir_to_comp_ufo_file = dir_to_comp+'/'+fontfilename+'_'+w+'.ufo'
		#
		#
		dir_flat_ufo_file_kern=dir_flat_ufo_file+'/'+'kerning.plist'
		#
		copyfile(file_base_group, os.path.join(dir_to_comp_ufo_file,'groups.plist'))
		#
		print('Compressing: ',fontfilename+'_'+w)
		#
		do_adbuct(file_base_group, dir_flat_ufo_file_kern, dir_to_comp_ufo_file)
		#
faults = False
#
print('!!!THIS WILL OVERWRITE: features.fea, groups.plist, kerning.plist !!!')
#
if  args.group is None:
	#
	faults = True
	#
	print('=\n=> Please Provide Base Group File: -g "/base_groups.plist"\n=')	
	#
if  args.flatkern is None:
	#
	faults = True
	#
	print('=\n=> Please Provide Directory of flat kerned UFOs to extract pairs: -k "/flat_kern_ufo_dir"\n=')	
	#
else:
	#
	if os.path.isdir(args.flatkern) == False:
		#
		faults = True
		#
		print('=\n=> Please Provide Valid Directory of flat kerned UFOs to extract pairs: -k "/flat_kern_ufo_dir"\n=')	
		#
	#
if  args.compkern is None:
	#
	faults = True
	#
	print('=\n=> Please Provide Directory of component kerned UFOs to replace kerning and grouping: -c "/ufo_dir_to_comp_kern"\n=')	
	#
else:
	#
	if os.path.isdir(args.compkern) == False:
		#
		faults = True
		#
		print('=\n=> Please Provide Valid Directory of component kerned UFOs to replace kerning and grouping: -c "/ufo_dir_to_comp_kern"\n=')	
		#
	#

if args.fontfile is None:
	#
	faults = True
	#
	print('=\n=> Please Provide Font Family File Name: -f "fontfile"\n=')
	#
#
if args.weights is None:
	#
	faults = True
	#
	print('=\n=> Please Provide Comma Separated Font Weights String: -w "thn,reg,bld"\n=')
	#
#
if faults == False:
	#
	do_class_kern_replacement(args.flatkern, args.compkern, args.group, args.fontfile, args.weights)
	#
#

