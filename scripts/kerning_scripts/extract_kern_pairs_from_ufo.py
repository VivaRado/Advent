'''
example command:

python3 'extract_kern_pairs_from_ufo.py' -d '/sources_ufo' -f 'fontname' -w 'thn,reg,bld' -o '/kern_fixes_output_dir'

example directory structure:

/sources_ufo
	fontname_thn.ufo
	fontname_reg.ufo
	fontname_bold.ufo

we assume underscore to separate the name and the weight

'''
import os
import re
#
import plistlib
#
from argparse import ArgumentParser
#


parser = ArgumentParser()
parser.add_argument("-d", "--dir", dest="directory",
					help="Directory of UFOs to extract kerning pairs", metavar="FILE")
parser.add_argument("-f", "--fontfile", dest="fontfiles", 
					help="The font filename of the UFOs without the weights, example filename: fontname_bld (we assume underscore)")
parser.add_argument("-w", "--weights", dest="weights", 
					help="The weights comma separated, example filename: fontname_bld (we assume underscore)")
parser.add_argument("-o", "--output", dest="outputdir", 
					help="Directory to output the textfiles with kern pairs")
#
args = parser.parse_args()
#
def extract_pairs(dir_path, fontfilename, weights, outputdir):
	#
	_dir = dir_path
	#
	weights= weights.split(',')
	#
	weights_perm = {}
	#
	for z in range(len(weights)):
		#
		weights_perm[weights[z]] = []
		#
	#
	x = 0
	#
	total_permut = ''
	#
	for w in weights:	
		#
		orig_w = w
		#
		result_lines = ''
		result_keys = []
		#
		w = w + '_it'
		#
		out_fnt=_dir+'/'+fontfilename+"_"+w+"_krn.ufo"+'/'+'kerning.plist'
		#
		pl = plistlib.readPlist(out_fnt)
		#
		for x,v in pl.items():
			#
			for z,y in v.items():
				#
				permu_list = [x,z]
				permut_str = '"'+x+'","'+z+'"'+'\n'
				#
				total_permut = total_permut + permut_str
				#
				weights_perm[orig_w].append(permu_list)
				#
			#
		#
		file = open(_dir+'/'+fontfilename+"_"+w+"_krn_fix_list", 'w')
		file.write(total_permut)
		file.close()
	#
	print(weights_perm)
	#
	print("Done!")
	print("Files at:",dir_path)
	#
#
faults = False
#
if  args.directory is None:
	#
	faults = True
	#
	print('=\n=> Please Provide Valid Directory: -d "/font_ufo_directory"\n=')	
	#
else:
	#
	if os.path.isdir(args.directory) == False:
		#
		faults = True
		#
		print('=\n=> Please Provide Valid Directory: -d "/font_ufo_directory"\n=')	
		#
	#
if  args.outputdir is None:
	#
	faults = True
	#
	print('=\n=> Please Provide Valid Output Directory: -o "/font_kern_pair_output_directory"\n=')
	#
else:
	if os.path.isdir(args.outputdir) == False:
		#
		faults = True
		#
		print('=\n=> Please Provide Valid Output Directory: -o "/font_kern_pair_output_directory"\n=')
		#

if args.fontfiles is None:
	#
	faults = True
	#
	print('=\n=> Please Provide Font Family File Name: -f "fontname"\n=')
	#
#
if args.weights is None:
	#
	faults = True
	#
	print('=\n=> Please Provide Comma Separated Font Weights String: -w "thn,reg,bld"\n=')
	#
#
if faults == False:
	#
	extract_pairs(args.directory, args.fontfiles, args.weights, args.outputdir)
	#
#

