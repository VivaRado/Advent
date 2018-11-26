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
                    help="Source fontinfo.JSON", metavar="FILE")
parser.add_argument("-o", "--output", dest="output", 
                    help="Directory to output EFO file")
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
	print('=\n=> Please Provide Source fontinfo.JSON File: -s "/fontinfo.json"\n=')	
	#
if  args.output is None:
	#
	#faults = True
	#
	print('=\n=> Output Directory for EFO is fontinfo.JSON Parent Directory or Provide: -o "dir/"\n=')	
	#
if faults == False:
	#
	EFO = EFO(args.source,args.output)
	#
	EFO._ufos_to_efo()
	#
	fontinfo_json = EFO.fontinfo
	#
	#print(fontinfo_json)
	#
#

