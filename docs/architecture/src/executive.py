"""NFL Events Hub — executive architecture slide (16:9).

Usage: python3 executive.py <output-dir>
"""
import sys, os, base64, html

OUT = sys.argv[1]
ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")


def _b64(n, mime):
    with open(os.path.join(ASSETS, n), "rb") as fh:
        return f"data:{mime};base64," + base64.b64encode(fh.read()).decode()


AMARK = _b64("adobe-mark-crop.png", "image/png")
AWSMARK = _b64("aws-cloud-logo.svg", "image/svg+xml")
e = html.escape
W, H = 1600, 900

ICON = {
    "phone": '<rect x="6" y="2" width="12" height="20" rx="2.5"/><path d="M10.5 18.5h3"/>',
    "app": '<rect x="6" y="2" width="12" height="20" rx="2.5"/><path d="M9 7h6M9 10.5h6M9 14h4"/>',
    "laptop": '<rect x="4" y="5" width="16" height="11" rx="1.5"/><path d="M2 19h20"/>',
    "form": '<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M9 8h6M9 12h6M9 16h3"/>',
    "id": '<circle cx="12" cy="9" r="3.5"/><path d="M5 20c1.2-3.6 3.8-5.5 7-5.5s5.8 1.9 7 5.5"/>',
    "wallet": '<rect x="3" y="6" width="18" height="13" rx="2"/><path d="M3 10h18M15 14.5h3"/>',
    "qr": '<rect x="4" y="4" width="6" height="6"/><rect x="14" y="4" width="6" height="6"/><rect x="4" y="14" width="6" height="6"/><path d="M14 14h2v2h-2zM18 18h2v2h-2zM14 18h2"/>',
}


def icon(k, size=22, color="#334155"):
    return (f'<svg viewBox="0 0 24 24" width="{size}" height="{size}" fill="none" stroke="{color}" stroke-width="1.6" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICON[k]}</svg>')


def box(x, y, w, h, cls, inner=""):
    return f'<div class="b {cls}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px">{inner}</div>'


def row(ic, title, sub):
    return f'<div class="row">{icon(ic)}<div><b>{e(title)}</b><i>{e(sub)}</i></div></div>'


B = []
# build & publish strip
B.append(box(64, 148, 1472, 44, "strip",
             '<span class="k">BUILD &amp; PUBLISH</span>'
             '<span><b>Club &amp; league authors</b> Document Authoring / Universal Editor</span><span class="sep"></span>'
             '<span><b>Developers</b> GitHub · JavaScript &amp; CSS blocks</span><span class="sep"></span>'
             '<span><b>Preview → Live</b> in seconds</span>'))
# column headers
for x, w, t in [(64, 236, "FANS"), (348, 452, "EXPERIENCE · ADOBE"), (856, 292, "SECURE API · AWS"), (1204, 332, "NFL &amp; PARTNER SYSTEMS")]:
    B.append(box(x, 212, w, 16, "colh", t))
# 1 fans
B.append(box(64, 236, 236, 340, "card c-fan",
             '<div class="rows">'
             + row("phone", "NFL OnePass", "embedded hub")
             + row("app", "NFL App", "embedded hub")
             + row("laptop", "events.nfl.com", "web")
             + '</div>'))
# 2 hub
B.append(box(348, 236, 452, 340, "card c-adobe",
             f'<img class="mark" src="{AMARK}" alt="">'
             '<div class="ht">NFL Events Hub</div>'
             '<div class="hs">AEM Edge Delivery Services · served from Adobe CDN</div>'
             '<div class="cols">'
             '<div><div class="cl">Discover</div><ul><li>League, club &amp; international</li><li>Events near me</li><li>Search, detail &amp; calendar</li></ul></div>'
             '<div><div class="cl">Attend</div><ul><li>Register — guest or signed in</li><li>Ticket hand-off</li><li>My Events · entry QR · wallet</li></ul></div>'
             '</div>'
             '<div class="pers">Personalized for every fan · profile-based when signed in</div>'))
# 3 middleware
B.append(box(856, 312, 292, 264, "card c-aws",
             f'<img class="mark" src="{AWSMARK}" alt="">'
             '<div class="ht">Middleware API</div>'
             '<div class="hs">API Gateway · Lambda · Secrets Manager</div>'
             '<div class="rows tight">'
             + row("form", "Registration", "guest & signed-in")
             + row("id", "Sign-in", "NFL ID session")
             + row("wallet", "Wallet passes", "Apple & Google")
             + '</div><div class="note">Stateless · no fan data stored</div>'))
