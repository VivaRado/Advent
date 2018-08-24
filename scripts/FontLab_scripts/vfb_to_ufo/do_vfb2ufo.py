import os
from os.path import basename
from argparse import ArgumentParser
#
parser = ArgumentParser()
parser.add_argument("-d", "--idir", dest="indirectory",
					help="Input Directory of VFBs", metavar="FILE")
parser.add_argument("-o", "--odir", dest="outdirectory", 
					help="Output Directory of UFOs", metavar="FILE")
parser.add_argument("-f", "--format", dest="toformat", 
					help="Output Format")
#
dir_path = os.path.dirname(os.path.realpath(__file__))
#
exe_loc = dir_path+'\\'+'vfb2ufoWin\\exe\\'+'vfb2ufo.exe'
#
def doConvert(in_dir, out_dir, to_format):
	#
	print (to_format)
	#
	for filename in os.listdir(in_dir):
		#
		if to_format == "vfb":
			find_format = "ufo"
		else:
			find_format = "vfb"

		if filename.endswith("."+find_format): 
			
			print(exe_loc)
			print(os.path.join(in_dir, filename))
			#
			infile = os.path.join(in_dir, filename)
			outfile = out_dir+'\\'+basename(filename).split('.')[0]+'.'+to_format
			#
			os.system(exe_loc+" "+infile+" "+outfile)
			#
		else:
			continue

args = parser.parse_args()
#
#
faults = False
#
if  args.indirectory is None:
	#
	faults = True
	#
	print('=\n=> Please Provide Valid Directory: -d "/font_input_directory"\n=')	
	#
else:
	#
	if os.path.isdir(args.indirectory) == False:
		#
		faults = True
		#
		print('=\n=> Please Provide Valid Directory: -d "/font_input_directory"\n=')	
		#

#
if  args.outdirectory is None:
	#
	faults = True
	#
	print('=\n=> Please Provide Valid Output Directory: -o "/font_output_directory"\n=')	
	#
else:
	#
	if os.path.isdir(args.outdirectory) == False:
		#
		faults = True
		#
		print('=\n=> Please Provide Valid Output Directory: -o "/font_output_directory"\n=')	
		#

#
if  args.toformat is None:
	#
	faults = True
	#
	print('=\n=> Please Provide Valid Output Format: -f "vfb" or -f "ufo"\n=')	
	#
#
if faults == False:
	#
	doConvert(args.indirectory, args.outdirectory, args.toformat)
	#
#

