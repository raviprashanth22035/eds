"""Generate the two NFL Events Hub diagrams in the diagram-design default skin."""
import sys, html


PAPER, INK, MUTED, SOFT, ACCENT, LINK = "#f5f5f5", "#2d3142", "#4f5d75", "#5a6580", "#bf4520", "#2e5aa8"
SANS, MONO = "'Geist', system-ui, sans-serif", "'Geist Mono', ui-monospace, monospace"

TREAT = {
    "focal":    ("rgba(191,69,32,0.08)", ACCENT, "rgba(191,69,32,0.50)", ACCENT),
    "backend":  ("#ffffff", INK, "rgba(45,49,66,0.40)", INK),
    "store":    ("rgba(45,49,66,0.05)", MUTED, "rgba(79,93,117,0.50)", MUTED),
    "external": ("rgba(45,49,66,0.03)", "rgba(45,49,66,0.30)", "rgba(45,49,66,0.22)", SOFT),
    "input":    ("rgba(79,93,117,0.10)", SOFT, "rgba(90,101,128,0.40)", SOFT),
}


def esc(s):
    return html.escape(s, quote=True)


def node(x, y, w, h, kind, tag, name, sub, extra=()):
    fill, stroke, tagstroke, tagtext = TREAT[kind]
    tw = max(28, ((len(tag) * 6 + 12) + 3) // 4 * 4)
    cx = x + w / 2
    name_y = y + 40 if h <= 72 else y + 48
    out = [
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{PAPER}"/>',
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="1"/>',
        f'<rect x="{x+8}" y="{y+8}" width="{tw}" height="12" rx="2" fill="transparent" stroke="{tagstroke}" stroke-width="0.8"/>',
        f'<text x="{x+8+tw/2:g}" y="{y+17}" fill="{tagtext}" font-size="8" font-family="{MONO}" text-anchor="middle" letter-spacing="0.08em">{esc(tag)}</text>',
        f'<text x="{cx:g}" y="{name_y}" fill="{INK}" font-size="16" font-weight="600" font-family="{SANS}" text-anchor="middle">{esc(name)}</text>',
        f'<text x="{cx:g}" y="{name_y+20}" fill="{MUTED}" font-size="12" font-family="{MONO}" text-anchor="middle">{esc(sub)}</text>',
    ]
    for i, line in enumerate(extra):
        out.append(f'<text x="{cx:g}" y="{name_y+52+i*20}" fill="{MUTED}" font-size="12" font-family="{MONO}" text-anchor="middle">{esc(line)}</text>')
    return "\n".join(out)


def zone(x, y, w, h, label):
    lw = (int(len(label) * 8 * 0.76) + 16 + 3) // 4 * 4
    return "\n".join([
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="rgba(45,49,66,0.02)" stroke="rgba(45,49,66,0.10)" stroke-width="0.8"/>',
        f'<rect x="{x + w/2 - lw/2:g}" y="{y+4}" width="{lw}" height="12" rx="2" fill="{PAPER}"/>',
        f'<text x="{x + w/2:g}" y="{y+13}" fill="{SOFT}" font-size="8" font-family="{MONO}" text-anchor="middle" letter-spacing="0.14em">{esc(label)}</text>',
    ])


def arrow(d, kind="muted", dashed=False):
    color, marker, sw = {"muted": (MUTED, "arrow", 1.2), "accent": (ACCENT, "arrow-accent", 1.4), "link": (LINK, "arrow-link", 1.2)}[kind]
    dash = ' stroke-dasharray="4,3"' if dashed else ""
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}"{dash} marker-end="url(#{marker})"/>'


def label(cx, y_top, text, kind="muted"):
    """Mask + text; y_top is the mask's top edge (mask height 16)."""
    color = {"muted": SOFT, "accent": ACCENT, "link": LINK}[kind]
    w = (int(len(text) * 12 * 0.62 + 0.06 * 12 * len(text)) + 12 + 3) // 4 * 4
    return "\n".join([
        f'<rect x="{cx - w/2:g}" y="{y_top}" width="{w}" height="16" rx="2" fill="{PAPER}"/>',
        f'<text x="{cx:g}" y="{y_top+12}" fill="{color}" font-size="12" font-family="{MONO}" text-anchor="middle" letter-spacing="0.06em">{esc(text)}</text>',
    ])


def legend(items):
    out = [f'<line x1="40" y1="652" x2="1240" y2="652" stroke="rgba(45,49,66,0.10)" stroke-width="0.8"/>',
           f'<text x="40" y="672" fill="{MUTED}" font-size="8" font-family="{MONO}" letter-spacing="0.18em">LEGEND</text>']
    x = 40
    for kind, text in items:
        if kind.startswith("arrow:"):
            a = kind.split(":")[1]
            color, marker = {"link": (LINK, "arrow-link"), "accent": (ACCENT, "arrow-accent"), "muted": (MUTED, "arrow")}[a]
            out.append(f'<line x1="{x}" y1="692" x2="{x+28}" y2="692" stroke="{color}" stroke-width="1.2" marker-end="url(#{marker})"/>')
            tx = x + 36
        else:
            fill, stroke, *_ = TREAT[kind]
            out.append(f'<rect x="{x}" y="686" width="16" height="12" rx="2" fill="{fill}" stroke="{stroke}" stroke-width="1"/>')
            tx = x + 24
        out.append(f'<text x="{tx}" y="696" fill="{MUTED}" font-size="10" font-family="{SANS}">{esc(text)}</text>')
        x += 176
    return "\n".join(out)


DEFS = f"""<defs>
<marker id="arrow" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="{MUTED}"/></marker>
<marker id="arrow-accent" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="{ACCENT}"/></marker>
<marker id="arrow-link" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="{LINK}"/></marker>
</defs>
<rect width="100%" height="100%" fill="{PAPER}"/>"""


def page(slug, eyebrow, h1, title, desc, body):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(title)}</title>
  <link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Geist:wght@400;500;600&family=Geist+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    :root {{
      --color-paper: {PAPER}; --color-ink: {INK}; --color-muted: {MUTED};
      --font-sans: 'Geist', system-ui, sans-serif;
      --font-serif: 'Instrument Serif', serif;
      --font-mono: 'Geist Mono', ui-monospace, monospace;
    }}
    body {{ font-family: var(--font-sans); background: var(--color-paper); color: var(--color-ink);
           min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 3rem 2rem; }}
    .frame {{ max-width: 1280px; width: 100%; min-width: 0; }}
    .eyebrow {{ font-family: var(--font-mono); font-size: 0.66rem; font-weight: 500; letter-spacing: 0.18em;
               text-transform: uppercase; color: var(--color-muted); margin-bottom: 0.5rem; }}
    h1 {{ font-family: var(--font-serif); font-size: clamp(1.5rem, 2.4vw + 0.75rem, 2.5rem); font-weight: 400;
         letter-spacing: -0.02em; line-height: 1.15; color: var(--color-ink); margin-bottom: 1.5rem; }}
    .diagram-container {{ width: 100%; overflow-x: auto; }}
    svg {{ width: 100%; min-width: 1280px; display: block; }}
    @media print {{ .diagram-container {{ overflow-x: visible; }} svg {{ min-width: 0; }} }}
  </style>
</head>
<body>
  <div class="frame">
    <p class="eyebrow">{esc(eyebrow)}</p>
    <h1>{esc(h1)}</h1>
    <div class="diagram-container">
    <svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="{slug}-title {slug}-desc">
<title id="{slug}-title">{esc(title)}</title>
<desc id="{slug}-desc">{esc(desc)}</desc>
{DEFS}
{body}
    </svg>
    </div>
  </div>
</body>
</html>
"""


