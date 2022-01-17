Overview:

**2019-06-12**:

We are preparing our approval documents for our stakeholders to review, for Script Extension to Cyrillic for version 3.

**2019-07-06**:

We have a layout for the plan of Script Extension and Master Extension that will take place between 2019-04-27 until 2019-06-02.

We will initially design and integrate the Cyrillic to Advent∞3, to 3 Original Masters (MO) and 3 Generated Master (MG). The design and integration for Advent∞3 SeC will take approximately 11 days. At this point Advent∞3 will be available with Cyrillic at 7 Instances of Upright and 7 Instances of Italic.

After that we will branch and update the Advent∞3 to Advent∞4: 3 MO and 3 MG with additional Masters 1 MO and 9 MG, Initially we will do a Master Extension for all the new masters. That will cover the Black, Wide axes and Wide Italic and result to Advent∞4. Approximately by the end of July.

The planning is for alphabetic glyphs and does not include any calculation of additional glyphs of any form. We will have to review the progress and update accordingly. After the review of the plan and assignment of additional tasks for fulfilment of additional glyphs, kerning and arbitrary corrections, Advent∞4 will be available with Cyrillic at 18 Instances of Upright and Upright Wide, 18 Instances of Italic and Italic Wide, total of 36 Instances.

**2019-11-23**:

We have just finished the main work on all the wide masters from thin, regular, bold and finally black. This means that it is time for minor adjustments and iterations on these masters, after this we can conclude the work by generating the italics for those masters.


