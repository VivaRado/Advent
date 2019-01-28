![Screenshot](https://github.com/VivaRado/Advent/blob/master/font_preview/assets/img/adventprovar.gif)

**Introduction**

*   Company: VivaRado LLP
*   Designer: Andreas Kalpakidis
*   Proposal Date: 22/08/2018
*   Type family name: Advent Pro Var (Advent Professional Variable)
*   Twitter: [@vivarado](https://twitter.com/VivaRado)
*   Google+: [+vivarado](https://plus.google.com/u/1/106810481377952020277)
*   Google Group:[VivaRado Typography Google Group](https://groups.google.com/a/vivarado.com/forum/#!forum/typography)

**Phases**

1.  Planning and Execution
    1.  Design
    1.  Production
    1.  Weights and Masters
     1.  Kerning
     1.  Components
    1.  Language Scripts / Glyph Range
    1.  Features
    1.  Timeline
    1.  Delivery
1.  Design
    1.  Design Methods
        1.  Introduction
        1.  Method Structure
1.  Script extension
    1.  Future Script Support
    1.  Future Opentype Feature Support


**TLDR;**

To make a variable font:

*   Use VRD TYPL

**  **

**Planning and Execution**

Decide on the encoding sets and supported language scripts. Decide and plan the weights and how you will generate each weight. Understand the procedures and steps. Calculate or keep track of timelines, steps procedures and pitfalls.

**  **

**Design**

Advent was designed in 2007 by Andreas Kalpakidis, It features as originally intended 7 Weights of geometric sharp curved high rise forms and modernized Greek Letters.

**  **

**Production**

To produce the font, Illustrator and Fontlab was used originally in 2007, updating to Advent  Pro Variable in 2018, a set of scripts for Adobe Illustrator (JSX) and Fontlab (Python) where written, additionally python scripts and bash, for the composition and kerning. Later on VRD Typography Library was introduced allowing for easier modifications to the font by utilizing a new format - a container for UFO, called the EFO. VRD TYPL for kerning - and compression and Googles fontmake to compile the final variable font. 

Work was done on a Linux box with VirtualBox running Windows 8 and Mac OSX Lion.

**  **

**Weights and Masters**

1.  Masters:
    1.  Thin (100)
    1.  Regular (400)
    1.  Bold (700)
    1.  Thin Italic (100)
    1.  Regular Italic (400)
    1.  Bold Italic(700)
1.  Master Instances:
    1.  **thn**      100     Thin (Hairline) *MM*
    1.  **xlg**      200     Extra Light (Ultra Light)
    1.  **lgt**      300     Light
    1.  **reg**      400     Regular *MM*
    1.  **med**      500     Medium
    1.  **smb**      600     Semi Bold (Demi Bold)
    1.  **bld**      700     Bold *MM*
    1.  ~~xbd      800     Extra Bold (Ultra Bold)~~
    1.  ~~blk      900     Black (Heavy)~~
    1.  **thn_it**       100     Italic Thin (Hairline) *MM*
    1.  **xlg_it**       200     Italic Extra Light (Ultra Light)
    1.  **lgt_it**       300     Italic Light
    1.  **reg_it**       400     Italic Regular *MM*
    1.  **med_it**   500     Italic Medium
    1.  **smb_it**   600     Italic Semi Bold (Demi Bold)
    1.  **bld_it**    700     Italic Bold *MM*
    1.  ~~xbd_it       800     Extra Bold (Ultra Bold)~~
    1.  ~~blk_it       900     Black (Heavy)~


**  **

**Kerning**

With the help of Typefacet Integrated Autokern, we have obtained the first layer of kerning for the upright bold.
By using VRD TYPL Kerning Adjust, 
we made the corrections, and the rest of the optimisations required per weight.

We have Classified our glyphs in a way where no kerning loss is observed. By dividing by Language Set, without language intrusion between classes.
Small Case and Capitals are also ~ non intruding. This increases size minimally but maintains kerning pair loss at zero.

During the process we attempted to maintain the Italics width according to the contour. This created a larger alteration size and jittering italics transition due to changing width - even if the kerning was precise. We eventually opted for the slant-to-right-side-corner and maintained the regular kerning along to the italics and smoother animation on Italics.

This brings us to kern a specific set of letters, the other letters are left to your creative kerning.
VivaRado standard kerning sets are defined as follows:

 - Class Based(CB):

  - Latin Capitals(CBLC):
   - ```A B C G D E I J H O P R S M F K L T U V Y Z```
  - Latin SmallCase(CBLS):
   - ```a e o c d m i t g h k l r s u v y j z f t b ß```
  - Greek (GREEK UNICODES)(CBGC):
   - ```Α Β Γ Ε Ι Χ Μ Ψ Κ Ο Ω Υ Ρ Τ```
  - Greek SmallCase(CBGS):
   - ```α β ι ο χ ε γ μ ω```
  - Symbols(CBSY):
   - ```~ | " % @ * / ```
  - Numbers(CBNU):
   - ```8```
 
 - Letter Based(LB):

  - Latin Capitals(LBLC):
   - ```A B C D E F G H I J K L M N O P Q R S T U V W X Y Z```
  - Latin SmallCase(LBLS):
   - ```a b c d e f g h i j k l m n o p q r s t u v w x y```
  - Greek (GREEK UNICODES)(LBGC):
   - ```Α Β Γ Δ Ε Ζ Η Θ Ι Κ Λ Μ Ν Ξ Ο Π Ρ Σ Τ Υ Φ Χ Ψ Ω```
  - Greek SmallCase(LBGS):
   - ```α β γ δ ε ζ η θ ι κ λ μ ν ξ ο π ρ σ ς τ υ φ χ ψ ω```
  - Numbers(LBNU):
   - ```0 1 2 3 4 5 6 7 8 9```

 - Resulting Permutations that have been Adjusted:

  - Class Based Permutations (CB):

   - Latin VS Latin Capitals Class Based Permutation (CBLCLC)
   - Latin VS Latin SmallCase Class Based Permutation (CBLSLS)
   - Latin Capitals VS Latin SmallCase Class Based Permutation (CBLCLS)

   - Greek VS Greek Capitals Class Based Permutation (CBGCGC)
   - Greek VS Greek SmallCase Class Based Permutation (CBGSGS)
   - Greek Capitals VS Greek SmallCase Class Based Permutation (CBGCGS)

  - Letter Based Permutations (LB):

   - Latin VS Latin Capitals Letter Based Permutation (LBLCLC)
   - Latin VS Latin SmallCase Letter Based Permutation (LBLSLS)
   - Latin Capitals VS Latin SmallCase Letter Based Permutation (LBLCLS)

   - Greek VS Greek Capitals Letter Based Permutation (LBGCGC)
   - Greek VS Greek SmallCase Letter Based Permutation (LBGSGS)
   - Greek Capitals VS Greek SmallCase Letter Based Permutation (LBGCGS)

 - Letter to Letter Adjustments:
  - These are small adjustments due to design quirks, and when we decide that a glyph doesn't fit into classes or the class is not satisfying the kerning requirements completely.
 - Ommited:
  - Cross Language System Kerning (grek to latn and latn to grek).
  - Greek "sigma1" on the Left Side for all grek.
 - Glossary:
  - Class Based (CB): One letter from each class.
  - Letter Based (LB): Alphabet / Complete Range.

More information in ```kerning_adjustments/kerning_pair_details```

**If you notice a possible kerning improvement we would like to hear about it.**

VRD TYPL/kerning_adjust.py: [VRD-Typography-Library-Kerning-Adjust](https://github.com/VivaRado/VRD-Typography-Library/tree/master/Lib/kerning_adjust)
VRD TYPL/kerning_autokern.py: [VRD-Typography-Library-Autokern](https://github.com/VivaRado/VRD-Typography-Library/tree/master/Lib/kerning)

**  **

**Components**

Components are created by first running VRD/TYPL/SIMEX to obtain a component similarity index, then VRD/TYPL/COMPONENTS to Componentize the EFO,
later you can export to Componentized UFOs.

**  **

**Language Scripts / Glyph Range**

At this moment advent supports Latin, and Greek Encoding. The glyph range is ~ 391 \
The Proposed glyph list is ~1500 Glyphs not including the glyphs for Opentype Features  \
(Script Extension).
**  **
**Current Character Support:**
- *Latin*
- *Extended Latin*
- *Greek*

**Intended Character Support:**
**( Script Extension / Future Script Support )**

- The Proposed Encoding/Glyph List: /encoding_list/suggested_encoding.py
- Current Encoding/Glyph List: /encoding_list/current_encoding.enc

**  **

**Features**

Advent has NO features. The plan is to create all the features available in popular scripts. Additionally Glyphs exist for ligatures like the standard set fl, ffl … but the current version has no opentype features written to substitute the ligatures.


**Intended Opentype Feature Support:**

( Script Extension / Future Opentype Features Support )

**  **

**Timeline**

July 2018 to December 1 - assuming final will be released in about 7 - 14 days. Hopefully before the New Year.

Eventually Delivered in January 28 2019.

**  **

1. **Research:**

Encoding files based on Adobe Glyph list,  Operational Illustrator Adobe script to create layers from encoding file. Installed python 2.7 x32 for Fontlab, EPS export with proportional resize and proper positioning, fontlab script to import EPS.

1. **Design:**

Started Componentizing Advent, smart object placement scripts.

1. **Post Production:**

VRD TYPL for kerning - kerning compression and componentization

**  **

**Delivery**

Advent Pro Variable will be delivered in 7 Weights and Variable format. All the Adobe Illustrator scripts, Fontlab Python and additional scripts will be provided. Forks of the original libraries with their alterations, and Encoding Files.

The delivered font files are provided in UFO, EPS, VFB, OTF.

All the above files are available on VivaRado Github Account.

**  **

**Design / Design Methods / Introduction**

VRD created EFO (Extraordinary Font Object) and utilises VRD Typography Library Functions to design, kern and prepare the fonts for export.

**  **

**Design / Design Methods / Method Structure**

Just like in a UFO, all glyphs should be visible and editable through any vector editor. Even if the original design is made using Adobe Illustrator CC. To achieve this, we export all glyphs from the UFOs
that are located in the EFO, to SVG and later when design is finished we import them back to the EFO and we can export our UFOs.


**Script Extension**

Every modern font needs a set of OpenType features, especially if it is served by google!
Here is what VivaRado wants to add to Advent font!


**Future Script Support**

    Latin
    Extended Latin
    Greek
    Polytonal Greek
    Cyrillic
    Qazaq
    Ligatures
    Discretionary Ligatures
    Fractions
    Stylistic Alternatives
    Lining Proportional
    Oldstyle Tabular
    Oldstyle Proportional
    Superior Letters
    Numerators & Denominators
    Uppercase Variants
    Scientific Inferiors
    Superscripts
    Localized Forms
    Punctuation
    Miscellaneous
    Math Symbols

**Future Opentype Features Support**

    Ligatures
    Discretionary Ligatures
    Stylistic Alternate per Set
    Oldstyle Figures
    Lining Figures
    Proportional Figures
    Tabular Figures
    Superiors
    Scientific Inferiors
    Numerators
    Denominators
    Fractions
    Ordinals
    Localized Forms
    Case-Sensitive Forms
    Capital Spacing
    Access all Alternates



**Thank You**

Thanks goes to Dave Crossland for his initiative to regenerate Advent and quite frankly the desire to make quality typography once again and Michael LaGattuta for all his attention to detail and great ideas.
Releases and news will be public through all the VivaRado accounts.