#!/usr/bin/env python
""" Convert SVG paths to UFO glyphs.
"""
# Author: Cosimo Lupo / Vivarado
# Email: cosimo@anthrotype.com, support@vivarado.com
# License: Apache Software License 2.0

from __future__ import print_function, absolute_import

__requires__ = ["svg.path", "ufoLib", "FontTools"]

import io
import xml.etree.ElementTree as ET

from svg.path import parse_path, Line, CubicBezier, QuadraticBezier

from fontTools.pens.transformPen import TransformPen

from ufoLib.pointPen import SegmentToPointPen
from ufoLib.glifLib import writeGlyphToString

from .simple_path import *

#from .tools import *

__version__ = "0.1.0"
__all__ = ["svg2glif", "SVGOutline"]

def get_additional_info_from_path_id(svg):
	#
	root = ET.fromstring(svg)
	paths = []
	for el in root.findall(".//{http://www.w3.org/2000/svg}path[@d]"):
		_id = el.get("id")
		paths.append(_id)
	#
	if len(paths):
		return paths[0].split('__')
	else:
		return "NONE"

def svg2glif(svg, name, width=0, height=0, unicodes=None, transform=None,
			 version=1):
	""" Convert an SVG outline to a UFO glyph, and assign the given 'name',
	advance 'width' and 'height' (int), 'unicodes' (list of int) to the
	generated glyph.
	Return the resulting string in GLIF format (default: version 2).
	If 'transform' is provided, apply a transformation matrix before the
	conversion (must be tuple of 6 floats, or a FontTools Transform object).
	"""
		
	add_info = get_additional_info_from_path_id(svg)

	glyph = SVGOutline.fromstring(svg, transform=transform)
	glyph.name = add_info[0]
	glyph.width = width
	glyph.height = height
	glyph.unicodes = unicodes or []
	#
	glif_string = writeGlyphToString(glyph.name,
							  glyphObject=glyph,
							  drawPointsFunc=glyph.drawPoints,
							  formatVersion=version)
	#
	if add_info != "NONE":
		#
		tree = ET.fromstring(glif_string)
		#
		_adv = ET.Element("advance", width=add_info[2])
		tree.insert(0,_adv)
		#
		if add_info[1] != "NONE":
			_uni = ET.Element("unicode", hex=add_info[1])
			tree.insert(1,_uni)
		#
		xmlstr = ET.tostring(tree, encoding='utf8', method='xml').decode("utf-8")
		#
	else:
		#
		xmlstr = glif_string
		#
	return xmlstr

class SVGOutline(object):

	def __init__(self, filename=None, transform=None):
		if filename:
			tree = ET.parse(filename)
			root = tree.getroot()
			self.paths = self.parse_paths(root)
		else:
			self.paths = []
		self.transform = transform

	@classmethod
	def fromstring(cls, data, transform=None):
		self = cls(transform=transform)
		root = ET.fromstring(data)
		self.paths = cls.parse_paths(root)
		return self

	@staticmethod
	def parse_paths(root):
		paths = []
		for el in root.findall(".//{http://www.w3.org/2000/svg}path[@d]"):
			if el.get("d") != "Z":
				path = parse_path(el.get("d"))
				paths.append(path)

		return paths

	def draw(self, pen):
		if self.transform:
			pen = TransformPen(pen, self.transform)
		for path in self.paths:
			current_pos = None
			for s in path:
				if current_pos != s.start:
					if current_pos is not None:
						pen.closePath()
					pen.moveTo((s.start.real, s.start.imag))
				if isinstance(s, Line):
					pen.lineTo((s.end.real, s.end.imag))
				elif isinstance(s, CubicBezier):
					pen.curveTo(
						(s.control1.real, s.control1.imag),
						(s.control2.real, s.control2.imag),
						(s.end.real, s.end.imag))
				elif isinstance(s, QuadraticBezier):
					pen.qCurveTo(
						(s.control.real, s.control.imag),
						(s.end.real, s.end.imag))
				#else:
					# TODO convert Arc segments to bezier?
					#raise NotImplementedError(s)
				current_pos = s.end
			pen.closePath()

	def drawPoints(self, pointPen):
		pen = SegmentToPointPen(pointPen)
		self.draw(pen)
