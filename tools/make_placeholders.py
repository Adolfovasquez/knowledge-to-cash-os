"""Dev-only: generate branded placeholder WebP images in the brand palette.
Replace these by dropping real photos in assets/photos/source/ and running webp_convert.py.
Not shipped to production (tools/ folder is dev-only)."""
import os
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "img")
os.makedirs(OUT, exist_ok=True)

# Brand palette
PEACH = (247, 224, 214)
PINK = (233, 30, 140)
ROSE = (245, 183, 200)
LAV = (189, 178, 255)
INK = (42, 30, 38)

def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

def gradient(w, h, c1, c2, c3):
    img = Image.new("RGB", (w, h))
    px = img.load()
    for y in range(h):
        ty = y / max(h - 1, 1)
        if ty < 0.5:
            row = lerp(c1, c2, ty * 2)
        else:
            row = lerp(c2, c3, (ty - 0.5) * 2)
        for x in range(w):
            tx = x / max(w - 1, 1)
            px[x, y] = lerp(row, lerp(c3, c1, tx), 0.18)
    return img

def monogram(img, label):
    d = ImageDraw.Draw(img, "RGBA")
    w, h = img.size
    # soft vignette
    d.ellipse([w*0.2, h*0.15, w*0.8, h*0.95], fill=(255, 255, 255, 26))
    try:
        f_big = ImageFont.truetype("arialbd.ttf", int(min(w, h) * 0.22))
        f_small = ImageFont.truetype("arial.ttf", int(min(w, h) * 0.045))
    except Exception:
        f_big = ImageFont.load_default()
        f_small = ImageFont.load_default()
    text = "MC"
    tb = d.textbbox((0, 0), text, font=f_big)
    d.text(((w - (tb[2]-tb[0])) / 2, (h - (tb[3]-tb[1])) / 2 - h*0.06),
           text, font=f_big, fill=(255, 255, 255, 235))
    lb = d.textbbox((0, 0), label, font=f_small)
    d.text(((w - (lb[2]-lb[0])) / 2, h*0.62),
           label, font=f_small, fill=(255, 255, 255, 210))
    return img

SPECS = [
    ("retrato.webp",     1400, 1750, (PEACH, ROSE, LAV),  "RETRATO PROFESIONAL"),
    ("consultorio.webp", 2000, 1200, (LAV, ROSE, PEACH),  "CONSULTORIO"),
    ("sonrisa-1.webp",   1200, 1500, (ROSE, PINK, LAV),   "CASO CLÍNICO 01"),
    ("sonrisa-2.webp",   1200, 1500, (PEACH, PINK, ROSE), "CASO CLÍNICO 02"),
    ("sonrisa-3.webp",   1200, 1500, (LAV, PINK, PEACH),  "CASO CLÍNICO 03"),
]

for name, w, h, (c1, c2, c3), label in SPECS:
    img = gradient(w, h, c1, c2, c3)
    img = monogram(img, label)
    q = 80 if "retrato" in name or "consultorio" in name else 78
    img.save(os.path.join(OUT, name), "WEBP", quality=q, method=6)
    print("wrote", name, img.size)

print("done")
