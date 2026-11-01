"""NFL Events Hub — platform architecture (layers, ownership, integrations) in the EDS-map visual style.

Usage: python3 platform_eds.py <output-dir>
"""
import sys, os, base64, html

OUT = sys.argv[1]
ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
with open(os.path.join(ASSETS, "adobe-mark-crop.png"), "rb") as f:
    AMARK = "data:image/png;base64," + base64.b64encode(f.read()).decode()
e = html.escape
W, H = 1440, 960

ICON = {
    "phone": '<rect x="6" y="2" width="12" height="20" rx="2.5"/><path d="M10.5 18.5h3"/>',
    "app": '<rect x="6" y="2" width="12" height="20" rx="2.5"/><path d="M9 7h6M9 10.5h6M9 14h4"/>',
    "laptop": '<rect x="4" y="5" width="16" height="11" rx="1.5"/><path d="M2 19h20"/>',
}


def box(x, y, w, h, cls, inner):
    return f'<div class="b {cls}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px">{inner}</div>'


def zone(x, y, w, h, label, cls=""):
    return box(x, y, w, h, f"zone {cls}", f'<div class="zl">{e(label)}</div>')


def adobe(x, y, w, h, title, sub=""):
    s = f'<div class="s">{e(sub)}</div>' if sub else ""
    return box(x, y, w, h, "adobe", f'<img class="mark" src="{AMARK}" alt=""><div class="t">{e(title)}</div>{s}')


def tile(x, y, w, h, cls, title, sub):
    return box(x, y, w, h, f"tile {cls}", f'<div class="t">{e(title)}</div><div class="s">{e(sub)}</div>')


def chan(x, y, icon, title, sub):
    svg = (f'<svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="#3b3b3b" stroke-width="1.7" '
           f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICON[icon]}</svg>')
    return box(x, y, 168, 64, "chan", f'{svg}<div><div class="t">{e(title)}</div><div class="s">{e(sub)}</div></div>')


def group(x, y, w, h, title, items):
    lis = "".join(f'<li>{e(i)}</li>' for i in items)
    return box(x, y, w, h, "grp", f'<div class="t">{e(title)}</div><ul>{lis}</ul>')


def bar(x, y, w, h, cls, title, sub):
    return box(x, y, w, h, f"barx {cls}", f'<div class="t">{e(title)}</div><div class="s">{e(sub)}</div>')


B = []
# zones (ownership)
B.append(zone(24, 150, 200, 268, "1 · CHANNELS"))
B.append(zone(256, 108, 712, 610, "2 · EXPERIENCE PLATFORM · BUILT BY US", "ours"))
B.append(zone(1000, 254, 416, 96, "5 · PARTNERS"))
B.append(zone(1000, 450, 416, 194, "4 · ADOBE EXPERIENCE CLOUD"))
B.append(zone(1000, 664, 416, 148, "3 · NFL SYSTEMS · EXISTING"))
# channels
B.append(chan(40, 182, "laptop", "Web", "events.nfl.com · clubs"))
B.append(chan(40, 260, "phone", "NFL OnePass", "embeds the hub"))
B.append(chan(40, 338, "app", "NFL App", "embeds the hub"))
# platform
B.append(adobe(280, 140, 380, 72, "Adobe CDN", "fast, secure delivery · short links · country & language"))
B.append(adobe(700, 140, 244, 72, "AEM authoring", "clubs & league teams"))
B.append(box(280, 252, 664, 340, "panel hub", f'<img class="mark" src="{AMARK}" alt=""><div class="pt">NFL Events Hub · events.nfl.com<span>AEM Edge Delivery Services · content stays in AEM</span></div>'))
B.append(group(300, 318, 304, 156, "Discover", ["League, club & international events", "Event details & venue map", "Events near me · calendar"]))
B.append(group(620, 318, 304, 156, "Attend", ["Register as guest or signed in", "Guest: QR code by email", "Signed in: My Events + wallet", "Buy tickets (link-out)"]))
B.append(bar(300, 484, 624, 44, "pers", "Personalization · signed-in fans only", "guests see the standard page"))
B.append(bar(300, 536, 624, 44, "run", "Run by clubs & league", "event sheets · club × market roll-out · languages"))
B.append(adobe(280, 622, 664, 72, "Registration & sign-in service", "thin edge service · guest or NFL ID · stores no fan data"))
# right side
B.append(tile(1024, 282, 352, 56, "tm", "Ticketmaster · On Location", "paid tickets · hospitality — link-out"))
B.append(adobe(1024, 474, 352, 64, "Adobe Target · Real-Time CDP", "personalization · fan profiles"))
B.append(adobe(1024, 556, 352, 72, "Journey Optimizer · Campaign", "confirmations · reminders · alerts → fans"))
B.append(tile(1024, 676, 352, 48, "nfl", "NFL ID", "one fan account · SSO across NFL apps"))
B.append(tile(1024, 740, 352, 56, "leap", "OnePass registration", "registrations · QR codes · wallet passes"))
# cross-cutting
XC = [("Security", "WAF · bot protection · rate limits"), ("Identity & consent", "NFL ID · consent banner"),
      ("Observability", "AEM telemetry · logs · alerts"), ("Delivery", "GitHub → preview → live")]
