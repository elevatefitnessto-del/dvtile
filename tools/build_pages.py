"""Generate the DV Tile service pages, cost guide and portfolio into public/.
Usage: python3 tools/build_pages.py public
Job photos (Recent work) come from tools/data/jobs.json and the service-page
"Recent installations" sections from tools/data/service_recent.json."""
import json, sys, html, os
OUT = sys.argv[1]
O = "https://www.olympiatile.com/en/"
FONTS = "https://fonts.googleapis.com/css2?family=Familjen+Grotesk:wght@400;500;600&family=Pinyon+Script&family=Newsreader:ital,opsz,wght@0,6..72,300..500;1,6..72,300..400&display=swap"
V = "dv8"
PAGE_V = "dv12"
JS_V = "dv11"
HERE = os.path.dirname(os.path.abspath(__file__))
JOBS = json.load(open(os.path.join(HERE, "data", "jobs.json")))
RECENT = json.load(open(os.path.join(HERE, "data", "service_recent.json")))

MARK = ('<svg class="pg-brand__mark" viewBox="0 0 100 100" aria-hidden="true"><defs><clipPath id="pgm"><rect x="4" y="4" width="44.5" height="44.5" rx="1.2"/><rect x="51.5" y="4" width="44.5" height="44.5" rx="1.2"/><rect x="4" y="51.5" width="44.5" height="44.5" rx="1.2"/><rect x="51.5" y="51.5" width="44.5" height="44.5" rx="1.2"/></clipPath></defs>'
        '<g fill="#eceae4"><rect x="4" y="4" width="44.5" height="44.5" rx="1.2"/><rect x="51.5" y="4" width="44.5" height="44.5" rx="1.2"/><rect x="4" y="51.5" width="44.5" height="44.5" rx="1.2"/><rect x="51.5" y="51.5" width="44.5" height="44.5" rx="1.2"/></g>'
        '<g clip-path="url(#pgm)"><path fill="#a9824f" d="M-2 19 C 28 13, 40 38, 50 49 C 60 60, 72 85, 102 79 L 102 83.5 C 69 91, 55 66, 46.5 55 C 37.5 43, 27 21, -2 24.5 Z"/><path fill="#bfa27a" d="M57 -2 C 59 15, 73 25, 102 22 L 102 23.6 C 71 27, 57 17, 55.4 -2 Z"/><path fill="#bfa27a" d="M-2 66 C 14 63, 24 70, 30 102 L 28.4 102 C 22.5 72, 13 65.5, -2 67.6 Z"/></g></svg>')

