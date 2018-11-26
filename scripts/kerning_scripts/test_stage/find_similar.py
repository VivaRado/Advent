import os
# import io
import random
from math import sqrt, ceil, floor
import datetime
import collections
# import itertools
# import threading
# import time
import sys
from sys import argv
import re
import json
# import getpass
# import shutil
#from datetime import datetime
# from time import gmtime, strftime
#
#from svg2data import svg2data
from lxml import etree
from xml.dom import minidom
from svg.path import parse_path
import itertools
#
from PIL import Image
import cairosvg
#
import cairo
#import rsvg

# python startup file 
import readline 
import rlcompleter 
import atexit
#
from collections import Iterable
#
import difflib
import numpy as np
from numpy import allclose
#
this_path = os.path.dirname(os.path.realpath(__file__))
scripts_path = os.path.abspath(os.path.join(this_path, os.pardir))
#
tfs_path = os.path.join(scripts_path,'test_stage/tfsp/common')
#
sys.path.append(tfs_path)
#
from fontParts.world import *
from TFSFont import *
from TFSSvg import *
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

#
# left, center, right
# max_diff = [0.8, 0.8, 0.8] loose for kern groups
max_diff = [1, 1, 1] # tight for components
checking = ['A', 'Alphatonos', 'Abreve', 'Deltagreek', 'Omicron', 'Theta', 'O', 'E', 'F', 'P', 'R', 'L', 'Lacute', 'J', 'Eng', 'V', 'W']
#checking = ['A', 'Alphatonos', 'Abreve', 'Deltagreek', 'Omicron', 'Theta', 'O']
check_list = False
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
	#print('>>>>>>')
	#print(paired)
	#print(x)
	#
	flat_list = list(flatten(x))
	#
	return flat_list
#
seen_values = []
#
def unique_groups(mils):
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
def keep_probable(mils):
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
def getGlyphContours(ufoglyph):
	#def getCachedContours():
	contours = ufoglyph.getContours(warnings=False)
	return contours
	#return getCachedValue('getCachedContours %s' % ufoglyph.name, getCachedContours)
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
def get_black_level(img):
	pixels = img.getdata()
	black_thresh = 50
	nblack = 0
	for pixel in pixels:
		if sum(pixel) < black_thresh:
			nblack += 1
	n = len(pixels)

	return nblack / float(n)
#
class Tile(object):

	def __init__(self, image, number, position, coords, filename=None):
		self.image = image
		self.number = number
		self.position = position
		self.coords = coords
		#self.filename = filename

	@property
	def row(self):
		return self.position[0]

	@property
	def column(self):
		return self.position[1]
	
	def save(self, filename=None, format='png'):
		
		self.image.save(filename, format)
		self.filename = filename

def calc_columns_rows(n):

	num_rows = int(floor(sqrt(n)))
	num_columns = int(floor(n / float(num_rows)))
	return (num_rows, num_columns)

def matrix_slice(image_path, outdir, out_name):
	#
	im = Image.open(image_path)
	#
	slices = 16
	#
	im_w, im_h = im.size
	columns, rows = calc_columns_rows(slices)
	extras = (columns * rows) - slices
	tile_w, tile_h = int(floor(im_w / columns)), int(floor(im_h / rows))
	#
	tiles = []
	number = 1
	#
	for pos_y in range(0, im_h - rows, tile_h): # -rows for rounding error.
		#
		for pos_x in range(0, im_w - columns, tile_w): # as above.
			#
			area = (pos_x, pos_y, pos_x + tile_w, pos_y + tile_h)
			image = im.crop(area)
			#
			position = (int(floor(pos_x / tile_w)) + 1,
						int(floor(pos_y / tile_h)) + 1)
			#
			coords = (pos_x, pos_y)
			tile = Tile(image, number, position, coords)
			tiles.append(tile)
			number += 1
			#
		#
	#
	count = 0
	color_matrix = []
	#
	for x in tiles:
		#
		img_dir = os.path.join(outdir, "slice_"+ out_name +'_'+ str(count) +".png")
		x.save(img_dir)
		#
		contrast_lvl = round(get_black_level(x.image),4)
		color_matrix.append(contrast_lvl)

		os.remove(img_dir)
		
		#
		count = count + 1 
		#
	#
	#
	
	return color_matrix

