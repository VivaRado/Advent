#
import os
from shutil import copyfile
#
def copy_metainfo(self, _stream="Downstream"):
	#
	if _stream == "Downstream":
		#
		print('EFO: Copying MetaInfo')
		#
		EFO_metainfo_file = os.path.join(self._in,'metainfo.plist')
		UFO_metainfo_file = os.path.join(self.current_font_instance_directory,'metainfo.plist')
		#
		copyfile(EFO_metainfo_file, UFO_metainfo_file)
		#
		print('\tCopied metainfo PLIST: ',UFO_metainfo_file)
		#
	else:
		#
		UFO_metainfo_file = os.path.join(self.current_source_ufo, "metainfo.plist")
		EFO_metainfo_file = os.path.join(self.new_efo_dir, "metainfo.plist") 
		#
		copyfile(UFO_metainfo_file, EFO_metainfo_file)
		#
		#