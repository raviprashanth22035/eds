"""NFL Events Hub — simple platform architecture (one slide, seven boxes).

Usage: python3 simple.py <output-dir>
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa: F401,F403

OUT = sys.argv[1]
H = 760


def legend_y(y0, items):
    out = [f'<line x1="40" y1="{y0}" x2="1240" y2="{y0}" stroke="rgba(45,49,66,0.10)" stroke-width="0.8"/>',
           f'<text x="40" y="{y0+20}" fill="{MUTED}" font-size="8" font-family="{MONO}" letter-spacing="0.18em">LEGEND</text>']
    x = 40
    for kind, text in items:
        if kind.startswith("arrow:"):
            a, *dash = kind.split(":")[1:]
            color, marker = {"link": (LINK, "arrow-link"), "accent": (ACCENT, "arrow-accent"), "muted": (MUTED, "arrow")}[a]
            da = ' stroke-dasharray="4,3"' if dash else ""
            out.append(f'<line x1="{x}" y1="{y0+40}" x2="{x+28}" y2="{y0+40}" stroke="{color}" stroke-width="1.2"{da} marker-end="url(#{marker})"/>')
            tx = x + 36
        else:
            fill, stroke, *_ = TREAT[kind]
            out.append(f'<rect x="{x}" y="{y0+34}" width="16" height="12" rx="2" fill="{fill}" stroke="{stroke}" stroke-width="1"/>')
            tx = x + 24
        out.append(f'<text x="{tx}" y="{y0+44}" fill="{MUTED}" font-size="10" font-family="{SANS}">{esc(text)}</text>')
        x += 176
    return "\n".join(out)


def vlabel(x, cy, text, kind="muted"):
    w = (int(len(text) * 12 * 0.62 + 0.06 * 12 * len(text)) + 12 + 3) // 4 * 4
    return label(x + 8 + w / 2, cy - 8, text, kind)


d = []
# connectors
d.append(arrow("M 560,168 V 262"))                                                   # authors -> hub
d.append(vlabel(560, 216, "PUBLISH"))
d.append(arrow("M 280,352 H 398"))                                                   # fans -> hub
d.append(label(340, 324, "PAGES"))
d.append(arrow("M 160,424 V 518", "link", dashed=True))                              # fans -> Ticketmaster
d.append(vlabel(160, 472, "BUY TICKETS", "link"))
d.append(arrow("M 560,440 V 518", "accent"))                                         # hub -> worker
d.append(vlabel(560, 480, "SIGNED IN ONLY", "accent"))
d.append(arrow("M 720,552 H 792 Q 800,552 800,544 V 496 Q 800,488 808,488 H 918", "link"))  # -> NFL ID
d.append(label(864, 460, "SIGN-IN", "link"))
d.append(arrow("M 720,632 H 918", "link"))                                           # -> OnePass
d.append(label(820, 604, "REGISTER · QR", "link"))
# nodes
d.append(node(400, 96, 320, 72, "input", "AUTHORS", "Clubs & league", "docs · sheets · Universal Editor"))
d.append(node(40, 280, 240, 144, "input", "FANS", "Fans", "web browser", ["NFL OnePass app", "NFL App"]))
d.append(node(400, 264, 320, 176, "focal", "PORTAL", "NFL Events Hub", "AEM Edge Delivery + CDN",
              ["events · filters · forms", "same page for every fan"]))
d.append(node(40, 520, 240, 72, "external", "PARTNER", "Ticketmaster", "paid events · link-out"))
d.append(node(400, 520, 320, 144, "focal", "EDGE", "Thin edge worker", "sign-in · registration",
              ["stateless · no data stored"]))
d.append(node(920, 456, 320, 64, "external", "NFL", "NFL ID", "one fan account"))
d.append(node(920, 600, 320, 64, "external", "NFL", "OnePass", "registration · QR · check-in"))
d.append(legend_y(692, [("focal", "What we build"), ("external", "NFL / partner system"), ("input", "People"),
                        ("arrow:muted", "Content"), ("arrow:accent", "Signed-in path"), ("arrow:link:dashed", "Link-out")]))

doc = page("nfl-events-hub-simple", "Platform architecture · NFL Events Hub",
           "NFL Events Hub — platform architecture",
           "NFL Events Hub platform architecture",
           "Simple architecture of the NFL Events Hub: clubs and the league publish to one portal on AEM Edge Delivery and CDN that serves "
           "the same pages on the web, NFL OnePass and the NFL App; only signed-in actions go through a thin, stateless edge worker to NFL ID "
           "and OnePass; paid events link out to Ticketmaster.",
           "\n".join(d))
doc = doc.replace('viewBox="0 0 1280 720"', f'viewBox="0 0 1280 {H}"', 1)
caption = ("<ol class=\"points\"><li><b>One portal.</b> Clubs and the league publish; every fan on web, OnePass and the NFL App sees the same fast, cached pages.</li>"
           "<li><b>Thin edge worker.</b> Only sign-in and registration pass through it, to NFL ID and OnePass. It stores nothing.</li>"
           "<li><b>No payments.</b> Paid events link out to Ticketmaster.</li></ol>")
css = """    .points { margin-top: 1.5rem; padding-left: 1.3rem; display: grid; gap: 0.45rem; max-width: 60rem; }
    .points li { font-size: 0.95rem; line-height: 1.55; color: #4f5d75; } .points b { color: #2d3142; }
  </style>"""
doc = doc.replace("  </style>", css, 1).replace("    </div>\n  </div>\n</body>", "    </div>\n    " + caption + "\n  </div>\n</body>", 1)
open(f"{OUT}/nfl-events-hub-simple-architecture.html", "w").write(doc)
print("ok")
