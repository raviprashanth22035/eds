"""NFL Event Hub — unified event platform (platform architecture).

Usage: python3 client_arch.py <output-dir>
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa: F401,F403

OUT = sys.argv[1]
H = 1024


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
d.append(text(1240, 28, "NFL, ADOBE & PARTNERS", anchor="end"))
# zones
d.append(zone(24, 240, 200, 280, "CHANNELS"))
d.append(zone(264, 232, 176, 280, "DELIVERY EDGE"))
d.append(zone(488, 144, 416, 472, "NFL EVENTS HUB · EVENTS.NFL.COM · AEM EDGE DELIVERY"))
d.append(zone_l(488, 656, 416, 128, "MIDDLEWARE · THIN, STATELESS"))
d.append(zone(952, 232, 288, 152, "TICKETING PARTNERS"))
d.append(zone(952, 520, 288, 104, "ADOBE EXPERIENCE CLOUD"))
d.append(zone(952, 680, 288, 248, "NFL SYSTEMS & MESSAGING"))
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
d.append(arrow("M 216,384 H 278"))                                                   # NFL App -> CDN
d.append(arrow("M 216,464 H 278"))                                                   # web -> CDN
d.append(label(248, 276, "HTTPS"))
d.append(arrow("M 424,336 H 486"))                                                   # CDN -> hub
d.append(label(456, 308, "ORIGIN"))
d.append(arrow("M 696,616 V 686", "accent"))                                         # hub -> middleware
d.append(vlabel(696, 652, "REGISTER · SIGN-IN", "accent"))
d.append(arrow("M 880,320 H 920 Q 928,320 928,312 V 296 Q 928,288 936,288 H 966", "link", dashed=True))  # -> Ticketmaster
d.append(arrow("M 880,344 H 966", "link", dashed=True))                              # -> On Location
d.append(label(924, 350, "HAND-OFF", "link"))
d.append(arrow("M 880,572 H 966", "link", dashed=True))                              # personalization -> RT-CDP
d.append(label(922, 550, "WEB SDK", "link"))
d.append(arrow("M 880,728 H 966", "link"))                                           # middleware -> NFL ID
d.append(label(922, 704, "SIGN-IN", "link"))
d.append(arrow("M 880,744 H 936 Q 944,744 944,752 V 784 Q 944,792 952,792 H 966", "link"))   # -> registration
d.append(arrow("M 1096,816 V 854", "link", dashed=True))                             # registration -> notifications
d.append(vlabel(1096, 836, "EVENTS", "link"))
# channels
d.append(node(40, 272, 176, 64, "input", "APP", "NFL OnePass", "embeds the hub"))
d.append(node(40, 352, 176, 64, "input", "APP", "NFL App", "embeds the hub"))
d.append(node(40, 432, 176, 64, "input", "WEB", "Web", "events.nfl.com"))
d.append(node(280, 264, 144, 224, "external", "CDN", "Adobe CDN", "WAF · cache", ["routing · queue", "short links"]))
# authoring
d.append(node(536, 40, 320, 64, "input", "AUTHORS", "AEM authoring", "clubs & league · events · forms"))
# hub capability grid
discover = [("Event Discovery", "league · club · intl"), ("Events Near Me", "location-aware"),
            ("Event Detail", "venue · map · FAQ"), ("Search & Filters", "events.json"),
            ("Calendar / Schedule", "add to calendar")]
attend = [("Registration", "guest or signed in"), ("Ticketing", "Ticketmaster link-out"),
          ("My Events", "signed in · wallet"), ("QR / Check-in", "guests: by email"),
          ("Event Alerts", "AJO · Campaign")]
for i, (n, s) in enumerate(discover):
    d.append(mini(512, 244 + i * 60, 176, 52, n, s))
for i, (n, s) in enumerate(attend):
    d.append(mini(704, 244 + i * 60, 176, 52, n, s))
d.append(mini(512, 552, 368, 40, "Personalization · signed-in fans only", kind="focal"))
# middleware
d.append(node(512, 688, 368, 80, "focal", "BFF", "Registration & sign-in service", "guest or NFL ID · stores no fan data"))
# right column
d.append(mini(968, 264, 256, 48, "Ticketmaster", "ticketing", "external"))
d.append(mini(968, 320, 256, 48, "On Location", "official hospitality", "external"))
d.append(mini(968, 544, 256, 56, "Adobe Target · Real-Time CDP", "signed-in personalization", "external"))
d.append(mini(968, 704, 256, 48, "NFL ID", "one fan account · SSO", "external"))
d.append(mini(968, 768, 256, 48, "OnePass registration", "registrations · QR · wallet", "external"))
d.append(mini(968, 856, 256, 56, "Journey Optimizer · Campaign", "confirmations · reminders · alerts", "external"))
d.append(legend_y(952, [("input", "Channels / authors"), ("focal", "Built by us"), ("backend", "Hub capability"),
                        ("external", "NFL / Adobe / partner"), ("arrow:muted", "Content"), ("arrow:accent", "Signed-in"),
                        ("arrow:link", "Synchronous"), ("arrow:link:dashed", "Async / external")]))

doc = page("nfl-events-hub-client", "Draft for discussion · NFL Events Hub",
           "NFL Events Hub — platform & integrations",
           "NFL Events Hub platform and integrations",
           "NFL Events Hub on AEM Edge Delivery: NFL OnePass, the NFL App and the web reach the hub through the Adobe CDN; the hub offers discover "
           "and attend capabilities over one event model, with personalization for signed-in fans; a thin registration and sign-in service calls "
           "NFL ID and OnePass registration, whose events drive Journey Optimizer and Campaign; tickets hand off to Ticketmaster and On Location.",
           "\n".join(d))
doc = doc.replace('viewBox="0 0 1280 720"', f'viewBox="0 0 1280 {H}"', 1)
open(f"{OUT}/nfl-events-hub-client-architecture.html", "w").write(doc)
print("ok")
