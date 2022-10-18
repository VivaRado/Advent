#!/bin/bash

# These versions where used:
# fonttools==4.0.0
# cu2qu==1.6.6
# ufo2ft==2.9.0
# defcon==0.6.0

#definitive
fontmake -o variable -m "`dirname "$0"`/UFOs/adv_wght_wdth_ital.designspace" --output-path "`dirname "$0"`/VAR/adventpro-def-VF.ttf" #--verbose="DEBUG"

#active
fontmake -o variable -m "`dirname "$0"`/UFOs/adv_wght.designspace" --output-path "`dirname "$0"`/VAR/adventpro-wght-VF.ttf" #--verbose="DEBUG"
fontmake -o variable -m "`dirname "$0"`/UFOs/adv_wght_wdth.designspace" --output-path "`dirname "$0"`/VAR/adventpro-wght-wdth-VF.ttf" #--verbose="DEBUG"
fontmake -o variable -m "`dirname "$0"`/UFOs/adv_wght_ital.designspace" --output-path "`dirname "$0"`/VAR/adventpro-wght-ital-VF.ttf" #--verbose="DEBUG"

#preset
fontmake -o variable -m "`dirname "$0"`/UFOs/adv_wght_preital.designspace" --output-path "`dirname "$0"`/VAR/adventpro-wght-preital-VF.ttf" #--verbose="DEBUG"
fontmake -o variable -m "`dirname "$0"`/UFOs/adv_wght_prewdth.designspace" --output-path "`dirname "$0"`/VAR/adventpro-wght-prewdth-VF.ttf" #--verbose="DEBUG"
fontmake -o variable -m "`dirname "$0"`/UFOs/adv_wght_prewdth_preital.designspace" --output-path "`dirname "$0"`/VAR/adventpro-wght-prewdth-preital-VF.ttf" #--verbose="DEBUG"
fontmake -o variable -m "`dirname "$0"`/UFOs/adv_wght_wdth_preital.designspace" --output-path "`dirname "$0"`/VAR/adventpro-wght-wdth-preital-VF.ttf" #--verbose="DEBUG"
fontmake -o variable -m "`dirname "$0"`/UFOs/adv_wght_ital_prewdth.designspace" --output-path "`dirname "$0"`/VAR/adventpro-wght-ital-prewdth-VF.ttf" #--verbose="DEBUG"
