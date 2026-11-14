#!/usr/bin/env python3
"""Draw a top-down poke bowl, 1024x1024, procedurally with Pillow.

A glossy poke bowl on a dark walnut table: sushi rice, salmon and tuna
cubes, avocado fan, mango, edamame, cucumber, pickled ginger, seaweed
salad, tobiko, scallions, sesame and a spicy-mayo drizzle. Rendered at
build time; the entry ships the PNG and main.py only copies it.
"""
import math
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

W = 1024
rng = random.Random(20261114)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def ellipse_gradient(draw, box, top, bottom):
    """Vertical gradient fill inside an ellipse, via horizontal strips."""
    x0, y0, x1, y1 = box
    h = max(1, y1 - y0)
    for y in range(y0, y1 + 1):
        t = (y - y0) / h
        c = lerp(top, bottom, t)
        # chord width at this y
        cy = (y - (y0 + y1) / 2) / ((y1 - y0) / 2)
        if abs(cy) > 1:
            continue
        hw = ((x1 - x0) / 2) * math.sqrt(1 - cy * cy)
        cx = (x0 + x1) / 2
        draw.line([(cx - hw, y), (cx + hw, y)], fill=c)


def soft_shadow(base, box, blur=18, alpha=110):
    layer = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse(box, fill=(0, 0, 0, alpha))
    layer = layer.filter(ImageFilter.GaussianBlur(blur))
    return Image.alpha_composite(base.convert("RGBA"), layer).convert("RGB")


def grain(img, amount=9):
    arr = np.asarray(img).astype(np.int16)
    noise = rng_np.normal(0, amount, arr.shape[:2])[..., None]
    arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(arr, "RGB")


rng_np = np.random.default_rng(7)

img = Image.new("RGB", (W, W), (46, 32, 22))
draw = ImageDraw.Draw(img)

# ---- dark walnut table: planks + grain streaks ----
for px in range(0, W, 256):
    tone = rng.choice([(52, 36, 24), (44, 30, 20), (58, 40, 26)])
    draw.rectangle([px, 0, px + 255, W - 1], fill=tone)
    draw.line([(px, 0), (px, W - 1)], fill=(28, 18, 11), width=3)
for _ in range(260):
    x = rng.randint(0, W - 1)
    y = rng.randint(0, W - 1)
    ln = rng.randint(40, 220)
    c = rng.choice([(66, 46, 30), (38, 25, 16), (74, 52, 34)])
    draw.line([(x, y), (x + rng.randint(-6, 6), y + ln)], fill=c, width=1)

