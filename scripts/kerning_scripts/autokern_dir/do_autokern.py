import glob
import os
#
from Autokern import Autokern
from AutokernSettings import AutokernSettings
import tfs.common.TFSProject as TFSProject
from tfs.common.TFSMap import TFSMap
#
PIDDIR="/media/root/Malysh1/winshm/all_advent/Advent_Pro_Local_Copy/new_advent/KERN/charlesmchen-typefacet-8c6db26/python/src-main-reord/Autokern.py"
_dir = '/media/root/Malysh1/_code/advent_variable/variable_fonts_test/procedure_fonts/thn_reg/varfontfiles/sources_ufo/'

#
fontfilename = "adventprofmm"
#
#weights=["thn","thn_it","reg","reg_it","bld","bld_it"]
weights=["thn_it","reg_it","bld_it"]
#
x = 0
#
for w in weights:	
	#
	print("________________________")
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
					'0.04',
					'--precision-ems',
					'0.005'
	               )

	print ('pseudo_argv', ' '.join([str(arg) for arg in pseudo_argv]))

	autokernArgs = TFSMap()
	AutokernSettings(autokernArgs).getCommandLineSettings(*pseudo_argv)
	autokern = Autokern(autokernArgs)
	autokern.process()
	#
	x = x + 1
	#
	print ('Completed:'+w+' '+str(x)+'/'+str(len(weights)))
	#

	#italics
	'''pseudo_argv = ('--ufo-src-path',
					in_fnt,
					'--ufo-dst-path',
					out_fnt,
					'--min-distance-ems',
					'0.08',
					'--max-distance-ems',
					'0.09',
					'--max-x-extrema-overlap-ems',
					'0.4',
					'--intrusion-tolerance-ems',
					'0.08',#for reg'0.04',
					'--precision-ems',
					'0.005'
	               )'''
	#
	# reg
	'''
	('--ufo-src-path',
					in_fnt,
					'--ufo-dst-path',
					out_fnt,
					'--min-distance-ems',
					'0.04',
					'--max-distance-ems',
					'0.05',
					'--max-x-extrema-overlap-ems',
					'0.2',
					'--intrusion-tolerance-ems',
					'0.04',
					'--precision-ems',
					'0.005'
	               )
	               '''