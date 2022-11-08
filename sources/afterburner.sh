rm fonts/variable/split/*.ttf
set -e
fonttools varLib.instancer -o "fonts/variable/split/AdventPro[wdth,wght].ttf" "fonts/variable/AdventPro[ital,wdth,wght].ttf" ital=0
fonttools varLib.instancer -o "fonts/variable/split/AdventPro-Italic[wdth,wght].ttf" "fonts/variable/AdventPro[ital,wdth,wght].ttf" ital=1
python3 sources/afterburner.py fonts/variable/split/AdventPro-Italic[wdth,wght].ttf