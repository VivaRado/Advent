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
    1.  Language Scripts / Glyph Range
    1.  Features
    1.  Timeline
    1.  Delivery
1.  Design
    1.  Design Methods
        1.  Introduction
        1.  Method Structure
        1.  Command Procedure
            1.  Font Reconstruction
            1.  Font Design / Retouch
            1.  Kerning
            1.  Create Variable font
    1.  Expansion
1.  Script extension
    1.  Future Script Support
    1.  Future Opentype Feature Support


**TLDR;**

To make a variable font:

*   Match every weight in terms of glyph list
    *   Match every path / shape anchor count
        *   Match every start point and enumeration of path items in glyph \
Keep main glyph as #1 so kerning reads that instead of punctuation.
*   Run Fontlab/Tools/Blend and run it again until all paths across all weights are corrected.
*   Export edge cases back for more blending
*   Blend again and again and some more
*   Save and convert VFBs to UFOs
*   Test convert to variable with fontmake
*   Kern the non Italics with typeface
*   Get the glyph list from each non Italic UFO's kern.plist
*   Pass the permutation of that Kern.plist to typeface on the Italics or fontmake will fail
*   Done.
*   Advent has no opentype features, they have been cleared for the initial variable font release.
*   Advent needs your support for VivaRado and Andreas Kalpakidis to develop language support and all the opentype features people want!

**  **

**Planning and Execution**

Decide on the encoding sets and supported language scripts. Decide and plan the weights and how you will generate each weight. Understand the procedures and steps. Calculate or keep track of timelines, steps procedures and pitfalls.

**  **

**Design**

Advent was designed in 2007 by Andreas Kalpakidis, It features as originally intended 7 Weights of geometric sharp curved high rise forms and modernized Greek Letters.

**  **

**Production**

To produce the font, Illustrator and Fontlab was used originally in 2007, updating to Advent  Pro Variable in 2018, a set of scripts for Adobe Illustrator (JSX) and Fontlab (Python) where written, additionally python scripts and bash, for the composition and kerning. Typefacets Autokern.py was used for kerning and Googles fontmace to compile the final variable font. 

Work was done on a Linux box with VirtualBox running Windows 8 and Mac OSX Lion. The scripts used are in a pre-alpha state written in python. They could be automated. Addition of Opentype Features and scripts to generate them will be needed. The general process is aided mainly by python.

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

