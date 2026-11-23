import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// Hand-in for news-image-20261122: copy the entry image to the output dir.
// The image itself is laid out in page.html (HTML/SVG, see BUILD.md) and
// committed as entry.png.
const here = dirname(fileURLToPath(import.meta.url));
const botDir = process.env.MAKEFUN_BOT_DIR || here;
const outDir = process.env.MAKEFUN_OUTPUT_DIR || join(here, "output");

mkdirSync(outDir, { recursive: true });
copyFileSync(join(botDir, "entry.png"), join(outDir, "entry.png"));
console.log("entry.png copied to", outDir);
