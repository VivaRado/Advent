# -*- coding: cp1252 -*-

import os, time

headerTemplate = '''%%!PS-Adobe-3.0 EPSF-3.0
%%%%Creator: %s
%%%%Title: %s
%%%%CreationDate: %s
%%%%BoundingBox: %s %s %s %s
%%%%EndComments'''

prolog = '''
%%BeginProlog
/FontLab 24 dict def FontLab begin
/Version 0 def
/bd {bind def} def
/n {newpath} bd
/c {curveto} bd
/C {curveto} bd
/L {lineto} bd
/l {lineto} bd
/m {moveto} bd
/f {closepath} bd
/S {} bd
/*u { } bd
/*U { fill} bd
/A {pop} bd
/O {pop} bd
/D {pop} bd
/g {setgray} bd
end
%%EndProlog'''

setup = '''
%%BeginSetup
FontLab begin
n
%%EndSetup
0 A  *u 0 O 0 g
0 D
'''

trailer = '''*U
%%PageTrailer
showpage
%%Trailer
end
%%EOF'''
#
nMOVE = 17
nCURVE = 35
nLINE = 1
#
def header(glyph, creator='', title=''):
	#
	c = creator or 'Eigi'
	t = title or 'Glyph %s' % glyph.name
	d = time.strftime('%a %b %d %m:%H:%M %Y')
	r = glyph.GetBoundingRect()
	#
	left = int(r.ll.x)
	bottom = int(r.ll.y)
	right = int(r.ur.x)
	top = int(r.ur.y)
	return headerTemplate % (c, t, d, r.ll.x, r.ll.y, r.ur.x, r.ur.y)

def glyph2ps(glyph):
	#
	result = ''
	first = True
	for node in glyph.nodes:
		
		_x = ((node.x + glyph.width) + node.x) - glyph.width
		_y = ((node.y + glyph.height) + node.y) - glyph.height
		
		if node.type == nMOVE:
			if not first:
				result += 'f\n'
			result += '%s %s m\n' %(_x, _y)
		elif node.type == nLINE:
			result += '%s %s l\n' %(_x, _y)
		elif node.type == nCURVE:
			p = node.points
			p_a_x = ((p[1].x + glyph.width) + p[1].x) - glyph.width
			p_b_x = ((p[2].x + glyph.width) + p[2].x) - glyph.width
			p_c_x = ((p[0].x + glyph.width) + p[0].x) - glyph.width
			#
			p_a_y = ((p[1].y + glyph.height) + p[1].y) - glyph.height
			p_b_y = ((p[2].y + glyph.height) + p[2].y) - glyph.height
			p_c_y = ((p[0].y + glyph.height) + p[0].y) - glyph.height
			#
			result += '%s %s %s %s %s %s c\n' %(p_a_x, p_a_y, p_b_x, p_b_y, p_c_x, p_c_y)
		first = False
	result += 'f\n0 0 m\nf\n'
	return result
	#
#
def glyph2eps(glyph, epsPath):
	#
	g_name = glyph.name
	g_index = str(glyph.index)
	if '.' in g_name:
		g_name = g_name.replace('.','--')
	print(epsPath+'\\'+g_index+'___'+g_name+'.eps')
	epsFile = file(epsPath+'\\'+g_index+'___'+g_name+'.eps', 'w')
	epsFile.write(header(glyph)+prolog+setup+glyph2ps(glyph)+trailer)
	#
	epsFile.close()
	#
#
def main():
	#
	outPath = fl.GetPathName("Choose folder with EPS files...")
	#
	for gs in fl.font.glyphs:
		#
		if gs is not None:
			#
			glyph2eps(gs, outPath)
			#
		else:
			#
			print 'No current glyph!'
			#
#
if __name__ == '__main__':
	main()
