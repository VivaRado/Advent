#
import os
import sys
import shutil
import re
import plistlib
import json
#
import xml.etree.cElementTree as ET
import xml.dom.minidom as minidom
#
#
def merge_two_dicts(x, y):
	"""Given two dicts, merge them into a new dict as a shallow copy."""
	z = x.copy()
	z.update(y)
	return z
#
def json_to_plist(data):
	#
	plist_data = plistlib.dumps(data,sort_keys=False).decode("utf-8") 
	#
	return plist_data
	#
def plist_to_json(_dir):
	#
	#file = open(_dir, 'r')
	plist_data = plistlib.readPlist(_dir)#.decode("utf-8") 
	#
	return plist_data
	#
#
def sanitize_string(string):
	#
	# Author: https://blog.dolphm.com/slugify-a-string-in-python/
	#
	s = string.encode().decode("utf8","ignore")
	#
	s = s.lower()

	# "[some] _ article's_title--"
	# "[some]___article's_title__"
	for c in [' ', '-', '.', '/']:
		s = s.replace(c, '_')

	# "[some]___article's_title__"
	# "some___articles_title__"
	s = re.sub('\W', '', s)

	# "some___articles_title__"
	# "some   articles title  "
	s = s.replace('_', ' ')

	# "some   articles title  "
	# "some articles title "
	s = re.sub('\s+', ' ', s)

	# "some articles title "
	# "some articles title"
	s = s.strip()

	# "some articles title"
	# "some-articles-title"
	s = s.replace(' ', '_')
	#
	return s
	#
#
def make_dir(directory):
	#
	if not os.path.exists(directory):
		os.makedirs(directory)
	#
#
def write_to_file(_file,_data):
	#
	file = open(_file, 'w')
	file.write(_data)
	file.close()
	#
#
def check_given_fonts_exist( _fonts, font_files):
	#
	given_fonts = _fonts.split(',')
	#
	faults = False
	#
	if ',' in _fonts:
		#
		for f in given_fonts:
			#
			if f not in font_files:
				#
				faults = True
				#
				print('\tGiven Font: '+f+' IS NOT IN EFO FONTS ✗')
				#
			#
			else:
				#
				print('\tGiven Font: '+f+' IS IN EFO FONTS ✓')
				#
		#
	else:
		#
		f = _fonts
		#
		if f not in font_files:
			#
			faults = True
			#
			print('\tGiven Font: '+f+' IS NOT IN EFO FONTS ✗')
			#
		#
		else:
			#
			print('\tGiven Font: '+f+' IS IN EFO FONTS ✓')
			#
	#
	return faults
	#
#
def check_given_vectors_exist( _fonts, _vectors_dir):
	#
	given_fonts = _fonts.split(',')
	#
	faults = False
	#
	print(_vectors_dir)
	print(_fonts)
	#
	if ',' in _fonts:
		#
		for f in given_fonts:
			#
			if f not in font_files:
				#
				faults = True
				#
				print('\tGiven Font: '+f+' IS NOT IN EFO FONTS ✗')
				#
			#
			else:
				#
				print('\tGiven Font: '+f+' IS IN EFO FONTS ✓')
				#
		#
	else:
		#
		f = _fonts
		#
		if f not in font_files:
			#
			faults = True
			#
			print('\tGiven Font: '+f+' IS NOT IN EFO FONTS ✗')
			#
		#
		else:
			#
			print('\tGiven Font: '+f+' IS IN EFO FONTS ✓')
			#
	#
	return faults
	#
#
def empty_dir(_dir):
	#
	print('\tEmptied Directory: '+_dir)
	#
	for the_file in os.listdir(_dir):
		file_path = os.path.join(_dir, the_file)
		try:
			if os.path.isfile(file_path):
				os.unlink(file_path)
			elif os.path.isdir(file_path): shutil.rmtree(file_path)
		except Exception as e:
			print(e)
	#
#
def rm_dir(_dir):
	#
	shutil.rmtree(_dir)
	#
#
def rename_dir(src, dst):
	#
	os.rename(src, dst)
	#
