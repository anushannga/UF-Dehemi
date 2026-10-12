"""Add auxiliary Latin coverage without changing existing outlines or hints.

Call add_latin_extensions after compiling the maintained feature source and
before transforming the Regular outlines/positioning. For a fontmake outline
build which already contains these glyphs, call apply_latin_positioning with
the equivalent italic-space reference before the Regular positioning transform.

New accent/ligature glyphs use this font's existing matching components. Ezh,
long s and the added G/g bars are new drawings, not foreign font outlines.
These new designs need human review. The separate caron_components module
retains the existing alternate-caron point order/instructions while maintaining
the actual body and distinctive accent drawings as editable components.

Character identities/reference forms: Unicode Latin Extended-A/B, IPA
Extensions and Spacing Modifier Letters charts at https://unicode.org/charts/.
"""

from math import radians, tan

from fontTools.misc.roundTools import otRound
from fontTools.otlLib.builder import (
    buildAnchor, buildLookup, buildMarkBasePosSubtable,
)
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.reverseContourPen import ReverseContourPen


SHEAR = tan(radians(14))
CARON_BASES = {
    0x01CD: "A", 0x01CE: "a", 0x01D3: "U", 0x01D4: "u",
    0x021E: "H", 0x021F: "h", 0x01E8: "K", 0x01E9: "k",
    0x01EE: "uni01B7", 0x01EF: "uni0292",
}
AUXILIARY_CODEPOINTS = tuple(sorted((
    *CARON_BASES, 0x0132, 0x0133, 0x02BB, 0x01E4, 0x01E5,
    0x01B7, 0x0292, 0x017F,
)))
MANUAL_CARON_REVIEW = ("Lcaron", "dcaron", "lcaron", "tcaron")


def _add(font, codepoint, glyph, width):
    name = f"uni{codepoint:04X}"
    cmap = font.getBestCmap()
    if codepoint in cmap:
        return cmap[codepoint], False
    if name in font.getGlyphOrder():
        raise ValueError(f"Unmapped glyph name already exists: {name}")
    order = font.getGlyphOrder()[:]
    font["glyf"][name] = glyph
    font["hmtx"].metrics[name] = (width, 0)
    font.setGlyphOrder(order + [name])
    glyph.recalcBounds(font["glyf"])
    font["hmtx"].metrics[name] = (width, getattr(glyph, "xMin", 0))
    for table in font["cmap"].tables:
        if table.isUnicode():
            table.cmap[codepoint] = name
    return name, True


def _component_glyph(font, parts):
    pen = TTGlyphPen(font.getGlyphSet())
    for name, x, y in parts:
        pen.addComponent(name, (1, 0, 0, 1, otRound(x), otRound(y)))
    return pen.glyph()


def _top_anchor(font, name):
    # Reuse the maintained FEA's existing top anchor where it exists.
    if "GPOS" in font:
        for lookup in font["GPOS"].table.LookupList.Lookup:
            if lookup.LookupType != 4:
                continue
            for table in lookup.SubTable:
                if "uni030C" not in table.MarkCoverage.glyphs:
                    continue
                if name not in table.BaseCoverage.glyphs:
                    continue
                mark = table.MarkArray.MarkRecord[
                    table.MarkCoverage.glyphs.index("uni030C")
                ]
                anchor = table.BaseArray.BaseRecord[
                    table.BaseCoverage.glyphs.index(name)
                ].BaseAnchor[mark.Class]
                if anchor is not None:
                    return anchor.XCoordinate, anchor.YCoordinate
    glyph = font["glyf"][name]
    glyph.recalcBounds(font["glyf"])
    top = glyph.yMax + 35
    # Center in upright space, then restore the font's original italic shear.
    middle_y = (glyph.yMin + glyph.yMax) / 2
    middle_x = (glyph.xMin + glyph.xMax) / 2
    return otRound(middle_x + SHEAR * (top - middle_y)), top


