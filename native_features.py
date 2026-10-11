"""Compile editable OpenType features and transform upright positioning.

The feature source began as a FontForge export of the original Tight-232
layout. It is compiled by feaLib rather than copied from a binary font. The
small language policy below preserves the original Dutch aalt exclusion.
"""

from pathlib import Path

from fontTools.feaLib.builder import addOpenTypeFeatures
from fontTools.misc.roundTools import otRound
from fontTools.ttLib.tables import otTables
from fontTools.ttLib.tables.otBase import ValueRecord


FEATURE_SOURCE = Path(__file__).resolve().parent / "sources" / "features.fea"


def compile_features(font, source=FEATURE_SOURCE):
    """Build native GSUB/GPOS/GDEF from FEA without changing glyph outlines.

feaLib's aalt feature applies to every declared language system. Tight-232
intentionally did not register aalt for Dutch, so retain that source policy.
Feature-name records may be added to the name table by feaLib.
    """
    addOpenTypeFeatures(font, str(source))
    # Recompilation supplies fresh, unsheared positioning objects.
    if hasattr(font, "_ufdehemi_positioning_transform"):
        del font._ufdehemi_positioning_transform
    if "GSUB" not in font:
        return
    table = font["GSUB"].table
    for record in table.ScriptList.ScriptRecord:
        if record.ScriptTag != "latn":
            continue
        for language in record.Script.LangSysRecord:
            if language.LangSysTag != "NLD ":
                continue
            language.LangSys.FeatureIndex = [
                index
                for index in language.LangSys.FeatureIndex
                if table.FeatureList.FeatureRecord[index].FeatureTag != "aalt"
            ]
            language.LangSys.FeatureCount = len(language.LangSys.FeatureIndex)


def _objects(root):
    """Visit shared OpenType objects once, including extension subtables."""
    pending = [root]
    visited = set()
    while pending:
        value = pending.pop()
        if value is None or isinstance(value, (str, bytes, int, float, bool)):
            continue
        identity = id(value)
        if identity in visited:
            continue
        visited.add(identity)
        if isinstance(value, dict):
            pending.extend(value.values())
        elif isinstance(value, (list, tuple)):
            pending.extend(value)
        elif hasattr(value, "__dict__"):
            yield value
            pending.extend(vars(value).values())


def _formats(values):
    result = 0
    for value in values:
        if value is not None:
            result |= value.getFormat()
    return result


def unskew_positioning(font, shear):
    """Apply x' = x + shear*y to anchors and GPOS vectors exactly once.

Use the same shear as the outline transformation. Shared anchors/value
records are visited once. Calling this twice with the same shear is a no-op;
using a different shear on an already transformed font raises an error.
Y-device tables require a size-dependent transformation and are rejected
before mutation. Current static sources do not contain those tables.
    """
    previous = getattr(font, "_ufdehemi_positioning_transform", None)
    if previous is not None:
        if previous[0] != shear:
            raise ValueError("Positioning was already transformed with another shear")
        return previous[1]
    if "GPOS" not in font:
        result = {"anchors": 0, "value_records": 0}
        font._ufdehemi_positioning_transform = (shear, result)
        return result

    objects = list(_objects(font["GPOS"].table))
    for value in objects:
        if isinstance(value, otTables.Anchor):
            if getattr(value, "YDeviceTable", None) is not None:
                raise ValueError("Y anchor devices cannot be sheared as static coordinates")
        elif isinstance(value, ValueRecord):
            if any(
                getattr(value, name, None) is not None
                for name in ("YPlaDevice", "YAdvDevice")
            ):
                raise ValueError("Y positioning devices need size-dependent transformation")

    result = {"anchors": 0, "value_records": 0}
    for value in objects:
        if isinstance(value, otTables.Anchor):
            value.XCoordinate = otRound(value.XCoordinate + shear * value.YCoordinate)
            result["anchors"] += 1
        elif isinstance(value, ValueRecord):
            changed = False
            for x_name, y_name in (
                ("XPlacement", "YPlacement"),
                ("XAdvance", "YAdvance"),
            ):
                y_value = getattr(value, y_name, 0)
                if y_value:
                    setattr(
                        value,
                        x_name,
                        otRound(getattr(value, x_name, 0) + shear * y_value),
                    )
                    changed = True
            result["value_records"] += int(changed)

    # A pure-Y record may have acquired an X field. Keep binary value formats
    # consistent with the fields that the transformation now emits.
    for value in objects:
        if isinstance(value, otTables.SinglePos):
            records = value.Value if isinstance(value.Value, list) else [value.Value]
            value.ValueFormat = _formats(records)
        elif isinstance(value, otTables.PairPos):
            if value.Format == 1:
                pairs = [
                    pair
                    for pair_set in value.PairSet
                    for pair in pair_set.PairValueRecord
                ]
            else:
                pairs = [
                    pair
                    for class_one in value.Class1Record
                    for pair in class_one.Class2Record
                ]
            value.ValueFormat1 = _formats(pair.Value1 for pair in pairs)
            value.ValueFormat2 = _formats(pair.Value2 for pair in pairs)

    font._ufdehemi_positioning_transform = (shear, result)
    return result