for i, (t, s) in enumerate(XC):
    B.append(tile(24 + i * 350, 838, 334, 52, "xc", t, s))

P, LAB = [], []


def path(d, cls="", dashed=False):
    a = ' stroke-dasharray="6 5"' if dashed else ""
    P.append(f'<path class="{cls}" d="{d}"{a} marker-end="url(#ah{"r" if cls == "acc" else ("b" if cls == "lnk" else "")})"/>')


def lab(x, y, t, anchor="start", cls=""):
    LAB.append(f'<text class="{cls}" x="{x}" y="{y}" text-anchor="{anchor}">{e(t)}</text>')


path("M 224,216 H 278")                                  ; lab(251, 208, "https", "middle")
path("M 470,212 V 250")                                  ; lab(478, 236, "pages")
path("M 822,212 V 250", "thick")                         ; lab(830, 236, "publish")
path("M 612,592 V 620", "acc")                           ; lab(624, 610, "register · sign in", cls="acc")
path("M 944,310 H 1022", "lnk", dashed=True)             ; lab(983, 302, "buy", "middle", "lnk")
path("M 944,506 H 1022", "lnk", dashed=True)             ; lab(983, 498, "web sdk", "middle", "lnk")
path("M 944,686 H 1022", "lnk")                          ; lab(983, 676, "sign in", "middle", "lnk")
path("M 900,694 V 760 Q 900,768 908,768 H 1022", "lnk")
lab(912, 758, "register", cls="lnk")
path("M 1376,768 H 1392 Q 1400,768 1400,760 V 600 Q 1400,592 1392,592 H 1378", "lnk", dashed=True)
lab(1394, 656, "events", "end", "lnk")

