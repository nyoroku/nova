from copy import deepcopy
from pathlib import Path

from docx import Document
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


SOURCE = Path(r"C:\Users\Administrator\Downloads\rafiki-kkday-design-brief.docx")
OUTPUT = Path(r"C:\rafiki\outputs\rafiki-kkday-design-brief-seo-aeo-geo-audit.docx")

ORANGE = "F97316"
TEAL = "14B8A6"
INK = "1F2937"
MUTED = "6B7280"
BORDER = "E5E7EB"
WARM = "FFF7ED"
WHITE = "FFFFFF"
LIGHT_TEAL = "ECFDF9"
LIGHT_ORANGE = "FFF3EA"

USABLE_DXA = 9960


def set_cell_shading(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = tc_pr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tc_pr.append(shd)
    shd.set(qn("w:fill"), fill)


def set_cell_margins(cell, top=100, start=120, bottom=100, end=120):
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_mar = tc_pr.find(qn("w:tcMar"))
    if tc_mar is None:
        tc_mar = OxmlElement("w:tcMar")
        tc_pr.append(tc_mar)
    for name, value in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        node = tc_mar.find(qn(f"w:{name}"))
        if node is None:
            node = OxmlElement(f"w:{name}")
            tc_mar.append(node)
        node.set(qn("w:w"), str(value))
        node.set(qn("w:type"), "dxa")


def set_cell_width(cell, width):
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_w = tc_pr.find(qn("w:tcW"))
    if tc_w is None:
        tc_w = OxmlElement("w:tcW")
        tc_pr.append(tc_w)
    tc_w.set(qn("w:w"), str(width))
    tc_w.set(qn("w:type"), "dxa")


def set_table_borders(table, color=BORDER, size=6):
    tbl_pr = table._tbl.tblPr
    borders = tbl_pr.find(qn("w:tblBorders"))
    if borders is None:
        borders = OxmlElement("w:tblBorders")
        tbl_pr.append(borders)
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        node = borders.find(qn(f"w:{edge}"))
        if node is None:
            node = OxmlElement(f"w:{edge}")
            borders.append(node)
        node.set(qn("w:val"), "single")
        node.set(qn("w:sz"), str(size))
        node.set(qn("w:space"), "0")
        node.set(qn("w:color"), color)


def set_table_geometry(table, widths):
    table.autofit = False
    tbl_pr = table._tbl.tblPr
    tbl_w = tbl_pr.find(qn("w:tblW"))
    if tbl_w is None:
        tbl_w = OxmlElement("w:tblW")
        tbl_pr.append(tbl_w)
    tbl_w.set(qn("w:w"), str(sum(widths)))
    tbl_w.set(qn("w:type"), "dxa")

    tbl_ind = tbl_pr.find(qn("w:tblInd"))
    if tbl_ind is None:
        tbl_ind = OxmlElement("w:tblInd")
        tbl_pr.append(tbl_ind)
    tbl_ind.set(qn("w:w"), "120")
    tbl_ind.set(qn("w:type"), "dxa")

    grid = table._tbl.tblGrid
    for child in list(grid):
        grid.remove(child)
    for width in widths:
        col = OxmlElement("w:gridCol")
        col.set(qn("w:w"), str(width))
        grid.append(col)

    for row in table.rows:
        for idx, cell in enumerate(row.cells):
            set_cell_width(cell, widths[idx])
            set_cell_margins(cell)
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER


def set_repeat_table_header(row):
    tr_pr = row._tr.get_or_add_trPr()
    header = tr_pr.find(qn("w:tblHeader"))
    if header is None:
        header = OxmlElement("w:tblHeader")
        tr_pr.append(header)
    header.set(qn("w:val"), "true")


def set_cant_split(row):
    tr_pr = row._tr.get_or_add_trPr()
    cant_split = tr_pr.find(qn("w:cantSplit"))
    if cant_split is None:
        cant_split = OxmlElement("w:cantSplit")
        tr_pr.append(cant_split)


def set_run_font(run, size=None, bold=None, color=None):
    if size is not None:
        run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold
    if color is not None:
        run.font.color.rgb = RGBColor.from_string(color)


def set_para_spacing(paragraph, before=0, after=6, line=1.15):
    fmt = paragraph.paragraph_format
    fmt.space_before = Pt(before)
    fmt.space_after = Pt(after)
    fmt.line_spacing = line
    fmt.widow_control = True


def set_style_id(paragraph, style_id):
    p_pr = paragraph._p.get_or_add_pPr()
    p_style = p_pr.find(qn("w:pStyle"))
    if p_style is None:
        p_style = OxmlElement("w:pStyle")
        p_pr.insert(0, p_style)
    p_style.set(qn("w:val"), style_id)


def add_heading(doc, text, level=1, page_break=False):
    paragraph = doc.add_paragraph()
    if page_break:
        paragraph.paragraph_format.page_break_before = True
    style_id = {1: "Heading1", 2: "Heading2", 3: "Heading3"}[level]
    set_style_id(paragraph, style_id)
    paragraph.add_run(text)
    paragraph.paragraph_format.keep_with_next = True
    if level == 1:
        set_para_spacing(paragraph, before=16, after=8)
    elif level == 2:
        set_para_spacing(paragraph, before=12, after=6)
    else:
        set_para_spacing(paragraph, before=9, after=5)
    return paragraph


def add_body(doc, text="", bold_label=None, italic=False, after=6):
    paragraph = doc.add_paragraph()
    set_para_spacing(paragraph, after=after)
    if bold_label and text.startswith(bold_label):
        label_run = paragraph.add_run(bold_label)
        label_run.bold = True
        rest = text[len(bold_label):]
        paragraph.add_run(rest)
    else:
        run = paragraph.add_run(text)
        run.italic = italic
    return paragraph


def add_bullet(doc, text, bold_label=None, level=0):
    paragraph = doc.add_paragraph()
    set_style_id(paragraph, "ListParagraph")
    p_pr = paragraph._p.get_or_add_pPr()
    num_pr = p_pr.find(qn("w:numPr"))
    if num_pr is None:
        num_pr = OxmlElement("w:numPr")
        p_pr.append(num_pr)
    ilvl = OxmlElement("w:ilvl")
    ilvl.set(qn("w:val"), str(level))
    num_id = OxmlElement("w:numId")
    num_id.set(qn("w:val"), "2")
    num_pr.append(ilvl)
    num_pr.append(num_id)
    set_para_spacing(paragraph, after=3)
    if bold_label and text.startswith(bold_label):
        run = paragraph.add_run(bold_label)
        run.bold = True
        paragraph.add_run(text[len(bold_label):])
    else:
        paragraph.add_run(text)
    return paragraph


def add_hyperlink(paragraph, text, url, color=TEAL):
    relationship_id = paragraph.part.relate_to(
        url,
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
        is_external=True,
    )
    hyperlink = OxmlElement("w:hyperlink")
    hyperlink.set(qn("r:id"), relationship_id)
    run = OxmlElement("w:r")
    r_pr = OxmlElement("w:rPr")
    color_node = OxmlElement("w:color")
    color_node.set(qn("w:val"), color)
    underline = OxmlElement("w:u")
    underline.set(qn("w:val"), "single")
    r_pr.append(color_node)
    r_pr.append(underline)
    run.append(r_pr)
    text_node = OxmlElement("w:t")
    text_node.text = text
    run.append(text_node)
    hyperlink.append(run)
    paragraph._p.append(hyperlink)
    return hyperlink


def add_resource(doc, name, url, purpose):
    paragraph = doc.add_paragraph()
    set_style_id(paragraph, "ListParagraph")
    p_pr = paragraph._p.get_or_add_pPr()
    num_pr = OxmlElement("w:numPr")
    ilvl = OxmlElement("w:ilvl")
    ilvl.set(qn("w:val"), "0")
    num_id = OxmlElement("w:numId")
    num_id.set(qn("w:val"), "2")
    num_pr.append(ilvl)
    num_pr.append(num_id)
    p_pr.append(num_pr)
    set_para_spacing(paragraph, after=4)
    add_hyperlink(paragraph, name, url)
    paragraph.add_run(f" — {purpose}")
    return paragraph


def add_callout(doc, label, text, fill=LIGHT_ORANGE, border_color=ORANGE):
    paragraph = doc.add_paragraph()
    set_para_spacing(paragraph, before=4, after=8)
    p_pr = paragraph._p.get_or_add_pPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), fill)
    p_pr.append(shd)
    borders = OxmlElement("w:pBdr")
    left = OxmlElement("w:left")
    left.set(qn("w:val"), "single")
    left.set(qn("w:sz"), "22")
    left.set(qn("w:space"), "8")
    left.set(qn("w:color"), border_color)
    borders.append(left)
    p_pr.append(borders)
    run = paragraph.add_run(label)
    run.bold = True
    run.font.color.rgb = RGBColor.from_string(INK)
    paragraph.add_run(text)
    return paragraph