PAGES = [
 dict(slug="marble-natural-stone-floors", nav="Marble and stone floors", img="marble-floors",
  title="Marble and Natural Stone Floor Installation in Toronto | DV Tile",
  desc="Marble, travertine, limestone and slate floors installed flat and vein-matched for fine homes across Toronto and the GTA. Layouts approved before we cut.",
  h1="Marble and natural stone floors",
  lede="Calacatta, Carrara, Nero Marquina, travertine, limestone and slate, in tile or full slab, laid to a plan you approve before the first cut.",
  alt="Waterjet-cut marble medallion with a brass ring set into a polished Calacatta floor",
  sections=[
   ("What we install", ["Polished, honed and brushed marble in tile and slab formats", "Travertine, limestone and slate floors, filled or open", "Waterjet medallions, borders and inlays, including brass and contrasting stone", "Herringbone, chevron, Versailles and checkerboard patterns", "Thresholds, stair treads and hearths cut from the same stone"]),
   ("How we lay stone", ["We check the subfloor for flatness, deflection and moisture before quoting, because natural stone shows every flaw beneath it.", "You approve a layout drawing showing where joints, cuts and veins fall. For slab and feature floors we dry-lay pieces so you can see the veining before anything is set.", "Stone goes down over an uncoupling membrane where the substrate calls for it, with full mortar coverage so the floor sounds solid and edges sit flat.", "Joints are grouted and the stone sealed for the finish and room, and you receive care instructions for that material."]),
  ],
  olympia=[("Natural stone", "tile-stone/explore-by-look/natural-stone.html"), ("Marble slabs", "slab-division/explore-by-material/marble.html"), ("Limestone slabs", "slab-division/explore-by-material/limestone.html"), ("Travertine slabs", "slab-division/explore-by-material/travertine.html")],
  faq=[("Can marble go in a kitchen or entry?", "Yes, with the right finish. Honed marble hides wear and etching better than polished; we talk through finish and sealing for each room at the site assessment."),
       ("Do you install marble over in-floor heating?", "Yes. Heating mats go in first, are tested with the thermostat, and the stone is set over an uncoupling layer so the heat cycle does not crack joints.")]),
 dict(slug="porcelain-slab-installation", nav="Porcelain slabs and large format", img="porcelain-slab",
  title="Large-Format Porcelain and Slab Installation in Toronto | DV Tile",
  desc="Porcelain panels up to 160 x 320 cm installed on floors, walls and fireplaces across Toronto and the GTA, with lippage held under a millimetre.",
  h1="Large-format porcelain and slabs",
  lede="Panels up to 160 × 320 cm on floors, walls, fireplaces and showers, with lippage held under a millimetre across the room.",
  alt="Kitchen with a leathered granite island, full-height quartzite backsplash and large-format porcelain floor",
  sections=[
   ("What we install", ["Large-format floor tile from 24 × 48 in up", "Porcelain slabs as wall cladding, shower walls and fireplace surrounds", "Book-matched porcelain feature walls", "Thin porcelain panels over existing surfaces where the substrate allows", "Outdoor 2 cm porcelain pavers"]),
   ("Why large format needs a different crew", ["Big panels magnify any unevenness in the floor or wall, so we flatten the substrate first rather than relying on mortar to hide it.", "Each panel is back-buttered and set with a levelling system for full coverage and even edges.", "Slabs are moved and set with suction lifters and slab carts, so corners and edges arrive undamaged.", "We plan cuts and seams on a drawing so joints line up with cabinetry, windows and fixtures."]),
  ],
  olympia=[("Porcelain", "tile-stone/explore-by-material/porcelain.html"), ("Marble-look porcelain", "tile-stone/explore-by-look/stone-replica/marble-replica.html"), ("Floor tiles", "tile-stone/explore-by-use/floors.html"), ("Wall tiles", "tile-stone/explore-by-use/wall-tiles.html")],
  faq=[("What is lippage and why does it matter?", "Lippage is the height difference between neighbouring tiles. With large panels and raking light from big windows, even a small step catches the eye. We aim for under a millimetre."),
       ("Can porcelain slabs go in a shower?", "Yes. Slabs make a shower wall with very few joints. They go over a waterproofing membrane that is flood-tested before tile.")]),
 dict(slug="shower-installation", nav="Showers and wet rooms", img="showers",
  title="Custom Shower and Wet Room Tile Installation in Toronto | DV Tile",
  desc="Curbless showers, linear drains, custom niches, benches and steam rooms, waterproofed and flood-tested before tile, for homes across Toronto and the GTA.",
  h1="Showers and wet rooms",
  lede="Curbless entries, linear drains, custom niches, benches and steam showers, waterproofed and flood-tested before a single tile goes on.",
  alt="Custom recessed shower niche in marble with a warm LED strip and a brushed brass shower valve",
  sections=[
   ("What we build", ["Curbless and walk-in showers with linear drains", "Custom recessed niches, mitred at the corners and lit with LED where you want it", "Built-in benches and ledges in tile, slab or solid stone", "Steam showers with sloped ceilings and vapour-tight assemblies", "Shower jambs and thresholds in solid stone"]),
   ("Waterproofing first", ["We build the shower pan to slope correctly to the drain and install a bonded waterproofing membrane over the walls and floor.", "The pan is flood-tested and left to stand before any tile is installed, so a problem shows up while it is cheap to fix.", "Niches and benches are framed and waterproofed as part of the same system, not added afterwards.", "We coordinate with your plumber on valve, rainhead and drain positions so tile layout and fixtures line up."]),
  ],
  olympia=[("Shower tiles", "tile-stone/explore-by-use/shower.html"), ("Shower jambs", "tile-stone/explore-by-use/shower-jambs.html"), ("Mosaics", "tile-stone/explore-by-look/mosaics.html"), ("Bathroom tiles", "tile-stone/explore-by-use/bathroom.html")],
  faq=[("Do you install the plumbing fixtures?", "We install the tile, stone and waterproofing and work alongside your plumber, who installs valves, rainheads and drains."),
       ("Can you add LED lighting to a niche?", "Yes. We plan the LED channel when the niche is framed so the light is hidden and the strip sits behind waterproofing. Your electrician makes the connection.")]),
 dict(slug="kitchen-backsplash-installation", nav="Kitchen backsplashes", img="backsplash",
  title="Kitchen Backsplash and Feature Wall Installation in Toronto | DV Tile",
  desc="Full-height slab, zellige, mosaic and 3D tile backsplashes installed with outlets, windows and hoods scribed in, for kitchens across Toronto and the GTA.",
  h1="Kitchen backsplashes and feature walls",
  lede="Full-height slab, zellige, mosaic and 3D tile, with outlets, window returns and range hoods scribed in rather than worked around.",
  alt="Book-matched quartzite kitchen backsplash washed by a warm LED strip under a stone ledge, with a brass pot filler",
  sections=[
   ("What we install", ["Full-height slab backsplashes in natural stone or porcelain, book-matched where the stone allows", "Handmade zellige and glazed tile", "Mosaics, subway and herringbone patterns", "3D and fluted decorative tile", "Stone ledges and shelves with space for hidden LED strips"]),
   ("Details that make a backsplash look built in", ["We set out the layout from the focal point, usually the range or sink, so cuts land evenly at the ends.", "Outlets and switches are cut cleanly in the tile or slab, with box extenders where needed.", "Window returns and the underside of hoods are finished in the same material, not left with exposed edges.", "Edges meet cabinets and counters with a consistent joint or a metal trim you choose in advance."]),
  ],
  olympia=[("Backsplash tiles", "tile-stone/explore-by-use/backsplash.html"), ("Kitchen tiles", "tile-stone/explore-by-use/kitchen.html"), ("3D decor", "tile-stone/explore-by-look/3d.html"), ("Quartzite slabs", "slab-division/explore-by-material/quartzite.html")],
  faq=[("Can the backsplash match my stone countertop?", "Yes. If your countertop fabricator supplies slab offcuts or extra slab, we can install a matching full-height backsplash."),
       ("How long does a backsplash take?", "It depends on size and material. We give you a schedule in writing with the quote after the site assessment.")]),
 dict(slug="heated-floor-installation", nav="Heated floors", img="heated-floors",
  title="Heated Marble and Tile Floor Installation in Toronto | DV Tile",
  desc="Electric in-floor heating installed under marble, natural stone and porcelain, tested with the thermostat before the floor is set, across Toronto and the GTA.",
  h1="Heated floors under stone and tile",
  lede="Electric in-floor heating under marble, natural stone and porcelain, installed and tested before the floor is set.",
  alt="Marble ensuite at night lit by LED under the vanity, reflected in a polished stone floor",
  sections=[
   ("What we install", ["Electric heating mats and cables for bathrooms, kitchens, entries and mudrooms", "Uncoupling and heating membranes that combine both layers", "Thermostats and floor sensors placed for your electrician to connect", "Heated shower floors and benches where the system allows"]),
   ("How we install it", ["We lay out heating to cover the walkable floor and avoid areas under cabinets and tubs.", "Resistance is tested when the mat arrives, after it is laid, and after it is covered, so a damaged wire is caught before the stone goes on.", "A licensed electrician makes the final connection to the thermostat.", "The stone or tile is set over the system with full coverage, then the heat is brought up gradually once the mortar has cured."]),
  ],
  olympia=[("Floor tiles", "tile-stone/explore-by-use/floors.html"), ("Natural stone", "tile-stone/explore-by-look/natural-stone.html"), ("Bathroom tiles", "tile-stone/explore-by-use/bathroom.html")],
  faq=[("Is heated flooring safe under marble?", "Yes, when it is installed with an uncoupling layer and the heat is introduced slowly after curing. Stone holds and spreads heat well."),
       ("Can heating be added to an existing floor?", "Not under a floor that stays. Heating goes in during a new floor installation, so it is best planned with the renovation.")]),
 dict(slug="outdoor-stone-terraces-pools", nav="Terraces and pools", img="outdoor-stone",
  title="Outdoor Stone Terraces and Pool Surrounds in Toronto | DV Tile",
  desc="Thermal limestone, flamed granite and 2 cm porcelain on terraces, steps and pool surrounds, built for freeze and thaw across Toronto and the GTA.",
  h1="Terraces, pools and outdoor stone",
  lede="Thermal limestone, flamed granite and 2 cm outdoor porcelain on terraces, steps and pool surrounds, built to handle Toronto’s freeze and thaw.",
  alt="Limestone pool coping and flamed granite steps with LED step lights beside a lit pool at dusk",
  sections=[
   ("What we install", ["Terraces and patios in natural stone or 2 cm porcelain pavers", "Pool coping and pool surrounds", "Exterior steps with solid treads, including recesses for LED step lights", "Balconies and rooftop terraces on pedestals where the structure allows"]),
   ("Built for winter", ["We choose materials rated for freeze and thaw and slip resistance outdoors, and confirm them with you before ordering.", "Surfaces are sloped to drain away from the house and pool.", "Stone is set on a base designed for outdoor movement, with joints planned for expansion.", "We seal stone where the material calls for it and explain winter care, including which de-icers to avoid."]),
  ],
  olympia=[("Outdoor tiles", "tile-stone/explore-by-use/outdoors.html"), ("Pool tiles", "tile-stone/explore-by-use/pool.html"), ("Flamed finishes", "slab-division/explore-by-finish/flamed.html"), ("Granite slabs", "slab-division/explore-by-material/granite.html")],
  faq=[("Which stone works best outdoors in Toronto?", "Dense stones with a textured finish, such as thermal limestone and flamed granite, and 2 cm porcelain pavers rated for freeze and thaw. We confirm ratings for each product."),
       ("Can LED step lights be built into stone steps?", "Yes. We plan recesses in the risers or treads when the steps are laid out; your electrician wires them.")]),
 dict(slug="stone-restoration-polishing", nav="Restoration and polishing", img="restoration",
  title="Marble and Stone Floor Restoration and Polishing in Toronto | DV Tile",
  desc="Honing, polishing, crack repair, regrouting and sealing for marble and natural stone floors that have lost their finish, across Toronto and the GTA.",
  h1="Stone restoration and polishing",
  lede="Honing, polishing, crack and chip repair, regrouting and sealing for marble and stone floors that have lost their finish.",
  alt="Herringbone limestone floor meeting a polished Calacatta Viola marble hearth along a brass strip",
  sections=[
   ("What we restore", ["Dull, etched or scratched marble and limestone", "Uneven tiles where edges have worn proud", "Cracked or chipped stone, filled and colour-matched", "Stained or failing grout, cleaned or replaced", "Stone that needs resealing after cleaning"]),
   ("How restoration works", ["We assess the stone, finish and damage on site and test a small area so you can see the result before we start.", "Floors are ground flat where needed, honed through progressively finer grits, then polished or left honed to suit the room.", "Repairs are filled with colour-matched resin and blended into the surrounding stone.", "The floor is sealed and you receive care instructions to keep the finish longer."]),
  ],
  olympia=[("Marble slabs", "slab-division/explore-by-material/marble.html"), ("Honed finish", "slab-division/explore-by-finish/honed.html"), ("Polished finish", "slab-division/explore-by-finish/polished.html")],
  faq=[("Can etching from acids be removed?", "Usually. Light etching can be honed and polished out. Deep damage may need grinding, which we assess on site."),
       ("Can you match a replacement tile?", "We try to match from the same stone type and finish. Natural stone varies, so we show you the replacement before setting it.")]),
]

