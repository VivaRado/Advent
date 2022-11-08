import sys
from fontTools.ttLib import TTFont

font = TTFont(sys.argv[-1])
name = font["name"]


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


set_name(2, "Italic")
name.setName("Regular", 262, 3, 1, 1033)
name.setName("Regular", 262, 1, 0, 0)

for nameID in (3, 4, 6):
    set_name(nameID, get_name(nameID).replace("Regular", "Italic"))

stat = font["STAT"]
stat.table.AxisValueArray.AxisValue[3].ValueNameID = 262

font.save(sys.argv[-1])
