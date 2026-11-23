# news-image-20261123-intl — The Global Herald: Monday 23 November 2026

One international front page that sums up Monday 23 November 2026: a big
masthead, a world-map strip with numbered pins, the burning tanker in the
Strait of Hormuz as the main story, the Peru quake and the COP31 collapse
as hero panels, a dense LEFT side packed with small stories from every
continent (three columns, 18 stories), and a right side with a stat strip,
an ALSO TODAY list and a date-check box. 30 stories, all verified, are
documented in STORIES.md.

## Files

- `draw.py` — renders `entry.png` (1024×1024 JPEG) with Pillow from
  fixed coordinates. Deterministic: no network, no clock, no randomness.
  The tanker photo and the map strip are cropped from the generated
  concept illustration in `assets/` (generated art, not a news photo).
  Run: `python3 draw.py`
- `main.py` — the entrypoint (Python 3.13, standard library only).
  Checks the picture is a genuine 1024×1024 JPEG under the 1 MiB cap,
  then copies it to the output directory: argv[1], then
  `MAKEFUN_OUTPUT_DIR`, then `./out`. Run:
  `MAKEFUN_OUTPUT_DIR=out python3 main.py`
- `entry.png` — the finished picture.
- `STORIES.md` — the 30 verified stories behind the picture.

## Status

- Built fresh 23 Nov 2026 in a session started after the competition
  opened (opens 23 Nov 2026 00:00 UTC / 07:00 WIB).
- Concept: Bos chose concept 20 (international newspaper) with the left
  side packed much denser with news and the right side kept as in the
  concept. Earlier pop-up-book concept (21) was chosen then dropped by
  Bos — not used here.
- NOT submitted yet. Bos must see the rendered image first, then Gas.