EXTRA = {
 "marble-floors": [("marble-floors-a", "Large-format polished marble floor through an entry hall"), ("marble-floors-b", "Large-format polished marble floor in a bright kitchen")],
 "porcelain-slab": [("porcelain-slab-a", "Book-matched porcelain slab fireplace wall over a large-format floor"), ("porcelain-slab-b", "Bathroom clad in large porcelain slabs with very few seams")],
 "showers": [("showers-a", "Curbless marble slab shower with an LED niche and brass linear drain"), ("showers-b", "White tile steam shower with marble benches and an LED cove")],
 "backsplash": [("backsplash-a", "Green handmade tile backsplash with open oak shelves"), ("backsplash-b", "Full-height marble slab backsplash behind a professional range")],
 "heated-floors": [("heated-floors-a", "Heated honed marble floor in a winter ensuite"), ("heated-floors-b", "Heated slate-look floor in a winter mudroom")],
 "outdoor-stone": [("outdoor-stone-a", "Flagstone terrace with a fire table at dusk"), ("outdoor-stone-b", "Pale stone pavers and coping around a backyard pool")],
 "restoration": [("restoration-a", "Polished marble foyer floor with a mirror finish"), ("restoration-b", "Honed and sealed travertine hallway floor")],
}

COST = [
 ("Porcelain and ceramic floor tile", "$10–$40 per sq ft", "Tile choice, pattern and floor preparation"),
 ("Large-format porcelain (24 × 48 in and up)", "$19–$25 per sq ft plus levelling", "Panel size, substrate flatness, handling"),
 ("Porcelain slab walls and floors", "$45–$90 per sq ft", "Slab size, seams, cut-outs, access"),
 ("Marble and natural stone floors", "$25–$50 per sq ft", "Stone, finish, pattern, sealing"),
 ("Custom shower (tile and waterproofing)", "$3,500–$8,000+", "Size, curbless entry, niches, benches, slab vs tile"),
 ("Heated floor system", "$12–$20 per sq ft", "Room size, thermostat, membrane"),
 ("Kitchen backsplash", "$800–$5,000", "Area, material, slab vs tile, outlets and windows"),
]

