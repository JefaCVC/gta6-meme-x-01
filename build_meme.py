#!/usr/bin/env python3
"""Build the GTA 6 meme for make.fun bounty gta6-meme-x-01.

Concept: GTA's iconic "WASTED" screen, but the thing wasted is 13 years of
waiting for GTA 6. Vice City sunset scene, make.fun ghost badge worked in as
a character in the bottom band with the pitch line in the meme's own voice.
Canvas 1200x675 (16:9, X-friendly). All text measured against its box.
"""
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1200, 675
OUT = "/home/hatch/workspace/makefun/gta6-meme-x-01/meme.png"
MARK = "/tmp/press/mark-1024.png"

BLACK = "/usr/share/fonts/truetype/noto/NotoSansDisplay-Black.ttf"
XBOLD = "/usr/share/fonts/truetype/noto/NotoSans-ExtraBold.ttf"
BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"

img = Image.new("RGB", (W, H))
d = ImageDraw.Draw(img)

# --- sky gradient: deep purple -> magenta -> orange, horizon at y=430 ---
stops = [(0, (26, 11, 46)), (180, (74, 18, 89)), (300, (160, 21, 94)),
         (430, (249, 115, 22))]
ocean_stops = [(430, (120, 45, 70)), (520, (30, 10, 40)), (675, (16, 6, 26))]

def color_at(stops_, y):
    for i in range(len(stops_) - 1):
        y0, c0 = stops_[i]
        y1, c1 = stops_[i + 1]
        if y0 <= y <= y1:
            t = (y - y0) / max(1, y1 - y0)
            return tuple(int(c0[k] + (c1[k] - c0[k]) * t) for k in range(3))
    return stops_[-1][1]

for y in range(430):
    d.line([(0, y), (W, y)], fill=color_at(stops, y))

# --- sun with synthwave slats (clipped at the horizon) ---
SUN_C, SUN_R = (600, 400), 165
d.ellipse([SUN_C[0] - SUN_R, SUN_C[1] - SUN_R,
           SUN_C[0] + SUN_R, SUN_C[1] + SUN_R], fill=(255, 209, 102))
for sy, th in [(330, 3), (358, 4), (385, 5), (408, 7)]:
    d.rectangle([SUN_C[0] - SUN_R - 2, sy, SUN_C[0] + SUN_R + 2, sy + th],
                fill=color_at(stops, sy))

# --- ocean gradient below the horizon (covers the sun's lower half) ---
for y in range(430, H):
    d.line([(0, y), (W, y)], fill=color_at(ocean_stops, y))

