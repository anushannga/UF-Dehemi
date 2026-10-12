# Dehemi: proposed Google Fonts serving coverage review

Status: **proposal for curator review; not an applied Google Fonts serving fix**.
Submitted as [draft PR 32](https://github.com/googlefonts/nam-files/pull/32). The overlap test is not green: seven new cross-subset conflicts require a maintainer policy decision. No deployment is claimed.
The adjacent [SUBSET-COVERAGE-PROPOSAL.patch](SUBSET-COVERAGE-PROPOSAL.patch) targets
the upstream `googlefonts/nam-files` repository. It does not modify the published
Dehemi fonts, turn off a QA check, or claim that Google has accepted the proposal.

## What the baseline check actually examined

The v2.420 baseline was checked with Fontspector 1.9.0. There is no `METADATA.pb`
in this project. In that situation,
[`googlefonts/metadata/unreachable_subsetting`](https://github.com/fonttools/fontspector/blob/main/profile-googlefonts/src/checks/googlefonts/metadata/unreachable_subsetting.rs)
infers subsets with `subsets_in_font(codepoints, 50.0, Some(0.01))` and compares
encoded characters against compiled subset lists. For these fonts it inferred
`latin`, `latin-ext`, `sinhala` and `vietnamese`.

The report wording refers to metadata even when that file is absent. This is a
prediction based on inferred subset declarations and the checker's data. Dehemi
is not yet an accepted, live Google Fonts API family, so this is not an observed
failure of a deployed Google Fonts service.

The font authoring glyphsets and the API serving subsets are separate datasets.
Google documents that distinction in the
[glyphsets README](https://github.com/googlefonts/glyphsets#whats-the-difference).
The actual serving subset definitions are maintained in
[googlefonts/nam-files](https://github.com/googlefonts/nam-files). Adding characters
to a local authoring glyphset, or changing a project QA configuration, does not
automatically change Google Fonts' served subsets.

## The 17 codepoints listed in the report

These characters are already encoded in both Dehemi styles. They support Latin
accents, spacing accent forms and a general mathematical symbol; selecting an
unrelated writing-system subset solely to make them reachable would misdescribe
the family.

| Codepoint | Unicode name |
| --- | --- |
| U+02D8 | BREVE |
| U+02D9 | DOT ABOVE |
| U+02DB | OGONEK |
| U+0302 | COMBINING CIRCUMFLEX ACCENT |
| U+0306 | COMBINING BREVE |
| U+0307 | COMBINING DOT ABOVE |
| U+030A | COMBINING RING ABOVE |
| U+030B | COMBINING DOUBLE ACUTE ACCENT |
| U+030C | COMBINING CARON |
| U+0311 | COMBINING INVERTED BREVE |
| U+0312 | COMBINING TURNED COMMA ABOVE |
| U+0324 | COMBINING DIAERESIS BELOW |
| U+0326 | COMBINING COMMA BELOW |
| U+0327 | COMBINING CEDILLA |
| U+032E | COMBINING BREVE BELOW |
| U+0331 | COMBINING MACRON BELOW |
| U+2219 | BULLET OPERATOR |

The proposed patch adds these to the editable Latin Extended serving definition.
Dehemi 2.440 also supplies U+2010 HYPHEN for application discretionary line
breaking; the current checker lists that character outside the inferred Latin
subsets too. The adjacent patch therefore covers 18 characters: the 17 baseline
characters above plus U+2010. Its addition is a typography coverage proposal,
not a request to declare unrelated scripts or hide the warning.
U+02D8, U+02D9 and U+02DB are already covered by its Spacing Modifier Letters
block, but explicit exclusions currently remove them. The patch removes those
three exclusions and adds the other 14 characters. U+02DA remains excluded here
because the Latin subset already supplies it. Curators may prefer a different
placement for U+2219, or a different general policy for the shared accent forms.
This proposal is subject to that review.

## The displayed list is not exhaustive

An independent comparison with the `google-fonts-subsets` 0.202602.1 data and
the current upstream `.nam` lists found eight additional encoded characters
outside the union of the four inferred subsets:

- U+030F COMBINING DOUBLE GRAVE ACCENT;
- U+031B COMBINING HORN;
- U+0328 COMBINING OGONEK;
- U+2028 LINE SEPARATOR and U+2029 PARAGRAPH SEPARATOR;
- U+EC7F, the existing private-use mapping for `lvakuru`;
- U+FB01 LATIN SMALL LIGATURE FI and U+FB02 LATIN SMALL LIGATURE FL.

The check's bullet-generation loop skips a codepoint if it is absent from every
compiled subset. The codepoint can still be in the unreachable set that triggers
the warning. Consequently, resolving the 17 displayed codepoints alone is not
evidence that the full check will pass. The adjacent patch is deliberately limited
to those 17, and the additional eight need a separate policy decision. Private-use
characters and formatting controls in particular should not be added globally
to a Latin subset without curator agreement.

## Subsetter closure and rendering caveats

A font subset can retain unencoded glyphs through composite or OpenType layout
closure. For example, a ligature glyph may remain because GSUB references it, even
when the ligature's own Unicode alias was not requested. Retaining a glyph is not
the same as retaining every encoded cmap entry or including its codepoint in the
CSS `unicode-range`. Conversely, a complete downloadable TTF can support a
character that a hosted subset does not advertise. The check compares encoded
character lists; it does not demonstrate the final subset's rendered behavior.

Review must therefore include actual subset generation and inspection of cmap,
GSUB, GPOS, glyph closure and CSS ranges. Test decomposed Latin accents, standalone
marks, fi/fl input aliases, relevant formatting controls and Sinhala text against
both the full font and the served subset combinations. Preserve shaping and mark
placement; do not delete required accents merely to reduce the check's warning
count. A local subset experiment is useful evidence, but is not proof that Google
has deployed those definitions.

## Requested maintainer actions

1. Confirm the intended `METADATA.pb` subsets for Dehemi during onboarding.
2. Review the 17-character patch and decide how to handle the eight additional
   codepoints, including private-use and control characters.
3. If accepted, regenerate the machine-readable `.nam` files using the upstream
   preprocessing workflow and publish/update the corresponding subset data.
4. Re-run the unmodified Fontspector profile with the updated data and metadata,
   then test actual generated subsets and the Google Fonts API serving output.

Until those steps occur, keep the raw subsetting warning and this proposal in the
audit record. No Fontspector result has been relabeled as a pass.
