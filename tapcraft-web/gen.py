import math, uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

FONT = "/home/claude/Poppins-Bold.ttf"
_tt = TTFont(FONT)
_gs = _tt.getGlyphSet()
_order = _tt.getGlyphOrder()
_upm = _tt["head"].unitsPerEm
_blob = hb.Blob.from_file_path(FONT)
_hbfont = hb.Font(hb.Face(_blob))


def shape(text, size, tracking=0.0):
    """zwraca [(glyphname, x, advance)] w jednostkach rysunku, szerokość"""
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(_hbfont, buf, {"kern": True})
    k = size / _upm
    x = 0.0
    out = []
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        out.append((_order[info.codepoint], x, pos.x_advance * k))
        x += pos.x_advance * k + tracking
    width = x - tracking
    return out, width


def text_paths(text, size, cx, baseline, tracking=0.0, split=None):
    """tekst jako krzywe, wyśrodkowany optycznie po geometrii liter.
    split: lista (liczba_znaków, kolor) -> zwraca kilka <path>"""
    glyphs, width = shape(text, size, tracking)
    k = size / _upm
    # korekta: wyśrodkuj po faktycznym obrysie (bez bocznych marginesów 1. i ostatniej litery)
    first = _tt["hmtx"][glyphs[0][0]][1] * k
    lastg = glyphs[-1][0]
    last_rsb = (_tt["hmtx"][lastg][0] - _tt["glyf"][lastg].xMax) * k
    ink_w = width - first - last_rsb
    x0 = cx - ink_w / 2 - first
    parts = []
    for i, (g, gx, adv) in enumerate(glyphs):
        pen = SVGPathPen(_gs, ntos=lambda v: ("%.3f" % v).rstrip("0").rstrip("."))
        tp = TransformPen(pen, (k, 0, 0, -k, x0 + gx, baseline))
        _gs[g].draw(tp)
        parts.append(pen.getCommands())
    out = []
    idx = 0
    if split is None:
        split = [(len(text), None)]
    for n, col in split:
        out.append(("".join(parts[idx:idx + n]), col))
        idx += n
    return out, ink_w


