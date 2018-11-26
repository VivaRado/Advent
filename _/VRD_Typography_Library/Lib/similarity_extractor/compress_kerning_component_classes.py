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
#
#
#
#
#
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
plist_header = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>'''
#
plist_footer = '''\n</dict>\n</plist>'''
#
plist_string = '''    <string>{0}</string>'''
#
plist_group = '''  <key>{0}</key>
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
			plist_g_str = plist_g_str +'\n'+plist_group.format( xk, plist_strs)
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
		print('_______________________')
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
	for k in gsl:
		#
		print('____')
		print(k)
		#
		plist_str = plist_string.format( k )
		#
		plist_strs = plist_strs + plist_str+'\n'
		#
	#
	plist_g_str = plist_g_str +'\n'+plist_group.format( letter, plist_strs)
	#
	return plist_g_str
	#
#

def build_group_plist_data_test(kern_class_groups):
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
		time_now = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
		filename = time_now+'_component_groups'+'.plist'
		#
		dstFile = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)),os.path.join('component_class_group_loc', filename)))
		#
		with open(dstFile, 'w') as the_file:
			the_file.write(cg_group)
			the_file.close()
		
	#
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
classlocjson_src_path = input("component class loc json file: ")
#
if len(classlocjson_src_path) > 0:
	build_group_plist_data_test(classlocjson_src_path)
#