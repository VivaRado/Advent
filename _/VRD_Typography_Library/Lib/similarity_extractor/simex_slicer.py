import os
from PIL import Image
import cairosvg

from math import sqrt, ceil, floor
#
import difflib

def get_black_level(img):
	pixels = img.getdata()
	black_thresh = 50
	nblack = 0
	for pixel in pixels:
		if sum(pixel) < black_thresh:
			nblack += 1
	n = len(pixels)

	return nblack / float(n)
#
class Tile(object):

	def __init__(self, image, number, position, coords, filename=None):
		self.image = image
		self.number = number
		self.position = position
		self.coords = coords
		#self.filename = filename

	@property
	def row(self):
		return self.position[0]

	@property
	def column(self):
		return self.position[1]
	
	def save(self, filename=None, format='png'):
		
		self.image.save(filename, format)
		self.filename = filename


def calc_columns_rows(n):

	num_rows = int(floor(sqrt(n)))
	num_columns = int(floor(n / float(num_rows)))
	return (num_rows, num_columns)

def matrix_slice(image_path, outdir, out_name):
	#
	im = Image.open(image_path)
	#
	slices = 16
	#
	im_w, im_h = im.size
	columns, rows = calc_columns_rows(slices)
	extras = (columns * rows) - slices
	tile_w, tile_h = int(floor(im_w / columns)), int(floor(im_h / rows))
	#
	tiles = []
	number = 1
	#
	for pos_y in range(0, im_h - rows, tile_h): # -rows for rounding error.
		#
		for pos_x in range(0, im_w - columns, tile_w): # as above.
			#
			area = (pos_x, pos_y, pos_x + tile_w, pos_y + tile_h)
			image = im.crop(area)
			#
			position = (int(floor(pos_x / tile_w)) + 1,
						int(floor(pos_y / tile_h)) + 1)
			#
			coords = (pos_x, pos_y)
			tile = Tile(image, number, position, coords)
			tiles.append(tile)
			number += 1
			#
		#
	#
	count = 0
	color_matrix = []
	#
	for x in tiles:
		#
		img_dir = os.path.join(outdir, "slice_"+ out_name +'_'+ str(count) +".png")
		x.save(img_dir)
		#
		contrast_lvl = round(get_black_level(x.image),4)
		color_matrix.append(contrast_lvl)

		os.remove(img_dir)
		
		#
		count = count + 1 
		#
	#
	#
	
	return color_matrix
#
#