def add_table(doc, headers, rows, widths, priority_colors=False):
    table = doc.add_table(rows=1, cols=len(headers))
    set_table_geometry(table, widths)
    set_table_borders(table)
    header = table.rows[0]
    set_repeat_table_header(header)
    set_cant_split(header)
    for index, text in enumerate(headers):
        cell = header.cells[index]
        set_cell_shading(cell, ORANGE)
        p = cell.paragraphs[0]
        set_para_spacing(p, after=0, line=1.05)
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        run = p.add_run(text)
        set_run_font(run, size=9, bold=True, color=WHITE)

    for row_index, values in enumerate(rows):
        row = table.add_row()
        set_cant_split(row)
        for col_index, value in enumerate(values):
            cell = row.cells[col_index]
            if row_index % 2:
                set_cell_shading(cell, WARM)
            if priority_colors and col_index == 0:
                if str(value).startswith("P0"):
                    set_cell_shading(cell, "FEE2E2")
                elif str(value).startswith("P1"):
                    set_cell_shading(cell, "FEF3C7")
                else:
                    set_cell_shading(cell, LIGHT_TEAL)
            p = cell.paragraphs[0]
            set_para_spacing(p, after=0, line=1.05)
            run = p.add_run(str(value))
            set_run_font(run, size=8.7, color=INK)
            if col_index == 0:
                run.bold = True
    spacer = doc.add_paragraph()
    set_para_spacing(spacer, after=2)
    return table


def insert_after(paragraph, new_paragraph):
    paragraph._p.addnext(new_paragraph._p)


doc = Document(SOURCE)

# Resolve the original "design-only" scope conflict at the point where it appears.
scope_callout = doc.add_paragraph()
set_para_spacing(scope_callout, before=4, after=8)
p_pr = scope_callout._p.get_or_add_pPr()
shd = OxmlElement("w:shd")
shd.set(qn("w:fill"), LIGHT_TEAL)
p_pr.append(shd)
borders = OxmlElement("w:pBdr")
left = OxmlElement("w:left")
left.set(qn("w:val"), "single")
left.set(qn("w:sz"), "22")
left.set(qn("w:space"), "8")
left.set(qn("w:color"), TEAL)
borders.append(left)
p_pr.append(borders)
run = scope_callout.add_run("Approved scope addendum (29 July 2026): ")
run.bold = True
scope_callout.add_run(
    "Sections 11–18 authorize targeted content, metadata, URL, internal-link, schema, "
    "sitemap, robots, analytics, and internationalization changes. This exception "
    "supersedes the design-only/zero-content-change rule only where those sections "
    "require it. Prices, safety claims, certifications, reviews, and booking links "
    "must still be verified before alteration or publication."
)
insert_after(doc.paragraphs[6], scope_callout)

