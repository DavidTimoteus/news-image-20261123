#!/usr/bin/env python3
"""Render the v2 front page for news-image-20261123 (Monday 23 Nov 2026).

Design: a dense one-page newspaper, 1024x1024, built to the pattern
the Track A winners show: one lead, four big headlines, then a dated
"day in brief" grid — 32 stories in total, every one dated 23 Nov 2026,
grouped by region. Text is wrapped by measured pixel width so nothing
overlaps; the brief items use a bold date tag plus one short headline.

Run: python3 render_image.py  -> writes entry.png beside this file.
Deterministic: no randomness, no network, no timestamps in the image.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

BLACK = (15, 15, 15)
INK = (30, 30, 30)
GREY = (110, 110, 110)
RED = (158, 20, 20)
RULE = (180, 180, 180)
PAPER = (255, 255, 255)
BAND = (245, 242, 235)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Wrap text to lines that fit max_w pixels (measured, not guessed)."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, text, fnt, x, y, max_w, fill=INK, leading=None):
    lh = leading or int(fnt.size * 1.28)
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    m = 28  # margin
    x0, x1 = m, W - m

    # ---- Masthead -------------------------------------------------------
    f_mast = font(SERIF, 58)
    d.text((x0, 14), "THE WORLD IN ONE DAY", font=f_mast, fill=BLACK)
    d.line([(x0, 86), (x1, 86)], fill=BLACK, width=3)
    f_date = font(SANS_B, 20)
    d.text((x0, 94), "MONDAY, 23 NOVEMBER 2026", font=f_date, fill=RED)
    f_meta = font(SANS, 17)
    meta = "32 STORIES  •  6 REGIONS  •  EVERY STORY DATED 23 NOV 2026"
    mw = d.textlength(meta, font=f_meta)
    d.text((x1 - mw, 96), meta, font=f_meta, fill=GREY)
    d.line([(x0, 126), (x1, 126)], fill=BLACK, width=1)

    # ---- Lead: COP31 ----------------------------------------------------
    y = 138
    d.rectangle([x0, y, x1, y + 118], fill=BAND, outline=RULE, width=1)
    f_kick = font(SANS_B, 14)
    d.text((x0 + 14, y + 8), "LEAD  —  CLIMATE", font=f_kick, fill=RED)
    f_lead = font(SERIF, 30)
    y2 = draw_wrapped(d, "COP31 collapses: no deal on fossil fuels",
                      f_lead, x0 + 14, y + 28, x1 - x0 - 28, fill=BLACK)
    f_body = font(SANS, 17)
    draw_wrapped(
        d,
        "The longest UN climate talks in history end in Antalya with no "
        "agreement. The final draft never mentions fossil fuels; the EU "
        "and Pacific islands refuse a deal without it. First failure since 2009.",
        f_body, x0 + 14, y2 + 2, x1 - x0 - 28)
    y = y + 118 + 12

    # ---- Four big headlines, 2 x 2 --------------------------------------
    heads = [
        ("1  IRAN WAR WIDENS",
         "Iran strikes a Bahrain industrial site, injuring two, and hits "
         "tankers in the Strait of Hormuz; Trump says Tehran wants a deal "
         "he cannot accept."),
        ("2  UKRAINE SINKS WARSHIP",
         "Zelenskyy confirms naval drones sank the Russian corvette "
         "Merkury off Benghazi and hit the cargo ship Angara."),
        ("3  RUSSIA HITS KYIV REGION",
         "Strikes kill 11 in Dymer, a child among them; a block of flats "
         "is partly destroyed and 14 people are missing."),
        ("4  DEMOCRATS WIN THE HOUSE",
         "At least 258 seats — the largest House majority since 1992. "
         "Trump moves to block oversight."),
    ]
    col_w = (x1 - x0 - 16) // 2
    row_h = 118
    f_h = font(SERIF, 19)
    f_hb = font(SANS, 15)
    for i, (title, body) in enumerate(heads):
        cx = x0 + (i % 2) * (col_w + 16)
        cy = y + (i // 2) * (row_h + 10)
        d.rectangle([cx, cy, cx + col_w, cy + row_h], outline=RULE, width=1)
        d.text((cx + 10, cy + 8), title, font=f_h, fill=BLACK)
        draw_wrapped(d, body, f_hb, cx + 10, cy + 34, col_w - 20, leading=19)
    y = y + 2 * row_h + 10 + 12

    # ---- Day in brief: 27 more stories, 3 columns -----------------------
    d.line([(x0, y), (x1, y)], fill=BLACK, width=2)
    y += 8
    f_sec = font(SANS_B, 17)
    d.text((x0, y), "THE DAY IN BRIEF — 27 MORE STORIES, ALL 23 NOVEMBER 2026",
           font=f_sec, fill=BLACK)
    y += 26
    d.line([(x0, y), (x1, y)], fill=RULE, width=1)
    y += 10

    brief = [
        ("MIDDLE EAST", "Trump 'inclined' to resume war if no Iran deal by New Year"),
        ("MIDDLE EAST", "Gaza food-truck strike kills three, health ministry says"),
        ("MIDDLE EAST", "Houthis claim a strike on Saudi Arabia's Rabigh refinery"),
        ("EUROPE", "Kryvyi Rih strike kills a child and a young woman"),
        ("EUROPE", "NATO meets after Russian missiles enter Polish airspace"),
        ("EUROPE", "Denmark expels Russia's defence attache over 'Kyivstoner' plot"),
        ("EUROPE", "NATO intel: Russia plans a nuclear-armed satellite"),
        ("EUROPE", "Russia hits Ukrainian energy sites; power cuts spread"),
        ("EUROPE", "Finland tows damaged Russian cargo ship out; 16 crew safe"),
        ("ASIA", "Indonesia candy-factory fire kills 24; about 30 missing"),
        ("ASIA", "EU and Indonesia sign trade deal; most tariffs go"),
        ("ASIA", "Prabowo names Sugiono and Amran Sulaiman as VP picks"),
        ("ASIA", "India gives Nepal $1.62bn in aid after the floods"),
        ("TECH", "Nvidia board reinstates Jensen Huang as CEO"),
        ("TECH", "US blacklists Megaspeed over the Nvidia spy scandal"),
        ("TECH", "Anthropic says AI helped prove Riemann — claim debated"),
        ("TECH", "US stock futures rebound after the AI tech rout"),
        ("AMERICAS", "Trump expects China to buy 250 more Boeing jets"),
        ("AMERICAS", "Trump hosts dinner for top holders of his meme coin"),
        ("AMERICAS", "Senate talks: fund the Pentagon, cut Iran war money"),
        ("SPORT", "Liverpool thrash Man Utd 4-0 in Pochettino's debut"),
        ("SPORT", "49ers rout Vikings 35-10 in Mexico City"),
        ("SPORT", "Eagles end seven-game skid, beat Steelers 19-16"),
        ("SPORT", "Cowboys rout Titans 51-30; Prescott throws five TDs"),
        ("SPORT", "Alcaraz beats Zverev for his first ATP Finals title"),
        ("SPORT", "Skubal agrees record nine-year, $450m Mets deal"),
        ("SPACE", "BepiColombo reaches Mercury orbit despite engine glitch"),
    ]
    assert len(brief) == 27, len(brief)
    f_tag = font(SANS_B, 12)
    f_item = font(SANS, 13)
    col_w2 = (x1 - x0 - 2 * 14) // 3
    row_h2 = 46
    for i, (tag, text) in enumerate(brief):
        cx = x0 + (i % 3) * (col_w2 + 14)
        cy = y + (i // 3) * row_h2
        d.text((cx, cy), f"23 NOV · {tag}", font=f_tag, fill=RED)
        draw_wrapped(d, text, f_item, cx, cy + 16, col_w2, leading=16)
    y = y + 9 * row_h2 + 8

    # ---- Footer ---------------------------------------------------------
    d.line([(x0, y), (x1, y)], fill=BLACK, width=1)
    f_foot = font(SANS, 13)
    d.text((x0, y + 6),
           "Sources: Just Security Early Edition 23 Nov 2026; AP; Reuters; BBC; "
           "Xinhua; ESA; Nvidia; Anthropic. All 32 stories reported 23 Nov 2026.",
           font=f_foot, fill=GREY)

    img.save("entry.png", format="PNG", optimize=True)
    print(f"wrote entry.png {img.size}")


if __name__ == "__main__":
    main()