Kerning was done by utilizing Typefacets Autokern Python script: [https://github.com/charlesmchen/typefacet ](https://github.com/charlesmchen/typefacet)

After the initial kerning result, Typefacet Autokern produces unclassified data.
see. Design / Design Methods / Command Procedure / Kerning

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

Export / Import Tests Illustrator File to EPS, EPS to Fontlab, Multiple Masters, Multiple Master Blending, Kerning, Crossblends, Variable font compile.

1. **Total Hours / Days:**

*   05-08-2018 - 11-08-2018 = **51 Hours**
*   12-08-2018 - 18-08-2018 = **44 Hours**
*   18-08-2018 - 19-08-2018 = **19 Hours**
*   19-08-2018 - 20-08-2018 = **12 Hours**
*   20-08-2018 - 22-08-2018 = **41 Hours**

    Total Hours: **167 Hours**

**  **

**Delivery**

Advent Pro Variable will be delivered in 7 Weights and Variable format. All the Adobe Illustrator scripts, Fontlab Python and additional scripts will be provided. Forks of the original libraries with their alterations, and Encoding Files.

The delivered font files are provided in UFO, EPS, VFB, OTF.

All the above files are available on VivaRado Github Account.

**  **

**Design / Design Methods / Introduction**

The circular logic we try to achieve, is the generation logic. Where the information is brought from its components right down to its final deliverable stage, by utilizing specific structures and methods of design and development to achieve rapid delivery or at least… not slow delivery.

**  **

**Design / Design Methods / Method Structure**

Just like in a UFO, all glyphs should be visible and editable through any vector editor. Even if the original design is made using Adobe Illustrator CC. To achieve this, we export all glyphs from Adobe Illustrator layers to SVGs / EPSs by maintaining a naming format that will later allow us to package the font to its final state. With those files we have sets of encodings files that will promise language / script support and will allow tracking of influenced, added, removed or updated glyphs. The fonts Multiple Master is another important component that will allow further design decisions for the endpoint user of the font. Kerning is also generated and embedded to the font by means of automation.


**Design / Design Methods / Command Procedure**


**  **

**Font Reconstruction**


1.  Convert all Glyphs to PostScript for Export.
1.  Export the glyph vectors to EPS files for each weight.
    
    	Script: _FL_export_font_glyphs_to_EPS_files.py_

1.  Rename each glyph set to include UNICODE.

        Script: _do_ufo.bat_
		Pitfalls: Runs vfb2ufoWin provided from FontLab on the directory of the fonts. Edit the bat for directories of VFBs

1.  Rename each glyph set to include UNICODE.

        Script: _encoding_to_eps_rename.py_

**  **

**Font Design / Retouch**


1.  Import weights back to New Font Files in Fontlab for each weight.

        Script: _FL_import_EPS_files_to_glyphs.py_

1.  Use Fontlabs Tools/Blend.

        Pitfalls: If the paths don't match up blend until they do. Try to keep the paths as they were designed in illustrator and make sure to not allow any simplification or optimization of the paths or it creates too much noise to handle between similar glyphs and will result to problems when using fontmake to create the variable font.


1.  Import the exported from Fontlab EPS Glyphs to Illustrator
	
    	Script: _AI_import_eps_positions_tpg.jsx
		Pitfalls: The script imports to layers that need different grouping for the export and componentization to occur, needs update that groups appropriately. There is a sizing process when importing from FontLab or any editor the font is too big for illustrator design plane to fit all the letters. The percentage downscale has to be scaled up on export.

1. Componentize by using Illustrator Symbols.

        Scripts:
          	1.  _AI_replace_with_symbol_all_weights.jsx:
			By selecting the layer with appropriately grouped PathObject. You can run the script and give the appropriate Symbol, it replaces the path with the appropriately weight named symbol, for all weight layers.
    		2.  _AI_replace_with_symbol.jsx: 
			Replaces only selected object with given symbol.
        Pitfalls: A specific structure is required for Symbol helper scripts to work.
1.  Manual Editing of each weight layer
1.  Export each weight layer to EPSs:
		
        Script: _AI_EPS_Exporter_tpg.jsx
        
1.  Import exported from Illustrator EPS Glyphs, back to FontLab \
		
        ( Font Construction #6 )


**  **

**Kerning**


1.  Kern only the non Italics.

        Scripts: do_autokern.py
        Pitfalls: Edit the file with proper names and weights and directories.

1.  Extract the kerning pairs for each weight so as to kern the Italic equivalent \
Scripts: extract_pairs.py

        Pitfalls: Run the script in the directory of the non Italic UFOs

1.  Run the kerning on the Italics using the Fix Pairs from step 2

        Scripts: do_autokern_per_weight.py
        Pitfalls: Edit the file with proper names and weights and directories.

1.  Replace the kerning with the newly generated Italics kerning.plists
        
1.  Classify the Unclassified Kerning using the originally autokerned UFOs

        Scripts: find_similar.py
        Pitfalls: Settings are required inside the script so visual weight gets properly identified.

1.  Compress the generated from find_similar.py class_loc/kern_class.json to a groups.plist file

        Scripts: compress_kerning.py
        Pitfalls: Before starting, check the json for unidentified direction values or other direction issues.

1.  Transfer the kern values from the original Unclassified to a new kerning.plist based on the generated kern_class_group_loc/groups.plist

        Scripts: abduct_kern_vals.py
        Pitfalls: Values that don't match the classes, will be appended at the end of the file.



**  **

**Create Variable font**


1.  Create a designspace file and run fontmake

        Scripts: fontmake

        Pitfalls: Pray

**  **

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

Thanks goes to Dave Crossland for his initiative to regenerate Advent and quite frankly the desire to make quality typography once again. If all goes well new fonts, updates, releases and news will be public through all the VivaRado accounts.