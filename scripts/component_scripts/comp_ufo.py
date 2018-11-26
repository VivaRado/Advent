import os
import random
import sys
from sys import argv
import re
import plistlib
import glob
from lxml import html
from lxml import etree
from os.path import basename
import difflib
#
# tab completion 
#
import readline 
import rlcompleter 
import atexit
#
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
#
#
#
base_top_accent_tall_pos_y = 735
base_top_accent_tall_tonos_pos_y = 700
base_top_accent_short_pos_y = 545
comb_top_accent_pos_y = 600
comb_bottom_accent_pos_y = 0
tall_small_case = ['l','t']
#l_dots_list = ['Ldot','ldot']
#
comp_anchors_top = '''<contour>
      <point x="{1}" y="750" type="move" name="top"/>
    </contour>
    <contour>
      <point x="{1}" y="{0}" type="move" name="_top"/>
    </contour>'''
#
##
comp_anchors_top_tonos = '''<contour>
      <point x="{1}" y="750" type="move" name="tonos"/>
    </contour>
    <contour>
      <point x="{1}" y="{0}" type="move" name="_tonos"/>
    </contour>'''
#
# ##
# comp_anchors_center = '''<contour>
#       <point x="{1}" y="750" type="move" name="center"/>
#     </contour>
#     <contour>
#       <point x="{1}" y="{0}" type="move" name="_center"/>
#     </contour>'''
# #
#
comp_anchors_bot = '''<contour>
      <point x="{1}" y="-250" type="move" name="bottom"/>
    </contour>
    <contour>
      <point x="{1}" y="{0}" type="move" name="_bottom"/>
    </contour>'''
#
base_anchors = '''<contour>
      <point x="{2}" y="0" type="move" name="ogonek"/>
    </contour>
    <contour>
      <point x="{0}" y="0" type="move" name="bottom"/>
    </contour>
    <contour>
      <point x="{0}" y="{1}" type="move" name="top"/>
    </contour>
    <contour>
      <point x="{3}" y="{4}" type="move" name="tonos"/>
    </contour>
    <contour>
      <point x="{0}" y="300" type="move" name="center"/>
    </contour>'''
#
comb_top = ['acutecomb',
			'tonoscomb',
			'dieresistonoscomb',
			'brevecomb',
			'caroncomb',
			'circumflexcomb',
			'commaturnedabovecomb',
			'dieresiscomb',
			'dotaccentcomb',
			'gravecomb',
			'hungarumlautcomb',
			'macroncomb',
			'croat',
			'ringcomb',
			'tildecomb'];

comb_top_rebase = ['acute',
			'tonos',
			'dieresistonos',
			'breve',
			'caron',
			'circumflex',
			'quoteleft',
			'dieresis',
			'dotaccent',
			'grave',
			'hungarumlaut',
			'overscore',
			'overscore',
			'ring',
			'tilde'];

comb_bot = ['cedillacomb',
			'ogonekcomb',
			'commaturnedbelowcomb'
			# 'slashlongcomb',
			# 'slashshortcomb',
			# 'strokelongcomb',
			# 'strokeshortcomb'
			];
comb_bot_rebase = ['cedilla',
			'ogonek',
			'commaaccent'
			# 'slashlongcomb',
			# 'slashshortcomb',
			# 'strokelongcomb',
			# 'strokeshortcomb'
			];
#
def get_between(_start, _end, _str):
	#
	return _str[_str.find(_start)+len(_start):_str.find(_end)]
	#
#
def get_base_glif_width(_dir_glif, glif, exact_loc = False):
	#
	res_width = 0
	res_name = ''
	#
	if exact_loc == True:
		#
		with open(_dir_glif, 'r') as f:
			#
			glif_data = f.read()
			#
			out_start = 'name="'
			out_end = '" format'
			#
			res_name=get_between(out_start, out_end, glif_data)
			#
			try:
				#
				out_start = '<advance width="'
				out_end = '"/>'
				#
				res_width=int(get_between(out_start, out_end, glif_data))
				#
			except Exception:
				#
				res_width = 0
				#
				pass
					#
		#
	else:
		#
		for file in glob.glob(_dir_glif+"/*.glif"):
			#
			with open(file, 'r') as the_file:
				#
				glif_data = the_file.read()
				#
				out_start = 'name="'
				out_end = '" format'
				#
				res_name=get_between(out_start, out_end, glif_data)
				#
				if glif == res_name:
					#
					try:
						#
						out_start = '<advance width="'
						out_end = '"/>'
						#
						res_width=int(get_between(out_start, out_end, glif_data))
						#
						break
						#
					except Exception:
						#
						res_width = 0
						#
						pass
						#

			#
	return res_name,res_width
