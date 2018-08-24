#FLM: Import EPS glyphs from folder
import os.path, glob
import fl_cmd
f = fl.font
#
folder = fl.GetPathName("Choose folder with EPS files...")
pathmask = "*.eps"
paths = []
#
target_glyph = None
#
if(f.FindGlyph("ZERO") == -1):
	g = Glyph()
	glyphName = "ZERO" #g_split[0]
	g.name = glyphName
	f.glyphs.append(g)
	#

#pass
zero_index = 0
z = 0
#
#
for gs in f.glyphs:
	#
	if ( gs.name == "ZERO"):
		#
		zero_index = z
		print( gs.name )
		target_glyph = f.glyphs[zero_index]
		#
		break
	else:
		#
		z = z + 1
		#
	#
#
print(target_glyph)
#
xx = 0
#
for filename in sorted(glob.glob(os.path.join(folder, pathmask))):
	#
	print "Importing EPS files from %s..." % (folder)
	#for path in paths:
	basename = os.path.splitext(os.path.split(filename)[1])[0]
	try:
		g = target_glyph
		#
		g = g.LoadEPS(filename)
		#
		g_split = basename.split('__')
		glyphName = "ZERO"+g_split[0]
		g.name = glyphName
		#
		g_index = xx+zero_index+1
		#
		f.glyphs.append(g)
		#
		fl.EditGlyph(g_index)
		fl.CallCommand(32873)#select all
		fl.CallCommand(57634)#copy
		#
		fl.EditGlyph(zero_index)
		fl.CallCommand(32873)#select all
		fl.CallCommand(32871)#delete
		fl.CallCommand(57637)#paste
		#
		fl.EditGlyph(f.FindGlyph(g_split[0]))
		fl.CallCommand(57637)#paste
		fl.CallCommand(fl_cmd.MaskCopy)
		fl.CallCommand(32871)#delete
		fl.CallCommand(33146)
		#
		print(target_glyph)
		#
		fl.EditGlyph(g_index)
		fl.CallCommand(32873)#select all
		fl.CallCommand(32871)#delete
		fl.Close(g_index)
		f.glyphs[g_index].name = "DELETE"
		#
		print "%s.eps imported" % (basename)
	except:
		print "%s.eps IGNORED" % (basename)
		fl.UpdateFont(fl.ifont)
	xx = xx + 1
fl.CallCommand(33490)
#fl.CallCommand(32946)
fl.CallCommand(32885)
print "Finished."

