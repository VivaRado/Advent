import collections
from collections import Iterable
#
from fontParts.world import *
from TFSFont import *
from TFSSvg import *
#
from PIL import Image
import cairosvg
#
from math import sqrt, ceil, floor
#
import difflib
#
from .simex_slicer import *
from .simex_render import *
#
#
flush_space = '                                                             '
#
def get_glyphs(srcUfoFont, check_list, checking):
	#
	glyph_nums = collections.OrderedDict()
	#
	all_glyphs = srcUfoFont.getGlyphs()
	all_glyph_len = len(all_glyphs)
	#
	x = 0
	#
	for ufoglyph in all_glyphs:
		#
		if all_glyph_len > x:
			#
			print('\r\t'+'RENDERING ('+str(x)+'/'+str(all_glyph_len)+'): '+ ufoglyph.name +flush_space, end='')
			#
			#
			x = x + 1
			#
		#
		if all_glyph_len == x:
			#
			print('\r\t'+'DONE RENDERING: '+str(all_glyph_len)+' Glyphs'+flush_space, end='')
			#
			print('\n')
		#
		contours = getGlyphContours(ufoglyph)
		#
		if len(contours) < 1:
			continue
		#
		if check_list:
		
			if ufoglyph.name in checking:
				#
				glyph_nums[ufoglyph.name] = render_glyph(contours, ufoglyph)
				#
		else:
			#
			glyph_nums[ufoglyph.name] = render_glyph(contours, ufoglyph)
			#
		
	#
	return glyph_nums
	#
#
#
def getGlyphContours(ufoglyph):
	#def getCachedContours():
	contours = ufoglyph.getContours(warnings=False)
	return contours
	#return getCachedValue('getCachedContours %s' % ufoglyph.name, getCachedContours)
#
def flatten(items):
	"""Yield items from any nested iterable; see Reference."""
	for x in items:
		if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
			for sub_x in flatten(x):
				yield sub_x
		else:
			yield x
#
def split(arr, size):
	arrs = []
	while len(arr) > size:
		pice = arr[:size]
		arrs.append(pice)
		arr   = arr[size:]
	arrs.append(arr)
	return arrs
#
def dedup_pairs(s):
	#
	paired = split(s, 2)
	#
	#
	x = list(paired for paired,_ in itertools.groupby(paired))
	#
	flat_list = list(flatten(x))
	#
	return flat_list
#
#
def unique_groups(mils):
	#
	seen_values = []
	#
	unique_mils = collections.OrderedDict()
	#
	for key, vals in mils.items():
		#
		for x, v in vals.items():
			#
			if x not in seen_values:
				#
				if len(vals) > 1:
					#			
					unique_mils[key] = vals
					#
				#
				seen_values.append(x)
				#
			#
	#
	return unique_mils
	#

#
def keep_probable(mils, max_diff):
	#
	prob_mils = collections.OrderedDict()
	#
	for key, vals in mils.items():
		#
		direction = vals[1]
		#
		if direction == 'center':
			#
			dir_diff = max_diff[1]
			#
		elif direction == 'circle':
			#
			dir_diff = max_diff[1]
			#
		elif direction == 'left':
			#
			dir_diff = max_diff[0]
			#
		elif direction == 'right':
			#
			dir_diff = max_diff[2]
			#
		else:
			#
			dir_diff = max_diff[1]
			#
		if vals[0] >= dir_diff:
			#
			#if len(vals[1]):
				#
			prob_mils[key] = vals
				#
			#
		#
	#
	return prob_mils

#
def get_flat_numbers (contour):
	#
	contour_str = str(contour)
	#
	nums = re.findall(r"[-+]?\d*\.\d+|\d+", contour_str)
	#
	new_nums = []
	#
	for num in nums:
		#
		num = int(float(num))
		#
		new_nums.append(num)
		#
	#
	return new_nums
	#
#
def get_range_x(_list):
	#
	just_x = [item[0] for item in _list]
	#
	max_value = max(just_x)
	min_value = min(just_x)
	avg_value = sum(just_x)/len(just_x)
	#
	return[min_value, avg_value, max_value]
	#
#
def split_half(_l, _o):
	
	if _o == "h":
		half = int(len(_l)/2)
		return _l[:half], _l[half:]
	elif _o == "v":
		return _l[::2], _l[1::2]

def split_letter_mtx (letter_mtx):
	#
	_H = split_half(letter_mtx, 'h')
	_V = split_half(letter_mtx, 'v')
	#
	_T = _H[0]
	_B = _H[1]
	#
	_L = _V[0]
	_R = _V[1]
	#
	return [_T,_B],[_L,_R]
	#
def sum_list (_l):
	#
	return round(sum(_l[0:len(_l)]),4)
	#
def optical_weight(contrast_mtx, name):
	#
	_Tl = contrast_mtx[0][0]
	_Bl = contrast_mtx[0][1]
	#
	_T = sum_list(_Tl)
	_B = sum_list(_Bl)
	#
	_Ll = contrast_mtx[1][0]
	_Rl = contrast_mtx[1][1]
	#
	_L = sum_list(_Ll)
	_R = sum_list(_Rl)
	#
	diff_LR = round(difflib.SequenceMatcher(None, str(_Ll), str(_Rl)).ratio(), 5)
	diff_TB = round(difflib.SequenceMatcher(None, str(_Ll), str(_Rl)).ratio(), 5)
	#
	subt_LR = round(abs(round(_R,2) - round(_L,2)),4)
	subt_TB = round(abs(round(_T,2) - round(_B,2)),4)
	#
	is_dir = ""
	#
	# print(subt_LR)
	# print(subt_TB)
	#
	if ( (diff_LR > 0.4 ) ):
		#
		#
		if (subt_LR < 0.05):
			#
			is_dir = "center"
			#
		else:
			#
			if ( round(_R,1) < round(_L,1) ):
				#
				is_dir = "left"
				#
			elif ( round(_R,1) > round(_L,1) ):
				#
				is_dir = "right"
				#
			else:
				#
				is_dir = "circle"
				#
		#
	else:
		#
	
		if ( round(_R,1) < round(_L,1) ):
			#
			is_dir = "left"
			#
		elif ( round(_R,1) > round(_L,1) ):
			#
			is_dir = "right"
			#
	#
	if len(is_dir) == 0:
		#
		is_dir = 'uncategorized'
		#
	#
	return is_dir
	#
