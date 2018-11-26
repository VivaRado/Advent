import os
import io
import random
import itertools
import threading
import time
import sys
from sys import argv
import re
import json
import getpass
import shutil
from datetime import datetime
import csv
import ast

from PIL import Image

from subprocess import Popen, PIPE

from time import gmtime, strftime

# python startup file 
import readline 
import rlcompleter 
import atexit 
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
user_input_enc = input("Glyph Audit file: ")
#
data_read = []
found_weights = []
#
# Read CSV file
kwargs = {'newline': ''}
mode = 'r'
if sys.version_info < (3, 0):
	kwargs.pop('newline', None)
	mode = 'rb'
#
#
with open(user_input_enc, mode, **kwargs) as fp:
	#
	reader = csv.reader(fp, delimiter=',', quotechar='"')
	#
	data_read = []
	#
	next(reader)
	#
	for line_list in reader:
		#
		#print(line_list[-1])
		#
		anchor_count_list = line_list[-1].replace('[','').replace(']','');
		#
		anchor_count_list = [int(x) for x in anchor_count_list.split(',')]
		#
		line_list[-1] = anchor_count_list
		#
		if line_list[0] not in found_weights:
			found_weights.append(line_list[0])
		#
		data_read.append(line_list)
		#
	#
#
layers = []
#
for x in found_weights:
	layers.append([])
#
ix = 0
#
for y in data_read:
	#
	if ix <= len(found_weights):
		#
		#
		#if y[0] not in found_weights:
			#
		layers[ix].append(y)
			#
		if y[0] != found_weights[ix]:
			#
			ix = ix + 1
			#
	else:
		#
		break
		#
#
try:
	for z in range(len(layers[0])):
		#
		if z == 0:
			print('Report'+'\n'+','.join(found_weights))
		#
		#
		audit_result = ''
		#
		if (layers[0][z][-1] != layers[1][z][-1] != layers[2][z][-1]):
			audit_result = "✕"
		else:
			audit_result = "✓"
		#
		print (str(layers[0][z][-1])+", "+str(layers[1][z][-1])+", "+str(layers[2][z][-1]) + str(layers[0][z][1])+": "+layers[0][z][2]+' = '+audit_result)
		#
except Exception:
	pass