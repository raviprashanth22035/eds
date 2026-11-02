"""NFL Events Hub — platform overview slide (Splunk-style: needs | diagram | EDS checklist), 16:9.

Usage: python3 overview_slide.py <output-dir>
"""
import sys, os, base64, html

OUT = sys.argv[1]
ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
with open(os.path.join(ASSETS, "adobe-mark-crop.png"), "rb") as f:
    AMARK = "data:image/png;base64," + base64.b64encode(f.read()).decode()
def _svg(n):
    with open(os.path.join(ASSETS, n), "rb") as fh:
        return "data:image/svg+xml;base64," + base64.b64encode(fh.read()).decode()
AWSMARK, AWS_LAMBDA, AWS_APIGW, AWS_SECRETS = (_svg(n) for n in ("aws-cloud-logo.svg", "aws-lambda.svg", "aws-api-gateway.svg", "aws-secrets-manager.svg"))
e = html.escape
W, H = 1600, 900

PERSON = ('<svg viewBox="0 0 48 48" width="34" height="34" aria-hidden="true"><circle cx="24" cy="15" r="8" fill="#ffd8a8" stroke="#3b3b3b" stroke-width="1.5"/>'
          '<path d="M10 40c0-8 6-13 14-13s14 5 14 13z" fill="#3a6ea5" stroke="#3b3b3b" stroke-width="1.5"/></svg>')
GH = ('<svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><path fill="#24292f" d="M12 .5a11.5 11.5 0 0 0-3.6 22.4c.6.1.8-.3.8-.6v-2c-3.2.7-3.9-1.5-3.9-1.5-.5-1.3-1.3-1.7-1.3-1.7-1-.7.1-.7.1-.7 1.2.1 1.8 1.2 1.8 1.2 1 1.8 2.8 1.3 3.5 1 .1-.8.4-1.3.8-1.6-2.6-.3-5.3-1.3-5.3-5.7 0-1.3.5-2.3 1.2-3.1-.1-.3-.5-1.5.1-3.1 0 0 1-.3 3.2 1.2a11 11 0 0 1 5.8 0c2.2-1.5 3.2-1.2 3.2-1.2.6 1.6.2 2.8.1 3.1.7.8 1.2 1.8 1.2 3.1 0 4.4-2.7 5.4-5.3 5.7.4.4.8 1.1.8 2.2v3.2c0 .3.2.7.8.6A11.5 11.5 0 0 0 12 .5z"/></svg>')


def box(x, y, w, h, cls, inner, style=""):
    return f'<div class="b {cls}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;{style}">{inner}</div>'


def zone(x, y, w, h, label, cls=""):
    return box(x, y, w, h, f"zone {cls}", f'<div class="zl">{e(label)}</div>')


def node(x, y, w, h, cls, title, sub="", mark=False):
    m = f'<img class="mark" src="{mark if isinstance(mark, str) else AMARK}" alt="">' if mark else ""
    s = f'<div class="s">{e(sub)}</div>' if sub else ""
    return box(x, y, w, h, f"n {cls}", f'{m}<div class="t">{e(title)}</div>{s}')


def person(x, y, name):
    return box(x, y, 76, 64, "person", f'{PERSON}<div class="t">{e(name)}</div>')


D = []
# zones
D.append(zone(470, 150, 140, 254, "AUTHORING", "pink"))
D.append(zone(650, 150, 120, 110, "CONTENT STORAGE", "sand"))
D.append(zone(790, 150, 410, 110, "EDS RUNTIME + DELIVERY", "blue"))
D.append(zone(790, 300, 410, 96, "ENVIRONMENTS", "sand"))
D.append(zone(790, 430, 410, 110, "MIDDLEWARE API · AWS", "grey"))
D.append(zone(462, 440, 162, 150, "DEVELOPMENT", "grey"))
# people
D.append(person(386, 172, "Club & league authors"))
D.append(person(386, 486, "Dev team"))
# authoring chips
for i, t in enumerate(["Document Authoring", "Universal Editor", "Registration Forms", "Club & league event feeds"]):
    D.append(node(482, 178 + i * 54, 116, 42, "chip", t))
