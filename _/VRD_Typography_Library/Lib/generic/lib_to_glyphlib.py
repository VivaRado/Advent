import os
# import io
import random
from math import sqrt, ceil, floor
import datetime
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
from .glyphnames import * #adobe_glyph_list
#
import xml.etree.cElementTree as ET
import xml.dom.minidom as minidom
#
from Lib.generic import generic_tools
#
def match_glyph_uni(_name):
	#
	for x in adobe_glyph_list:
		#
		char_split = x.split(';', 1)
		char_name = str(char_split[0])
		char_uni = str(char_split[1])
		#
		if char_name == _name:
			#
			return char_uni
			#
	#
#
def lib_to_glyphlib(_in, _out):
	#
	glyphlib = ET.Element("glyphlib")
	#
	found = []
	#
	p_g = plistlib.readPlist(_in)
	#
	no_uni_found = []
	#
	for k,v in p_g.items():
		#
		for glyph_name in v:
			#
			ret_uni = match_glyph_uni(glyph_name)
			#
			if ret_uni:
				#
				pass
				#
			else: 
				#
				print('\r\t'+"NO_UNI: ", glyph_name, end='')
				#
				no_uni_found.append(glyph_name)
				#
				ret_uni = ""
				#
			#
			glyph = ET.Element("glyph", dict(name=glyph_name, unicode=ret_uni, glif=generic_tools.glyphNameToFileName(glyph_name).split('.glif')[0]))
			#
			glyphlib.append(glyph)
			#
		#
	#
	print('\r\t'+'No Unicode Values for: ', ','.join(no_uni_found),end='')
	print('\n')
	#
	rough_string = ET.tostring(glyphlib, 'utf-8')
	reparsed = minidom.parseString(rough_string)
	#
	with open(_out, "w") as writter:
		#
		pretty_xml_as_string = reparsed.toprettyxml(indent="\t")
		dom = minidom.parseString(pretty_xml_as_string)
		#
		writter.write(pretty_xml_as_string)
	#
#
