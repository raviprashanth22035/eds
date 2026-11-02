"""NFL Events Hub — platform architecture in an Adobe AEP/AJO deck look (16:9).

Usage: python3 aep_style.py <output-dir>
"""
import sys, os, base64, html

OUT = sys.argv[1]
ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
with open(os.path.join(ASSETS, "adobe-mark-crop.png"), "rb") as f:
    AMARK = "data:image/png;base64," + base64.b64encode(f.read()).decode()
e = html.escape
W, H = 1600, 900

ICON = {
    "phone": '<rect x="6" y="2" width="12" height="20" rx="2.5"/><path d="M10.5 18.5h3"/>',
    "app": '<rect x="6" y="2" width="12" height="20" rx="2.5"/><path d="M9 7h6M9 10.5h6M9 14h4"/>',
    "laptop": '<rect x="4" y="5" width="16" height="11" rx="1.5"/><path d="M2 19h20"/>',
}


def icon(k):
    return (f'<svg viewBox="0 0 24 24" width="30" height="30" fill="none" stroke="#5a5a5a" stroke-width="1.6" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICON[k]}</svg>')


def box(x, y, w, h, cls, inner=""):
    return f'<div class="b {cls}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px">{inner}</div>'


def item(x, y, w, h, title, sub=""):
    s = f'<i>{e(sub)}</i>' if sub else ""
    return box(x, y, w, h, "item", f'<b>{e(title)}</b>{s}')


def panel(x, y, w, h, title, items, ih=44, gap=6):
    out = [box(x, y, w, h, "panel"), box(x, y, w, 28, "ph", e(title))]
    yy = y + 36
    for t, s in items:
        out.append(item(x + 10, yy, w - 20, ih, t, s))
        yy += ih + gap
    return "\n".join(out)


B = []
# header band
B.append(box(140, 118, 1320, 22, "band",
             '<span style="left:20px">CHANNELS</span><span style="left:230px">AUTHORING &amp; DELIVERY</span>'
             '<span style="left:640px">NFL EVENTS HUB</span><span style="left:1150px">INTEGRATIONS</span>'))
# channels column
B.append(box(140, 250, 100, 390, "src", '<div class="st">Channels</div>'
             f'<div class="ci">{icon("phone")}<span>NFL OnePass<br><i>embedded hub</i></span></div>'
             f'<div class="ci">{icon("app")}<span>NFL App<br><i>embedded hub</i></span></div>'
             f'<div class="ci">{icon("laptop")}<span>Web<br><i>events.nfl.com</i></span></div>'))
# CDN bar
B.append(box(290, 180, 470, 28, "dark", '<img class="mk" src="' + AMARK + '" alt="">Adobe CDN · WAF · edge cache · routing &amp; queuing'))
# outer platform panel + gold hub box
B.append(box(270, 226, 950, 534, "outer"))
B.append(box(540, 246, 660, 414, "gold"))
# authoring & delivery
B.append(panel(290, 250, 220, 210, "EDS Authoring",
               [("Document Authoring", ""), ("Universal Editor", ""), ("Registration Forms", ""), ("Event Sources", "")], ih=32))
B.append(panel(290, 480, 220, 112, "Content & Code", [("Content & media bus", "EDS"), ("GitHub", "EDS blocks · middleware")], ih=30))
B.append(box(290, 620, 220, 120, "dark mw", '<img class="mk" src="' + AMARK + '" alt=""><b>Middleware · Edge Worker</b>'
             '<i>NFL ID sign-in &amp; session<br>stateless · no data persisted</i>'))
# hub
B.append(box(560, 262, 620, 30, "dark", '<img class="mk" src="' + AMARK + '" alt="">NFL Events Hub · events.nfl.com · AEM Edge Delivery Services'))
B.append(box(560, 302, 620, 30, "model", '<b>Unified Event Model</b> League · Club · International &nbsp;|&nbsp; Free · Paid · Ticketed · Registration'))
B.append(panel(560, 346, 200, 296, "Discover",
               [("Event Discovery", "league, club & international"), ("Location Search", "events near me"),
                ("Event Detail", "venue, schedule, FAQ"), ("Search & Filter", "indexed event catalog"),
                ("Calendar", "add to calendar")]))