#
def get_base_glif_contours(_dir_glif, needed_glifs):
	#
	base_contours = {}
	#
	seen_glifs = []
	#
	res_width = 0
	#
	for file in glob.glob(_dir_glif+"/*.glif"):
		#
		with open(file, 'r') as the_file:
			#
			glif_data = the_file.read()
			#
			name = re.search('<glyph name="(.*)" format', glif_data).group(1)
			#
			if name not in seen_glifs:
				#
				if name in needed_glifs:
					#
					#
					try:
						#
						try:
							#
							#
							out_start = '<advance width="'
							out_end = '"/>'
							#
							res_width=int(get_between(out_start, out_end, glif_data))
							#
						except Exception:
							#
							res_width = 0
							#
							pass
							#
						#
						out_start = "<outline>"
						out_end = "</outline>"
						#
						result=get_between(out_start, out_end, glif_data)
						#
						base_contours[name] = [basename(file),result,res_width]
						#
					except Exception:
						#
						print('FAILED FOR GLIF: ', name)
						#
					#
					seen_glifs.append(name)
					#
				#
	return base_contours, res_width
#
non_exist = []
#
def rebase_accent(acc_orig, acc_dest, glif_loc, _acc_pos, g_info):
	#
	#
	print(acc_orig, acc_dest, glif_loc)
	#
	acc_orig_glif = os.path.join(glif_loc, acc_orig+'.glif')
	acc_dest_glif = os.path.join(glif_loc, acc_dest+'.glif')
	#
	exist_orig = os.path.isfile(acc_orig_glif)
	exist_orig_comp = False
	exist_dest = os.path.isfile(acc_dest_glif)
	exist_dest_comp = False
	#
	if exist_orig:
		#
		with open(acc_orig_glif, 'r') as o_f:
			#
			o_f_r = o_f.read()
			#
			comp_o = '<component base="'+acc_dest+'"/>'
			#
			if comp_o in o_f_r:
				#
				print(acc_orig,'INCLUDES: ',acc_dest)
				#
				exist_orig_comp = True
				#
			#
		#
	#
	else:
		#
		print('NON EXIST: ', acc_orig)
		#
		if acc_orig not in non_exist:
			#
			non_exist.append(acc_orig)
			#
		#
	#
	if exist_dest:
		#
		with open(acc_dest_glif, 'r') as d_f:
			#
			d_f_r = d_f.read()
			#
			comp_d = '<component base="'+acc_orig+'"/>'
			#
			if comp_d in d_f_r:
				#
				print(acc_dest,'INCLUDES: ',acc_orig)
				#
				exist_dest_comp = True
				#
			#
		#
	#
	else:
		#
		print('NON EXIST: ', acc_dest)
		#
	#
	if exist_orig and exist_dest:
		#
		if exist_dest_comp:
			#
			print('>>>>>', 'OK')
			#
		else:
			#
			print('>>>>>', 'NOK')
			print('>>>>>', 'combs should not include components, original accents should include combs')
			#
			print(acc_dest_glif)
			print(acc_orig_glif)
			#
			exchange_replace_contour(acc_orig, acc_dest, acc_dest_glif, acc_orig_glif, acc_orig, _acc_pos, g_info)
			#
		#
#
def exchange_replace_contour(acc_orig, acc_dest, acc_dest_glif, acc_orig_glif, comb_accent_name, _acc_pos, g_info):
	#
	accent_comp = '\n    <component base="{0}"/>\n  '.format(comb_accent_name)
	pos_anchors = ''
	eventual_pos_y = comb_top_accent_pos_y
	#
	is_accent_info = get_base_glif_width(acc_dest_glif, comb_accent_name, True)
	#
	if _acc_pos == 'top':
		#
		eventual_pos_x = 0
		#
		if 'tonos' in is_accent_info[0]:
			#
			pos_anchors = comp_anchors_top_tonos.format(int(eventual_pos_y), int(is_accent_info[1]/2))
			#
		# if is_accent_info[0] in l_dots_list:
		# 	#
		# 	pos_anchors = comp_anchors_top_tonos.format(int(300), int(is_accent_info[1]/2))
		# 	#
		else:
			#
			pos_anchors = comp_anchors_top.format(int(eventual_pos_y), int(is_accent_info[1]/2))
			#
		#
	else: 
		#
		eventual_pos_y = 0
		#
		pos_anchors = comp_anchors_bot.format(int(eventual_pos_y), int(is_accent_info[1]/2))
		#
	#
	replaced_a = replace_contour(accent_comp, acc_dest_glif, True) +'  '+ pos_anchors + '\n'
	#
	replace_contour(replaced_a, acc_orig_glif, False)
	#
	print('EXCANGED CONTENTS OF:', acc_orig, acc_dest)
	#
