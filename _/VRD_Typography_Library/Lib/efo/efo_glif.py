#
import os
import xml.etree.cElementTree as ET
import xml.dom.minidom as minidom
import json
from distutils.dir_util import copy_tree
from shutil import copytree, ignore_patterns
#
from Lib.generic import generic_tools
#
def generate_contents_plist(self):
	#
	print('EFO: Generating UFO GLIF contents PLIST')
	#
	contents = {}
	#
	glyphs_directory = os.path.join(self.current_font_instance_directory,"glyphs")
	#
	generic_tools.make_dir(glyphs_directory)
	#
	UFO_contents_plist_file = os.path.join(glyphs_directory,'contents.plist')
	#
	xmlTree = ET.parse(os.path.join(self._in,'glyphlib.xml') )
	#
	for elem in xmlTree.iter():
		#
		if elem.tag == "glyph":
			#
			contents[elem.attrib.get("name")] = elem.attrib.get("glif")+'.glif'
			#
	#
	contents_plist = generic_tools.json_to_plist(contents)
	#
	generic_tools.write_to_file(UFO_contents_plist_file, contents_plist)
	#
	print('\tGenerated UFO contents PLIST from glyphlib.xml: ',UFO_contents_plist_file)
	#
#
#
def copy_glif_files(self, _stream):
	#
	if _stream == "Downstream":
		#
		print('EFO: Copying EFO GLIF Files to UFOs')
		#
		#
		EFO_glyphs_dir = os.path.join(self._in,self.EFO_glyphs_dir)
		#
		EFO_current_glyphs = os.path.join(EFO_glyphs_dir,self.current_font_file_name)
		UFO_glyphs_dir = os.path.join(self.current_font_instance_directory,'glyphs')
		#
		copy_tree(EFO_current_glyphs, UFO_glyphs_dir)
		#
		print('\tCopied GLIFS from EFO to UFO: ',UFO_glyphs_dir)
		#
	elif _stream == "Upstream":
		#
		#
		print('EFO: Copying UFO GLIF Files to EFO')
		#
		# Make Glyphs Directories
		current_glyphs_dir = os.path.join(*(self.new_efo_dir,self.EFO_glyphs_dir,self.current_font_file_name))
		generic_tools.make_dir(current_glyphs_dir)
		#
		if os.path.exists(os.path.dirname(current_glyphs_dir)):
			#
			generic_tools.rm_dir(current_glyphs_dir)
			#
		#
		copytree(self.current_source_ufo_glyphs_dir, current_glyphs_dir, ignore=ignore_patterns("*contents.plist", 'glyphs*'))
		#
	#