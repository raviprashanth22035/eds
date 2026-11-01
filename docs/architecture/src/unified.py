"""NFL Event Hub — unified event platform (platform architecture).

Usage: python3 unified.py <output-dir>
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa: F401,F403

OUT = sys.argv[1]
H = 1000


def mini(x, y, w, h, name, sub=None, kind="backend"):
    """Compact block for the hub's inner capability grid."""
    fill, stroke, *_ = TREAT[kind]
    cx = x + w / 2
    ny = y + h / 2 + (4 if not sub else -2)
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{PAPER}"/>',
           f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="1"/>',
           f'<text x="{cx:g}" y="{ny:g}" fill="{INK}" font-size="12" font-weight="600" font-family="{SANS}" text-anchor="middle">{esc(name)}</text>']
    if sub:
        out.append(f'<text x="{cx:g}" y="{ny + 15:g}" fill="{MUTED}" font-size="10" font-family="{MONO}" text-anchor="middle">{esc(sub)}</text>')
    return "\n".join(out)


def text(x, y, s, size=8, color=None, anchor="start", spacing="0.18em", weight=None):
    w = f' font-weight="{weight}"' if weight else ""
    return (f'<text x="{x}" y="{y}" fill="{color or SOFT}" font-size="{size}" font-family="{MONO}"{w} '
            f'text-anchor="{anchor}" letter-spacing="{spacing}">{esc(s)}</text>')


def legend_y(y0, items):
    out = [f'<line x1="40" y1="{y0}" x2="1240" y2="{y0}" stroke="rgba(45,49,66,0.10)" stroke-width="0.8"/>',
           f'<text x="40" y="{y0+20}" fill="{MUTED}" font-size="8" font-family="{MONO}" letter-spacing="0.18em">LEGEND</text>']
    x = 40
    for kind, label_text in items:
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
        out.append(f'<text x="{tx}" y="{y0+44}" fill="{MUTED}" font-size="10" font-family="{SANS}">{esc(label_text)}</text>')
        x = tx + int(len(label_text) * 5.8) + 28
    return "\n".join(out)


def vlabel(x, cy, t, kind="muted"):
    w = (int(len(t) * 12 * 0.62 + 0.06 * 12 * len(t)) + 12 + 3) // 4 * 4
    return label(x + 8 + w / 2, cy - 8, t, kind)


def zone_l(x, y, w, h, t):
    lw = (int(len(t) * 8 * 0.76) + 16 + 3) // 4 * 4
    return "\n".join([
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="rgba(45,49,66,0.02)" stroke="rgba(45,49,66,0.10)" stroke-width="0.8"/>',
        f'<rect x="{x + 16}" y="{y + 4}" width="{lw}" height="12" rx="2" fill="{PAPER}"/>',
        f'<text x="{x + 16 + lw / 2:g}" y="{y + 13}" fill="{SOFT}" font-size="8" font-family="{MONO}" text-anchor="middle" letter-spacing="0.14em">{esc(t)}</text>'])


