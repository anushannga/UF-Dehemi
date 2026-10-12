"""Normalize unhinted Regular contours while retaining their filled geometry.

Original Italic point order and hint instructions must remain untouched. The
tiny, non-identical sinTI quadratic spike is deliberately retained for review.
"""
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.reverseContourPen import ReverseContourPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.areaPen import AreaPen
from math import tan, radians, dist
from fontTools.misc.roundTools import otRound


def _align_axes(glyph, max_shift):
    """Bounded corrections of almost-axis straight lines, never curves."""
    if glyph.numberOfContours <= 0:
        return 0, 0.0
    old = list(glyph.coordinates)
    coordinates = glyph.coordinates
    flags = glyph.flags
    tolerance = tan(radians(0.51))
    for _ in range(8):
        changed = False
        start = 0
        for end in glyph.endPtsOfContours:
            for index in range(start, end + 1):
                other = start if index == end else index + 1
                if not (flags[index] & 1 and flags[other] & 1):
                    continue
                x, y = coordinates[index]
                xx, yy = coordinates[other]
                dx, dy = xx - x, yy - y
                if dx and dy and abs(dx / dy) < tolerance:
                    target = otRound((x + xx) / 2)
                    coordinates[index] = (target, y)
                    coordinates[other] = (target, yy)
                    changed = True
                elif dx and dy and abs(dy / dx) < tolerance:
                    target = otRound((y + yy) / 2)
                    coordinates[index] = (x, target)
                    coordinates[other] = (xx, target)
                    changed = True
            start = end + 1
        if not changed:
            break
    shifts = [dist(a, b) for a, b in zip(old, coordinates)]
    maximum = max(shifts, default=0)
    if maximum > max_shift:
        raise ValueError(f'Axis correction {maximum} exceeds {max_shift} design units')
    return sum(value != 0 for value in shifts), maximum


def normalize_regular_outlines(font, snap_axes=False, max_axis_shift=3):
    """Drop zero-length/zero-area line paths, then correct original winding.

    Apply to the canonical unhinted Regular derivation before serialization.
    This helper accepts only the unhinted Regular style. It never modifies glyph
    metrics, names, cmap or layout. Whole-glyph signed area selects reversal;
    already clockwise new drawings are preserved. Individual hole contours
    are never flipped independently, which would change nonzero filled areas.
    Optional axis alignment is a bounded design correction, separately from the
    geometric-equivalent winding/degenerate cleanup. It requires visual review.
    """
    if font['name'].getDebugName(2) != 'Regular':
        raise ValueError('Outline normalization is restricted to Regular')
    prior = getattr(font, '_dehemi_regular_outline_cleanup', None)
    if prior is not None:
        if prior['axis_alignment_requested'] != snap_axes:
            raise ValueError('Outlines were already normalized with different axis options')
        return prior
    for name in font.getGlyphOrder():
        program = getattr(font['glyf'][name], 'program', None)
        if program is not None and program.getBytecode():
            raise ValueError(f'Cannot reorder hinted glyph points: {name}')
    source = font.getGlyphSet()
    fresh = {}
    stats = {'zero_segments_removed': 0, 'zero_area_line_contours_removed': 0,
             'glyphs_reoriented': 0, 'retained_nonidentical_retrace': 'sinTI',
             'axis_points_adjusted': 0, 'axis_glyphs_adjusted': 0,
             'max_axis_shift': 0.0, 'axis_alignment_requested': snap_axes,
             'ambiguous_zero_signed_area_glyphs': [],
             'cleanup_area_magnitude_max_difference': 0.0}
    for name in font.getGlyphOrder():
        recording = DecomposingRecordingPen(source)
        source[name].draw(recording)
        output = []
        contour = []
        position = None
        for operation, arguments in recording.value:
            if operation == 'moveTo':
                contour = []
                position = arguments[0]
            elif operation in ('lineTo', 'qCurveTo'):
                if position is not None and all(p == position for p in arguments):
                    stats['zero_segments_removed'] += 1
                    continue
                position = arguments[-1]
            contour.append((operation, arguments))
            if operation in ('closePath', 'endPath'):
                points = [p for _, args in contour for p in args if p is not None]
                axis_line = points and (
                    len({p[0] for p in points}) == 1 or
                    len({p[1] for p in points}) == 1
                )
                two_point_line = (
                    len(set(points)) <= 2 and all(
                        op in ('moveTo', 'lineTo', 'closePath', 'endPath')
                        for op, _ in contour
                    )
                )
                if not points or axis_line or two_point_line:
                    stats['zero_area_line_contours_removed'] += 1
                else:
                    output.extend(contour)
                # An all-off-curve TrueType contour starts with qCurveTo(...,
                # None) and has no moveTo. Reset here rather than relying on
                # the next contour to contain moveTo.
                contour = []
                position = None
        recording.value = output
        pen = TTGlyphPen(None)
        area = AreaPen(None)
        recording.replay(area)
        if area.value > 0:
            recording.replay(ReverseContourPen(pen))
            stats['glyphs_reoriented'] += bool(output)
        else:
            recording.replay(pen)
            if output and area.value == 0:
                stats['ambiguous_zero_signed_area_glyphs'].append(name)
        fresh[name] = pen.glyph()
        checked_area = AreaPen(None)
        fresh[name].draw(checked_area, {})
        difference = abs(abs(checked_area.value) - abs(area.value))
        stats['cleanup_area_magnitude_max_difference'] = max(
            stats['cleanup_area_magnitude_max_difference'], difference
        )
        if difference > 1e-7:
            raise ValueError(f'Cleanup changed the curve area of {name}: {difference}')
        if snap_axes:
            count, shift = _align_axes(fresh[name], max_axis_shift)
            stats['axis_points_adjusted'] += count
            stats['axis_glyphs_adjusted'] += bool(count)
            stats['max_axis_shift'] = max(stats['max_axis_shift'], shift)
    for name, glyph in fresh.items():
        font['glyf'][name] = glyph
    font._dehemi_regular_outline_cleanup = stats
    return stats

