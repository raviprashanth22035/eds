"""NFL Events Hub — platform & integrations (client version) in the Adobe 'how it works' look.

Usage: python3 client_adobe.py <output-dir>
"""
import sys, os, base64, html

OUT = sys.argv[1]
ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
with open(os.path.join(ASSETS, "adobe-mark-crop.png"), "rb") as f:
    AMARK = "data:image/png;base64," + base64.b64encode(f.read()).decode()
e = html.escape
W, H = 1440, 1064

ICON = {
    "phone": '<rect x="6" y="2" width="12" height="20" rx="2.5"/><path d="M10.5 18.5h3"/>',
    "app": '<rect x="6" y="2" width="12" height="20" rx="2.5"/><path d="M9 7h6M9 10.5h6M9 14h4"/>',
    "laptop": '<rect x="4" y="5" width="16" height="11" rx="1.5"/><path d="M2 19h20"/>',
}


def box(x, y, w, h, cls, inner):
    return f'<div class="b {cls}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px">{inner}</div>'


def zone(x, y, w, h, label, cls=""):
    return box(x, y, w, h, f"zone {cls}", f'<div class="zl">{e(label)}</div>')


def adobe(x, y, w, h, title, sub="", items=()):
    its = "".join(f'<div class="item">{e(i)}</div>' for i in items)
    s = f'<div class="s">{e(sub)}</div>' if sub else ""
    return box(x, y, w, h, "adobe", f'<img class="mark" src="{AMARK}" alt=""><div class="t">{e(title)}</div>{s}{its}')


def tile(x, y, w, h, cls, title, sub):
    return box(x, y, w, h, f"tile {cls}", f'<div class="t">{e(title)}</div><div class="s">{e(sub)}</div>')


def mini(x, y, title, sub):
    return box(x, y, 212, 48, "blk", f'<div class="t">{e(title)}</div><div class="s">{e(sub)}</div>')


def chan(x, y, icon, title, sub):
    svg = (f'<svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="#3b3b3b" stroke-width="1.7" '
           f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICON[icon]}</svg>')
    return box(x, y, 168, 64, "chan", f'{svg}<div><div class="t">{e(title)}</div><div class="s">{e(sub)}</div></div>')


B = []
# zones
B.append(zone(24, 300, 200, 300, "CHANNELS"))
B.append(zone(1024, 300, 392, 168, "TICKETING PARTNERS"))
B.append(zone(1024, 588, 392, 104, "ADOBE EXPERIENCE CLOUD"))
B.append(zone(1024, 732, 392, 268, "NFL SYSTEMS & MESSAGING"))
# channels
B.append(chan(40, 330, "phone", "NFL OnePass", "embeds the hub"))
B.append(chan(40, 410, "app", "NFL App", "embeds the hub"))
B.append(chan(40, 490, "laptop", "Web", "events.nfl.com"))
# edge + authoring
B.append(adobe(260, 300, 170, 268, "Adobe CDN", "", ["WAF · cache", "routing · queue", "short links"]))
B.append(adobe(520, 92, 400, 76, "AEM authoring", "clubs & league · events · forms"))
# hub
B.append(box(480, 208, 480, 486, "panel hub", f'<img class="mark" src="{AMARK}" alt=""><div class="pt">NFL Events Hub · events.nfl.com<span>AEM Edge Delivery Services</span></div>'))
B.append(box(500, 270, 440, 44, "model", '<b>ONE EVENT<br>MODEL</b><span>League · Club · International<br>Free · Paid · Ticketed · Registration-based</span>'))
discover = [("Event Discovery", "league · club · intl"), ("Events Near Me", "location-aware"),
            ("Event Detail", "venue · map · FAQ"), ("Search & Filters", "events.json"),
            ("Calendar / Schedule", "add to calendar")]
attend = [("Registration", "guest or signed in"), ("Ticketing", "Ticketmaster link-out"),
          ("My Events", "signed in · wallet"), ("QR / Check-in", "guests: by email"),
          ("Event Alerts", "AJO · Campaign")]
for i, (t, s) in enumerate(discover):
    B.append(mini(500, 344 + i * 56, t, s))
for i, (t, s) in enumerate(attend):
    B.append(mini(728, 344 + i * 56, t, s))
