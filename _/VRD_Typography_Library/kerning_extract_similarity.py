import os
#
#import Lib.generic.tab_completion
from Lib.efo import EFO
from Lib.similarity_extractor import SIMEX
#
from argparse import ArgumentParser
#
#
parser = ArgumentParser()
parser.add_argument("-s", "--source", dest="source",
					help="Source EFO", metavar="FILE")
parser.add_argument("-f", "--font", dest="font", 
					help="UFO Font to Extract Similarity.")
parser.add_argument("-p", "--purpose", dest="purpose", 
					help='What is the purpose of Similarity Extraction')
# parser.add_argument("-c", "--compress", dest="compress", 
# 					help='Compress Similarity to Class Based Plist')
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
if  args.font is None:
	#
	faults = True
	#
	print('=\n=> Please Provide the Font to Extract Similarity one Similarity Component and one Similarity Kerning Plist for each font family, preferably provide the Regular: -f "reg"\n=')	
	#
#
if  args.purpose is None:
	#
	faults = True
	#
	print('=\n=> Please Provide the Purpose of Similarity Extraction: component 1 to 1 similarity, or kerning groups loose similarity: -p "comp" or "kern"\n=')	
	#
#
# if  args.compress is None:
# 	#
# 	faults = True
# 	#
# 	print('=\n=> Please Select to Compress to Class Based Plist: -c "Yes" or "No" \n=')	
	#
#
if faults == False:
	#
	EFO_temp = os.path.join(args.source,"temp")
	#
	EFO = EFO(args.source,EFO_temp)
	#
	EFO._efo_to_ufos(args.font, True)
	#
	SIMEX = SIMEX(args.source, args.purpose, args.compress, args.font)
	#
	SIMEX.extract_similarity()
	#
	print("Manual Crosscheck would be wise for the generated Similarity Plists")
	#
#