# Add the same exception to the opening scope table.
scope_table = doc.tables[0]
new_row = scope_table.add_row()
new_row.cells[0].text = "Approved growth exception"
new_row.cells[1].text = (
    "Technical SEO/AEO/GEO, indexation cleanup, schema, sitemap/robots, internal "
    "linking, analytics, and five-language internationalization per Sections 11–18."
)
for idx, cell in enumerate(new_row.cells):
    set_cell_margins(cell)
    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    set_cell_shading(cell, LIGHT_TEAL)
    for paragraph in cell.paragraphs:
        set_para_spacing(paragraph, after=0, line=1.05)
        for run in paragraph.runs:
            set_run_font(run, size=9, color=INK, bold=(idx == 0))

# Start the growth addendum on a fresh page.
add_heading(doc, "11. Approved Growth & Discoverability Workstream", level=1, page_break=True)
add_body(
    doc,
    "The following requirements extend the visual redesign into a controlled SEO, "
    "answer-engine optimization (AEO), generative-engine optimization (GEO), "
    "internationalization, and technical-quality program. They are functional delivery "
    "requirements, not optional polish.",
)
add_callout(
    doc,
    "Operating principle: ",
    "Fix crawl quality before adding more pages or translations. The site should win "
    "through first-hand local expertise, trustworthy booking information, fast pages, "
    "and a clean entity/URL architecture—not through thousands of near-duplicate query variants.",
)
add_heading(doc, "11.1 Guardrails", level=2)
for text, label in [
    (
        "Freeze page generators: Do not publish additional town, audience, “edition,” "
        "“volume,” “ref,” or translated variants until the indexation cleanup is approved.",
        "Freeze page generators:",
    ),
    (
        "Protect value before removal: Export Google Search Console, GA4, backlinks, "
        "bookings, and server-log data before any redirect, noindex, or deletion decision.",
        "Protect value before removal:",
    ),
    (
        "Use evidence, not claims: Prices, operating hours, safety statistics, wildlife "
        "facts, certifications, ratings, and review counts must be current, visible, and supportable.",
        "Use evidence, not claims:",
    ),
    (
        "Make one canonical source of truth: Tour facts, prices, policies, organization "
        "details, translations, and schema must derive from shared structured data.",
        "Make one canonical source of truth:",
    ),
    (
        "Deploy on staging first: Crawl, validate, compare, and obtain owner sign-off "
        "before production release.",
        "Deploy on staging first:",
    ),
]:
    add_bullet(doc, text, bold_label=label)

add_heading(doc, "11.2 Audit Method & Limits", level=2)
add_body(
    doc,
    "Snapshot date: 29 July 2026. The review checked the public homepage, robots.txt, "
    "sitemap.xml, search-index samples, and a 12-URL HTML sample covering the homepage, "
    "FAQ, tours, destinations, editorial guides, generated posts, and long-URL posts. "
    "This is a public technical audit; Search Console coverage, GA4 conversions, server "
    "logs, backlink quality, Core Web Vitals field data, and a complete authenticated crawl "
    "must be added during implementation.",
)

add_heading(doc, "12. Live SEO/AEO/GEO Audit — Priority Findings", level=1)
audit_rows = [
    (
        "P0",
        "Index footprint",
        "sitemap.xml contains 3,249 entries but only 2,740 unique URLs; /faq/ is repeated 510 times (509 exact duplicates).",
        "Deduplicate the generator and sitemap. Submit only canonical, indexable 200 URLs.",
    ),
    (
        "P0",
        "Scaled content",
        "The sitemap exposes 1,720 blog URLs, including 1,000 “ref/edition/volume” URLs, plus roughly 605 location-variant URLs.",
        "Inventory as Keep / Improve / Merge / Remove. Consolidate low-value variants into expert hubs and proven landing pages.",
    ),
    (
        "P0",
        "Robots & sitemap",
        "robots.txt returns 404. One 681 KB sitemap carries polluted URLs; 3,232 entries share the same 2026-07-10 lastmod.",
        "Serve a 200 robots.txt, publish a sitemap index by page type/locale, and emit truthful per-URL lastmod values.",
    ),
    (
        "P1",
        "Title template",
        "Sample titles are 94–241 characters and append “Rafiki Boat Rides Naivasha” twice; homepage is 127 characters.",
        "Fix the shared title helper: one descriptive page title plus one concise brand suffix.",
    ),
    (
        "P1",
        "Link & HTML bloat",
        "Sampled pages expose about 1,012–1,031 unique internal links; HTML is about 266–384 KB uncompressed.",
        "Remove sitewide mega-lists, link through hubs and contextual modules, and shrink rendered HTML/DOM.",
    ),
    (
        "P1",
        "Heading semantics",
        "Homepage exposes five H1 elements, apparently including carousel feature slides.",
        "Keep one persistent page H1; use H2/H3 or styled text for slides and feature labels.",
    ),
    (
        "P1",
        "Schema graph",
        "LocalBusiness/TouristAttraction/TouristTrip/FAQ/BlogPosting markup exists, but the homepage duplicates TouristAttraction and sampled blocks lack stable @id links.",
        "Replace disconnected blocks with one validated entity graph; add WebSite, WebPage, and BreadcrumbList where applicable.",
    ),
    (
        "P1",
        "Internationalization",
        "Sampled pages declare html lang=en but expose no hreflang alternates.",
        "Launch five crawlable locales with reciprocal hreflang, self-canonicals, translated metadata/schema, and an accessible language switcher.",
    ),
    (
        "P1",
        "Content trust",
        "Generated samples combine audience, town, and activity modifiers and contain time-sensitive prices, safety, wildlife, and certification claims.",
        "Require named expert review, source/date fields, first-hand media, and a fact-check before indexing.",
    ),
    (
        "P2",
        "Performance",
        "Large server-rendered pages and 1,000+ links create a clear crawl, parse, and interaction risk; field CWV data was not available publicly.",
        "Measure templates in PSI/Lighthouse and Search Console; meet LCP ≤2.5 s, INP <200 ms, CLS <0.1 at the 75th percentile.",
    ),
    (
        "P2",
        "Measurement",
        "Public HTML cannot confirm reliable booking/WhatsApp attribution or indexation reporting.",
        "Instrument consent-aware GA4 events and connect Search Console, Bing Webmaster Tools, GBP, and a weekly health dashboard.",
    ),
]
add_table(
    doc,
    ["Priority", "Area", "Observed evidence", "Required action"],
    audit_rows,
    [720, 1500, 3700, 4040],
    priority_colors=True,
)
add_heading(doc, "12.1 What Is Already Working", level=2)
for text in [
    "Sampled URLs returned 200, used HTTPS, declared English, contained self-referencing canonicals, and included meta descriptions.",
    "The site already has reusable templates and JSON-LD foundations, so fixes can be applied centrally.",
    "Core tours, FAQ, destinations, first-hand local expertise, direct booking, and Lake Naivasha subject depth provide a strong base once index bloat is removed.",
]:
    add_bullet(doc, text)

