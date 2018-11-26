#
import os
import xml.etree.cElementTree as ET
import xml.dom.minidom as minidom
import json
#
from Lib.generic import generic_tools
#
def generate_lib(self):
	#
	print('EFO: Generating Lib')
	#
	glyphlist = []
	glyphorder = {"public.glyphOrder":[]}
	#
	UFO_lib_plist_file = os.path.join(self.current_font_instance_directory,'lib.plist')
	#
	xmlTree = ET.parse(os.path.join(self._in,'glyphlib.xml') )
	#
	for elem in xmlTree.iter():
		#
		if elem.tag == "glyph":
			#
			glyph_name = elem.attrib.get("name")
			#
			glyphlist.append(glyph_name)
			#
	#
	glyphorder["public.glyphOrder"] = glyphlist
	#
	lib_plist = generic_tools.json_to_plist(glyphorder)
	#
	generic_tools.write_to_file(UFO_lib_plist_file, lib_plist)
	#
	print('\tGenerated UFO Lib PLIST from glyphlib.xml: ',UFO_lib_plist_file)
	#