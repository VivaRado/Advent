#
import os
from shutil import copyfile
#
from Lib.generic import generic_tools
#
def copy_kerning(self, kerning_type="class", _stream="Downstream"):
	#
	if _stream == "Downstream":
		#
		print('EFO: Copying Class Based Kerning')
		#
		EFO_kerning_dir = os.path.join(os.path.join(self._in,self.EFO_kerning_dir),kerning_type)
		#
		EFO_class_kerning_groups_file = os.path.join(EFO_kerning_dir,self.current_font_file_name+'.plist')
		UFO_class_kerning_groups_file = os.path.join(self.current_font_instance_directory,'kerning.plist')
		#
		copyfile(EFO_class_kerning_groups_file, UFO_class_kerning_groups_file)
		#
		print('\tCopied Kerning '+kerning_type+': ',UFO_class_kerning_groups_file)
		#
	else:
		# self.current_font_family_name, self.current_font_instance_name,
		kerning_dir = os.path.join(self.new_efo_dir, "kerning")
		kerning_dir_flat = os.path.join(kerning_dir,"flat")
		kerning_dir_class = os.path.join(kerning_dir,"class")
		#
		generic_tools.make_dir(kerning_dir)
		generic_tools.make_dir(kerning_dir_flat)
		generic_tools.make_dir(kerning_dir_class)
		#
		UFO_kerning_file = os.path.join(self.current_source_ufo, "kerning.plist")
		EFO_kerning_file = os.path.join( *(self.new_efo_dir, "kerning", kerning_type, self.current_font_file_name+".plist") ) 
		#
		copyfile(UFO_kerning_file, EFO_kerning_file)
		#print(self.current_source_ufo, efo_groups_file)
		#