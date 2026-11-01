"""NFL Events Hub — client-friendly platform map (same layout as eds_map.py, plain language, numbered story).

Usage: python3 eds_story.py <output-dir>
"""
import sys, os, base64, html

OUT = sys.argv[1]
ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
with open(os.path.join(ASSETS, "adobe-mark-crop.png"), "rb") as f:
    AMARK = "data:image/png;base64," + base64.b64encode(f.read()).decode()
e = html.escape

PERSON = ('<svg viewBox="0 0 48 48" width="44" height="44" aria-hidden="true"><circle cx="24" cy="15" r="8" fill="#ffd8a8" stroke="#3b3b3b" stroke-width="1.5"/>'
          '<path d="M10 40c0-8 6-13 14-13s14 5 14 13z" fill="#3a6ea5" stroke="#3b3b3b" stroke-width="1.5"/>'
          '<rect x="15" y="33" width="18" height="10" rx="1.5" fill="#6b6b6b" stroke="#3b3b3b" stroke-width="1.2"/></svg>')


def box(x, y, w, h, cls, inner):
    return f'<div class="b {cls}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px">{inner}</div>'


def adobe(x, y, w, h, title, sub="", items=()):
    its = "".join(f'<div class="item">{e(i)}</div>' for i in items)
    s = f'<div class="s">{e(sub)}</div>' if sub else ""
    return box(x, y, w, h, "adobe", f'<img class="mark" src="{AMARK}" alt=""><div class="t">{e(title)}</div>{s}{its}')


def tile(x, y, w, h, cls, title, sub):
    return box(x, y, w, h, f"tile {cls}", f'<div class="t">{e(title)}</div><div class="s">{e(sub)}</div>')


def group(x, y, w, h, title, items):
    lis = "".join(f'<li>{e(i)}</li>' for i in items)
    return box(x, y, w, h, "grp", f'<div class="t">{e(title)}</div><ul>{lis}</ul>')


def bar(x, y, w, h, cls, title, sub):
    return box(x, y, w, h, f"barx {cls}", f'<div class="t">{e(title)}</div><div class="s">{e(sub)}</div>')


def person(x, y, name, sub=""):
    s = f'<div class="s">{e(sub)}</div>' if sub else ""
    return box(x, y, 112, 104, "person", f'{PERSON}<div class="t">{e(name)}</div>{s}')


B = []
B.append(person(24, 326, "Fans", "web · OnePass · NFL App"))
B.append(adobe(170, 60, 270, 214, "Adobe CDN", "", ["Fast, secure pages worldwide",
                                                   "Short campaign links (/draftaccess)",
                                                   "Right country & language site"]))
B.append(adobe(740, 190, 260, 90, "AEM authoring", "teams create & publish events"))
B.append(person(1150, 214, "Club & league teams"))
B.append(adobe(170, 356, 220, 112, "Secure registration & sign-in", "guest or NFL ID · stores no fan data"))
B.append(tile(170, 540, 140, 64, "leap", "Registration", "OnePass · QR code"))
B.append(tile(320, 540, 120, 64, "nfl", "NFL ID", "one fan account"))
B.append(adobe(200, 860, 270, 72, "Journey Optimizer · Campaign", "confirmations · reminders · alerts"))
# the hub
B.append(box(480, 318, 540, 392, "panel hub", f'<img class="mark" src="{AMARK}" alt=""><div class="pt">NFL Events Hub · events.nfl.com<span>one event platform on AEM Edge Delivery Services</span></div>'))
B.append(group(500, 384, 240, 168, "Discover", ["Find league, club & international events", "Event details & venue map", "Events near me", "Calendar & schedule"]))
B.append(group(760, 384, 240, 168, "Attend", ["Register as guest or signed in", "Guest: QR code by email", "Signed in: My Events + wallet", "Buy tickets · live alerts"]))
B.append(bar(500, 566, 500, 52, "pers", "Personalized for signed-in fans", "based on the NFL ID profile · guests see the standard page"))
B.append(bar(500, 630, 500, 56, "run", "Run by clubs & league", "event sheets · club × market roll-out · languages · short links"))
# partners on the right
B.append(tile(1100, 400, 240, 56, "tm", "Ticketmaster · On Location", "buy tickets · hospitality"))
B.append(adobe(1100, 564, 240, 56, "Adobe Target · RT-CDP", "personalization"))

