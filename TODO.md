VRD Typography Library TODO list
=============================

**Development Suggestions**

 * ```<issue 00100/>``` EFO Componentize Integration
 * ```<issue 00200/>``` Create Tests for all functions
 * ```<issue 00300/>``` Test Python3 Type Facet Library Update on functionality other than Autokerning.

**Suggestions and Observations by Contributors**

 * ```<issue 00400/>``` The anchoring does not seem to be properly done, perhaps this is getting messed up by the componentization script? There are some letters with uneccesary anchors: /B with ogonek and center, /epsilon with ogonek and center, etc.

 * ```<issue 00500/>``` Ogonek anchors are not in the right position in the Regular Roman, this might be because of the componentization script, look at /Aogonek

 * ```<issue 00600/>``` In the Regular Roman, combining accents are being kerned but they most likely should not have any kerning

 * ```<issue 00700/>``` The kerning class assignments could be much more efficient. /D for example could have a class of /H on the left and /O on the right, but right now it has /D and /D

	 * ```<issue 00701/>``` This will significantly reduce the number of kerns and the file size

 * ```<issue 00800/>``` Many outlines are somewhat messy, offcurve points on straight segments, 0-length handles, points near but not on extremes, and some odd forms like the joining of the two curved strokes in /B

     * ```<issue 00801/>``` A lot of this should be fixed to keep file size down and to ensure smooth interpolations

 * ```<issue 00900/>``` Some of the glyphs with diagonal strokes appear to be kerned a bit too tightly. If you type something like "WANDER" the /W and /A appear very close, and the /A /N appear significantly further

 * ```<issue 01000/>``` I had compared the static roman to the one on Google Fonts:

     * ```<issue 01001/>``` There are significant differences in the vertical metrics, this should be fixed

     * ```<issue 01002/>``` Some spacing differences, this isn't bad if it isn't too significant and improves the design, this will have to be verified

     * ```<issue 01003/>``` The outlines are slightly shorter than those currently up online by a couple of units. Ideally there should be no change in outline height

 * ```<issue 01100/>``` The italics appear to be mechanically slanted Romans without few or no optical compensations

     * ```<issue 01101/>``` The most notable are glyphs with diagonal strokes which appear very heavy when slanted. I think fixing these diagonals would be a small time investment that would really help the texture of the Italic


**Known Issues**

| Issue | State     | Notes                                                                                                               |
|-------|-----------|---------------------------------------------------------------------------------------------------------------------|
| 00100 | Adressing | Componentization script.                                                                                            |
| 00200 | Postponed | N/A                                                                                                                 |
| 00300 | Postponed | N/A                                                                                                                 |
| 00400 | Adressing | Componentization script.                                                                                            |
| 00500 | Adressing | Componentization script.                                                                                            |
| 00600 | Postponed | N/A                                                                                                                 |
| 00700 | Postponed | N/A                                                                                                                 |
| 00701 | Postponed | N/A                                                                                                                 |
| 00800 | Postponed | N/A                                                                                                                 |
| 00801 | Postponed | N/A                                                                                                                 |
| 00900 | Ignored   | Looks ok to me - According to current UFOs in sources.                                                              |
| 01000 | N/A       | N/A                                                                                                                 |
| 01001 | Postponed | Differrence of 700 - 696 = 4px height difference - under 5px not significant. According to current UFOs in sources. |
| 01002 | Ignored   | Please Elaborate                                                                                                    |
| 01003 | Ignored   | Duplicate of 01001                                                                                                  |
| 01100 | Postponed | Very good idea - should be real italics atleast on the part of widths.                                              |
| 01101 | Postponed | Duplicate of 01100                                                                                                  |