# warm light pool, top-left
glow = Image.new("RGBA", (W, W), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.ellipse([-260, -300, 900, 700], fill=(255, 190, 110, 46))
glow = glow.filter(ImageFilter.GaussianBlur(180))
img = Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB")
draw = ImageDraw.Draw(img)

# ---- linen napkin corner, bottom-right ----
nap = Image.new("RGBA", (W, W), (0, 0, 0, 0))
nd = ImageDraw.Draw(nap)
nd.polygon([(1024, 700), (700, 1024), (1024, 1024)], fill=(214, 196, 168, 255))
nd.line([(1024, 700), (700, 1024)], fill=(180, 160, 128, 255), width=4)
for i in range(8):
    nd.line([(1024, 730 + i * 38), (730 + i * 38, 1024)], fill=(196, 178, 150, 255), width=2)
img = Image.alpha_composite(img.convert("RGBA"), nap).convert("RGB")
draw = ImageDraw.Draw(img)

# ---- bowl shadow + bowl ----
CX, CY, R = 512, 500, 372
img = soft_shadow(img, [CX - R - 8, CY - R + 26, CX + R + 8, CY + R + 40], blur=26, alpha=130)
draw = ImageDraw.Draw(img)
# outer bowl: deep teal ceramic
ellipse_gradient(draw, [CX - R, CY - R, CX + R, CY + R], (58, 112, 108), (24, 52, 56))
draw.ellipse([CX - R, CY - R, CX + R, CY + R], outline=(16, 34, 38), width=3)
# rim highlight, top-left arc
draw.arc([CX - R + 6, CY - R + 6, CX + R - 6, CY + R - 6], start=150, end=330,
         fill=(150, 205, 200), width=7)
# inner bowl
IR = R - 34
ellipse_gradient(draw, [CX - IR, CY - IR, CX + IR, CY + IR], (238, 226, 205), (214, 196, 168))
draw.ellipse([CX - IR, CY - IR, CX + IR, CY + IR], outline=(120, 100, 78), width=2)
# inner shadow at bottom of bowl
sh = Image.new("RGBA", (W, W), (0, 0, 0, 0))
sd = ImageDraw.Draw(sh)
sd.ellipse([CX - IR, CY - IR + 60, CX + IR, CY + IR], fill=(90, 70, 45, 70))
sh = sh.filter(ImageFilter.GaussianBlur(30))
img = Image.alpha_composite(img.convert("RGBA"), sh).convert("RGB")
draw = ImageDraw.Draw(img)

# ---- rice bed ----
rice = Image.new("RGBA", (W, W), (0, 0, 0, 0))
rd = ImageDraw.Draw(rice)
for _ in range(6500):
    a = rng.uniform(0, 2 * math.pi)
    rr = math.sqrt(rng.uniform(0, 1)) * (IR - 14)
    x, y = CX + rr * math.cos(a), CY + rr * math.sin(a) * 0.98
    c = rng.choice([(250, 244, 230), (242, 234, 214), (255, 250, 240), (232, 222, 198)])
    rd.ellipse([x - 6.5, y - 3.2, x + 6.5, y + 3.2], fill=c + (255,))
img = Image.alpha_composite(img.convert("RGBA"), rice).convert("RGB")
draw = ImageDraw.Draw(img)


def fish_cube(x, y, s, base, dark, stripe, rot=0):
    """Glossy raw-fish cube with fat stripes and a specular highlight."""
    layer = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle([x - s, y - s * 0.82, x + s, y + s * 0.82],
                        radius=int(s * 0.32), fill=base + (255,),
                        outline=dark + (255,), width=2)
    # fat stripes
    for k, off in enumerate([-0.42, 0.0, 0.42]):
        d.line([(x - s * 0.85, y + s * off), (x + s * 0.85, y + s * off)],
               fill=stripe + (200,), width=max(2, int(s * 0.13)))
    # shading: darker bottom edge
    d.rounded_rectangle([x - s, y + s * 0.45, x + s, y + s * 0.82],
                        radius=int(s * 0.3), fill=dark + (110,))
    # specular gloss
    d.ellipse([x - s * 0.7, y - s * 0.78, x + s * 0.15, y - s * 0.08],
              fill=(255, 255, 255, 170))
    layer = layer.rotate(rot, center=(x, y), resample=Image.BICUBIC)
    img.paste(layer, (0, 0), layer)
    return img


def cube_pile(cx, cy, s, base, dark, stripe, n=5):
    pts = []
    for i in range(n):
        a = rng.uniform(0, 2 * math.pi)
        rr = rng.uniform(0, s * 1.7)
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a) * 0.9))
    pts.sort(key=lambda p: p[1])  # back to front
    for x, y in pts:
        fish_cube(x, y, s * rng.uniform(0.85, 1.05), base, dark, stripe,
                  rot=rng.randint(-28, 28))


