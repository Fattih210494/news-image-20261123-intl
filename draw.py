#!/usr/bin/env python3
"""Render entry.png for news-image-20261123 (international newspaper).

Fresh renderer for the 'Global Herald' concept: big masthead, world-map
strip with numbered pins, burning-tanker hero, two hero panels, a dense
left column of small stories (3 columns x 6 rows) and a right column
with a stat strip + ALSO TODAY list. Deterministic: no network, no
clock, no randomness. Hero art is cropped from the generated concept
image in assets/ (a generated illustration, not a news photo).
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (17, 17, 17)
RED = (176, 42, 42)
DARKRED = (139, 30, 30)
GREY = (105, 100, 90)
LINE = (198, 192, 176)
LIGHT = (233, 228, 214)
SKY = (214, 226, 232)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANSB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, f, max_w):
    """Greedy word wrap to a list of lines fitting max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(d, lines, x, y, f, fill=INK, lh=None):
    if lh is None:
        lh = f.size + 3
    for ln in lines:
        d.text((x, y), ln, font=f, fill=fill)
        y += lh
    return y


def rule(d, x0, y, x1, w=1, fill=INK):
    d.line([(x0, y), (x1, y)], fill=fill, width=w)


def pin(d, x, y, n):
    d.ellipse([x - 10, y - 10, x + 10, y + 10], fill=RED, outline=(255, 255, 255), width=2)
    f = font(SANSB, 11)
    t = str(n)
    d.text((x - d.textlength(t, font=f) / 2, y - 8), t, font=f, fill=(255, 255, 255))


def mountains(d, x, y, w, h):
    """Small flat mountain illustration for the Peru panel."""
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.polygon([(x, y + h), (x + w * 0.28, y + h * 0.25), (x + w * 0.52, y + h)], fill=(96, 110, 128))
    d.polygon([(x + w * 0.38, y + h), (x + w * 0.66, y + h * 0.12), (x + w * 0.95, y + h)], fill=(70, 82, 100))
    d.polygon([(x + w * 0.60, y + h * 0.22), (x + w * 0.66, y + h * 0.12), (x + w * 0.72, y + h * 0.22),
               (x + w * 0.68, y + h * 0.30), (x + w * 0.64, y + h * 0.26)], fill=(255, 255, 255))
    pts = [(x + w * 0.18, y + h * 0.55), (x + w * 0.30, y + h * 0.68), (x + w * 0.44, y + h * 0.58),
           (x + w * 0.58, y + h * 0.72), (x + w * 0.72, y + h * 0.60), (x + w + 2, y + h * 0.74)]
    d.line(pts, fill=RED, width=3)
    f = font(SANSB, 20)
    d.text((x + 6, y + h - 26), "6.9", font=f, fill=(255, 255, 255))


def summit(d, x, y, w, h):
    """Small flat summit-table illustration for the COP31 panel."""
    d.rectangle([x, y, x + w, y + h], fill=(226, 222, 205))
    d.rectangle([x + 8, y + h * 0.62, x + w - 8, y + h * 0.72], fill=(90, 70, 50))
    flags = [(140, 90, 200), (60, 110, 70), (200, 160, 60)]
    for i, c in enumerate(flags):
        fx = x + 12 + i * 24
        d.rectangle([fx, y + h * 0.30, fx + 18, y + h * 0.58], fill=c)
        d.line([(fx + 18, y + h * 0.30), (fx + 18, y + h * 0.62)], fill=INK, width=1)
    d.arc([x + w * 0.55, y + 6, x + w - 6, y + h * 0.55], start=200, end=340, fill=RED, width=4)
    f = font(SANSB, 15)
    d.text((x + 6, y + h - 22), "NO DEAL", font=f, fill=DARKRED)


