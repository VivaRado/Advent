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
from argparse import ArgumentParser

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
	weights_perm= {"thn":[],"reg":[],"bld":[]}
	#
	x = 0
	#
	move_by = 20
	#
	inner = ''
	#
	all_letters = []
	#
	for w in weights:	
		#
		orig_w = w
		#
		result_lines = ''
		result_keys = []
		#
		out_fnt=_dir+'/'+fontfilename+"_"+w+"_krn.ufo"+'/'+'kerning.plist'
		#
		with open(out_fnt) as f:
	 		#
			lines = f.readlines()
			#
			for x in lines:
				#
				if '<?xml' in x or '<!DOCTYPE' in x or '<plist' in x or '</plist' in x:
					pass
				else:
					#
					result_lines = result_lines + x
					#
		#
		the_dict = [x.strip() for x in re.findall('<dict.*?>(.*)</dict>', result_lines, re.MULTILINE | re.DOTALL)][0]
		#
		the_keys_text = the_dict.split('''\t</dict>\n\t''')
		#
		total_permut = ''
		#
		for u in the_keys_text:
			#
			the_keys = [x.strip() for x in re.findall('<key.*?>(.*)</key>', u)]
			#
			num_of_glyphs = 0
			not_found = []
			all_results = []
			orig_results = []
			#
			for y in the_keys:
				#
				orig_results.append(y)
				#
			#
			permut_str = ''
			#
			iter_res = iter(orig_results)
			next(iter_res)
			#
			for z in iter_res:
				#
				permut_str = permut_str + "'"+orig_results[0]+"','"+z+"',"+'\n'
				#
			#
			total_permut = total_permut + permut_str
			#
			weights_perm[orig_w].append(permut_str)
			#
		#
		file = open(outputdir+'/'+fontfilename+"_"+w+"_krn_fix_list", 'w')
		file.write(total_permut)
		file.close()
		#
		print(fontfilename+"_"+w+' '+'Done!')
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

