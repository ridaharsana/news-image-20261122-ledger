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
PAPER = (247, 242, 228)     # cream paper
BAND = (14, 30, 24)         # deep green-black (masthead band)
INK = (18, 36, 29)          # deep green-black ink
INK2 = (74, 88, 80)         # muted ink
RED = (176, 32, 40)         # accent red
HAIR = (150, 152, 138)      # hairline
CREAM_DIM = (214, 206, 182)  # dim cream on the band
TINT = (236, 229, 208)      # pale art tint (sand)
TINT2 = (224, 230, 222)     # pale art tint (sage)
TINT3 = (241, 227, 214)     # pale art tint (rose)
GOLD = (198, 164, 92)

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

REGIONS = [("EUROPE", 12), ("ASIA", 8), ("MIDDLE EAST", 6), ("N. AMERICA", 5),
           ("AFRICA", 3), ("S. AMERICA", 2), ("OCEANIA & SPACE", 3)]

TIMELINE = [
    ("OVERNIGHT", "186 drones over Ukraine; 161 downed, Dymer hit"),
    ("06:30 WIB", "Cikande fire out after some 14 hours"),
    ("14:30 UTC", "Cikande count: 24 body bags, 32 missing"),
    ("16:30 UTC", "Liverpool 4\u20130 Man United \u2014 full time"),
    ("17:00 UTC", "Alcaraz champion in Turin, 6-2 7-6(7)"),
    ("EVENING", "Antalya plenary collapses \u2014 no deal"),
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
     "Record final turnout, 98.79%: 5,640 voters fill 723 of 856 seats; "
     "two seats decided by lot.", "ballot"),
    (5, "NEW ZEALAND", "REPORTED", "India declare on 720/9",
     "Rahul 136, Pant 128; first innings ever with 50+ stands for all "
     "seven first wickets. NZ 119/2.", "cricket"),
    (6, "LAS VEGAS", "REPORTED", "Verstappen takes Las Vegas",
     "By 0.639s, after 35 lead changes. Piastri 17th to 3rd; Antonelli's "
     "pole became a 6th-place start.", "race"),
    (7, "ANFIELD, LIVERPOOL", "REPORTED", "Liverpool rout United 4\u20130",
     "Pochettino's debut: Yoro off at 8', then Szoboszlai, Wirtz, "
     "Ngumoha and Mu\u00f1oz. United stay 19th.", "football"),
    (8, "TURIN", "REPORTED", "Alcaraz takes the ATP Finals",
     "6-2 7-6(7) over world No.1 Zverev: a maiden title, a 5\u20130 week, "
     "three set points saved, $5.17m.", "tennis"),
    (9, "CIKANDE, BANTEN", "REPORTED", "Cikande: the search goes on",
     "Out at 06:30 WIB after ~14 hours; 24 body bags by nightfall, "
     "32 missing, toll unconfirmed.", "factory"),
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
    (14, "GAZA", "REPORTED", "Four die as fire hits a food-aid vehicle",
     "Three killed in Tel al-Hawa and one in Jabalia.", "aid"),
    (15, "THE VATICAN", "REPORTED", "1,300 poor guests lunch with Leo XIV",
     "The Pope hosts lunch for the World Day of the Poor.", "pope"),
]