def _barred_g(font, base, small=False):
    # A new horizontal bar is part of the new glyph only. Keep the base's
    # ink details and counter outlines intact; no existing glyph is edited.
    pen = TTGlyphPen(None)
    font.getGlyphSet()[base].draw(pen)
    draw = TransformPen(pen, (1, 0, SHEAR, 1, 0, 0))
    left, right, bottom, top = (0, 565, -92, -55) if small else (30, 515, 268, 306)
    # The copied upstream outer outlines have positive winding. Match it
    # here so overlap with a stem fills rather than cancelling that stem.
    draw.moveTo((left, bottom)); draw.lineTo((right, bottom))
    draw.lineTo((right, top)); draw.lineTo((left, top)); draw.closePath()
    return pen.glyph()


def _ezh(small=False):
    # Authored Z-like upper stroke with a curved lower bowl. The lowercase
    # has x-height 489 and a descender near -211; it is not an alias for z/3.
    pen = TTGlyphPen(None)
    sx, sy, dy = (0.8, 700 / 660, -190) if small else (1, 1, 0)
    # Match the positive winding of the existing caron component. A composite
    # Ezh+caron must have consistent outer contours before the Regular builder
    # performs its whole-glyph clockwise normalization. Only this new Ezh
    # drawing is reversed; the original caron and old glyphs stay untouched.
    draw = TransformPen(ReverseContourPen(pen),
                        (sx, 0, SHEAR * sy, sy, SHEAR * dy, dy))
    draw.moveTo((50, 640)); draw.lineTo((440, 640))
    draw.lineTo((440, 600)); draw.lineTo((230, 360))
    draw.qCurveTo((440, 365), (465, 210))
    draw.qCurveTo((465, -20), (225, -20))
    draw.qCurveTo((90, -20), (30, 80)); draw.lineTo((68, 116))
    draw.qCurveTo((122, 36), (218, 36))
    draw.qCurveTo((350, 36), (350, 205))
    draw.qCurveTo((350, 340), (190, 320))
    draw.lineTo((136, 352)); draw.lineTo((344, 590))
    draw.lineTo((50, 590)); draw.closePath()
    return pen.glyph()


def _long_s():
    # An independently drawn ascending long-s form, without f's crossbar.
    pen = TTGlyphPen(None)
    draw = TransformPen(pen, (1, 0, SHEAR, 1, 0, 0))
    draw.moveTo((58, 0)); draw.lineTo((58, 32))
    draw.qCurveTo((90, 32), (90, 95)); draw.lineTo((90, 550))
    draw.qCurveTo((90, 715), (240, 715))
    draw.qCurveTo((305, 715), (332, 663)); draw.lineTo((300, 631))
    draw.qCurveTo((283, 670), (247, 670))
    draw.qCurveTo((180, 670), (180, 560)); draw.lineTo((180, 95))
    draw.qCurveTo((180, 34), (214, 32)); draw.lineTo((214, 0))
    draw.closePath()
    return pen.glyph()