def blend(fg, bg, a):
    f = [int(fg[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(bg[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02X%02X%02X" % tuple(round(f[j] * a + b[j] * (1 - a)) for j in range(3))


def arc(cx, cy, r, a0, a1):
    p0 = (cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0)))
    p1 = (cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1)))
    sweep = 1 if a1 > a0 else 0
    large = 1 if abs(a1 - a0) > 180 else 0
    return "M%.2f %.2f A%.2f %.2f 0 %d %d %.2f %.2f" % (p0[0], p0[1], r, r, large, sweep, p1[0], p1[1])


# ---------- parametry geometrii (jednostki 0.1 mm, płótno 35 x 35 mm = 350) ----------
C = 175.0
CUT_R = 150.0          # linia cięcia Ø30
HOLE_Y = 30.0          # środek otworu: 3 mm od krawędzi breloka (do pomiaru!)
HOLE_R = 30.0          # kółko pomocnicze Ø6
RING_R = 136.0


THEMES = {
    "ciemna": dict(bg="#0F172A", ring="#38BDF8", tap="#FFFFFF", craft="#38BDF8",
                   wave="#38BDF8", band0="#7DD3FC", band1="#38BDF8", band_text="#0F172A",
                   band_edge="#BAE6FD", guide="#FFFFFF", wave_bg="#0F172A"),
    "jasna": dict(bg="#F1F5F9", ring="#0F172A", tap="#0F172A", craft="#2563EB",
                  wave="#2563EB", band0="#1E293B", band1="#0F172A", band_text="#FFFFFF",
                  band_edge="#38BDF8", guide="#0F172A", wave_bg="#F1F5F9"),
}


def build(theme="ciemna", guides="full", size_mm=35, badge=False, band=True):
    t = THEMES[theme]
    S = []
    S.append('<svg xmlns="http://www.w3.org/2000/svg" width="%dmm" height="%dmm" viewBox="0 0 350 350">' % (size_mm, size_mm))
    S.append("<defs>")
    S.append('<linearGradient id="drop" x1="0.15" y1="0.05" x2="0.85" y2="1">'
             '<stop offset="0" stop-color="#7DD3FC"/><stop offset="0.45" stop-color="#38BDF8"/>'
             '<stop offset="1" stop-color="#2563EB"/></linearGradient>')
    S.append('<linearGradient id="dropShade" x1="0" y1="0" x2="1" y2="1">'
             '<stop offset="0.55" stop-color="#2563EB"/><stop offset="1" stop-color="#1E40AF"/></linearGradient>')
    S.append('<linearGradient id="band" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>' % (t["band0"], t["band1"]))
    S.append("</defs>")
    # tło do spadu
    if badge:
        S.append('<clipPath id="cp"><circle cx="175" cy="175" r="175"/></clipPath><g clip-path="url(#cp)">')
        S.append('<circle cx="175" cy="175" r="175" fill="%s"/>' % t["bg"])
    else:
        S.append('<rect width="350" height="350" fill="%s"/>' % t["bg"])

    # --- pierścień z przerwą na otwór (symetryczna) ---
    gap = 14.5
    if badge:
        S.append('<circle cx="175" cy="175" r="158" fill="none" stroke="%s" stroke-width="4"/>' % t["ring"])
        if not band:
            S.append('<g transform="translate(0,13)">')
    else:
      S.append('<path d="%s" fill="none" stroke="%s" stroke-width="3.6" stroke-linecap="round"/>'
               % (arc(C, C, RING_R, -90 + gap, 270 - gap), t["ring"]))

    # --- fale NFC (3 pary, współśrodkowe z kroplą), przezroczystość policzona na pełne kolory ---
    wcx, wcy = C, 150.0
    span = 33
    for r, a in ((54, 1.0), (73, 0.62), (92, 0.34)):
        col = blend(t["wave"], t["wave_bg"], a)
        for (a0, a1) in ((180 + span, 180 - span), (-span, span)):
            S.append('<path d="%s" fill="none" stroke="%s" stroke-width="8.6" stroke-linecap="round"/>'
                     % (arc(wcx, wcy, r, a0, a1), col))

    # --- kropla żywicy ---
    tip = (C, 82.0)
    drop = ("M175 82 C166 98 138 124 138 158 A37 37 0 0 0 212 158 C212 124 184 98 175 82 Z")
    S.append('<path d="%s" fill="url(#drop)"/>' % drop)
    # połysk
    S.append('<path d="M168 118 C152 132 143 152 147 170 C149 177 154 175 154 168 C154 152 160 138 172 123 C171 120 169 119 168 118 Z" fill="#BAE6FD"/>')
    S.append('<ellipse cx="161" cy="182" rx="3.2" ry="5" transform="rotate(-16 161 182)" fill="#DFF3FE"/>')

    # --- TapCraft ---
    parts, w = text_paths("TapCraft", 33, C, 242, tracking=-0.2, split=[(3, t["tap"]), (5, t["craft"])])
    for d, col in parts:
        S.append('<path d="%s" fill="%s"/>' % (d, col))

    if badge and not band:
        S.append('</g>')
    # --- pas SCAN ME ---
    BY = 262.0; w2 = 0
    if band:
      pass
    if band:
      S.append('<rect x="0" y="%.1f" width="350" height="%.1f" fill="url(#band)"/>' % (BY, 350 - BY))
      S.append('<rect x="0" y="%.1f" width="350" height="1.6" fill="%s"/>' % (BY, t["band_edge"]))
      parts, w2 = text_paths("SCAN ME", 31, C, 296, tracking=5.2, split=[(7, t["band_text"])])
      for d, col in parts:
          S.append('<path d="%s" fill="%s"/>' % (d, col))

    # --- linie pomocnicze ---
    if guides in ("full", "cut"):
        S.append('<circle cx="%d" cy="%d" r="%d" fill="none" stroke="%s" stroke-width="1.6" stroke-dasharray="6 5"/>'
                 % (C, C, CUT_R, t["guide"]))
    if guides in ("full", "hole"):
        S.append('<circle cx="%d" cy="%d" r="%d" fill="none" stroke="%s" stroke-width="1.6" stroke-dasharray="4 3.5"/>'
                 % (C, HOLE_Y, HOLE_R, t["guide"]))
    if badge:
        S.append("</g>")
    S.append("</svg>")
    return "\n".join(S), w, w2


if __name__ == "__main__":
    import sys
    for th in THEMES:
        svg, w, w2 = build(th, "full")
        open("/home/claude/tc/%s.svg" % th, "w").write(svg)
        print(th, "TapCraft szer. %.1f  SCAN ME szer. %.1f (0.1mm)" % (w, w2))
