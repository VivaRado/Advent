import os
import time
#
#import Lib.generic.tab_completion
from Lib.efo import EFO
from Lib.similarity_extractor import SIMEX
from Lib.kerning import AUTOKERN
from Lib.compress_kerning import COMPRESS
from Lib.generic import generic_tools
#
from argparse import ArgumentParser
#
import json
#
parser = ArgumentParser()
parser.add_argument("-s", "--source", dest="source",
					help="Source EFO", metavar="FILE")
parser.add_argument("-f", "--fonts", dest="fonts", 
					help="UFO Fonts to Automatically Kern, comma separated")
# parser.add_argument("-c", "--compress_class_plist", dest="compress_class_plist", 
# 					help="Similarity Plist to Use for Compression to Class Based Kerning")
#
args = parser.parse_args()
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
	print('=\n=> Please Provide the Fonts to Compress: -f "thn,reg,bld"\n=')	
	#
#
# if  args.compress_class_plist is None:
# 	#
# 	faults = True
# 	#
# 	print('=\n=> Please Select to Compress to Class Based Kerning through Similarity Plist (Obtained by kerning_extract_similarity.py and stored in your EFO/groups): -c "Yes"/"No" \n=')
# 	#
#
new_class_fontinfo = [
    {
        "shared_info": {
            "familyName": ""
        }
    },
    {
        "font_files": []
    },
    {
        "font_info": []
    },
    {
        "font_kerning_settings": []
    }
]
#
if faults == False:
	#
	EFO_temp = os.path.join(args.source,"temp")
	#
	EFO = EFO(args.source,EFO_temp)
	#
	EFO._efo_to_ufos(args.fonts, True, "flat")
	#
	given_fonts = args.fonts.split('.')
	#
	source_efo_flat_kern_dir = os.path.join(EFO._in, "kerning/flat")
	source_efo_similarity_kern_plist = os.path.join(EFO._in, "groups/kerning.plist")
	#
	f_files_class = []
	#
	for x in EFO.all_exported_ufo_dst:
		#
		for k, v in x.items():
			#
			copy_ufo_for_class_compress = v.split('.ufo')[0]+'_class.ufo'
			#
			source_font_flat_kerning = os.path.join(source_efo_flat_kern_dir,k+'.plist')
			#
			generic_tools.copyDirectory(v, copy_ufo_for_class_compress)
			#
			f_files_class.append(k+'_class')
			#
			_COMPRESS = COMPRESS(k,v, copy_ufo_for_class_compress, source_efo_similarity_kern_plist)
			#
			_COMPRESS.do_class_kern_replacement()
			#
		#
	#
	new_class_fontinfo[0]["shared_info"]["familyName"] = EFO.current_font_family_name
	new_class_fontinfo[1]["font_files"] = f_files_class
	#
	print(new_class_fontinfo)
	#
	c_fontinfo_dir = os.path.join(*(EFO._in,"temp",EFO.current_font_family_name,"fontinfo.json"))
	#
	with open(c_fontinfo_dir, 'w') as outfile:
		#
		json.dump(new_class_fontinfo, outfile)
		#
	#
	#python3 '/media/root/Malysh1/winshm/advent_repo/Advent/_/VRD_Typography_Library/ufos_to_efo.py' -s '/media/root/Malysh1/winshm/advent_repo/Advent/_/font_efo.efo/fontinfo.json' -o '/media/root/Malysh1/winshm/advent_repo/Advent/_/font_efo.efo
	#
	print(c_fontinfo_dir,args.source)
	#
	c_source_ufo_family = os.path.join(*(EFO._in,"temp",EFO.current_font_family_name))
	#
	EFO._in = c_fontinfo_dir
	EFO._out = args.source
	EFO.current_source_ufo_family = c_source_ufo_family
	#
	#time.sleep(4)
	#
	EFO._ufos_to_efo(["kerning","features"], False, True)
	#
	#
#