def head(title, desc, canon, extra_ld):
    return f'''<!doctype html>
<html lang="en-CA">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(desc)}">
  <meta name="theme-color" content="#14201d">
  <link rel="canonical" href="https://dvtile.ca/{canon}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="DV Tile | Don Valley Tile">
  <meta property="og:title" content="{html.escape(title)}">
  <meta property="og:description" content="{html.escape(desc)}">
  <meta property="og:url" content="https://dvtile.ca/{canon}">
  <meta property="og:image" content="https://dvtile.ca/assets/og.jpg">
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preload" as="style" href="{FONTS}" onload="this.onload=null;this.rel='stylesheet'">
  <noscript><link rel="stylesheet" href="{FONTS}"></noscript>
  <link rel="stylesheet" href="/styles.css?v={V}">
  <link rel="stylesheet" href="/site.css?v={V}">
  <link rel="stylesheet" href="/page.css?v={PAGE_V}">
  <script type="application/ld+json">{json.dumps(extra_ld, ensure_ascii=False)}</script>
</head>
<body class="pg">
  <a class="skip" href="#main">Skip to content</a>
  <header class="pg-nav">
    <a class="pg-brand" href="/">{MARK}<span class="pg-brand__words"><span class="pg-brand__name">DV TILE</span> <span class="pg-brand__script">Don Valley Tile</span></span></a>
    <nav class="pg-nav__links" aria-label="Primary">
      <a href="/portfolio">Portfolio</a>
      <a href="/inspiration">Inspiration</a>
      <a href="/#services">Services</a>
      <a href="/#materials">Products</a>
      <a href="/cost-guide">Cost guide</a>
    </nav>
    <a class="pg-tel" href="tel:+14379292563">437-929-2563</a>
    <a class="pg-cta" href="/#contact">Book a site assessment</a>
  </header>
'''

def foot():
    links = "".join(f'<li><a href="/{p["slug"]}">{p["nav"]}</a></li>' for p in PAGES)
    return f'''  <footer class="pg-foot">
    <div class="pg-foot__inner">
      <div>
        <p class="footer__mark">DV TILE</p>
        <p class="footer__script">Don Valley Tile</p>
        <p class="pg-foot__addr">44 Jackes Avenue, Toronto, Ontario</p>
        <p class="pg-foot__addr">Call or text <a href="tel:+14379292563">437-929-2563</a></p>
      </div>
      <nav aria-label="Services"><p class="pg-foot__h">Services</p><ul>{links}<li><a href="/cost-guide">Toronto cost guide</a></li><li><a href="/portfolio">Portfolio</a></li><li><a href="/inspiration">Inspiration</a></li></ul></nav>
    </div>
    <p class="legal">DV Tile is operated by 1000508858 Ontario Inc. Images on this page are concept renderings of finishes we install.</p>
  </footer>
</body>
</html>
'''

def crumbs(name, slug):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "DV Tile", "item": "https://dvtile.ca/"},
        {"@type": "ListItem", "position": 2, "name": name, "item": f"https://dvtile.ca/{slug}"}]}