add_heading(doc, "13. Indexation, Content & Internal-Link Architecture", level=1)
add_heading(doc, "13.1 Safe Index Cleanup Workflow", level=2)
cleanup_steps = [
    (
        "1. Baseline",
        "Export 16 months of Search Console queries/pages, GA4 landing-page conversions, "
        "backlinks, booking/WhatsApp leads, index coverage, and server-log crawl activity.",
    ),
    (
        "2. Classify",
        "Assign every URL to Keep, Improve, Merge, Redirect, Noindex, or Remove. Add owner, "
        "target URL, traffic, links, conversions, content uniqueness, and decision reason.",
    ),
    (
        "3. Consolidate",
        "Merge overlapping pages into a smaller set of expert guides/tour/location pages. "
        "Use a single-hop 301 where a close replacement exists; use 410 only when no useful replacement exists.",
    ),
    (
        "4. Clean signals",
        "Remove retired URLs from sitemaps and global navigation. Update internal links, "
        "canonicals, hreflang, schema, and breadcrumbs to point directly to final URLs.",
    ),
    (
        "5. Monitor",
        "Track excluded/indexed counts, crawl requests, impressions, clicks, conversions, "
        "redirect errors, soft 404s, and ranking clusters weekly for at least 12 weeks.",
    ),
]
add_table(
    doc,
    ["Step", "Implementation requirement"],
    cleanup_steps,
    [1500, 8460],
)
add_callout(
    doc,
    "Do not blanket-delete: ",
    "A generated URL with clicks, strong backlinks, bookings, or genuinely distinct local "
    "value may be worth improving. Decisions must be data-led and mapped before deployment.",
    fill=LIGHT_TEAL,
    border_color=TEAL,
)

add_heading(doc, "13.2 Target Information Architecture", level=2)
add_body(
    doc,
    "Use a small, navigable hub-and-spoke model. Recommended durable hubs: /tours/, "
    "/destinations/, /guides/, /safety/, /about/, /faq/, /contact/, plus policy pages "
    "for cancellation, privacy, and terms. Keep the existing English root to avoid an "
    "unnecessary migration; add locale folders only for translated pages.",
)
for text, label in [
    (
        "Breadcrumbs: Home → hub → page, implemented as visible links and BreadcrumbList schema.",
        "Breadcrumbs:",
    ),
    (
        "Contextual links: Each indexable page links to its hub, booking CTA, and 2–5 genuinely related pages using descriptive anchor text.",
        "Contextual links:",
    ),
    (
        "Global navigation: Keep only business-critical hubs and policies; do not print hundreds of town/blog URLs in every page footer.",
        "Global navigation:",
    ),
    (
        "Location pages: Retain only locations with real travel demand and unique logistics, pickup, route, timing, price, imagery, or testimonials.",
        "Location pages:",
    ),
    (
        "Topic ownership: Assign one primary URL per intent—price, safety, Crescent Island, hippos, sunset, birding, transport, and group/private tours—to prevent cannibalization.",
        "Topic ownership:",
    ),
]:
    add_bullet(doc, text, bold_label=label)