B.append(panel(780, 346, 200, 296, "Attend",
               [("Registration", "guest & authenticated"), ("Ticketing", "hand-off to Ticketmaster"),
                ("My Events", "authenticated · wallet"), ("Entry QR", "email (guest) · in-app"),
                ("Event Alerts", "status & cancellations")]))
B.append(panel(1000, 500, 156, 142, "Personalization", [("Contextual · all fans", "near me · market · language"), ("Profile · signed-in", "favourite club · past events")], ih=46))
# integrations column
B.append(box(1250, 250, 210, 500, "src", '<div class="st">Integrations</div>'))
B.append(item(1262, 296, 186, 44, "Journey Optimizer · Campaign", "confirmations · alerts"))
B.append(item(1262, 388, 186, 44, "NFL Event Registration", "OnePass · QR · wallet pass"))
B.append(item(1262, 438, 186, 44, "Ticketmaster · On Location", "ticketing · hospitality"))
B.append(item(1262, 568, 186, 44, "Adobe Target · RT-CDP", "contextual & profile-based"))
B.append(item(1262, 658, 186, 44, "NFL ID", "identity · single sign-on"))
# footer
B.append(box(290, 800, 420, 40, "foot", f'<img src="{AMARK}" alt="">Adobe Experience Manager · Edge Delivery Services'))
B.append(box(740, 800, 360, 40, "foot", f'<img src="{AMARK}" alt="">Adobe Experience Cloud'))

P, L = [], []


def path(d, kind="egress", dashed=False):
    a = ' stroke-dasharray="5 4"' if dashed else ""
    P.append(f'<path class="{kind}" d="{d}"{a} marker-end="url(#m-{kind})"/>')


def lab(x, y, t, anchor="start", kind=""):
    L.append(f'<text class="{kind}" x="{x}" y="{y}" text-anchor="{anchor}">{e(t)}</text>')


path("M 215,250 V 202 Q 215,194 223,194 H 288", "ingress")            ; lab(222, 186, "HTTPS", kind="ingress")
path("M 700,208 V 244", "ingress")                                     ; lab(706, 230, "pages", kind="ingress")
path("M 510,300 H 538", "intra", dashed=True)                          ; lab(524, 292, "publish", "middle", "intra")
path("M 400,460 V 478", "intra", dashed=True)
path("M 540,652 Q 526,652 526,660 V 672 Q 526,680 518,680 H 512", "egress") ; lab(536, 674, "authenticate", kind="egress")
path("M 968,410 H 1260", "egress")                                     ; lab(1090, 402, "register", "middle", "egress")
path("M 968,460 H 1260", "egress", dashed=True)                        ; lab(1090, 452, "hand-off", "middle", "egress")
path("M 1156,590 H 1260", "egress")                                    ; lab(1206, 582, "Web SDK", "middle", "egress")
path("M 510,710 H 1236 Q 1244,710 1244,702 V 688 Q 1244,680 1252,680 H 1260", "egress") ; lab(860, 702, "sign-in", "middle", "egress")
path("M 1355,388 V 342", "intra", dashed=True)                         ; lab(1361, 368, "registration events", kind="intra")
path("M 1448,318 H 1484 Q 1492,318 1492,310 V 168 Q 1492,160 1484,160 H 173 Q 165,160 165,168 V 248", "egress")
lab(830, 152, "confirmations · reminders · alerts → fans", "middle", "egress")