def render_glyph(contours, ufoglyph):
	
	LETTER_COLOR = 0x90000000
	CANVAS_BACKGROUND_COLOR = 0xffffffff

	def subrenderGlyphContours( tfsSvg, contours):
		#
		paths_in = []
		paths_out = []
		#
		x = 0
		for contour in contours:
			#
			if isClosedPathClockwise(contour):
				paths_in.append(contour)
			else:
				paths_out.append(contour)

		#
		#for path_out in paths_out:
		svgPath_out = TFSSvgPath(contours[0])
		svgPath_out.fillColor = LETTER_COLOR
		tfsSvg.addItem(svgPath_out)
		# for path_out in paths_out:
		# 	svgPath_out = TFSSvgPath(path_out)
		# 	svgPath_out.fillColor = LETTER_COLOR
		# 	tfsSvg.addItem(svgPath_out)
		#
		for path_in in paths_in:
			
			svgPath_in = TFSSvgPath(path_in)
			svgPath_in.fillColor = CANVAS_BACKGROUND_COLOR
			tfsSvg.addItem(svgPath_in)
	
	tfsSvg = TFSSvg().withBackground(CANVAS_BACKGROUND_COLOR)#.withBorder(CANVAS_BORDER_COLOR)

	subrenderGlyphContours(tfsSvg, contours)

	#
	filename = '%s.svg' % ( ufoglyph.name, )
	filename_png = '%s.png' % ( ufoglyph.name, )
	dstFile = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)),os.path.join('svg_loc', filename)))
	dstlocpng = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)),'svg_loc'))
	dstFilepng = os.path.abspath(os.path.join(dstlocpng, filename_png ))

	svgdata = tfsSvg.renderToFile(None,
								  margin=10,
								  timing=None,
								  #width=width, height=height, 
								  maxWidth = 700,
								  maxHeight = 250,
								  #maxWidth=maxWidth, maxHeight=maxHeight,
								  padding=None)
	
	#svgdata = svgdata.replace('fill="none"', 'fill="black"')
	svgdata = svgdata.replace('fill-opacity="0.565"', 'fill-opacity="1"')
	#svgdata = svgdata.replace('fill="rgb(0,0,0)" ', 'fill="rgb(255,255,255)" ')
	#print(svgdata)
	#
	with open(dstFile, 'w') as the_file:
		the_file.write(svgdata)
		the_file.close()
		#
	tempobject = svgwrite.Drawing(svgdata, profile='tiny', width=700, height=250)
	#
	#print(tempobject)
	#
	cairosvg.svg2png(url=dstFile, write_to=dstFilepng)
	#
	raster_data = matrix_slice(dstFilepng, dstlocpng, ufoglyph.name)
	#
	os.remove(dstFile)
	os.remove(dstFilepng)
	#
	return raster_data
	#
#
def get_glyphs(srcUfoFont):
	#
	glyph_nums = collections.OrderedDict()
	#
	for ufoglyph in srcUfoFont.getGlyphs():
		#
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
	print('====')
	print('====')
	print(subt_LR)
	print(subt_TB)
	#
	if ( (diff_LR > 0.4 ) ):
		#
		#
		if (subt_LR < 0.05):
			#
			# if ((_T + _B + _L + _R) / 4) > 1 :
			# 	#
			print('+++++')
			# 	print((_T + _B) / 2)
			# 	print((_T + _B + _L + _R) / 4)
			# 	#
			# 	if (_T + _B) / 2 >= 2.2:
					#
			is_dir = "center"
					#
				#else:
					#
				#	is_dir = "center"
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
def ratio_to_rgb(_color_mtx):
	#
	image = []
	#
	for c in _color_mtx:
		#
		perc = (c / 1) * 100
		#
		per_rgb = abs(int((255 / 100) * perc) - 255)
		#
		pixel = [per_rgb,per_rgb,per_rgb]
		#
		image.append(pixel)
		#
	#
	return image
	#
def create_ratio_img(rgb_array, _name):
	#
	paired = split(rgb_array, 2)
	#
	list_of_pixels = np.asarray(paired)
	#
	im2 = Image.fromarray(list_of_pixels.astype('uint8'))
	#
	filename_png = '%s.png' % ( 'grad_'+_name )
	dstlocpng = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)),'svg_loc'))
	dstFilepng = os.path.abspath(os.path.join(dstlocpng, filename_png ))
	#
	im2 = im2.resize((100, 100), Image.ANTIALIAS)
	#
	im2.save(dstFilepng)
	#
