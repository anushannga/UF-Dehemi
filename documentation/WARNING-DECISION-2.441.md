# Candidate warning decision, 13 October 2026

Keep the current drawings for the next review candidate. This targeted review did not establish a visible defect that justifies changing the preserved hinted Italic. The eight raw warnings remain eight warnings; no checks or severities were changed.

The five existing contour proof pages were visually reviewed: all 81 flagged encoded glyphs have recognizable forms and visible accents/punctuation at 112 px. Disconnected ink cuts account for many count differences. This supports retaining the design for review, not certifying every contour or typographic quality.

New direct-glyph proofs cover 12 selected glyphs in both styles at 24, 48 and 112 px: [jaggy representatives](review-2.441/targeted-outlines-1.png), [overlap representatives](review-2.441/targeted-outlines-2.png). These include sinA, sinI, sinIi, sinKa, sinRa, sinSa, sinTVa, sinTTha, sinTTh.virama, sinTI, sinTVI and sinAa. In these proofs the forms remain recognizable; no gross filled counter, missing body or isolated spike was apparent. They are direct FreeType renders, not new shaping or application tests. Existing platform regression results cover their recorded text corpus separately.

| Warning | Decision |
| --- | --- |
| contour_count, both styles | Retain textured design; submit the 81-glyph proofs. The reference counts are heuristic. |
| outline_jaggy_segments, both styles | Retain for review. Raw metadata contains 463 segment records in 282 Italic glyphs and 413 in 276 Regular glyphs. The new proofs are representative, not exhaustive certification of these records. |
| overlapping_path_segments, Italic | Retain original hinting. Several displayed records are zero-length quadratic segments, while sinTI includes a retraced nonzero segment. Neither implies a visible broken letter by itself. Removing points changes indices used by hint programs; previous broad cleanup attempts regressed results. |
| outline_direction, Italic | Keep as an unresolved technical warning with recorded rendering evidence. The raw message reports many contours; successful rendering is not a proof that winding is ideal. |
| unreachable_subsetting, both styles | Hand to onboarding maintainers, following their existing guidance. Do not reopen the rejected cross-subset proposal. Full downloadable TTFs and hosted subsets have different coverage responsibilities. |

Reproduction: `python sources/warning_proofs.py` with the existing review dependencies (fontTools, freetype-py and Pillow). The script uses Windows Arial for labels. [Inventory and exact candidate hashes](../qa/warning-triage-2.441.json). The candidate TTF bytes were not modified by this review.

Next delivery step: merge the tested repository/licensing candidate and publish it as a prerelease for curator review. Describe the remaining warnings and Maname-derived design plainly. Ask for a specific design/onboarding assessment in one concise update; repeated technical status comments will not produce acceptance. Google Fonts acceptance remains a curator decision.