def figure(img, alt):
    return f'''    <figure class="pg-hero__fig">
      <img src="/assets/services/{img}-800.webp" srcset="/assets/services/{img}-800.webp 800w, /assets/services/{img}.webp 1600w" sizes="(max-width: 960px) 100vw, 1200px" width="1600" height="905" alt="{html.escape(alt)}" fetchpriority="high">
      <figcaption>Concept rendering</figcaption>
    </figure>'''

def cta():
    return '''    <section class="pg-cta-band">
      <h2>Book a site assessment</h2>
      <p>We measure, check the floor and walls, talk through materials and your schedule, then send a written, line-itemed quote and a layout drawing.</p>
      <a class="btn" href="/#contact">Request a site assessment</a>
    </section>'''

for p in PAGES:
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Service", "name": p["h1"], "serviceType": p["nav"], "description": p["desc"],
         "provider": {"@type": "HomeAndConstructionBusiness", "@id": "https://dvtile.ca/#business", "name": "DV Tile"},
         "areaServed": "Toronto and the Greater Toronto Area"},
        crumbs(p["nav"], p["slug"]),
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faq"]]}]}
    secs = ""
    for i, (h, items) in enumerate(p["sections"]):
        tag = "ol" if i == 1 else "ul"
        secs += f'''    <section class="pg-sec">
      <h2>{h}</h2>
      <{tag} class="pg-list{' pg-list--steps' if tag == 'ol' else ''}">{''.join(f'<li>{html.escape(x)}</li>' for x in items)}</{tag}>
    </section>
'''
    oly = "".join(f'<li><a href="{O}{u}" rel="noopener" target="_blank">{n}</a></li>' for n, u in p["olympia"])
    faqs = "".join(f'<details class="faq__item"><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>' for q, a in p["faq"])
    related = "".join(f'<li><a href="/{r["slug"]}">{r["nav"]}</a></li>' for r in PAGES if r is not p)
    if p["slug"] in RECENT:
        secs += RECENT[p["slug"]]["html"]
    extra = EXTRA.get(p["img"], [])
    if extra:
        figs = "".join(f'<figure><img src="/assets/services/{k}-800.webp" srcset="/assets/services/{k}-800.webp 800w, /assets/services/{k}.webp 1344w" sizes="(max-width: 700px) 100vw, 50vw" width="1344" height="768" alt="{html.escape("AI-generated design concept. " + a)}" loading="lazy" decoding="async"><figcaption>{html.escape("AI-generated design concept. " + a)}</figcaption></figure>' for k, a in extra)
        secs += f'''    <section class="pg-sec pg-sec--more">
      <h2>More examples</h2>
      <div class="pg-more">{figs}</div>
      <p class="pg-more__note">AI-generated design concept. Not a completed DV Tile installation.</p>
    </section>
'''
    body = f'''  <main id="main" class="pg-main">
    <nav class="pg-crumbs" aria-label="Breadcrumb"><a href="/">DV Tile</a><span aria-hidden="true">/</span><span aria-current="page">{p["nav"]}</span></nav>
    <header class="pg-hero">
      <h1>{p["h1"]}</h1>
      <p class="pg-lede">{html.escape(p["lede"])}</p>
      <a class="btn" href="/#contact">Book a site assessment</a>
    </header>
{figure(p["img"], p["alt"])}
    <div class="pg-body">
{secs}    <section class="pg-sec pg-sec--olympia">
      <h2>Choose from the Olympia range</h2>
      <p>As an installation partner of Olympia Tile + Stone, we order, deliver and install anything in their catalogue. Start with these collections:</p>
      <ul class="pg-chips">{oly}</ul>
    </section>
    <section class="pg-sec">
      <h2>Questions</h2>
      <div class="faq__list">{faqs}</div>
    </section>
    </div>
{cta()}
    <nav class="pg-related" aria-label="Other services"><h2>Other services</h2><ul>{related}</ul></nav>
  </main>
'''
    page = head(p["title"], p["desc"], p["slug"], ld) + body + foot()
    if p["slug"] in RECENT:
        page = page.replace("Images on this page are concept renderings of finishes we install.", "Recent installations are photographs of DV Tile jobs. The other images are concept renderings or AI-generated design concepts, not completed installations.")
    open(f'{OUT}/{p["slug"]}.html', 'w').write(page)

# Cost guide
ld = {"@context": "https://schema.org", "@graph": [
    {"@type": "Article", "headline": "What tile and stone installation costs in Toronto (2026)", "author": {"@type": "Organization", "name": "DV Tile"}, "publisher": {"@id": "https://dvtile.ca/#business"}, "datePublished": "2026-11-09", "image": "https://dvtile.ca/assets/services/cost-guide.webp"},
    crumbs("Cost guide", "cost-guide")]}
