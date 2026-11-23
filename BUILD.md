# Build notes

`entry.png` (1024×1024) is the competition image. Two generations live here:

- **V7** — drawn by `render.py` (Python/PIL) straight to `entry.png`.
- **V8** — laid out in `page.html` (HTML/CSS + inline SVG, no external
  assets, no network) and rasterised once, locally, at exactly 1024×1024:

  ```
  chrome --headless=new --force-device-scale-factor=1 \
         --window-size=1024,1024 --screenshot=entry.png page.html
  ```

- **V9 (current)** — `page.html` rewritten as a true front page on the same
  rasterisation route: the COP31 story is a full-width hero (crossed-out
  draft document, plenary dome, flag row) beside a "THE DAY IN NUMBERS"
  rail; two supporting leads; eight cards in a 4×2 grid; the map and the
  26 briefs (white number discs) below. Same 37 verified stories, same
  copy discipline — only the hierarchy changed, answering the dev judge's
  "an infographic, not a picture of the day" criticism of the flat grid.

`main.ts` is the submitted program for both: it copies the committed
`entry.png` into `$MAKEFUN_OUTPUT_DIR`, byte for byte, so the two harness
runs always agree.