# --- skyline silhouette (dark purple) along the horizon ---
import random
random.seed(6)
SKY = (18, 8, 31)
x = -10
while x < W + 10:
    bw = random.randint(55, 130)
    bh = random.randint(60, 190)
    d.rectangle([x, 430 - bh, x + bw, 430], fill=SKY)
    # antenna on some towers
    if random.random() < 0.35:
        d.line([x + bw // 2, 430 - bh, x + bw // 2, 430 - bh - 28],
               fill=SKY, width=4)
    # lit windows
    for _ in range(random.randint(2, 8)):
        wx = x + random.randint(6, max(7, bw - 10))
        wy = 430 - bh + random.randint(8, max(9, bh - 12))
        d.rectangle([wx, wy, wx + 5, wy + 7], fill=(255, 214, 120))
    x += bw + random.randint(2, 14)

# --- ocean: sun-reflection streaks, clustered under the sun ---
for i in range(14):
    y = 442 + i * 8
    wdt = random.randint(50, 170)
    cx = 600 + random.randint(-180, 180)
    col = (249, 115, 22) if i < 4 else (210, 70, 110) if i < 9 else (130, 45, 95)
    d.line([cx - wdt // 2, y, cx + wdt // 2, y], fill=col, width=3)

# --- palm silhouettes, left and right foreground ---
def bez(p0, p1, p2, n=24):
    pts = []
    for i in range(n + 1):
        t = i / n
        pts.append(((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0],
                    (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]))
    return pts

def palm(cx, base_y, s, direction):
    # curved trunk rising to the crown
    crown = (cx + direction * 42 * s, base_y - 215 * s)
    mid = (cx + direction * 8 * s, base_y - 110 * s)
    d.line(bez((cx, base_y), mid, crown), fill=SKY,
           width=int(14 * s), joint="curve")
    # 7 fronds fanning from the crown, arching up then drooping at the tips
    for k in range(7):
        a = math.pi * (0.05 + 0.9 * k / 6)
        L = 105 * s * (0.85 + 0.25 * math.sin(k * 1.7))
        ex = crown[0] + math.cos(a) * L
        ey = crown[1] - math.sin(a) * L * 0.6 + 70 * s
        ctrl = ((crown[0] + ex) / 2, crown[1] - 45 * s - math.sin(a) * 30 * s)
        d.line(bez(crown, ctrl, (ex, ey)), fill=SKY,
               width=int(8 * s), joint="curve")
    # coconuts under the crown
    d.ellipse([crown[0] - 10 * s, crown[1] + 2, crown[0] + 10 * s,
               crown[1] + 14 * s], fill=SKY)

palm(90, 680, 1.45, 1)
palm(1110, 685, 1.55, -1)

# --- soft vignette ---
vig = Image.new("L", (W, H), 0)
vd = ImageDraw.Draw(vig)
vd.ellipse([-W * 0.25, -H * 0.35, W * 1.25, H * 1.35], fill=255)
vig = vig.filter(ImageFilter.GaussianBlur(90))
black = Image.new("RGB", (W, H), (0, 0, 0))
img = Image.composite(img, black, vig.point(lambda p: 255 - int((255 - p) * 0.45)))
d = ImageDraw.Draw(img)

# --- top-left location tag, GTA style ---
loc_font = ImageFont.truetype(BOLD, 30)
d.text((42, 28), "VICE CITY, LEONIDA", font=loc_font, fill=(255, 255, 255),
       stroke_width=3, stroke_fill=(10, 5, 18))

# --- wanted stars, top-right ---
def star(cx, cy, r, fill, outline=None):
    pts = []
    for i in range(10):
        rr = r if i % 2 == 0 else r * 0.45
        a = -math.pi / 2 + i * math.pi / 5
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=fill, outline=outline)

for i in range(5):
    star(1020 + i * 34, 46, 13, (255, 200, 60), (10, 5, 18))

# --- WASTED: huge, letterspaced, white with black outline ---
def draw_tracked(cx, y, text, font, tracking, fill, stroke_w, stroke_fill):
    widths = [d.textlength(ch, font=font) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = cx - total / 2
    for ch, wch in zip(text, widths):
        d.text((x, y), ch, font=font, fill=fill,
               stroke_width=stroke_w, stroke_fill=stroke_fill)
        x += wch + tracking
    return total

wasted_font = ImageFont.truetype(BLACK, 168)
tw = draw_tracked(600, 118, "WASTED", wasted_font, 14,
                  (248, 248, 248), 7, (12, 6, 20))
assert tw < W - 80, f"WASTED too wide: {tw}"

# --- subtitle ---
sub_font = ImageFont.truetype(XBOLD, 46)
sub = "13 YEARS WAITING FOR GTA 6"
sw = d.textlength(sub, font=sub_font)
assert sw < W - 80, f"subtitle too wide: {sw}"
d.text(((W - sw) / 2, 308), sub, font=sub_font, fill=(255, 255, 255),
       stroke_width=4, stroke_fill=(12, 6, 20))

# --- bottom band: ghost badge + pitch line ---
band = Image.new("RGBA", (W, H), (0, 0, 0, 0))
bd = ImageDraw.Draw(band)
bd.rounded_rectangle([48, 540, 1152, 648], radius=22, fill=(8, 4, 16, 205))
img = Image.alpha_composite(img.convert("RGBA"), band)
d = ImageDraw.Draw(img)

mark = Image.open(MARK).convert("RGBA").resize((96, 96), Image.LANCZOS)
img.paste(mark, (66, 546), mark)
d = ImageDraw.Draw(img)

pitch_font = ImageFont.truetype(XBOLD, 33)
pitch1 = "my AI agent earned real money while I waited"
pitch2 = "make.fun"
p1w = d.textlength(pitch1, font=pitch_font)
assert 180 + p1w < 1130, f"pitch too wide: {p1w}"
d.text((180, 556), pitch1, font=pitch_font, fill=(255, 255, 255))
d.text((180, 598), pitch2, font=ImageFont.truetype(XBOLD, 30),
       fill=(255, 77, 168))

img.convert("RGB").save(OUT, "PNG")
print("saved", OUT, img.size)

# 30% thumbnail for the legibility check
img.convert("RGB").resize((360, 203), Image.LANCZOS).save("/tmp/meme-30pct.png")
print("saved /tmp/meme-30pct.png")
