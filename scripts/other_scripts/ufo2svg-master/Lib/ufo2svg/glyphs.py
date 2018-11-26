from __future__ import absolute_import
from fontTools.misc.py23 import *

from xml.etree.ElementTree import Element
from xml.etree import ElementTree
from .svgPathPen import SVGPathPen
from .tools import valueToString

def writeGlyphPath(glyph):
    svgGlyphAttrib = {}
    _writeGlyphName(glyph, svgGlyphAttrib)
    #_writeHorizAdvX(glyph, svgGlyphAttrib)
    _writeUnicode(glyph, svgGlyphAttrib)
    _writeD(glyph, svgGlyphAttrib)
    svgGlyph = Element("path", attrib=svgGlyphAttrib)

    #xml_str = ElementTree.tostring(svgGlyph).decode()

    print(ElementTree.tostring(svgGlyph, method='xml'))

    #svgFont.append(svgGlyph)

    return svgGlyph


def _writeDefaultMissingGlyphAttrib(font):

    if font.info.postscriptDefaultWidthX is not None:
        width = font.info.postscriptDefaultWidthX
    elif not font.info.unitsPerEm:
        width = 500
    else:
        width = int(font.info.unitsPerEm * .5)
    return {"horiz-adv-x" : valueToString(width)}

def _writeGlyphName(glyph, attrib):

    assert glyph.name is not None
    attrib["glyph-name"] = glyph.name

def _writeHorizAdvX(glyph, attrib):

    assert glyph.width >= 0
    attrib["horiz-adv-x"] = valueToString(glyph.width)

def _writeUnicode(glyph, attrib):

    if glyph.unicode:
        attrib["unicode"] = unichr(glyph.unicode)

def _writeD(glyph, attrib):

    pen = SVGPathPen(glyph.getParent())
    glyph.draw(pen)
    pathCommands = pen.getCommands()
    if pathCommands:
        attrib["d"] = pathCommands

if __name__ == "__main__":
    import doctest
    doctest.testmod()