doc = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NFL Events Hub Architecture</title>
<link href="https://fonts.googleapis.com/css2?family=Source+Sans+3:ital,wght@0,400;0,600;0,700;1,400&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{ background:#fff; font-family:'Source Sans 3',Calibri,system-ui,sans-serif; color:#222; }}
  .wrap {{ width:100%; overflow-x:auto; }}
  .slide {{ position:relative; width:{W}px; height:{H}px; margin:0 auto; background:#f7f7f7; overflow:hidden; }}
  .over {{ position:absolute; left:60px; top:34px; font-size:16px; color:#555; }}
  h1 {{ position:absolute; left:60px; top:54px; font-size:34px; font-weight:400; color:#e0533a; letter-spacing:-0.01em; }}
  .b {{ position:absolute; }}
  .band {{ background:#dcdcdc; }} .band span {{ position:absolute; top:4px; font-size:11px; font-weight:600; letter-spacing:0.06em; color:#444; }}
  .src {{ background:#e6e6e6; border-radius:6px; padding:10px 8px; }}
  .st {{ font-size:12px; font-weight:600; color:#444; text-align:center; margin-bottom:12px; }}
  .ci {{ display:flex; flex-direction:column; align-items:center; gap:4px; margin-bottom:34px; text-align:center; }}
  .ci span {{ font-size:12px; font-weight:600; line-height:1.2; }} .ci i {{ font-weight:400; font-size:10.5px; color:#555; }}
  .dark {{ background:#3a3a3a; color:#fff; border-radius:4px; font-size:13px; font-weight:600; display:flex; align-items:center; justify-content:center; gap:8px; }}
  .dark .mk {{ width:18px; height:18px; border-radius:3px; }}
  .mw {{ flex-direction:column; justify-content:center; text-align:center; padding:10px; gap:6px; }}
  .mw b {{ font-size:14px; }} .mw i {{ font-size:11.5px; font-weight:400; line-height:1.35; color:#e8e8e8; }}
  .mw .mk {{ position:absolute; left:8px; top:8px; }}
  .outer {{ border:1.5px solid #4a4a4a; border-radius:10px; }}
  .gold {{ border:2.5px solid #e9b63b; border-radius:10px; }}
  .panel {{ background:#3a3a3a; border-radius:5px; }}
  .ph {{ color:#fff; font-size:13px; font-weight:600; display:flex; align-items:center; justify-content:center; }}
  .item {{ background:#fff; border-radius:3px; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; padding:2px 6px; }}
  .item b {{ font-size:12.5px; font-weight:600; line-height:1.15; }} .item i {{ font-size:10.5px; color:#555; line-height:1.2; }}
  .src .item, .b.item {{ box-shadow:0 0 0 1px #c9c9c9; }}
  .model {{ background:#e9e9e9; border:1px solid #cfcfcf; border-radius:4px; font-size:12px; color:#333; display:flex; align-items:center; justify-content:center; gap:10px; }}
  .model b {{ color:#222; }}
  .foot {{ display:flex; align-items:center; gap:12px; font-size:17px; color:#444; }}
  .foot img {{ width:34px; height:34px; border-radius:5px; }}
  .key {{ position:absolute; left:1250px; top:786px; font-size:12.5px; color:#444; }}
  .key div {{ display:flex; align-items:center; gap:8px; margin-top:4px; }}
  .key svg {{ width:34px; height:8px; }}
  svg.conn {{ position:absolute; left:0; top:0; }}
  svg.conn > path {{ fill:none; stroke-width:1.6; }}
  path.ingress {{ stroke:#3b74c4; }} path.intra {{ stroke:#8a8a8a; }} path.egress {{ stroke:#d0402b; }}
  svg.conn text {{ font-size:11px; paint-order:stroke; stroke:#f7f7f7; stroke-width:4px; fill:#444; }}
  text.ingress {{ fill:#3b74c4; }} text.egress {{ fill:#c0392b; }} text.intra {{ fill:#666; }}
</style></head>
<body><div class="wrap"><div class="slide" role="img" aria-label="NFL Events Hub platform architecture">
<div class="over">Overall platform flow</div>
<h1>NFL Events Hub Platform Architecture</h1>
{''.join(B)}
<svg class="conn" width="{W}" height="{H}" aria-hidden="true">
  <defs>
    <marker id="m-ingress" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="#3b74c4"/></marker>
    <marker id="m-intra" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="#8a8a8a"/></marker>
    <marker id="m-egress" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="#d0402b"/></marker>
  </defs>
  {''.join(P)}{''.join(L)}
</svg>
<div class="key"><b>Diagram Key</b>
  <div><svg><line x1="0" y1="4" x2="34" y2="4" stroke="#3b74c4" stroke-width="2"/></svg>Ingress flow</div>
  <div><svg><line x1="0" y1="4" x2="34" y2="4" stroke="#8a8a8a" stroke-width="2" stroke-dasharray="5 4"/></svg>Intra-system flow</div>
  <div><svg><line x1="0" y1="4" x2="34" y2="4" stroke="#d0402b" stroke-width="2"/></svg>Egress flow</div>
</div>
</div></div></body></html>
"""
open(f"{OUT}/nfl-events-hub-aep-style.html", "w").write(doc)
print("ok")
