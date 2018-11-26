from fontParts.world import *
from TFSFont import *
from TFSSvg import *
#
from PIL import Image
import cairosvg
#
from .simex_slicer import *
#
def render_glyph(contours, ufoglyph):
		
	LETTER_COLOR = 0x90000000
	CANVAS_BACKGROUND_COLOR = 0xffffffff
	#

	#
	def subrenderGlyphContours( tfsSvg, contours):
		#
		paths_in = []
		paths_out = []
		#
		x = 0
		for contour in contours:
			#
			if isClosedPathClockwise(contour):
				paths_in.append(contour)
			else:
				paths_out.append(contour)
			#
		#
		svgPath_out = TFSSvgPath(contours[0])
		svgPath_out.fillColor = LETTER_COLOR
		tfsSvg.addItem(svgPath_out)
		#
		for path_in in paths_in:
			
			svgPath_in = TFSSvgPath(path_in)
			svgPath_in.fillColor = CANVAS_BACKGROUND_COLOR
			tfsSvg.addItem(svgPath_in)
	#
	#
	tfsSvg = TFSSvg().withBackground(CANVAS_BACKGROUND_COLOR)#.withBorder(CANVAS_BORDER_COLOR)
	#
	subrenderGlyphContours(tfsSvg, contours)
	#
	filename = '%s.svg' % ( ufoglyph.name, )
	filename_png = '%s.png' % ( ufoglyph.name, )
	dstFile = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)),os.path.join('svg_loc', filename)))
	dstlocpng = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)),'svg_loc'))
	dstFilepng = os.path.abspath(os.path.join(dstlocpng, filename_png ))

	svgdata = tfsSvg.renderToFile(None,
								  margin=10,
								  timing=None,
								  #width=width, height=height, 
								  maxWidth = 700,
								  maxHeight = 250,
								  #maxWidth=maxWidth, maxHeight=maxHeight,
								  padding=None)
	
	#svgdata = svgdata.replace('fill="none"', 'fill="black"')
	svgdata = svgdata.replace('fill-opacity="0.565"', 'fill-opacity="1"')
	#svgdata = svgdata.replace('fill="rgb(0,0,0)" ', 'fill="rgb(255,255,255)" ')
	#print(svgdata)
	#
	with open(dstFile, 'w') as the_file:
		the_file.write(svgdata)
		the_file.close()
		#
	tempobject = svgwrite.Drawing(svgdata, profile='tiny', width=700, height=250)
	#
	cairosvg.svg2png(url=dstFile, write_to=dstFilepng)
	#
	raster_data = matrix_slice(dstFilepng, dstlocpng, ufoglyph.name)
	#
	os.remove(dstFile)
	#os.remove(dstFilepng)
	#
	return raster_data
	#