# storage + runtime
D.append(node(660, 178, 100, 66, "store", "Content & media bus", "EDS"))
D.append(node(800, 178, 116, 56, "run", "EDS runtime", "content + code", True))
D.append(node(930, 178, 116, 56, "run", "Adobe CDN", "edge cache · WAF", True))
D.append(node(1060, 178, 130, 56, "site", "events.nfl.com", "web · OnePass · NFL App"))
# environments
D.append(node(800, 328, 170, 52, "store", "Preview", "*.aem.page · authors review"))
D.append(node(1020, 328, 170, 52, "store", "Live", "*.aem.live · CDN-cached"))
# middleware
D.append(node(800, 460, 390, 62, "ours", "API Gateway → Lambda (Node.js)", "/api/* routed by Adobe CDN · Secrets Manager · stateless, no fan data", AWSMARK))
# github
D.append(node(474, 470, 140, 44, "gh", "GitHub · EDS blocks", "JavaScript · CSS"))
D.append(node(474, 532, 140, 44, "gh", "GitHub · middleware", "Node.js · CI/CD to AWS"))

P, L = [], []


def path(d, cls="", dashed=False):
    a = ' stroke-dasharray="5 4"' if dashed else ""
    P.append(f'<path class="{cls}" d="{d}"{a} marker-end="url(#ah{"b" if cls=="lnk" else ""})"/>')


def lab(x, y, t, anchor="start", cls=""):
    L.append(f'<text class="{cls}" x="{x}" y="{y}" text-anchor="{anchor}">{e(t)}</text>')


path("M 462,204 H 468")
path("M 610,212 H 648")                         ; lab(629, 204, "publish", "middle")
path("M 770,206 H 798")
path("M 916,206 H 928")
path("M 1046,206 H 1058")
# content preview -> live
path("M 712,244 V 346 Q 712,354 720,354 H 798", dashed=True) ; lab(756, 346, "preview", "middle")
path("M 970,354 H 1018")                        ; lab(994, 346, "go live", "middle")
# code sync: GitHub blocks -> runtime (over the top)
path("M 614,492 H 622 Q 630,492 630,484 V 148 Q 630,140 638,140 H 850 Q 858,140 858,148 V 176", dashed=True)
lab(636, 420, "code sync")
# deploy: GitHub middleware -> Node.js API
path("M 614,554 H 700 Q 708,554 708,546 V 500 Q 708,492 716,492 H 798", dashed=True) ; lab(756, 484, "deploy", "middle")
# CDN routes /auth to middleware
path("M 462,516 H 472")

NEEDS = ["One platform for league, club & international events",
         "Free registration & ticketed events",
         "Guest & signed-in registration with entry QR",
         "Embedded in NFL OnePass & the NFL App",
         "Club & market content in local languages",
         "Fast at peak event moments"]
EDS = ["Blocks in JavaScript & CSS — no Java backend",
       "Document Authoring or Universal Editor",
       "Publish in seconds · Adobe CDN edge delivery",
       "Stateless middleware on AWS · no fan data stored",
       "Preview & live environments for every change",
       "Independent dev / test / release via GitHub"]
needs = "".join(f"<li>{e(t)}</li>" for t in NEEDS)
eds = "".join(f"<li>{e(t)}</li>" for t in EDS)