B.append(box(500, 632, 440, 44, "pers", '<div class="t">Personalization · signed-in fans only</div>'))
# middleware
B.append(adobe(480, 764, 480, 80, "Secure API layer · edge worker", "forwards registration & sign-in to NFL · stateless · no data"))
# right side
B.append(tile(1048, 330, 344, 52, "tm", "Ticketmaster", "ticketing"))
B.append(tile(1048, 394, 344, 52, "tm", "On Location", "official hospitality"))
B.append(adobe(1048, 626, 344, 52, "Adobe Target · Real-Time CDP", "signed-in personalization"))
B.append(tile(1048, 764, 344, 48, "nfl", "NFL ID", "one fan account · SSO"))
B.append(tile(1048, 828, 344, 52, "leap", "NFL event registration", "OnePass · issues QR · wallet"))
B.append(adobe(1048, 916, 344, 64, "Journey Optimizer · Campaign", "confirmations · reminders · alerts"))

P, LAB = [], []


def path(d, cls="", dashed=False, thick=False):
    a = ' stroke-dasharray="6 5"' if dashed else ""
    m = {"acc": "ahr", "lnk": "ahb"}.get(cls, "ah")
    c = f'{cls} thick' if thick else cls
    P.append(f'<path class="{c}" d="{d}"{a} marker-end="url(#{m})"/>')


def lab(x, y, t, anchor="start", cls=""):
    LAB.append(f'<text class="{cls}" x="{x}" y="{y}" text-anchor="{anchor}">{e(t)}</text>')


for y in (362, 442, 522):
    path(f"M 208,{y} H 258")
lab(234, 350, "https", "middle")
path("M 430,436 H 478")                                  ; lab(454, 428, "origin", "middle")
path("M 720,168 V 206", thick=True)                      ; lab(728, 192, "publish")
path("M 720,694 V 762", "acc")                           ; lab(728, 732, "register (anyone) · sign in", cls="acc")
path("M 960,356 H 1046", "lnk", dashed=True)
path("M 960,420 H 1046", "lnk", dashed=True)            ; lab(1003, 392, "hand-off", "middle", "lnk")
path("M 960,652 H 1046", "lnk", dashed=True)            ; lab(1003, 642, "web sdk", "middle", "lnk")
path("M 960,788 H 1046", "lnk")                          ; lab(1003, 780, "sign in", "middle", "lnk")
path("M 960,824 H 992 Q 1000,824 1000,832 V 846 Q 1000,854 1008,854 H 1046", "lnk")
lab(1003, 874, "register", "middle", "lnk")
path("M 1220,880 V 914", "lnk", dashed=True)             ; lab(1228, 902, "events", cls="lnk")

