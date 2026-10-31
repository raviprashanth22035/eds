"""NFL Events Hub — layered platform architecture (authoring / edge / services).

Usage: python3 layered.py <output-dir>
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa: F401,F403

OUT = sys.argv[1]
H = 1064


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
        x += 150
    return "\n".join(out)


def vlabel(x, cy, text, kind="muted"):
    """Label beside a vertical connector at x (mask starts 8px to the right)."""
    w = (int(len(text) * 12 * 0.62 + 0.06 * 12 * len(text)) + 12 + 3) // 4 * 4
    return label(x + 8 + w / 2, cy - 8, text, kind)


def zone_l(x, y, w, h, text):
    """Zone with a left-aligned label so centre connectors never cross it."""
    lw = (int(len(text) * 8 * 0.76) + 16 + 3) // 4 * 4
    return "\n".join([
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="rgba(45,49,66,0.02)" stroke="rgba(45,49,66,0.10)" stroke-width="0.8"/>',
        f'<rect x="{x + 16}" y="{y + 4}" width="{lw}" height="12" rx="2" fill="{PAPER}"/>',
        f'<text x="{x + 16 + lw / 2:g}" y="{y + 13}" fill="{SOFT}" font-size="8" font-family="{MONO}" text-anchor="middle" letter-spacing="0.14em">{esc(text)}</text>',
    ])


d = []
# layers (zones)
d.append(zone_l(40, 40, 1200, 272, "1 · CONTENT & CODE AUTHORING · ADOBE AEM"))
d.append(zone_l(40, 344, 1200, 360, "2 · EDGE LAYER & SECURITY"))
d.append(zone_l(40, 736, 1200, 232, "3 · SERVICES & INTEGRATIONS · NFL"))
# connectors
for x, t in ((240, "PUBLISH"), (640, "PUBLISH"), (1040, "CODE SYNC")):
    d.append(arrow(f"M {x},160 V 206"))
    d.append(vlabel(x, 184, t))
d.append(arrow("M 640,280 V 382"))                                   # storage -> CDN
d.append(vlabel(640, 332, "ORIGIN · PURGE"))
d.append(arrow("M 312,432 H 518"))                                   # fans -> CDN
d.append(label(416, 404, "HTTPS"))
d.append(arrow("M 192,472 V 558", "link", dashed=True))              # fans -> Ticketmaster
d.append(vlabel(192, 516, "BUY TICKETS", "link"))
d.append(arrow("M 760,432 H 878"))                                   # CDN -> cached pages
d.append(label(820, 404, "PUBLIC"))
d.append(arrow("M 640,496 V 542", "accent"))                         # CDN -> worker
d.append(vlabel(640, 520, "SIGNED IN", "accent"))
d.append(arrow("M 640,656 V 774", "accent"))                         # worker -> NFL APIs
d.append(vlabel(640, 716, "/AUTH · /API", "accent"))
for x, dashed in ((204, False), (492, False), (780, False), (1068, True)):
    d.append(arrow(f"M {x},840 V 878", "link", dashed=dashed))
# nodes
d.append(node(72, 80, 336, 80, "input", "CONTENT", "Marketing teams", "Universal Editor · Word / Docs"))
d.append(node(472, 80, 336, 80, "input", "DATA", "Operations teams", "Excel · Google Sheets"))
d.append(node(872, 80, 336, 80, "input", "CODE", "Developer teams", "GitHub · vanilla JS · CSS"))
d.append(node(72, 208, 1136, 72, "backend", "EDS", "AEM Edge Delivery storage",
              "content bus · media bus · code bus — preview .aem.page · live .aem.live"))
d.append(node(72, 392, 240, 80, "input", "USERS", "Fans", "browser · OnePass · NFL App"))
d.append(node(72, 560, 240, 64, "external", "PARTNER", "Ticketmaster", "link-out · VIP On Location"))
d.append(node(520, 384, 240, 112, "external", "CDN", "Edge CDN", "cache · WAF · waiting room",
              ["Adobe-managed or BYO CDN"]))
d.append(node(880, 384, 328, 112, "backend", "STATIC", "Cached pages & JSON", "HTML · blocks · events.json",
              ["same for every fan"]))
d.append(node(520, 544, 240, 112, "focal", "EDGE", "Edge worker", "session / auth layer",
              ["stateless · no data at rest"]))
d.append(node(72, 776, 1136, 64, "external", "API", "NFL APIs", "called server-side by the edge worker (via NFL API gateway, if present)"))
d.append(node(72, 880, 264, 64, "external", "IDP", "NFL ID", "id.nfl.com · one account"))
d.append(node(360, 880, 264, 64, "external", "SOR", "OnePass event platform", "registration · QR · check-in"))
d.append(node(648, 880, 264, 64, "external", "SOR", "Notifications", "email · app push"))
d.append(node(936, 880, 264, 64, "external", "EVENT TECH", "Leap", "badges · scan · offers"))
d.append(legend_y(1000, [("input", "People / teams"), ("backend", "Adobe EDS"), ("focal", "Thin edge worker"),
                         ("external", "CDN / NFL / partner"), ("arrow:muted", "Content path"), ("arrow:accent", "Signed-in path"),
                         ("arrow:link", "Server-side call"), ("arrow:link:dashed", "Exit / later")]))

doc = page("nfl-events-hub-layered", "Platform architecture · NFL Events Hub on AEM Edge Delivery Services",
           "NFL Events Hub — platform architecture",
           "NFL Events Hub layered platform architecture",
           "Three-layer architecture of the NFL Events Hub: marketing, operations and developer teams publish into AEM Edge Delivery storage; "
           "the edge CDN serves cached pages to every fan and routes only signed-in calls to a stateless edge worker; the worker calls NFL ID, "
           "the OnePass event platform and notifications; paid tickets link out to Ticketmaster.",
           "\n".join(d))
doc = doc.replace('viewBox="0 0 1280 720"', f'viewBox="0 0 1280 {H}"', 1)
open(f"{OUT}/nfl-events-hub-layered-architecture.html", "w").write(doc)
print("ok")
