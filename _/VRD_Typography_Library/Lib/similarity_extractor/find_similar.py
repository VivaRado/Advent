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

# # tab completion 
# readline.parse_and_bind('tab: complete') 
# # history file 
# histfile = os.path.join(os.environ['HOME'], '.pythonhistory') 
# try: 
# 	readline.read_history_file(histfile) 
# except IOError: 
# 	pass 
# atexit.register(readline.write_history_file, histfile) 
# del histfile, readline, rlcompleter
# #
# #



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