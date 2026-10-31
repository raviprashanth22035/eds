"""NFL Events Hub — high-level design (clients box, request flow, platform, NFL services, operations).

Usage: python3 hld.py <output-dir>
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa: F401,F403

OUT = sys.argv[1]
H = 1080

ICONS = {
    # 24x24 line icons, stroke = currentColor
    "phone": '<rect x="6" y="2" width="12" height="20" rx="2.5"/><path d="M10.5 18.5h3"/>',
    "app": '<rect x="6" y="2" width="12" height="20" rx="2.5"/><path d="M9 7h6M9 10.5h6M9 14h4"/>',
    "laptop": '<rect x="4" y="5" width="16" height="11" rx="1.5"/><path d="M2 19h20"/>',
}


def client_row(x, y, w, h, icon, name, sub):
    fill, stroke, *_ = TREAT["input"]
    cy = y + h / 2
    return "\n".join([
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{PAPER}"/>',
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="1"/>',
        f'<g transform="translate({x + 12} {cy - 14}) scale(1.17)" fill="none" stroke="{MUTED}" stroke-width="1.6" '
        f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[icon]}</g>',
        f'<text x="{x + 48}" y="{cy - 2}" fill="{INK}" font-size="16" font-weight="600" font-family="{SANS}">{esc(name)}</text>',
        f'<text x="{x + 48}" y="{cy + 16}" fill="{MUTED}" font-size="12" font-family="{MONO}">{esc(sub)}</text>',
    ])


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
    w = (int(len(text) * 12 * 0.62 + 0.06 * 12 * len(text)) + 12 + 3) // 4 * 4
    return label(x + 8 + w / 2, cy - 8, text, kind)


d = []
# zones
d.append(zone(24, 136, 200, 320, "CLIENTS"))
d.append(zone(512, 104, 368, 768, "PLATFORM · WHAT WE BUILD"))
d.append(zone(1064, 104, 176, 712, "NFL & PARTNERS"))
d.append(f'<text x="40" y="900" fill="{SOFT}" font-size="8" font-family="{MONO}" letter-spacing="0.18em">OPERATIONS</text>')
# connectors
d.append(arrow("M 224,184 H 294"))                                                    # clients -> DNS
d.append(label(260, 156, "HTTPS"))
d.append(arrow("M 376,216 V 278"))                                                    # DNS -> CDN
d.append(arrow("M 456,336 H 534"))                                                    # CDN -> EDS origin
d.append(label(496, 308, "ORIGIN"))
d.append(arrow("M 696,200 V 278"))                                                    # authoring -> EDS
d.append(vlabel(696, 240, "PUBLISH"))
d.append(arrow("M 376,392 V 520 Q 376,528 384,528 H 534", "accent"))                  # CDN -> worker
d.append(label(452, 500, "/AUTH · /API", "accent"))
d.append(arrow("M 856,304 H 1048 Q 1056,304 1056,296 V 176 Q 1056,168 1064,168 H 1078", "link", dashed=True))  # -> Ticketmaster
d.append(vlabel(1056, 248, "BUY", "link"))
d.append(arrow("M 856,488 H 1078", "link"))                                           # worker -> NFL ID
d.append(label(960, 460, "SIGN-IN · SSO", "link"))
d.append(arrow("M 696,568 V 622", "accent"))                                          # worker -> registration
d.append(vlabel(696, 596, "REGISTER", "accent"))
d.append(arrow("M 696,736 V 782"))                                                    # registration -> DB
d.append(arrow("M 856,664 H 1078", "link"))                                           # registration -> notifications
d.append(label(960, 636, "ALERTS", "link"))
d.append(arrow("M 856,712 H 944 Q 952,712 952,720 V 752 Q 952,760 960,760 H 1078", "link"))   # registration -> wallet
d.append(label(900, 684, "PASS", "link"))
# client rows
d.append(client_row(40, 168, 176, 72, "phone", "NFL OnePass", "embeds the hub"))
d.append(client_row(40, 264, 176, 72, "app", "NFL App", "embeds the hub"))
d.append(client_row(40, 360, 176, 72, "laptop", "Web", "nfl.com · clubs"))
# nodes
d.append(node(296, 152, 160, 64, "external", "DNS", "DNS", "nfl.com subdomain"))
d.append(node(296, 280, 160, 112, "external", "CDN", "Edge CDN", "cache · WAF · queue", ["Adobe or BYO"]))
d.append(node(536, 136, 320, 64, "input", "AUTHORS", "AEM authoring", "clubs · league · docs · sheets · UE"))
d.append(node(536, 280, 320, 112, "focal", "PORTAL", "NFL Events Hub", "AEM Edge Delivery",
              ["pages · blocks · events.json"]))
d.append(node(536, 456, 320, 112, "backend", "BFF", "Edge worker", "session · API proxy",
              ["stateless · no data stored"]))
d.append(node(536, 624, 320, 112, "focal", "SERVICE", "Event registration service", "registration · QR · check-in",
              ["capacity · wallet passes"]))
d.append(node(536, 784, 320, 64, "store", "DATA", "Registrations DB", "managed database"))
d.append(node(1080, 136, 144, 64, "external", "PARTNER", "Ticketmaster", "paid events"))
d.append(node(1080, 456, 144, 64, "external", "IDP", "NFL ID", "id.nfl.com"))
d.append(node(1080, 632, 144, 64, "external", "NFL", "Notifications", "email · push"))
d.append(node(1080, 728, 144, 64, "external", "PARTNER", "Wallet", "Apple · Google"))
for i, (tag, name, sub) in enumerate([("CI/CD", "Code", "GitHub → code sync"),
                                      ("ENV", "Preview → live", ".aem.page → .aem.live"),
                                      ("SEC", "Security", "WAF · bot · rate limits"),
                                      ("OBS", "Observability", "AEM telemetry · logs")]):
    d.append(node(40 + i * 304, 912, 288, 64, "store", tag, name, sub))
d.append(legend_y(1008, [("input", "Clients / authors"), ("focal", "Core platform"), ("backend", "Thin edge worker"),
                         ("external", "NFL / partner"), ("store", "Data / operations"), ("arrow:accent", "Signed-in path"),
                         ("arrow:link", "Server-side call"), ("arrow:link:dashed", "Link-out")]))

doc = page("nfl-events-hub-hld", "High-level design · NFL Events Hub",
           "NFL Events Hub — high-level design",
           "NFL Events Hub high-level design",
           "High-level design of the NFL Events Hub: NFL OnePass, NFL App and web clients reach the hub through DNS and the edge CDN; "
           "pages come from AEM Edge Delivery, authored by clubs and the league; only signed-in calls reach a stateless edge worker that "
           "signs fans in with NFL ID and forwards registrations to the event registration service we build, which stores registrations, issues QR codes and wallet passes and triggers notifications; paid events link out to Ticketmaster.",
           "\n".join(d))
doc = doc.replace('viewBox="0 0 1280 720"', f'viewBox="0 0 1280 {H}"', 1)
points = ("<ol class=\"points\">"
          "<li><b>Clients.</b> NFL OnePass and the NFL App open the hub in a WebView; the web is nfl.com and club sites. One portal for all three.</li>"
          "<li><b>Edge.</b> DNS → CDN. The CDN serves cached pages to everyone and sends only <code>/auth</code> and <code>/api</code> to the edge worker.</li>"
          "<li><b>Platform we build.</b> The NFL Events Hub on AEM Edge Delivery (authored by clubs and the league), a thin stateless edge worker, and one event registration service with its own database: registration, capacity, QR codes, check-in and wallet passes.</li>"
          "<li><b>NFL &amp; partners.</b> NFL ID for sign-in, NFL notifications (email, app push) for confirmations and cancellations, Apple / Google Wallet for passes.</li>"
          "<li><b>Partners.</b> Paid events link out to Ticketmaster (VIP via On Location). No payments in the hub.</li>"
          "<li><b>Operations.</b> GitHub → code sync → preview → live; WAF and bot rules at the CDN; AEM telemetry and logs. The only data we hold is in the registration service’s managed database.</li></ol>")
css = """    .points { margin-top: 1.5rem; padding-left: 1.3rem; display: grid; gap: 0.45rem; max-width: 64rem; }
    .points li { font-size: 0.95rem; line-height: 1.55; color: #4f5d75; } .points b { color: #2d3142; }
    code { font-family: var(--font-mono); font-size: 0.82em; }
  </style>"""
doc = doc.replace("  </style>", css, 1).replace("    </div>\n  </div>\n</body>", "    </div>\n    " + points + "\n  </div>\n</body>", 1)
open(f"{OUT}/nfl-events-hub-hld.html", "w").write(doc)
print("ok")
