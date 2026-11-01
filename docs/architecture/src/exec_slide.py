"""NFL Events Hub — executive platform slide (EDS), corrected version of the client's draft.

Usage: python3 exec_slide.py <output-dir>
Logos are cropped from the client's draft slide (docs/architecture/assets) — replace with official brand files.
"""
import sys, os, base64, html

OUT = sys.argv[1]
ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")


def b64(name):
    with open(os.path.join(ASSETS, name), "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()


NFL, ADOBE, AMARK = b64("nfl-logo-crop.png"), b64("adobe-logo-crop.png"), b64("adobe-mark-crop.png")

# 24x24 line icons
I = {
    "phone": '<rect x="6" y="2" width="12" height="20" rx="2.5"/><path d="M10.5 18.5h3"/>',
    "app": '<rect x="6" y="2" width="12" height="20" rx="2.5"/><path d="M9 7h6M9 10.5h6M9 14h4"/>',
    "laptop": '<rect x="4" y="5" width="16" height="11" rx="1.5"/><path d="M2 19h20"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="M16 16l5 5"/>',
    "pin": '<path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
    "cal": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
    "edit": '<path d="M4 20h4l11-11-4-4L4 16z"/><path d="M13 7l4 4"/>',
    "ticket": '<path d="M3 7h18v3a2 2 0 0 0 0 4v3H3v-3a2 2 0 0 0 0-4z"/><path d="M15 7v10" stroke-dasharray="2 2"/>',
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
    "sheet": '<rect x="4" y="3" width="16" height="18" rx="2"/><path d="M4 9h16M4 15h16M10 3v18"/>',
    "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.5"/>',
    "shield": '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
    "bell": '<path d="M6 16v-5a6 6 0 0 1 12 0v5l2 2H4z"/><path d="M10 21a2 2 0 0 0 4 0"/>',
    "hotel": '<path d="M3 21V8l9-5 9 5v13"/><path d="M9 21v-6h6v6"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3.5 3 14.5 0 18M12 3c-3 3.5-3 14.5 0 18"/>',
    "check": '<circle cx="12" cy="12" r="9"/><path d="M8 12l3 3 5-6"/>',
    "layers": '<path d="M12 3l9 5-9 5-9-5z"/><path d="M3 13l9 5 9-5"/>',
    "fans": '<circle cx="8" cy="9" r="3"/><circle cx="16" cy="9" r="3"/><path d="M2 20a6 6 0 0 1 12 0M10 20a6 6 0 0 1 12 0"/>',
    "trend": '<path d="M3 17l6-6 4 4 8-8"/><path d="M15 7h6v6"/>',
}


def icon(name, size=26, color="#0b2a5b"):
    return (f'<svg viewBox="0 0 24 24" width="{size}" height="{size}" fill="none" stroke="{color}" stroke-width="1.7" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{I[name]}</svg>')


e = html.escape


def card(ic, title, sub):
    return f'<div class="card">{icon(ic, 28)}<div><b>{e(title)}</b><span>{e(sub)}</span></div></div>'


def tile(ic, title):
    return f'<div class="tile">{icon(ic, 30)}<b>{e(title)}</b></div>'


def pills(items):
    return "".join(f'<span class="pill">{e(t)}</span>' for t in items)


doc = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NFL Events Hub Platform Architecture</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
  :root {{ --navy:#0b2a5b; --ink:#16213a; --muted:#4a5872; --blue:#eaf2fb; --blue-line:#c6d8ef; --pink:#fdeef0; --pink-line:#f2c2c8; --red:#e1251b; }}
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{ background:#fff; font-family:'Inter',system-ui,sans-serif; color:var(--ink); }}
  .wrap {{ width:100%; overflow-x:auto; }}
  .slide {{ position:relative; width:1600px; height:900px; margin:0 auto; background:#fff; }}
  .abs {{ position:absolute; }}
  .hdr img.nfl {{ height:70px; }} .hdr img.adobe {{ height:42px; }}
  h1 {{ font-size:36px; font-weight:800; color:var(--navy); letter-spacing:-0.01em; }}
  .sub {{ font-size:17px; color:var(--muted); margin-top:4px; }}
  .bar {{ display:flex; align-items:center; gap:10px; border-radius:12px; padding:0 22px; font-size:15px; color:var(--muted); }}
  .bar.pink {{ background:var(--pink); border:1.5px solid var(--pink-line); }}
  .bar.blue {{ background:var(--blue); border:1.5px solid var(--blue-line); }}
  .bar b {{ font-size:19px; color:var(--ink); font-weight:700; margin-right:8px; }}
  .bar .sep {{ width:1px; height:20px; background:#b9c3d3; }}
  .bar img {{ width:30px; height:30px; }}
  .bar svg, .card svg, .wide svg {{ flex:none; }}
  .tile, .wide {{ min-width:0; }}
  .panel {{ background:#f6f9fd; border:1.5px solid var(--blue-line); border-radius:14px; padding:16px; }}
  .panel h2 {{ font-size:19px; font-weight:800; color:var(--navy); margin-bottom:12px; }}
  .panel h3 {{ font-size:12px; font-weight:600; color:var(--muted); letter-spacing:0.08em; text-transform:uppercase; margin:-6px 0 10px; }}
  .card {{ display:flex; align-items:center; gap:14px; background:#fff; border:1px solid var(--blue-line); border-radius:10px; padding:7px 14px; margin-bottom:8px; }}
  .card b {{ display:block; font-size:16px; font-weight:700; color:var(--ink); }}
  .card span {{ display:block; font-size:12.5px; color:var(--muted); }}
  .hub {{ background:var(--navy); border-radius:16px; padding:14px 16px 16px; }}
  .hub .t {{ text-align:center; color:#fff; font-size:27px; font-weight:800; }}
  .hub .s {{ text-align:center; color:#cfdcf0; font-size:15px; margin:2px 0 12px; }}
  .inner {{ background:#fff; border-radius:12px; padding:12px; display:grid; gap:10px; }}
  .row {{ display:flex; gap:8px; align-items:stretch; }}
  .lbl {{ width:124px; flex:none; background:var(--blue); border-radius:10px; padding:10px 14px; font-weight:700; font-size:15.5px; color:var(--navy); display:flex; align-items:center; line-height:1.2; }}
  .tile {{ flex:1; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:6px; border:1px solid var(--blue-line); border-radius:10px; padding:10px 4px; }}
  .tile b {{ font-size:13px; font-weight:700; white-space:nowrap; }}
  .wide {{ flex:1; display:flex; align-items:center; gap:12px; border:1px solid var(--blue-line); border-radius:10px; padding:10px 16px; font-size:14px; color:var(--muted); }}
  .wide b {{ font-size:18px; font-weight:700; color:var(--ink); }}
  .wide small {{ display:block; font-size:12.5px; color:var(--muted); }}
  .pill {{ border-left:1px solid #b9c3d3; padding:0 8px; font-size:12.5px; color:var(--ink); white-space:nowrap; }}
  .bar b, .wide small {{ white-space:nowrap; }}
  .edge {{ background:var(--blue); border:1.5px solid var(--blue-line); border-radius:14px; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; gap:8px; padding:12px 8px; }}
  .edge b {{ font-size:16px; font-weight:800; color:var(--navy); }}
  .edge span {{ font-size:12.5px; color:var(--muted); line-height:1.35; }}
  .value {{ display:flex; align-items:center; justify-content:space-around; background:var(--blue); border:1.5px solid var(--blue-line); border-radius:14px; }}
  .value div {{ display:flex; align-items:center; gap:12px; font-size:18px; font-weight:600; color:var(--ink); }}
  .note {{ font-size:11.5px; color:#7a869b; }}
  .lab {{ font-size:13px; font-weight:600; fill:var(--muted); font-family:'Inter',sans-serif; }}
</style></head>
<body><div class="wrap"><div class="slide" role="img" aria-label="NFL Events Hub platform architecture on AEM Edge Delivery Services">

<div class="abs hdr" style="left:40px;top:18px;display:flex;align-items:center;gap:22px">
  <img class="nfl" src="{NFL}" alt="NFL logo"><span style="width:1.5px;height:56px;background:#c7cfdc"></span><img class="adobe" src="{ADOBE}" alt="Adobe logo">
</div>
<div class="abs" style="left:430px;top:20px"><h1>NFL Events Hub — Platform Architecture (EDS)</h1>
  <div class="sub">One event platform to author, manage and deliver league, regional and club events — on web, NFL OnePass and the NFL App.</div></div>

<div class="abs bar pink" style="left:412px;top:118px;width:828px;height:52px"><img src="{AMARK}" alt=""><b>Event Authoring · AEM</b>{pills(["Events", "Forms", "Club & market variants", "Multilingual"])}</div>

<div class="abs panel" style="left:24px;top:236px;width:262px;height:336px"><h2>Experience Channels</h2>
  {card("phone", "NFL OnePass", "embeds the hub")}{card("app", "NFL App", "embeds the hub")}{card("laptop", "Web", "events.nfl.com · nfl.com · clubs")}
</div>

<div class="abs edge" style="left:310px;top:236px;width:82px;height:336px">{icon("globe", 30)}<b>Edge CDN</b><span>global delivery<br>caching<br>WAF · bot</span><span style="font-size:11px">Adobe-managed or BYO</span></div>

<div class="abs hub" style="left:412px;top:196px;width:828px;height:330px">
  <div class="t">NFL Events Hub · events.nfl.com</div><div class="s">Built on AEM Edge Delivery Services — event experience, data and personalization</div>
  <div class="inner">
    <div class="row"><div class="lbl">Experience<br>Layer</div>{tile("search","Discover")}{tile("pin","Near Me")}{tile("cal","Event Detail")}{tile("edit","Register")}{tile("ticket","Tickets")}{tile("user","My Events")}</div>
    <div class="row"><div class="lbl">Event Data</div><div class="wide">{icon("sheet", 34)}<div><b>Event Catalog</b><small>authored sheets → events.json</small></div><div style="margin-left:auto;display:flex">{pills(["Events", "Venues", "Schedule", "Eligibility", "Status"])}</div></div></div>
    <div class="row"><div class="lbl">Personal-<br>ization</div><div class="wide">{icon("target", 34)}<div><b>Personalization</b><small>Adobe Target · Real-Time CDP via Web SDK</small></div><div style="margin-left:auto">Relevant experiences across web, OnePass and the NFL App</div></div></div>
  </div>
</div>

<div class="abs bar pink" style="left:412px;top:616px;width:828px;height:56px">{icon("user", 30)}<b>Session &amp; Identity Middleware</b>{pills(["NFL ID session", "SSO", "API proxy", "Stateless · no data stored"])}</div>

<div class="abs panel" style="left:1272px;top:180px;width:304px;height:332px"><h2>Experience Services</h2><h3>from the page</h3>
  {card("target", "Adobe Target · RT-CDP", "personalization")}{card("shield", "OneTrust", "consent & privacy")}{card("ticket", "Ticketmaster", "ticketing · link-out")}{card("hotel", "On Location", "official hospitality · link-out")}
</div>
<div class="abs panel" style="left:1272px;top:524px;width:304px;height:272px"><h2>Platform Services</h2><h3>via middleware</h3>
  {card("user", "NFL ID", "SSO · identity")}{card("cal", "OnePass registration", "QR · check-in")}{card("bell", "Notifications", "AJO · Campaign")}
</div>

<svg class="abs" style="left:0;top:0" width="1600" height="900" aria-hidden="true">
  <defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#16213a"/></marker></defs>
  <g stroke="#16213a" stroke-width="2" fill="none">
    <path d="M826 170 V194" marker-end="url(#ah)"/>
    <path d="M286 404 H308" marker-end="url(#ah)"/>
    <path d="M392 404 H410" marker-end="url(#ah)"/>
    <path d="M826 526 V614" marker-start="url(#ah)" marker-end="url(#ah)"/>
    <path d="M1240 346 H1270" marker-start="url(#ah)" marker-end="url(#ah)"/>
    <path d="M1240 644 H1270" marker-start="url(#ah)" marker-end="url(#ah)"/>
  </g>
  <text class="lab" x="836" y="188">Publish</text>
</svg>

<div class="abs value" style="left:60px;top:812px;width:1480px;height:56px">
  <div>{icon("check", 30)}Faster event delivery</div><div>{icon("layers", 30)}One event catalog</div>
  <div>{icon("fans", 30)}Personalized fan experiences</div><div>{icon("trend", 30)}Scalable &amp; secure</div>
</div>
<div class="abs note" style="left:60px;top:878px">OneTrust to be confirmed with NFL. Logos cropped from the draft for internal review — replace with official brand assets before sharing.</div>

</div></div></body></html>
"""
open(f"{OUT}/nfl-events-hub-exec-slide.html", "w").write(doc)
print("ok")
