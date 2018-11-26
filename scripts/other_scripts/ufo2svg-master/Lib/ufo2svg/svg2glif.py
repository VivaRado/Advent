#!/usr/bin/env python
""" Convert SVG paths to UFO glyphs.
"""
# Author: Cosimo Lupo
# Email: cosimo@anthrotype.com
# License: Apache Software License 2.0

from __future__ import print_function, absolute_import

__requires__ = ["svg.path", "ufoLib", "FontTools"]

try:
    from xml.etree import cElementTree as ElementTree  # python 2
except ImportError:
    from xml.etree import ElementTree  # python 3

from svg.path import parse_path, Line, CubicBezier, QuadraticBezier

from fontTools.pens.transformPen import TransformPen

from ufoLib.pointPen import SegmentToPointPen
from ufoLib.glifLib import writeGlyphToString


__version__ = "0.1.0"
__all__ = ["svg2glif", "SVGOutline"]


def svg2glif(svg, name, width=0, height=0, unicodes=None, transform=None,
             version=2):
    """ Convert an SVG outline to a UFO glyph, and assign the given 'name',
    advance 'width' and 'height' (int), 'unicodes' (list of int) to the
    generated glyph.
    Return the resulting string in GLIF format (default: version 2).
    If 'transform' is provided, apply a transformation matrix before the
    conversion (must be tuple of 6 floats, or a FontTools Transform object).
    """
    glyph = SVGOutline.fromstring(svg, transform=transform)
    glyph.name = name
    glyph.width = width
    glyph.height = height
    glyph.unicodes = unicodes or []
    return writeGlyphToString(glyph.name,
                              glyphObject=glyph,
                              drawPointsFunc=glyph.drawPoints,
                              formatVersion=version)


class SVGOutline(object):
    """ Parse SVG ``path`` elements from a file or string, and draw them
    onto a glyph object that supports the FontTools Pen protocol, or
    the ufoLib (ex RoboFab) PointPen protocol.

    For example, using a Defcon Glyph:

        import defcon

        glyph = defcon.Glyph()
        pen = glyph.getPen()
        svg = SVGOutline("path/to/a/glyph.svg")
        svg.draw(pen)

        pen = glyph.getPointPen()
        svg = SVGOutline.fromstring('<?xml version="1.0" ...')
        svg.drawPoints(pen)

    The constructor can optionally take a 'transform' matrix (6-float tuple,
    or FontTools Transform object).
    """

    def __init__(self, filename=None, transform=None):
        if filename:
            tree = ElementTree.parse(filename)
            root = tree.getroot()
            self.paths = self.parse_paths(root)
        else:
            self.paths = []
        self.transform = transform

    @classmethod
    def fromstring(cls, data, transform=None):
        self = cls(transform=transform)
        root = ElementTree.fromstring(data)
        self.paths = cls.parse_paths(root)
        return self

    @staticmethod
    def parse_paths(root):
        paths = []
        for el in root.findall(".//{http://www.w3.org/2000/svg}path[@d]"):
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


def parse_args(args):
    import argparse

    def split(arg):
        return arg.replace(",", " ").split()

    def unicode_hex_list(arg):
        try:
            return [int(unihex, 16) for unihex in split(arg)]
        except ValueError:
            msg = "Invalid unicode hexadecimal value: %r" % arg
            raise argparse.ArgumentTypeError(msg)

    def transform_list(arg):
        try:
            return [float(n) for n in split(arg)]
        except ValueError:
            msg = "Invalid transformation matrix: %r" % arg
            raise argparse.ArgumentTypeError(msg)

    parser = argparse.ArgumentParser(
        description="Convert SVG outlines to UFO glyphs (.glif)")
    parser.add_argument(
        "infile", metavar="INPUT.svg", help="Input SVG file containing "
        '<path> elements with "d" attributes.')
    parser.add_argument(
        "outfile", metavar="OUTPUT.glif", help="Output GLIF file (default: "
        "print to stdout)", nargs='?')
    parser.add_argument(
        "-n", "--name", help="The glyph name (default: input SVG file "
        "basename, without the .svg extension)")
    parser.add_argument(
        "-w", "--width", help="The glyph advance width (default: 0)",
        type=int, default=0)
    parser.add_argument(
        "-H", "--height", help="The glyph vertical advance (optional if "
        '"width" is defined)', type=int, default=0)
    parser.add_argument(
        "-u", "--unicodes", help="List of Unicode code points as hexadecimal "
        'numbers (e.g. -u "0041 0042")',
        type=unicode_hex_list)
    parser.add_argument(
        "-t", "--transform", help="Transformation matrix as a list of six "
        'float values (e.g. -t "0.1 0 0 -0.1 -50 200")', type=transform_list)
    parser.add_argument(
        "-f", "--format", help="UFO GLIF format version (default: 2)",
        type=int, choices=(1, 2), default=2)
    parser.add_argument('--version', action='version', version=__version__)

    return parser.parse_args(args)


def main(args=None):
    from io import open

    options = parse_args(args)

    svg_file = options.infile

    if options.name:
        name = options.name
    else:
        import os
        name = os.path.splitext(os.path.basename(svg_file))[0]

    with open(svg_file, "r", encoding="utf-8") as f:
        svg = f.read()

    glif = svg2glif(svg, name,
                    width=options.width,
                    height=options.height,
                    unicodes=options.unicodes,
                    transform=options.transform,
                    version=options.format)

    if options.outfile is None:
        print(glif)
    else:
        with open(options.outfile, 'w', encoding='utf-8') as f:
            f.write(glif)


if __name__ == "__main__":
    main()