d = []
# column headers
d.append(text(24, 28, "CHANNELS & DELIVERY"))
d.append(text(696, 28, "UNIFIED EVENT PLATFORM", color=ACCENT, anchor="middle"))
d.append(text(1240, 28, "EXISTING SYSTEMS & PARTNERS", anchor="end"))
# zones
d.append(zone(24, 240, 200, 200, "CHANNELS"))
d.append(zone(264, 232, 176, 200, "DELIVERY EDGE"))
d.append(zone(488, 144, 416, 472, "NFL EVENT HUB · EXPERIENCE COMPOSITION · AEM EDGE DELIVERY"))
d.append(zone_l(488, 656, 416, 128, "MIDDLEWARE · THIN, STATELESS"))
d.append(zone(952, 232, 288, 208, "COMMERCE & CONSENT"))
d.append(zone(952, 520, 288, 104, "ADOBE EXPERIENCE PLATFORM"))
d.append(zone(952, 680, 288, 224, "PLATFORMS & MESSAGING"))
# one event model bar
d.append(f'<rect x="512" y="168" width="368" height="44" rx="6" fill="{INK}"/>')
d.append(text(528, 186, "ONE EVENT", color=PAPER, spacing="0.16em", weight="600"))
d.append(text(528, 200, "MODEL", color=PAPER, spacing="0.16em", weight="600"))
d.append(f'<line x1="612" y1="176" x2="612" y2="204" stroke="rgba(245,245,245,0.35)" stroke-width="1"/>')
d.append(f'<text x="624" y="186" fill="{PAPER}" font-size="10" font-family="{SANS}">League · Club · International</text>')
d.append(f'<text x="624" y="201" fill="{PAPER}" font-size="10" font-family="{SANS}">Free · Paid · Ticketed · Registration-based</text>')
d.append(text(512, 236, "DISCOVER"))
d.append(text(704, 236, "ATTEND"))
# connectors (behind nodes)
d.append(arrow("M 696,104 V 142", dashed=True))                                      # authoring -> hub
d.append(vlabel(696, 128, "PUBLISH"))
d.append(arrow("M 216,304 H 278"))                                                   # OnePass -> CDN
d.append(arrow("M 216,384 H 278"))                                                   # web -> CDN
d.append(label(248, 276, "HTTPS"))
d.append(arrow("M 424,336 H 486"))                                                   # CDN -> hub
d.append(label(456, 308, "ORIGIN"))
d.append(arrow("M 696,616 V 686", "accent"))                                         # hub -> middleware
d.append(vlabel(696, 652, "/AUTH · /API", "accent"))
d.append(arrow("M 880,320 H 920 Q 928,320 928,312 V 296 Q 928,288 936,288 H 966", "link", dashed=True))  # -> Ticketmaster
d.append(arrow("M 880,344 H 966", "link", dashed=True))                              # -> On Location
d.append(label(924, 350, "HAND-OFF", "link"))
d.append(arrow("M 966,400 H 906", "link", dashed=True))                              # OneTrust -> hub
d.append(label(928, 406, "CONSENT", "link"))
d.append(arrow("M 880,572 H 966", "link", dashed=True))                              # personalization -> RT-CDP
d.append(label(922, 550, "WEB SDK", "link"))
d.append(arrow("M 880,696 H 984 Q 992,696 992,688 V 602", "link", dashed=True))      # middleware -> RT-CDP
d.append(label(940, 674, "PROFILE DATA", "link"))
d.append(arrow("M 880,728 H 966", "link"))                                           # middleware -> Leap
d.append(arrow("M 880,744 H 936 Q 944,744 944,752 V 784 Q 944,792 952,792 H 966", "link"))   # -> NFL ID
d.append(arrow("M 880,760 H 920 Q 928,760 928,768 V 848 Q 928,856 936,856 H 966", "link", dashed=True))  # -> notifications
# channels
d.append(node(40, 272, 176, 64, "input", "APP", "NFL OnePass", "WebView · token"))
d.append(node(40, 352, 176, 64, "input", "WEB", "Web", "nfl.com · events"))
d.append(node(280, 264, 144, 144, "external", "CDN", "Edge CDN", "WAF · cache", ["routing · queue"]))
# authoring
d.append(node(536, 40, 320, 64, "input", "AUTHORS", "Content authoring", "events · forms · club × market × lang"))
# hub capability grid
discover = [("Event Discovery", "league · club · intl"), ("Events Near Me", "location-aware"),
            ("Event Detail", "venue · map · FAQ"), ("Search & Filters", "events.json"),
            ("Calendar / Schedule", "add to calendar")]
attend = [("Registration", "EDS forms → Leap"), ("Ticketing", "Ticketmaster · On Loc."),
          ("My Events", "signed-in profile"), ("QR / Check-in", "via Leap"),
          ("Event Alerts", "AJO · Campaign")]
for i, (n, s) in enumerate(discover):
    d.append(mini(512, 244 + i * 60, 176, 52, n, s))
for i, (n, s) in enumerate(attend):
    d.append(mini(704, 244 + i * 60, 176, 52, n, s))
d.append(mini(512, 552, 368, 40, "Personalization · applied across all blocks", kind="focal"))
# middleware
d.append(node(512, 688, 368, 80, "focal", "BFF", "Identity & API middleware", "anonymous + NFL ID session · API mediation"))
# right column
d.append(mini(968, 264, 256, 48, "Ticketmaster", "ticketing", "external"))
d.append(mini(968, 320, 256, 48, "On Location", "official hospitality", "external"))
d.append(mini(968, 376, 256, 48, "OneTrust", "consent & privacy", "external"))
d.append(mini(968, 544, 256, 56, "Real-Time CDP", "Edge Network · NFL ID identity", "external"))
d.append(mini(968, 704, 256, 48, "Leap Event Platform", "registration · QR · check-in", "external"))
d.append(mini(968, 768, 256, 48, "NFL ID", "SSO · all NFL apps", "external"))
d.append(mini(968, 832, 256, 56, "Notifications", "Journey Optimizer · Campaign", "external"))
d.append(legend_y(928, [("input", "Channels / authors"), ("focal", "Platform focus"), ("backend", "Hub capability"),
                        ("external", "Existing system / partner"), ("arrow:muted", "Content"), ("arrow:accent", "Signed-in"),
                        ("arrow:link", "Synchronous"), ("arrow:link:dashed", "Async / external")]))

doc = page("nfl-event-hub-unified", "Capability & integration view · NFL Event Hub",
           "NFL Event Hub — capabilities & integrations",
           "NFL Event Hub unified event platform",
           "Platform architecture of the NFL Event Hub: NFL OnePass and web channels reach the hub through the edge CDN; the hub on AEM Edge "
           "Delivery composes discover and attend capabilities over one event model with personalization across all blocks; a thin identity and "
           "API middleware handles NFL ID sessions and calls Leap for registration, QR and check-in, Adobe Real-Time CDP for profile data and "
           "Journey Optimizer and Campaign for notifications; ticketing hands off to Ticketmaster and On Location, and OneTrust supplies consent.",
           "\n".join(d))
doc = doc.replace('viewBox="0 0 1280 720"', f'viewBox="0 0 1280 {H}"', 1)
open(f"{OUT}/nfl-event-hub-unified-platform.html", "w").write(doc)
print("ok")