doc = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NFL Events Hub Platform Architecture</title>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;600&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{ background:#fff; font-family:'IBM Plex Mono',ui-monospace,monospace; color:#1f1f1f; }}
  .wrap {{ width:100%; overflow-x:auto; }}
  .slide {{ position:relative; width:{W}px; height:{H}px; margin:0 auto; background:#fff; }}
  h1 {{ position:absolute; left:24px; top:24px; font-size:22px; font-weight:600; }}
  h1 span {{ display:block; font-size:13px; font-weight:400; color:#555; margin-top:4px; }}
  .b {{ position:absolute; border-radius:6px; }}
  .zone {{ border:1.5px dashed #b5b5b5; background:#fafafa; }}
  .zone.ours {{ border:2px dashed #e1251b; background:#fff8f8; }}
  .zl {{ position:absolute; left:12px; top:-9px; background:#fff; padding:0 6px; font-size:10.5px; font-weight:600; letter-spacing:0.08em; color:#555; }}
  .zone.ours .zl {{ color:#c11a12; }}
  .adobe {{ background:#fbd3d3; padding:12px 14px; }}
  .adobe .mark, .hub .mark {{ position:absolute; left:-12px; top:-14px; width:30px; height:30px; border-radius:4px; }}
  .adobe .t {{ font-size:15px; font-weight:600; }}
  .adobe .s {{ font-size:11.5px; color:#444; margin-top:4px; line-height:1.35; }}
  .panel {{ background:#d6d6d6; }} .hub {{ border:2px solid #e1251b; }}
  .pt {{ position:absolute; left:20px; top:12px; font-size:17px; font-weight:600; }}
  .pt span {{ display:block; font-size:11.5px; font-weight:400; color:#444; margin-top:2px; }}
  .grp {{ background:#ececec; padding:10px 14px; box-shadow:2px 2px 0 #bdbdbd; }}
  .grp .t {{ font-size:14px; font-weight:600; margin-bottom:6px; }}
  .grp ul {{ list-style:none; display:grid; gap:6px; }}
  .grp li {{ font-family:'IBM Plex Sans',sans-serif; font-size:12.5px; line-height:1.3; padding-left:12px; position:relative; }}
  .grp li::before {{ content:""; position:absolute; left:0; top:6px; width:5px; height:5px; border-radius:50%; background:#e1251b; }}
  .barx {{ padding:6px 14px; box-shadow:2px 2px 0 #bdbdbd; display:flex; align-items:baseline; gap:12px; }}
  .barx .t {{ font-size:13px; font-weight:600; }} .barx .s {{ font-size:11px; color:#444; }}
  .pers {{ background:#fde7e7; }} .run {{ background:#ececec; }}
  .tile {{ padding:8px 12px; border:1.5px solid rgba(0,0,0,0.12); }}
  .tile .t {{ font-size:13px; font-weight:600; }} .tile .s {{ font-size:11px; color:#555; margin-top:3px; }}
  .nfl {{ background:#dfe6f6; }} .leap {{ background:#e9e0ff; }} .tm {{ background:#dceaff; }} .xc {{ background:#f0f0f0; }}
  .chan {{ background:#e6e6e6; display:flex; align-items:center; gap:10px; padding:8px 12px; }}
  .chan .t {{ font-size:13px; font-weight:600; }} .chan .s {{ font-size:10.5px; color:#555; margin-top:2px; }}
  svg.conn {{ position:absolute; left:0; top:0; }}
  svg.conn > path {{ fill:none; stroke:#4a4a4a; stroke-width:1.8; }}
  svg.conn > path.thick {{ stroke-width:3; }}
  svg.conn > path.acc {{ stroke:#c11a12; stroke-width:2.2; }}
  svg.conn > path.lnk {{ stroke:#2e5aa8; }}
  svg.conn marker path {{ stroke:none; }}
  svg.conn text {{ font-family:'IBM Plex Mono',monospace; font-size:11.5px; fill:#333; paint-order:stroke; stroke:#fff; stroke-width:4px; }}
  svg.conn text.acc {{ fill:#c11a12; }} svg.conn text.lnk {{ fill:#2e5aa8; }}
  .xh {{ position:absolute; left:24px; top:814px; font-size:10.5px; font-weight:600; letter-spacing:0.08em; color:#555; }}
  .legend {{ position:absolute; left:24px; top:906px; display:flex; gap:26px; font-size:11px; color:#444; align-items:center; }}
  .legend i {{ display:inline-block; width:26px; height:0; border-top:2px solid #4a4a4a; margin-right:8px; vertical-align:middle; }}
  .legend i.acc {{ border-color:#c11a12; }} .legend i.lnk {{ border-color:#2e5aa8; }} .legend i.dash {{ border-top-style:dashed; }}
  .legend b {{ display:inline-block; width:14px; height:12px; margin-right:8px; vertical-align:middle; border-radius:2px; }}
</style></head>
<body><div class="wrap"><div class="slide" role="img" aria-label="NFL Events Hub platform architecture: channels, the experience platform we build, NFL systems, Adobe Experience Cloud and partners">
<h1>NFL Events Hub — platform architecture<span>One event platform on AEM Edge Delivery Services · events.nfl.com (proposed) · web, NFL OnePass and the NFL App</span></h1>
{''.join(B)}
<svg class="conn" width="{W}" height="{H}" aria-hidden="true">
  <defs>
    <marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#4a4a4a"/></marker>
    <marker id="ahr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#c11a12"/></marker>
    <marker id="ahb" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#2e5aa8"/></marker>
  </defs>
  {''.join(P)}{''.join(LAB)}
</svg>
<div class="xh">CROSS-CUTTING</div>
<div class="legend">
  <span><b style="background:#fff8f8;border:2px dashed #e1251b"></b>Built by us</span>
  <span><b style="background:#fbd3d3"></b>Adobe</span>
  <span><b style="background:#dfe6f6;border:1px solid #ccc"></b>NFL / partner</span>
  <span><i></i>Content</span><span><i class="acc"></i>Fan request</span><span><i class="lnk"></i>Server-side</span><span><i class="lnk dash"></i>Async / link-out</span>
  <span style="color:#777">Target / RT-CDP licences to be confirmed with NFL.</span>
</div>
</div></div></body></html>
"""
open(f"{OUT}/nfl-events-hub-platform.html", "w").write(doc)
print("ok")