ALSO = [
    (16, "Manipur", "toll settles at 18; 1,130 screened"),
    (17, "Peru count", "1 dead, 853 displaced after Friday's M6.7"),
    (18, "FBI", "probes a hack of its crime database"),
    (19, "Khartoum", "homes struck by drones"),
    (20, "Hamas", "seeks urgent talks on Gaza"),
    (21, "Delhi", "Nepal's PM Shah lands, on his first visit"),
    (22, "Estonia", "shuts five Russia crossings on 1 Dec"),
    (23, "Denmark", "expels a Russian attach\u00e9"),
    (24, "Somalia", "expels the UAE envoy"),
    (25, "El-Fasher", "MSF counts the missing"),
    (26, "Zelenskyy", "bridge strikes \u201ca fair response\u201d"),
    (27, "Beijing", "hits back at the US carrier ban"),
    (28, "Ladakh", "70% vote in first polls since 2019"),
    (29, "Seoul", "minister quits in AI-cheating scandal"),
    (30, "Fukushima", "snow strands 1,500 in one village"),
    (31, "BepiColombo", "reaches Mercury orbit"),
    (32, "Rugby", "England 37\u201312 New Zealand"),
    (33, "Arsenal", "held 2\u20132 by Newcastle"),
    (34, "Columbus Crew", "beat Messi's Miami 3\u20130"),
    (35, "Russia", "says 170 Ukrainian drones downed \u2014 CLAIM"),
    (36, "Saudi", "downs a Houthi missile \u2014 CLAIM"),
    (37, "Riemann", "AI \u2018helps prove\u2019 the hypothesis"),
    (38, "Melbourne", "marks 70 years since the 1956 Games"),
    (39, "Markets", "gold near $5,555; Bitcoin over $60,000"),
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


def art_cop(x, y, w, h):
    # sun, a row of flags, the delegates' table with heads and a gavel,
    # and the rejected text under a red X
    d.ellipse([x + w - 52, y + 8, x + w - 24, y + 36], fill=GOLD)
    cols = [RED, GOLD, (52, 96, 66), INK, (84, 104, 128)]
    for i, c in enumerate(cols):
        fx = x + 18 + i * 26
        d.line([(fx, y + 14), (fx, y + 44)], fill=INK, width=2)
        d.rectangle([fx, y + 14, fx + 15, y + 25], fill=c)
    # delegates' table: a long table, a row of heads above it, papers
    tx0, tx1, ty = x + 14, x + w - 90, y + h - 8
    d.rectangle([tx0, ty - 7, tx1, ty], fill=INK)
    for i in range(6):
        hx = tx0 + 12 + i * 30
        d.ellipse([hx, ty - 19, hx + 10, ty - 9], fill=INK)
        d.rectangle([hx - 2, ty - 9, hx + 12, ty - 7], fill=INK2)
        d.rectangle([hx + 1, ty - 6, hx + 9, ty - 3],
                    fill=(252, 250, 244))
    # the chair's gavel, raised at the head of the table
    gx, gy = tx1 + 8, ty - 22
    d.line([(gx, gy + 12), (gx + 9, gy)], fill=INK, width=3)
    d.rectangle([gx + 6, gy - 5, gx + 15, gy + 2], fill=INK)
    d.rectangle([gx + 2, gy + 13, gx + 16, gy + 16], fill=INK2)
    dx, dy = x + w - 74, y + 30
    d.rectangle([dx, dy, dx + 44, dy + 34], fill=(252, 250, 244),
                outline=INK, width=2)
    d.line([(dx + 7, dy + 6), (dx + 37, dy + 28)], fill=RED, width=4)
    d.line([(dx + 37, dy + 6), (dx + 7, dy + 28)], fill=RED, width=4)


def art_drone(x, y, w, h):
    # three drones over a broken block; rubble, a rescue crane, and a
    # rescuer's lamp in the wreckage
    for (cx, cy) in [(x + 52, y + 18), (x + 128, y + 12), (x + 205, y + 20)]:
        d.line([(cx - 13, cy - 8), (cx + 13, cy + 8)], fill=INK, width=3)
        d.line([(cx - 13, cy + 8), (cx + 13, cy - 8)], fill=INK, width=3)
        d.rectangle([cx - 6, cy - 4, cx + 6, cy + 4], fill=INK)
    bx, by = x + 16, y + h - 6
    d.polygon([(bx, by), (bx, by - 44), (bx + 26, by - 44), (bx + 34, by - 30),
               (bx + 58, by - 38), (bx + 58, by)], fill=INK)
    for r_ in range(3):
        for c_ in range(2):
            d.rectangle([bx + 8 + c_ * 26, by - 36 + r_ * 13,
                         bx + 18 + c_ * 26, by - 28 + r_ * 13], fill=TINT2)
    # snapped floor slabs leaning out of the broken cross-section
    d.polygon([(bx + 58, by - 38), (bx + 88, by - 20), (bx + 90, by - 14),
               (bx + 58, by - 28)], fill=INK2)
    d.polygon([(bx + 58, by - 24), (bx + 80, by - 8), (bx + 82, by - 3),
               (bx + 58, by - 14)], fill=INK2)
    d.polygon([(bx + 66, by), (bx + 92, by - 16), (bx + 118, by)], fill=INK2)
    d.polygon([(bx + 100, by), (bx + 120, by - 10), (bx + 140, by)], fill=INK2)
    # rescue crane: mast, jib and a hook line over the rubble
    mx = x + w - 96
    d.line([(mx, by), (mx, y + 16)], fill=INK, width=3)
    d.line([(mx, y + 16), (mx + 62, y + 24)], fill=INK, width=3)
    d.line([(mx, y + 16), (mx - 14, by)], fill=INK2, width=1)
    d.line([(mx + 48, y + 22), (mx + 48, by - 18)], fill=INK, width=1)
    d.line([(mx + 43, by - 18), (mx + 53, by - 18)], fill=INK, width=2)
    d.rectangle([mx - 8, by - 3, mx + 8, by], fill=INK)
    lx, ly = x + w - 56, y + h - 26
    d.ellipse([lx - 9, ly - 9, lx + 9, ly + 9], fill=GOLD)
    for a in range(0, 360, 45):
        import math
        d.line([(lx, ly), (lx + 15 * math.cos(math.radians(a)),
                           ly + 15 * math.sin(math.radians(a)))],
               fill=GOLD, width=2)


def art_radar(x, y, w, h):
    # TWO Patriot radar dishes on masts, signal arcs, incoming tracks
    # kept inside the panel, the denial's shield, and tankers on the water
    import math
    gy = y + h - 16                     # ground line; sea below it

    def dish(cx, big):
        my = gy                           # mast foot
        d.polygon([(cx - 9, my), (cx - 2, my - 26), (cx + 2, my - 26),
                   (cx + 9, my)], fill=INK)
        d.rectangle([cx - 13, my - 29, cx + 13, my - 25], fill=INK)
        r = 17 if big else 13
        ccx, ccy = cx + 5, my - 29 - r + 4
        d.pieslice([ccx - r, ccy - r, ccx + r, ccy + r], start=140, end=320,
                   fill=INK)
        d.ellipse([ccx - 3, ccy - 3, ccx + 3, ccy + 3], fill=GOLD)
        d.line([(ccx, ccy), (ccx + 10, ccy - 9)], fill=INK, width=2)
        for rr in (8, 14, 20):
            d.arc([ccx + 8, ccy - rr, ccx + 8 + rr + 8, ccy + rr],
                  start=250, end=40, fill=INK2, width=2)
        return ccx, ccy

    dish(x + 46, True)
    dish(x + 116, False)
    # incoming tracks: flat arcs that stay inside the panel
    for (sx, sy, ex) in [(x + w - 16, y + 4, x + 196),
                         (x + w - 60, y + 2, x + 224)]:
        pts = []
        for t in range(21):
            tt = t / 20
            px = sx + (ex - sx) * tt
            py = sy + (y + 30 - sy) * tt - 9 * math.sin(tt * math.pi)
            pts.append((px, py))
        d.line(pts, fill=RED, width=2)
        d.polygon([(pts[-1][0], pts[-1][1]), (pts[-1][0] - 9, pts[-1][1] - 1),
                   (pts[-1][0] - 2, pts[-1][1] - 8)], fill=RED)
    # the shield of the denial, smaller, at the right
    sx, sy = x + w - 44, y + 22
    d.polygon([(sx, sy), (sx + 26, sy), (sx + 26, sy + 15), (sx + 13, sy + 27),
               (sx, sy + 15)], outline=INK, width=3)
    d.line([(sx + 7, sy + 11), (sx + 11, sy + 16), (sx + 20, sy + 6)],
           fill=(52, 96, 66), width=3)
    # the water, and two tankers on it
    d.line([(x + 4, gy), (x + w - 4, gy)], fill=INK2, width=1)
    for (hx, s) in [(x + 168, 1.0), (x + 238, 0.8)]:
        hw = 44 * s
        d.polygon([(hx, gy + 3), (hx + hw, gy + 3), (hx + hw - 6, gy + 10),
                   (hx + 5, gy + 10)], fill=INK)
        d.rectangle([hx + 8 * s, gy - 3, hx + 26 * s, gy + 3], fill=INK2)
        d.rectangle([hx + 30 * s, gy - 6, hx + 35 * s, gy + 3], fill=INK)
    for wx_ in range(int(x) + 10, int(x + w) - 12, 26):
        d.arc([wx_, gy + 9, wx_ + 12, gy + 15], start=0, end=180,
              fill=INK2, width=1)


LEAD_ART = [art_cop, art_drone, art_radar]


def icon(kind, cx, cy):
    """Tiny bold pictograms for the card art strips (centre cx, cy)."""
    if kind == "ballot":
        d.rectangle([cx - 13, cy + 1, cx + 13, cy + 11], outline=INK, width=2)
        d.rectangle([cx - 7, cy - 11, cx + 5, cy + 2], fill=(252, 250, 244),
                    outline=INK, width=2)
        d.line([(cx - 8, cy + 1), (cx + 8, cy + 1)], fill=RED, width=2)
    elif kind == "cricket":
        d.polygon([(cx - 4, cy - 12), (cx + 3, cy - 12), (cx + 6, cy + 6),
                   (cx + 1, cy + 12), (cx - 6, cy + 6)], fill=GOLD,
                  outline=INK)
        d.ellipse([cx + 8, cy + 2, cx + 18, cy + 12], fill=RED)
    elif kind == "race":
        for i in range(4):
            for j in range(2):
                if (i + j) % 2 == 0:
                    d.rectangle([cx - 16 + i * 8, cy - 12 + j * 8,
                                 cx - 8 + i * 8, cy - 4 + j * 8], fill=INK)
        d.rectangle([cx - 14, cy + 3, cx + 12, cy + 9], fill=RED)
        d.ellipse([cx - 10, cy + 7, cx - 3, cy + 13], fill=INK)
        d.ellipse([cx + 5, cy + 7, cx + 12, cy + 13], fill=INK)
    elif kind == "football":
        d.ellipse([cx - 11, cy - 11, cx + 11, cy + 11], outline=INK, width=2)
        d.polygon([(cx, cy - 5), (cx + 5, cy - 1), (cx + 3, cy + 5),
                   (cx - 3, cy + 5), (cx - 5, cy - 1)], fill=INK)
    elif kind == "tennis":
        d.ellipse([cx - 11, cy - 11, cx + 11, cy + 11], fill=(168, 178, 74))
        d.arc([cx - 11, cy - 11, cx + 3, cy + 11], start=90, end=270,
              fill=(252, 250, 244), width=2)
        d.arc([cx - 3, cy - 11, cx + 11, cy + 11], start=270, end=90,
              fill=(252, 250, 244), width=2)
    elif kind == "factory":
        d.rectangle([cx - 14, cy - 2, cx + 12, cy + 11], fill=INK)
        d.rectangle([cx + 6, cy - 12, cx + 12, cy - 2], fill=INK)
        d.polygon([(cx - 2, cy - 13), (cx + 3, cy - 5), (cx - 1, cy - 2),
                   (cx - 6, cy - 6)], fill=RED)
        d.polygon([(cx - 1, cy - 9), (cx + 2, cy - 5), (cx - 1, cy - 3),
                   (cx - 4, cy - 6)], fill=GOLD)
    elif kind == "basket":
        d.ellipse([cx - 11, cy - 11, cx + 11, cy + 11], fill=(206, 118, 44))
        d.line([(cx - 11, cy), (cx + 11, cy)], fill=INK, width=1)
        d.line([(cx, cy - 11), (cx, cy + 11)], fill=INK, width=1)
        d.arc([cx - 17, cy - 11, cx - 1, cy + 11], start=90, end=270,
              fill=INK, width=1)
        d.arc([cx + 1, cy - 11, cx + 17, cy + 11], start=270, end=90,
              fill=INK, width=1)
    elif kind == "power":
        d.polygon([(cx + 2, cy - 12), (cx - 7, cy + 2), (cx - 1, cy + 2),
                   (cx - 3, cy + 12), (cx + 8, cy - 3), (cx + 1, cy - 3)],
                  fill=GOLD, outline=INK)
    elif kind == "medical":
        d.ellipse([cx - 11, cy - 11, cx + 11, cy + 11],
                  fill=(252, 250, 244), outline=INK, width=2)
        d.rectangle([cx - 2, cy - 7, cx + 2, cy + 7], fill=RED)
        d.rectangle([cx - 7, cy - 2, cx + 7, cy + 2], fill=RED)
    elif kind == "ship":
        d.polygon([(cx - 15, cy + 3), (cx + 15, cy + 3), (cx + 10, cy + 11),
                   (cx - 11, cy + 11)], fill=INK)
        d.rectangle([cx - 8, cy - 3, cx + 6, cy + 3], fill=INK2)
        d.polygon([(cx + 2, cy - 13), (cx + 7, cy - 4), (cx + 3, cy - 2),
                   (cx - 2, cy - 6)], fill=RED)
    elif kind == "aid":
        d.rectangle([cx - 15, cy - 8, cx + 4, cy + 5], fill=(252, 250, 244),
                    outline=INK, width=2)
        d.rectangle([cx - 10, cy - 4, cx - 4, cy + 2], fill=RED)
        d.rectangle([cx - 13, cy - 1, cx - 2, cy + 2], fill=RED)
        d.polygon([(cx + 4, cy - 3), (cx + 11, cy - 3), (cx + 14, cy + 5),
                   (cx + 4, cy + 5)], fill=INK2)
        d.ellipse([cx - 10, cy + 4, cx - 4, cy + 10], fill=INK)
        d.ellipse([cx + 6, cy + 4, cx + 12, cy + 10], fill=INK)
    elif kind == "pope":
        d.pieslice([cx - 12, cy - 10, cx + 12, cy + 14], start=180, end=360,
                   fill=GOLD, outline=INK)
        d.rectangle([cx - 13, cy + 2, cx + 13, cy + 5], fill=INK)
        d.line([(cx, cy - 15), (cx, cy - 8)], fill=INK, width=2)
        d.line([(cx - 3, cy - 13), (cx + 3, cy - 13)], fill=INK, width=2)


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
    15: (0.484, 0.275), 2: (0.538, 0.20), 1: (0.540, 0.295),
    14: (0.556, 0.33), 3: (0.582, 0.355), 11: (0.590, 0.295),
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
                          fill=(172, 176, 154))
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
d.rectangle([0, 0, W, 106], fill=BAND)
center(11, "T H E   S U N D A Y   L E D G E R", F("pf8", 20),
       (238, 232, 210))
