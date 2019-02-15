fontmake -o variable -g AdventPro.glyphs

rm -rf master_ufo
rm -rf instance_ufo

cd variable_ttf

gftools fix-nonhinting AdventPro-VF.ttf AdventPro-VF.ttf
gftools fix-dsig --autofix AdventPro-VF.ttf
gftools fix-gasp AdventPro-VF.ttf

ttx AdventPro-VF.ttf

rm -rf AdventPro-VF.ttf
rm -rf AdventPro-VF-backup-fonttools-prep-gasp.ttf

cd ..

cat variable_ttf/AdventPro-VF.ttx | tr '\n' '\r' | sed -e "s,<STAT>.*<\/fvar>,$(cat tools/patch.xml | tr '\n' '\r')," | tr '\r' '\n' > AdventPro-VF.ttx

rm -rf variable_ttf

ttx AdventPro-VF.ttx

rm -rf AdventPro-VF.ttx