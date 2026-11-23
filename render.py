#!/usr/bin/env python3
"""
THE SUNDAY LEDGER — entry image for make.fun news-image-20261122.
Draws a 1024x1024 broadsheet of Sunday 22 November 2026 with PIL.
Every fact and number comes from ../ANALYSIS.md (verified canon).
Fonts: Playfair Display (masthead/headlines) + Liberation Sans (body).
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W = H = 1024
M = 24                      # page margin
CW = W - 2 * M              # content width = 976

# ---- palette -------------------------------------------------------------
PAPER = (250, 246, 234)     # cream paper
BAND = (12, 52, 40)         # deep emerald (masthead band)
INK = (24, 27, 44)          # navy-black ink
INK2 = (72, 74, 88)         # muted ink
RED = (190, 30, 38)         # accent red
HAIR = (150, 152, 138)      # hairline
CREAM_DIM = (214, 206, 182)  # dim cream on the band
TINT = (243, 224, 178)      # pale art tint (warm sand)
TINT2 = (196, 226, 205)     # pale art tint (mint)
TINT3 = (246, 203, 182)     # pale art tint (peach)
TINT4 = (203, 226, 244)     # pale art tint (sky)
GOLD = (206, 158, 60)
SKY = (172, 210, 238)       # scene sky
SEA = (110, 168, 212)       # scene sea
GREEN = (96, 168, 96)       # scene grass
BRICK = (198, 96, 62)       # scene brick
SLATE = (94, 114, 154)      # scene slate blue
SAND2 = (224, 182, 116)     # scene sand block

FONT_DIR = os.path.expanduser("~/.fonts")
LIB = "/usr/share/fonts/truetype/liberation"

_cache = {}


def F(kind, size):
    key = (kind, size)
    if key in _cache:
        return _cache[key]
    paths = {
        "pf9": os.path.join(FONT_DIR, "PlayfairDisplay-900.ttf"),
        "pf8": os.path.join(FONT_DIR, "PlayfairDisplay-800.ttf"),
        "pf7": os.path.join(FONT_DIR, "PlayfairDisplay-700.ttf"),
        "sans": os.path.join(LIB, "LiberationSans-Regular.ttf"),
        "bold": os.path.join(LIB, "LiberationSans-Bold.ttf"),
        "ital": os.path.join(LIB, "LiberationSans-Italic.ttf"),
    }
    f = ImageFont.truetype(paths[kind], size)
    _cache[key] = f
    return f


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def tw(text, font):
    return d.textlength(text, font=font)


def wrap(text, font, maxw):
    """Greedy word wrap; returns list of lines that fit maxw."""
    words = text.split()
    lines, cur = [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if tw(t, font) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def block(x, y, text, font, fill, maxw, leading=1.25, max_lines=None):
    """Draw wrapped text; returns y just below the block."""
    lines = wrap(text, font, maxw)
    if max_lines:
        lines = lines[:max_lines]
    lh = int(font.size * leading)
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


def center(y, text, font, fill):
    d.text(((W - tw(text, font)) / 2, y), text, font=font, fill=fill)


def hrule(y, x0=M, x1=W - M, fill=HAIR, width=1):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)


def chip(x, y, text, fill):
    """Small certainty tag; returns width used."""
    f = F("bold", 8)
    w_ = int(tw(text, f)) + 10
    d.rectangle([x, y, x + w_, y + 13], fill=fill)
    d.text((x + 5, y + 2), text, font=f, fill=(250, 248, 240))
    return w_


def numb(x, y, n, r=9):
    """Red story-number disc with white numeral."""
    d.ellipse([x, y, x + 2 * r, y + 2 * r], fill=RED)
    f = F("bold", 11 if n < 10 else 10)
    s = str(n)
    d.text((x + r - tw(s, f) / 2, y + r - 6), s, font=f, fill=(252, 250, 244))


# ---- canon content (from ANALYSIS.md; nothing invented) -------------------
STRAPLINE = ("COP31 ENDS WITH NO DEAL  ·  LIVERPOOL 4\u20130 IN POCHETTINO'S DEBUT"
             "  ·  ALCARAZ TAKES THE ATP FINALS")

FIGURES = [
    ("NO DEAL", "COP31 adopts nothing\nat Antalya"),
    ("186 / 161", "drones fired at Ukraine /\nbrought down"),
    ("98.79%", "Hong Kong's final turnout,\na record"),
    ("720/9", "India's total \u2014 the highest\never in New Zealand"),
    ("4\u20130", "Liverpool over Manchester\nUnited, at Anfield"),
    ("6-2 7-6(7)", "Alcaraz over Zverev in\nthe Turin final"),
]

REGIONS = [("EUROPE", 12), ("ASIA", 8), ("MIDDLE EAST", 4), ("N. AMERICA", 5),
           ("AFRICA", 2), ("S. AMERICA", 2), ("OCEANIA & SPACE", 2)]

TIMELINE = [
    ("OVERNIGHT", "186 drones; Dymer hit"),
    ("06:30 WIB", "Cikande fire out"),
    ("14:30 UTC", "24 body bags counted"),
    ("16:30 UTC", "Liverpool 4\u20130 United"),
    ("17:00 UTC", "Alcaraz champion"),
    ("EVENING", "Antalya: no deal"),
]

LEADS = [
    dict(n=1, loc="ANTALYA, T\u00dcRKIYE", tag="REPORTED", tint=TINT,
         head="COP31 ends with no deal",
         deck="Kurum concedes: \u201cThere is no agreement on this text.\u201d "
              "The draft, silent on fossil fuels, is rejected \u2014 a first "
              "since The Hague in 2000; the rest rolls to COP32."),
    dict(n=2, loc="KYIV REGION, UKRAINE", tag="REPORTED", tint=TINT2,
         head="A boy of seven, out of the rubble alive",
         deck="186 drones overnight, 72 of them jet-powered; 161 downed, "
              "18 places hit. In Dymer the boy is freed after some 14 hours; "
              "14 people remain unaccounted for."),
    dict(n=3, loc="MANAMA, BAHRAIN", tag="CLAIM", tint=TINT3,
         head="Claim against denial over Bahrain",
         deck="Iran says its strike hit two Patriot radars, at Riffa and "
              "Awali. Bahrain denies it \u2014 a civilian site, a fire, no "
              "injuries. Two tankers were also hit near Khasab."),
]

# (num, location, tag, headline, deck, art-key)
CARDS = [
    (4, "HONG KONG", "REPORTED", "Hong Kong elects its Election Committee",
     "Record turnout of 98.79%: 5,640 voters fill 723 of 856 seats; "
     "two by lot.", "ballot"),
    (5, "NEW ZEALAND", "REPORTED", "India declare on 720/9",
     "Rahul 136, Pant 128; 50+ for every one of the first seven "
     "stands. NZ 119/2.", "cricket"),
    (6, "LAS VEGAS", "REPORTED", "Verstappen takes Las Vegas",
     "By 0.639s; 35 lead changes. Piastri 17th to 3rd; Antonelli 6th "
     "on a penalty.", "race"),
    (7, "ANFIELD, LIVERPOOL", "REPORTED", "Liverpool rout United 4\u20130",
     "Yoro off 8'; Szoboszlai, Wirtz, Ngumoha, Mu\u00f1oz score. "
     "United stay 19th.", "football"),
    (8, "TURIN", "REPORTED", "Alcaraz takes the ATP Finals",
     "6-2 7-6(7) over Zverev: maiden title, a 5\u20130 week, record "
     "$5.17m prize.", "tennis"),
    (9, "CIKANDE, BANTEN", "REPORTED", "Cikande: the search goes on",
     "Out at 06:30 WIB; 24 body bags by nightfall, 32 missing, "
     "toll unconfirmed.", "factory"),
    (10, "NEW ORLEANS", "REPORTED", "Wembanyama's 50 sinks New Orleans",
     "50 points, 19 rebounds and 5 blocks in a 114\u201391 Spurs win.",
     "basket"),
    (11, "IRAN", "REPORTED", "Iran begins rationing power",
     "Rolling two-hour cuts begin as rationing starts.", "power"),
    (12, "BRAS\u00cdLIA", "REPORTED", "Bolsonaro in intensive care",
     "The former president is treated for a bowel obstruction and "
     "is stable.", "medical"),
    (13, "THE BALTIC", "REPORTED", "Tanker Sparta II still burning",
     "All 16 crew are safely off; Finland suspects a Ukrainian strike.",
     "ship"),
]

ALSO = [
    (14, "Manipur", "toll settles at 18; 1,130 screened"),
    (15, "Peru count", "1 dead, 853 displaced after Friday's M6.7"),
    (16, "FBI", "probes a hack of its crime database"),
    (17, "Gaza", "four die in strikes on a food-aid vehicle"),
    (18, "Vatican", "1,300 poor guests lunch with Leo XIV"),
    (19, "Delhi", "Nepal's PM Shah lands, on his first visit"),
    (20, "Estonia", "shuts five Russia crossings on 1 Dec"),
    (21, "Denmark", "expels a Russian attach\u00e9"),
    (22, "Somalia", "expels the UAE envoy"),
    (23, "El-Fasher", "MSF counts the missing"),
    (24, "Zelenskyy", "bridge strikes \u201ca fair response\u201d"),
    (25, "Beijing", "hits back at the US carrier ban"),
    (26, "Ladakh", "70% vote in first polls since 2019"),
    (27, "Seoul", "minister quits in AI-cheating scandal"),
    (28, "Fukushima", "snow strands 1,500 in one village"),
    (29, "BepiColombo", "reaches Mercury orbit"),
    (30, "Rugby", "England 37\u201312 New Zealand"),
    (31, "Arsenal", "held 2\u20132 by Newcastle"),
    (32, "Columbus Crew", "beat Messi's Miami 3\u20130"),
    (33, "Russia", "says 170 Ukrainian drones downed \u2014 CLAIM"),
    (34, "Saudi", "downs a Houthi missile \u2014 CLAIM"),
    (35, "Markets", "gold near $5,555; Bitcoin over $60,000"),
]

DATECHECK = ("NOT SUNDAY \u2014 SO NOT ON THIS PAGE:  the ICJ's Myanmar ruling "
             "was Thu 19 Nov \u00b7 the EU\u2013Indonesia CEPA was signed Sat 21 "
             "in Brussels \u00b7 \u2018El Chapo Isidro\u2019 was captured Fri 20 "
             "\u00b7 the Bayelsa funeral boat capsized Fri 20 (24 dead by Sat) "
             "\u00b7 Basra's power fire was Sat \u00b7 Geneva's killer-robot "
             "talks ended Sat \u00b7 the 400-drone barrage was Thu\u2013Fri night "
             "(Sunday's count: 186) \u00b7 Peru's M6.7 struck Fri 20 \u2014 its "
             "Sunday count is inside.")

SOURCES = ("Sources: Reuters \u00b7 Sky \u00b7 ATP \u00b7 ESPNcricinfo \u00b7 "
           "China Daily \u00b7 Xinhua \u00b7 BBC \u00b7 SES Ukraine \u00b7 "
           "Basarnas \u00b7 UKMTO \u00b7 F1/FIA \u00b7 MSF \u00b7 The Times")
KEYLINE = ("Certainty: REPORTED = carried by the day's wires \u00b7 CLAIM = "
           "one side's account, labelled as such \u00b7 Results marked FT are "
           "final.")


# ---- scene art (flat, bold shapes on pale tints) ---------------------------
def panel(x, y, w, h, tint):
    d.rectangle([x, y, x + w, y + h], fill=tint)


def render_art(fn, w, h, tint):
    """Draw art on its own layer, clipped to the panel by construction —
    nothing an art function draws can ever bleed outside its panel."""
    global d
    layer = Image.new("RGB", (w, h), tint)
    saved = d
    d = ImageDraw.Draw(layer)
    fn(0, 0, w, h)
    d = saved
    return layer


def art_cop(x, y, w, h):
    # the Antalya hall: a big screen carrying the rejected text, flags
    # along the wall, and the delegates' table below
    d.rectangle([x, y, x + w, y + 52], fill=(238, 214, 168))
    # the screen: the draft itself, crossed out
    sx0, sy0, sx1, sy1 = x + 108, y + 8, x + 200, y + 62
    d.rectangle([sx0, sy0, sx1, sy1], fill=(24, 34, 54))
    d.rectangle([sx0 + 10, sy0 + 8, sx0 + 38, sy0 + 48],
                fill=(252, 250, 244))
    for r_ in range(3):
        d.line([(sx0 + 14, sy0 + 15 + r_ * 9), (sx0 + 34, sy0 + 15 + r_ * 9)],
               fill=INK2, width=1)
    d.line([(sx0 + 6, sy0 + 4), (sx1 - 6, sy1 - 4)], fill=RED, width=4)
    d.line([(sx1 - 6, sy0 + 4), (sx0 + 6, sy1 - 4)], fill=RED, width=4)
    # flags along the wall, on both sides of the screen
    cols = [RED, GOLD, (52, 96, 66), INK, (84, 104, 128)]
    for i, c in enumerate(cols):
        fx = x + 14 + i * 17
        d.line([(fx, y + 8), (fx, y + 52)], fill=INK, width=2)
        d.rectangle([fx, y + 8, fx + 11, y + 19], fill=c)
        fx2 = x + w - 25 - (4 - i) * 17
        d.line([(fx2, y + 8), (fx2, y + 52)], fill=INK, width=2)
        d.rectangle([fx2, y + 8, fx2 + 11, y + 19], fill=c)
    # delegates' table: seven heads, papers, three hands raised
    tx0, tx1, ty = x + 14, x + w - 52, y + h - 6
    d.rectangle([tx0, ty - 7, tx1, ty], fill=INK)
    for i in range(7):
        hx = tx0 + 10 + i * 30
        d.ellipse([hx, ty - 21, hx + 11, ty - 10], fill=INK)
        d.rectangle([hx - 2, ty - 10, hx + 13, ty - 7], fill=INK2)
        d.rectangle([hx + 1, ty - 6, hx + 9, ty - 3],
                    fill=(252, 250, 244))
    for i in (0, 3, 5):
        hx = tx0 + 10 + i * 30
        d.line([(hx + 14, ty - 11), (hx + 20, ty - 23)], fill=INK, width=2)
        d.ellipse([hx + 18, ty - 26, hx + 23, ty - 21], fill=INK)
    # the chair's gavel at the head of the table
    gx, gy = tx1 + 6, ty - 24
    d.line([(gx, gy + 12), (gx + 9, gy)], fill=INK, width=3)
    d.rectangle([gx + 6, gy - 5, gx + 15, gy + 2], fill=INK)
    d.rectangle([gx + 2, gy + 13, gx + 16, gy + 16], fill=INK2)


def art_drone(x, y, w, h):
    # Kyiv region at night: searchlights and pale drones over a burning,
    # broken block in Dymer; a rescue crane at work
    d.rectangle([x, y, x + w, y + h], fill=(22, 30, 52))
    for i in range(26):
        sx_ = x + (i * 53) % (w - 8) + 4
        sy_ = y + (i * 37) % 54 + 2
        d.ellipse([sx_, sy_, sx_ + 2, sy_ + 2], fill=(232, 234, 240))
    d.ellipse([x + w - 44, y + 6, x + w - 26, y + 24], fill=(238, 226, 170))
    # searchlight beams sweeping up from the rescue line
    d.polygon([(x + 188, y + h), (x + 128, y + 8), (x + 140, y + 6)],
              fill=(216, 202, 142))
    d.polygon([(x + 292, y + h), (x + 196, y + 10), (x + 208, y + 8)],
              fill=(216, 202, 142))
    pale = (198, 204, 214)
    for (cx, cy, s) in [(52, 20, 1.0), (128, 14, 1.0), (205, 24, 1.0),
                        (88, 44, 0.6), (172, 48, 0.6)]:
        cx, cy = x + cx, y + cy
        d.line([(cx - 13 * s, cy - 8 * s), (cx + 13 * s, cy + 8 * s)],
               fill=pale, width=2)
        d.line([(cx - 13 * s, cy + 8 * s), (cx + 13 * s, cy - 8 * s)],
               fill=pale, width=2)
        d.rectangle([cx - 6 * s, cy - 4 * s, cx + 6 * s, cy + 4 * s],
                    fill=pale)
    # the broken block: lit windows, a collapsed corner, fire at its foot
    bx, by = x + 14, y + h
    dark = (8, 12, 22)
    d.polygon([(bx, by), (bx, by - 64), (bx + 26, by - 64),
               (bx + 34, by - 48), (bx + 56, by - 56), (bx + 56, by)],
              fill=dark)
    for (wx_, wy_) in [(8, -54), (34, -46), (8, -38), (40, -28), (8, -22)]:
        d.rectangle([bx + wx_, by + wy_, bx + wx_ + 9, by + wy_ + 7],
                    fill=(255, 170, 60))
    d.polygon([(bx + 56, by - 42), (bx + 86, by - 24), (bx + 88, by - 17),
               (bx + 56, by - 32)], fill=(40, 48, 66))
    d.polygon([(bx + 62, by), (bx + 88, by - 14), (bx + 114, by)],
              fill=(40, 48, 66))
    d.polygon([(bx + 96, by), (bx + 116, by - 9), (bx + 136, by)],
              fill=(40, 48, 66))
    # fire at the foot of the block
    d.polygon([(bx + 18, by), (bx + 24, by - 12), (bx + 29, by)],
              fill=(232, 110, 40))
    d.polygon([(bx + 22, by), (bx + 25, by - 8), (bx + 28, by)],
              fill=(250, 180, 60))
    d.polygon([(bx + 40, by), (bx + 45, by - 9), (bx + 50, by)],
              fill=(232, 110, 40))
    # rescue crane, pale against the night
    mx = x + w - 88
    d.line([(mx, by), (mx, y + 18)], fill=pale, width=3)
    d.line([(mx, y + 18), (mx + 58, y + 26)], fill=pale, width=3)
    d.line([(mx, y + 18), (mx - 12, by)], fill=(120, 130, 148), width=1)
    d.line([(mx + 44, y + 24), (mx + 44, by - 16)], fill=pale, width=1)
    d.line([(mx + 39, by - 16), (mx + 49, by - 16)], fill=pale, width=2)
    d.rectangle([mx - 8, by - 3, mx + 8, by], fill=pale)


def art_radar(x, y, w, h):
    # Bahrain at dusk: two Patriot radar dishes on the coast, incoming
    # tracks overhead, tankers on the water, the shield of the denial
    import math
    bands = [(110, 128, 178), (168, 138, 158), (226, 156, 120),
             (246, 190, 140)]
    bh = (h - 16) // 4
    for i, bc in enumerate(bands):
        d.rectangle([x, y + i * bh, x + w, y + (i + 1) * bh], fill=bc)
    gy = y + h - 16                     # coast line; sea below it
    d.rectangle([x, gy, x + w, y + h], fill=SEA)
    d.polygon([(x, gy), (x + 150, gy), (x + 138, gy - 5), (x, gy - 5)],
              fill=(30, 34, 40))

    def dish(cx, big):
        my = gy - 4                       # mast foot, on the coast
        d.polygon([(cx - 9, my), (cx - 2, my - 24), (cx + 2, my - 24),
                   (cx + 9, my)], fill=INK)
        d.rectangle([cx - 13, my - 27, cx + 13, my - 23], fill=INK)
        r = 14 if big else 11
        ccx, ccy = cx + 5, my - 27 - r + 4
        d.pieslice([ccx - r, ccy - r, ccx + r, ccy + r], start=140, end=320,
                   fill=INK)
        d.ellipse([ccx - 3, ccy - 3, ccx + 3, ccy + 3], fill=GOLD)
        d.line([(ccx, ccy), (ccx + 10, ccy - 9)], fill=INK, width=2)
        for rr in (6, 10, 14):
            d.arc([ccx + 8, ccy - rr, ccx + 8 + rr + 8, ccy + rr],
                  start=250, end=40, fill=(250, 246, 234), width=2)
        return ccx, ccy

    dish(x + 46, True)
    dish(x + 112, False)
    # incoming tracks: flat arcs that stay inside the panel
    for (sx, sy, ex) in [(x + w - 16, y + 4, x + 196),
                         (x + w - 60, y + 2, x + 224)]:
        pts = []
        for t in range(21):
            tt = t / 20
            px = sx + (ex - sx) * tt
            py = sy + (y + 52 - sy) * tt - 12 * math.sin(tt * math.pi)
            pts.append((px, py))
        d.line(pts, fill=RED, width=2)
        d.polygon([(pts[-1][0], pts[-1][1]), (pts[-1][0] - 9, pts[-1][1] - 1),
                   (pts[-1][0] - 2, pts[-1][1] - 8)], fill=RED)
    # the shield of the denial, smaller, at the right
    sx, sy = x + w - 44, y + 36
    d.polygon([(sx, sy), (sx + 26, sy), (sx + 26, sy + 15), (sx + 13, sy + 27),
               (sx, sy + 15)], outline=INK, width=3)
    d.line([(sx + 7, sy + 11), (sx + 11, sy + 16), (sx + 20, sy + 6)],
           fill=(52, 96, 66), width=3)
    # the water, and two tankers on it
    for (hx, s) in [(x + 168, 1.0), (x + 238, 0.8)]:
        hw = 44 * s
        d.polygon([(hx, gy + 3), (hx + hw, gy + 3), (hx + hw - 6, gy + 10),
                   (hx + 5, gy + 10)], fill=INK)
        d.rectangle([hx + 8 * s, gy - 3, hx + 26 * s, gy + 3], fill=INK2)
        d.rectangle([hx + 30 * s, gy - 6, hx + 35 * s, gy + 3], fill=INK)
    for wx_ in range(int(x) + 10, int(x + w) - 12, 26):
        d.arc([wx_, gy + 9, wx_ + 12, gy + 15], start=0, end=180,
              fill=(252, 250, 244), width=1)


LEAD_ART = [art_cop, art_drone, art_radar]


def scene(kind, x, y, w, h):
    """Panoramic mini-scenes for the card art strips (strip x, y, w, h)."""
    gy = y + h - 4

    def figure(fx, fy):
        d.ellipse([fx - 3, fy - 13, fx + 3, fy - 7], fill=INK)
        d.rectangle([fx - 3, fy - 7, fx + 3, fy], fill=INK)

    if kind == "ballot":
        for (bx, bh), bc in zip([(10, 13), (28, 17), (48, 11)],
                                [SLATE, BRICK, SAND2]):
            d.rectangle([x + bx, gy - bh, x + bx + 12, gy], fill=bc)
            d.rectangle([x + bx + 3, gy - bh + 4, x + bx + 6, gy - bh + 7],
                        fill=GOLD)
        d.rectangle([x + 148, gy - 10, x + 176, gy], fill=INK)
        d.rectangle([x + 144, gy - 12, x + 180, gy - 10], fill=INK)
        d.rectangle([x + 158, gy - 17, x + 168, gy - 11],
                    fill=(252, 250, 244), outline=INK)
        for i in range(3):
            figure(x + 200 + i * 13, gy)
    elif kind == "cricket":
        d.rectangle([x + 4, gy, x + w - 4, gy + 3], fill=GREEN)
        d.ellipse([x + 198, y + 3, x + 210, y + 15], fill=GOLD)
        for sx_ in (28, 34, 40):
            d.rectangle([x + sx_, gy - 12, x + sx_ + 2, gy], fill=GOLD,
                        outline=INK)
        figure(x + 118, gy)
        d.polygon([(x + 122, gy - 9), (x + 137, gy - 1), (x + 140, gy - 4),
                   (x + 126, gy - 12)], fill=INK)
        d.arc([x + 138, gy - 20, x + 176, gy - 2], start=200, end=330,
              fill=INK2, width=1)
        d.ellipse([x + 172, gy - 13, x + 177, gy - 8], fill=RED)
        d.line([(x + 8, gy), (x + w - 8, gy)], fill=INK2, width=1)
    elif kind == "race":
        for bx, bh in [(8, 10), (24, 15), (42, 8)]:
            d.rectangle([x + bx, gy - bh, x + bx + 11, gy], fill=SLATE)
        for cxx, col in [(x + 86, INK), (x + 140, RED)]:
            d.polygon([(cxx, gy - 6), (cxx + 10, gy - 10), (cxx + 30, gy - 10),
                       (cxx + 40, gy - 6), (cxx + 40, gy - 3), (cxx, gy - 3)],
                      fill=col)
            d.rectangle([cxx + 30, gy - 13, cxx + 36, gy - 10], fill=col)
            d.ellipse([cxx + 6, gy - 4, cxx + 13, gy + 2], fill=INK)
            d.ellipse([cxx + 28, gy - 4, cxx + 35, gy + 2], fill=INK)
        for i in range(4):
            for j in range(2):
                if (i + j) % 2 == 0:
                    d.rectangle([x + 206 + i * 6, y + 2 + j * 6,
                                 x + 212 + i * 6, y + 8 + j * 6], fill=INK)
        d.line([(x + 206, y + 2), (x + 206, gy)], fill=INK, width=2)
    elif kind == "football":
        d.rectangle([x + 4, gy, x + w - 4, gy + 3], fill=GREEN)
        d.arc([x + 30, y - 6, x + 150, y + 34], start=180, end=360,
              fill=INK, width=2)
        for fx in (44, 128):
            d.line([(x + fx, y + 8), (x + fx, gy)], fill=INK, width=2)
            d.ellipse([x + fx - 4, y + 2, x + fx + 4, y + 9], fill=GOLD)
        d.rectangle([x + 176, gy - 14, x + 208, gy], outline=(252, 250, 244),
                    width=2)
        d.rectangle([x + 176, gy - 14, x + 208, gy], outline=INK, width=1)
        d.ellipse([x + 96, gy - 8, x + 104, gy], fill=(252, 250, 244),
                  outline=INK)
        d.line([(x + 8, gy), (x + w - 8, gy)], fill=(52, 96, 66), width=2)
    elif kind == "tennis":
        d.rectangle([x + 4, gy, x + w - 4, gy + 3], fill=GREEN)
        d.line([(x + 20, gy - 8), (x + w - 20, gy - 8)], fill=INK, width=2)
        for nx in range(28, w - 24, 12):
            d.line([(x + nx, gy - 8), (x + nx, gy)], fill=INK2, width=1)
        figure(x + 52, gy)
        d.ellipse([x + 56, gy - 16, x + 66, gy - 8], outline=INK, width=2)
        figure(x + w - 52, gy)
        d.ellipse([x + w - 66, gy - 16, x + w - 56, gy - 8], outline=INK,
                  width=2)
        d.arc([x + 66, gy - 24, x + w - 66, gy - 6], start=200, end=340,
              fill=INK2, width=1)
        d.ellipse([x + w // 2 - 2, gy - 21, x + w // 2 + 2, gy - 17],
                  fill=(168, 178, 74))
    elif kind == "factory":
        d.rectangle([x + 20, gy - 12, x + 84, gy], fill=BRICK)
        d.rectangle([x + 66, gy - 20, x + 74, gy - 12], fill=BRICK)
        for r_ in range(2):
            d.ellipse([x + 62 + r_ * 7, gy - 27 + r_ * 2,
                       x + 70 + r_ * 7, gy - 21 + r_ * 2],
                      fill=(176, 178, 170))
        d.polygon([(x + 34, gy - 13), (x + 39, gy - 5), (x + 35, gy - 2),
                   (x + 29, gy - 7)], fill=RED)
        d.polygon([(x + 35, gy - 10), (x + 38, gy - 5), (x + 35, gy - 3),
                   (x + 32, gy - 7)], fill=GOLD)
        for bx_ in (120, 148, 176):
            d.line([(x + bx_, gy), (x + bx_ - 8, y + 3)], fill=GOLD, width=2)
        figure(x + 206, gy)
        figure(x + 220, gy)
    elif kind == "basket":
        d.rectangle([x + 150, y + 2, x + 182, y + 14], fill=(252, 250, 244),
                    outline=INK, width=2)
        d.ellipse([x + 158, y + 13, x + 174, y + 19], outline=RED, width=2)
        d.line([(x + 166, y + 14), (x + 166, gy)], fill=INK, width=2)
        figure(x + 84, gy)
        d.line([(x + 86, gy - 10), (x + 104, gy - 17)], fill=INK, width=3)
        d.ellipse([x + 102, gy - 22, x + 110, gy - 14], fill=(206, 118, 44),
                  outline=INK)
        d.line([(x + 8, gy), (x + w - 8, gy)], fill=INK2, width=1)
    elif kind == "power":
        for px_ in (36, 108):
            d.polygon([(x + px_ - 10, gy), (x + px_, gy - 20),
                       (x + px_ + 10, gy)], outline=INK, width=2)
            d.line([(x + px_ - 13, gy - 15), (x + px_ + 13, gy - 15)],
                   fill=INK, width=2)
        d.arc([x + 46, gy - 24, x + 98, gy - 8], start=20, end=160,
              fill=INK, width=1)
        for hx, lit, hc in [(168, True, BRICK), (192, False, SLATE),
                            (216, True, SAND2)]:
            d.rectangle([x + hx, gy - 9, x + hx + 14, gy], fill=hc)
            d.rectangle([x + hx + 4, gy - 7, x + hx + 8, gy - 3],
                        fill=GOLD if lit else INK2)
    elif kind == "medical":
        d.rectangle([x + 26, gy - 18, x + 62, gy], fill=(252, 250, 244),
                    outline=INK, width=2)
        d.rectangle([x + 40, gy - 15, x + 48, gy - 7], fill=RED)
        d.rectangle([x + 36, gy - 11, x + 52, gy - 11 + 0], fill=RED)
        d.rectangle([x + 37, gy - 12, x + 51, gy - 10], fill=RED)
        d.rectangle([x + 120, gy - 9, x + 168, gy], fill=(252, 250, 244),
                    outline=INK, width=2)
        d.polygon([(x + 168, gy - 7), (x + 180, gy - 7), (x + 184, gy),
                   (x + 168, gy)], fill=INK2)
        d.rectangle([x + 140, gy - 7, x + 146, gy - 1], fill=RED)
        d.rectangle([x + 138, gy - 5, x + 148, gy - 3], fill=RED)
        d.ellipse([x + 128, gy - 2, x + 134, gy + 3], fill=INK)
        d.ellipse([x + 168, gy - 2, x + 174, gy + 3], fill=INK)
        figure(x + 206, gy)
        figure(x + 220, gy)
    elif kind == "ship":
        d.rectangle([x, gy + 1, x + w, y + h], fill=SEA)
        d.polygon([(x + 60, gy - 4), (x + 190, gy - 4), (x + 178, gy + 3),
                   (x + 70, gy + 3)], fill=INK)
        d.rectangle([x + 84, gy - 10, x + 150, gy - 4], fill=INK2)
        d.rectangle([x + 152, gy - 14, x + 164, gy - 4], fill=INK)
        d.polygon([(x + 156, gy - 22), (x + 162, gy - 13), (x + 157, gy - 11),
                   (x + 151, gy - 15)], fill=RED)
        d.polygon([(x + 157, gy - 19), (x + 160, gy - 13), (x + 157, gy - 12),
                   (x + 154, gy - 15)], fill=GOLD)
        d.ellipse([x + 148, gy - 27, x + 158, gy - 21], fill=INK2)
        d.ellipse([x + 158, gy - 29, x + 170, gy - 22], fill=INK2)
        for wx_ in range(16, w - 20, 30):
            d.arc([x + wx_, gy + 1, x + wx_ + 14, gy + 6], start=0, end=180,
                  fill=(252, 250, 244), width=1)
    elif kind == "aid":
        d.rectangle([x + 24, gy - 13, x + 76, gy - 2], fill=(252, 250, 244),
                    outline=INK, width=2)
        d.rectangle([x + 44, gy - 10, x + 52, gy - 4], fill=RED)
        d.rectangle([x + 42, gy - 8, x + 54, gy - 6], fill=RED)
        d.polygon([(x + 76, gy - 9), (x + 90, gy - 9), (x + 96, gy - 2),
                   (x + 76, gy - 2)], fill=INK2)
        d.ellipse([x + 32, gy - 3, x + 39, gy + 3], fill=INK)
        d.ellipse([x + 78, gy - 3, x + 85, gy + 3], fill=INK)
        d.rectangle([x + 140, gy - 8, x + 158, gy], fill=SAND2)
        d.rectangle([x + 143, gy - 14, x + 155, gy - 8], fill=SAND2)
        d.rectangle([x + 147, gy - 12, x + 151, gy - 6], fill=RED)
        figure(x + 196, gy)
        d.rectangle([x + 200, gy - 10, x + 212, gy - 4], fill=INK2)
    elif kind == "pope":
        d.pieslice([x + 30, gy - 24, x + 74, gy + 2], start=180, end=360,
                   fill=GOLD, outline=INK)
        d.line([(x + 52, gy - 27), (x + 52, gy - 21)], fill=INK, width=2)
        d.line([(x + 49, gy - 25), (x + 55, gy - 25)], fill=INK, width=2)
        d.rectangle([x + 24, gy - 2, x + 80, gy], fill=INK)
        d.rectangle([x + 110, gy - 5, x + 210, gy - 2], fill=INK)
        for i in range(4):
            hx = x + 118 + i * 24
            d.ellipse([hx, gy - 14, hx + 8, gy - 6], fill=INK)
        d.rectangle([x + 150, gy - 5, x + 158, gy - 2], fill=(252, 250, 244))


# ---- dotted world map + numbered pins --------------------------------------
MAP_ROWS = [
    "     #  #                 #    #  #   #                         ",
    "   ########        ##     #################                     ",
    "  ##########      ####   #####################    #             ",
    " ############      ##   #########################              ",
    "  ##########            ##########################  ##         ",
    "   ########              #############################         ",
    "    ######      #         #########  #################  #      ",
    "     ####      ###         ########   ############### ####     ",
    "      ##        ##           ######     #############  #####    ",
    "       #                     #####       ###########    ###     ",
    "                ####          ###         #########      #      ",
    "                 ###          ##           #######              ",
    "                 ####         #             #####        #      ",
    "                  ###                        ###         ##     ",
    "                  ####                       ##      ########   ",
    "                   ##                              #########    ",
    "                   #                                #######     ",
    "                                                                ",
    "                                                      #  ###    ",
    "                                                         ##     ",
]

# pin positions as fractions of the map panel (story number -> (fx, fy))
PINS = {
    6: (0.115, 0.30), 10: (0.160, 0.40), 12: (0.250, 0.68),
    7: (0.452, 0.17), 13: (0.508, 0.14), 8: (0.470, 0.235),
    2: (0.538, 0.20), 1: (0.540, 0.295),
    3: (0.582, 0.355), 11: (0.590, 0.295),
    9: (0.752, 0.60), 4: (0.778, 0.375), 5: (0.955, 0.86),
}


def draw_map(x, y, w, h):
    rows = len(MAP_ROWS)
    cols = max(len(r) for r in MAP_ROWS)
    cw_ = w / cols
    ch_ = h / rows
    for ri, row in enumerate(MAP_ROWS):
        for ci, ch in enumerate(row):
            if ch == "#":
                cx = x + ci * cw_ + cw_ / 2
                cy = y + ri * ch_ + ch_ / 2
                d.ellipse([cx - 1.6, cy - 1.6, cx + 1.6, cy + 1.6],
                          fill=(126, 166, 110))
    for n, (fx, fy) in PINS.items():
        px, py = x + fx * w, y + fy * h
        r = 8.5
        d.ellipse([px - r, py - r, px + r, py + r], fill=RED,
                  outline=(252, 250, 244), width=1)
        f = F("bold", 10 if n < 10 else 9)
        s = str(n)
        d.text((px - tw(s, f) / 2, py - 5.5), s, font=f,
               fill=(252, 250, 244))


# ============================ LAYOUT =======================================
warn = []

# ---- masthead band ---------------------------------------------------------
_kick = "SUNDAY'S WORLD NEWS \u00b7 ONE PICTURE"
_kf = F("bold", 11.5)
d.text((M, 10), _kick, font=_kf, fill=RED)
_right = "THE SUNDAY LEDGER \u00b7 35 STORIES \u00b7 7 REGIONS"
d.text((W - M - tw(_right, _kf), 10), _right, font=_kf, fill=INK)
_date = "Sunday 22 November 2026"
_df = F("pf9", 72)
_db = d.textbbox((0, 0), _date, font=_df)
_dtop = min(30, 114 - (_db[3] - _db[1]))
d.text(((W - tw(_date, _df)) / 2 - _db[0], _dtop - _db[1]), _date, font=_df,
       fill=INK)
d.line([(0, 122), (W, 122)], fill=RED, width=3)

# ---- strapline --------------------------------------------------------------
center(131, STRAPLINE, F("bold", 14.5), RED)
hrule(152)

# ---- figures band -----------------------------------------------------------
uy = 158
d.rectangle([M, uy, M + 86, uy + 40], fill=RED)
d.text((M + 8, uy + 6), "THE DAY", font=F("bold", 10.5),
       fill=(252, 250, 244))
d.text((M + 8, uy + 21), "IN UTC", font=F("bold", 10.5),
       fill=(252, 250, 244))
uw = (W - M - (M + 98)) / 6
for i, (tm, txt) in enumerate(TIMELINE):
    cx = M + 98 + i * uw
    d.text((cx, uy + 2), tm, font=F("bold", 12.5), fill=RED)
    d.text((cx, uy + 21), txt, font=F("sans", 10.5), fill=INK)
hrule(206)

# ---- the day in numbers -------------------------------------------------------
ny = 212
d.rectangle([M, ny, M + 86, ny + 52], fill=RED)
d.text((M + 8, ny + 12), "THE DAY", font=F("bold", 10.5),
       fill=(252, 250, 244))
d.text((M + 8, ny + 27), "IN NUMBERS", font=F("bold", 10.5),
       fill=(252, 250, 244))
cellw = (W - M - (M + 98)) / 6
for i, (num, lab) in enumerate(FIGURES):
    cx = M + 98 + i * cellw
    nf = F("pf8", 25 if len(num) <= 7 else 22)
    d.text((cx + 2, ny), num, font=nf, fill=INK)
    lf = F("sans", 9.5)
    if i == 1:
        ln = "fired at Ukraine \u00b7 downed"
        d.text((cx + 2, ny + 30), ln, font=lf, fill=INK2)
        bw = cellw - 12
        d.rectangle([cx + 2, ny + 42, cx + 2 + bw, ny + 45], fill=INK2)
        d.rectangle([cx + 2, ny + 48, cx + 2 + bw * 161 / 186, ny + 51],
                    fill=(52, 120, 80))
    elif i == 2:
        ln = "Hong Kong's final turnout"
        d.text((cx + 2, ny + 30), ln, font=lf, fill=INK2)
        bw = cellw - 12
        d.rectangle([cx + 2, ny + 42, cx + 2 + bw, ny + 45], fill=HAIR)
        d.rectangle([cx + 2, ny + 42, cx + 2 + bw * 0.9879, ny + 45],
                    fill=RED)
    else:
        for j, ln in enumerate(lab.split("\n")):
            d.text((cx + 2, ny + 30 + j * 11), ln, font=lf, fill=INK2)
    if i:
        d.line([(cx, ny + 2), (cx, ny + 46)], fill=HAIR, width=1)
hrule(272)

# ---- region strip -----------------------------------------------------------
seg = ""  # region counts now ride in the ALSO heading below

# ---- timeline ---------------------------------------------------------------
ly = 280
lead_w = 309
for i, L in enumerate(LEADS):
    x = M + i * (lead_w + 24.5)
    img.paste(render_art(LEAD_ART[i], lead_w, 120, L["tint"]), (int(x), ly))
    ry = ly + 126
    numb(x, ry, L["n"], r=8)
    d.text((x + 22, ry + 1), L["loc"], font=F("bold", 11.5), fill=INK)
    cw_ = int(tw(L["tag"], F("bold", 8))) + 10
    chip(x + lead_w - cw_, ry, L["tag"], RED if L["tag"] == "CLAIM" else INK)
    hy = ry + 21
    lines = wrap(L["head"], F("pf7", 22), lead_w)
    if len(lines) > 2:
        warn.append(f"lead {L['n']} headline {len(lines)} lines")
    for ln in lines[:2]:
        d.text((x, hy), ln, font=F("pf7", 22), fill=INK)
        hy += 25
    dy = hy + 4
    dlines = wrap(L["deck"], F("sans", 11), lead_w)
    if len(dlines) > 3:
        warn.append(f"lead {L['n']} deck {len(dlines)} lines")
    for ln in dlines[:3]:
        d.text((x, dy), ln, font=F("sans", 11), fill=INK)
        dy += 13.5
hrule(528)

# ---- cards ------------------------------------------------------------------
cy0 = 534
card_w, card_h = 188, 110
for idx, (n, loc, tag, head, deck, art) in enumerate(CARDS):
    x = M + (idx % 5) * (card_w + 9)
    y = cy0 + (idx // 5) * (card_h + 6)
    img.paste(render_art(lambda ax, ay, aw, ah, k=art: scene(k, ax, ay, aw, ah),
                         card_w, 32, [TINT, TINT2, TINT3, TINT4][idx % 4]),
              (int(x), y))
    ry = y + 37
    numb(x, ry, n, r=7)
    d.text((x + 18, ry + 1), loc, font=F("bold", 9), fill=INK)
    cw_ = int(tw(tag, F("bold", 8))) + 10
    chip(x + card_w - cw_, ry, tag, INK)
    hy = y + 53
    hlines = wrap(head, F("bold", 12.5), card_w)
    if len(hlines) > 2:
        warn.append(f"card {n} headline {len(hlines)} lines")
    for ln in hlines[:2]:
        d.text((x, hy), ln, font=F("bold", 12.5), fill=INK)
        hy += 14.5
    dy = y + 84
    dlines = wrap(deck, F("sans", 9.5), card_w)
    if len(dlines) > 2:
        warn.append(f"card {n} deck {len(dlines)} lines: {deck[:40]}...")
    for ln in dlines[:2]:
        d.text((x, dy), ln, font=F("sans", 9.5), fill=INK)
        dy += 12
hrule(764)

# ---- bottom band: map + ALSO -------------------------------------------------
by = 770
d.text((M, by), "THE DAY MAPPED", font=F("bold", 11.5), fill=RED)
d.text((M + tw("THE DAY MAPPED", F("bold", 11.5)) + 8, by),
       "\u2014 pins match story numbers", font=F("sans", 10), fill=INK2)
draw_map(M, by + 18, 292, 118)
ax = M + 316
d.text((ax, by), "ALSO ON SUNDAY", font=F("bold", 11.5), fill=RED)
d.text((ax + tw("ALSO ON SUNDAY", F("bold", 11.5)) + 10, by + 1),
       "EUROPE 12 \u00b7 ASIA 8 \u00b7 MIDDLE EAST 4 \u00b7 N. AMERICA 5 "
       "\u00b7 AFRICA 2 \u00b7 S. AMERICA 2 \u00b7 OCEANIA & SPACE 2",
       font=F("sans", 9), fill=INK2)
acol_w = (W - M - ax - 14) / 2
for i, (n, lead, rest) in enumerate(ALSO):
    cx = ax + (i // 11) * (acol_w + 14)
    cy = by + 18 + int((i % 11) * 13.5)
    nf = F("bold", 10)
    d.text((cx, cy), str(n), font=nf, fill=RED)
    x2 = cx + tw(str(n), nf) + 4
    d.text((x2, cy), lead, font=F("bold", 10), fill=INK)
    x3 = x2 + tw(lead, F("bold", 10)) + 3
    d.text((x3, cy), rest, font=F("sans", 10), fill=INK)
    if x3 + tw(rest, F("sans", 9.5)) > cx + acol_w:
        warn.append(f"also {n} overflows column")

# ---- date check ---------------------------------------------------------------
dy0 = 944
d.rectangle([M, dy0, W - M, dy0 + 44], outline=RED, width=2)
d.text((M + 12, dy0 + 6), "DATE", font=F("pf7", 13), fill=RED)
d.text((M + 12, dy0 + 21), "CHECK", font=F("pf7", 13), fill=RED)
block(M + 84, dy0 + 5, DATECHECK, F("sans", 10), INK, W - M - (M + 84) - 10,
      leading=1.3)

# ---- footer -------------------------------------------------------------------
center(994, SOURCES, F("sans", 9.5), INK2)
center(1007, KEYLINE, F("sans", 9.5), INK2)

img.save(OUT, format="JPEG", quality=88)
print("saved", OUT, os.path.getsize(OUT), "bytes")
for w_ in warn:
    print("WARN:", w_)
print("done")