# 4 systems
B.append(box(1204, 236, 332, 60, "card c-part slim",
             '<div><b>Ticketing partners</b><i>Ticketmaster · On Location</i></div>'))
B.append(box(1204, 312, 332, 264, "card c-nfl",
             '<div class="ht">NFL systems</div><div class="hs">remain the system of record</div>'
             '<div class="rows tight">'
             + row("qr", "NFL Event Registration", "registration · entry QR")
             + row("id", "NFL ID", "identity · single sign-on")
             + row("wallet", "Apple Wallet · Google Wallet", "event passes")
             + '</div>'))
# engagement band
B.append(box(348, 612, 1188, 76, "card band",
             f'<div class="bl"><img src="{AMARK}" alt=""><span>Adobe Experience Cloud</span></div>'
             '<div class="bi"><b>Journey Optimizer · Campaign</b><i>reminders, updates &amp; cancellations · email &amp; SMS</i></div>'
             '<div class="bi"><b>Target · Real-Time CDP</b><i>personalization for every fan</i></div>'))
# outcomes
OUTS = [("Seconds", "from author to live — no release cycle"),
        ("One platform", "league, club &amp; international events"),
        ("Zero", "fan data stored by the middleware"),
        ("Launch-day ready", "edge-cached pages at peak traffic")]
for i, (big, sub) in enumerate(OUTS):
    B.append(box(64 + i * 373, 724, 353, 92, "out", f'<b>{big}</b><i>{sub}</i>'))
# footer
B.append(box(64, 846, 1472, 24, "foot",
             '<span>Adobe — experience &amp; engagement</span><span class="dot"></span>'
             '<span>AWS — secure API layer</span><span class="dot"></span>'
             '<span>NFL — identity, registration &amp; ticketing systems of record</span>'))

P, L = [], []


def path(d, dashed=False):
    a = ' stroke-dasharray="6 5"' if dashed else ""
    P.append(f'<path d="{d}"{a} marker-end="url(#ah)"/>')


def lab(x, y, t, anchor="middle"):
    L.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}">{e(t)}</text>')


path("M 300,406 H 344")                 ; lab(324, 398, "HTTPS")
path("M 800,446 H 852")                 ; lab(826, 438, "/api")
path("M 1148,446 H 1200")               ; lab(1174, 438, "API")
path("M 800,266 H 1200", dashed=True)   ; lab(1000, 258, "ticket hand-off")
path("M 574,576 V 608")                 ; lab(582, 597, "Web SDK", "start")
path("M 1370,576 V 608", dashed=True)   ; lab(1378, 597, "registration events", "start")