```mermaid
gantt
dateFormat  YYYY-MM-DD
title Advent Schedule
section Advent 3
#ADV-0001 Advent 3:                                                  done, des1,  2018-08-22, 2019-02-16
#ADV-0003 Advent 3 PR:                                               done, des2,  2019-02-16, 2019-04-01
#ADV-0004 Advent 4 Planning:                                               des3,  after des2, 2019-04-30
#ADV-0004-0001:                                                      done, des4,  2019-03-31, 2h
ADV-0004-0002 Compare NAM:                                           done, des5,  2019-04-09, 2h
ADV-0004-0003 MI Map:                                                done, des6,  2019-04-10, 2h
ADV-0004-0005 Autokern Reintegration to TYPL - Standalone Repo:      done, des8,  2019-04-12, 6h
ADV-0004-0006 Cupcake Day!:                                          done, des9,  2019-04-13, 2h

ADV-0004-0007-0001 Advent 3 and 4 Master Planning:                         des10, 2019-04-14, 2019-04-25

ADV-0003-0008-0001 Advent 3 Script Extension Cyrillic (SeC) Planning:      des27, 2019-04-26, 2h
ADV-0004-0007-0001 Advent 4 Master Extension Latin (MaE) Planning:         des28, 2019-04-27, 2h
ADV-0004-0008-0001 Advent 4 Script Extension Cyrillic (SeC) Planning:      des28, 2019-04-27, 1h
#
section Advent 3 SE Cyrillic

ADV-0003-0008-0001 Advent 3 SE Cyrillic:                             crit, des29, 2019-04-27, 23d
    ADV-0003-0008-0001-0001 Advent SeC MO:                           done, des30, 2019-04-27,  9d
        SeC MO 1 reg (04/27 to 04/30):                               done, des39, 2019-04-27,  3d
            MO reg Capital:                                          done, des31, 2019-04-27,  5h
            MO reg Capital 39/39:                                    done, des31, 2019-04-28,  5h
            MO reg SmallCase 9/45:                                   done, des31, 2019-04-28,  1h
            MO reg SmallCase 45/45:                                  done, des62, 2019-04-29,  4h
        3 SeC MO 2 thn (04/30 to 05/03):                             done, des40, after des39, 3d
            MO thn Capital 15/39, SmallCase 17/45:                   done, des63, 2019-05-01,  4h
            MO thn Capital 39/39, SmallCase 45/45:                   done, des64, 2019-05-02,  2h
        3 SeC MO 3 bld:                                              done, des41, after des40, 3d
            MO bld Capital 39/39, SmallCase 45/45:                   done, des65, 2019-05-05,  5h

    ADV-0003-0008-0001-0002 Advent SeC MO Integration of vectors:    done, des58, after des30, 11d
        3 SeC MO 1 thn:                                              done, des64, after des30, 3d
            MO thn Capitals:                                         done, des59, 2019-05-07,  5h
            MO thn LowerCase:                                        done, des62, 2019-05-08,  5h
            MO thn Complete:                                         done, des63, 2019-05-09,  6h
        3 SeC MO 2 reg:                                              done, des65, after des64, 3d
            MO reg 16/39 Capitals:                                   done, des59, 2019-05-09,  6h
            MO reg Capitals:                                         done, des67, 2019-05-10,  6h
            MO reg Complete:                                         done, des68, 2019-05-11,  8h
        3 SeC MO 3 bld:                                              done, des66, after des65, 5d
            MO bld 24/39 Capitals:                                   done, des69, 2019-05-14,  4h
            MO bld All Capitals:                                     done, des70, 2019-05-15,  2h
            MO bld Complete:                                         done, des71, 2019-05-16,  5h

    ADV-0003-0008-0001-0001 SeC MG:                                  done, des32, after des58, 4d
        3 SeC MG 1 reg_it:                                           done, des42, after des58, 1d
        3 SeC MG 2 bld_it:                                           done, des43, after des42, 1d
        3 SeC MG 3 thn_it:                                           done, des44, after des43, 1d
        SeC MG fixes:                                                done, des72, after des44, 1d

    ADV-0003-0003-0001 Preview and Approval Documents:                     des77, 2019-06-12,  2d
    #ADV-0003-0004-0001 EFO Build for Version 3:                           des76, after des77, 10d
    #ADV-0003-0004-0001-0001 EFO Glyph Distributor:                        des78, after des77, 10d

    #ADV-0003-0005-0001 Kerning Planning SeC:                              des73, after des76, 2d
    #    Kerning Pairs and Grouping:                                       des74, after des76, 1d
    #    Kerning Compression:                                              des75, after des74, 1d
#
section 4 Master Extension All Scripts

ADV-0004-0007-0001 4 Master Extension:                              crit, des33, 2019-07-06, 150d
    ADV-0004-0007-0001 MaE MO:                                      done, des76, 2019-07-06, 2019-08-19
        4 MaE MO 4 blk:                                             done, des77, 2019-07-06, 2019-08-19
    ADV-0004-0007-0001 MaE MG blk_it:                               done, des78, after des77, 2d
        4 MaE MO 4 blk_it:                                          done, des79, after des77, 2d
    ADV-0004-0007-0001 MaE MG wd:                                   done, des34, after des79, 95d
        4 MaE MG 1 thn_wd:                                          done, des45, after des79, 7d
        4 MaE MG 2 reg_wd:                                          done, des46, after des45, 10d
        4 MaE MG 3 bld_wd:                                          done, des47, after des46, 30d
        4 MaE MG 4 blk_wd:                                          done, des57, after des47, 48d
    ADV-0004-0007-0001 MaE MG wd_it:                                done, des35, after des57, 8d
        4 MaE MG 1 reg_wd_it:                                       done, des48, after des57, 2d
        4 MaE MG 2 thn_wd_it:                                       done, des49, after des48, 2d
        4 MaE MG 3 bld_wd_it:                                       done, des50, after des49, 2d
        4 MaE MG 4 blk_wd_it:                                       done, des51, after des50, 2d
```


