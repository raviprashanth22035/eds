"""NFL Events Hub — EDS implementation map (freeform style: CDN, EDS, authoring blocks, integrations, people).

Usage: python3 eds_map.py <output-dir>
"""
import sys, os, base64, html

OUT = sys.argv[1]
ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
with open(os.path.join(ASSETS, "adobe-mark-crop.png"), "rb") as f:
    AMARK = "data:image/png;base64," + base64.b64encode(f.read()).decode()
e = html.escape

PERSON = ('<svg viewBox="0 0 48 48" width="46" height="46" aria-hidden="true"><circle cx="24" cy="15" r="8" fill="#ffd8a8" stroke="#3b3b3b" stroke-width="1.5"/>'
          '<path d="M10 40c0-8 6-13 14-13s14 5 14 13z" fill="#3a6ea5" stroke="#3b3b3b" stroke-width="1.5"/>'
          '<rect x="15" y="33" width="18" height="10" rx="1.5" fill="#6b6b6b" stroke="#3b3b3b" stroke-width="1.2"/></svg>')


def box(x, y, w, h, cls, inner):
    return f'<div class="b {cls}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px">{inner}</div>'


def adobe(x, y, w, h, title, sub="", items=()):
    its = "".join(f'<div class="item">{e(i)}</div>' for i in items)
    s = f'<div class="s">{e(sub)}</div>' if sub else ""
    return box(x, y, w, h, "adobe", f'<img class="mark" src="{AMARK}" alt=""><div class="t">{e(title)}</div>{s}{its}')


def block(x, y, title, sub):
    return box(x, y, 240, 56, "blk", f'<div class="t">{e(title)}</div><div class="s">{e(sub)}</div>')


def tile(x, y, w, h, cls, title, sub):
    return box(x, y, w, h, f"tile {cls}", f'<div class="t">{e(title)}</div><div class="s">{e(sub)}</div>')


def person(x, y, name):
    return box(x, y, 104, 96, "person", f'{PERSON}<div class="t">{e(name)}</div>')


B = []
B.append(person(28, 330, "Fans"))
B.append(adobe(170, 60, 270, 214, "Adobe CDN", "", ["Path routing: /auth · /api → edge worker",
                                                   "301s & vanity URLs (/draftaccess)",
                                                   "Geo-IP → market & language site"]))
B.append(adobe(520, 190, 220, 90, "Edge Delivery Services", "events.nfl.com"))
B.append(adobe(170, 360, 270, 100, "Session & identity middleware", "edge worker · stateless · NFL ID session · API proxy"))
B.append(tile(170, 540, 120, 64, "leap", "Leap", "registration · QR"))
B.append(tile(320, 540, 120, 64, "nfl", "NFL ID", "SSO · one account"))
B.append(adobe(200, 860, 270, 72, "Journey Optimizer · Campaign", "confirmations · reminders · alerts"))
# authoring panel
B.append(box(480, 330, 540, 410, "panel", '<div class="pt">Document Authoring · Universal Editor</div>'))
blocks = [("Event listing & filters", "events.json · search"), ("Event detail block", "venue · map · tickets"),
          ("Registration form block", "EDS forms · extra fields"), ("Personalization block", "Target offers"),
          ("My Events block", "signed-in · QR · wallet"), ("Event alerts block", "live status banner"),
          ("Event sheets", "schedule · status · forms"), ("Authorable redirects", "vanity URLs"),
          ("Page authoring & roll-out", "league · club × market"), ("Localization", "multilingual sites")]