def replace_contour(_this, _here, _return_replaced):
	#
	out_start = "<outline>"
	out_end = "</outline>"
	#
	replacement = ''
	#
	with open(_here, 'r') as rf:
		#
		glif_data = rf.read()
		#
		result=get_between(out_start, out_end, glif_data)
		#
		replacement = result
		#
		with open(_here, 'w') as wf:
			#
			new_data = glif_data.replace(result, _this)
			#
			wf.write(new_data)
			#
			wf.close()
			#
	#
	if _return_replaced:
		#
		return result
		#
	#
#
def get_matching_contour(base_cont, rep_cont):
	#
	parser = etree.XMLParser(remove_blank_text=True)
	#
	base_cont_list = [ e for e in html.fromstring(base_cont).iter() if e.tag == 'contour']
	rep_cont_list = [ e for e in html.fromstring(rep_cont).iter() if e.tag == 'contour']
	#
	final_match = []
	seen_ = []
	#
	keep_index = []
	#
	for x in base_cont_list:
		#
		_e_base = etree.tostring(x, encoding='unicode', pretty_print=True)
		_e_base_test = ''.join([i for i in _e_base if not i.isdigit()])
		#
		for y in rep_cont_list:
			#
			_e_rep = etree.tostring(y, encoding='unicode', pretty_print=True)
			_e_rep_test =  ''.join([i for i in _e_rep if not i.isdigit()])
			#
			inner_diff_ratio = difflib.SequenceMatcher(a=_e_base_test,b=_e_rep_test).ratio()		
			#
			if _e_rep in seen_ :
				pass
			else:
				if inner_diff_ratio > 0.7:
					#
					keep_index.append(1)
					#
					final_match.append(_e_rep)
					#
				else:
					#
					keep_index.append(0)
					#
					final_match.append(_e_rep)
					#
				#
			seen_.append(_e_rep)
			#
	final_string = ''
	#
	c = 0
	#
	for x in keep_index:
		#
		if x == 0:
			#
			try:

				final_string = final_string + final_match[ c ]

			except Exception:
				pass
			#
		#
		c = c + 1
		#
	#
	return final_string
	#
#
def check_accents (name, combs, rebase_combs, _dir_glif, glif_width, _pos, g_info):
	#
	x = 0
	accent_name = ''
	accent_comp = ''
	#
	if 'uni' in name:
		#
		if name == 'uni021B' or name == 'uni021A':
			#
			if name == 'uni021B':
				#
				u_name = 'tcommaaccent'
				accent_name = 'commaturnedbelowcomb'
				#
			#
			if name == 'uni021A':
				#
				u_name = 'Tcommaaccent'
				accent_name = 'commaturnedbelowcomb'
				#
			#
		#
		if _pos == 'top':
			#
			_x = str(int(glif_width/2))
			_y = str(135)
			#
		else:
			#
			_x = str(glif_width-10)
			_y = str(-50)
			#
		#
		rebase_accent(accent_name, 'commaaccent', _dir_glif, _pos, g_info)
		#
		accent_comp = '<component base="{0}" xOffset="{1}" yOffset="{2}"/>'.format(accent_name, _x, _y)
		#
	elif 'commaaccent' in name:
		#
		#
		if name == 'gcommaaccent':
			#
			rebased = 'commaturnedabove'
			accent_name = 'commaturnedabovecomb'
			#
			#
		else:

			rebased = 'commaaccent'
			accent_name = 'commaturnedbelowcomb'
		#
		if _pos == 'top':
			#
			_x = str(int(glif_width/2))
			_y = str(135)
			#
		else:
			#
			_x = str(glif_width-10)
			_y = str(-50)
			#
		#
		rebase_accent(accent_name, rebased, _dir_glif, _pos, g_info)
		#
		accent_comp = '<component base="{0}" xOffset="{1}" yOffset="{2}"/>'.format(accent_name, _x, _y)
		#
		#
	else:
		#
		for c_t in combs:
			#
			if 'comb' in c_t:
				#
				accent = c_t.replace('comb', '')
				#
			#
			else:
				#
				accent = c_t
				#
			#
			if accent in name: 
				#
				rebased = rebase_combs[x]
				#
				accent_name = c_t
				#
				if 'croat' in c_t:
					#
					rebased = 'macroncomb'
					accent_name = 'macroncomb'
					#
				#
				print('CAN BE ACCENTED WITH: ',c_t)
				#
				rebase_accent(c_t, rebased, _dir_glif, _pos, g_info)
				#
				#
				if _pos == 'top':
					#
					_x = str(int(glif_width/2))
					_y = str(135)
					#
				else:
					#
					_x = str(glif_width-10)
					_y = str(-50)
					#
				accent_comp = '<component base="{0}" xOffset="{1}" yOffset="{2}"/>'.format(accent_name, _x, _y)
			#
			x = x + 1
		#
	#
	return accent_comp, accent_name
	#