doc = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NFL Events Hub Executive Architecture</title>
<link href="https://fonts.googleapis.com/css2?family=Source+Sans+3:ital,wght@0,400;0,600;0,700;1,400&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{ background:#fff; font-family:'Source Sans 3',Calibri,system-ui,sans-serif; color:#0f172a; }}
  .wrap {{ width:100%; overflow-x:auto; }}
  .slide {{ position:relative; width:{W}px; height:{H}px; margin:0 auto; background:#fff; overflow:hidden; }}
  .eyebrow {{ position:absolute; left:64px; top:40px; font-size:13px; font-weight:600; letter-spacing:0.16em; color:#64748b; }}
  h1 {{ position:absolute; left:64px; top:58px; font-size:36px; font-weight:700; letter-spacing:-0.01em; color:#0b1f3a; }}
  .sub {{ position:absolute; left:64px; top:106px; font-size:17px; color:#475569; }}
  .b {{ position:absolute; }}
  .strip {{ background:#f1f5f9; border-radius:8px; display:flex; align-items:center; gap:22px; padding:0 20px; font-size:14px; color:#334155; }}
  .strip .k {{ font-size:11.5px; font-weight:700; letter-spacing:0.14em; color:#64748b; }}
  .strip b {{ font-weight:600; color:#0f172a; margin-right:6px; }}
  .strip .sep {{ width:1px; height:18px; background:#cbd5e1; }}
  .colh {{ font-size:11.5px; font-weight:700; letter-spacing:0.14em; color:#64748b; }}
  .card {{ background:#fff; border:1px solid #e2e8f0; border-radius:10px; box-shadow:0 1px 2px rgba(15,23,42,0.06),0 4px 14px rgba(15,23,42,0.05); padding:18px 20px; border-top-width:4px; }}
  .c-fan {{ border-top-color:#94a3b8; }} .c-adobe {{ border-top-color:#eb1000; }} .c-aws {{ border-top-color:#ff9900; }}
  .c-nfl {{ border-top-color:#013369; }} .c-part {{ border-top-color:#94a3b8; }}
  .mark {{ position:absolute; right:16px; top:14px; width:28px; height:28px; border-radius:5px; }}
  .ht {{ font-size:20px; font-weight:700; color:#0b1f3a; }}
  .hs {{ font-size:13px; color:#64748b; margin-top:2px; }}
  .rows {{ display:flex; flex-direction:column; justify-content:space-around; height:100%; }}
  .rows.tight {{ height:auto; margin-top:12px; gap:9px; }}
  .row {{ display:flex; align-items:center; gap:12px; }}
  .row svg {{ flex:none; }}
  .row b {{ display:block; font-size:15px; font-weight:600; }} .row i {{ display:block; font-style:normal; font-size:12.5px; color:#64748b; }}
  .c-fan .row b {{ font-size:17px; }}
  .cols {{ display:grid; grid-template-columns:1fr 1fr; gap:20px; margin-top:18px; }}
  .cl {{ font-size:12px; font-weight:700; letter-spacing:0.12em; text-transform:uppercase; color:#eb1000; margin-bottom:8px; }}
  ul {{ list-style:none; }} li {{ font-size:14.5px; padding:7px 0; border-bottom:1px solid #f1f5f9; }}
  .pers {{ position:absolute; left:20px; right:20px; bottom:18px; background:#fff5f4; border:1px solid #fbd0cb; border-radius:6px; padding:9px 12px; font-size:13.5px; font-weight:600; color:#9f1d12; text-align:center; }}
  .note {{ position:absolute; left:20px; right:20px; bottom:16px; font-size:12.5px; font-weight:600; color:#b45309; }}
  .slim {{ display:flex; align-items:center; padding:10px 20px; }}
  .slim b {{ display:block; font-size:15px; font-weight:600; }} .slim i {{ display:block; font-style:normal; font-size:12.5px; color:#64748b; }}
  .band {{ display:flex; align-items:center; gap:36px; padding:12px 20px; border-top-color:#eb1000; }}
  .bl {{ display:flex; align-items:center; gap:10px; font-size:16px; font-weight:700; color:#0b1f3a; width:270px; }}
  .bl img {{ width:28px; height:28px; border-radius:5px; }}
  .bi {{ padding-left:24px; border-left:1px solid #e2e8f0; }}
  .bi b {{ display:block; font-size:15px; font-weight:600; }} .bi i {{ display:block; font-style:normal; font-size:12.5px; color:#64748b; }}
  .out {{ background:#0b1f3a; border-radius:10px; padding:16px 20px; color:#fff; }}
  .out b {{ display:block; font-size:24px; font-weight:700; }} .out i {{ display:block; font-style:normal; font-size:14px; color:#cbd5e1; margin-top:4px; }}
  .foot {{ display:flex; align-items:center; gap:14px; font-size:13px; color:#64748b; }}
  .foot .dot {{ width:4px; height:4px; border-radius:2px; background:#cbd5e1; }}
  svg.ov {{ position:absolute; left:0; top:0; pointer-events:none; }}
  svg.ov path {{ fill:none; stroke:#334155; stroke-width:1.6; }}
  svg.ov text {{ font-size:12px; font-weight:600; fill:#475569; font-family:'Source Sans 3',Calibri,system-ui,sans-serif; }}
</style></head>
<body><div class="wrap"><div class="slide" role="img" aria-label="Executive architecture of the NFL Events Hub: fans on NFL OnePass, the NFL App and the web reach the NFL Events Hub on AEM Edge Delivery Services through the Adobe CDN; the hub hands off ticketing to Ticketmaster and On Location and calls a stateless middleware API on AWS for registration, NFL ID sign-in and wallet passes, which connects to NFL systems; Adobe Journey Optimizer, Target and Real-Time CDP provide engagement and personalization.">
<div class="eyebrow">EXECUTIVE ARCHITECTURE</div>
<h1>NFL Events Hub</h1>
<div class="sub">One events platform for the league, clubs and international markets — built on Adobe, integrated with NFL systems</div>
{chr(10).join(B)}
<svg class="ov" width="{W}" height="{H}" viewBox="0 0 {W} {H}" aria-hidden="true">
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#334155" stroke="none"/></marker></defs>
{chr(10).join(P)}
{chr(10).join(L)}
</svg>
</div></div></body></html>
"""
open(os.path.join(OUT, "nfl-events-hub-executive.html"), "w").write(doc)
print("ok")
