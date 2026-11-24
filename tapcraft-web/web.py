import os, io, shutil, cairosvg, gen
from gen import text_paths, arc, shape
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.transformPen import TransformPen
from PIL import Image

OUT = "web"; os.makedirs(OUT + "/svg", exist_ok=True); os.makedirs(OUT + "/png", exist_ok=True); os.makedirs(OUT + "/favicon", exist_ok=True)
GRAD = ('<linearGradient id="drop" x1="0.15" y1="0.05" x2="0.85" y2="1"><stop offset="0" stop-color="#7DD3FC"/>'
        '<stop offset="0.45" stop-color="#38BDF8"/><stop offset="1" stop-color="#2563EB"/></linearGradient>')
DROP = "M175 82 C166 98 138 124 138 158 A37 37 0 0 0 212 158 C212 124 184 98 175 82 Z"
HL = "M168 118 C152 132 143 152 147 170 C149 177 154 175 154 168 C154 152 160 138 172 123 C171 120 169 119 168 118 Z"


def mark(wave, mode="color", mono="#FFFFFF"):
    """znak w układzie współrzędnych 350 (środek 175); przezroczystość fal prawdziwa (tło dowolne)"""
    o = []
    for r, a in ((54, 1.0), (73, 0.62), (92, 0.34)):
        for (a0, a1) in ((180 + 33, 180 - 33), (-33, 33)):
            o.append('<path d="%s" fill="none" stroke="%s" stroke-width="8.6" stroke-linecap="round"%s/>'
                     % (arc(175, 150, r, a0, a1), wave if mode == "color" else mono, ' stroke-opacity="%s"' % a if a < 1 else ""))
    if mode == "color":
        o.append('<path d="%s" fill="url(#drop)"/><path d="%s" fill="#BAE6FD"/>' % (DROP, HL))
        o.append('<ellipse cx="161" cy="182" rx="3.2" ry="5" transform="rotate(-16 161 182)" fill="#DFF3FE"/>')
    else:
        o.append('<path d="%s" fill="%s"/>' % (DROP, mono))
    return "".join(o)

MARK_BOX = (70, 74, 210, 138)   # x y w h


def word(size, tap, craft, x_center=0, baseline=0, mono=None):
    parts, w = text_paths("TapCraft", size, x_center, baseline, tracking=-0.006 * size, split=[(3, mono or tap), (5, mono or craft)])
    return "".join('<path d="%s" fill="%s"/>' % (d, c) for d, c in parts), w


def wbounds(size, x_center, baseline):
    glyphs, width = shape("TapCraft", size, -0.006 * size)
    k = size / gen._upm
    first = gen._tt["hmtx"][glyphs[0][0]][1] * k
    lastg = glyphs[-1][0]
    rsb = (gen._tt["hmtx"][lastg][0] - gen._tt["glyf"][lastg].xMax) * k
    ink = width - first - rsb
    x0 = x_center - ink / 2 - first
    xs, ys = [], []
    for g, gx, adv in glyphs:
        bp = BoundsPen(gen._gs); gen._gs[g].draw(TransformPen(bp, (k, 0, 0, -k, x0 + gx, baseline)))
        if bp.bounds: xs += [bp.bounds[0], bp.bounds[2]]; ys += [bp.bounds[1], bp.bounds[3]]
    return min(xs), min(ys), max(xs), max(ys)


def svg(w, h, body, vb=None):
    vb = vb or "0 0 %s %s" % (w, h)
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="%s" width="%s" height="%s"><defs>%s</defs>%s</svg>' % (vb, w, h, GRAD, body))

BG = {"ciemnym": dict(tap="#FFFFFF", craft="#38BDF8", wave="#38BDF8", mono="#FFFFFF"),
      "jasnym": dict(tap="#0F172A", craft="#2563EB", wave="#2563EB", mono="#0F172A")}

files = {}
mx, my, mw, mh = MARK_BOX
for bg, c in BG.items():
    # znak
    files[f"tapcraft-znak-na-{bg}"] = (svg(mw, mh, mark(c["wave"]), f"{mx} {my} {mw} {mh}"), 1000)
    # sama nazwa
    x0, y0, x1, y1 = wbounds(100, 0, 0); pad = 6
    b, _ = word(100, c["tap"], c["craft"])
    files[f"tapcraft-nazwa-na-{bg}"] = (svg(x1 - x0 + 2 * pad, y1 - y0 + 2 * pad, b, f"{x0 - pad} {y0 - pad} {x1 - x0 + 2 * pad} {y1 - y0 + 2 * pad}"), 1600)
    # poziome: znak po lewej, nazwa po prawej (środek optyczny kropli ~ y 140)
    size = 72; gap = 34
    tx0, ty0, tx1, ty1 = wbounds(size, 0, 0)
    capmid = (ty0 + 0) / 2 if False else -0.35 * size   # środek wysokości wersalików
    cy = 143
    base = cy - capmid
    tx = mx + mw + gap - tx0
    b, _ = word(size, c["tap"], c["craft"], x_center=tx, baseline=base)
    tt, tb = base + ty0, base + ty1
    top = min(my, tt) - 4; bot = max(my + mh, tb) + 4
    left = mx - 4; right = tx + tx1 + 4
    body = mark(c["wave"]) + b
    files[f"tapcraft-logo-poziome-na-{bg}"] = (svg(right - left, bot - top, body, f"{left} {top} {right - left} {bot - top}"), 2000)
    # pionowe: znak nad nazwą
    size = 58; gapv = 26
    x0, y0, x1, y1 = wbounds(size, 175, 0)
    base = my + mh + gapv - y0
    b, _ = word(size, c["tap"], c["craft"], x_center=175, baseline=base)
    top = my - 4; bot = base + y1 + 4
    left = min(mx, x0) - 4; right = max(mx + mw, x1) + 4
    files[f"tapcraft-logo-pionowe-na-{bg}"] = (svg(right - left, bot - top, mark(c["wave"]) + b, f"{left} {top} {right - left} {bot - top}"), 1400)

