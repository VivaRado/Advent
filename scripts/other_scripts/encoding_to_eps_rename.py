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

from PIL import Image

from subprocess import Popen, PIPE

from time import gmtime, strftime

# python startup file 
import readline 
import rlcompleter 
import atexit 
#
from glyphnames import *
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
def uni_to_char(lookup, _type):
	#
	found = []

	for x in adobe_glyph_list:
		#
		char_split = x.split(';', 1)
		char_name = str(char_split[0])
		char_uni = str(char_split[1])
		#
		#print('> ',lookup,char_uni)
		#
		append_opentype = ''
		is_dash = ''
		#
		if "." in lookup:
			l_s = lookup.split('.')
			lookup = l_s[0]
			append_opentype = l_s[1]
			is_dash = '-'
		#
		if (_type == 'uni'):
			
			if (lookup == char_uni):
				found.append([str('\\u'+lookup).encode('utf-8').decode("unicode-escape"),char_name+is_dash+append_opentype,char_uni])
		
		else:
			if (lookup == char_name):
				found.append([str('\\u'+char_uni).encode('utf-8').decode("unicode-escape"),char_name+is_dash+append_opentype,char_uni])	
		#
	#
	if len(found) >= 1:
		ret = found[0]
	else:
		ret = found
	#
	return ret
	#
#
#
#
user_input_eps = input("Directory of EPS files: ")
user_input_enc = input("Directory of ENC file: ")
#
all_results = [];
#
not_found = [];
#
#
for file in os.listdir(user_input_enc):
	#
	if file.endswith(".enc"):
		#
		fp = open(os.path.join(user_input_enc, file)) # Open file on read mode
		lines = fp.read().split("\n") # Create a list containing all lines
		#
		del lines[0]
		#
		for x in lines:
			#
			charname = x.split(" ")[0]
			#
			print(charname)
			#
			if 'uni' in charname:
				#print(y)
				get_uni = charname.split('uni')[1];
				#print('>>',get_uni)
				ret_char = uni_to_char(get_uni, 'uni')
				#
				if ret_char != []:
					#print(ret_char )
					all_results.append(ret_char)
				else:
					#print('not_found:',charname)
					not_found.append(charname)
					all_results.append(["undefined",charname,"9999"])
			else:
				#
				ret_char = uni_to_char(charname, 'nom')
				#
				if ret_char != []:
					#print(ret_char )
					all_results.append(ret_char)
				else:
					#print('not_found:',charname)
					not_found.append(charname)
					all_results.append(["undefined",charname,"9999"])
				#
				
			#
		#
		fp.close() # Close file
		#print(os.path.join(user_input, file))
#
#print('###############')
#print(all_results)
#print('###############')
#print(not_found)
#print(len(not_found))
#
new_dir_name = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
#
seen_names = []
#
def copy_rename(old_file, new_file_name, given_curdir):
	#
	given_curdir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', given_curdir))
	#
	try:
		new_dir_full = os.path.join(given_curdir, new_dir_name)
		new_dir_full_exists = os.path.join(new_dir_full, 'exists')
		#
		if not os.path.exists(new_dir_full):
			os.makedirs(new_dir_full)
		#
		#
		if not os.path.exists(new_dir_full_exists):
			os.makedirs(new_dir_full_exists)
		#
		#dst_dir= os.path.join(given_curdir, new_dir_name)
		#src_file = os.path.join(given_curdir, old_file)
		#
		#
		if new_file_name in seen_names:
			print(new_file_name+' EXISTS NAME')
			try:
				shutil.copy(os.path.join(given_curdir, old_file),new_dir_full_exists)
				
			except Exception as ex:
				print ("Unable to copy file. %s" % ex)
			#
			dst_file = os.path.join(new_dir_full_exists, old_file)
			new_dst_file_name = os.path.join(new_dir_full_exists, new_file_name)
			#
			try:
				
				os.rename(dst_file, new_dst_file_name)
				print('____________________='+new_file_name)
				
			except Exception as ex:

				print ("Unable to rename. %s" % ex+'='+new_file_name)
			#
			#shutil.move(os.path.join(given_curdir, old_file),os.path.join(new_dir_full, new_file_name))
		else:

			#shutil.copy(os.path.join(given_curdir, old_file),new_dir_full)
			#shutil.move(os.path.join(given_curdir, old_file),os.path.join(new_dir_full, new_file_name))
			#
			try:
				shutil.copy(os.path.join(given_curdir, old_file),new_dir_full)
				
			except Exception as ex:
				print ("Unable to copy file. %s" % ex)
			#
			dst_file = os.path.join(new_dir_full, old_file)
			new_dst_file_name = os.path.join(new_dir_full, new_file_name)
			#
			try:
				
				os.rename(dst_file, new_dst_file_name)
				print('____________________='+new_file_name)
				
			except Exception as ex:

				print ("Unable to rename. %s" % ex+'='+new_file_name)
			#
		seen_names.append(new_file_name)

		#
	except Exception as ex:
		print(ex)
# 
	


#
#
corrupt_files = []
u = 0
#
filelist = os.listdir(user_input_eps)
#
filelist = sorted(filelist,key=lambda x: int(os.path.splitext(x)[0].split('___')[0]))
#
for file in filelist:
	#
	if file.endswith(".eps"):
		#pass
		is_corrupt = False
		#
		print(os.path.join(user_input_eps, file), all_results[u])
		#
		print(file)
		#
		try:	
			test = Image.open(os.path.join(user_input_eps, file))

		except Exception as ex:
			print ("Corrupt file. %s" % ex)
			corrupt_files.append(file)
			is_corrupt = True
		#
		if is_corrupt == False:
			
			copy_rename(file, all_results[u][1].replace('.','-')+'__'+all_results[u][2]+'.eps', user_input_eps)
		#
		
		#
		u = u + 1
#
print('CORRUPT')
print(corrupt_files)
print(len(sorted(os.listdir(user_input_eps))))
print(u)

# file = open(user_input,'r+')
# #
# with file as f:
# 	#
# 	data = json.load(f)
# 	#
# 	for d in data:
# 		print(d)
# 	#
# 	#print(data)
# 	#
# #
# f.close()