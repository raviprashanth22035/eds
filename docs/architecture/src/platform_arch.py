"""NFL Event Hub — platform architecture (ownership, data, cross-cutting).

Usage: python3 platform_arch.py <output-dir>
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa: F401,F403

OUT = sys.argv[1]
H = 984


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



def block(x, y, w, kind, tag, name, lines):
    """Box with tag, name and up to three short mono lines."""
    fill, stroke, tagstroke, tagtext = TREAT[kind]
    h = 64 + 16 * len(lines)
    tw = max(28, ((len(tag) * 6 + 12) + 3) // 4 * 4)
    cx = x + w / 2
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{PAPER}"/>',
           f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="1"/>',
           f'<rect x="{x+8}" y="{y+8}" width="{tw}" height="12" rx="2" fill="transparent" stroke="{tagstroke}" stroke-width="0.8"/>',
           f'<text x="{x+8+tw/2:g}" y="{y+17}" fill="{tagtext}" font-size="8" font-family="{MONO}" text-anchor="middle" letter-spacing="0.08em">{esc(tag)}</text>',
           f'<text x="{cx:g}" y="{y+42}" fill="{INK}" font-size="14" font-weight="600" font-family="{SANS}" text-anchor="middle">{esc(name)}</text>']
    for i, ln in enumerate(lines):
        out.append(f'<text x="{cx:g}" y="{y+62+i*16}" fill="{MUTED}" font-size="11" font-family="{MONO}" text-anchor="middle">{esc(ln)}</text>')
    return "\n".join(out)


d = []
# column headers
d.append(text(24, 28, "CHANNELS & DELIVERY"))
d.append(text(696, 28, "UNIFIED EVENT PLATFORM", color=ACCENT, anchor="middle"))
d.append(text(1240, 28, "EXISTING SYSTEMS & PARTNERS", anchor="end"))
# zones (ownership in the labels)
d.append(zone(24, 240, 200, 200, "CHANNELS · NFL APPS & WEB"))
d.append(zone(264, 232, 176, 200, "EDGE · ADOBE-MANAGED OR BYO"))
d.append(zone(488, 144, 416, 280, "NFL EVENT HUB · BUILT BY US ON AEM EDGE DELIVERY"))
d.append(zone_l(488, 496, 416, 120, "MIDDLEWARE · OURS · STATELESS"))
d.append(zone(952, 208, 288, 208, "PARTNERS"))
d.append(zone(952, 424, 288, 96, "ADOBE EXPERIENCE PLATFORM"))
d.append(zone(952, 560, 288, 216, "NFL PLATFORMS & MESSAGING"))
# one event model bar
d.append(f'<rect x="512" y="168" width="368" height="44" rx="6" fill="{INK}"/>')
d.append(text(528, 186, "ONE EVENT", color=PAPER, spacing="0.16em", weight="600"))
d.append(text(528, 200, "MODEL", color=PAPER, spacing="0.16em", weight="600"))
d.append(f'<line x1="612" y1="176" x2="612" y2="204" stroke="rgba(245,245,245,0.35)" stroke-width="1"/>')
d.append(f'<text x="624" y="186" fill="{PAPER}" font-size="10" font-family="{SANS}">League · Club · International</text>')
d.append(f'<text x="624" y="201" fill="{PAPER}" font-size="10" font-family="{SANS}">Free · Paid · Ticketed · Registration-based</text>')
# connectors
d.append(arrow("M 696,104 V 142", dashed=True))                                      # authoring -> hub
d.append(vlabel(696, 128, "PUBLISH"))
d.append(arrow("M 216,304 H 278"))
d.append(arrow("M 216,384 H 278"))
d.append(label(248, 276, "HTTPS"))
d.append(arrow("M 424,336 H 486"))
d.append(label(456, 308, "ORIGIN"))
d.append(arrow("M 696,424 V 526", "accent"))                                         # hub -> middleware
d.append(vlabel(696, 460, "/AUTH · /API", "accent"))
d.append(arrow("M 880,264 H 966", "link", dashed=True))                              # attend -> Ticketmaster
d.append(arrow("M 880,320 H 966", "link", dashed=True))                              # attend -> On Location
d.append(label(924, 242, "HAND-OFF", "link"))
d.append(arrow("M 966,376 H 906", "link", dashed=True))                              # OneTrust -> hub
d.append(label(928, 354, "CONSENT", "link"))
d.append(arrow("M 860,400 V 468 Q 860,476 868,476 H 966", "link", dashed=True))   # web sdk
d.append(label(916, 454, "WEB SDK", "link"))
d.append(arrow("M 880,536 H 984 Q 992,536 992,528 V 506", "link", dashed=True))      # profile data
d.append(label(940, 514, "PROFILE", "link"))
d.append(arrow("M 880,560 H 936 Q 944,560 944,568 V 600 Q 944,608 952,608 H 966", "link"))   # -> Leap
d.append(arrow("M 880,576 H 920 Q 928,576 928,584 V 664 Q 928,672 936,672 H 966", "link"))  # -> NFL ID
d.append(arrow("M 880,592 H 904 Q 912,592 912,600 V 728 Q 912,736 920,736 H 966", "link", dashed=True))  # -> notifications
# nodes
d.append(node(40, 272, 176, 64, "input", "APP", "NFL OnePass", "WebView · token"))
d.append(node(40, 352, 176, 64, "input", "WEB", "Web", "nfl.com · events"))
d.append(node(280, 264, 144, 144, "external", "CDN", "Edge CDN", "WAF · cache", ["data: cache only"]))
d.append(node(536, 40, 320, 64, "input", "AUTHORS", "Content authoring", "events · forms · club × market × lang"))
d.append(block(512, 232, 180, "backend", "OURS", "Discover", ["discovery · near me", "detail · search", "calendar / schedule"]))
d.append(block(700, 232, 180, "backend", "OURS", "Attend", ["registration · ticketing", "my events · QR", "event alerts"]))
d.append(mini(512, 360, 368, 40, "Personalization · applied across all blocks", kind="focal"))
d.append(node(512, 528, 368, 72, "focal", "OURS", "Identity & API middleware", "NFL ID session · API mediation"))
d.append(mini(968, 240, 256, 48, "Ticketmaster", "ticketing · payments", "external"))
d.append(mini(968, 296, 256, 48, "On Location", "official hospitality", "external"))
d.append(mini(968, 352, 256, 48, "OneTrust", "consent & privacy", "external"))
d.append(mini(968, 448, 256, 56, "Real-Time CDP", "data: profiles · NFL ID identity", "external"))
d.append(mini(968, 584, 256, 48, "OnePass registration", "data: registrations · QR", "external"))
d.append(mini(968, 648, 256, 48, "NFL ID", "data: fan accounts · SSO", "external"))
d.append(mini(968, 712, 256, 48, "Notifications", "Journey Optimizer · Campaign", "external"))
# cross-cutting band
d.append(text(40, 808, "CROSS-CUTTING"))
for i, (tag, name, sub) in enumerate([("SEC", "Security", "WAF · bot rules · rate limits"),
                                      ("IAM", "Identity & consent", "NFL ID · OneTrust · minors"),
                                      ("OBS", "Observability", "AEM telemetry · logs · alerts"),
                                      ("OPS", "CI/CD & environments", "GitHub · preview → live")]):
    d.append(node(40 + i * 304, 816, 288, 64, "store", tag, name, sub))
d.append(legend_y(912, [("input", "Channels / authors"), ("focal", "Built by us · focus"), ("backend", "Built by us"),
                        ("external", "Adobe / NFL / partner"), ("store", "Cross-cutting"), ("arrow:accent", "Signed-in"),
                        ("arrow:link", "Synchronous"), ("arrow:link:dashed", "Async / external")]))

doc = page("nfl-event-hub-platform", "Platform architecture · NFL Event Hub",
           "NFL Event Hub — platform architecture",
           "NFL Event Hub platform architecture",
           "Platform architecture of the NFL Event Hub with ownership and data: NFL OnePass and web reach the hub through an Adobe-managed or "
           "BYO edge CDN; the hub and a thin, stateless identity and API middleware are built by us on AEM Edge Delivery; partners handle "
           "ticketing and consent; Real-Time CDP holds profiles; OnePass registration, NFL ID and Adobe messaging hold registrations, accounts and notifications; "
           "security, identity and consent, observability and CI/CD run across the platform.",
           "\n".join(d))
doc = doc.replace('viewBox="0 0 1280 720"', f'viewBox="0 0 1280 {H}"', 1)
open(f"{OUT}/nfl-event-hub-platform-architecture.html", "w").write(doc)
print("ok")
