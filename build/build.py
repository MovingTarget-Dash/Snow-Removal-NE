# -*- coding: utf-8 -*-
"""Gerador do site New England Snow Removal (HTML estático).
Uso:  python build.py      -> escreve as páginas em ../site
Para trocar textos, contatos ou imagens, edite este arquivo e rode de novo."""
import os, json, html, datetime
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "site"))
IMGDIR = os.path.join(OUT, "assets", "img")

SITE = "https://snowremoval-ne.com"
NAME = "New England Snow Removal"
PHONE = "978-809-6279"; TEL = "+19788096279"
EMAIL = "deck@newenglandcarpenters.com"
ADDR = "North Andover, Massachusetts 01845, United States"
WA = "https://wa.me/19788096279?text=I%20came%20across%20your%20website%20and%20need%20a%20quote%21"
SMS = "sms:+19788096279?body=I%20came%20across%20your%20website%20and%20need%20a%20quote%21"
FB = "https://www.facebook.com/newenglandcarpenter.decknewengland/"
IG = "https://www.instagram.com/newenglandcarpenters/"
CITIES = ["Haverhill", "Methuen", "Lawrence", "North Andover", "Groveland", "Georgetown", "Boxford", "Andover"]
TODAY = datetime.date.today().isoformat()
e = lambda s: html.escape(str(s), quote=True)

ICON = {
 'snow': '<path d="M12 2v20M4.3 7l15.4 10M4.3 17L19.7 7M9 3.5l3 2.5 3-2.5M9 20.5l3-2.5 3 2.5"/>',
 'truck': '<path d="M2 7h11v9H2zM13 10h4l3 3v3h-7z"/><circle cx="6.5" cy="17.5" r="1.8"/><circle cx="16.5" cy="17.5" r="1.8"/>',
 'shovel': '<path d="M15 3l6 6M13 5l6 6-7 3-3-3zM9 14l-6 7"/>',
 'door': '<path d="M6 21V4h12v17M3 21h18M15 12.5h.01"/>',
 'clip': '<path d="M9 4h6v3H9zM7 5H5v16h14V5h-2M8.5 12h7M8.5 16h5"/>',
 'shield': '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6zM8.5 12l2.5 2.5 4.5-5"/>',
 'pin': '<path d="M12 21s7-6.2 7-11a7 7 0 10-14 0c0 4.8 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/>',
 'clock': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 'home': '<path d="M3 11l9-8 9 8M5 10v10h14V10"/>',
 'chat': '<path d="M4 5h16v11H9l-5 4z"/>',
 'tag': '<path d="M3 12V3h9l9 9-9 9z"/><circle cx="7.5" cy="7.5" r="1.3"/>',
 'phone': '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 005 5L15 13l5 2v4a2 2 0 01-2 2A16 16 0 013 6a2 2 0 012-2z"/>',
 'mail': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
 'build': '<path d="M4 21V4h10v17M14 9h6v12M8 8h2M8 12h2M8 16h2"/>',
}
def svg(k): return f'<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">{ICON.get(k, ICON["snow"])}</svg>'
def ico(k): return f'<div class="ico">{svg(k)}</div>'
SEAL = f'<span class="seal" role="img" aria-label="Snow Removal"><span class="in">{svg("snow")}<span class="t1">SNOW</span><span class="t2">REMOVAL</span></span></span>'

# ---------------------------------------------------------------- imagens
_dim = {}
def dim(name):
    if name not in _dim:
        with Image.open(os.path.join(IMGDIR, name)) as im: _dim[name] = im.size
    return _dim[name]
def img(base, alt, cls="", lazy=True, sizes="(max-width: 800px) 100vw, 600px", eager=False):
    big = base + ".webp"; sm = base + "-sm.webp"
    w, h = dim(big)
    srcset = ""
    if os.path.exists(os.path.join(IMGDIR, sm)):
        sw, _ = dim(sm); srcset = f' srcset="/assets/img/{sm} {sw}w, /assets/img/{big} {w}w" sizes="{sizes}"'
    load = ' fetchpriority="high"' if eager else (' loading="lazy"' if lazy else '')
    c = f' class="{cls}"' if cls else ''
    return f'<img{c} src="/assets/img/{big}"{srcset} alt="{e(alt)}" width="{w}" height="{h}"{load} decoding="async">'

ALT = {
 "hero-adobestock": "Pickup truck with a red plow pushing a wall of snow in a parking lot",
 "fisher-plow": "Pickup truck with a yellow plow throwing snow on a wooded road",
 "chevy-plow": "Black pickup truck plowing a snowy road",
 "red-plow": "White pickup with a red plow blade clearing snow",
 "street-shoveling": "Man shoveling snow on a residential street",
 "shoveling-man": "Person shoveling heavy snow from a driveway",
 "truck-forest": "Red truck with a plow driving down a snowy forest road",
 "truck-road": "White truck with a red plow on a snowy tree-lined road",
 "deck-woman": "Woman shoveling snow off a wooden deck",
 "shovel-closeup": "Blue snow shovel lifting snow from a walkway",
}
def photo(base, cls="", **kw): return img(base, ALT[base], cls, **kw)

# ---------------------------------------------------------------- blocos
def btn(text, href, kind="p", extra=""):
    return f'<a class="btn {kind}" href="{href}"{extra}>{e(text)}</a>'
def btns(items):
    return '<div class="row">' + "".join(btn(t, h, "p" if i == 0 else "s") for i, (t, h) in enumerate(items)) + '</div>' if items else ""
def eb(t): return f'<div class="eb">{e(t)}</div>' if t else ""
def sec(inner, tone="", sid="", center=False, label=""):
    cls = "sec" + (f" {tone}" if tone else "") + (" center" if center else "")
    ida = f' id="{sid}"' if sid else ""
    la = f' aria-label="{e(label)}"' if label else ""
    return f'<section class="{cls}"{ida}{la}><div class="wrap">{inner}</div></section>'
