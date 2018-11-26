import os
#
#import Lib.generic.tab_completion
from Lib.efo import EFO
from Lib.similarity_extractor import SIMEX
from Lib.kerning import AUTOKERN
#
from argparse import ArgumentParser
#
#
parser = ArgumentParser()
parser.add_argument("-s", "--source", dest="source",
					help="Source EFO", metavar="FILE")
parser.add_argument("-f", "--fonts", dest="fonts", 
					help="UFO Fonts to Automatically Kern, comma separated")
parser.add_argument("-c", "--compress_class_plist", dest="compress_class_plist", 
					help="Similarity Plist to Use for Compression to Class Based Kerning")
#
args = parser.parse_args()
#
#dir_path = os.path.dirname(os.path.realpath(__file__))
#
faults = False
#
if  args.source is None:
	#
	faults = True
	#
	print('=\n=> Please Provide Source EFO File: -s "/font.efo"\n=')	
	#
if  args.fonts is None:
	#
	faults = True
	#
	print('=\n=> Please Provide the Fonts to Extract Similarity: -f "thn,reg,bld"\n=')	
	#
#
if  args.compress_class_plist is None:
	#
	faults = True
	#
	print('=\n=> Please Select to Compress to Class Based Kerning through Similarity Plist (Obtained by kerning_extract_similarity.py and stored in your EFO/groups): -c "Yes"/"No" \n=')
	#
#
if faults == False:
	#
	EFO_temp = os.path.join(args.source,"temp")
	#
	EFO = EFO(args.source,EFO_temp)
	#
	EFO._efo_to_ufos(args.fonts, True, "flat")
	#
	AUTOKERN = AUTOKERN(args.source, args.fonts, args.compress_class_plist)
	#
	AUTOKERN.do_kern_for_pairs()
	#
	AUTOKERN.flat_kern_to_efo(args.source)
	#
#

