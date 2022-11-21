import sys
import math
from fontTools.ttLib import TTFont

font = TTFont(sys.argv[-1])
name = font["name"]

stat = font["STAT"]


def set_name(nameID, string):
    for record in name.names:
        if record.nameID == nameID:
            name.setName(
                string,
                record.nameID,
                record.platformID,
                record.platEncID,
                record.langID,
            )


def get_name(nameID):
    for record in name.names:
        if record.nameID == nameID:
            return record.toUnicode()


def get_axis(tag):
    for i, axis in enumerate(font["STAT"].table.DesignAxisRecord.Axis):
        if axis.AxisTag == tag:
            return i, axis


def get_axis_value(axisTag, name):
    for axisValue in stat.table.AxisValueArray.AxisValue:
        if (
            axisValue.AxisIndex == get_axis(axisTag)[0]
            and get_name(axisValue.ValueNameID) == name
        ):
            return axisValue


set_name(2, "Italic")
name.setName("Regular", 262, 3, 1, 1033)
name.setName("Regular", 262, 1, 0, 0)

for nameID in (3, 4, 6):
    set_name(nameID, get_name(nameID).replace("Regular", "Italic"))


get_axis_value("wght", "Italic").ValueNameID = 262

# Italic angle
post = font["post"]
post.italicAngle = -12
font["post"] = post

# Caret slope
hhea = font["hhea"]
hhea.caretSlopeRise = font["head"].unitsPerEm
hhea.caretSlopeRun = round(
    math.atan(math.radians(abs(post.italicAngle))) * font["head"].unitsPerEm
)
font["hhea"] = hhea

font["head"].macStyle |= 1 << 1

# Unset
for value in [0, 5, 6]:
    font["OS/2"].fsSelection &= ~(1 << value)
# Set Italic
font["OS/2"].fsSelection |= 1 << 0


font["STAT"] = stat
font.save(sys.argv[-1])