def cards(items, cols=3, icons=True, center=False):
    out = []
    for it in items:
        t, d = it[0], it[1]; k = it[2] if len(it) > 2 else None
        out.append(f'<div class="card{" center" if center else ""}">{ico(k) if k else ""}<h3>{e(t)}</h3>{f"<p>{e(d)}</p>" if d else ""}</div>')
    return f'<div class="grid c{cols}">{"".join(out)}</div>'
def pills(items):
    return '<ul class="pills">' + "".join(f'<li class="pill">{e(i)}</li>' for i in items) + '</ul>'
def steps(items, cols=3):
    return f'<ol class="grid c{cols}" style="list-style:none;padding:0">' + "".join(
        f'<li class="card"><div class="num">{n}</div><h3>{e(t)}</h3><p>{e(d)}</p></li>' for n, (t, d) in enumerate(items, 1)) + '</ol>'
def faq(items, first_open=True):
    return '<div class="faqw">' + "".join(
        f'<details class="faq"{" open" if (first_open and i == 0) else ""}><summary>{e(q)}</summary><p>{e(a)}</p></details>' for i, (q, a) in enumerate(items)) + '</div>'
def hl_title(title, hl):
    t = e(title)
    return t.replace(e(hl), f'<span class="g">{e(hl)}</span>', 1) if hl and hl in title else t
def hero(h1, hl, photo_base, eyebrow="", text="", buttons=None, badges=None, small=False):
    b = ""
    if badges: b = '<ul class="badges">' + "".join(f'<li>{e(x)}</li>' for x in badges) + '</ul>'
    return (f'<section class="hero{" sm" if small else ""}">{photo(photo_base, "bg", eager=True, sizes="100vw")}'
            f'<div class="wrap"><div class="in">{eb(eyebrow)}<h1>{hl_title(h1, hl)}</h1>'
            f'{f"<p class=lead>{e(text)}</p>" if text else ""}{btns(buttons)}{b}</div></div></section>')
def split(left, pic_html, rev=False):
    return f'<div class="split{" rev" if rev else ""}"><div>{left}</div>{pic_html}</div>'
def pic(base, **kw): return f'<figure class="pic">{photo(base, **kw)}</figure>'
def cta(title, text="", buttons=None, eyebrow=""):
    return sec(f'{eb(eyebrow)}<h2>{e(title)}</h2>{f"<p class=lead>{e(text)}</p>" if text else ""}{btns(buttons or [("Get a Free Quote", "/contact/")])}', "dark", center=True)
def mapbox(title, text, extra="", rev=True):
    left = f'<h2>{e(title)}</h2><p class="lead">{e(text)}</p>{extra}'
    m = '<div class="map"><iframe src="https://maps.google.com/maps?q=North%20Andover%2C%20MA%2001845&amp;t=m&amp;z=10&amp;output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="Map of North Andover, MA"></iframe></div>'
    return split(left, m, rev)

def quote_form(title="Fill out the form and contact us"):
    return f'''<form class="fcard" data-lead action="/api/lead" method="post" novalidate>
<h3>{e(title)}</h3>
<label class="sr" for="f-name">Name</label><input id="f-name" name="name" type="text" placeholder="Name" autocomplete="name" required maxlength="120">
<label class="sr" for="f-email">Email</label><input id="f-email" name="email" type="email" placeholder="Email" autocomplete="email" required maxlength="160">
<label class="sr" for="f-phone">Phone</label><input id="f-phone" name="phone" type="tel" placeholder="Phone" autocomplete="tel" required maxlength="40">
<label class="sr" for="f-address">Property address</label><input id="f-address" name="address" type="text" placeholder="Property address" autocomplete="street-address" maxlength="200">
<label class="sr" for="f-type">Property type</label><select id="f-type" name="type"><option value="">Property type (Commercial / Residential)</option><option>Commercial</option><option>Residential</option></select>
<label class="sr" for="f-msg">Message</label><textarea id="f-msg" name="message" placeholder="Message" maxlength="3000"></textarea>
<div class="hp" aria-hidden="true"><label>Leave this field empty<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
<input type="hidden" name="page" value=""><input type="hidden" name="utm_source" value=""><input type="hidden" name="utm_medium" value=""><input type="hidden" name="utm_campaign" value=""><input type="hidden" name="gclid" value=""><input type="hidden" name="fbclid" value="">
<button class="btn p" type="submit" style="margin:6px 0 0">Submit the form</button>
<div class="fmsg" role="status" aria-live="polite"></div>
</form>'''

def quote_section(sid="quote"):
    left = (f'{eb("Free quote")}<h2>Get a free snow removal quote</h2>'
            '<p class="lead">Tell us the address and what sits on it. You get back a plan written for that site, a price per visit or for the season, and a number that is answered when it is actually snowing.</p>'
            f'<div class="side">{ico("phone")}<div><b>WhatsApp · SMS · Phone</b><a href="tel:{TEL}">{PHONE}</a></div></div>'
            f'<div class="side">{ico("mail")}<div><b>Email</b><a href="mailto:{EMAIL}">{EMAIL}</a></div></div>')
    return sec(f'<div class="fgrid"><div>{left}</div>{quote_form()}</div>', "dark", sid=sid)

# ---------------------------------------------------------------- layout
NAVKEYS = [("home", "Home", "/"), ("services", "Services", "/commercial-snow-removal/"), ("areas", "Service Areas", "/service-areas/"),
           ("about", "About", "/about/"), ("work", "Our Work", "/our-work/"), ("blog", "Blog", "/blog/"), ("contact", "Contact", "/contact/")]
