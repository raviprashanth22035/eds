"""NFL Events Hub — high-level system design (request-flow view).

Usage: python3 sysdesign.py <output-dir>
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa: F401,F403

OUT = sys.argv[1]
H = 860


def badge(cx, cy, n):
    """Numbered step marker placed beside (never on) a connector."""
    return (f'<circle cx="{cx}" cy="{cy}" r="11" fill="{PAPER}" stroke="{ACCENT}" stroke-width="1.2"/>'
            f'<text x="{cx}" y="{cy + 4}" fill="{ACCENT}" font-size="11" font-weight="600" '
            f'font-family="{MONO}" text-anchor="middle">{n}</text>')


def legend_y(y0, items):
    out = [f'<line x1="40" y1="{y0}" x2="1240" y2="{y0}" stroke="rgba(45,49,66,0.10)" stroke-width="0.8"/>',
           f'<text x="40" y="{y0+20}" fill="{MUTED}" font-size="8" font-family="{MONO}" letter-spacing="0.18em">LEGEND</text>']
    x = 40
    for kind, text in items:
        if kind == "badge":
            out.append(badge(x + 8, y0 + 40, "1"))
            tx = x + 24
        elif kind.startswith("arrow:"):
            a, *dash = kind.split(":")[1:]
            color, marker = {"link": (LINK, "arrow-link"), "muted": (MUTED, "arrow")}[a]
            da = ' stroke-dasharray="4,3"' if dash else ""
            out.append(f'<line x1="{x}" y1="{y0+40}" x2="{x+28}" y2="{y0+40}" stroke="{color}" stroke-width="1.2"{da} marker-end="url(#{marker})"/>')
            tx = x + 36
        else:
            fill, stroke, *_ = TREAT[kind]
            out.append(f'<rect x="{x}" y="{y0+34}" width="16" height="12" rx="2" fill="{fill}" stroke="{stroke}" stroke-width="1"/>')
            tx = x + 24
        out.append(f'<text x="{tx}" y="{y0+44}" fill="{MUTED}" font-size="10" font-family="{SANS}">{esc(text)}</text>')
        x += 168
    return "\n".join(out)


d = []
# zones
d.append(zone(248, 304, 552, 352, "EDGE · CDN + BFF"))
d.append(zone(560, 128, 504, 136, "ADOBE AEM · CONTENT"))
d.append(zone(824, 536, 416, 216, "NFL ONEPASS PLATFORM"))
# connectors
d.append(arrow("M 128,304 V 234", dashed=True))                                       # clients -> DNS
d.append(arrow("M 208,376 H 262"))                                                    # clients -> CDN
d.append(arrow("M 128,464 V 558", "link", dashed=True))                               # clients -> Ticketmaster
d.append(arrow("M 448,360 H 504 Q 512,360 512,352 V 208 Q 512,200 520,200 H 574"))   # CDN -> EDS (miss)
d.append(arrow("M 864,200 H 786"))                                                    # authoring -> EDS
d.append(arrow("M 448,392 H 504 Q 512,392 512,400 V 528 Q 512,536 520,536 H 574", "link"))  # CDN -> BFF
d.append(arrow("M 784,472 H 838", "link"))                                            # BFF -> NFL ID
d.append(arrow("M 784,600 H 838", "link"))                                            # BFF -> registration API
d.append(arrow("M 1016,600 H 1062"))                                                  # API -> DB
d.append(arrow("M 928,632 V 670"))                                                    # API -> queue
d.append(arrow("M 1016,704 H 1062"))                                                  # queue -> notifications
# step markers (beside their connectors)
d += [badge(148, 268, 1), badge(236, 352, 2), badge(536, 280, 3), badge(824, 176, 4),
      badge(536, 464, 5), badge(812, 448, 6), badge(812, 576, 7), badge(1040, 576, 8),
      badge(952, 652, 9), badge(148, 512, 10)]
# nodes
d.append(node(40, 168, 168, 64, "external", "DNS", "DNS", "event.nfl.com"))
d.append(node(40, 304, 168, 160, "input", "CLIENTS", "Fans", "web browser",
              ["NFL OnePass app", "NFL App (WebView)"]))
d.append(node(40, 560, 168, 64, "external", "PARTNER", "Ticketmaster", "paid · exit link"))
d.append(node(264, 336, 184, 80, "external", "CDN", "Edge CDN", "cache · WAF · queue"))
d.append(node(576, 160, 208, 80, "focal", "ORIGIN", "NFL Events Hub", "AEM Edge Delivery"))
d.append(node(864, 168, 184, 64, "input", "AUTHOR", "AEM authoring", "clubs · league"))
d.append(node(576, 440, 208, 192, "focal", "BFF", "Edge BFF", "stateless",
              ["/auth/* · OIDC", "/api/* · proxy", "no data at rest"]))
d.append(node(840, 440, 184, 64, "external", "IDP", "NFL ID", "id.nfl.com"))
d.append(node(840, 568, 176, 64, "external", "API", "Registration API", "QR · wallet pass"))
d.append(node(1064, 568, 160, 64, "store", "DB", "Registrations", "capacity · status"))
d.append(node(840, 672, 176, 64, "store", "QUEUE", "Event queue", "confirm · cancel"))
d.append(node(1064, 672, 160, 64, "external", "WORKER", "Notifications", "email · push"))
d.append(legend_y(784, [("badge", "Step (see below)"), ("focal", "Hub origin & BFF"), ("external", "Service / partner"),
                        ("store", "Data store / queue"), ("input", "Users / authoring"), ("arrow:link", "Dynamic path"),
                        ("arrow:muted", "Static path")]))

doc = page("nfl-events-hub-system-design", "High-level system design · NFL Events Hub",
           "NFL Events Hub — high-level system design",
           "NFL Events Hub high-level system design",
           "Request flow for the NFL Events Hub: fans on web, OnePass and the NFL App resolve event.nfl.com, every request hits the edge CDN, "
           "pages and event JSON come from the AEM Edge Delivery origin, and only sign-in and registration calls go through a stateless Edge BFF "
           "to NFL ID and the OnePass registration API, which stores registrations and queues notifications.",
           "\n".join(d))
doc = doc.replace('viewBox="0 0 1280 720"', f'viewBox="0 112 1280 {H - 112}"', 1).replace('<rect width="100%" height="100%"', '<rect y="112" width="100%" height="100%"', 1)

STEPS = [
    ("Static path", "Every fan, one portal", [
        "<b>Resolve.</b> Web, NFL OnePass and the NFL App open <code>event.nfl.com</code> (apps in a WebView).",
        "<b>Edge.</b> Every request lands on the CDN: cache, WAF, bot rules, and a waiting room for peak registration openings.",
        "<b>Origin on miss.</b> Pages, <code>events.json</code> (all events, filters, search) and status come from AEM Edge Delivery. Most traffic stops at the cache.",
        "<b>Publish.</b> Clubs and the league author in AEM; publishing purges the CDN in seconds (cancellations included)."]),
    ("Dynamic path", "Only signed-in actions", [
        "<b>Route.</b> The CDN sends only <code>/auth/*</code> and <code>/api/*</code> to the Edge BFF; everything else stays static.",
        "<b>Sign in.</b> The BFF runs OIDC with NFL ID (OnePass hands its session to the WebView) and sets an HttpOnly cookie.",
        "<b>Register.</b> The BFF forwards register / my events to the OnePass registration API with the fan’s identity.",
        "<b>Store.</b> The API enforces capacity and one-per-fan, stores the registration, issues the QR and wallet pass.",
        "<b>Notify.</b> Confirmations and cancellations go on a queue; the notifications worker sends email and push."]),
    ("Exit", "Paid events", [
        "<b>Buy.</b> Paid events link out to Ticketmaster (VIP via On Location); no payments in the hub."]),
]
n = 0
cards = []
for eyebrow, title, items in STEPS:
    lis = []
    for it in items:
        n += 1
        lis.append(f'<li><span class="num">{n}</span><span>{it}</span></li>')
    cards.append(f'<div class="card"><p class="card-eyebrow">{eyebrow}</p><h2>{title}</h2><ol>{"".join(lis)}</ol></div>')
css = """    .cards { display: grid; grid-template-columns: 1fr 1.15fr 0.75fr; gap: 12px; margin-top: 1.75rem; }
    .card { background: #fff; border: 1px solid rgba(45,49,66,0.12); border-radius: 6px; padding: 1rem 1.1rem; }
    .card-eyebrow { font-family: var(--font-mono); font-size: 0.66rem; letter-spacing: 0.16em; text-transform: uppercase; color: #bf4520; margin-bottom: 0.35rem; }
    .card h2 { font-size: 1rem; font-weight: 600; margin-bottom: 0.6rem; }
    .card ol { list-style: none; display: grid; gap: 0.5rem; }
    .card li { display: flex; gap: 0.6rem; font-size: 0.86rem; line-height: 1.5; color: #4f5d75; }
    .card li b { color: #2d3142; }
    .num { flex: none; width: 22px; height: 22px; border-radius: 50%; border: 1.2px solid #bf4520; color: #bf4520;
           font-family: var(--font-mono); font-size: 0.7rem; font-weight: 600; display: grid; place-items: center; margin-top: 1px; }
    code { font-family: var(--font-mono); font-size: 0.8rem; }
    @media (max-width: 720px) { .cards { grid-template-columns: 1fr; } }
  </style>"""
doc = doc.replace("  </style>", css, 1)
doc = doc.replace("    </div>\n  </div>\n</body>",
                  "    </div>\n    <div class=\"cards\">\n" + "\n".join(cards) + "\n    </div>\n  </div>\n</body>", 1)
open(f"{OUT}/nfl-events-hub-system-design.html", "w").write(doc)
print("ok")
