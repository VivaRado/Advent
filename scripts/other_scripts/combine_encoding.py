import os


dirpath = os.path.dirname(os.path.realpath(__file__))+'/'+'encoding_files_serial'+'/'
#
filelist = sorted(os.listdir(dirpath))
#
#
all_encs = []
#
#
for filename in filelist:
	#
	all_glyphs = []
	#
	if filename.endswith(".enc"):  
		with open(dirpath + filename, 'r') as f:
			#
			print('______________'+filename)
			#
			for line in f:
				#
				if line.startswith("%%FONTLAB"):
					pass
				else:
					# #
					uni_name = line.split()[0]
					#
					all_glyphs.append(uni_name)
					#
	#
	all_encs.append(all_glyphs)
	#
	print(filename)
	print(all_glyphs)
	print('#############################')
#
#
seen = []
repeated = []
new_all_encs=[]
w = 0
for l in all_encs:

	t_new_all_enc = []
	#

	for i in l:
		if i in seen:
			repeated.append(i)
		else:
			seen.append(i)
			t_new_all_enc.append(i)

	new_all_encs.append(t_new_all_enc)
	print(w)
	#
	w = w + 1
# 
t_seen = seen

print('________==========__________')
print(new_all_encs)
#
t_seen_unique = []
#
all_clean = []
#
xx = 0
for x_all in all_encs:
	#
	t_clean = []
	#
	for x_a in x_all:
		#
		#print(x_a)
		#
			#
		if x_a in t_seen_unique:
			#
			pass
			#
		else:
			#
			t_seen_unique.append(x_a)
			#
			if x_a in t_seen:
				
				t_clean.append(x_a)
			

	all_clean.append(t_clean)

print('DONE__________________________________')
print(len(seen))