def header(active, path):
    items = []
    for key, label, href in NAVKEYS:
        cur = ' aria-current="page"' if (key == active and path == href) else ""
        if key == "services":
            c1 = ' aria-current="page"' if path == "/commercial-snow-removal/" else ""
            c2 = ' aria-current="page"' if path == "/residential-snow-removal/" else ""
            items.append(f'<li class="has-sub"><a href="{href}"{c1 if path == href else ""}>{label} ▾</a><ul class="sub"><li><a href="/commercial-snow-removal/"{c1}>Commercial Snow Removal</a></li><li><a href="/residential-snow-removal/"{c2}>Residential Snow Removal</a></li></ul></li>')
        else:
            items.append(f'<li><a href="{href}"{cur}>{label}</a></li>')
    return (f'<a class="skip" href="#main">Skip to content</a>'
            f'<div class="topbar"><div class="wrap"><span>Commercial &amp; residential snow removal · North Andover, MA</span><a href="tel:{TEL}">WhatsApp {PHONE}</a></div></div>'
            f'<header class="site-header"><div class="wrap hdr"><a class="brand" href="/" aria-label="{NAME} - home"><img src="/assets/img/logo-horizontal.webp" alt="New England Carpenters" width="420" height="136">{SEAL}</a>'
            f'<nav class="nav" id="site-nav" aria-label="Main"><ul>{"".join(items)}</ul></nav>'
            f'<a class="btn p sm" href="/contact/">Get a Free Quote</a>'
            f'<button class="burger" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="Menu">&#9776;</button></div></header>')

def footer():
    cities = "".join(f"<li>{c}</li>" for c in CITIES)
    return f'''<footer class="ftr"><div class="wrap">
<div class="grid c4">
<div><div class="brandrow"><img src="/assets/img/logo-horizontal.webp" alt="New England Carpenters" width="420" height="136" loading="lazy">{SEAL}</div>
<p>{ADDR}</p><p><a href="tel:{TEL}">{PHONE}</a></p><p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
<p><a href="{FB}" rel="noopener" target="_blank">Facebook</a> · <a href="{IG}" rel="noopener" target="_blank">Instagram</a> · <a href="{WA}" rel="noopener" target="_blank">WhatsApp</a></p></div>
<div><h2>Quick Links</h2><ul><li><a href="/">Home</a></li><li><a href="/commercial-snow-removal/">Commercial Snow Removal</a></li><li><a href="/residential-snow-removal/">Residential Snow Removal</a></li><li><a href="/service-areas/">Service Areas</a></li><li><a href="/about/">About</a></li><li><a href="/our-work/">Our Work</a></li><li><a href="/blog/">Blog</a></li><li><a href="/contact/">Contact</a></li></ul></div>
<div><h2>Services</h2><ul><li>Parking Lot Snow Removal</li><li>Snow Plowing and Shoveling</li><li>Sidewalks and Entryways</li><li>Ice Control and Removal</li><li>Snow and Ice Management Plans</li></ul></div>
<div><h2>Service Areas</h2><ul>{cities}</ul></div></div>
<div class="sites"><h2>Discover our other websites</h2><a class="btn s" href="https://deck.newenglandcarpenters.com/" target="_blank" rel="noopener">Deck &amp; Porch · deck.newenglandcarpenters.com</a><a class="btn s" href="https://newenglandcarpenters.com/" target="_blank" rel="noopener">New England Carpenters · newenglandcarpenters.com</a></div>
<div class="copy">© 2026 {NAME} · A New England Carpenters company. All rights reserved. · <a href="/privacy-policy/">Privacy Policy</a> · <a href="/terms/">Terms</a></div>
</div></footer>'''

def max_btn(path):
    href = "#quote" if path == "/" else "/#quote"
    return (f'<a class="max" href="{href}" aria-label="Contact us: go to the quote form"><img src="/assets/img/max-contato.webp" '
            f'alt="Max, our mascot, holding a sign that says Click here and contact us" width="300" height="400" loading="lazy"></a>')

def jsonld_business():
    return {"@context": "https://schema.org", "@type": "LocalBusiness", "name": NAME, "url": SITE,
            "description": "Commercial and residential snow and ice removal in Essex County, Massachusetts.",
            "logo": SITE + "/assets/img/icon-512.png", "image": SITE + "/assets/img/og-image.jpg",
            "telephone": "+1-978-809-6279", "email": EMAIL,
            "address": {"@type": "PostalAddress", "addressLocality": "North Andover", "addressRegion": "MA", "postalCode": "01845", "addressCountry": "US"},
            "areaServed": [{"@type": "City", "name": c} for c in CITIES],
            "parentOrganization": {"@type": "Organization", "name": "New England Carpenters", "url": "https://newenglandcarpenters.com"},
            "sameAs": [FB, IG]}
def jsonld_faq(items):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}

