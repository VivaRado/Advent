# Advent Pro VARIABLE 2018

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
    1.  ~~blk_it       900     Black (Heavy)~~

- **Master A**: thn - reg = thn - xlg - lgt - reg
- **Master B**: reg - bld = reg - med - smb - bld ~~- xbd - blk~~

**  **

**Kerning**

Kerning was done by utilizing Typefacets Autokern Python3 Updated Script by using VRD TYPL/kerning_autokern.py: [VRD-Typography-Library](https://github.com/VivaRado/VRD-Typography-Library)

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

Timeline was reducted

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