# jednokolorowe
for name, col in (("biale", "#FFFFFF"), ("granatowe", "#0F172A")):
    files[f"tapcraft-znak-jednokolorowe-{name}"] = (svg(mw, mh, mark("", "mono", col), f"{mx} {my} {mw} {mh}"), 1000)

# odznaki
for th in ("ciemna", "jasna"):
    for band, nm in ((True, "z-SCAN-ME"), (False, "bez-napisu")):
        s, _, _ = gen.build(th, "none", size_mm=35, badge=True, band=band)
        s = s.replace('width="35mm" height="35mm"', 'width="350" height="350"')
        files[f"tapcraft-odznaka-{th}-{nm}"] = (s, 1200)

for n, (s, wpx) in files.items():
    open(f"{OUT}/svg/{n}.svg", "w").write(s)
    cairosvg.svg2png(bytestring=s.encode(), write_to=f"{OUT}/png/{n}.png", output_width=wpx)

# ---- favicony / ikony aplikacji (znak na granacie, bez napisu) ----
def icon_svg(size_units=350, rounded=False, pad_scale=1.0):
    # znak wyśrodkowany na granatowym tle, z zapasem (maskable safe zone)
    sc = 1.28 * pad_scale
    cx = mx + mw / 2; cy = my + mh / 2
    rect = '<rect width="350" height="350" fill="#0F172A"%s/>' % (' rx="70"' if rounded else "")
    g = '<g transform="translate(175 175) scale(%s) translate(%s %s)">%s</g>' % (sc, -cx, -cy, mark("#38BDF8"))
    return svg(350, 350, rect + g)

for fn, sv, px in (("apple-touch-icon-180.png", icon_svg(), 180), ("icon-192.png", icon_svg(pad_scale=0.85), 192),
                   ("icon-512.png", icon_svg(pad_scale=0.85), 512), ("avatar-1024.png", icon_svg(), 1024),
                   ("favicon-32.png", icon_svg(rounded=True), 32), ("favicon-16.png", icon_svg(rounded=True), 16)):
    cairosvg.svg2png(bytestring=sv.encode(), write_to=f"{OUT}/favicon/{fn}", output_width=px)
open(f"{OUT}/favicon/favicon.svg", "w").write(icon_svg(rounded=True))
ims = [Image.open(f"{OUT}/favicon/{n}").convert("RGBA") for n in ("favicon-16.png",)]
big = Image.open(f"{OUT}/favicon/icon-512.png").convert("RGBA")
cairosvg.svg2png(bytestring=icon_svg(rounded=True).encode(), write_to="/tmp/f48.png", output_width=48)
Image.open("/tmp/f48.png").convert("RGBA").save(f"{OUT}/favicon/favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])

# ---- OG image 1200x630 ----
s = files["tapcraft-logo-poziome-na-ciemnym"][0]
import re
vb = re.search(r'viewBox="([^"]+)"', s).group(1).split(); lw, lh = float(vb[2]), float(vb[3])
sc = 760 / lw
inner = s[s.index("</defs>") + 7:-6]
og = ('<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630"><defs>%s</defs>'
      '<rect width="1200" height="630" fill="#0F172A"/><g transform="translate(%s %s) scale(%s) translate(%s %s)">%s</g></svg>'
      % (GRAD, (1200 - 760) / 2, (630 - lh * sc) / 2, sc, -float(vb[0]), -float(vb[1]), inner))
cairosvg.svg2png(bytestring=og.encode(), write_to=f"{OUT}/png/tapcraft-og-image-1200x630.png")

open(f"{OUT}/favicon/WKLEJ-DO-HEAD.html", "w").write(
'''<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon-180.png">
<link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" content="#0F172A">
<meta property="og:image" content="https://TWOJA-DOMENA/tapcraft-og-image-1200x630.png">
''')
open(f"{OUT}/favicon/site.webmanifest", "w").write('''{
  "name": "TapCraft", "short_name": "TapCraft", "theme_color": "#0F172A", "background_color": "#0F172A", "display": "standalone",
  "icons": [{"src": "/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any maskable"},
            {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"}]
}
''')
print(len(files), "plików logo")
