"""Animated wave banners: GIF covers for Notion, SVG header/footer for GitHub README."""
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1500, 300
FR = 30  # frames per loop
C0, C1 = (30, 41, 59), (37, 99, 235)  # #1E293B -> #2563EB
BOLD = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"
MED = "/usr/share/fonts/opentype/inter/Inter-Medium.otf"

COVERS = {
    "main": ("Hwang Yeongho", "Java · Spring Boot Backend Developer"),
    "ridefit": ("RIDEFIT", "Motorcycle parts fit check · 2D try-on"),
    "easys": ("EASYS", "Study · Mentoring · Streaming platform"),
    "study": ("Study Notes", "Full-stack bootcamp · 2026"),
}


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def background():
    g = Image.new("RGB", (W, 1))
    for x in range(W):
        g.putpixel((x, 0), lerp(C0, C1, x / (W - 1)))
    return g.resize((W, H))


# each wave: (base y, amplitude, wavelength-count across width, speed in cycles per loop, alpha)
WAVES = [
    (222, 14, 1, 1, 45),
    (240, 11, 2, -1, 55),
    (262, 8, 1, 2, 70),
]


def wave_layer(phase_t):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for base, amp, k, speed, alpha in WAVES:
        m = Image.new("L", (W, H), 0)
        d = ImageDraw.Draw(m)
        ph = 2 * math.pi * speed * phase_t
        pts = [(x, base + amp * math.sin(2 * math.pi * k * x / W + ph)) for x in range(0, W + 1, 6)]
        d.polygon(pts + [(W, H), (0, H)], fill=alpha)
        white = Image.new("RGBA", (W, H), (255, 255, 255, 0))
        white.putalpha(m)
        layer = Image.alpha_composite(layer, white)
    return layer


def text_layer(title, sub):
    t = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(t)
    f1 = ImageFont.truetype(BOLD, 70)
    f2 = ImageFont.truetype(MED, 26)
    d.text((W / 2, 108), title, font=f1, fill="white", anchor="mm")
    d.text((W / 2, 166), sub, font=f2, fill=(226, 232, 240), anchor="mm")
    return t


def make_gif(name, title, sub):
    bg = background().convert("RGBA")
    txt = text_layer(title, sub)
    frames = []
    for i in range(FR):
        im = Image.alpha_composite(bg, wave_layer(i / FR))
        im = Image.alpha_composite(im, txt).convert("RGB")
        frames.append(im)
    # one shared palette so colours don't flicker between frames
    pal = frames[0].quantize(colors=256, method=Image.Quantize.MEDIANCUT)
    q = [f.quantize(palette=pal, dither=Image.Dither.FLOYDSTEINBERG) for f in frames]
    q[0].save(f"cover-{name}.gif", save_all=True, append_images=q[1:], duration=80, loop=0, optimize=True)


def svg_wave_path(width, base, amp, k, height):
    # path two periods-of-width wide so translating by -width loops seamlessly
    pts = []
    for x in range(0, 2 * width + 1, 10):
        y = base + amp * math.sin(2 * math.pi * k * x / width)
        pts.append(f"{x},{y:.1f}")
    return f"M0,{height} L" + " L".join(pts) + f" L{2*width},{height} Z"


def make_svg_header():
    w, h = 1200, 260
    waves = [(200, 14, 1, 14, 0.18), (215, 11, 2, 10, 0.22), (232, 8, 1, 7, 0.30)]
    parts = []
    for base, amp, k, dur, op in waves:
        p = svg_wave_path(w, base, amp, k, h)
        parts.append(
            f'<path d="{p}" fill="#ffffff" fill-opacity="{op}">'
            f'<animateTransform attributeName="transform" type="translate" from="0 0" to="-{w} 0" dur="{dur}s" repeatCount="indefinite"/></path>'
        )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<defs><linearGradient id="g" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="#1E293B"/><stop offset="1" stop-color="#2563EB"/></linearGradient></defs>
<rect width="{w}" height="{h}" fill="url(#g)"/>
{''.join(parts)}
<g font-family="Inter, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif" text-anchor="middle" fill="#ffffff">
<text x="{w/2}" y="108" font-size="54" font-weight="700">Hwang Yeongho
<animate attributeName="opacity" from="0" to="1" dur="1.2s" fill="freeze"/></text>
<text x="{w/2}" y="152" font-size="20" font-weight="500" fill="#E2E8F0">Java · Spring Boot Backend Developer
<animate attributeName="opacity" values="0;0;1" keyTimes="0;0.4;1" dur="1.8s" fill="freeze"/></text>
</g>
</svg>
'''


def make_svg_footer():
    w, h = 1200, 110
    waves = [(30, 12, 1, 14, 0.35), (45, 9, 2, 10, 0.55), (62, 7, 1, 7, 0.85)]
    parts = []
    for base, amp, k, dur, op in waves:
        p = svg_wave_path(w, base, amp, k, h)
        parts.append(
            f'<path d="{p}" fill="url(#g)" fill-opacity="{op}">'
            f'<animateTransform attributeName="transform" type="translate" from="0 0" to="-{w} 0" dur="{dur}s" repeatCount="indefinite"/></path>'
        )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<defs><linearGradient id="g" x1="0" x2="2400" y1="0" y2="0" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#2563EB"/><stop offset="0.5" stop-color="#1E293B"/><stop offset="1" stop-color="#2563EB"/></linearGradient></defs>
{''.join(parts)}
</svg>
'''


if __name__ == "__main__":
    import sys
    for n, (t, s) in COVERS.items():
        make_gif(n, t, s)
    open("wave-header.svg", "w").write(make_svg_header())
    open("wave-footer.svg", "w").write(make_svg_footer())
    # wide footer GIF for the bottom of Notion pages
    print("ok")