add_heading(doc, "13.3 AEO/GEO Content Standard", level=2)
add_body(
    doc,
    "For Google’s generative search features, foundational SEO remains the strategy. "
    "Do not create hundreds of query-fan-out pages, rewrite for machines, or rely on "
    "special “AI hacks.” Every priority page should instead contain:",
)
for text, label in [
    (
        "Answer-first summary: A clear 40–80 word answer immediately after the H1 where the query calls for one.",
        "Answer-first summary:",
    ),
    (
        "Scannable facts: Visible price/inclusions, duration, departure point, operating hours, accessibility, cancellation, safety, and what-to-bring information.",
        "Scannable facts:",
    ),
    (
        "Question-led sections: Natural H2/H3 questions with concise answers, followed by useful detail—not keyword variants.",
        "Question-led sections:",
    ),
    (
        "First-hand proof: Named captains/guides, experience, original route photos/video, boat details, seasonal observations, and real guest evidence.",
        "First-hand proof:",
    ),
    (
        "Provenance: Named author/reviewer, published/updated dates, source links for wildlife/safety/fees, and a correction/update process.",
        "Provenance:",
    ),
    (
        "Consistent entities: The same business name, telephone, address, coordinates, policies, offers, and URLs in visible content, GBP, citations, and schema.",
        "Consistent entities:",
    ),
    (
        "Measurement: Track Google generative-search visibility in Search Console where available, AI-assistant referral traffic in analytics, and assisted bookings.",
        "Measurement:",
    ),
]:
    add_bullet(doc, text, bold_label=label)
add_callout(
    doc,
    "llms.txt: ",
    "Do not treat llms.txt as a Google ranking requirement. Google states that it does "
    "not use special AI text files for Search visibility. Maintain one only if a specific "
    "non-Google service requires it and ownership is clear.",
)

add_heading(doc, "14. Structured Data Architecture", level=1, page_break=True)
schema_rows = [
    (
        "Homepage",
        "WebSite + Organization/TravelAgency (LocalBusiness subtype) + WebPage",
        "One stable business @id, concise site name/alternateName, NAP, geo, hours, sameAs, logo, contactPoint. Use TouristAttraction only if it describes a distinct visitor attraction.",
    ),
    (
        "Tour detail",
        "TouristTrip + Offer + WebPage + BreadcrumbList",
        "Match visible name, description, itinerary, duration, image, price/currency, availability, cancellation, provider, and URL. Do not force Product markup for a service unless valid.",
    ),
    (
        "Tours/destinations hub",
        "CollectionPage + ItemList + BreadcrumbList",
        "List only visible cards in page order with stable URLs; paginate or load crawlable hub pages rather than a sitewide mega-list.",
    ),
    (
        "Blog/guide",
        "BlogPosting + WebPage + BreadcrumbList",
        "Include author/reviewer, datePublished, truthful dateModified, image, publisher @id, headline, and mainEntityOfPage.",
    ),
    (
        "FAQ",
        "FAQPage + Question + Answer",
        "Use only for visible, site-authored questions and answers. It may aid machine understanding but does not guarantee a Google rich result.",
    ),
    (
        "Business location/contact",
        "TravelAgency/LocalBusiness + PostalAddress + GeoCoordinates",
        "Match Google Business Profile exactly. Link the same business @id; do not create a new entity on each page.",
    ),
    (
        "Accommodation/editorial lists",
        "ItemList + ListItem + WebPage",
        "Describe third-party properties accurately; do not mark them as Rafiki-owned LocalBusiness entities unless ownership is real.",
    ),
    (
        "Images/video",
        "ImageObject / VideoObject where applicable",
        "Use crawlable media URLs, captions, thumbnails, upload dates, and content that is visible on the page.",
    ),
]
add_table(
    doc,
    ["Page type", "Recommended JSON-LD", "Implementation notes"],
    schema_rows,
    [1700, 3100, 5160],
)
add_heading(doc, "14.1 Schema Quality Gates", level=2)
for text in [
    "Render JSON-LD in the initial HTML where practical and keep it synchronized with visible localized content.",
    "Use stable @id values such as /#business, /#website, and each page URL plus #webpage; connect entities instead of duplicating them.",
    "Keep one main business entity. Remove the duplicate standalone TouristAttraction observed on the homepage unless it represents a genuinely separate entity.",
    "Never invent aggregateRating, Review, certification, availability, or price data. Mark up only facts users can see and verify.",
    "Validate every template and every locale with Google Rich Results Test and Schema.org Validator; then monitor Search Console enhancement reports.",
]:
    add_bullet(doc, text)

add_heading(doc, "15. Robots, Sitemaps, Canonicals, Performance & Competitive Quality", level=1)
add_heading(doc, "15.1 robots.txt & Sitemap Requirements", level=2)
add_body(doc, "Minimum robots.txt (return HTTP 200 as text/plain):")
code = doc.add_paragraph()
set_para_spacing(code, after=8)
code.paragraph_format.left_indent = Inches(0.25)
code.paragraph_format.right_indent = Inches(0.25)
code_pr = code._p.get_or_add_pPr()
code_shd = OxmlElement("w:shd")
code_shd.set(qn("w:fill"), "F3F4F6")
code_pr.append(code_shd)
code_run = code.add_run(
    "User-agent: *\n"
    "Allow: /\n"
    "Sitemap: https://www.rafikiboatridesnaivasha.com/sitemap_index.xml"
)
code_run.font.name = "Consolas"
code_run.font.size = Pt(9)
for text in [
    "Use sitemap_index.xml to reference small sitemaps by page type and locale: core, tours, guides/blog, destinations, and each launched language.",
    "Include only unique, canonical, indexable URLs that return 200. Exclude redirects, 404/410, noindex, parameter variants, search/filter pages, and duplicates.",
    "Generate truthful lastmod values from meaningful content changes. Google ignores priority and changefreq, so remove them unless another consumer requires them.",
    "Submit the sitemap index to Google Search Console and Bing Webmaster Tools; compare submitted versus indexed by sitemap group.",
]:
    add_bullet(doc, text)