doc = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NFL Events Hub Platform Overview</title>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@500&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{ background:#fff; font-family:'IBM Plex Sans',system-ui,sans-serif; color:#14171f; }}
  .wrap {{ width:100%; overflow-x:auto; }}
  .slide {{ position:relative; width:{W}px; height:{H}px; margin:0 auto; background:#fff; }}
  h1 {{ position:absolute; left:0; width:100%; text-align:center; top:34px; font-size:40px; font-weight:700; letter-spacing:-0.02em; }}
  .col {{ position:absolute; top:190px; }}
  .col h2 {{ font-size:26px; font-weight:700; color:#d50a0a; margin-bottom:18px; }}
  .col ul {{ list-style:none; display:grid; gap:16px; }}
  .col li {{ font-size:19px; line-height:1.3; position:relative; padding-left:30px; }}
  .needs li::before {{ content:""; position:absolute; left:4px; top:9px; width:8px; height:8px; border-radius:50%; background:#d50a0a; }}
  .eds li::before {{ content:"✓"; position:absolute; left:0; top:-1px; font-weight:700; }}
  .frame {{ position:absolute; left:368px; top:130px; width:850px; height:530px; border:2px solid #e8a3c9; border-radius:4px; }}
  .dg {{ position:absolute; left:0; top:32px; width:{W}px; height:{H}px; }}
  .b {{ position:absolute; border-radius:5px; }}
  .zone {{ border:1px dashed #c9ccd4; }}
  .zone.pink {{ background:#fdeeee; border-color:#f2c2c8; }} .zone.sand {{ background:#fbf6e6; border-color:#ebdcae; }}
  .zone.blue {{ background:#eef5fd; border-color:#c6d8ef; }} .zone.grey {{ background:#f6f7f9; }}
  .zl {{ position:absolute; left:0; width:100%; top:6px; text-align:center; font-family:'IBM Plex Mono',monospace; font-size:8.5px; font-weight:500; letter-spacing:0.1em; color:#6b7385; }}
  .n {{ background:#fff; border:1px solid #c9ccd4; padding:6px 8px; text-align:center; display:flex; flex-direction:column; justify-content:center; }}
  .n .t {{ font-size:11.5px; font-weight:600; line-height:1.2; }} .n .s {{ font-size:9.5px; color:#5b6375; margin-top:2px; line-height:1.2; }}
  .n .mark {{ position:absolute; left:-8px; top:-9px; width:18px; height:18px; border-radius:3px; }}
  .chip {{ border-style:dashed; }}
  .store {{ background:#fff8e1; }} .run {{ background:#fde7e7; border-color:#f2c2c8; }}
  .site {{ background:#dff0ff; border-color:#8fb8e8; }}
  .gh {{ background:#f3f0ff; border-color:#c9bdf2; }}
  .ours {{ background:#fde7e7; border:1.5px solid #d50a0a; }}
  .nfl {{ background:#e7ecf8; border-color:#b8c6e6; }} .adobe {{ background:#fde7e7; border-color:#f2c2c8; }} .tm {{ background:#dceaff; border-color:#b5cdf2; }}
  .person {{ display:flex; flex-direction:column; align-items:center; text-align:center; }}
  .person .t {{ font-size:9.5px; font-weight:600; line-height:1.15; margin-top:2px; }}
  svg.conn {{ position:absolute; left:0; top:0; }}
  svg.conn > path {{ fill:none; stroke:#5b6375; stroke-width:1.3; }}
  svg.conn > path.lnk {{ stroke:#2e5aa8; }}
  svg.conn text {{ font-family:'IBM Plex Mono',monospace; font-size:9px; fill:#444; paint-order:stroke; stroke:#fff; stroke-width:3px; }}
  svg.conn text.lnk {{ fill:#2e5aa8; }}
</style></head>
<body><div class="wrap"><div class="slide" role="img" aria-label="NFL Events Hub on EDS platform overview">
<h1>NFL Events Hub on EDS: Platform Overview</h1>
<div class="dg">
<div class="col needs" style="left:40px;width:300px"><h2>What NFL needs</h2><ul>{needs}</ul></div>
<div class="frame"></div>
<svg class="conn" width="{W}" height="{H}" aria-hidden="true">
  <defs>
    <marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="#5b6375"/></marker>
    <marker id="ahb" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="#2e5aa8"/></marker>
  </defs>
</svg>
{''.join(D)}
<svg class="conn" width="{W}" height="{H}" aria-hidden="true">
  <defs>
    <marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="#5b6375"/></marker>
    <marker id="ahb" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="#2e5aa8"/></marker>
  </defs>
  {''.join(P)}{''.join(L)}
</svg>
<div class="col eds" style="left:1250px;width:320px"><h2>How EDS delivers</h2><ul>{eds}</ul></div>
</div>
</div></div></body></html>
"""
open(f"{OUT}/nfl-events-hub-overview-slide.html", "w").write(doc)
print("ok")