PAGES = []   # (path, html)
def page(path, key, title, desc, body, schema=None, noindex=False, og_type="website", faq_items=None, lead_hero=None):
    url = SITE + path
    ld = [jsonld_business()] if path == "/" or key in ("contact", "areas") else []
    if faq_items: ld.append(jsonld_faq(faq_items))
    if schema: ld.append(schema)
    ldh = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    robots = '<meta name="robots" content="noindex, follow">' if noindex else ""
    doc = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
{robots}<link rel="canonical" href="{url}">
<meta name="theme-color" content="#0d0801">
<meta property="og:type" content="{og_type}"><meta property="og:site_name" content="{NAME}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{SITE}/assets/img/og-image.jpg"><meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/img/favicon-32.png"><link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/montserrat-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/style.css">
{ldh}
</head>
<body>
{header(key, path)}
<main id="main">
{body}
</main>
{footer()}
{max_btn(path)}
<script src="/assets/js/main.js" defer></script>
</body>
</html>
'''
    PAGES.append((path, doc))

# ================================================================ CONTEÚDO
SERVICES = [("Parking Lot Snow Removal", "Plowing and clearing so customers, employees and deliveries can get in and out safely.", "truck"),
            ("Snow Plowing and Shoveling", "Machine and hand clearing for lots, driveways and tight spaces.", "shovel"),
            ("Sidewalks and Entryways", "Clear, safe walkways right where people walk in.", "door"),
            ("Ice Control and Removal", "De-icing and salting to cut down on slips and falls.", "snow"),
            ("Snow and Ice Management Plans", "A written plan built around your property, priced per visit or for the whole season.", "clip")]
FAQ_HOME = [("What services do you offer?", "Parking lot and driveway plowing, shoveling, sidewalks and entryways, ice control and written snow and ice management plans."),
            ("Do you only plow, or do you handle de-icing and salting too?", "Both. We plow, shovel, de-ice and salt, so your surfaces are safe to walk and drive on, not just cleared."),
            ("When should I set up a snow contract?", "The best time is late summer through fall, before the first storm. Most properties are booked before winter, so planning early secures your spot and gives us time to walk your site and build the plan."),
            ("How do you prove the work was performed?", "Every visit is time-stamped and logged through GPS-tracked equipment and written work orders, and you get updates during the storm, so you have clear documentation for owners, tenants and your own files."),
            ("What happens if a storm hits overnight or on a weekend?", "Our crews and phone line run 24/7 during weather events, so your property is serviced and you can reach a real person no matter when the snow falls."),
            ("Do you offer free estimates?", "Yes. Send us the address and we will get back to you with a free quote.")]
HERO_BADGES = ["Free estimates", "Commercial & residential", "Local team in North Andover, MA", "24/7 storm response", "Fast response when it snows"]

# ---- HOME
home = hero("Snow Removal That Keeps Your Property Open and Safe", "Open and Safe", "hero-adobestock", "Snow removal · Essex County, MA",
            "Fast, reliable snow and ice removal for businesses and homes in Haverhill, Methuen, Lawrence, North Andover and nearby towns. Tell us the address and get a free quote.",
            [("Get a Free Quote", "/contact/"), ("Contact us", "#quote")], HERO_BADGES)
home += sec(eb("Our services") + "<h2>Everything it takes to clear your property</h2><p class=\"lead\">From parking lots to front steps, we handle the snow and the ice so you don't have to.</p>"
            + cards(SERVICES, 5) + btns([("See commercial services", "/commercial-snow-removal/"), ("See residential services", "/residential-snow-removal/")]), "dark")
home += sec(eb("Properties we clear") + "<h2>Built for the places people depend on</h2><p class=\"lead\">Customers, employees and deliveries all need a clear way in. We clear parking lots and store entrances to keep them safe, for:</p>"
            + pills(["Stores", "Malls", "Warehouses", "Distribution centers", "Condos", "Homes"]) + btns([("Ask about your property", "/contact/")]))
home += sec("<h2>Why property owners choose New England Snow Removal</h2>" + cards([
    ("Local and easy to reach", "Based in North Andover, MA. Reach a real person by phone, WhatsApp, SMS or email.", "pin"),
    ("A plan for your site", "What triggers a visit, what gets cleared first and where the snow is stacked.", "clip"),
    ("Clear pricing", "Per visit or for the whole season, agreed before the first storm.", "tag"),
    ("Documented service", "Trucks and salters are GPS-tracked, and every visit is time-stamped and logged with written work orders.", "shield"),
    ("Backed by New England Carpenters", "The same local company that builds decks and porches.", "home")], 5), "cream")
home += sec("<h2>How it works</h2>" + steps([("You send the details", "The address, the surfaces to clear, and how early the site has to be open."),
            ("We write the plan", "What triggers a visit, what gets cleared first and where the snow is stacked."),
            ("You approve the price", "Per visit or for the whole season, settled before the first storm.")]) + btns([("Start with a free quote", "/contact/")]))
home += sec(mapbox("Serving Essex County and nearby towns", "Our crews work in these communities. Not sure we reach you? Send us the address and we'll tell you.",
            pills(CITIES) + btns([("Check my address", "/contact/")])), "cream")
REVIEWS = [("Zhe Jenny Zhang", "“Tiago and his excellent crew did a fabulous job on our 30-yr old deck rebuild! Very timely arrival every single day and cleaned off work site before leaving every single day! Very well done and extra workmanship quality! Will hire them again in a heartbeat!”"),
           ("Robert Dwork", "“Excellent communication and willingness to work with the customer to get the desired results. Very professional and quality work.”"),
           ("Andre Alvaranga", "“Did a great job and great people with good prices”")]
rv = "".join(f'<figure class="rv"><div class="who"><div class="av">{e(n[0])}</div><div><b>{e(n)}</b><div style="font-size:12px;color:#888">Google review<span class="ex">example</span></div></div></div><div class="st" aria-label="5 stars">★★★★★</div><p>{e(t)}</p></figure>' for n, t in REVIEWS)
home += sec(f'{eb("Testimonials")}<h2>Customer testimonials</h2><div class="grid c3">{rv}</div>' + btns([("Be a satisfied customer!", "/contact/")]), center=True)
home += sec("<h2>Frequently asked questions</h2>" + faq(FAQ_HOME), "cream", center=True)
home += quote_section()
page("/", "home", "Snow Removal in Essex County, MA | New England Snow Removal",
     "Commercial and residential snow and ice removal in Haverhill, Methuen, Lawrence, North Andover and nearby towns. Get a free quote today.", home, faq_items=FAQ_HOME)

# ---- COMMERCIAL
FAQ_COM = [("When should I set up a commercial snow contract?", "The best time is late summer through fall, before the first storm."),
           ("Can you handle large parking lots and industrial sites?", "We plan equipment and crews around the size of the site. Send us the address and we will tell you how we would cover it."),
           ("How do you prove the work was performed?", "Every visit is time-stamped and logged through GPS and written work orders, so you have documentation for owners and tenants."),
           ("What happens if a storm hits overnight or on a weekend?", "Our crews and phone line run 24/7 during weather events so you can reach a real person.")]
c = hero("Commercial Snow Removal in Essex County, MA", "Essex County, MA", "fisher-plow", "Commercial snow removal",
         "Parking lots, store entrances and walkways cleared so your customers and employees can arrive and leave safely.", [("Get a Free Quote", "/contact/")])
c += sec(split(eb("") + "<h2>Safe access is part of doing business</h2><p class=\"lead\">Professional maintenance crews clear parking lots and store entrances to protect customers and employees. That is the job we do for commercial properties across Essex County.</p>"
               "<p class=\"lead\">Clearing a commercial lot takes more than a plow. It takes a plan: your site cleared, the salt down, the work documented, and someone who answers the phone when conditions change.</p>", pic("chevy-plow")))
c += sec("<h2>Our commercial snow and ice services</h2>" + cards([
    ("Parking Lot Snow Removal", "Plowing and clearing for lots of any size, so deliveries and customers keep moving.", "truck"),
    ("Snow Plowing and Shoveling", "Machine clearing for open areas and hand shoveling for corners, docks and tight spots.", "shovel"),
    ("Sidewalks and Entryways", "Clear, de-iced walkways and doors, where your people actually enter.", "door"),
    ("Ice Control and Removal", "Pre-treatment and de-icing ahead of the freeze, and salt after, to reduce slips and falls.", "snow"),
    ("Snow and Ice Management Plans", "A written plan for your site: triggers, priorities, snow storage and pricing.", "clip")], 5) + btns([("Ask for a quote", "/contact/")]), "cream")
c += sec("<h2>Properties we clear</h2>" + pills(["Stores", "Malls", "Warehouses", "Distribution centers", "Condos (common areas)"]))
c += sec("<h2>Our snow removal process</h2>" + steps([("Before the storm", "We watch the forecast and prepare. As the storm approaches, we apply brine to keep ice from bonding to your pavement."),
            ("During the storm", "Crews clear lots, entrances, exits and walkways and de-ice as they go, and the phone line stays open if anything changes."),
            ("After the storm", "We apply de-icer to guard against refreezing and improve traction, then document the visit, so your property is ready for the next business day.")]), "cream")
c += sec(split("<h2>A plan built around your property</h2><p class=\"lead\">Choose per-visit service or a seasonal plan. We settle the price before the first storm.</p><p class=\"lead\">Helpful to include in your request:</p>"
               "<ul class=\"checks\"><li>The site address</li><li>Which surfaces: lot, walkways, drive lanes</li><li>How early it has to be open</li><li>Per visit or seasonal</li></ul>" + btns([("Request a free quote", "/contact/")]),
               pic("truck-forest"), rev=True))
c += sec("<h2>Frequently asked questions</h2>" + faq(FAQ_COM), "cream", center=True)
c += cta("Get your property ready before the first storm", "Don't wait for the forecast to start thinking about snow. Talk to New England Snow Removal about a commercial snow removal plan built around your property, and head into winter knowing your site will stay open, safe and accessible.")
page("/commercial-snow-removal/", "services", "Commercial Snow Removal in Essex County, MA | New England Snow Removal",
     "Parking lot, entrance and sidewalk snow and ice removal for stores, malls, warehouses, distribution centers and condos in Essex County, MA. Free quote.", c, faq_items=FAQ_COM)

# ---- RESIDENTIAL
FAQ_RES = [("Do you clear decks and porches?", "Yes. We clear stairs, decks and porches with care for the surface, because we build them too."),
           ("Can I pay per visit or for the season?", "Both. Choose per-visit service or a seasonal plan, and we settle the price before the first storm."),
           ("How do I request a quote?", "Use the form, or reach us on WhatsApp, SMS, phone or email.")]
r = hero("Residential Snow Removal in Essex County, MA", "Essex County, MA", "street-shoveling", "Residential snow removal",
         "Wake up to a clear driveway, walkway and front steps. We handle the snow so you can get on with your day.", [("Get a Free Quote", "/contact/")])
r += sec("<h2>What we clear</h2>" + cards([("Driveways", "Plowed and cleared.", "truck"), ("Walkways and front steps", "Shoveled and treated for ice.", "door"),
            ("Stairs, decks and porches", "Cleared with care for the surface.", "home"), ("Ice control", "De-icing where it matters most.", "snow")], 4))
r += sec(split("<h2>Your deck and porch, in good hands</h2><p class=\"lead\">We are part of New England Carpenters, the team that builds decks, porches and stairs. We know these surfaces, so you can trust us to clear them.</p>",
               pic("deck-woman"), rev=True), "cream")
r += sec("<h2>How it works</h2>" + steps([("Tell us about your home", "Address, what needs clearing and how early."), ("We confirm the plan", "Per visit or for the season."),
            ("We clear", "And you stay inside where it is warm.")]) + btns([("Start with a free quote", "/contact/")]))
r += sec("<h2>Frequently asked questions</h2>" + faq(FAQ_RES), "cream", center=True)
r += cta("Get your home ready before the first storm", "Send us your address and get a free quote.")
page("/residential-snow-removal/", "services", "Residential Snow Removal in Essex County, MA | New England Snow Removal",
     "Driveway, walkway, steps and deck snow removal for homes in Essex County, MA. Free quote.", r, faq_items=FAQ_RES)

# ---- SERVICE AREAS
a = hero("Snow Removal Across Essex County and Nearby Towns", "Nearby Towns", "chevy-plow", "",
         "Local crews based in North Andover, MA, serving commercial and residential properties in these communities.", [("Check my address", "/contact/")], small=True)
a += sec("<h2>Cities we serve</h2>" + cards([(f"{cty}, MA", f"Snow and ice removal for businesses and homes in {cty}.", "pin") for cty in CITIES], 4))
a += sec(mapbox("Where we are", "Based in North Andover, MA 01845."), "cream")
a += cta("Don't see your town?", "Tell us the address. If we cover it, you get a plan before the first storm.", [("Ask about your address", "/contact/")])
page("/service-areas/", "areas", "Snow Removal Service Areas | Essex County, MA | New England Snow Removal",
     "We clear snow in Haverhill, Methuen, Lawrence, North Andover, Groveland, Georgetown, Boxford and Andover, MA.", a)

# ---- ABOUT
ab = hero("About New England Snow Removal", "Snow Removal", "street-shoveling", "", "A local team that keeps Essex County properties open when it snows.", small=True)
ab += sec(split(eb("Who we are") + "<h2>Who we are</h2><p class=\"lead\">New England Snow Removal is based in North Andover, MA, and is part of New England Carpenters, the local team known for building decks and porches, serving Massachusetts since 2016.</p>"
                "<p class=\"lead\">Our crews are experienced local professionals who live and work in the communities we serve.</p>", pic("truck-road")))
ab += sec("<h2>How we work</h2>" + cards([("Reliable", "We show up when the snow falls.", "clock"), ("Safe", "Clear surfaces and ice control that protect people.", "shield"),
            ("Communicative", "You can reach a real person, any way you prefer.", "chat"), ("Local", "Our crews live and work in the communities we serve.", "pin")], 4), "cream")
ab += sec(split("<h2>Meet Max</h2><p class=\"lead\">Max is our mascot and our fastest way to reach us. See him in the corner of the page? Click and send us a message.</p>" + btns([("Say hi on WhatsApp", WA)]),
                '<div class="pic-max"><img src="/assets/img/max-contato.webp" alt="Max, our mascot" width="300" height="400" loading="lazy"></div>', rev=True))
ab += sec("<h2>More from our family of companies</h2>" + '<div class="grid c2"><div class="card"><h3>New England Carpenters</h3><p>Discover more services.</p><a class="more" href="https://newenglandcarpenters.com/" target="_blank" rel="noopener">newenglandcarpenters.com →</a></div>'
            '<div class="card"><h3>Deck &amp; Porch</h3><p>Custom decks and porches.</p><a class="more" href="https://deck.newenglandcarpenters.com/" target="_blank" rel="noopener">deck.newenglandcarpenters.com →</a></div></div>', "cream")
ab += cta("Ready for a free quote?")
page("/about/", "about", "About New England Snow Removal | North Andover, MA",
     "Meet the local team behind New England Snow Removal, part of New England Carpenters in North Andover, MA.", ab)

# ---- OUR WORK
GAL = [("hero-adobestock", "Commercial", "Shopping center parking lot, Methuen, MA"), ("chevy-plow", "Commercial", "Warehouse truck court, Lawrence, MA"),
       ("street-shoveling", "Residential", "Driveway and front steps, North Andover, MA"), ("fisher-plow", "Commercial", "Condo entrance, Andover, MA"),
       ("deck-woman", "Stairs, decks and porches", "Deck, Boxford, MA"), ("shoveling-man", "Residential", "Sidewalk, Haverhill, MA"),
       ("red-plow", "Commercial", "Plow route, Georgetown, MA"), ("truck-forest", "Commercial", "Access road, Groveland, MA")]
cats = ["All", "Commercial", "Residential", "Stairs, decks and porches"]
fl = "".join(f'<button type="button" class="pill{" on" if i == 0 else ""}" data-filter="{"all" if i == 0 else e(cat)}" aria-pressed="{"true" if i == 0 else "false"}">{e(cat)}</button>' for i, cat in enumerate(cats))
fig = "".join(f'<figure data-cat="{e(cat)}">{img(b, ALT[b], sizes="(max-width: 800px) 50vw, 270px")}<figcaption>{e(cap)}</figcaption></figure>' for b, cat, cap in GAL)
w = hero("Our Work", "Our Work", "hero-adobestock", "", "Real properties, cleared and ready. A look at what we do when it snows.", small=True)
w += sec(f'<h2>Gallery</h2><div class="filters">{fl}</div><div class="gal">{fig}</div>')
w += cta("Want your property to look like this after the storm?")
page("/our-work/", "work", "Our Work | Snow Removal in Essex County, MA | New England Snow Removal",
     "See how we keep parking lots, entrances, driveways and walkways clear across Essex County, MA.", w)

# ---- BLOG
POSTS = [
 ("how-to-get-your-parking-lot-ready-for-the-first-snowfall", "How to get your parking lot ready for the first snowfall", "truck-forest",
  "A short checklist for property managers: mark hazards, clear vehicles and set your plan before the first storm.",
  [("Walk the site before winter", "Look at the lot the way a plow driver will. Note curbs, drains, speed bumps, bollards, light poles and any spot where water pools and later turns to ice."),
   ("Mark what the snow will hide", "Use stakes or reflectors for edges, hydrants and fixed obstacles so crews can work quickly and safely, and so nothing gets damaged."),
   ("Plan where the snow goes", "Decide in advance where plowed snow can be stacked without blocking entrances, parking spaces, drains or sight lines."),
   ("Set your plan in writing", "Agree on the depth that triggers a visit, what gets cleared first (entrances, accessible spaces, walkways) and how early the site has to be open."),
   ("Keep vehicles and dumpsters out of the way", "Ask tenants and staff to move vehicles from areas to be plowed, and keep dumpsters in a fixed, marked spot.")]),
 ("brine-vs-rock-salt-what-is-the-difference", "Brine vs. rock salt: what is the difference?", "shovel-closeup",
  "Why applying brine before a storm helps keep ice from bonding to pavement, and when salt still makes sense.",
  [("What brine does", "Brine is salt dissolved in water. Applied before a storm, it helps keep snow and ice from bonding to the pavement, which makes plowing easier and the surface safer."),
   ("What rock salt does", "Rock salt is applied after snow falls to melt ice and snow already on the surface. It needs moisture to start working and works more slowly in very cold weather."),
   ("Using both", "Many properties use brine ahead of the storm and salt afterward where ice has formed. Applying the right amount matters: too little leaves ice, too much wastes material and can damage surfaces and plants."),
   ("What to ask your contractor", "Ask when they apply anti-icing, how they measure the amount of material and how they record each visit.")]),
 ("per-visit-or-seasonal-snow-plan-which-is-better", "Per-visit or seasonal snow plan: which is better?", "truck-road",
  "How to choose the option that fits your property and your budget.",
  [("Two ways to pay", "Every winter, property owners face the same question: pay for each storm, or lock in a plan for the whole season? Both work. The right choice depends on your property and how you want to manage your budget."),
   ("Per-visit service", "You pay each time we clear your property. It suits small sites and owners who prefer to pay only when it snows. The cost changes with the weather, and a heavy winter can add up."),
   ("Seasonal plan", "You agree on one price for the whole winter. It suits businesses that cannot afford a closed lot and owners who want a predictable budget. We also plan your site before the first storm."),
   ("How to choose", "Choose per-visit if the property is small and you can be flexible. Choose seasonal if safe access is critical for customers, employees or deliveries. Not sure? Send us the address and we will recommend an option, free of charge.")]),
]
cardsb = "".join(f'<article class="card post">{img(b, ALT[b], sizes="(max-width: 800px) 100vw, 360px")}<div class="body"><div class="meta">Tips</div><h3><a href="/blog/{slug}/" style="text-decoration:none">{e(t)}</a></h3><p>{e(ex)}</p><a class="more" href="/blog/{slug}/">Read more →</a></div></article>' for slug, t, b, ex, _ in POSTS)
bl = hero("Snow Removal Tips and News", "Tips and News", "truck-forest", "", "Practical advice to help you get through winter with a clear, safe property.", small=True)
bl += sec(f'<h2>Latest articles</h2><div class="grid c3">{cardsb}</div>')
bl += cta("Ready for a free quote?")
page("/blog/", "blog", "Snow Removal Tips and News | New England Snow Removal", "Practical snow and ice advice for property managers and homeowners in Essex County, MA.", bl)
for slug, t, b, ex, secs in POSTS:
    body = "".join(f"<h3>{e(h)}</h3><p>{e(p)}</p>" for h, p in secs)
    art = (f'<div class="article"><div class="crumbs"><a href="/blog/">Blog</a> / {e(t)}</div><h1 style="font-size:36px;text-transform:uppercase;font-weight:800;line-height:1.15;color:#111">{e(t)}</h1>'
           f'<div class="pic" style="margin:26px 0">{img(b, ALT[b], eager=True, sizes="(max-width: 800px) 100vw, 760px")}</div><p class="lead" style="margin-top:0">{e(ex)}</p>{body}'
           f'{btns([("Get a Free Quote", "/contact/"), ("Back to blog", "/blog/")])}</div>')
    ld = {"@context": "https://schema.org", "@type": "Article", "headline": t, "description": ex, "image": f"{SITE}/assets/img/{b}.webp",
          "author": {"@type": "Organization", "name": NAME}, "publisher": {"@type": "Organization", "name": NAME, "logo": {"@type": "ImageObject", "url": SITE + "/assets/img/icon-512.png"}},
          "mainEntityOfPage": f"{SITE}/blog/{slug}/", "dateModified": TODAY}
    page(f"/blog/{slug}/", "blog", t if len(t) + len(NAME) > 62 else f"{t} | {NAME}", ex, sec(art), schema=ld, og_type="article")

# ---- CONTACT
ct = hero("Get a Free Snow Removal Quote", "Free Snow Removal Quote", "shoveling-man", "Contact New England Snow Removal", "Fill out the form and we will personally reach out.", small=True)
ct += sec("<h2>What happens next</h2>" + steps([("You send the details", "The address, the surfaces and how early the site has to be open."), ("We write the plan", "What triggers a visit, what gets cleared first."),
            ("You agree the price", "Per visit or for the whole season.")]) + pills(["Free estimate", "Fast reply"]))
ct += sec('<div style="max-width:760px;margin:0 auto"><h2>Fill out the form and contact us</h2><p class="lead" style="margin-bottom:26px">It takes a minute. We reply fast.</p>' + quote_form("Request a free quote") + '</div>', "cream", sid="quote")
ct += sec("<h2>If you prefer, choose your preferred contact method below.</h2>" +
          f'<div class="grid c4"><a class="card center" href="{WA}" target="_blank" rel="noopener" style="text-decoration:none"><div class="ico" style="margin:0 auto">{svg("chat")}</div><h3>WhatsApp</h3><p>{PHONE}</p></a>'
          f'<a class="card center" href="{SMS}" style="text-decoration:none"><div class="ico" style="margin:0 auto">{svg("chat")}</div><h3>SMS</h3><p>{PHONE}</p></a>'
          f'<a class="card center" href="tel:{TEL}" style="text-decoration:none"><div class="ico" style="margin:0 auto">{svg("phone")}</div><h3>Phone</h3><p>{PHONE}</p></a>'
          f'<a class="card center" href="mailto:{EMAIL}" style="text-decoration:none"><div class="ico" style="margin:0 auto">{svg("mail")}</div><h3>Email</h3><p>{EMAIL}</p></a></div>'
          f'<p class="lead center" style="font-size:14px">{ADDR} · <a href="{FB}" target="_blank" rel="noopener">Facebook</a> · <a href="{IG}" target="_blank" rel="noopener">Instagram</a></p>', center=True)
ct += sec("<h2>Helpful to include</h2>" + pills(["The site address", "Which surfaces: lot, walkways, drive lanes", "How early it has to be open", "Per visit or seasonal"]), "cream")
ct += sec(mapbox("Find us", "North Andover, Massachusetts 01845"))
page("/contact/", "contact", "Free Snow Removal Quote | New England Snow Removal", "Request a free snow removal quote in Essex County, MA. Call, text, WhatsApp, email or fill out the form.", ct)

# ---- THANK YOU / 404
ty = sec(f'<div class="thanks"><img src="/assets/img/max-contato.webp" alt="Max, our mascot" width="300" height="400"><h1 style="font-size:40px;text-transform:uppercase;font-weight:800;color:#111;margin-top:10px">Thank you! We got your request.</h1>'
         f'<p class="lead">We\'ll review the details and get back to you with your free quote, fast. Need us sooner?</p>{btns([("Chat on WhatsApp · " + PHONE, WA)])}</div>')
page("/thank-you/", "contact", "Thank you | New England Snow Removal", "Thank you for contacting New England Snow Removal.", ty, noindex=True)
nf = sec('<div class="thanks"><h1 style="font-size:40px;text-transform:uppercase;font-weight:800;color:#111">Page not found</h1><p class="lead">The page you are looking for does not exist or was moved.</p>' + btns([("Back to home", "/"), ("Get a Free Quote", "/contact/")]) + '</div>')
page("/404.html", "home", "Page not found | New England Snow Removal", "Page not found.", nf, noindex=True)

# ---- LEGAL
def legal(title, intro, secs):
    h = f'<div class="legal"><h1>{e(title)}</h1><p>{e(intro)}</p>' + "".join(
        f'<h2>{e(t)}</h2>' + "".join(f'<p>{e(p)}</p>' if isinstance(p, str) else '<ul>' + "".join(f'<li>{e(x)}</li>' for x in p) + '</ul>' for p in ps) for t, ps in secs) + '</div>'
    return sec(h)
PRIV = [("1. Information we collect", ["Information you give us: name, email, phone number, property address, property type and the message you send through our quote form, WhatsApp, SMS, phone or email.",
          "Information collected automatically: device and browser type, pages visited and approximate location, through cookies and analytics tools."]),
        ("2. How we use it", [["To respond to you: prepare quotes, schedule services and answer questions.", "To run and improve our business: understand how the site is used and improve our services and marketing.", "To communicate: send service updates, such as storm notices. We only send marketing messages if you agree to receive them."]]),
        ("3. Text messages and calls", ["If you give us your phone number, you agree that we may contact you by call, text or WhatsApp about your request. Message and data rates may apply. You can reply STOP at any time to stop text messages."]),
        ("4. Sharing", ["We do not sell your personal information. We share it only with service providers that help us operate (for example website hosting, form handling, email, analytics and advertising platforms), and when the law requires it."]),
        ("5. Cookies", ["We use cookies and similar tools for analytics and advertising measurement. You can block or delete cookies in your browser settings."]),
        ("6. Retention and security", ["We keep your information as long as needed to serve you and meet legal obligations, and we use reasonable measures to protect it. No online system is completely secure."]),
        ("7. Your choices", [f"You may ask to access, correct or delete the information we hold about you by contacting us at {EMAIL}."]),
        ("8. Children", ["Our website is not directed to children under 13, and we do not knowingly collect their information."]),
        ("9. Changes and contact", [f"We may update this policy and will post the new date at the top. Questions: {EMAIL} · {PHONE} · {ADDR}."])]
TERMS = [("1. Quotes and services", ["Quotes are free and based on the information you provide (address, surfaces and requirements). The final scope and price are agreed in writing, per visit or for the season, before service begins."]),
         ("2. Weather and service times", ["Snow removal depends on weather, road conditions and safety. We work to clear properties as quickly as conditions allow, but we cannot guarantee exact arrival times, and delays caused by weather or conditions beyond our control are not a breach of agreement."]),
         ("3. Property conditions", ["Please tell us about hazards that are hard to see under snow, such as curbs, drains, irrigation heads, uneven surfaces and loose pavers. Customers are responsible for marking them. Ice control reduces, but cannot eliminate, slip hazards."]),
         ("4. Access and payment", ["You agree to give us reasonable access to the property, including clearing vehicles from areas to be plowed. Payment terms are stated in your written agreement."]),
         ("5. Limitation of liability", ["To the extent permitted by law, our liability is limited to the amount paid for the service in question. We are not liable for indirect or consequential damages."]),
         ("6. Website use", ["Website content is provided for general information and may change without notice. Do not misuse the site or submit false information."]),
         ("7. Governing law and contact", [f"These terms are governed by the laws of the Commonwealth of Massachusetts. Contact: {EMAIL} · {PHONE}."])]
page("/privacy-policy/", "home", "Privacy Policy | New England Snow Removal", "How New England Snow Removal collects, uses and protects your information.",
     legal("Privacy Policy", f"Last updated: October 2026. {NAME} (\"we\", \"us\") respects your privacy. This policy explains what information we collect through this website, how we use it and the choices you have.", PRIV))
page("/terms/", "home", "Terms of Service | New England Snow Removal", "Terms of service for New England Snow Removal.",
     legal("Terms of Service", "Last updated: October 2026. By using this website or requesting our services, you agree to these terms.", TERMS))

# ================================================================ SAÍDA
for path, doc in PAGES:
    target = os.path.join(OUT, "404.html") if path == "/404.html" else os.path.join(OUT, path.strip("/"), "index.html") if path != "/" else os.path.join(OUT, "index.html")
    os.makedirs(os.path.dirname(target), exist_ok=True)
    open(target, "w", encoding="utf8").write(doc)
urls = [p for p, _ in PAGES if p not in ("/404.html", "/thank-you/")]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
    f'  <url><loc>{SITE}{u}</loc><lastmod>{TODAY}</lastmod></url>\n' for u in urls) + '</urlset>\n'
open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf8").write(sm)
open(os.path.join(OUT, "robots.txt"), "w", encoding="utf8").write(f"User-agent: *\nAllow: /\nDisallow: /api/\n\nSitemap: {SITE}/sitemap.xml\n")
print("páginas geradas:", len(PAGES), "| no sitemap:", len(urls))
