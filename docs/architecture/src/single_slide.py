"""NFL Events Hub — platform & integrations (client version) in the Adobe 'how it works' look.

Usage: python3 single_slide.py <output-dir>
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
    return box(x, y, 232, 44, "blk", f'<div class="t">{e(title)}</div><div class="s">{e(sub)}</div>')


def chan(x, y, icon, title, sub):
    svg = (f'<svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="#3b3b3b" stroke-width="1.7" '
           f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICON[icon]}</svg>')
    return box(x, y, 232, 64, "chan", f'{svg}<div><div class="t">{e(title)}</div><div class="s">{e(sub)}</div></div>')


B = []
# zones
B.append(zone(104, 236, 264, 264, "EXPERIENCE CHANNELS"))
B.append(zone(1064, 236, 512, 128, "TICKETING PARTNERS"))
B.append(zone(1064, 388, 512, 216, "ADOBE EXPERIENCE CLOUD"))
B.append(zone(1064, 616, 512, 168, "REGISTRATION, IDENTITY & WALLET"))
# channels
B.append(chan(120, 262, "phone", "NFL OnePass", "embedded hub"))
B.append(chan(120, 342, "app", "NFL App", "embedded hub"))
B.append(chan(120, 422, "laptop", "Web", "events.nfl.com"))
# edge + authoring
# hub
B.append(box(480, 172, 520, 428, "panel hub", f'<img class="mark" src="{AMARK}" alt=""><div class="pt">NFL Events Hub<span>events.nfl.com · AEM Edge Delivery Services</span></div>'))
B.append(box(500, 232, 480, 44, "model", '<b>UNIFIED<br>EVENT MODEL</b><span>League · Club · International<br>Free · Paid · Ticketed · Registration</span>'))
discover = [("Event Discovery", "league, club & international"), ("Location Search", "events near me"),
            ("Event Detail", "venue, schedule, FAQ"), ("Search & Filter", "indexed event catalog"),
            ("Calendar", "add to calendar")]
attend = [("Registration", "guest & authenticated"), ("Ticketing", "hand-off to Ticketmaster"),
          ("My Events", "authenticated · wallet"), ("Entry QR", "email · My Events · wallet"),
          ("Event Alerts", "status & cancellations")]
for i, (t, s_) in enumerate(discover):
    B.append(mini(500, 290 + i * 50, t, s_))
for i, (t, s_) in enumerate(attend):
    B.append(mini(748, 290 + i * 50, t, s_))
B.append(box(500, 546, 480, 38, "pers", '<div class="t">Personalization · contextual for all · profile-based when signed in · consent-gated</div>'))
# integration layer
B.append(box(480, 640, 520, 120, "adobe aws", f'<img class="mark" src="{AWSMARK}" alt=""><div class="t">Middleware API · AWS <em>stateless · no fan data stored · static egress IP</em></div>'
             f'<div class="svc"><span><img src="{AWS_APIGW}" alt="">Amazon API Gateway</span><span><img src="{AWS_LAMBDA}" alt="">AWS Lambda · Node.js</span><span><img src="{AWS_SECRETS}" alt="">AWS Secrets Manager</span></div>'
             '<div class="mwr"><span>/api/register</span><span>/api/session · NFL ID</span><span>/api/wallet</span></div>'))
# right side
B.append(tile(1088, 260, 464, 44, "tm", "Ticketmaster", "primary ticketing"))
B.append(tile(1088, 312, 464, 44, "tm", "On Location", "official hospitality"))
B.append(adobe(1088, 412, 464, 52, "Journey Optimizer · Campaign", "reminders · updates · cancellations — email & SMS"))
B.append(adobe(1088, 538, 464, 52, "Adobe Target · Real-Time CDP", "contextual & profile-based personalization"))
B.append(tile(1088, 628, 464, 44, "reg", "NFL Event Registration", "registration · entry QR"))
B.append(tile(1088, 678, 464, 44, "nfl", "NFL ID", "identity · single sign-on"))
B.append(tile(1088, 728, 464, 44, "wal", "Apple Wallet · Google Wallet", "event passes"))

B.append(box(104, 56, 1472, 88, "band", '<div class="bl">BUILD &amp; PUBLISH</div>'
           '<div class="grp"><b>Club &amp; league authors</b><span>Document Authoring</span><span>Universal Editor</span><span>Registration Forms</span><span>Club &amp; league event feeds</span></div>'
           '<div class="grp"><b>Dev team · GitHub</b><span>EDS blocks · JS/CSS</span><span>Middleware code</span></div>'
           '<div class="arr">→</div><div class="env"><b>Preview</b><small>*.aem.page</small></div><div class="arr">→</div><div class="env"><b>Live</b><small>*.aem.live</small></div>'))
B.append(box(104, 790, 1472, 34, "foot", '<span>JavaScript &amp; CSS blocks — no Java backend</span><span>Publish in seconds</span><span>Stateless middleware on AWS — no fan data stored</span><span>Independent releases via GitHub</span>'))

P, LAB = [], []


def path(d, cls="", dashed=False, thick=False):
    a = ' stroke-dasharray="6 5"' if dashed else ""
    m = {"acc": "ahr", "lnk": "ahb"}.get(cls, "ah")
    c = f'{cls} thick' if thick else cls
    P.append(f'<path class="{c}" d="{d}"{a} marker-end="url(#{m})"/>')


def lab(x, y, t, anchor="start", cls=""):
    LAB.append(f'<text class="{cls}" x="{x}" y="{y}" text-anchor="{anchor}">{e(t)}</text>')


for y in (294, 374, 454):
    path(f"M 352,{y} H 478")
lab(424, 284, "HTTPS", "middle")
lab(424, 330, "via Adobe CDN", "middle")
path("M 740,144 V 170", thick=True)                      ; lab(748, 162, "Publish")
path("M 740,600 V 638", "acc")                           ; lab(748, 624, "/api/* · via Adobe CDN", cls="acc")
path("M 1000,282 H 1086", "lnk", dashed=True)
path("M 1000,334 H 1086", "lnk", dashed=True)            ; lab(1043, 312, "Hand-off", "middle", "lnk")
path("M 1000,564 H 1086", "lnk", dashed=True)            ; lab(1043, 556, "Web SDK", "middle", "lnk")
path("M 1000,650 H 1086", "lnk")                         ; lab(1043, 642, "Register", "middle", "lnk")
path("M 1000,700 H 1086", "lnk")                         ; lab(1043, 692, "Sign in", "middle", "lnk")
path("M 1000,750 H 1086", "lnk")                         ; lab(1043, 742, "Wallet", "middle", "lnk")
path("M 1552,650 H 1560 Q 1568,650 1568,642 V 446 Q 1568,438 1560,438 H 1554", "lnk", dashed=True)
lab(1560, 520, "Events", "end", "lnk")

doc = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NFL Events Hub Platform</title>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;600&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{ background:#fff; font-family:'IBM Plex Sans',system-ui,sans-serif; color:#1b1f2a; }}
  .wrap {{ width:100%; overflow-x:auto; }}
  .slide {{ position:relative; width:{W}px; height:{H}px; margin:0 auto; background:#fff; }}
  h1 {{ position:absolute; left:0; width:100%; text-align:center; top:26px; font-size:26px; font-weight:600; letter-spacing:-0.01em; }}
  h1 span {{ display:block; font-size:14px; font-weight:400; color:#5b6375; margin-top:6px; }}
  .col {{ position:absolute; top:256px; font-size:10.5px; font-weight:600; letter-spacing:0.12em; color:#666; }}
  .b {{ position:absolute; border-radius:6px; }}
  .zone {{ border:1px solid #dcdfe6; background:transparent; }}
  .zl {{ position:absolute; left:12px; top:-8px; background:#fff; padding:0 6px; font-family:'IBM Plex Mono',monospace; font-size:10px; font-weight:600; letter-spacing:0.12em; color:#6b7385; }}
  .adobe {{ background:#fbd3d3; padding:12px 14px; }}
  .adobe .mark, .hub .mark {{ position:absolute; left:-12px; top:-14px; width:30px; height:30px; border-radius:4px; }}
  .adobe .t {{ font-size:15px; font-weight:600; }}
  .adobe .s {{ font-size:11.5px; color:#444; margin-top:4px; line-height:1.35; }}
  .item {{ background:#fff; border-radius:4px; font-size:12px; padding:8px 10px; margin-top:10px; }}
  .panel {{ background:#eef0f4; }} .hub {{ border:2px solid #e1251b; }}
  .pt {{ position:absolute; left:20px; top:12px; font-size:17px; font-weight:600; }}
  .pt span {{ display:block; font-size:11.5px; font-weight:400; color:#444; margin-top:2px; }}
  .model {{ background:#2d3142; color:#f5f5f5; display:flex; align-items:center; gap:16px; padding:0 16px; }}
  .model b {{ font-size:10.5px; letter-spacing:0.14em; line-height:1.4; border-right:1px solid rgba(255,255,255,0.35); padding-right:16px; }}
  .model span {{ font-family:'IBM Plex Sans',sans-serif; font-size:11.5px; line-height:1.4; }}
  .blk {{ background:#fff; padding:5px 12px; border:1px solid #e1e4ea; }}
  .blk .t, .tile .t {{ font-size:12.5px; font-weight:600; }}
  .blk .s, .tile .s {{ font-size:11px; color:#555; margin-top:2px; }}
  .pers {{ background:#fde7e7; border:1.5px solid #e1251b; display:flex; align-items:center; justify-content:center; }}
  .pers .t {{ font-size:13px; font-weight:600; }}
  .tile {{ padding:8px 12px; border:1.5px solid rgba(0,0,0,0.12); }}
  .nfl {{ background:#dfe6f6; }} .reg {{ background:#e9e0ff; }} .tm {{ background:#dceaff; }} .wal {{ background:#fff3d6; }}
  .chan {{ background:#eef0f4; display:flex; align-items:center; gap:10px; padding:8px 12px; }}
  .chan .t {{ font-size:13px; font-weight:600; }} .chan .s {{ font-size:10.5px; color:#555; margin-top:2px; }}
  svg.conn {{ position:absolute; left:0; top:0; }}
  svg.conn > path {{ fill:none; stroke:#4a4a4a; stroke-width:1.8; }}
  svg.conn > path.thick {{ stroke-width:3; }}
  svg.conn > path.acc {{ stroke:#c11a12; stroke-width:2.2; }}
  svg.conn > path.lnk {{ stroke:#2e5aa8; }}
  svg.conn text {{ font-family:'IBM Plex Mono',monospace; font-size:12px; fill:#333; paint-order:stroke; stroke:#fff; stroke-width:4px; }}
  svg.conn text.acc {{ fill:#c11a12; }} svg.conn text.lnk {{ fill:#2e5aa8; }}
  .foot {{ position:absolute; left:24px; top:836px; font-size:11.5px; color:#7a8294; }}
  .band {{ border:1px solid #f2c2c8; background:#fff6f6; display:flex; align-items:center; gap:14px; padding:16px 18px 10px; }}
  .band .bl {{ position:absolute; left:12px; top:-8px; background:#fff; padding:0 6px; font-family:'IBM Plex Mono',monospace; font-size:10px; font-weight:600; letter-spacing:0.12em; color:#c11a12; }}
  .band .grp {{ display:flex; align-items:center; gap:6px; }}
  .band .grp b {{ font-size:12.5px; margin-right:4px; white-space:nowrap; }}
  .band span {{ background:#fff; border:1px solid #f2c2c8; border-radius:4px; padding:5px 8px; font-size:11.5px; white-space:nowrap; }}
  .band .arr {{ font-size:18px; color:#5b6375; }}
  .band .env {{ background:#fbf6e6; border:1px solid #ebdcae; border-radius:4px; padding:4px 12px; text-align:center; }}
  .band .env b {{ display:block; font-size:12.5px; }} .band .env small {{ font-size:10.5px; color:#5b6375; }}
  .foot {{ display:flex; justify-content:space-between; gap:10px; }}
  .foot span {{ flex:1; text-align:center; background:#f3f4f7; border-radius:4px; padding:7px 8px; font-size:12.5px; font-weight:500; color:#2d3142; }}
  .foot span::before {{ content:"✓ "; color:#c11a12; font-weight:700; }}
  .aws {{ background:#fff0e0; box-shadow:inset 0 0 0 1px #f0c89a; }}
  .aws .t em {{ font-style:normal; font-weight:400; font-size:11.5px; color:#6b5a48; margin-left:8px; }}
  .svc {{ display:flex; gap:16px; margin-top:10px; font-size:12px; font-weight:600; color:#232f3e; }}
  .svc span {{ display:flex; align-items:center; gap:6px; }} .svc img {{ width:22px; height:22px; border-radius:3px; }}
  .mwr {{ display:flex; gap:8px; margin-top:8px; }}
  .mwr span {{ background:#fff; border-radius:4px; padding:6px 10px; font-size:12px; }}
  .chips {{ display:flex; gap:6px; margin-top:8px; flex-wrap:nowrap; }}
  .chips span {{ background:#fff; border-radius:4px; padding:5px 8px; font-size:11px; white-space:nowrap; }}
  .dg {{ position:absolute; left:0; top:62px; width:{W}px; height:{H}px; }}
  .legend {{ position:absolute; left:24px; top:800px; display:flex; gap:26px; font-size:11px; color:#444; align-items:center; }}
  .legend i {{ display:inline-block; width:26px; height:0; border-top:2px solid #4a4a4a; margin-right:8px; vertical-align:middle; }}
  .legend i.acc {{ border-color:#c11a12; }} .legend i.lnk {{ border-color:#2e5aa8; }} .legend i.dash {{ border-top-style:dashed; }}
  .legend b {{ display:inline-block; width:14px; height:12px; margin-right:8px; vertical-align:middle; border-radius:2px; }}
</style></head>
<body><div class="wrap"><div class="slide" role="img" aria-label="NFL Events Hub platform and integrations">
<h1>NFL Events Hub — Platform Architecture<span>One event platform for web, NFL OnePass and the NFL App — built on AEM Edge Delivery Services</span></h1>
<div class="dg">
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
</div>
</div></div></body></html>
"""
open(f"{OUT}/nfl-events-hub-single-slide.html", "w").write(doc)
print("ok")
