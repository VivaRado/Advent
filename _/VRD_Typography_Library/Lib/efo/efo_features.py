#
import os
import glob
from pathlib import Path
import time
#
from Lib.generic import generic_tools
#
#
'''
order?!
	Languagesystems
	Classes
	feature Kerning
	# until here for now
	feature AlternativeFractions;
	feature ScientificInferiors;
	feature Subscript;
	feature Superscript;
	feature Ordinals;
	feature Denominators;
	feature Numerators;
	feature Fractions;
	feature AlternateAnnotationForms;
	feature OldStyleFigures;
	feature DiscretionaryLigatures;
	feature Ligatures;
	feature Ornaments;
	feature StylisticAlternates;
	feature TerminalForms;
	feature HistoricalLigatures;
	feature HistoricalForms;
'''
#
features_requested_order = ["language_systems.fea", "classes.fea", "kern_fea"] # and other features
features_start_end_name = ["Languagesystems", "Classes", "Kerning"] # and other features / for getting UFO features start line end line split to EFO features
#
flush_space = '                                                                   '
#
def combine_fea(self):
	#
	print('EFO: Combining FEA')
	#
	EFO_features_dir = os.path.join(self._in,self.EFO_features_dir)
	#
	all_fea = ''
	#
	features_list_dir = os.listdir(EFO_features_dir)
	#
	#print(features_list_dir)
	sorted_features_list_dir = sorted(features_list_dir, key=lambda x: features_requested_order.index(x), reverse=False)
	#
	x = 0
	#
	for file in sorted_features_list_dir:
		#
		current_FEA_file_dir = os.path.join(self.current_font_instance_directory,"features.fea")
		#
		if file.endswith(".fea"):
			#
			EFO_features_file = os.path.join(EFO_features_dir,file)
			#
			print('\tFOUND FEATURE: ', features_start_end_name[x])
			#
			with open(EFO_features_file, 'r') as fea_file:
				#
				data = fea_file.read()
				#
				all_fea = all_fea + '\n# '+features_start_end_name[x]+' Start\n' + data + '\n# '+features_start_end_name[x]+' End'+'\n'
				#
			#
		elif "kern_fea" in file:
			#
			current_EFO_kern_fea = os.path.join( *(EFO_features_dir, 'kern_fea', self.current_font_file_name+'.fea') )
			#
			print('\tFOUND KERN FEA: ', current_EFO_kern_fea)
			#
			with open(current_EFO_kern_fea, 'r') as kern_fea_file:
				#
				data = kern_fea_file.read()
				#
				all_fea = all_fea + '\n# '+features_start_end_name[x]+' Start\n' + data + '\n# '+features_start_end_name[x]+' End'+'\n'
				#
			#
		#
		UFO_fea_file = open(current_FEA_file_dir, "w")
		UFO_fea_file.write(all_fea)
		UFO_fea_file.close()
		#
		x = x + 1
#
def split_fea(self, _from_compress = False):
	#
	print('EFO: Splitting FEA')
	#
	print(">>>>>>", self.current_source_ufo)
	#
	UFO_fea_file = os.path.join(self.current_source_ufo, "features.fea")
	#
	result_fea = []
	#
	with open(UFO_fea_file, 'r') as f:
		#
		fea_data = f.read()
		#
		x = 0
		#
		for _fea in features_start_end_name:
			#
			data = '# '+_fea+' Start'+generic_tools.get_between('# '+_fea+' Start', '# '+_fea+' End', fea_data)+'# '+_fea+' End'
			#
			if features_requested_order[x] == "kern_fea":
				#
				if _from_compress:
					self.current_font_file_name = self.current_font_file_name.split('_class')[0]
				#
				current_features_file = os.path.join( *(self.current_source_efo_features_dir, features_requested_order[x], self.current_font_file_name+'.fea') )
				#
				print("Current Feature File: ", current_features_file)
				#
			else:
				#
				current_features_file = os.path.join(self.current_source_efo_features_dir, features_requested_order[x])
				#
			#
			#print('\r\t'+"Splitting UFO FEA: "+_fea+flush_space, end='')
			#
			#time.sleep(0.4)
			#
			generic_tools.write_to_file(current_features_file, data)
			#
			x = x + 1
			#
		#
		print('\n')
	#