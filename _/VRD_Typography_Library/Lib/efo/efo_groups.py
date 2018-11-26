#
import os
from shutil import copyfile
#
from Lib.generic import generic_tools
#
def copy_groups_class_kerning(self, _stream = "Downstream"):
	#
	if _stream == "Downstream":
		#
		print('EFO: Copying Kerning Class Groups')
		#
		EFO_groups_dir = os.path.join(self._in,self.EFO_groups_dir)
		EFO_class_kerning_groups_file = os.path.join(EFO_groups_dir,'kerning.plist')
		UFO_class_kerning_groups_file = os.path.join(self.current_font_instance_directory,'groups.plist')
		#
		copyfile(EFO_class_kerning_groups_file, UFO_class_kerning_groups_file)
		#
		print('\tCopied Kerning Class Groups: ',UFO_class_kerning_groups_file)
	else:
		#
		groups_dir = os.path.join(*(self.new_efo_dir, self.EFO_groups_dir))
		#
		generic_tools.make_dir(groups_dir)
		#
		UFO_class_kerning_groups_file = os.path.join(self.current_source_ufo, "groups.plist")
		EFO_class_kerning_groups_file = os.path.join( *(self.new_efo_dir, self.EFO_groups_dir, "kerning.plist") ) 
		#
		copyfile(UFO_class_kerning_groups_file, EFO_class_kerning_groups_file)
		#

def remove_groups_class_kerning(self):
	#
	print('EFO: Copying Kerning Class Groups')
	#
	UFO_class_kerning_groups_file = os.path.join(self.current_font_instance_directory,'groups.plist')
	#
	try:
		os.remove(UFO_class_kerning_groups_file)
		#
		print('\tRemoved Kerning Class Groups: ',UFO_class_kerning_groups_file)
		#
	except OSError:
		#
		print('\tNo Kerning Class Groups File Found to Remove: ',UFO_class_kerning_groups_file)
		#
	#