# -*- encoding: utf-8 -*-
'''
example
	
	sh '/do_autokern.sh' -d '/sources_ufo' -k '/kern_fixes' -f 'fontname' -w 'thn,reg,bld'

'''
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
parser.add_argument("-k", "--kernlistdir", dest="kernlistdir", 
                    help="Directory to output the textfiles with kern pairs")
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
pairlist = {}
#
def get_kern_pair_file_to_tupple(fontfilename, weights, kern_file_location):
	#
	for w in weights:
		#
		weight_list = kern_file_location+'/'+fontfilename+'_'+w+'_krn_fix_list'
		#
		ifile=open(weight_list, "r")
		lines=ifile.readlines()
		#
		l = []
		#
		for li in lines:
			#
			for g in li.split(','):
				#
				l.append(g.strip().replace("'", ''))
				#
		#
		data = tuple(filter(None, l))
		#
		pairlist[w] = data
		#
	#
#
def do_kern_for_pairs(dir_path, fontfilename, weights_str, kernlistdir):
	x = 0
	#
	_dir = dir_path+'/'
	#
	weights = weights_str.split(',')
	#
	get_kern_pair_file_to_tupple(fontfilename, weights, kernlistdir)
	#
	for w in weights:	
		#
		print(_dir+fontfilename+"_"+w+".ufo")
		#
		in_fnt=_dir+fontfilename+"_"+w+"_krn.ufo"
		out_fnt=_dir+fontfilename+"_"+w+"_krn_fix.ufo"
		#
		pseudo_argv = ('--ufo-src-path',
							in_fnt,
							'--ufo-dst-path',
							out_fnt,
							'--min-distance-ems',
							'0.04',
							'--max-distance-ems',
							'0.05',
							'--max-x-extrema-overlap-ems',
							'0.1',
							'--intrusion-tolerance-ems',
							'0.02',
							'--precision-ems',
							'0.005',
							'--glyph-pairs-to-kern')

		autokernArgs = TFSMap()
		AutokernSettings(autokernArgs).getCommandLineSettings(*(pseudo_argv+pairlist[w]))
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
if  args.kernlistdir is None:
	#
	faults = True
	#
	print('=\n=> Please Provide Valid Kern List Directory: -d "/kern_list_dir"\n=')	
	#
else:
	#
	if os.path.isdir(args.kernlistdir) == False:
		#
		faults = True
		#
		print('=\n=> Please Provide Valid Kern List Directory: -d "/kern_list_dir"\n=')	
		#
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
	do_kern_for_pairs(args.directory, args.fontfiles, args.weights, args.kernlistdir)
	#
#