d.line([(M, 38), (W - M, 38)], fill=GOLD, width=1)
center(44, "Sunday 22 November 2026", F("pf9", 54), (247, 242, 228))
d.line([(0, 104), (W, 104)], fill=RED, width=2)

center(111, "39 STORIES \u00b7 7 REGIONS \u00b7 EVERY ONE DATED SUNDAY "
            "22 NOVEMBER 2026", F("bold", 12), INK)

# ---- strapline --------------------------------------------------------------
hrule(129)
center(133, STRAPLINE, F("bold", 14), RED)
hrule(153)

# ---- figures band -----------------------------------------------------------
fy = 158
cellw = CW / 6
for i, (num, lab) in enumerate(FIGURES):
    cx = M + i * cellw
    nf = F("pf8", 22 if len(num) <= 7 else 19)
    d.text((cx + (cellw - tw(num, nf)) / 2, fy), num, font=nf, fill=INK)
    lf = F("sans", 9)
    for j, ln in enumerate(lab.split("\n")):
        d.text((cx + (cellw - tw(ln, lf)) / 2, fy + 27 + j * 11), ln,
               font=lf, fill=INK2)
    if i:
        d.line([(cx, fy + 2), (cx, fy + 44)], fill=HAIR, width=1)
hrule(208)

# ---- region strip -----------------------------------------------------------
seg = "  \u00b7  ".join(f"{name} {n}" for name, n in REGIONS)
pre = "WHERE THE DAY HAPPENED \u2014  "
pf_, bf = F("bold", 11), F("bold", 11)
total = tw(pre, pf_) + tw(seg, bf)
sx = (W - total) / 2
d.text((sx, 214), pre, font=pf_, fill=RED)
d.text((sx + tw(pre, pf_), 214), seg, font=bf, fill=INK)
hrule(232)