def do_compare_mtx_colors(s1, s2, key, cey, direction):
	#
	_s1 = split_letter_mtx (s1)
	_s2 = split_letter_mtx (s2)
	#
	#rgb_array = ratio_to_rgb(s1)
	#create_ratio_img(rgb_array, key)
	#
	_s1T = _s1[0][0]
	_s1B = _s1[0][1]
	#
	_s1L = _s1[1][0]
	_s1R = _s1[1][1]
	#
	#
	_s2T = _s2[0][0]
	_s2B = _s2[0][1]
	#
	_s2L = _s2[1][0]
	_s2R = _s2[1][1]
	#
	o_w_1 = optical_weight(_s1,key)
	o_w_2 = optical_weight(_s2,cey)
	#
	diff_T = round(difflib.SequenceMatcher(None, str(_s1T), str(_s2T) ).ratio(),4)
	diff_B = round(difflib.SequenceMatcher(None, str(_s1B), str(_s2B) ).ratio(),4)
	diff_L = round(difflib.SequenceMatcher(None, str(_s1L), str(_s2L) ).ratio(),4)
	diff_R = round(difflib.SequenceMatcher(None, str(_s1R), str(_s2R) ).ratio(),4)
	#
	overall_diff = round(difflib.SequenceMatcher(None, str(s1), str(s2) ).ratio(),4)
	#
	print(key,'TB',_s1T, _s1B, 'LR',_s1L, _s1R, 'DIFF: '+key+'|'+cey,diff_T,diff_B,diff_L,diff_R,'ODIFF', overall_diff)
	#
	print('____________________________________________________________')
	#
	if o_w_1 != o_w_2:
		msg = "ignore"
	else:
		msg = True
	#
	#
	
	#
	return [overall_diff, msg, o_w_1]
	#
#
def init_permut(glyph_nums, direction):
	#
	seen_mililar = []
	seen_keys = []
	seen_vals = []
	seen_vals_extend = []
	#
	all_mils = collections.OrderedDict()
	#
	for key, vals in glyph_nums.items():
		#
		y = 0
		#
		#
		t_mils = collections.OrderedDict()
		#
		for in_key, in_vals in glyph_nums.items():
			#
			iny = 0
			#
			#res = do_compare_anchors(vals, in_vals, key, in_key, direction)
			res = do_compare_mtx_colors(vals, in_vals, key, in_key, direction)
			#
			if res[1] != 'ignore':# or res[1] != 'ignore':
				#
				#if key == in_key:
					#
				

				t_mils[in_key] = [res[0], res[2]] #+ res_b[0]
					#

				# print('=====')
				# print(t_mils)
				print('____________')
				print(len(t_mils[in_key]))
				#else:
					#
				#	t_mils[in_key]
					#
				#
				#t_mils[in_key] = [res[0], res[2]] #+ res_b[0]
			#	
			#print(t_mils)
			#
			seen_vals.append(vals)
			#

			#
		#	
			
		#
		y = y + 1
		#
		seen_keys.append(key)
		#
		if len(t_mils) > 1:
			#
			prob_mils = keep_probable(t_mils)
			all_mils[key] = prob_mils
			#
		#
		#
	#
	mil_dict = collections.OrderedDict()
	#
	t_z = 0
	#
	for z in seen_keys:
		#
		mil_dict[z] = seen_vals[t_z]
		#
		t_z = t_z + 1
		#
	#
	return mil_dict, all_mils
#

ufo_src_path = input("Directory of UFO file: ")
#
srcUfoFont = TFSFontFromFile(ufo_src_path)
#
glyph_nums = get_glyphs(srcUfoFont)
#

in_mils = init_permut(glyph_nums, 'right')
# #
mil_dict = in_mils[0]
all_mils = in_mils[1]
#
uni_groups = unique_groups(all_mils)
#
r = json.dumps(uni_groups)
parsed = json.loads(r)
parse_dumped = json.dumps(parsed, indent=4, sort_keys=False)
print (parse_dumped)
#
time_now = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
filename = time_now+'_kern_class'+'.json'
#
dstFile = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)),os.path.join('class_loc', filename)))
#
with open(dstFile, 'w') as the_file:
	the_file.write(parse_dumped)
	the_file.close()
#