def avocado_fan(cx, cy, n=6):
    for i in range(n):
        x = cx - 66 + i * 24
        y = cy + (i - n / 2) ** 2 * 2.2
        layer = Image.new("RGBA", (W, W), (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        d.rounded_rectangle([x - 15, y - 34, x + 15, y + 34], radius=15,
                            fill=lerp((150, 190, 80), (90, 140, 55), i / max(1, n - 1)) + (255,),
                            outline=(52, 92, 32, 255), width=2)
        d.ellipse([x - 9, y - 26, x + 9, y + 6], fill=(210, 235, 150, 160))
        layer = layer.rotate(-18 + i * 3, center=(x, y), resample=Image.BICUBIC)
        img.paste(layer, (0, 0), layer)


def edamame(cx, cy, n=8):
    for i in range(n):
        a = rng.uniform(0, 2 * math.pi)
        rr = rng.uniform(0, 62)
        x, y = cx + rr * math.cos(a), cy + rr * math.sin(a)
        r = rng.uniform(13, 18)
        draw.ellipse([x - r, y - r, x + r, y + r], fill=(96, 150, 62),
                     outline=(60, 100, 38), width=2)
        draw.ellipse([x - r * 0.45, y - r * 0.55, x + r * 0.1, y - r * 0.05],
                     fill=(190, 225, 140))


def mango_cubes(cx, cy, n=7):
    for i in range(n):
        a = rng.uniform(0, 2 * math.pi)
        rr = rng.uniform(0, 58)
        x, y = cx + rr * math.cos(a), cy + rr * math.sin(a)
        s = rng.uniform(15, 20)
        draw.rounded_rectangle([x - s, y - s, x + s, y + s], radius=6,
                               fill=(245, 180, 40), outline=(210, 130, 20), width=2)
        draw.ellipse([x - s * 0.5, y - s * 0.6, x + s * 0.1, y - s * 0.1],
                     fill=(255, 225, 130))


def cucumber(cx, cy, n=5):
    for i in range(n):
        x = cx - 52 + i * 26
        y = cy + rng.uniform(-8, 8)
        draw.ellipse([x - 16, y - 16, x + 16, y + 16], fill=(140, 190, 110),
                     outline=(60, 120, 60), width=3)
        draw.ellipse([x - 10, y - 10, x + 10, y + 10], fill=(205, 230, 170))


def ginger(cx, cy):
    for i in range(6):
        x = cx + rng.uniform(-38, 38)
        y = cy + rng.uniform(-26, 26)
        s = rng.uniform(13, 19)
        draw.ellipse([x - s, y - s * 0.6, x + s, y + s * 0.6],
                     fill=(248, 170, 175), outline=(225, 120, 130), width=2)


def seaweed(cx, cy):
    for i in range(46):
        a = rng.uniform(0, 2 * math.pi)
        rr = rng.uniform(0, 46)
        x, y = cx + rr * math.cos(a), cy + rr * math.sin(a)
        ln = rng.uniform(8, 16)
        ang = rng.uniform(0, 2 * math.pi)
        draw.line([(x, y), (x + ln * math.cos(ang), y + ln * math.sin(ang))],
                  fill=rng.choice([(25, 80, 50), (40, 105, 62), (18, 62, 40)]), width=5)


def tobiko(cx, cy, n=40):
    for i in range(n):
        a = rng.uniform(0, 2 * math.pi)
        rr = rng.uniform(0, 52)
        x, y = cx + rr * math.cos(a), cy + rr * math.sin(a)
        r = rng.uniform(3.5, 5.5)
        draw.ellipse([x - r, y - r, x + r, y + r], fill=(255, 110, 40))
        draw.ellipse([x - r * 0.4, y - r * 0.5, x, y - r * 0.1], fill=(255, 190, 120))


# ---- topping sections (clockwise from top) ----
cube_pile(CX - 130, CY - 140, 38, (255, 125, 80), (205, 80, 40), (255, 205, 180), n=5)   # salmon
cube_pile(CX + 130, CY - 140, 38, (185, 45, 70), (130, 25, 45), (240, 140, 150), n=5)    # tuna
avocado_fan(CX + 185, CY + 20)                                                            # avocado
mango_cubes(CX + 115, CY + 160)                                                          # mango
edamame(CX - 20, CY + 190)                                                               # edamame
cucumber(CX - 185, CY + 40)                                                              # cucumber
ginger(CX - 195, CY - 80)                                                                # pickled ginger
seaweed(CX + 5, CY - 185)                                                                # seaweed salad
tobiko(CX, CY - 10)                                                                      # tobiko centre

# ---- spicy mayo drizzle, zigzag over the two fish piles only ----
mz = Image.new("RGBA", (W, W), (0, 0, 0, 0))
md = ImageDraw.Draw(mz)
for cy0, x0, x1 in [(CY - 140, CX - 195, CX - 65), (CY - 140, CX + 65, CX + 195)]:
    pts = []
    x = x0
    while x < x1:
        pts.append((x, cy0 + rng.uniform(-22, 22)))
        x += 26
    md.line(pts, fill=(255, 235, 205, 235), width=9, joint="curve")
img = Image.alpha_composite(img.convert("RGBA"), mz).convert("RGB")
draw = ImageDraw.Draw(img)

# ---- scallion rings + sesame ----
for _ in range(46):
    a = rng.uniform(0, 2 * math.pi)
    rr = math.sqrt(rng.uniform(0, 1)) * (IR - 30)
    x, y = CX + rr * math.cos(a), CY + rr * math.sin(a)
    r = rng.uniform(5, 8)
    draw.ellipse([x - r, y - r, x + r, y + r], outline=(40, 130, 60), width=3)
    draw.ellipse([x - r + 2, y - r + 2, x + r - 2, y + r - 2], fill=(120, 200, 110))
for _ in range(130):
    a = rng.uniform(0, 2 * math.pi)
    rr = math.sqrt(rng.uniform(0, 1)) * (IR - 20)
    x, y = CX + rr * math.cos(a), CY + rr * math.sin(a)
    c = rng.choice([(245, 235, 210), (40, 30, 20)])
    draw.ellipse([x - 2.5, y - 1.5, x + 2.5, y + 1.5], fill=c)

# ---- lime wedge resting on the table, top-right of the bowl ----
lime = Image.new("RGBA", (W, W), (0, 0, 0, 0))
ld = ImageDraw.Draw(lime)
LX, LY = 845, 215
ld.pieslice([LX - 70, LY - 70, LX + 70, LY + 70], start=200, end=340,
            fill=(140, 200, 70, 255), outline=(60, 120, 40, 255), width=4)
ld.pieslice([LX - 58, LY - 58, LX + 58, LY + 58], start=200, end=340,
            fill=(210, 240, 140, 255))
for ang in range(215, 335, 24):
    a0 = math.radians(ang)
    ld.line([(LX, LY),
             (LX + 52 * math.cos(a0), LY + 52 * math.sin(a0))],
            fill=(250, 255, 210, 255), width=3)
img = Image.alpha_composite(img.convert("RGBA"), lime).convert("RGB")
draw = ImageDraw.Draw(img)

chop = Image.new("RGBA", (W, W), (0, 0, 0, 0))
cd = ImageDraw.Draw(chop)
for off in (0, 16):
    cd.line([(110, 950 + off), (620, 905 + off)], fill=(120, 70, 35, 255), width=11)
    cd.line([(110, 950 + off), (620, 905 + off)], fill=(170, 105, 55, 255), width=5)
chop = chop.rotate(-3, center=(360, 930), resample=Image.BICUBIC)
img = Image.alpha_composite(img.convert("RGBA"), chop).convert("RGB")

# ---- finish: gentle vignette + grain ----
arr = np.asarray(img).astype(np.float32)
yy, xx = np.mgrid[0:W, 0:W]
d2 = ((xx - CX) / 720) ** 2 + ((yy - CY) / 720) ** 2
vig = np.clip(1 - 0.22 * np.clip(d2 - 0.55, 0, None), 0, 1)[..., None]
arr = arr * vig
img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB")
img = grain(img, amount=0)
img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
