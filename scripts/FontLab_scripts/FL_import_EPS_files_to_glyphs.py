#FLM: Import EPS glyphs from folder
import os.path, glob
f = fl.font
#
folder = fl.GetPathName("Choose folder with EPS files...")
pathmask = "*.eps"
paths = []

for filename in sorted(glob.glob(os.path.join(folder, pathmask))):
	#
	print "Importing EPS files from %s..." % (folder)
	#for path in paths:
	basename = os.path.splitext(os.path.split(filename)[1])[0]
	try:
		g = Glyph()
		g = g.LoadEPS(filename)
		#
		g.SelectAll()
		#
		g_split = basename.split('__')
		#
		glyphName = g_split[0].replace('-','.')
		g.name = glyphName
		unisplit = g_split[1].split('~')
		g.unicodes = [int("0x"+unisplit[0], 16)]
		g.mark = 33
		g.width = int(unisplit[1])
		
		f.glyphs.append(g)
		
		print "%s.eps imported" % (basename)
	except:
		print "%s.eps IGNORED" % (basename)
		fl.UpdateFont(fl.ifont)

print "Finished."

#
f.DefineAxis("Weight", "Wt", "Weight")
#