for i, (t, s) in enumerate(blocks):
    B.append(block(500 + (i % 2) * 260, 384 + (i // 2) * 68, t, s))
# right-side integrations
B.append(tile(1100, 384, 240, 56, "tm", "Ticketmaster · On Location", "paid tickets · hospitality"))
B.append(adobe(1100, 452, 240, 56, "Adobe Target · RT-CDP", "Web SDK · audiences"))
B.append(tile(1100, 520, 240, 56, "ot", "OneTrust", "consent & privacy"))
B.append(tile(1100, 656, 240, 56, "tr", "Translation service", "vendor to be decided"))
B.append(person(1150, 220, "Club & league authors"))

LAB = []


def lab(x, y, t, anchor="start"):
    LAB.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}">{e(t)}</text>')


P = []


def path(d, dashed=False, both=False, thick=False):
    a = ' stroke-dasharray="6 5"' if dashed else ""
    s = ' marker-start="url(#ah)"' if both else ""
    w = 3 if thick else 1.8
    P.append(f'<path d="{d}" stroke-width="{w}"{a}{s} marker-end="url(#ah)"/>')


path("M 80,330 V 188 Q 80,180 88,180 H 168")                         ; lab(90, 250, "https")
path("M 440,150 H 622 Q 630,150 630,158 V 188")                       ; lab(535, 142, "/* pages", "middle")
path("M 630,280 V 328", thick=True)
path("M 305,274 V 358")                                               ; lab(313, 320, "/auth · /api")
path("M 230,460 V 538")                                               ; lab(238, 504, "register")
path("M 380,460 V 538")                                               ; lab(388, 504, "sign-in")
path("M 500,480 H 478 Q 470,480 470,472 V 418 Q 470,410 462,410 H 442")
path("M 500,548 H 466 Q 458,548 458,540 V 444 Q 458,436 450,436 H 442")
path("M 250,604 V 858", dashed=True)                                  ; lab(258, 740, "registration events")
path("M 200,892 H 88 Q 80,892 80,884 V 428")                          ; lab(144, 884, "email · push", "middle")
path("M 1000,412 H 1098", dashed=True)                                ; lab(1049, 404, "buy", "middle")
path("M 1000,480 H 1098", dashed=True)                                ; lab(1049, 472, "web sdk", "middle")
path("M 1100,548 H 1022", dashed=True)                                ; lab(1061, 540, "consent", "middle")
path("M 1000,684 H 1098", dashed=True, both=True)                     ; lab(1049, 676, "translate", "middle")
path("M 1150,268 H 908 Q 900,268 900,276 V 328")                      ; lab(1020, 260, "author · publish", "middle")

doc = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NFL Events Hub EDS Map</title>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{ background:#fff; font-family:'IBM Plex Mono',ui-monospace,monospace; color:#1f1f1f; }}
  .wrap {{ width:100%; overflow-x:auto; }}
  .slide {{ position:relative; width:1380px; height:980px; margin:0 auto; background:#fff; }}
  h1 {{ position:absolute; left:500px; top:40px; font-size:22px; font-weight:600; }}
  h1 span {{ display:block; font-size:13px; font-weight:400; color:#555; margin-top:4px; }}
  .b {{ position:absolute; border-radius:6px; }}
  .adobe {{ background:#fbd3d3; padding:12px 14px; }}
  .adobe .mark {{ position:absolute; left:-12px; top:-14px; width:30px; height:30px; border-radius:4px; }}
  .adobe .t {{ font-size:15px; font-weight:600; }}
  .adobe .s {{ font-size:11.5px; color:#444; margin-top:4px; line-height:1.35; }}
  .item {{ background:#e9e9e9; border-radius:4px; font-size:11.5px; padding:8px 10px; margin-top:10px; box-shadow:2px 2px 0 #cfcfcf; }}
  .panel {{ background:#d6d6d6; }}
  .pt {{ position:absolute; left:20px; top:14px; font-size:15px; font-weight:600; }}
  .blk {{ background:#ececec; padding:8px 12px; box-shadow:2px 2px 0 #bdbdbd; }}
  .blk .t, .tile .t {{ font-size:12.5px; font-weight:600; }}
  .blk .s, .tile .s {{ font-size:11px; color:#555; margin-top:3px; }}
  .tile {{ padding:9px 12px; border:1.5px solid rgba(0,0,0,0.12); }}
  .leap {{ background:#e9e0ff; }} .nfl {{ background:#dfe6f6; }} .tm {{ background:#dceaff; }}
  .ot {{ background:#dff3e3; }} .tr {{ background:#efe3f7; }}
  .person {{ background:#d9d9d9; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:4px; text-align:center; padding:6px; }}
  .person .t {{ font-size:11.5px; font-weight:600; line-height:1.2; }}
  svg.conn {{ position:absolute; left:0; top:0; }}
  svg.conn > path {{ fill:none; stroke:#4a4a4a; }}
  svg.conn marker path {{ fill:#4a4a4a; stroke:none; }}
  svg.conn text {{ font-family:'IBM Plex Mono',monospace; font-size:11.5px; fill:#333; paint-order:stroke; stroke:#fff; stroke-width:4px; }}
  .note {{ position:absolute; left:500px; top:800px; width:520px; font-size:11.5px; color:#555; line-height:1.5; }}
</style></head>
<body><div class="wrap"><div class="slide" role="img" aria-label="NFL Events Hub implementation map on AEM Edge Delivery Services">
<h1>NFL Events Hub — EDS implementation map<span>events.nfl.com · embedded in NFL OnePass and the NFL App</span></h1>
<svg class="conn" width="1380" height="980" aria-hidden="true">
  <defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#4a4a4a" stroke="none"/></marker></defs>
  {''.join(P)}
</svg>
{''.join(B)}
<svg class="conn" width="1380" height="980" aria-hidden="true">{''.join(LAB)}</svg>
<div class="note">Middleware is thin and stateless: sign-in and forwarding only, no data stored. Paid tickets link out; no payments in the hub.
Leap, OneTrust and the translation vendor to be confirmed with NFL.</div>
</div></div></body></html>
"""
open(f"{OUT}/nfl-events-hub-eds-map.html", "w").write(doc)
print("ok")
