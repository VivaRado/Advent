
import os
from argparse import ArgumentParser
#
from Autokern import Autokern
from AutokernSettings import AutokernSettings
import tfs.common.TFSProject as TFSProject
from tfs.common.TFSMap import TFSMap
#
parser = ArgumentParser()
parser.add_argument("-d", "--dir", dest="directory",
                    help="Directory of UFOs to kern", metavar="FILE")
parser.add_argument("-f", "--fontfile", dest="fontfiles", 
                    help="The font filename of the UFOs without the weights, example filename: fontname_bld (we assume underscore)")
parser.add_argument("-w", "--weights", dest="weights", 
                    help="The weights comma separated, example filename: fontname_bld (we assume underscore)")
#
args = parser.parse_args()
#
dir_path = os.path.dirname(os.path.realpath(__file__))
#
PIDDIR=dir_path+"/src-main-reord/Autokern.py"
#
#
def do_kern_for_pairs(dir_path, fontfilename, weights_str):
	x = 0
	#
	_dir = dir_path+'/'
	#
	weights = weights_str.split(',')
	#
	#
	for w in weights:	
		#
		print(_dir+fontfilename+"_"+w+".ufo")
		#
		in_fnt=_dir+fontfilename+"_"+w+".ufo"
		out_fnt=_dir+fontfilename+"_"+w+"_krn.ufo"
		#
		pseudo_argv = ('--ufo-src-path',
						in_fnt,
						'--ufo-dst-path',
						out_fnt,
						'--min-distance-ems',
						'0.08',
						'--max-distance-ems',
						'0.10',
						'--max-x-extrema-overlap-ems',
						'0.10',
						'--intrusion-tolerance-ems',
						'0.02',
						'--precision-ems',
						'0.005',
						#'--log-path',
						#'/media/root/Malysh1/winshm/advent_repo/Advent/scripts/kerning_scripts/kern_log/log',
						#'--log-basic-pairs',
						#'--write-kerning-pair-logs'
						)

		print ('pseudo_argv', ' '.join([str(arg) for arg in pseudo_argv]))
		
		autokernArgs = TFSMap()
		AutokernSettings(autokernArgs).getCommandLineSettings(*pseudo_argv)
		autokern = Autokern(autokernArgs)
		autokern.process()
		#
		x = x + 1
		#
		print ('Completed:'+w+' '+str(x)+'/'+str(len(weights))+'\n'+' Produced Kerned UFO:'+out_fnt)
		#
		print ('Replace the kern.plist at your leasure')
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
	do_kern_for_pairs(args.directory, args.fontfiles, args.weights)
	#
#

