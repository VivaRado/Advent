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
import difflib
import plistlib
import json
#
import collections
from collections import Counter
#
from pathlib import Path
#
#
#
#
#
#
'''
___________________________________

FL
___________________________________

opentype
--

languagesystem DFLT dflt;

@_A=[A  Aacute Alpha Deltagreek];
@_C=[C  Cacute];
@_O=[O  Omicron Q Theta];

feature kern {
   pos @_A @_C -30;
   pos @_A @_O -10;
   pos @_C @_O -40;
   pos @_O @_A -20;
} kern;


classes
-- 

_A: A' Aacute Alpha Deltagreek
_B: O' Omicron Q Theta
_C: C' Cacute


___________________________________

UFO
___________________________________

features.fea
--

languagesystem DFLT dflt;

@_A=[A  Aacute Alpha Deltagreek];
@_C=[C  Cacute];
@_O=[O  Omicron Q Theta];

feature kern {
   pos @_A @_C -30;
   pos @_A @_O -10;
   pos @_C @_O -40;
   pos @_O @_A -20;
} kern;


kerning.plist
--

<dict>
  <key>@MMK_L_O</key>
  <dict>
    <key>@MMK_R_A</key>
    <integer>-20</integer>
  </dict>
  <key>@MMK_L_C</key>
  <dict>
    <key>@MMK_R_O</key>
    <integer>-40</integer>
  </dict>
  <key>@MMK_L_A</key>
  <dict>
    <key>@MMK_R_O</key>
    <integer>-10</integer>
    <key>@MMK_R_C</key>
    <integer>-30</integer>
  </dict>
</dict>


groups.plist
--

<dict>
  <key>@MMK_L_A</key>
  <array>
    <string>A</string>
    <string>Aacute</string>
    <string>Alpha</string>
    <string>Deltagreek</string>
  </array>
  <key>@MMK_L_C</key>
  <array>
    <string>C</string>
    <string>Cacute</string>
  </array>
  <key>@MMK_L_O</key>
  <array>
    <string>O</string>
    <string>Omicron</string>
    <string>Q</string>
    <string>Theta</string>
  </array>

  <key>@MMK_R_A</key>
  <array>
    <string>A</string>
    <string>Aacute</string>
    <string>Alpha</string>
    <string>Deltagreek</string>
  </array>
  <key>@MMK_R_C</key>
  <array>
    <string>C</string>
    <string>Cacute</string>
  </array>
  <key>@MMK_R_O</key>
  <array>
    <string>O</string>
    <string>Omicron</string>
    <string>Q</string>
    <string>Theta</string>
  </array>
</dict>

'''
#
#
plist_header = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>'''
#
plist_footer = '''\n</dict>\n</plist>'''
#
plist_string = '''    <string>{0}</string>'''
#
plist_group = '''  <key>@MMK_{2}_{0}</key>
  <array>
{1}  </array>'''
	#
#
def do_kern_groups(gs):
	#
	plist_g_str = ""
	#
	for k,v in gs:
		#
		if k == "U":
			#
			k = "L"
			#
		#
		for xk, xv in v.items():
			#
			plist_strs = ''
			#
			for lk in xv:
				#
				plist_str = plist_string.format( lk )
				#
				plist_strs = plist_strs + plist_str + '\n'
				#
			#
			plist_g_str = plist_g_str +'\n'+plist_group.format( xk, plist_strs, k )
			#
		#
	#
	return plist_g_str
	#
#
def build_group_plist(kern_class_groups):
	#
	for x in kern_class_groups:
		#
		#print(x)
		#print('_______________________')
		#
		for k,v in x.items():
			#
			plist_strings = ''
			#
			gs = v[0]["groups"]
			#
			for j in gs:
				#
				plist_g_str = do_kern_groups( j.items() )
				#
				plist_strings = plist_strings + plist_g_str
				#
			#
			return plist_strings
			#
		#
#

#
def do_kern_groups_plist_line_test(gs):
	#
	#
	plist_strs = ""
	#
	plist_g_str = ""
	#
	gsl = list(gs)
	gsl.sort()
	#
	letter = gsl[0]
	#
	gsl.remove(letter)
	gsl.insert(0, letter)
	#
	_dir = ''
	#
	got_dir = gs.get(letter)[1]
	#
	#print(got_dir)
	#
	if got_dir == "left":
		#
		_dir = "L"
		#
	elif got_dir == "right":
		#
		_dir = "R"
		#
	elif got_dir == "center":
		#
		_dir = "C"
		#
	elif got_dir == "circle":
		#
		_dir = 'C'
		#
	#
	for k in gsl:
		#
		#print('____')
		#print(k)
		#
		plist_str = plist_string.format( k )
		#
		plist_strs = plist_strs + plist_str+'\n'
		#
	#
	if _dir == "C":
		#
		plist_g_str = plist_g_str +'\n'+plist_group.format( letter, plist_strs, 'L' )
		plist_g_str = plist_g_str +'\n'+plist_group.format( letter, plist_strs, 'R' )
		#
	else:
		#
		plist_g_str = plist_g_str +'\n'+plist_group.format( letter, plist_strs, 'L' )
		plist_g_str = plist_g_str +'\n'+plist_group.format( letter, plist_strs, 'R' )
		#
	#
	return plist_g_str
	#
#

def build_kerning_group_plist(kern_class_groups, EFO_groups_dir):
	#
	with open(kern_class_groups) as f:
		#
		cg_group = json.load(f)
		#
		plist_strings = ''
		#
		for x in cg_group:
			#
			plist_g_str = do_kern_groups_plist_line_test( cg_group[x] )
			#
			plist_strings = plist_strings + plist_g_str
			#
			#
		#return plist_strings
			#
		cg_group = plist_header+plist_strings+plist_footer
		#
		simex_json_file_name = Path(kern_class_groups).name.split('.json')[0]
		filename = 'kerning.plist'
		#
		#dstFile = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)),os.path.join('temp_simex', filename)))
		dstFile = os.path.join(EFO_groups_dir,filename)
		#
		print('\tUPDATING EFO Groups Directory with Extracted Similarity Kerning Plist', dstFile)
		#
		with open(dstFile, 'w') as the_file:
			the_file.write(cg_group)
			the_file.close()
		
	#
#
# def build_plists(kern_class_groups):
# 	#
# 	with open(kern_class_groups) as f:
# 		#
# 		data = json.load(f)
# 		g_plist = plist_header+build_group_plist(data)+plist_footer
# 		#
# 		time_now = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
# 		filename = time_now+'_groups'+'.plist'
# 		#
# 		dstFile = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)),os.path.join('temp_simex', filename)))
# 		#
# 		with open(dstFile, 'w') as the_file:
# 			the_file.write(g_plist)
# 			the_file.close()
		
#
def common(lst):
	#
	c = Counter(lst)
	#
	counts = []
	#
	ct = Counter(lst)
	#
	for t,s in ct.items():
		#
		if s > 1:
			counts.append(t)
		#
	#
	return counts
	#
#
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))
#
def deal_l (g_l, c_s_l, k, g_u, seen_all, seen_k_l):
	#
	for z in c_s_l:
		#
		do_add_l = []
		#
		for seen_l in k[1]:
			#
			lx = list(seen_l)
			#
			if z == lx[0]:
				#
				do_add_l.append(lx[1])
				#
				seen_k_l.append(lx[0])
				seen_k_l.append(lx[1])
				#
				seen_all.append(lx[0])
				seen_all.append(lx[1])
				#
			#
		g_l[z] = do_add_l#.sort()

	return g_l, g_u, seen_all, seen_k_l
	#
##
def deal_r (g_r, c_s_r, k, g_u, seen_all, seen_k_l):
	#
	for j in c_s_r:
		#
		do_add_r = []
		#
		for seen_r in k[1]:
			#
			lx = list(seen_r)
			#
			if j == lx[1]:
				#
				if lx[0] not in seen_k_l:
					#
					do_add_r.append(lx[0])
					#
					seen_all.append(lx[1])
					seen_all.append(lx[0])
					#
			#
		if len(do_add_r) > 0:
			
			g_r[j] = do_add_r#.sort()
		
		#
	return g_r, g_u, seen_all
	#
#
def direction_group_by_int(dir_path):
	#
	pl = plistlib.readPlist(dir_path)
	#
	kern_numbers = {}
	#
	for x,v in pl.items():
		#
		for z,y in v.items():
			#
			if y not in kern_numbers:
				#
				y = floor(y)
				#
				kern_numbers[y] = []
				#
				kern_numbers[y].append([x,z])
				#
			else:
				#
				kern_numbers[y].append([x,z])
				#
			#
		#
	#
	#print('__')
	#
	total_before = 0
	total_after = 0
	#
	i = 0
	#
	all_dir_groups = []
	#
	for k in kern_numbers.items():
		#
		lenk = len(k[1])
		#
		g_l = {}
		g_r = {}
		g_u = {}
		#
		seen_all = []
		seen_k_r = []
		seen_k_l = []
		#
		#
		if lenk > 1:
			#
			seen_right = []
			seen_left = []
			#
			# print(k[0])
			# print('-')
			# print(k[1])
			# print('-')
			#
			for x in k[1]:
				#
				lx = list(x)
				#
				if len(lx) > 1:
					#
					seen_left.append(lx[0])
					seen_right.append(lx[1])
					#
				#
			#
			c_s_l = common(seen_left)
			c_s_r = common(seen_right)
			#
			# print('L=',c_s_l)
			# print('R=',c_s_r)
			#
			if (len(c_s_l) != 0):
				#
				d_d_l = deal_l(g_l, c_s_l, k, g_u, seen_all, seen_k_l)
				g_l = d_d_l[0]#.sort()
				#
				seen_all = d_d_l[2]
				seen_k_l = d_d_l[3]

			if( len(c_s_r) != 0):
				#
				d_d_r = deal_r(g_r, c_s_r, k, g_u, seen_all, seen_k_l)
				g_r = d_d_r[0]#.sort()
				#
				seen_all = d_d_r[2]
				#
			for x in k[1]:
				#
				lx = list(x)
				#
				if lx[0] not in seen_all:
					#
					g_u[lx[0]] = [lx[1]]
				#
			# #
			#g_u = g_u.sort()
			# print('-L-')
			# print(g_l)
			# print('-R-')
			# print(g_r)
			# print('-U-')
			# print(g_u)
			# print('-')
			# #
			# print( len(k[1]) )
			# print( len(g_l) + len(g_r) + len(g_u) )
			#
			#print('============')
			#
			total_before = total_before + len(k[1])
			total_after = total_after + len(g_l) + len(g_r) + len(g_u)
		#
		sum_total = len(g_l)+len(g_r)+len(g_u)
		#
		if sum_total > 0:
			#
			info_block = {
							"name":id_generator(6), 
							"kern_int": k[0], 
							"L_R_U": [len(g_l), len(g_r), len(g_u)], 
							"group_sum":sum_total, 
							"groups": []
						  }
			#
			direction_group = {i:[]}
			direction_group[i].append(info_block)
			#
			grouplist = direction_group[i][0]["groups"]
			#
			grouplist.append({"L":g_l})
			grouplist.append({"R":g_r})
			grouplist.append({"U":g_u})
			#
			all_dir_groups.append(direction_group)
			#
		#
		i = i + 1
	#
	print('END:')
	#
	print(total_before,"/",total_after)
	#
	#
	return all_dir_groups
	#
#
# kernplist_src_path = ''
# #kernplist_src_path = input("kern plist base file: ")
# kerngroupsjson_src_path = ''
# #kerngroupsjson_src_path = input("kern class groups json file: ")
# classlocjson_src_path = ''
# classlocjson_src_path = input("class loc json file: ")
# #
# def do_plist_compress(kernplist_src_path):
# 	#
# 	kern_class_data = direction_group_by_int(kernplist_src_path)
# 	#
# 	r = json.dumps(kern_class_data)
# 	parsed = json.loads(r)
# 	parse_dumped = json.dumps(parsed, indent=4, sort_keys=False)
# 	#
# 	time_now = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
# 	filename = time_now+'_kern_class_groups'+'.json'
# 	#
# 	dstFile = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)),os.path.join('kern_class_group_loc', filename)))
# 	#
# 	with open(dstFile, 'w') as the_file:
# 		the_file.write(parse_dumped)
# 		the_file.close()
# 	#
# #
# if len(kernplist_src_path) > 0:
# 	do_plist_compress(kernplist_src_path)
# #
# if len(kerngroupsjson_src_path) > 0:
# 	build_plists(kerngroupsjson_src_path)
# #
# if len(classlocjson_src_path) > 0:
# 	build_group_plist_data_test(classlocjson_src_path)
# #