add_heading(doc, "15.2 Canonical & Status-Code Rules", level=2)
for text, label in [
    (
        "Canonical: Every indexable page uses one absolute self-canonical; translated pages self-canonicalize and connect via hreflang.",
        "Canonical:",
    ),
    (
        "301: Use for permanent merges and slug changes, directly to the final destination—no chains or loops.",
        "301:",
    ),
    (
        "404/410: Return real 404 for missing pages and 410 for intentionally retired pages without a close replacement; provide useful navigation.",
        "404/410:",
    ),
    (
        "Noindex: Use for temporary, utility, or low-value pages that must remain accessible. Do not block them in robots.txt until crawlers can see the noindex.",
        "Noindex:",
    ),
    (
        "Normalization: Force HTTPS and one preferred host/trailing-slash convention; update internal links to final URLs.",
        "Normalization:",
    ),
]:
    add_bullet(doc, text, bold_label=label)

add_heading(doc, "15.3 Performance & Accessibility Budget", level=2)
for text in [
    "Core Web Vitals field targets at the 75th percentile: LCP ≤2.5 seconds, INP <200 milliseconds, CLS <0.1.",
    "Reduce initial HTML and DOM by removing 1,000-link sitewide lists, repeated hidden content, duplicate JSON-LD, and unused component markup.",
    "Serve responsive AVIF/WebP imagery with width/height, srcset/sizes, lazy-load below the fold, and preload only the true LCP hero.",
    "Delay non-essential third-party scripts; reserve space for carousels, maps, embeds, cookie banners, and sticky CTAs.",
    "Use one semantic H1, logical heading order, keyboard-operable carousels/accordions, visible focus, descriptive link text, and translated alt text that reflects the actual image.",
]:
    add_bullet(doc, text)

add_heading(doc, "15.4 Competitive Advantage Requirements", level=2)
add_body(
    doc,
    "Search competitors and OTAs already emphasize ratings, prices, cancellation, "
    "availability, safety, and proof. Rafiki should differentiate with verifiable local "
    "expertise and a lower-friction direct-booking experience:",
)
for text in [
    "Publish clear per-boat/per-person pricing, inclusions/exclusions, sanctuary fees, duration, capacity, pickup/meeting point, payment methods, and cancellation terms.",
    "Show real-time or request-based availability, a short booking path, WhatsApp fallback, and confirmation expectations.",
    "Build genuine review acquisition and response workflows across Google Business Profile and relevant travel platforms; display only real, permissioned reviews.",
    "Create first-hand route maps, captain/guide profiles, boat/safety information, seasonal wildlife notes, original galleries, and short videos.",
    "Maintain an authoritative About, Contact, Safety, Privacy, Terms, and Cancellation set with consistent business details and evidence for certifications.",
    "Compare top organic/Maps/OTA competitors quarterly on query coverage, review strength, page experience, price clarity, booking friction, media, links, and multilingual reach.",
]:
    add_bullet(doc, text)

add_heading(doc, "16. Internationalization — Five Global Languages", level=1)
add_body(
    doc,
    "Launch five total languages for broad global reach: English, Simplified Chinese, "
    "Hindi, Spanish, and Arabic. Treat this as a reach-based starting set, then reprioritize "
    "using Search Console demand and booking data. Swahili is the recommended locally "
    "strategic next language; French or German may outperform a global-speaker ranking for inbound tourism.",
)
language_rows = [
    (
        "English",
        "en",
        "LTR",
        "Existing root URLs",
        "Source and x-default experience; preserve current URLs to avoid migration risk.",
    ),
    (
        "Simplified Chinese",
        "zh-Hans",
        "LTR",
        "/zh-cn/",
        "Native review; localize names/transliterations carefully and keep Kenyan place names consistent.",
    ),
    (
        "Hindi",
        "hi",
        "LTR",
        "/hi/",
        "Native review; localize numbers, dates, safety, payment, and booking instructions.",
    ),
    (
        "Spanish",
        "es",
        "LTR",
        "/es/",
        "Neutral international Spanish with tourism terminology and human-edited metadata.",
    ),
    (
        "Arabic",
        "ar",
        "RTL",
        "/ar/",
        "Set dir=rtl, mirror directional UI/icons where appropriate, and test mixed phone/price/date strings.",
    ),
]
add_table(
    doc,
    ["Language", "hreflang", "Direction", "URL pattern", "Launch notes"],
    language_rows,
    [1350, 1200, 900, 1500, 5010],
)
add_heading(doc, "16.1 Technical i18n Requirements", level=2)
for text, label in [
    (
        "Separate URLs: Use crawlable subdirectories. Do not swap language only with cookies, JavaScript state, or browser settings.",
        "Separate URLs:",
    ),
    (
        "Reciprocal hreflang: Every equivalent page lists itself and all available language alternates, plus x-default to the English/default selector. Links must be reciprocal.",
        "Reciprocal hreflang:",
    ),
    (
        "Self-canonical: Each locale canonicalizes to itself—not to English—unless it is intentionally not indexable.",
        "Self-canonical:",
    ),
    (
        "Language markup: Set the correct html lang and Arabic dir=rtl. Keep an accessible, crawlable language switcher on every translated page.",
        "Language markup:",
    ),
    (
        "No forced redirects: Suggest a language, but do not automatically redirect by IP or Accept-Language; users and crawlers must choose and revisit any locale.",
        "No forced redirects:",
    ),
    (
        "Translate the whole search surface: Visible copy, title, meta description, Open Graph, navigation, alt text, schema strings, forms, validation, policies, and confirmation messages.",
        "Translate the whole search surface:",
    ),
    (
        "Locale formatting: Localize dates, times, numbers, units, and currency display while keeping the authoritative charged currency and fees explicit.",
        "Locale formatting:",
    ),
]:
    add_bullet(doc, text, bold_label=label)