P, LAB, BAD = [], [], []


def path(d, dashed=False, both=False, thick=False):
    a = ' stroke-dasharray="6 5"' if dashed else ""
    s = ' marker-start="url(#ah)"' if both else ""
    P.append(f'<path d="{d}" stroke-width="{3 if thick else 1.8}"{a}{s} marker-end="url(#ah)"/>')


def lab(x, y, t, anchor="start"):
    LAB.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}">{e(t)}</text>')


def badge(x, y, n):
    BAD.append(f'<circle cx="{x}" cy="{y}" r="11" fill="#e1251b"/><text x="{x}" y="{y + 4}" class="n">{n}</text>')


path("M 1150,268 H 1002")                                ; lab(1076, 258, "create", "middle")        ; badge(1076, 284, 1)
path("M 870,280 V 316", thick=True)                      ; lab(880, 302, "publish")
path("M 80,326 V 188 Q 80,180 88,180 H 168")             ; lab(92, 250, "open the hub")             ; badge(60, 250, 2)
path("M 440,150 H 592 Q 600,150 600,158 V 316")          ; lab(520, 142, "fast pages", "middle")     ; badge(520, 168, 3)
path("M 478,430 H 392")                                  ; lab(435, 396, "register", "middle") ; lab(435, 412, "sign in", "middle") ; badge(435, 452, 4)
path("M 380,468 V 538")                                  ; lab(388, 504, "sign in")
path("M 230,468 V 538")                                  ; lab(238, 504, "register")                ; badge(212, 500, 5)
path("M 250,604 V 858", dashed=True)                     ; lab(258, 740, "registration events")     ; badge(232, 740, 6)
path("M 200,892 H 88 Q 80,892 80,884 V 432")             ; lab(144, 884, "email · push", "middle")
path("M 1000,428 H 1098", dashed=True)                   ; lab(1049, 420, "buy", "middle")           ; badge(1049, 446, 7)
path("M 1000,592 H 1098", dashed=True, both=True)        ; lab(1040, 584, "personalize", "middle")   ; badge(1040, 610, 8)

STEPS = ["Club & league teams create and publish events in AEM.",
         "Fans open events.nfl.com — on the web or inside OnePass and the NFL App.",
         "Adobe CDN serves fast pages in the right country and language.",
         "Fans register on the hub as a guest, or sign in with NFL ID (same account as OnePass) for one-tap registration.",
         "Registration creates the OnePass QR code. Guests get it by email; signed-in fans also see it in My Events with Add to Wallet.",
         "Confirmations, reminders and alerts go out through Journey Optimizer and Campaign.",
         "Paid events: Buy Tickets opens Ticketmaster — no payments in the hub.",
         "Signed-in fans get personalized events and offers (Adobe Target, Real-Time CDP), with their consent. Guests see the standard page."]
how = "".join(f'<li><span>{i + 1}</span>{e(t)}</li>' for i, t in enumerate(STEPS))