def remove_regular_tiny_retrace(font, allow_absent=False):
    """Remove sinTI's tiny out-and-back quadratic nib in unhinted Regular.

    This is a real geometric correction, not exact-area normalization. The
    measured change is 1.333 square design units; bounds/advance stay unchanged.
    Original hinted Italic is not processed. Fontmake sources already contain
    the correction, so their native build may legitimately find no retrace.
    """
    if font['name'].getDebugName(2)!='Regular':
        raise ValueError('Tiny retrace correction is restricted to Regular')
    glyph=font['glyf']['sinTI']
    if getattr(glyph,'program',None) and glyph.program.getBytecode():
        raise ValueError('Cannot remove hinted points')
    rec=DecomposingRecordingPen(font.getGlyphSet())
    font.getGlyphSet()['sinTI'].draw(rec)
    before=AreaPen(None);rec.replay(before)
    output=[];position=None;index=0;removed=0
    while index<len(rec.value):
        operation,args=rec.value[index]
        if operation=='qCurveTo' and len(args)==2 and index+1<len(rec.value):
            following,next_args=rec.value[index+1]
            if following=='qCurveTo' and len(next_args)==2 and next_args[-1]==position and max(abs(a-b) for a,b in zip(args[0],next_args[0]))<=1:
                removed+=1;index+=2;continue
        output.append((operation,args))
        if operation in ('moveTo','lineTo','qCurveTo'):position=args[-1]
        elif operation=='closePath':position=None
        index+=1
    if removed==0 and allow_absent:return {'removed_pairs':0,'already_corrected':True}
    if removed!=1:raise ValueError(f'Unexpected sinTI retrace count: {removed}')
    rec.value=output;after=AreaPen(None);rec.replay(after)
    difference=abs(before.value-after.value)
    if difference>2:raise ValueError('Tiny retrace change exceeded area bound')
    original_bounds=(glyph.xMin,glyph.yMin,glyph.xMax,glyph.yMax)
    pen=TTGlyphPen(None);rec.replay(pen)
    corrected=pen.glyph();corrected.recalcBounds(font['glyf'])
    if (corrected.xMin,corrected.yMin,corrected.xMax,corrected.yMax)!=original_bounds:
        raise ValueError('Tiny retrace correction changed bounds')
    font['glyf']['sinTI']=corrected
    return {'removed_pairs':removed,'area_change_square_design_units':difference,'bounds_unchanged':True}
