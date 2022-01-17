from defcon import Font

from glob import glob



fonts = glob("advent_pro/*.ufo")

for font in fonts:
    f = Font(font)
    f.info.copyright = "Copyright 2011 The Advent Pro Project Authors (https://github.com/VivaRado/Advent)"
    f.info.openTypeNameLicense = "This Font Software is licensed under the SIL Open Font License, Version 1.1. This license is available with a FAQ at: https://scripts.sil.org/OFL"
    f.info.openTypeNameLicenseURL = "https://scripts.sil.org/OFL"
    f.save()
    