# ---- timeline ---------------------------------------------------------------
d.text((M, 238), "THE DAY IN UTC", font=F("bold", 10.5), fill=RED)
tl_w = CW / 3
for i, (tm, txt) in enumerate(TIMELINE):
    cx = M + (i % 3) * tl_w
    cy = 254 + (i // 3) * 15
    d.text((cx, cy), tm, font=F("bold", 10), fill=RED)
    d.text((cx + tw(tm, F("bold", 10)) + 6, cy), txt, font=F("sans", 10),
           fill=INK)
hrule(288)

# ---- leads ------------------------------------------------------------------
ly = 294
lead_w = 309
for i, L in enumerate(LEADS):
    x = M + i * (lead_w + 24.5)
    panel(x, ly, lead_w, 68, L["tint"])
    LEAD_ART[i](x, ly, lead_w, 68)
    ry = ly + 74
    numb(x, ry, L["n"], r=8)
    d.text((x + 22, ry + 1), L["loc"], font=F("bold", 10.5), fill=INK)
    cw_ = int(tw(L["tag"], F("bold", 8))) + 10
    chip(x + lead_w - cw_, ry, L["tag"], RED if L["tag"] == "CLAIM" else INK)
    hy = ry + 20
    lines = wrap(L["head"], F("pf7", 17), lead_w)
    if len(lines) > 2:
        warn.append(f"lead {L['n']} headline {len(lines)} lines")
    for ln in lines[:2]:
        d.text((x, hy), ln, font=F("pf7", 17), fill=INK)
        hy += 21
    dy = hy + 3
    dlines = wrap(L["deck"], F("sans", 10.5), lead_w)
    if len(dlines) > 4:
        warn.append(f"lead {L['n']} deck {len(dlines)} lines")
    for ln in dlines[:4]:
        d.text((x, dy), ln, font=F("sans", 10.5), fill=INK)
        dy += 13
hrule(472)

# ---- cards ------------------------------------------------------------------
cy0 = 478
card_w, card_h = 238, 102
for idx, (n, loc, tag, head, deck, art) in enumerate(CARDS):
    x = M + (idx % 4) * (card_w + 8)
    y = cy0 + (idx // 4) * (card_h + 4)
    panel(x, y, card_w, 26, [TINT, TINT2, TINT3][idx % 3])
    icon(art, x + card_w / 2, y + 13)
    ry = y + 30
    numb(x, ry, n, r=7)
    d.text((x + 18, ry + 1), loc, font=F("bold", 8.5), fill=INK)
    cw_ = int(tw(tag, F("bold", 8))) + 10
    chip(x + card_w - cw_, ry, tag, INK)
    hy = y + 46
    hlines = wrap(head, F("bold", 12), card_w)
    if len(hlines) > 2:
        warn.append(f"card {n} headline {len(hlines)} lines")
    for ln in hlines[:2]:
        d.text((x, hy), ln, font=F("bold", 12), fill=INK)
        hy += 14
    dy = y + 76
    dlines = wrap(deck, F("sans", 9.5), card_w)
    if len(dlines) > 2:
        warn.append(f"card {n} deck {len(dlines)} lines: {deck[:40]}...")
    for ln in dlines[:2]:
        d.text((x, dy), ln, font=F("sans", 9.5), fill=INK)
        dy += 11.5
hrule(792)

# ---- bottom band: map + ALSO -------------------------------------------------
by = 798
d.text((M, by), "THE DAY MAPPED", font=F("bold", 10.5), fill=RED)
d.text((M + tw("THE DAY MAPPED", F("bold", 10.5)) + 8, by),
       "\u2014 pins match story numbers", font=F("sans", 9.5), fill=INK2)
draw_map(M, by + 16, 292, 104)
ax = M + 316
d.text((ax, by), "ALSO ON SUNDAY", font=F("bold", 10.5), fill=RED)
acol_w = (W - M - ax - 14) / 2
for i, (n, lead, rest) in enumerate(ALSO):
    cx = ax + (i // 12) * (acol_w + 14)
    cy = by + 16 + (i % 12) * 11
    nf = F("bold", 9.5)
    d.text((cx, cy), str(n), font=nf, fill=RED)
    x2 = cx + tw(str(n), nf) + 4
    d.text((x2, cy), lead, font=F("bold", 9.5), fill=INK)
    x3 = x2 + tw(lead, F("bold", 9.5)) + 3
    d.text((x3, cy), rest, font=F("sans", 9.5), fill=INK)
    if x3 + tw(rest, F("sans", 9.5)) > cx + acol_w:
        warn.append(f"also {n} overflows column")

# ---- date check ---------------------------------------------------------------
dy0 = 950
d.rectangle([M, dy0, W - M, dy0 + 42], outline=RED, width=2)
d.text((M + 12, dy0 + 6), "DATE", font=F("pf7", 13), fill=RED)
d.text((M + 12, dy0 + 22), "CHECK", font=F("pf7", 13), fill=RED)
block(M + 84, dy0 + 5, DATECHECK, F("sans", 9.5), INK, W - M - (M + 84) - 10,
      leading=1.3)

# ---- footer -------------------------------------------------------------------
center(996, SOURCES, F("sans", 9), INK2)
center(1009, KEYLINE, F("sans", 9), INK2)

img.save(OUT, format="JPEG", quality=88)
print("saved", OUT, os.path.getsize(OUT), "bytes")
for w_ in warn:
    print("WARN:", w_)
print("done")
