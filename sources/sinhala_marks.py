"""Focused Sinhala mark attachment, retaining the original glyph artwork.

Call this in the original italic coordinate space, before unskew_positioning.
The fontmake target must pass the original italic layout/outline reference even
when its output outlines have already been made upright.
"""

from statistics import median

from fontTools.misc.roundTools import otRound
from fontTools.otlLib.builder import (
    buildAnchor,
    buildLookup,
    buildMarkBasePosSubtable,
)


def attach_virama_to_dotted_circle(font, reference=None):
    """Add only sinVirama -> U+25CC to the existing abvm feature.

The virama's attachment point and optical placement are derived from the
upstream mark-to-base layout. The median inset from the upper/right outline
bounds of Sha, Ssa, Sa, Ha, Lla and Fa is applied to the dotted circle. This
places the existing virama at the circle's upper-right edge, in the same way
the upstream layout places it on those consonants. No artificial displacement
is added just to satisfy a QA detector.

With the Tight-232 italic reference this produces mark anchor (111, 382),
base anchor (428, 368), and mark origin (317, -14) relative to the base origin.
The circle and mark retain their outlines, hints and advances. Only GPOS is
changed, and the new lookup covers no normal Sinhala consonant.

Return the derived anchors/insets for the validation report. Repeated calls
before unskew are harmless. A call after unskew is rejected to prevent a
second or mixed-coordinate transformation.
    """
    if getattr(font, "_ufdehemi_positioning_transform", None) is not None:
        raise ValueError("Attach dotted-circle virama before unskew_positioning")
    reference = font if reference is None else reference
    if "GPOS" not in font or "GPOS" not in reference:
        raise ValueError("Dotted-circle attachment requires the maintained GPOS layout")
    mark = font.getBestCmap().get(0x0DCA)
    dotted_circle = font.getBestCmap().get(0x25CC)
    reference_mark = reference.getBestCmap().get(0x0DCA)
    reference_circle = reference.getBestCmap().get(0x25CC)
    if not all((mark, dotted_circle, reference_mark, reference_circle)):
        raise ValueError("Both font and reference must map virama and dotted circle")
    if font["GDEF"].table.GlyphClassDef.classDefs.get(mark) != 3:
        raise ValueError("Virama must remain in GDEF mark class 3")

    # Reuse the maintained virama mark anchor and derive the placement from
    # actual upstream consonant anchors. Bounding boxes must exist in the
    # reference; reading them does not alter glyf point order or instructions.
    sample_names = {"sinSha", "sinSsa", "sinSa", "sinHa", "sinLla", "sinFa"}
    anchor_pair = None
    insets = {}
    for lookup in reference["GPOS"].table.LookupList.Lookup:
        if lookup.LookupType != 4:
            continue
        for subtable in lookup.SubTable:
            if reference_mark not in subtable.MarkCoverage.glyphs:
                continue
            record = subtable.MarkArray.MarkRecord[
                subtable.MarkCoverage.glyphs.index(reference_mark)
            ]
            if record.MarkAnchor is None:
                continue
            pair = (record.MarkAnchor.XCoordinate, record.MarkAnchor.YCoordinate)
            for name, base_record in zip(
                subtable.BaseCoverage.glyphs, subtable.BaseArray.BaseRecord
            ):
                if name not in sample_names or name in insets:
                    continue
                anchor = base_record.BaseAnchor[record.Class]
                if anchor is None:
                    continue
                if anchor_pair is None:
                    anchor_pair = pair
                elif anchor_pair != pair:
                    raise ValueError("Reference virama anchors disagree")
                glyph = reference["glyf"][name]
                insets[name] = (
                    glyph.xMax - anchor.XCoordinate,
                    glyph.yMax - anchor.YCoordinate,
                )
    if anchor_pair is None or set(insets) != sample_names:
        raise ValueError("The complete reviewed upstream virama placement reference is missing")
    right_inset = otRound(median(pair[0] for pair in insets.values()))
    top_inset = otRound(median(pair[1] for pair in insets.values()))
    circle_glyph = reference["glyf"][reference_circle]
    base_pair = (circle_glyph.xMax - right_inset, circle_glyph.yMax - top_inset)
    result = {
        "reference_coordinate_space": "original italic before unskew",
        "mark_anchor": list(anchor_pair),
        "dotted_circle_anchor": list(base_pair),
        "right_inset": right_inset,
        "top_inset": top_inset,
        "reference_glyphs": sorted(insets),
    }

    table = font["GPOS"].table
    abvm = [
        (index, record.Feature)
        for index, record in enumerate(table.FeatureList.FeatureRecord)
        if record.FeatureTag == "abvm"
    ]
    if not abvm:
        raise ValueError("The maintained layout must supply an abvm feature")
    required_scripts = {"DFLT", "sinh"}
    for script in table.ScriptList.ScriptRecord:
        if script.ScriptTag not in required_scripts:
            continue
        default = script.Script.DefaultLangSys
        if default is None or not any(index in default.FeatureIndex for index, _ in abvm):
            raise ValueError(f"abvm must be registered for {script.ScriptTag} default language")
        required_scripts.remove(script.ScriptTag)
    if required_scripts:
        raise ValueError(f"Missing required layout scripts: {sorted(required_scripts)}")

    # Avoid appending an identical lookup when a caller invokes this twice.
    # Fresh feature compilation removes the prior lookup, so it will be added
    # again even when the same TTFont instance is reused by the build.
    for index, lookup in enumerate(table.LookupList.Lookup):
        if lookup.LookupType != 4:
            continue
        for subtable in lookup.SubTable:
            if (
                subtable.MarkCoverage.glyphs != [mark]
                or subtable.BaseCoverage.glyphs != [dotted_circle]
            ):
                continue
            record = subtable.MarkArray.MarkRecord[0]
            mark_anchor = record.MarkAnchor
            base_anchor = subtable.BaseArray.BaseRecord[0].BaseAnchor[record.Class]
            if (
                mark_anchor is not None and base_anchor is not None
                and (mark_anchor.XCoordinate, mark_anchor.YCoordinate) == anchor_pair
                and (base_anchor.XCoordinate, base_anchor.YCoordinate) == base_pair
                and all(index in feature.LookupListIndex for _, feature in abvm)
            ):
                result["lookup_index"] = index
                return result

    lookup = buildLookup([
        buildMarkBasePosSubtable(
            {mark: (0, buildAnchor(*anchor_pair))},
            {dotted_circle: {0: buildAnchor(*base_pair)}},
            font.getReverseGlyphMap(),
        )
    ])
    index = len(table.LookupList.Lookup)
    table.LookupList.Lookup.append(lookup)
    table.LookupList.LookupCount = len(table.LookupList.Lookup)
    for _, feature in abvm:
        feature.LookupListIndex.append(index)
        feature.LookupCount = len(feature.LookupListIndex)
    result["lookup_index"] = index
    return result