doc = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NFL Events Hub Platform</title>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;600&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{ background:#fff; font-family:'IBM Plex Mono',ui-monospace,monospace; color:#1f1f1f; }}
  .wrap {{ width:100%; overflow-x:auto; }}
  .slide {{ position:relative; width:{W}px; height:{H}px; margin:0 auto; background:#fff; }}
  h1 {{ position:absolute; left:24px; top:22px; font-size:22px; font-weight:600; }}
  h1 span {{ display:block; font-size:13px; font-weight:400; color:#555; margin-top:4px; }}
  .col {{ position:absolute; top:256px; font-size:10.5px; font-weight:600; letter-spacing:0.12em; color:#666; }}
  .b {{ position:absolute; border-radius:6px; }}
  .zone {{ border:1.5px dashed #b5b5b5; background:transparent; }}
  .zl {{ position:absolute; left:12px; top:-9px; background:#fff; padding:0 6px; font-size:10.5px; font-weight:600; letter-spacing:0.08em; color:#555; }}
  .adobe {{ background:#fbd3d3; padding:12px 14px; }}
  .adobe .mark, .hub .mark {{ position:absolute; left:-12px; top:-14px; width:30px; height:30px; border-radius:4px; }}
  .adobe .t {{ font-size:15px; font-weight:600; }}
  .adobe .s {{ font-size:11.5px; color:#444; margin-top:4px; line-height:1.35; }}
  .item {{ background:#e9e9e9; border-radius:4px; font-size:11.5px; padding:8px 10px; margin-top:12px; box-shadow:2px 2px 0 #cfcfcf; }}
  .panel {{ background:#d6d6d6; }} .hub {{ border:2px solid #e1251b; }}
  .pt {{ position:absolute; left:20px; top:12px; font-size:17px; font-weight:600; }}
  .pt span {{ display:block; font-size:11.5px; font-weight:400; color:#444; margin-top:2px; }}
  .model {{ background:#2d3142; color:#f5f5f5; display:flex; align-items:center; gap:16px; padding:0 16px; }}
  .model b {{ font-size:10.5px; letter-spacing:0.14em; line-height:1.4; border-right:1px solid rgba(255,255,255,0.35); padding-right:16px; }}
  .model span {{ font-family:'IBM Plex Sans',sans-serif; font-size:11.5px; line-height:1.4; }}
  .blk {{ background:#ececec; padding:6px 12px; box-shadow:2px 2px 0 #bdbdbd; }}
  .blk .t, .tile .t {{ font-size:12.5px; font-weight:600; }}
  .blk .s, .tile .s {{ font-size:11px; color:#555; margin-top:2px; }}
  .pers {{ background:#fde7e7; border:1.5px solid #e1251b; display:flex; align-items:center; justify-content:center; box-shadow:2px 2px 0 #bdbdbd; }}
  .pers .t {{ font-size:13px; font-weight:600; }}
  .tile {{ padding:8px 12px; border:1.5px solid rgba(0,0,0,0.12); }}
  .nfl {{ background:#dfe6f6; }} .leap {{ background:#e9e0ff; }} .tm {{ background:#dceaff; }}
  .chan {{ background:#e6e6e6; display:flex; align-items:center; gap:10px; padding:8px 12px; }}
  .chan .t {{ font-size:13px; font-weight:600; }} .chan .s {{ font-size:10.5px; color:#555; margin-top:2px; }}
  svg.conn {{ position:absolute; left:0; top:0; }}
  svg.conn > path {{ fill:none; stroke:#4a4a4a; stroke-width:1.8; }}
  svg.conn > path.thick {{ stroke-width:3; }}
  svg.conn > path.acc {{ stroke:#c11a12; stroke-width:2.2; }}
  svg.conn > path.lnk {{ stroke:#2e5aa8; }}
  svg.conn text {{ font-family:'IBM Plex Mono',monospace; font-size:11.5px; fill:#333; paint-order:stroke; stroke:#fff; stroke-width:4px; }}
  svg.conn text.acc {{ fill:#c11a12; }} svg.conn text.lnk {{ fill:#2e5aa8; }}
  .legend {{ position:absolute; left:24px; top:1024px; display:flex; gap:26px; font-size:11px; color:#444; align-items:center; }}
  .legend i {{ display:inline-block; width:26px; height:0; border-top:2px solid #4a4a4a; margin-right:8px; vertical-align:middle; }}
  .legend i.acc {{ border-color:#c11a12; }} .legend i.lnk {{ border-color:#2e5aa8; }} .legend i.dash {{ border-top-style:dashed; }}
  .legend b {{ display:inline-block; width:14px; height:12px; margin-right:8px; vertical-align:middle; border-radius:2px; }}
</style></head>
<body><div class="wrap"><div class="slide" role="img" aria-label="NFL Events Hub platform and integrations">
<h1>NFL Events Hub — platform &amp; integrations<span>Draft for discussion · one event platform for web, NFL OnePass and the NFL App</span></h1>
<div class="col" style="left:24px">CHANNELS &amp; DELIVERY</div>
<div class="col" style="left:480px;width:480px;text-align:center;top:72px;color:#c11a12">UNIFIED EVENT PLATFORM · BUILT BY US</div>
<div class="col" style="left:1024px;width:392px;text-align:right">NFL, ADOBE &amp; PARTNERS</div>
<svg class="conn" width="{W}" height="{H}" aria-hidden="true">
  <defs>
    <marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#4a4a4a"/></marker>
    <marker id="ahr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#c11a12"/></marker>
    <marker id="ahb" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#2e5aa8"/></marker>
  </defs>
  {''.join(P)}
</svg>
{''.join(B)}
<svg class="conn" width="{W}" height="{H}" aria-hidden="true">{''.join(LAB)}</svg>
<div class="legend">
  <span><b style="background:#fbd3d3"></b>Adobe</span><span><b style="background:#d6d6d6;border:2px solid #e1251b"></b>NFL Events Hub</span>
  <span><b style="background:#dfe6f6;border:1px solid #ccc"></b>NFL / partner</span>
  <span><i></i>Content</span><span><i class="acc"></i>Fan request</span><span><i class="lnk"></i>Server-side</span><span><i class="lnk dash"></i>Async / link-out</span>
</div>
</div></div></body></html>
"""
open(f"{OUT}/nfl-events-hub-client-adobe.html", "w").write(doc)
print("ok")