#
def run_ufo_glyphs(comp_dir_path, ufo_dir_path):
	#
	_dir_glif = os.path.abspath(os.path.join(ufo_dir_path, 'glyphs'))
	#
	pl = plistlib.readPlist(comp_dir_path)
	#
	needed_glifs = list(pl)
	#
	#
	run_base = get_base_glif_contours(_dir_glif, needed_glifs)
	base_contours = run_base[0]
	#
	for o,p in pl.items():
		#
		glif_info = get_base_glif_width(_dir_glif, o)
		#
		to_replace = list(p)
		#
		to_replace.pop(0)
		#
		run_rep = get_base_glif_contours(_dir_glif, to_replace)
		get_contours_to_rep = run_rep[0]
		#
		g_width = glif_info[1]
		#
		base_conts = base_contours.get(o)
		#
		for u,t in get_contours_to_rep.items():
			#
			print('=======================')
			print('BASE: ',o)
			print('INFO: ',glif_info)
			print('COMP: ',u)
			print('_______________________')
			#
			u_name = u
			all_accents = []
			#
			glif_info_inner = get_base_glif_width(_dir_glif, u)
			#
			c_acc_b = check_accents(u_name, comb_bot, comb_bot_rebase, _dir_glif, t[2], 'bot', glif_info_inner)
			check_bot = c_acc_b[0]
			all_accents.append(c_acc_b[1])
			#
			c_acc_t = check_accents(u_name, comb_top, comb_top_rebase, _dir_glif, t[2], 'top', glif_info_inner)
			#
			if c_acc_t[1] in all_accents:
				#
				check_top = ''
				#
			else:
				#
				check_top = c_acc_t[0]
				#
			#
			#
			all_accents = check_top+'\n    '+check_bot
			#
			base_cont = base_conts[1]
			rep_cont = t[1]
			#
			diff_ratio = difflib.SequenceMatcher(a=base_cont,b=rep_cont).ratio()
			#
			if diff_ratio == 1:
				#
				match_cont = ''
				add_comp = '\n    <component base="{0}"/>'.format(o)
				#
			else:
				#
				match_cont = get_matching_contour(base_cont, rep_cont)
				#
				if len(check_top+check_bot) > 0:
					#
					match_cont = ''
					add_comp = '\n    <component base="{0}"/>\n    {1}'.format(o, all_accents)
					#
				else:
					#
					add_comp = '\n    <component base="{0}"/>'.format(o)
					#
				#
				glif_now_loc = os.path.join(_dir_glif,t[0])
				#
			#
			replacement_contour = add_comp+match_cont
			#
			target_glif = os.path.join(_dir_glif, t[0])
			base_glif = os.path.join(_dir_glif, base_conts[0])
			#
			replace_contour(replacement_contour, target_glif, False)
			#
			all_combs = comb_top + comb_top_rebase + comb_bot + comb_bot_rebase
			#
			if o not in all_combs and u not in all_combs:
				#
				if glif_info[0][0].isupper() and glif_info[0][0] not in tall_small_case:
					#
					pos_y = base_top_accent_tall_pos_y
					#
				else:
					#
					pos_y = base_top_accent_short_pos_y
					#
				#
				print('FIXING POS', pos_y, glif_info[0])
				#
				center_pos_x = int(g_width/2)
				ogonek_pos_x = int(g_width/3) + int(g_width/6) 
				#
				#
				if glif_info[0][0].isupper() == False and glif_info[0][0] not in tall_small_case:
					#
					pos_tonos_y = pos_y
					pos_tonos_x = center_pos_x
					#
				else:
					#
					pos_tonos_y = base_top_accent_tall_tonos_pos_y
					pos_tonos_x = int(g_width/6) 
					pos_y = base_top_accent_tall_pos_y
					#
				#
				base_anchors_calc = base_anchors.format(center_pos_x, pos_y, ogonek_pos_x, pos_tonos_x, pos_tonos_y)
				#
				replace_contour(base_cont+base_anchors_calc, base_glif, False)
				#
			#
		#
	#
#
#
ufo_src_path = input("Directory of UFO file: ")
#
comp_class_file = input("components class group plist file: ")
#
run_ufo_glyphs(comp_class_file, ufo_src_path)
#
print('NOT EXISTING GLYPHS')
print(non_exist)