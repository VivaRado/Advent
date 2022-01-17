from defcon import Font

from glob import glob



fonts = glob("advent_pro/*.ufo")

for font in fonts:
    f = Font(font)
    f['uni00A0'].width = f['space'].width
    f.save()
#            print(font, f[glyph]transformation) 