rows = "".join(f'<tr><th scope="row">{a}</th><td>{b}</td><td>{c}</td></tr>' for a, b, c in COST)
body = f'''  <main id="main" class="pg-main">
    <nav class="pg-crumbs" aria-label="Breadcrumb"><a href="/">DV Tile</a><span aria-hidden="true">/</span><span aria-current="page">Cost guide</span></nav>
    <header class="pg-hero">
      <h1>What tile and stone installation costs in Toronto</h1>
      <p class="pg-lede">Typical installed price ranges published across the Toronto and GTA market in 2026, what moves a project up or down, and how to compare quotes.</p>
    </header>
{figure("cost-guide", "Double-height foyer with a honed Calacatta marble floor and a floating limestone staircase")}
    <div class="pg-body">
    <section class="pg-sec">
      <h2>Typical market ranges, 2026</h2>
      <p>These are ranges commonly published by Toronto and GTA installers in 2026, before HST. They are a guide to the market, not DV Tile prices. Every DV Tile quote is written and line-itemed after a site assessment.</p>
      <div class="pg-table"><table>
        <thead><tr><th scope="col">Work</th><th scope="col">Typical installed range</th><th scope="col">What moves the price</th></tr></thead>
        <tbody>{rows}</tbody>
      </table></div>
    </section>
    <section class="pg-sec">
      <h2>What drives the cost of a luxury floor</h2>
      <ul class="pg-list">
        <li><strong>Floor preparation.</strong> Large panels and stone need a flat, stiff subfloor. Levelling and membranes are often the difference between quotes.</li>
        <li><strong>Material and format.</strong> Book-matched slab, waterjet inlays and fragile stone take longer to plan, move and set than standard tile.</li>
        <li><strong>Layout.</strong> Herringbone, diagonal and vein-matched layouts mean more cuts and more waste than a straight lay.</li>
        <li><strong>Waterproofing.</strong> In showers, a bonded membrane and a flood test add cost and remove most of the risk.</li>
        <li><strong>Access and protection.</strong> Occupied homes, elevators and finished floors elsewhere in the house add protection and handling time.</li>
      </ul>
    </section>
    <section class="pg-sec">
      <h2>How to compare quotes</h2>
      <ol class="pg-list pg-list--steps">
        <li>Ask for a line-item quote that separates preparation, membranes, installation, trims and sealing.</li>
        <li>Ask for a layout drawing showing where joints, cuts and veins fall.</li>
        <li>Ask which waterproofing system will be used and whether the shower is flood-tested before tile.</li>
        <li>Ask for proof of WSIB coverage and liability insurance, and the length of the workmanship warranty, in writing.</li>
        <li>In Ontario, a written estimate cannot be exceeded by more than 10 percent without your consent.</li>
      </ol>
    </section>
    </div>
{cta()}
  </main>
'''
open(f'{OUT}/cost-guide.html', 'w').write(head("Tile and Stone Installation Costs in Toronto (2026) | DV Tile",
    "Typical 2026 installed price ranges for porcelain, large-format, slab, marble, showers, heated floors and backsplashes in Toronto and the GTA, and how to compare quotes.",
    "cost-guide", ld) + body + foot())

# sitemap
urls = ["", "portfolio", "inspiration", *[p["slug"] for p in PAGES], "cost-guide"]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
    f'  <url><loc>https://dvtile.ca/{u}</loc><lastmod>2026-11-09</lastmod></url>\n' for u in urls) + '</urlset>\n'
open(f'{OUT}/sitemap.xml', 'w').write(sm)
print("pages:", len(PAGES) + 1)
print(json.dumps([[p["slug"], p["nav"]] for p in PAGES]))

# ---------- Portfolio ----------
CATS = [("bath", "Bathrooms and showers"), ("kitchen", "Kitchens and backsplashes"), ("floors", "Floors, entries and laundry"), ("living", "Fireplaces and living spaces"), ("outdoor", "Terraces and pools")]
P = {
 1:("bath","Marble slab walls and a freestanding tub in a bay-window ensuite"), 2:("bath","Calacatta slab ensuite with a glass shower and freestanding tub"),
 3:("bath","Green glazed tile powder room with an onyx vessel basin"), 4:("bath","Large-format grey porcelain wet room with a linear drain"),
 5:("bath","Honed stone floor in a ravine-view ensuite"), 6:("bath","Hex mosaic floor and panelled tub in a classic bathroom"),
 7:("bath","Travertine-look tile ensuite with a stone soaking tub"), 8:("bath","Arched stone shower entry in a moody ensuite"),
 9:("bath","Green subway tile and checkerboard floor in a heritage bathroom"), 10:("bath","Curbless large-format shower with a lake view"),
 11:("kitchen","Sage glazed tile backsplash in a bay-window kitchen"), 12:("floors","Hexagon cement-look tile in a mudroom entry"),
 13:("living","Large-format porcelain floor and stone fireplace wall in a family room"), 14:("floors","Zellige backsplash and checkerboard floor in a laundry room"),
 15:("kitchen","Blue fish-scale tile backsplash under a stained-glass window"), 16:("kitchen","Handmade tile backsplash with navy cabinetry"),
 17:("floors","Terracotta tile floor in a lakeside mudroom"), 18:("floors","Flagstone floor and stacked-stone wall in an entry mudroom"),
 19:("living","Stacked-stone bar front over a wood-look porcelain floor"), 20:("kitchen","Green subway tile backsplash with black stone counters"),
 21:("bath","Book-matched marble slab wall behind a freestanding tub"), 22:("kitchen","Leathered grey marble with a mitred waterfall edge"),
 23:("bath","Polished marble floor through a double-vanity ensuite"), 24:("bath","Green zellige shower with twin recessed niches"),
 25:("kitchen","Marble waterfall island on a large-format porcelain floor"), 26:("floors","Pearl mosaic walls and a polished marble corridor"),
 27:("floors","Waterjet marble floor inlay in a grand lobby"), 28:("floors","Polished porcelain floor and stone feature wall in a street-front lobby"),
 29:("outdoor","Indoor pool with stone coping and tiled steps"), 30:("bath","Herringbone floor and glass wet room"),
 31:("outdoor","Large-format limestone terrace in a Toronto front garden"), 32:("outdoor","Freeform pool with natural stone coping and deck"),
 33:("outdoor","Rooftop terrace in large-format porcelain pavers"), 34:("outdoor","Limestone front steps and landing"),
 35:("outdoor","Slate-look porcelain outdoor kitchen terrace"), 36:("outdoor","Encaustic patterned tile under a garden cabana"),
 37:("outdoor","Wood-look porcelain pool deck"), 38:("outdoor","Stone-look porcelain covered dining terrace"),
 39:("outdoor","Pale porcelain pavers around a pool"), 40:("outdoor","Limestone-look terrace with built-in steps"),
 41:("floors","Marble medallion floor in a curved-stair foyer"), 42:("living","Green glazed tile fireplace surround"),
 43:("floors","Marble stair treads and a polished foyer floor"), 44:("bath","Terrazzo-style shower wall with niche and stone tub"),
 45:("living","Terrazzo floor and stone bar in a wine room"), 46:("living","Patterned tile floor in a garden sunroom"),
 47:("floors","Stone floor in a double-height foyer"), 48:("living","Book-matched marble slab fireplace wall"),
 49:("floors","Herringbone stone hallway with a lake view"), 50:("living","Light stone floor in a lakeside sunroom"),
}
WORK = [("pool-terrace","outdoor","Large-format outdoor porcelain pavers and pool coping"),("chevron-shower","bath","Chevron shower wall with recessed niche and linear drain"),
 ("steam-shower","bath","Steam shower in handmade tile, LED under the bench"),("calacatta-viola-wall","bath","Book-matched Calacatta Viola slab feature wall"),
 ("terrazzo-bathroom","bath","Terrazzo floor running into a curbless shower"),("fluted-powder-room","bath","Fluted tile feature wall in a powder room"),
 ("marble-medallion-foyer","floors","Waterjet marble medallion in a polished foyer"),("marble-ensuite","bath","Vein-matched marble slab ensuite"),
 ("slab-kitchen","kitchen","Marble-look slab backsplash and waterfall island"),("condo-fluted-ensuite","bath","Fluted tile wall and marble vanity in a downtown condo ensuite"),
 ("laundry-subway-tile","floors","Handmade subway tile and hex mosaic floor in a laundry room"),("condo-marble-fireplace","living","Book-matched marble slab fireplace overlooking the city"),
 ("herringbone-living","living","Wood-look porcelain laid in herringbone"),("lakeside-porcelain-floor","living","Wood-look porcelain plank floor in a lakeside sunroom")]


