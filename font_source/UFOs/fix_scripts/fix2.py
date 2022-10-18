from defcon import Font

from glob import glob
import os
import shutil

fonts = glob("advent_pro/*.ufo")

for font in fonts:
    f = Font(font)
    f.info.copyright = "Copyright (c) VivaRado, Andreas Kalpakidis (support@vivarado.com) and Advent Pro Project Authors to the extent of their contribution (https://github.com/VivaRado/Advent)"
    f.info.openTypeNameLicense = "This Font Software is licensed under the SIL Open Font License, Version 1.1. This license is available with a FAQ at: https://scripts.sil.org/OFL"
    f.info.openTypeNameLicenseURL = "https://scripts.sil.org/OFL"
    f.info.openTypeNameVersion = "Version 2.0"
    f.info.openTypeOS2Type = [0]

    f.save()