# ---- story data: (number, region, headline, deck) ----
LEFT = [
    (4, "EUROPE", "Russian cargo ship still burning off Finland",
     "Drone strike in the Baltic Sea; Helsinki on alert as the fire rages on."),
    (5, "EUROPE", "Drone hits Kyiv flat block, 14 missing",
     "Rescuers search rubble in Dymer; two children among the missing."),
    (6, "EUROPE", "Poland: Russian missiles crossed border",
     "NATO jets scramble as two missiles and a drone crash in Poland."),
    (7, "ASIA", "Sweets factory fire: 24 body bags found",
     "Dozens still missing in Cikande, Banten; the search resumes Monday."),
    (8, "ASIA", "Seoul minister quits over exam AI chaos",
     "Education chief Choi Kyo-jin resigns after entrance-exam uproar."),
    (9, "EUROPE", "UK and EU agree Brexit reset deal",
     "Food trade, carbon and youth mobility covered; tuition row remains."),
    (10, "SPORT", "Rahul's 117* puts India 309/2 in Wellington",
     "India trail New Zealand's 368 on day four of the first Test."),
    (11, "ASIA", "ICJ: evidence of genocide against Rohingya",
     "Myanmar's junta calls the ASEAN decision 'unfair and imbalanced'."),
    (12, "ASIA", "Japan and India deepen defence ties",
     "Japanese troops to use Indian ranges for live-fire training."),
    (13, "ASIA", "China builds new South China Sea runway",
     "Satellite images show a bigger military footprint on disputed isles."),
    (14, "AFRICA", "Sea drones hit Russian warship in Libya",
     "Corvette Merkury capsizes at Benghazi; ten people injured."),
    (15, "AMERICAS", "Hegseth curbs US-Canada defence ties",
     "Classified memo imposes new limits on the alliance, Post reports."),
    (16, "WORLD", "BepiColombo enters orbit around Mercury",
     "Only the second mission ever to circle the innermost planet."),
    (17, "ASIA", "Lahore world's most polluted city again",
     "AQI hits 538 on Sunday morning, IQAir data shows."),
    (18, "AFRICA", "Drones strike Khartoum, hit UN facility",
     "At least three killed in Omdurman as the war grinds on."),
    (19, "MIDDLE EAST", "Settlers torch 12 cars near Ramallah",
     "Racist graffiti sprayed in four West Bank villages overnight."),
    (20, "ASIA", "Shuri Castle rises again in Okinawa",
     "Restored main hall opens seven years after the 2019 fire."),
    (21, "SPORT", "Alcaraz wins first ATP Finals title",
     "Spaniard beats Zverev to close the season on top."),
]

ALSO = [
    (22, "Thitikul wins third straight LPGA title with a 65 in the finale"),
    (23, "FIFA to confirm UK as 2035 Women's World Cup host"),
    (24, "Markets slide: KOSPI -4%, Shanghai under 3,500, gold $3,603"),
    (25, "UN states keep talking on lethal AI weapons"),
    (26, "Thousands march in Lisbon over living costs"),
    (27, "Xi, Trump and Putin's Shenzhen summit still echoes"),
    (28, "'El Chapo Isidro' held; 11 killed in Sinaloa"),
    (29, "Bolsonaro in ICU with bowel obstruction"),
    (30, "Nvidia row: Huang tied to chip diversion network"),
]

STATS = [
    ("120+", "vessels attacked\nin the Strait"),
    ("24", "seafarers killed\nsince February"),
    ("6.9", "Peru quake\nmagnitude"),
    ("93,000", "without power\nin Peru"),
    ("538", "Lahore AQI\non Sunday"),
    ("$3,603", "gold per ounce\nup ~2%"),
]

