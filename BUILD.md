# Build notes

`entry.png` (1024×1024) is the competition image. Two generations live here:

- **V7** — drawn by `render.py` (Python/PIL) straight to `entry.png`.
- **V8 (current)** — laid out in `page.html` (HTML/CSS + inline SVG, no external
  assets, no network) and rasterised once, locally, at exactly 1024×1024:

  ```
  chrome --headless=new --force-device-scale-factor=1 \
         --window-size=1024,1024 --screenshot=entry.png page.html
  ```

`main.ts` is the submitted program for both: it copies the committed
`entry.png` into `$MAKEFUN_OUTPUT_DIR`, byte for byte, so the two harness
runs always agree.