add_heading(doc, "16.2 Translation & Launch Workflow", level=2)
for text in [
    "Phase 1 translates only the highest-value set: homepage, tours hub, active tour pages, FAQ, safety, contact/meeting point, booking flow, cancellation, privacy, and terms.",
    "Do not translate low-value generated pages. This would multiply the current index bloat by five and increase quality risk.",
    "Use a translation management system with stable content keys, translation memory, and a glossary for Rafiki, Lake Naivasha, Crescent Island, Karagita, wildlife, boat types, fees, and safety terms.",
    "Require native-language review for marketing, booking, safety, legal, and policy content; record reviewer and review date.",
    "QA every locale at 375 px and desktop for overflow, Arabic RTL, fonts, input direction, WhatsApp links, currency, schema, canonicals, sitemap membership, and reciprocal hreflang.",
    "Measure organic landing pages, language-switch usage, booking conversion, WhatsApp clicks, revenue, and support questions by locale before expanding.",
]:
    add_bullet(doc, text)

add_heading(doc, "17. SEO/AEO/GEO Tools & Guides", level=1)
add_body(
    doc,
    "Use official platforms as the source of truth. Paid crawlers and visibility tools "
    "support workflow and monitoring; they do not have access to search engines’ internal ranking systems.",
)
add_heading(doc, "17.1 Required Free Platforms", level=2)
for name, url, purpose in [
    (
        "Google Search Console",
        "https://search.google.com/search-console/about",
        "indexing, URL Inspection, queries, Core Web Vitals, enhancements, sitemaps, and generative-search reporting where available.",
    ),
    (
        "Google Analytics 4",
        "https://analytics.google.com/",
        "landing-page, locale, booking, WhatsApp, phone, form, and assisted-conversion measurement.",
    ),
    (
        "Google Business Profile",
        "https://www.google.com/business/",
        "local entity accuracy, reviews, photos, services, hours, location, and Maps visibility.",
    ),
    (
        "Bing Webmaster Tools",
        "https://www.bing.com/webmasters/",
        "Bing crawl/index reports, Site Explorer, backlinks, keyword data, sitemaps, and URL inspection.",
    ),
    (
        "IndexNow",
        "https://www.indexnow.org/",
        "notify participating search engines when approved URLs are added, updated, redirected, or deleted.",
    ),
    (
        "Google Rich Results Test",
        "https://search.google.com/test/rich-results",
        "validate Google-supported structured-data eligibility on every template and locale.",
    ),
    (
        "Schema.org Validator",
        "https://validator.schema.org/",
        "inspect the full Schema.org graph and syntax beyond Google rich-result types.",
    ),
    (
        "PageSpeed Insights",
        "https://pagespeed.web.dev/",
        "template-level lab diagnostics and available Chrome UX Report field data.",
    ),
    (
        "Chrome Lighthouse",
        "https://developer.chrome.com/docs/lighthouse/",
        "repeatable performance, accessibility, best-practice, and SEO checks in staging/CI.",
    ),
]:
    add_resource(doc, name, url, purpose)

add_heading(doc, "17.2 Crawl, Research & Monitoring Tools", level=2)
for name, url, purpose in [
    (
        "Screaming Frog SEO Spider",
        "https://www.screamingfrog.co.uk/seo-spider/",
        "full crawl exports for status, canonical, title, H1, links, hreflang, sitemap, and structured-data QA; the free limit is too small for the current site.",
    ),
    (
        "Sitebulb",
        "https://sitebulb.com/",
        "visual crawl prioritization, internal-link maps, hints, and recurring audit reports.",
    ),
    (
        "Ahrefs Site Audit",
        "https://ahrefs.com/site-audit",
        "optional technical crawl, backlinks, content overlap, and competitor-link research.",
    ),
    (
        "Semrush Site Audit",
        "https://www.semrush.com/siteaudit/",
        "optional technical monitoring, keyword/cannibalization research, and competitive tracking.",
    ),
    (
        "Google Trends",
        "https://trends.google.com/",
        "seasonality and market/language demand validation before creating or translating content.",
    ),
    (
        "AlsoAsked",
        "https://alsoasked.com/",
        "question-cluster research to inform useful FAQ and guide sections; validate against real customer/support data.",
    ),
    (
        "AnswerThePublic",
        "https://answerthepublic.com/",
        "supplementary question research; avoid turning every query variation into a separate page.",
    ),
]:
    add_resource(doc, name, url, purpose)
add_body(
    doc,
    "Optional AI-visibility platforms may be used for directional brand/citation monitoring "
    "across assistants, but validate all recommendations against official search guidance, "
    "analytics, and actual bookings. No third-party tool can guarantee inclusion or ranking.",
    italic=True,
)

