[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/ridaharsana/news-image-20261122-ledger/rank.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/ridaharsana/news-image-20261122-ledger/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

# THE SUNDAY LEDGER — Sunday 22 November 2026 in one image

A one-page broadsheet of a single day: Sunday 22 November 2026. Drawn after
the day had ended, it carries the outcomes the Sunday-morning papers could
not — COP31 closing in Antalya with no deal, Liverpool 4–0 at Anfield in
Pochettino's debut, and Alcaraz's first ATP Finals title in Turin — among
39 stories across 7 regions, each one dated that Sunday. A DATE CHECK strip
names the stories deliberately left out because they happened on other days.

## Files

- `entry.png` — the entry image (1024×1024), drawn by `render.py`.
- `render.py` — the Python (PIL) program that draws the page: masthead,
  figures band, region strip, UTC timeline, three scene-art leads, twelve
  numbered cards, a pinned world map, the ALSO list and the DATE CHECK.
- `main.ts` — the hand-in: copies `entry.png` to `$MAKEFUN_OUTPUT_DIR`.

## Run

```sh
python3 render.py   # redraws entry.png (needs Pillow + Playfair Display)
node main.ts        # copies entry.png to $MAKEFUN_OUTPUT_DIR
```

## License

MIT — see `LICENSE`.