def add_latin_extensions(font):
    """Add 18 actual auxiliary characters and italic-space Latin attachment.

    Existing glyph entries/coordinates/programs are never replaced. The added
    designs are unhinted; the caller must keep them under visual review.
    """
    added = []

    def put(cp, glyph, width):
        name, created = _add(font, cp, glyph, width)
        if created:
            added.append(name)

    for cp, components in [(0x0132, ("I", "J")), (0x0133, ("i", "j"))]:
        first, second = components
        advance = font["hmtx"].metrics[first][0]
        put(cp, _component_glyph(font, [(first, 0, 0), (second, advance, 0)]),
            advance + font["hmtx"].metrics[second][0])
    # Turned comma has the same appropriate left-quotation shape in this
    # design, but receives its own encoded glyph/advance rather than sharing
    # a cmap entry with an unrelated right apostrophe.
    put(0x02BB, _component_glyph(font, [("quoteleft", 0, 0)]),
        font["hmtx"].metrics["quoteleft"][0])
    put(0x01E4, _barred_g(font, "G"), font["hmtx"].metrics["G"][0])
    put(0x01E5, _barred_g(font, "g", small=True), font["hmtx"].metrics["g"][0])
    put(0x01B7, _ezh(), 650)
    put(0x0292, _ezh(small=True), 530)
    put(0x017F, _long_s(), 510)
    for cp, base in CARON_BASES.items():
        anchor_x, anchor_y = _top_anchor(font, base)
        put(cp, _component_glyph(font, [
            (base, 0, 0), ("uni030C", anchor_x - 112, anchor_y - 426)
        ]), font["hmtx"].metrics[base][0])
    positioning = apply_latin_positioning(font, reference=font)
    return {
        "added_glyphs": added,
        "auxiliary_codepoints": [f"U+{cp:04X}" for cp in AUXILIARY_CODEPOINTS],
        "positioning": positioning,
        "manual_caron_review": list(MANUAL_CARON_REVIEW),
        "new_drawing_review": ["uni01E4", "uni01E5", "uni01B7", "uni0292", "uni017F"],
    }


def apply_latin_positioning(font, reference):
    """Generate Latin mark attachment from the equivalent italic reference.

    This is source-driven lookup construction, not a copied binary layout.
    Call before unskew_positioning for Regular. All added bases and the two
    formerly unclassified l/k bases receive top-mark anchors; l+tilde is the
    specific existing Latin sequence corrected by this lookup.
    """
    if getattr(font, "_dehemi_latin_positioning", False):
        return {"already_applied": True}
    cmap = font.getBestCmap()
    names = ["l", "k"] + [cmap[cp] for cp in AUXILIARY_CODEPOINTS if cp in cmap]
    classes = font["GDEF"].table.GlyphClassDef.classDefs
    for name in names:
        classes[name] = 1
    # These anchors are the original maintained FEA's italic-space top-mark
    # anchors. Separate classes retain their different geometric origins.
    mark_anchors = {
        "uni0308": (110, 426), "uni0307": (112, 426),
        "gravecomb": (112, 426), "uni030B": (112, 426),
        "uni030C": (112, 426), "acutecomb": (125, 478),
        "uni030A": (125, 478), "uni0302": (125, 479),
        "uni0306": (116, 447), "tildecomb": (124, 478),
        "uni0304": (111, 426), "hookabovecomb": (111, 426),
        "uni030F": (111, 426), "uni0311": (111, 426),
        "uni0312": (111, 426), "uni031B": (111, 426),
    }
    marks = {}
    grouped = {}
    for name, coordinates in mark_anchors.items():
        if name not in font.getGlyphOrder():
            continue
        mark_class = grouped.setdefault(coordinates, len(grouped))
        marks[name] = (mark_class, buildAnchor(*coordinates))
    bases = {}
    for name in names:
        x, y = _top_anchor(reference, name)
        bases[name] = {i: buildAnchor(x, y) for i in range(len(grouped))}
    lookup = buildLookup([buildMarkBasePosSubtable(marks, bases, font.getReverseGlyphMap())])
    table = font["GPOS"].table
    index = len(table.LookupList.Lookup)
    table.LookupList.Lookup.append(lookup)
    table.LookupList.LookupCount = len(table.LookupList.Lookup)
    mark_features = [r for r in table.FeatureList.FeatureRecord if r.FeatureTag == "mark"]
    if not mark_features:
        raise ValueError("Maintained feature source has no Latin mark feature")
    for record in mark_features:
        record.Feature.LookupListIndex.append(index)
        record.Feature.LookupCount = len(record.Feature.LookupListIndex)
    font._dehemi_latin_positioning = True
    return {"bases": names, "lookup_index": index, "mark_classes": len(grouped)}
