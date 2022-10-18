from defcon import Font

from glob import glob


bad_glyphs = [
    'Gcommaaccent', 'Kcommaaccent', 'Lcommaaccent', 'Ncommaaccent', 'Omegatonos', 'Rcommaaccent', 'Scommaaccent', 'Tcedilla', 'V_alt', 'gcommaaccent', 'jcircumflex', 'kcommaaccent', 'lcommaaccent', 'mugreek', 'ncommaaccent', 'rcommaaccent', 'scommaaccent', 'tcedilla'
]

fonts = glob("advent_pro/*.ufo")

for font in fonts:
    f = Font(font)
    fixed = False
    for glyph in bad_glyphs:
        for comp in f[glyph].components:
#            print(comp.transformation)
            if comp.transformation[2] != 0:
                trans = list(comp.transformation)
                trans[2] = 0
                comp.transformation = tuple(trans)
                fixed = True
    if fixed:
        f.save()
#            print(font, f[glyph]transformation) 