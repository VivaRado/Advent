import collections
from collections import Iterable
#
from .simex_tools import *
#
#
flush_space = '                            '
'''
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
'''
#
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
	# 'TB'+str(_s1T)+ str(_s1B)+'LR'+str(_s1L)+ str(_s1R)
	# str(diff_T)+str(diff_B)+str(diff_L)+str(diff_R)
	#
	if o_w_1 != o_w_2:
		msg = "ignore"
	else:
		msg = True
	#
	return [overall_diff, msg, o_w_1]
	#
#
def init_permut(glyph_nums, direction, max_diff):
	#
	seen_mililar = []
	seen_keys = []
	seen_vals = []
	seen_vals_extend = []
	#
	all_mils = collections.OrderedDict()
	#
	glyph_items = glyph_nums.items()
	#
	glyph_items_len = len(glyph_items)
	glyph_items_pemut_len = glyph_items_len*glyph_items_len
	#
	all_y = 0
	#
	for key, vals in glyph_items:
		#
		y = 0
		#
		#
		t_mils = collections.OrderedDict()
		#
		for in_key, in_vals in glyph_items:
			#
			#
			res = do_compare_mtx_colors(vals, in_vals, key, in_key, direction)
			#
			print('\r\t'+str([glyph_items_pemut_len, all_y])+' > SIM: '+str(float("%0.1f" % (res[0])))+' FOR: '+key+' OVER: '+str(in_key)+flush_space, end='')
			#
			if res[1] != 'ignore':
				#
				t_mils[in_key] = [res[0], res[2]]
				#
			#
			seen_vals.append(vals)
			#
			y = y + 1
			#
		#
		all_y = all_y + y
		#
		seen_keys.append(key)
		#
		if len(t_mils) > 1:
			#
			prob_mils = keep_probable(t_mils, max_diff)
			all_mils[key] = prob_mils
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