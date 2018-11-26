#STAY
import json
import os
import sys
from os.path import dirname, join, abspath
import copy
#
#sys.path.insert(0, abspath(join(dirname("generic"), '..')))
#
from Lib.generic import generic_tools
#
#REMOVE
from pprint import pprint
#
def read_efo_json_fontinfo(self, _direction = "Downstream"):
	#
	print('EFO: Reading FontInfo JSON')
	#
	if _direction == "Downstream":
		#
		fontinfo_json = os.path.join(self._in,self.EFO_fontinfo)
		#
	else:
		#
		fontinfo_json = self._in
		#
	#
	with open(fontinfo_json) as f:
		#
		data = json.load(f)
		#
		print('\tRead FontInfo: ',fontinfo_json)
		#
		self.fontinfo = data
		#
	#
	get_shared_info(self)
	get_kerning_settings(self)
	#
#
def get_shared_info(self):
	#
	f_i = self.fontinfo
	#
	for data in f_i:
		#
		for key, value in data.items():
			#
			if key == "shared_info":
				#
				self.shared_info = value
				#
				self.current_font_family_name = generic_tools.sanitize_string(value["familyName"])
				#
			#
		#
	#
#
#
def get_kerning_settings(self):
	#
	f_i = self.fontinfo
	#
	for data in f_i:
		#
		for key, value in data.items():
			#
			if key == "font_kerning_settings":
				#
				self.kerning_settings = value
				#
			#
		#
	#
#
def get_font_info_for_weight(self, _type="plist"):
	#
	f_i = self.fontinfo
	#
	for data in f_i:
		#
		for key, value in data.items():
			#
			if key == "font_info":
				#
				for f_info in value:
					#pass
					#
					for k, v in f_info.items():
						#
						if k == self.current_font_file_name:
							#
							complete_font_info = generic_tools.merge_two_dicts(self.shared_info, v)
							#
							if _type == "plist":
								#
								return generic_tools.json_to_plist(complete_font_info)
								#
							else:
								#
								return complete_font_info
								#
							#
						#
					#
				#
			#
		#
	#
def get_font_file_array(self):
	#
	f_i = self.fontinfo
	#
	for data in f_i:
		#
		for key, value in data.items():
			#
			if key == "font_files":
				#
				return value
				#
			#
		#
	#
#
def generate_fontinfo(self):
	#
	print('EFO: Generating FontInfo')
	#
	# print(self._out)
	# print(self.current_font_file_name)
	# print(self.current_fontinfo)
	# print(self.current_font_family_name)
	# print(self.current_font_family_directory)
	# print(self.current_font_instance_name)
	# print(self.current_font_instance_directory)
	#
	#
	UFO_fontinfo_plist_file = os.path.join(self.current_font_instance_directory,'fontinfo.plist')
	#
	generic_tools.write_to_file(UFO_fontinfo_plist_file,self.current_fontinfo)
	#
	print('\tGenerated FontInfo: ',UFO_fontinfo_plist_file)
	#print(UFO_fontinfo_plist_file)
	#
#
shared_info_list = ["familyName",
"openTypeNameDesigner",
"openTypeNameDesignerURL",
"openTypeNameLicense",
"openTypeNameLicenseURL",
"openTypeNameManufacturer",
"openTypeNameManufacturerURL",
"openTypeNameDescription",
"openTypeNameSampleText",
"openTypeNameUniqueID",
"openTypeNameVersion",
"styleMapFamilyName",
"trademark",
"versionMajor",
"versionMinor",
"year",
"openTypeHeadCreated",
"macintoshFONDFamilyID"]
#
default_kerning_settings = {
	"--min-distance-ems":0.04,
	"--max-distance-ems":0.05,
	"--max-x-extrema-overlap-ems":0.1,
	"--intrusion-tolerance-ems":0.02,
	"--precision-ems":0.005
}
#
def update_font_info(self, _fdata, _f):
	#
	print('EFO: Updating FontInfo From UFOs')
	#
	self.current_source_ufo_fontinfo = os.path.join(self.current_source_ufo,'fontinfo.plist')
	#
	UFO_fontinfo_plist_file = os.path.join(self.current_source_ufo,'fontinfo.plist')
	#
	fontinfo_json = generic_tools.plist_to_json(UFO_fontinfo_plist_file)
	#
	x = 0
	#
	non_shared = {}
	#
	for z in _fdata:
		#
		for k,v in z.items():
			#
			if k == "shared_info":
				#
				for y in fontinfo_json:
					#
					if y in shared_info_list:
						#
						_fdata[x]["shared_info"][y] = fontinfo_json[y]
						#
					else:
						#
						non_shared[y] = fontinfo_json[y]
						#
			if k == "font_info":
				#
				for ke, va in _fdata[x].items():
					#
					f_keys_fontinfo = set().union(*(d.keys() for d in va))
					#
					if _f not in f_keys_fontinfo:
						#
						va.append({_f:non_shared})
						#
					#
				#
			if k == "font_kerning_settings":
				#
				for ke, va in _fdata[x].items():
					#
					f_keys_fontinfo = set().union(*(d.keys() for d in va))
					#
					if _f not in f_keys_fontinfo:
						#
						va.append({_f:default_kerning_settings})
						#
					#
				#
		x = x + 1
		#
	#
#