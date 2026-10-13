# Historical Maname input identity

Read-only verification on 13 October 2026 identified the historical study input
`C:/Users/MCTech/Downloads/Sinhala-Fonts-main/maname.ttf`.

| Property | Recorded value |
| --- | --- |
| Size | 474,876 bytes |
| SHA-256 | `8e616ff912bf881ffafbf032c9b80a46d0200c6037271352871d526b3be3f24f` |
| Internal family/style | Maname Regular |
| Internal version | 1.002; ttfautohint v1.8.4.7-5d5b |

The [official Google Fonts download manifest](https://fonts.google.com/download/list?family=Maname)
points to [this distributed TTF](https://fonts.gstatic.com/s/maname/v2/gNMFW3J8RpCx9my42FkGGI6q_Q.ttf).
Its bytes, size and SHA-256 exactly match the local input. The same bytes are
present in the local `Sinhala-Fonts-main.zip` member `Sinhala-Fonts-main/maname.ttf`.
The archive's download metadata records only `https://github.com/`; it does not
establish a repository, original download URL or acquisition date.

This is a verified binary identity. It does not establish the origin or timing of
the user's acquisition, and it is not an exact build reproduction from a Git
commit.

## Repository and release comparison

The binary at [google/fonts commit c482576](https://github.com/google/fonts/blob/c48257652b27eea3219f5782bccbb04f70c00c2a/ofl/maname/Maname-Regular.ttf)
and the `mooniak/maname-font` v1.002 release TTF are 501,400 bytes, SHA-256
`db07b4953f547081186104ab8e626bf405616b033598ee82eae90166e0c84e14`.
They do not byte-match the historical input. The upstream tag identifies
[commit 626ceee](https://github.com/mooniak/maname-font/tree/626ceee1311626c5240a68b0ef27722f44c374af).
Do not describe the smaller distributed input as an exact reproduction of that
source commit solely because both binaries report version 1.002.

## Remaining historical pipeline gaps

Local scripts and reports describe the earlier study, extraction, texture,
production and tightening stages, but the submitted project contains only part
of that historical pipeline. In particular, the checked tightening script writes
2.320 after an 80-unit change, while the final report describes a separate
2.320-to-2.330 seven-unit change across 513 Sinhala glyphs. The checked scripts
do not preserve the implementation of that final step. Exact historical hinting
invocations/configuration are also absent; several reports record hashes before
hinting.

The supplied Tight232 TTF reports version 2.330 and has SHA-256
`b14f0012641b9322271e0fd0bc3cd9fb9708092b716943643670bdf229ac60a5`.
The canonical release remains reproducible from its committed TTX export, as
described in [SOURCE-HISTORY.md](SOURCE-HISTORY.md). The recovered upstream input
identity does not establish complete, byte-exact Maname-to-Tight232 reproduction,
original drawing authorship, contributor agreement coverage or curator approval.
