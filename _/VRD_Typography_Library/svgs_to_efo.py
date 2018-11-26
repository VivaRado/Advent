#
#!/usr/bin/env python
import os
#
from Lib.efo import EFO
from Lib.ufo2svg import UFO2SVG
import Lib.generic.tab_completion
#
from argparse import ArgumentParser
#
#REMOVE
from pprint import pprint
#
parser = ArgumentParser()
parser.add_argument("-s", "--source", dest="source",
                    help="Source EFO", metavar="FILE")
parser.add_argument("-f", "--fonts", dest="fonts", 
                    help="Vector Fonts to convert comma separated")
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
if  args.fonts is None:
	#
	faults = True
	#
	print('=\n=> Please Provide the Fonts to Convert to GLIF and Integrate to EFO: -f "thn,reg,bld"\n=')	
	#
# if len(args.fonts) == 0:
# 	#
# 	faults = True
# 	#
# 	print('=\n=> Please Provide the Fonts to Convert to GLIF and Integrate to EFO: -f "thn,reg,bld"\n=')	
# 	#
#
if faults == False:
	#
	#EFO_temp = os.path.join(args.source,"temp")
	#
	#EFO = EFO(args.source,EFO_temp)
	#
	#EFO._efo_to_ufo(args.fonts)
	#
	UFO_to_SVG = UFO2SVG(args.source,args.fonts)
	#
	UFO_to_SVG.svgs_to_efo()
	#
#

