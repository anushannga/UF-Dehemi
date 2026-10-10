## FontSpector report

fontspector version: 1.9.0






## Check results




<details><summary>[3] ofl-release/UF-Dehemi-2.351</summary>
<div>


<details>
    <summary>🔥 <b>FAIL</b> Ensure Italic styles have Roman counterparts. (googlefonts/family/italics_have_roman_counterparts)</summary>
    <div>


> For each font family on Google Fonts, every Italic style must have a Roman sibling.
> 
> This kind of problem was first observed at [1] where the Bold style was missing but BoldItalic was included.
> 
> [1] https://github.com/google/fonts/pull/1482




Original proposal: [https://github.com/fonttools/fontbakery/issues/1733]





- 🔥 **FAIL** Italics missing a Roman counterpart:

* ofl-release/UF-Dehemi-2.351/UF-Dehemi-Italic.ttf [code: missing-roman]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Ensure Fonts have 'ital' STAT axis. (opentype/STAT/ital_axis)</summary>
    <div>


> Check that related Upright and Italic have an 'ital' axis in the STAT table.
> 
> Since the STAT table can be used to create new instances, it is important to ensure that such an 'ital' axis be the last one declared in the STAT table so that the eventual naming of new instances follows the subfamily traditional scheme (RIBBI / WWS) where "Italic" is always last.
> 
> The 'ital' axis should also be strictly boolean, only accepting values of 0 (for Uprights) or 1 (for Italics). This usually works as a mechanism for selecting between two linked variable font files.
> 
> Also, the axis value name for uprights must be set as elidable.




Original proposal: [https://github.com/fonttools/fontbakery/issues/2934, https://github.com/fonttools/fontbakery/issues/3668, https://github.com/fonttools/fontbakery/issues/3669]





- ⚠️ **WARN** Static font is missing the 'STAT' table. [code: no-stat-table]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Check for codepoints not covered by METADATA subsets. (googlefonts/metadata/unreachable_subsetting)</summary>
    <div>


> This check ensures that all encoded glyphs in the font are covered by a subset declared in the METADATA.pb. Google Fonts splits the font into a set of subset fonts based on the contents of the `subsets` field and the subset definitions in the `glyphsets` repository.
> 
> Any encoded glyphs which are not by any of these subset definitions will not be served in the subsetted fonts, and so will be unreachable to the end user.




Original proposal: [https://github.com/fonttools/fontbakery/issues/4097 and https://github.com/fonttools/fontbakery/pull/4273]





- ⚠️ **WARN** ofl-release/UF-Dehemi-2.351/UF-Dehemi-Italic.ttf: The following codepoints supported by the font are not covered by any subsets defined in the font's metadata file, and will never be served. You can solve this by either manually adding additional subset declarations to METADATA.pb, or by editing the glyphset definitions.

* U+02D8 BREVE: try adding one of: canadian-aboriginal, yi
* U+02D9 DOT ABOVE: try adding one of: yi, canadian-aboriginal
* U+02DB OGONEK: try adding one of: canadian-aboriginal, yi
* U+0302 COMBINING CIRCUMFLEX ACCENT: try adding one of: coptic, tifinagh, cherokee, math
* U+0306 COMBINING BREVE: try adding one of: tifinagh, old-permic
* U+0307 COMBINING DOT ABOVE: try adding one of: old-permic, tifinagh, math, malayalam, canadian-aboriginal, syriac, todhri, tai-le, hebrew, coptic, duployan
* U+030A COMBINING RING ABOVE: try adding one of: duployan, syriac
* U+030B COMBINING DOUBLE ACUTE ACCENT: try adding one of: cherokee, osage
* U+030C COMBINING CARON: try adding one of: cherokee, tai-le
... and 8 others

Or you can add the above codepoints to one of the subsets supported by the font: latin-ext, latin, sinhala, vietnamese [code: unreachable-subsetting]
  
  

</div>
</details>


</div>
</details>


<details><summary>[20] ofl-release/UF-Dehemi-2.351/UF-Dehemi-Italic.ttf</summary>
<div>


<details>
    <summary>🔥 <b>FAIL</b> Check base characters have non-zero advance width. (base_has_width)</summary>
    <div>


> Base characters should have non-zero advance width. Additionally, certain Unicode characters (such as zero-width joiners and zero-width spaces) are expected to have zero advance width. If they have a non-zero width, they may cause unexpected spacing in text layout.




Original proposal: [Rod on chat, https://github.com/fonttools/fontspector/issues/518]





- 🔥 **FAIL** The following glyphs had zero advance width:

* uni02C9 (Some(713)) [code: zero-width-bases]
  
  

</div>
</details>





<details>
    <summary>🔥 <b>FAIL</b> Check family name for GF Guide compliance. (googlefonts/family_name_compliance)</summary>
    <div>


> Checks the family name for compliance with the Google Fonts Guide. https://googlefonts.github.io/gf-guide/onboarding.html#new-fonts
> 
> If you want to have your family name added to the CamelCase exceptions list, please submit a pull request to the camelcased_familyname_exceptions.txt file.
> 
> Similarly, abbreviations can be submitted to the abbreviations_familyname_exceptions.txt file.
> 
> These are located in the Lib/fontbakery/data/googlefonts/ directory of the FontBakery source code currently hosted at https://github.com/fonttools/fontbakery/




Original proposal: [https://github.com/fonttools/fontbakery/issues/4049]





- 🔥 **FAIL** "UF-Dehemi" contains an abbreviation. [code: abbreviation]
  
  


- 🔥 **FAIL** "UF-Dehemi" contains the following characters which are not allowed: "-". [code: forbidden-characters]
  
  

</div>
</details>





<details>
    <summary>🔥 <b>FAIL</b> Check font names are correct (googlefonts/font_names)</summary>
    <div>


> Google Fonts has several rules which need to be adhered to when setting a font's name table. Please read: https://googlefonts.github.io/gf-guide/statics.html#supported-styles https://googlefonts.github.io/gf-guide/statics.html#style-linking https://googlefonts.github.io/gf-guide/statics.html#unsupported-styles https://googlefonts.github.io/gf-guide/statics.html#single-weight-families




Original proposal: [https://github.com/fonttools/fontbakery/pull/3800]





- 🔥 **FAIL** Font names are incorrect:

| Name                       | Current          | Expected         |
|----------------------------|------------------|------------------|
| Family Name                | UF-Dehemi        | UF-Dehemi        |
| Subfamily Name             | Italic           | Italic           |
| Full Name                  | UF-Dehemi Italic | UF-Dehemi Italic |
| Postscript Name            | UF-Dehemi-Italic | UF-Dehemi-Italic |
| Typographic Family Name    | **UF-Dehemi**    | **N/A**          |
| Typographic Subfamily Name | **Italic**       | **N/A**          | [code: bad-names]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Check hhea.caretSlopeRise and hhea.caretSlopeRun (opentype/caret_slope)</summary>
    <div>


> Checks whether hhea.caretSlopeRise and hhea.caretSlopeRun match with post.italicAngle.
> 
> For Upright fonts, you can set hhea.caretSlopeRise to 1 and hhea.caretSlopeRun to 0.
> 
> For Italic fonts, you can set hhea.caretSlopeRise to head.unitsPerEm and calculate hhea.caretSlopeRun like this: round(math.tan(   math.radians(-1 * font["post"].italicAngle)) * font["head"].unitsPerEm)
> 
> This check allows for a 0.1° rounding difference between the Italic angle as calculated by the caret slope and post.italicAngle




Original proposal: [https://github.com/fonttools/fontbakery/issues/3670]





- ⚠️ **WARN** hhea.caretSlopeRise and hhea.caretSlopeRun do not match with post.italicAngle.
Got caretSlopeRise: 1000, caretSlopeRun: 0, expected caretSlopeRise: 1000, caretSlopeRun: 249 [code: mismatch]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Check that OS/2 fsSelection WWS bit is set correctly. (opentype/fsselection_wws)</summary>
    <div>


> According to the OpenType specification, OS/2.fsSelection bit 8 (WWS) should be set if the font has name table strings consistent with a weight/width/slope family without requiring use of name IDs 21 and 22.
> 
> Conversely, if name IDs 21 and 22 are present (indicating the font names are not WWS-conformant), the WWS bit should not be set.




Original proposal: [https://github.com/fonttools/fontspector/issues/577]





- ⚠️ **WARN** OS/2 fsSelection WWS bit is not set, and the font does not have name IDs 21/22 (WWS Family/Subfamily). If the font's naming is WWS-conformant, the WWS bit should be set. [code: no-wws-without-wws-names]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Check glyphs in mark glyph class are non-spacing. (opentype/GDEF_spacing_marks)</summary>
    <div>


> Glyphs in the GDEF mark glyph class should be non-spacing.
> 
> Spacing glyphs in the GDEF mark glyph class may have incorrect anchor positioning that was only intended for building composite glyphs during design.




Original proposal: [https://github.com/fonttools/fontbakery/issues/2877]





- ⚠️ **WARN** The following glyphs seem to be spacing (because they have width > 0 on the hmtx table) so they may be in the GDEF mark glyph class by mistake, or they should have zero width instead:

* sinVirama [code: spacing-mark-glyphs]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Checking OS/2 fsSelection value. (opentype/xavgcharwidth)</summary>
    <div>


> The OS/2.xAvgCharWidth field is used to calculate the width of a string of characters. It is the average width of all non-zero width glyphs in the font.
> 
> This check ensures that the value is correct. A failure here may indicate a bug in the font compiler, rather than something that the designer can do anything about.




Original proposal: [https://github.com/fonttools/fontbakery/issues/4829]





- ⚠️ **WARN** OS/2 xAvgCharWidth is 653 but it should be 680 which corresponds to the average of the widths of all glyphs in the font. This may indicate a problem with the font editor or the font compiler. [code: xAvgCharWidth-wrong]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Check accent of Lcaron, dcaron, lcaron, tcaron (alt_caron)</summary>
    <div>


> Lcaron, dcaron, lcaron, tcaron should NOT be composed with quoteright or quotesingle or comma or caron(comb). It should be composed with a distinctive glyph which doesn't look like an apostrophe.
> 
> Source: https://ilovetypography.com/2009/01/24/on-diacritics/ http://diacritics.typo.cz/index.php?id=5 https://www.typotheque.com/articles/lcaron




Original proposal: [https://github.com/fonttools/fontbakery/issues/3308]





- ⚠️ **WARN** Lcaron is decomposed and therefore could not be checked. Please check manually. [code: decomposed-outline]
  
  


- ⚠️ **WARN** dcaron is decomposed and therefore could not be checked. Please check manually. [code: decomposed-outline]
  
  


- ⚠️ **WARN** lcaron is decomposed and therefore could not be checked. Please check manually. [code: decomposed-outline]
  
  


- ⚠️ **WARN** tcaron is decomposed and therefore could not be checked. Please check manually. [code: decomposed-outline]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Check if each glyph has the recommended amount of contours. (contour_count)</summary>
    <div>


> Visually QAing thousands of glyphs by hand is tiring. Most glyphs can only be constructured in a handful of ways. This means a glyph's contour count will only differ slightly amongst different fonts, e.g a 'g' could either be 2 or 3 contours, depending on whether its double story or single story.
> 
> However, a quotedbl should have 2 contours, unless the font belongs to a display family.
> 
> This check currently does not cover variable fonts because there's plenty of alternative ways of constructing glyphs with multiple outlines for each feature in a VarFont. The expected contour count data for this check is currently optimized for the typical construction of glyphs in static fonts.




Original proposal: [https://github.com/fonttools/fontbakery/issues/4829]





- ⚠️ **WARN** This check inspects the glyph outlines and detects the total number of contours in each of them. The expected values are
     inferred from the typical amounts of contours observed in a
     large collection of reference font families. The divergences
     listed below may simply indicate a significantly different
     design on some of your glyphs. On the other hand, some of these
     may flag actual bugs in the font such as glyphs mapped to an
     incorrect codepoint. Please consider reviewing the design and
     codepoint assignment of these to make sure they are correct.


    The following glyphs do not have the recommended number of contours:
* sinAa (U+0D86): found 7, expected one of: [3, 4, 5]
* sinAe (U+0D87): found 8, expected one of: [3, 4, 5]
* sinAae (U+0D88): found 6, expected one of: [3, 4, 5]
* sinRVocalic (U+0D8D): found 5, expected one of: [3, 4, 6]
* sinAi (U+0D93): found 7, expected one of: [4, 5, 6]
* sinO (U+0D94): found 4, expected one of: [1, 2, 3]
* sinOo (U+0D95): found 7, expected one of: [3, 4]
* sinAu (U+0D96): found 5, expected one of: [2, 3, 4]
* sinKha (U+0D9B): found 4, expected one of: [2, 3]
... and 70 others [code: contour-count]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Check math signs have the same width. (math_signs_width)</summary>
    <div>


> #,         It is a common practice to have math signs sharing the same width         (preferably the same width as tabular figures accross the entire font family).
> 
> This probably comes from the will to avoid additional tabular math signs knowing that their design can easily share the same width.




Original proposal: [https://github.com/fonttools/fontbakery/issues/3832]





- ⚠️ **WARN** The most common width is 554 among a set of 7  math glyphs.
The following math glyphs have a different width, though:
width=502: greater
width=511: multiply
width=470: minus
width=529: equal
width=462: divide
width=509: plus [code: width-outliers]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Ensure indic fonts have the Indian Rupee Sign glyph. (rupee)</summary>
    <div>


> Per Bureau of Indian Standards every font supporting one of the official Indian languages needs to include Unicode Character “₹” (U+20B9) Indian Rupee Sign.




Original proposal: [https://github.com/fonttools/fontbakery/issues/2967]





- ⚠️ **WARN** Font is missing the Indian Rupee Sign glyph. Please add a glyph for Indian Rupee Sign (₹) at codepoint U+20B9. [code: missing-rupee]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Does the font contain a soft hyphen? (soft_hyphen)</summary>
    <div>


> The 'Soft Hyphen' character (codepoint 0x00AD) is used to mark a hyphenation possibility within a word in the absence of or overriding dictionary hyphenation.
> 
> It is sometimes designed empty with no width (such as a control character), sometimes the same as the traditional hyphen, sometimes double encoded with the hyphen.
> 
> That being said, it is recommended to not include it in the font at all, because discretionary hyphenation should be handled at the level of the shaping engine, not the font. Also, even if present, the software would not display that character.
> 
> More discussion at: https://typedrawers.com/discussion/2046/special-dash-things-softhyphen-horizontalbar




Original proposal: [https://github.com/fonttools/fontbakery/issues/4046, https://github.com/fonttools/fontbakery/issues/3486]





- ⚠️ **WARN** This font has a 'Soft Hyphen' character. [code: softhyphen]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Check font contains no unreachable glyphs (unreachable_glyphs)</summary>
    <div>


> Glyphs are either accessible directly through Unicode codepoints or through        substitution rules.
> 
> In Color Fonts, glyphs are also referenced by the COLR table. And mathematical fonts also reference glyphs via the MATH table.
> 
> Any glyphs not accessible by these means are redundant and serve only to increase the font's file size.




Original proposal: [https://github.com/fonttools/fontbakery/issues/3160]





- ⚠️ **WARN** The following glyphs could not be reached by codepoint or substitution rules:

* uni030C.alt [code: unreachable-glyphs]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Shapes languages in all GF glyphsets. (googlefonts/glyphsets/shape_languages)</summary>
    <div>


> This check uses a heuristic to determine which GF glyphsets a font supports. Then it checks the font for correct shaping behaviour for all languages in those glyphsets.




Original proposal: [https://github.com/googlefonts/fontbakery/issues/4147]





- ⚠️ **WARN** Warning language shaping:

| Message                                                           | Languages                    |
|-------------------------------------------------------------------|------------------------------|
| Auxiliary orthography codepoints:                                 | * nl_Latn (Dutch)            |
|   The following auxiliary characters are missing from the font: Ĳ |                              |
|   The following auxiliary characters are missing from the font: ĳ |                              |
| Auxiliary orthography codepoints:                                 | * de_Latn (German)           |
|   The following auxiliary characters are missing from the font: ſ |                              |
| Auxiliary orthography codepoints:                                 | * fi_Latn (Finnish)          |
|   The following auxiliary characters are missing from the font: Ǥ |                              |
|   The following auxiliary characters are missing from the font: Ȟ |                              |
|   The following auxiliary characters are missing from the font: Ǩ |                              |
|   The following auxiliary characters are missing from the font: Ʒ |                              |
|   The following auxiliary characters are missing from the font: Ǯ |                              |
|   The following auxiliary characters are missing from the font: ǥ |                              |
|   The following auxiliary characters are missing from the font: ȟ |                              |
|   The following auxiliary characters are missing from the font: ǩ |                              |
|   The following auxiliary characters are missing from the font: ʒ |                              |
|   The following auxiliary characters are missing from the font: ǯ |                              |
| Auxiliary orthography codepoints:                                 | * fr_Latn (French)           |
|   The following auxiliary characters are missing from the font: Ǔ |                              |
|   The following auxiliary characters are missing from the font: ſ |                              |
|   The following auxiliary characters are missing from the font: ǔ |                              |
| Auxiliary orthography codepoints:                                 | * en_Latn (English)          |
|   The following auxiliary characters are missing from the font: ʻ |                              |
| Auxiliary orthography codepoints:                                 | * lt_Latn (Lithuanian)       |
|   Shaper didn't attach tildecomb to l when shaping the text 'l̃'   |                              |
| Auxiliary orthography codepoints:                                 | * nb_Latn (Norwegian Bokmål) |
|   The following auxiliary characters are missing from the font: Ǎ |                              |
|   The following auxiliary characters are missing from the font: ǎ |                              | [code: warning-language-shaping]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Font has correct separator glyphs? (googlefonts/separator_glyphs)</summary>
    <div>


> U+2028 and U+2029 should be present; otherwise tofu is displayed. (whitespace_ink will check that they are empty)




Original proposal: [https://github.com/fonttools/fontspector/issues/93]





- ⚠️ **WARN** Missing separator glyph U+2028 [code: missing-separator-glyphs]
  
  


- ⚠️ **WARN** Missing separator glyph U+2029 [code: missing-separator-glyphs]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Check the direction of the outermost contour in each glyph (outline_direction)</summary>
    <div>


> In TrueType fonts, the outermost contour of a glyph should be oriented clockwise, while the inner contours should be oriented counter-clockwise. Getting the path direction wrong can lead to rendering issues in some software.




Original proposal: [https://github.com/fonttools/fontbakery/issues/2056]





- ⚠️ **WARN** The following glyphs have a counter-clockwise outer contour:

* .notdef has a counter-clockwise outer contour
* sinA (U+0D85) has a counter-clockwise outer contour
* sinAa (U+0D86) has a counter-clockwise outer contour
* sinAa (U+0D86) has a counter-clockwise outer contour
* sinAa (U+0D86) has a counter-clockwise outer contour
* sinAa (U+0D86) has a counter-clockwise outer contour
* sinAe (U+0D87) has a counter-clockwise outer contour
* sinAe (U+0D87) has a counter-clockwise outer contour
* sinAe (U+0D87) has a counter-clockwise outer contour
... and 2295 others [code: ccw-outer-contour]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Do outlines contain any jaggy segments? (outline_jaggy_segments)</summary>
    <div>


> This check heuristically detects outline segments which form a particularly small angle, indicative of an outline error. This may cause false positives in cases such as extreme ink traps, so should be regarded as advisory and backed up by manual inspection.




Original proposal: [https://github.com/fonttools/fontbakery/issues/3064]





- ⚠️ **WARN** The following glyphs have jaggy segments:

* sinA (U+0D85): Quad(QuadBez { p0: (373.0, 42.0), p1: (363.0, 39.0), p2: (352.0, 37.0) })/Line(Line { p0: (352.0, 37.0), p1: (370.0, 37.0) }) = 10.304846468766044 degrees
* sinA (U+0D85): Line(Line { p0: (260.0, 35.0), p1: (271.0, 35.0) })/Quad(QuadBez { p0: (271.0, 35.0), p1: (210.0, 42.0), p2: (181.0, 76.0) }) = 6.546290783294054 degrees
* sinI (U+0D89): Quad(QuadBez { p0: (319.5, -50.5), p1: (306.0, -52.0), p2: (294.0, -53.0) })/Quad(QuadBez { p0: (294.0, -53.0), p1: (404.0, -23.0), p2: (475.5, 27.0) }) = 10.491477012331599 degrees
* sinIi (U+0D8A): Quad(QuadBez { p0: (312.0, 441.0), p1: (264.0, 416.0), p2: (232.0, 390.0) })/Quad(QuadBez { p0: (232.0, 390.0), p1: (262.0, 415.0), p2: (303.5, 441.5) }) = 0.7117122060358106 degrees
* sinRrVocalic (U+0D8E): Line(Line { p0: (907.0, 199.0), p1: (821.0, 198.0) })/Quad(QuadBez { p0: (821.0, 198.0), p1: (826.0, 197.0), p2: (830.0, 195.0) }) = 11.976132444203364 degrees
* sinE (U+0D91): Quad(QuadBez { p0: (218.0, 260.0), p1: (240.0, 267.0), p2: (263.0, 272.0) })/Quad(QuadBez { p0: (263.0, 272.0), p1: (250.0, 267.0), p2: (238.0, 261.0) }) = 8.772737297529394 degrees
* sinEe (U+0D92): Quad(QuadBez { p0: (219.0, 266.0), p1: (232.0, 269.0), p2: (245.0, 272.0) })/Quad(QuadBez { p0: (245.0, 272.0), p1: (238.0, 269.0), p2: (230.0, 266.0) }) = 10.203973721731737 degrees
* sinAi (U+0D93): Quad(QuadBez { p0: (470.0, 173.0), p1: (483.0, 223.0), p2: (475.0, 256.0) })/Line(Line { p0: (475.0, 256.0), p1: (475.0, 248.0) }) = 13.626994859891557 degrees
* sinAi (U+0D93): Quad(QuadBez { p0: (675.0, 266.0), p1: (686.0, 269.0), p2: (698.0, 272.0) })/Quad(QuadBez { p0: (698.0, 272.0), p1: (691.0, 269.0), p2: (685.0, 266.0) }) = 9.162347045721706 degrees
... and 454 others [code: found-jaggy-segments]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Check there are no overlapping path segments (overlapping_path_segments)</summary>
    <div>


> Some rasterizers encounter difficulties when rendering glyphs with overlapping path segments.
> 
> A path segment is a section of a path defined by two on-curve points. When two segments share the same coordinates, they are considered overlapping.




Original proposal: [https://github.com/google/fonts/issues/7594#issuecomment-2401909084]





- ⚠️ **WARN** The following glyphs have overlapping path segments:

* sinTVa: Quad(QuadBez { p0: (79.0, 53.0), p1: (79.0, 53.0), p2: (79.0, 53.0) }) has the same coordinates as a previous segment.
* sinTVa: Quad(QuadBez { p0: (79.0, 53.0), p1: (79.0, 53.0), p2: (79.0, 53.0) }) has the same coordinates as a previous segment.
* sinTTha: Quad(QuadBez { p0: (90.0, 53.0), p1: (90.0, 53.0), p2: (90.0, 53.0) }) has the same coordinates as a previous segment.
* sinTTha: Quad(QuadBez { p0: (90.0, 53.0), p1: (90.0, 53.0), p2: (90.0, 53.0) }) has the same coordinates as a previous segment.
* sinTTh.virama: Quad(QuadBez { p0: (90.0, 53.0), p1: (90.0, 53.0), p2: (90.0, 53.0) }) has the same coordinates as a previous segment.
* sinTTh.virama: Quad(QuadBez { p0: (90.0, 53.0), p1: (90.0, 53.0), p2: (90.0, 53.0) }) has the same coordinates as a previous segment.
* sinTI: Quad(QuadBez { p0: (264.0, 266.0), p1: (266.0, 268.0), p2: (269.0, 270.0) }) has the same coordinates as a previous segment.
* sinTVI: Quad(QuadBez { p0: (79.0, 53.0), p1: (79.0, 53.0), p2: (79.0, 53.0) }) has the same coordinates as a previous segment.
* sinTVI: Quad(QuadBez { p0: (79.0, 53.0), p1: (79.0, 53.0), p2: (79.0, 53.0) }) has the same coordinates as a previous segment.
... and 24 others [code: overlapping-path-segments]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Ensure fonts have ScriptLangTags declared on the 'meta' table. (googlefonts/meta/script_lang_tags)</summary>
    <div>


> The OpenType 'meta' table originated at Apple. Microsoft added it to OT with just two DataMap records:
> 
> - dlng: comma-separated ScriptLangTags that indicate which scripts,   or languages and scripts, with possible variants, the font is designed for.
> 
> - slng: comma-separated ScriptLangTags that indicate which scripts,   or languages and scripts, with possible variants, the font supports.
> 
> The slng structure is intended to describe which languages and scripts the font overall supports. For example, a Traditional Chinese font that also contains Latin characters, can indicate Hant,Latn, showing that it supports Hant, the Traditional Chinese variant of the Hani script, and it also supports the Latn script.
> 
> The dlng structure is far more interesting. A font may contain various glyphs, but only a particular subset of the glyphs may be truly "leading" in the design, while other glyphs may have been included for technical reasons. Such a Traditional Chinese font could only list Hant there, showing that it’s designed for Traditional Chinese, but the font would omit Latn, because the developers don’t think the font is really recommended for purely Latin-script use.
> 
> The tags used in the structures can comprise just script, or also language and script. For example, if a font has Bulgarian Cyrillic alternates in the locl feature for the cyrl BGR OT languagesystem, it could also indicate in dlng explicitly that it supports bul-Cyrl. (Note that the scripts and languages in meta use the ISO language and script codes, not the OpenType ones).
> 
> This check ensures that the font has the meta table containing the slng and dlng structures.
> 
> All families in the Google Fonts collection should contain the 'meta' table. Windows 10 already uses it when deciding on which fonts to fall back to. The Google Fonts API and also other environments could use the data for smarter filtering. Most importantly, those entries should be added to the Noto fonts.
> 
> In the font making process, some environments store this data in external files already. But the meta table provides a convenient way to store this inside the font file, so some tools may add the data, and unrelated tools may read this data. This makes the solution much more portable and universal.




Original proposal: [https://github.com/fonttools/fontbakery/issues/3349]





- ⚠️ **WARN** This font file does not have a 'meta' table. [code: lacks-meta-table]
  
  

</div>
</details>





<details>
    <summary>⚠️ <b>WARN</b> Check font follows the Google Fonts vertical metric schema (googlefonts/vertical_metrics)</summary>
    <div>


> This check generally enforces Google Fonts’ vertical metrics specifications. In particular: * lineGap must be 0 * Sum of hhea ascender + abs(descender) + linegap must be   between 120% and 200% of UPM * Warning if sum is over 150% of UPM
> 
> The threshold levels 150% (WARN) and 200% (FAIL) are somewhat arbitrarily chosen and may hint at a glaring mistake in the metrics calculations or UPM settings.
> 
> Our documentation includes further information: https://github.com/googlefonts/gf-docs/tree/main/VerticalMetrics




Original proposal: [https://github.com/fonttools/fontbakery/pull/3762 and https://github.com/fonttools/fontbakery/pull/3921]





- ⚠️ **WARN** We recommend the absolute sum of the hhea metrics should be between 1.2-1.5x of the font's upm. This font has 1.553x (1553) [code: bad-hhea-range]
  
  

</div>
</details>


</div>
</details>






### Summary

| 🔥 FAIL | ⚠️ WARN | ℹ️ INFO | ✅ PASS | ⏩ SKIP | 
| ---|---|---|---|---|
| 5 | 23 | 6 | 91 | 84 | 
| 2% | 11% | 3% | 44% | 40% | 