doc = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NFL Events Hub Platform</title>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;600&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{ background:#fff; font-family:'IBM Plex Mono',ui-monospace,monospace; color:#1f1f1f; }}
  .wrap {{ width:100%; overflow-x:auto; }}
  .slide {{ position:relative; width:1380px; height:990px; margin:0 auto; background:#fff; }}
  h1 {{ position:absolute; left:500px; top:40px; font-size:22px; font-weight:600; }}
  h1 span {{ display:block; font-size:13px; font-weight:400; color:#555; margin-top:4px; }}
  .b {{ position:absolute; border-radius:6px; }}
  .adobe {{ background:#fbd3d3; padding:12px 14px; }}
  .adobe .mark, .hub .mark {{ position:absolute; left:-12px; top:-14px; width:30px; height:30px; border-radius:4px; }}
  .adobe .t {{ font-size:15px; font-weight:600; }}
  .adobe .s {{ font-size:11.5px; color:#444; margin-top:4px; line-height:1.35; }}
  .item {{ background:#e9e9e9; border-radius:4px; font-size:11.5px; padding:8px 10px; margin-top:10px; box-shadow:2px 2px 0 #cfcfcf; }}
  .panel {{ background:#d6d6d6; }}
  .hub {{ border:2px solid #e1251b; }}
  .pt {{ position:absolute; left:20px; top:12px; font-size:17px; font-weight:600; }}
  .pt span {{ display:block; font-size:11.5px; font-weight:400; color:#444; margin-top:2px; }}
  .grp {{ background:#ececec; padding:10px 14px; box-shadow:2px 2px 0 #bdbdbd; }}
  .grp .t {{ font-size:15px; font-weight:600; margin-bottom:6px; }}
  .grp ul {{ list-style:none; display:grid; gap:7px; }}
  .grp li {{ font-family:'IBM Plex Sans',sans-serif; font-size:13px; line-height:1.3; padding-left:12px; position:relative; }}
  .grp li::before {{ content:""; position:absolute; left:0; top:7px; width:5px; height:5px; border-radius:50%; background:#e1251b; }}
  .barx {{ padding:8px 14px; box-shadow:2px 2px 0 #bdbdbd; }}
  .barx .t {{ font-size:13.5px; font-weight:600; }} .barx .s {{ font-size:11px; color:#444; margin-top:3px; }}
  .pers {{ background:#fde7e7; }} .run {{ background:#ececec; }}
  .tile {{ padding:9px 12px; border:1.5px solid rgba(0,0,0,0.12); }}
  .tile .t {{ font-size:12.5px; font-weight:600; }} .tile .s {{ font-size:11px; color:#555; margin-top:3px; }}
  .leap {{ background:#e9e0ff; }} .nfl {{ background:#dfe6f6; }} .tm {{ background:#dceaff; }}
  .ot {{ background:#dff3e3; }} .tr {{ background:#efe3f7; }}
  .person {{ background:#d9d9d9; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:2px; text-align:center; padding:6px; }}
  .person .t {{ font-size:12px; font-weight:600; line-height:1.2; }} .person .s {{ font-size:10px; color:#444; }}
  svg.conn {{ position:absolute; left:0; top:0; }}
  svg.conn > path {{ fill:none; stroke:#4a4a4a; }}
  svg.conn marker path {{ fill:#4a4a4a; stroke:none; }}
  svg.conn text {{ font-family:'IBM Plex Mono',monospace; font-size:11.5px; fill:#333; paint-order:stroke; stroke:#fff; stroke-width:4px; }}
  svg.conn text.n {{ fill:#fff; stroke:none; font-size:12px; font-weight:600; text-anchor:middle; }}
  .how {{ position:absolute; left:500px; top:740px; width:840px; }}
  .how h2 {{ font-size:14px; font-weight:600; margin-bottom:8px; }}
  .how ol {{ list-style:none; columns:2; column-gap:28px; }}
  .how li {{ font-family:'IBM Plex Sans',sans-serif; font-size:12.5px; line-height:1.35; margin-bottom:8px; display:flex; gap:8px; break-inside:avoid; }}
  .how li span {{ flex:none; width:20px; height:20px; border-radius:50%; background:#e1251b; color:#fff; font-family:'IBM Plex Mono'; font-size:11px; font-weight:600; display:grid; place-items:center; }}
  .foot {{ position:absolute; left:500px; top:948px; font-size:10.5px; color:#777; }}
</style></head>
<body><div class="wrap"><div class="slide" role="img" aria-label="NFL Events Hub platform: how fans, teams and partner systems connect">
<h1>NFL Events Hub — how it works<span>events.nfl.com (proposed) · one event platform for web, NFL OnePass and the NFL App</span></h1>
<svg class="conn" width="1380" height="990" aria-hidden="true">
  <defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z"/></marker></defs>
  {''.join(P)}
</svg>
{''.join(B)}
<svg class="conn" width="1380" height="990" aria-hidden="true">{''.join(LAB)}{''.join(BAD)}</svg>
<div class="how"><h2>How it works</h2><ol>{how}</ol></div>
<div class="foot">Target / RT-CDP licences to be confirmed with NFL.</div>
</div></div></body></html>
"""
open(f"{OUT}/nfl-events-hub-how-it-works.html", "w").write(doc)
print("ok")
