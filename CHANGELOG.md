# Changelog

## 2026-11-16 - Canonical SDK snapshot synchronization

Applies to `v2.0/pet_lib.py`, `v3.0/pet_lib.py`, `v4.0/pet_lib.py`,
and `v5.0/pet_lib.py`. These snapshots synchronize the full canonical course
source, including earlier numeric behavior changes; this is broader than an
image or CSS update.

- `show_image` provides meaningful mood image alternatives and a filename-based
  alternative for other images. Alternative text is HTML-escaped, including
  quotes.
- Stat cards and speech bubbles retain explicit foreground/background color
  pairs for readable contrast in light and dark notebook themes. Stat cards
  retain their 324px desktop outer width and fit narrower containers using
  `max-width: 100%` and `box-sizing: border-box`.
- `show_stats` names and `say` names/messages render as literal plain text in
  HTML output. Markup-like strings, Unicode, quotes, and ampersands are
  preserved as text rather than interpreted as HTML. This text handling
  leaves terminal text and public signatures unchanged.
- Long literal messages wrap within the existing flex message bubble using
  `min-width: 0` and `overflow-wrap: anywhere`.
- Numeric stat rendering accepts finite integers and floats, rejects booleans
  and nonnumeric values, and rejects NaN and infinity. Display values round to
  at most two decimal places without trailing zeros or negative zero.
  Progress percentages round to two decimal places and clamp to 0-100%; bars
  do not clamp the stored player data. Zero or negative maximum HP produces
  an empty progress bar rather than division by zero in the v3.0-v5.0 HUD and
  dashboard.
- Console output now includes fixed-width stat bars. Console/HUD numeric
  formatting and default text may differ from earlier public files. In
  v3.0-v5.0, missing HP in the terminal HUD now defaults to 100 rather than 0;
  missing HP in the terminal dashboard now displays 100 rather than None.
  Keep player dictionaries as data instead of parsing printed messages.

The existing version directory labels and `__version__` literals remain
unchanged. A version label alone does not identify the exact source: use the
release commit hash (and file hashes when comparing snapshots). No new
semantic version or publication status is implied by this entry.