P2 = [
 ("q01","kitchen","Handmade white tile backsplash in a garden-view kitchen"),("q02","floors","Geometric patterned tile floor in a mudroom"),
 ("q03","living","Honed stone floor in a walnut wine cellar"),("q04","kitchen","Marble slab backsplash and waterfall island"),
 ("q05","outdoor","Porcelain-paved balcony over Lake Ontario"),("q06","bath","Blue glazed tile shower beside a freestanding tub"),
 ("q07","kitchen","Glass mosaic backsplash behind a range"),("q08","bath","Marble shower with a recessed niche and brass fixtures"),
 ("q09","kitchen","Glazed tile range wall under a plaster hood"),("q10","bath","Green herringbone powder room with a mosaic floor"),
 ("q11","bath","Zellige walls and terrazzo floor in a garden bathroom"),("q12","bath","Marble slab bathroom with a glass shower"),
 ("q13","bath","Marble ensuite with an arched window and freestanding tub"),("q14","bath","Shower with a long LED niche and built-in bench"),
 ("q15","outdoor","Pool pavilion with large-format stone pavers"),("q16","bath","Marble ensuite with brushed brass fixtures"),
 ("q17","bath","Large porcelain slab bathroom with tub and shower"),("q18","living","Herringbone porcelain floor in a wine room"),
 ("q19","outdoor","Indoor-outdoor pool with stone coping"),("q20","bath","Stone-look porcelain bathroom with matte black fixtures"),
 ("q21","bath","Zellige wall and stone pedestal sink"),("q22","floors","Book-matched marble slab walls in a stair hall"),
 ("q23","bath","Terrazzo floor and oak vanity in a ravine-view bathroom"),("q24","floors","Marble slab wall and polished floor in an entry"),
 ("q25","bath","Herringbone shower wall with a teak bench"),("q26","kitchen","Glazed white tile backsplash with open shelves"),
 ("q27","outdoor","Porcelain terrace in the treetops"),("q28","outdoor","Mosaic-tiled plunge pool in a spa room"),
 ("q29","bath","Powder room with a brass mirror and stone vanity"),("q30","floors","Terrazzo floor in a sage green mudroom"),
 ("r01","outdoor","Rooftop terrace and outdoor kitchen facing the CN Tower"),("r02","floors","Patterned cement tile floor in a Toronto mudroom"),
 ("r03","living","Stone fireplace and porcelain floor in a lakeside condo"),("r05","outdoor","Large-format porcelain rooftop terrace at sunset"),
 ("r06","bath","Marble slab shower overlooking the city at sunset"),("r07","bath","Black marble shower with an LED niche"),
 ("r08","bath","Brick loft bathroom with a stone vessel basin"),("r10","bath","Marble ensuite with a lake view"),
 ("r11","floors","Polished marble foyer with a lit stair"),("r12","bath","Marble slab bathroom with a city view in winter"),
 ("r13","living","Large-format stone floor in a private gym"),("r14","floors","Book-matched stone walls in a condo lobby"),
 ("r15","living","Light porcelain floor in a lakeside living room"),("r16","bath","Book-matched marble wall and floating vanity"),
 ("r18","kitchen","Stone island and porcelain backsplash in a condo kitchen"),("r19","bath","Backlit onyx slab wall behind a freestanding tub"),
 ("r20","kitchen","Marble slab kitchen with a lake view"),("r21","bath","Black hex tile powder room with a backlit mirror"),
 ("r22","kitchen","Book-matched marble slab kitchen with brass pendants"),("r23","kitchen","Green glazed tile bar with LED shelving"),
 ("r24","bath","Marble slab shower framing the CN Tower"),("r25","outdoor","Stone-edged infinity pool above the Scarborough Bluffs"),
 ("r26","bath","Checkerboard marble floor and clawfoot tub in a heritage bathroom"),
]
items = [(f"/assets/portfolio/p{i:02d}-640.webp", f"/assets/portfolio/p{i:02d}.webp", c, t) for i, (c, t) in P.items()]
items = [(f"/assets/portfolio/{k}-640.webp", f"/assets/portfolio/{k}.webp", c, t) for k, c, t in P2] + items
items += [(f"/assets/work/{n}-720.webp", f"/assets/work/{n}.webp", c, t) for n, c, t in WORK]
order = {k: i for i, (k, _) in enumerate(CATS)}
items.sort(key=lambda x: order[x[2]])  # stable: newest photos lead each room
counts = {k: sum(1 for x in items if x[2] == k) + sum(1 for j in JOBS if j["cat"] == k) for k, _ in CATS}
total = len(items) + len(JOBS)
btns = f'<button type="button" class="pf-filter" aria-pressed="true" data-cat="all">All <span>{total}</span></button><button type="button" class="pf-filter" aria-pressed="false" data-cat="recent">Recent work <span>{len(JOBS)}</span></button>' + "".join(
    f'<button type="button" class="pf-filter" aria-pressed="false" data-cat="{k}">{n} <span>{counts[k]}</span></button>' for k, n in CATS)