*  Current:
    *  **ADV-0003** / from February 02 2019 to April 01 2019:
        *  **Advent PR ∞3.000**
            *  We are waiting for PR to Google Fonts.
    *  **ADV-0004** / After PR in April 2019:
        *  **Advent ∞4.000**
    *  **ADV-0004 Advent ∞4.000 Planning** / After PR whole April 2019:
        *  Planning for ∞4.000: 
            *  Project Goals
            *  Duration
                *  Alphabetic Glyphs:
                    *  Script Extension:
                        *  Advent 3 SE Cyrillic 11 days
                        *  Advent 4 SE Cyrillic 10 days
                    *  Master Extension
                        *  Advent 4 ME Latin and Greek 11 days
            *  Masters and Instances
                *  Masters and Instances Map
            *  Scripts
                *  Encoding NAM Files
            *  Glyphs
            *  Personnel Plan

*  Completed:
    *  ~~**ADV-0001** / July 01 2018 to 2019-02-16~~:
        *  Advent  ∞3.000 Delivered.
    *  **ADV-0004**:
        *  ~~**ADV-0004-0002 Compare Current Encoding Support against NAM**~~ 2019-04-09 2h
        *  ~~**ADV-0004-0003 Masters and Instances Map**~~ 2019-04-10 4h
        *  ~~**ADV-0004-0005 Autokern Reintegration to TYPL**~~ 2019-04-12 6h
        *  ~~**ADV-0004-0006 Advent Fontbakery Cupcake Day!**~~ 2019-04-13 2h
        *  ~~**ADV-0004-0007-0001 Advent Master Planning**~~ 2019-04-14 2h
            *  Master Planning MA and MG added to README/plans
    *  **ADV-0003-0008**:
        *  ~~**ADV-0003-0008-0001-0001 Advent SeC MO**~~

Task Codes:

*  ADV-∞-0002: Encodings
*  ADV-∞-0003: Information Architecture
    *  ADV-∞-0003-0001: Preview and Approval Documents
*  ADV-∞-0004: EFO
    *  ADV-∞-0004-0001: EFO Build
        *  ADV-∞-0004-0001-0001: EFO Glyph Distributor
*  ADV-∞-0005: Kerning
    *  ADV-∞-0005-0001: Kerning Planning
*  ADV-∞-0006: Mentions
*  ADV-∞-0007: Masters
    *  ADV-∞-0007-0001: Master Planning
    *  ADV-∞-0007-0002: Master Extension
*  ADV-∞-0008: Script Extension
    *  ADV-∞-0008-0001: Cyrillic Script Extension (SeC)
        *  ADV-∞-0008-0001-0001: 
            SeC Capitals, SeC SmallCase MO and MG
        *  ADV-∞-0008-0001-0002: SeC integration of vectors to the font.

Task Codes Versioned:

*  ADV-0003: Advent 3
    *  ADV-0003-0007: Masters
        *  ADV-0003-0007-0001: Master Planning
    *  ADV-0003-0008: Script Extension
        *  ADV-0003-0008-0001: Cyrillic Script Extension (SeC)
            *  ADV-0003-0008-0001-0001: SeC Capitals MO and MG
            *  ADV-0003-0008-0001-0002: SeC SmallCase MO and MG
    *  ADV-0003-0004: EFO
        *  ADV-0003-0004-0001: EFO Build for Version 3
            *  ADV-0003-0004-0001-0001: EFO Glyph Distributor
    *  ADV-0003-0003: Information Architecture
        *  ADV-0003-0003-0001: Preview and Approval Documents
*  ADV-0004: Advent 4
    *  ADV-0004-0002: Encodings
    *  ADV-0004-0003: Information Architecture
    *  ADV-0004-0004: EFO
    *  ADV-0004-0005: Kerning
        *  ADV-0004-0005-0001: Kerning Planning
    *  ADV-0004-0007: Masters
        *  ADV-0004-0007-0001: Master Planning
        *  ADV-0004-0007-0002: Master Extension
    *  ADV-0004-0008: Script Extension
        *  ADV-0004-0008-0001: Cyrillic Script Extension (SeC)
            *  ADV-0004-0008-0001-0001: SeC Capitals, SmallCase MO and MG
            *  ADV-0004-0008-0001-0002: SeC integration of vectors to the font.
        *  ADV-0004-0008-0001: Cyrillic Script Extension (SeC)