add_heading(doc, "17.3 Official Implementation Guides", level=2)
for name, url, purpose in [
    (
        "Google: Generative AI search optimization",
        "https://developers.google.com/search/docs/fundamentals/ai-optimization-guide",
        "current official guidance on AEO/GEO, useful content, crawlability, duplicate reduction, measurement, and myths.",
    ),
    (
        "Google: Spam policies",
        "https://developers.google.com/search/docs/essentials/spam-policies",
        "scaled content, doorway pages, link spam, and other practices that can remove search eligibility.",
    ),
    (
        "Google: Build and submit a sitemap",
        "https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap",
        "canonical URL selection, limits, truthful lastmod, and sitemap submission.",
    ),
    (
        "Google: Multilingual and multi-regional sites",
        "https://developers.google.com/search/docs/specialty/international/managing-multi-regional-sites",
        "separate locale URLs, hreflang, discoverability, and language selection.",
    ),
    (
        "Google: Structured-data guidelines",
        "https://developers.google.com/search/docs/appearance/structured-data/sd-policies",
        "accuracy, visibility, completeness, relevance, and rich-result eligibility.",
    ),
    (
        "Google: Link best practices",
        "https://developers.google.com/search/docs/crawling-indexing/links-crawlable",
        "crawlable links, contextual internal linking, and useful anchor text.",
    ),
    (
        "Google: Title-link best practices",
        "https://developers.google.com/search/docs/appearance/title-link",
        "concise, unique titles; avoid repeated boilerplate and duplicated site names.",
    ),
    (
        "Google: Core Web Vitals",
        "https://developers.google.com/search/docs/appearance/core-web-vitals",
        "LCP, INP, CLS thresholds and measurement resources.",
    ),
    (
        "W3C Internationalization",
        "https://www.w3.org/International/",
        "language tags, bidirectional text, locale-aware design, and international content standards.",
    ),
]:
    add_resource(doc, name, url, purpose)

add_heading(doc, "17.4 Audit Cadence", level=2)
for text in [
    "Weekly: Search Console/Bing coverage, sitemap deltas, 4xx/5xx, security/manual actions, leads, and priority-query changes.",
    "Monthly: Full crawl, redirect/canonical/hreflang/schema validation, title/H1 duplication, orphan pages, Core Web Vitals, and language QA samples.",
    "Quarterly: Content prune/merge review, competitor benchmark, backlink/citation review, GBP/review health, and locale expansion decision.",
    "Per release: Staging crawl, HTML diff, redirect map test, Lighthouse, accessibility keyboard pass, Rich Results Test, Schema.org Validator, and analytics event verification.",
]:
    add_bullet(doc, text)

add_heading(doc, "18. Delivery Roadmap & Definition of Done Addendum", level=1, page_break=True)
roadmap_rows = [
    (
        "0",
        "Baseline & freeze",
        "Back up production; freeze generators; connect GSC/GA4/Bing/GBP; export URL-level evidence; crawl full site; define KPI baseline.",
        "Inventory and decision owners approved.",
    ),
    (
        "1",
        "Technical containment",
        "Fix robots 404, sitemap duplicates, title helper, homepage H1, global-link bloat, canonicals/status rules, and analytics events.",
        "No P0 crawl/index defects on staging.",
    ),
    (
        "2",
        "Consolidation & trust",
        "Keep/merge/remove decisions; 301/410 map; expert content upgrades; schema graph; hubs/breadcrumbs/contextual links; booking clarity.",
        "Approved canonical set and redirect QA pass.",
    ),
    (
        "3",
        "Five-language launch",
        "Translate priority set; native review; reciprocal hreflang; locale sitemap/schema; Arabic RTL; mobile/booking QA.",
        "All locale acceptance tests pass.",
    ),
    (
        "4",
        "Measure & expand",
        "Monitor indexation, CWV, rankings, AI/organic referrals, leads, revenue, reviews, and locale performance; expand only from evidence.",
        "Monthly dashboard and quarterly review active.",
    ),
]
add_table(
    doc,
    ["Phase", "Workstream", "Primary actions", "Exit gate"],
    roadmap_rows,
    [700, 1800, 5260, 2200],
)
add_heading(doc, "18.1 Additional Definition of Done", level=2)
for text in [
    "robots.txt returns 200, declares the sitemap index, and does not block pages that need crawling to process noindex or redirects.",
    "Submitted sitemaps contain zero exact duplicates and only canonical, indexable 200 URLs with truthful lastmod; page-type/locale groups are visible in GSC and Bing.",
    "Every indexable template has one clear H1, one concise unique title with one brand suffix, a useful meta description, a self-canonical, breadcrumbs where appropriate, and contextual internal links.",
    "No page prints a sitewide list of hundreds of destination/blog URLs; crawl depth and orphan-page reports are documented.",
    "Priority templates/locales pass Rich Results Test and Schema.org validation with no critical errors, disconnected duplicate business entities, or invented ratings/reviews.",
    "All five languages have crawlable URLs, correct lang/dir, reciprocal hreflang plus x-default, self-canonicals, accessible switching, translated metadata/schema, native review, and locale sitemaps.",
    "Core Web Vitals meet good thresholds at the 75th percentile for mobile page groups, or each failing group has an owner, measured cause, and dated remediation plan.",
    "Booking form, WhatsApp, phone, email, and confirmed-booking events are tested in analytics with source/medium and locale attribution.",
    "Removed/merged URLs follow the approved map with no redirect chains, loops, soft 404s, orphaned value, or stale internal links.",
    "No new generated or translated page is indexable without unique user value, expert/fact review, source dates, canonical ownership, internal links, schema QA, and inclusion in the correct sitemap.",
    "A quarterly competitor benchmark shows Rafiki’s position on price clarity, booking ease, authentic reviews, local proof, page experience, structured data, media, and multilingual coverage.",
]:
    add_bullet(doc, text)

add_callout(
    doc,
    "Final sign-off: ",
    "The design refresh and growth workstream ship together only after staging review by "
    "the owner and implementer, with the production backup, audit export, redirect map, "
    "QA evidence, and rollback plan retained.",
    fill=LIGHT_TEAL,
    border_color=TEAL,
)

# Keep headings and table rows readable, and retain the original document metadata.
for paragraph in doc.paragraphs:
    if paragraph.style and paragraph.style.name.startswith("Heading"):
        paragraph.paragraph_format.keep_with_next = True

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
doc.save(OUTPUT)
print(OUTPUT)