jobs_li = "\n".join(
    f'''        <li class="pf-item" data-cat="{j["cat"]}" data-real="1"><a class="pf-link" href="{j["full"]}" data-full="{j["full"]}"><img src="{j["small"]}" alt="{html.escape(j["alt"])}" width="{j["w"]}" height="{j["h"]}" loading="lazy" decoding="async"><span class="pf-badge" aria-hidden="true">{j["badge"]}</span><span class="pf-cap">{html.escape(j["cap"])}</span></a></li>''' for j in JOBS)
grid = jobs_li + "\n" + "\n".join(
    f'''        <li class="pf-item" data-cat="{c}"><a class="pf-link" href="{full}" data-full="{full}"><img src="{small}" alt="{html.escape(t)}" width="640" height="427" loading="lazy" decoding="async"><span class="pf-cap">{html.escape(t)}</span></a></li>'''
    for small, full, c, t in items)
ld = {"@context": "https://schema.org", "@graph": [
    {"@type": "CollectionPage", "name": "DV Tile portfolio", "url": "https://dvtile.ca/portfolio", "about": {"@id": "https://dvtile.ca/#business"}},
    crumbs("Portfolio", "portfolio")]}
body = f'''  <main id="main" class="pg-main pg-main--wide">
    <nav class="pg-crumbs" aria-label="Breadcrumb"><a href="/">DV Tile</a><span aria-hidden="true">/</span><span aria-current="page">Portfolio</span></nav>
    <header class="pg-hero">
      <h1>Portfolio</h1>
      <p class="pg-lede">Bathrooms and showers, kitchens and backsplashes, floors and entries, fireplaces and outdoor stone. Photos marked Recent work are DV Tile jobs, including prep and waterproofing. The rest mix earlier installations with design concepts of finishes we offer. Generated studies, design references, and promotional ads are on the <a href="/inspiration">inspiration page</a>, not in this portfolio.</p>
    </header>
    <div class="pf-filters" role="group" aria-label="Filter by room">{btns}</div>
    <p class="pf-count" aria-live="polite">Showing {total} photos</p>
    <ul class="pf-grid">
{grid}
    </ul>
{cta()}
  </main>
  <dialog class="pf-dialog" aria-label="Enlarged photo">
    <form method="dialog"><button class="pf-close" aria-label="Close">Close</button></form>
    <img alt="">
    <p class="pf-dialog__cap"></p>
  </dialog>
  <script src="/portfolio.js?v={JS_V}" defer></script>
'''
portfolio_page = head("Tile and Stone Installation Portfolio | DV Tile Toronto",
    "Bathrooms, showers, kitchen backsplashes, marble floors, fireplaces, terraces and pools: tile and stone finishes installed by DV Tile across Toronto and the GTA.",
    "portfolio", ld) + body + foot().replace("Images on this page are concept renderings of finishes we install.", "Photos marked Recent work are DV Tile jobs. The rest of this portfolio mixes earlier installations and design concepts.")
portfolio_page = portfolio_page.replace('<a href="/portfolio">Portfolio</a>', '<a href="/portfolio" aria-current="page">Portfolio</a>', 1)
open(f'{OUT}/portfolio.html', 'w').write(portfolio_page)
print("portfolio items:", len(items), counts)