GLANCE = [
    "Strait carries ~20% of global oil supply",
    "120+ vessels attacked since February",
    "24 seafarers killed; LPG tanker burned 17 Nov",
    "US struck Qeshm; Iran hit assets in Kuwait, Bahrain",
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    concept = Image.open(os.path.join(HERE, "assets", "concept20.webp")).convert("RGB")

    # ---- masthead ----
    f_mast = font(SERIF, 54)
    t = "THE GLOBAL HERALD"
    d.text(((W - d.textlength(t, font=f_mast)) / 2, 6), t, font=f_mast, fill=INK)
    f_sub = font(SANSB, 11)
    t = "I N T E R N A T I O N A L   •   I N D E P E N D E N T   •   M O N D A Y  2 3  N O V E M B E R  2 0 2 6"
    d.text(((W - d.textlength(t, font=f_sub)) / 2, 66), t, font=f_sub, fill=INK)
    rule(d, 24, 80, 1000, 2)

    # ---- world map strip (cropped from concept art) ----
    map_art = concept.crop((88, 220, 1560, 355)).resize((976, 90), Image.LANCZOS)
    img.paste(map_art, (24, 84))
    d.rectangle([24, 84, 1000, 174], outline=INK, width=1)
    for n, fx, fy in [(1, 0.60, 0.48), (2, 0.295, 0.68), (3, 0.56, 0.42),
                      (4, 0.53, 0.18), (7, 0.80, 0.65), (8, 0.845, 0.32), (17, 0.70, 0.45)]:
        pin(d, 24 + int(fx * 976), 84 + int(fy * 90), n)
    f_cap = font(SANSB, 9)
    t = "GLOBAL OVERVIEW  •  MONDAY, NOVEMBER 23, 2026  •  30 STORIES FROM EVERY CONTINENT  •  PAGE 1"
    d.text(((W - d.textlength(t, font=f_cap)) / 2, 179), t, font=f_cap, fill=GREY)

    # ---- main headline + breaking tag ----
    f_head = font(SERIF, 40)
    d.text((24, 196), "THE GULF ON FIRE", font=f_head, fill=INK)
    d.rectangle([700, 200, 1000, 232], fill=RED)
    f_br = font(SANSB, 14)
    t = "BREAKING  •  DEVELOPING"
    d.text((700 + (300 - d.textlength(t, font=f_br)) / 2, 208), t, font=f_br, fill=(255, 255, 255))
    f_deck = font(SANS, 13)
    d.text((24, 240), "Two more tankers hit near the Strait of Hormuz as attacks on shipping pass 120 since February.",
           font=f_deck, fill=INK)

    # ---- hero row ----
    HY, HH = 258, 205
    tanker = concept.crop((88, 585, 656, 841)).resize((456, HH), Image.LANCZOS)
    img.paste(tanker, (24, HY))
    d.rectangle([24, HY, 480, HY + HH], outline=INK, width=1)
    d.rectangle([24, HY + HH - 22, 480, HY + HH], fill=INK)
    f_cap2 = font(SANS, 10)
    d.text((30, HY + HH - 17), "1  •  A tanker burns in the Strait of Hormuz — the war's newest front.",
           font=f_cap2, fill=(255, 255, 255))

    # AT A GLANCE box
    gx, gw = 492, 208
    d.rectangle([gx, HY, gx + gw, HY + HH], outline=INK, width=1)
    d.rectangle([gx, HY, gx + gw, HY + 28], fill=RED)
    f_gh = font(SANSB, 12)
    d.text((gx + 8, HY + 7), "AT A GLANCE", font=f_gh, fill=(255, 255, 255))
    f_gl = font(SANS, 10)
    yy = HY + 36
    for b in GLANCE:
        for ln in wrap(d, "•  " + b, f_gl, gw - 16):
            d.text((gx + 8, yy), ln, font=f_gl, fill=INK)
            yy += 13
        yy += 4

    # hero panels 2-3
    px, pw = 712, 288
    # Peru
    py = HY
    d.rectangle([px, py, px + pw, py + 98], outline=INK, width=1)
    mountains(d, px + 1, py + 1, 82, 96)
    f_tag = font(SANSB, 9)
    d.text((px + 92, py + 6), "2  •  AMERICAS", font=f_tag, fill=RED)
    f_ph = font(SANSB, 12)
    yy = draw_lines(d, wrap(d, "6.9 quake shakes Peru's Andes", f_ph, pw - 100), px + 92, py + 20, f_ph, lh=14)
    f_pd = font(SANS, 9)
    draw_lines(d, wrap(d, "1 dead, 16 hurt, 156 homes damaged, 93,000 without power.", f_pd, pw - 100),
               px + 92, yy + 2, f_pd, lh=11)
    # COP31
    py = HY + 102
    d.rectangle([px, py, px + pw, py + 103], outline=INK, width=1)
    summit(d, px + 1, py + 1, 82, 101)
    d.text((px + 92, py + 6), "3  •  WORLD", font=f_tag, fill=RED)
    yy = draw_lines(d, wrap(d, "COP31 collapses in Antalya", f_ph, pw - 100), px + 92, py + 20, f_ph, lh=14)
    draw_lines(d, wrap(d, "EU rejects a draft that never says 'fossil fuels'; no deal is reached.", f_pd, pw - 100),
               px + 92, yy + 2, f_pd, lh=11)

    # ---- section header ----
    rule(d, 24, 476, 1000, 2)
    f_sec = font(SERIF, 15)
    t = "WORLD IN BRIEF  —  NEWS FROM ALL CONTINENTS"
    d.text(((W - d.textlength(t, font=f_sec)) / 2, 482), t, font=f_sec, fill=INK)
    rule(d, 24, 502, 1000, 1)

    # ---- LEFT dense zone: 3 cols x 6 rows, stories 4-21 ----
    LX, LW = 24, 576
    TOP, ROWH = 508, 81
    cols = [LX, LX + 192, LX + 384]
    cw = 184
    f_tag2 = font(SANSB, 9)
    f_hl = font(SANSB, 11)
    f_dk = font(SANS, 9)
    for i, (n, region, hl, dk) in enumerate(LEFT):
        col, row = i % 3, i // 3
        x = cols[col]
        y = TOP + row * ROWH
        if row > 0:
            d.line([(x, y - 4), (x + cw, y - 4)], fill=LINE, width=1)
        d.text((x, y), f"{n}  •  {region}", font=f_tag2, fill=RED)
        yy = draw_lines(d, wrap(d, hl, f_hl, cw)[:3], x, y + 13, f_hl, lh=13)
        draw_lines(d, wrap(d, dk, f_dk, cw)[:2], x, yy + 1, f_dk, lh=11)
    # vertical divider
    d.line([(608, 508), (608, 984)], fill=LINE, width=1)

    # ---- RIGHT zone ----
    RX, RW = 616, 384
    # stat strip
    f_sh = font(SANSB, 11)
    d.text((RX, 508), "THE DAY IN NUMBERS", font=f_sh, fill=INK)
    rule(d, RX, 524, RX + RW, 1)
    f_num = font(SANSB, 16)
    f_lab = font(SANS, 8)
    sw = RW // 3
    for i, (num, lab) in enumerate(STATS):
        cx = RX + (i % 3) * sw
        cy = 528 + (i // 3) * 32
        d.text((cx, cy), num, font=f_num, fill=DARKRED)
        for j, ln in enumerate(lab.split("\n")):
            d.text((cx, cy + 18 + j * 9), ln, font=f_lab, fill=GREY)
    rule(d, RX, 600, RX + RW, 1)
    # ALSO TODAY
    d.text((RX, 608), "ALSO TODAY", font=f_sh, fill=INK)
    rule(d, RX, 624, RX + RW, 1)
    f_ah = font(SANSB, 10)
    yy = 630
    for n, hl in ALSO:
        lines = wrap(d, hl, f_ah, RW - 30)[:2]
        d.text((RX, yy), f"{n}.", font=f_ah, fill=RED)
        draw_lines(d, lines, RX + 26, yy, f_ah, lh=12)
        yy += max(24, len(lines) * 12 + 12)
    # date check box
    by = 930
    d.rectangle([RX, by, RX + RW, 984], outline=INK, width=1)
    d.rectangle([RX, by, RX + RW, by + 16], fill=INK)
    f_bh = font(SANSB, 9)
    d.text((RX + 6, by + 3), "DATE CHECK", font=f_bh, fill=(255, 255, 255))
    f_bb = font(SANS, 9)
    draw_lines(d, wrap(d, "All 30 stories verified from news reported 22–23 Nov 2026. Sources in STORIES.md.",
                       f_bb, RW - 12), RX + 6, by + 20, f_bb, lh=11)

    # ---- footer ----
    rule(d, 24, 994, 1000, 2)
    f_ft = font(SANSB, 9)
    t = "THE GLOBAL HERALD  •  MONDAY 23 NOVEMBER 2026  •  30 VERIFIED STORIES FROM EVERY CONTINENT"
    d.text(((W - d.textlength(t, font=f_ft)) / 2, 1000), t, font=f_ft, fill=GREY)

    out = os.path.join(HERE, "entry.png")
    img.save(out, "JPEG", quality=88, optimize=True)
    print("wrote", out)


if __name__ == "__main__":
    main()