#
def copyDirectory(src, dest):
	try:
		shutil.copytree(src, dest)
	# Directories are the same
	except shutil.Error as e:
		print('Directory not copied. Error: %s' % e)
	# Any error saying that the directory doesn't exist
	except OSError as e:
		print('Directory not copied. Error: %s' % e)


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
def get_dict_wo_key(dictionary, key):
	"""Returns a **shallow** copy of the dictionary without a key."""
	_dict = dictionary.copy()
	_dict.pop(key, None)
	return _dict
#

def glyphNameToFileName(glyphName):
	"""Default algorithm for making a file name out of a glyph name.
	This one has limited support for case insensitive file systems:
	it assumes glyph names are not case sensitive apart from the first
	character:
		'a'     -> 'a.glif'
		'A'     -> 'A_.glif'
		'A.alt' -> 'A_.alt.glif'
		'A.Alt' -> 'A_.Alt.glif'
		'T_H'   -> 'T__H_.glif'
		'T_h'   -> 'T__h.glif'
		't_h'   -> 't_h.glif'
		'F_F_I' -> 'F__F__I_.glif'
		'f_f_i' -> 'f_f_i.glif'
		'AE'    -> 'AE__.glif'
	"""
	if glyphName.startswith("."):
		# some OSes consider filenames such as .notdef "hidden"
		glyphName = "__" + glyphName[1:]
	parts = glyphName.split(".")
	if parts[0].find("_")!=-1:
		# it is a compound name, check the separate parts
		bits = []
		for p in parts[0].split("_"):
			if p != p.lower():
				bits.append(p+"_")
				continue
			bits.append(p)
		parts[0] = "_".join(bits)
	else:
		#
		# is capital digram
		have_upper = 0
		#
		for p in parts:
			#
			if len(p) > 1:
				#
				_p = list(p)
				#
				for x in _p:
					#
					if x.isupper():
						#
						have_upper += 1
						#
				#
			#
		#
		if have_upper > 1:
			#
			parts[0] += "__"
			#
		else:
			# it is a single name
			if parts[0] != parts[0].lower():
				parts[0] += "_"
			#
	for i in range(1, len(parts)):
		# resolve additional, period separated parts, like alt / Alt
		if parts[i] != parts[i].lower():
			parts[i] += "_"
	return ".".join(parts) + ".glif"


def GLIFFileNametoglyphName(glyphName):
	"""Default algorithm for making a file name out of a glyph name.
	This one has limited support for case insensitive file systems:
	it assumes glyph names are not case sensitive apart from the first
	character:
		'a'     <- 'a'
		'A'     <- 'A_'
		'A.alt' <- 'A_.alt'
		'A.Alt' <- 'A_.Alt'
		'T_H'   <- 'T__H_'
		'T_h'   <- 'T__h'
		't_h'   <- 't_h'
		'F_F_I' <- 'F__F__I_'
		'f_f_i' <- 'f_f_i'
		'AE'    <- 'AE__'
	"""
	if glyphName.startswith("__"):
		# some OSes consider filenames such as .notdef "hidden"
		glyphName = "." + glyphName[1:]
	parts = glyphName.split(".")
	#
	if parts[0].find(".")!=-1:
		# it is a compound name, check the separate parts
		bits = []
		for p in parts[0].split("."):
			if p != p.lower():
				bits.append(p+".")
				continue
			bits.append(p)
		parts[0] = ".".join(bits)
	else:
		# it is a single name
		if parts[0] != parts[0].lower():
			parts[0] += "."
	for i in range(1, len(parts)):
		# resolve additional, period separated parts, like alt / Alt
		if parts[i] != parts[i].lower():
			parts[i] += "."
	return "".join(parts)# + ".glif"
#
def determine_kerning_type_ufo(ufo_dir):
	#
	has_groups = os.path.isfile(os.path.join(ufo_dir,"groups.plist"))
	#
	return has_groups
#
def get_between(_start, _end, _str):
	#
	return _str[_str.find(_start)+len(_start):_str.find(_end)]
	#
#
def copy_dict(_d):
	return {k:v for k,v in _d.items()}