#
#!/usr/bin/env python
import os
#
from Lib.efo import EFO
#import Lib.generic.tab_completion
#
from argparse import ArgumentParser
#
#REMOVE
from pprint import pprint
#
parser = ArgumentParser()
parser.add_argument("-s", "--source", dest="source",
                    help="Source EFO", metavar="FILE")
parser.add_argument("-o", "--output", dest="output", 
                    help="Directory to output UFO files")
parser.add_argument("-f", "--fonts", dest="fonts", 
                    help="EFO Fonts Instances to Export to UFOs comma separated")
parser.add_argument("-k", "--kerning_type", dest="kerning_type", 
                    help='Kerning Type to copy to UFOs')
#
args = parser.parse_args()
#
dir_path = os.path.dirname(os.path.realpath(__file__))
#
faults = False
#
if  args.source is None:
	#
	faults = True
	#
	print('=\n=> Please Provide Source EFO File: -s "/font.efo"\n=')	
	#
if  args.output is None:
	#
	faults = True
	#
	print('=\n=> Please Provide Output Directory for UFOs: -o "dir/"\n=')	
	#
if  args.fonts is None:
	#
	faults = True
	#
	print('=\n=> Please Provide the Font Instances to Export to UFO: -f "thn,reg,bld"\n=')	
	#
if  args.kerning_type is None:
	#
	faults = True
	#
	print('=\n=> Please Provide the Kerning Type to copy to UFOs: -k "class" / "flat" \n=')	
	#
else:
		
	if args.kerning_type not in ["class","flat"]:
		#
		faults = True
		#
		print('=\n=> Please Provide a Valid Kerning Type: -k "class" / "flat" \n=')	
		#
if faults == False:
	#
	EFO = EFO(args.source,args.output)
	#
	EFO._efo_to_ufos(args.fonts, False, args.kerning_type)
	#
	fontinfo_json = EFO.fontinfo
	#
#

