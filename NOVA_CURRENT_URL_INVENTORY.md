# Nova Current URL Inventory
**Document:** NOVA_CURRENT_URL_INVENTORY.md  
**Product:** Nova Boat Rides Naivasha  
**Domain:** `https://www.novaboatridesnaivasha.co.ke`  
**Generated:** September 2026  
**Status:** Canonical Audit Baseline  

---

## 1. Core & Transactional Commercial Pages

| URL | View Function / Class | Template | Primary Model | HTTP Status | Canonical URL | Indexability | Purpose | Primary Target Keyword | Recommended Action |
|---|---|---|---|---|---|---|---|---|---|
| `/` | `core.views.HomeView` | `core/home.html` | `core.SiteSettings` | 200 | `https://www.novaboatridesnaivasha.co.ke/` | Index, Follow | Primary brand homepage & core conversion portal | `Nova Boat Rides Naivasha`, `Lake Naivasha boat tours` | **UPDATE** (Align H1 to "Boat Rides on Lake Naivasha", remove SEO jargon, update trust bar) |
| `/boat-rides/` | `tours.views.TourListView` | `tours/tour_list.html` | `tours.Tour` | 200 | `https://www.novaboatridesnaivasha.co.ke/boat-rides/` | Index, Follow | Primary commercial hub for all boat safari offerings | `boat rides naivasha`, `boat ride on Lake Naivasha` | **UPDATE** (Rebuild as Tier 1 transactional hub with 12 structured sections) |
| `/prices/` | `core.views.PricesView` | `core/prices.html` | `tours.ExperienceRate` | 200 | `https://www.novaboatridesnaivasha.co.ke/prices/` | Index, Follow | Official transparent pricing directory & rate breakdown | `Lake Naivasha boat ride price`, `boat rides naivasha prices` | **UPDATE** (Remove "Canonical Price Truth" jargon, pull from ExperienceRate service layer, update Crescent Island fee) |
| `/about/` | `core.views.AboutView` | `core/about.html` | `content.Captain` | 200 | `https://www.novaboatridesnaivasha.co.ke/about/` | Index, Follow | Brand trust, captain biographies, safety philosophy | `about Nova boat rides`, `Lake Naivasha captains` | **UPDATE** (Enforce verified captain certifications and local experience) |
| `/plan-naivasha/` | `core.views.PlanNaivashaView` | `core/plan_naivasha.html` | `core.SiteSettings` | 200 | `https://www.novaboatridesnaivasha.co.ke/plan-naivasha/` | Index, Follow | Comprehensive visitor hub: weather, packing, directions | `plan Lake Naivasha trip`, `Naivasha travel guide` | **UPDATE** (Streamline logistics, add internal links to boat rides) |
| `/contact/` | `core.views.ContactView` | `core/contact.html` | `core.SiteSettings` | 200 | `https://www.novaboatridesnaivasha.co.ke/contact/` | Index, Follow | Base location, GPS directions, direct WhatsApp/phone | `Nova Karagita Base contact`, `Karagita beach boat rides` | **UPDATE** (Synchronize NAP with SiteSettings, embed verified map directions) |
| `/sitemap/` | `core.views.SitemapView` | `core/sitemap.html` | Multiple | 200 | `https://www.novaboatridesnaivasha.co.ke/sitemap/` | Index, Follow | Human-readable HTML sitemap directory | `Nova sitemap`, `Lake Naivasha boat directory` | **KEEP** (Maintain real-time links to all published pages) |
| `/book/` | `bookings.views.BookingView` | `bookings/book.html` | `bookings.BookingLead` | 200 | `https://www.novaboatridesnaivasha.co.ke/book/` | Index, Follow | Low-friction 6-step booking-to-WhatsApp funnel | `book boat ride Naivasha` | **UPDATE** (Contextual pre-filled WhatsApp link generator) |

---

## 2. Experience Detail Pages (`/boat-rides/*`)

| URL | View Function / Class | Template | Primary Model | HTTP Status | Canonical URL | Indexability | Purpose | Primary Target Keyword | Recommended Action |
|---|---|---|---|---|---|---|---|---|---|
| `/boat-rides/classic-lake-safari/` | `tours.views.TourDetailView` | `tours/tour_detail.html` | `tours.Tour` | 200 | `https://www.novaboatridesnaivasha.co.ke/boat-rides/classic-lake-safari/` | Index, Follow | 1-hour introductory wildlife & hippo boat tour | `Lake Naivasha boat ride`, `classic boat safari` | **UPDATE** (Adopt standard 13-section template, server-side rates) |
| `/boat-rides/hippo-bird-safari/` | `tours.views.TourDetailView` | `tours/tour_detail.html` | `tours.Tour` | 200 | `https://www.novaboatridesnaivasha.co.ke/boat-rides/hippo-bird-safari/` | Index, Follow | Dedicated 1.5–2 hour ornithology & hippo photography tour | `Lake Naivasha boat safari`, `hippo boat tour Naivasha` | **UPDATE** (Target Tier 3 safari demand, clarify no guaranteed sightings) |
| `/boat-rides/crescent-island/` | `tours.views.TourDetailView` | `tours/tour_detail.html` | `tours.Tour` | 200 | `https://www.novaboatridesnaivasha.co.ke/boat-rides/crescent-island/` | Index, Follow | Water crossing + walking safari combo experience | `Crescent Island boat ride`, `boat to Crescent Island` | **UPDATE** (Target Tier 4, separate boat rate from sanctuary ticket) |
| `/boat-rides/sunset-cruise/` | `tours.views.TourDetailView` | `tours/tour_detail.html` | `tours.Tour` | 200 | `https://www.novaboatridesnaivasha.co.ke/boat-rides/sunset-cruise/` | Index, Follow | Golden hour evening cruise toward Longonot/Mau | `sunset boat cruise Naivasha`, `evening boat ride` | **UPDATE** (Highlight 16:45 PM timing and romantic couples appeal) |
| `/boat-rides/private-charter/` | `tours.views.TourDetailView` | `tours/tour_detail.html` | `tours.Tour` | 200 | `https://www.novaboatridesnaivasha.co.ke/boat-rides/private-charter/` | Index, Follow | Exclusive hire for families, VIPs, custom pacing | `private boat hire Naivasha`, `boat charter Lake Naivasha` | **UPDATE** (Clear per-boat pricing: KES 4,500/hr, not inflated 16k) |
| `/boat-rides/family-ride/` | `tours.views.TourDetailView` | `tours/tour_detail.html` | `tours.Tour` | 200 | `https://www.novaboatridesnaivasha.co.ke/boat-rides/family-ride/` | Index, Follow | Family-centric calm morning cruise with child life vests | `family boat ride Naivasha`, `Naivasha with kids` | **UPDATE** (Detail infant/child life vest safety, senior boarding) |
| `/boat-rides/photography-birding/` | `tours.views.TourDetailView` | `tours/tour_detail.html` | `tours.Tour` | 200 | `https://www.novaboatridesnaivasha.co.ke/boat-rides/photography-birding/` | Index, Follow | Specialized dawn bird photography charter | `Lake Naivasha bird watching boat`, `photo safari Naivasha` | **UPDATE** (Position Captain Josphat's birding credentials, 400+ species) |
| `/boat-rides/groups-events/` | `tours.views.TourDetailView` | `tours/tour_detail.html` | `tours.Tour` | 200 | `https://www.novaboatridesnaivasha.co.ke/boat-rides/groups-events/` | Index, Follow | Synchronized multi-boat flotillas for corporate offsites | `corporate boat rides Naivasha`, `team building boat safari` | **UPDATE** (Volume pricing tiers, LPO invoicing, safety compliance) |

---

## 3. Hotel Departures (`/hotel-boat-rides/*`)

| URL | View Function / Class | Template | Primary Model | HTTP Status | Canonical URL | Indexability | Purpose | Primary Target Keyword | Recommended Action |
|---|---|---|---|---|---|---|---|---|---|
| `/hotel-boat-rides/` | `partners.views.HotelHubView` | `partners/hotel_hub.html` | `partners.HotelPartner` | 200 | `https://www.novaboatridesnaivasha.co.ke/hotel-boat-rides/` | Index, Follow | Hotel-origin launch directory & HTMX checker | `boat ride from hotel Naivasha`, `hotel jetty boat rides` | **UPDATE** (Introduce HTMX `/hotel-access/check/` endpoint, use verified access status) |
| `/hotel-boat-rides/enashipai-resort-spa/` | `partners.views.HotelDetailView` | `partners/hotel_detail.html` | `partners.HotelPartner` | 200 | `https://www.novaboatridesnaivasha.co.ke/hotel-boat-rides/enashipai-resort-spa/` | Index, Follow | Jetty departure guide from Enashipai pier | `Enashipai boat ride`, `Enashipai boat safari` | **UPDATE** (Ensure relationship status is verified operational, not unverified "partner") |
| `/hotel-boat-rides/lake-naivasha-sopa-resort/` | `partners.views.HotelDetailView` | `partners/hotel_detail.html` | `partners.HotelPartner` | 200 | `https://www.novaboatridesnaivasha.co.ke/hotel-boat-rides/lake-naivasha-sopa-resort/` | Index, Follow | Jetty departure guide from Sopa lawn pier | `Lake Naivasha Sopa Resort boat ride` | **UPDATE** (Detail deep-water pier access, positioning fee notice) |
| `/hotel-boat-rides/kiboko-luxury-camp/` | `partners.views.HotelDetailView` | `partners/hotel_detail.html` | `partners.HotelPartner` | 200 | `https://www.novaboatridesnaivasha.co.ke/hotel-boat-rides/kiboko-luxury-camp/` | Index, Follow | Boutique tented camp private dock departures | `Kiboko Luxury Camp boat ride` | **UPDATE** (Clarify advance confirmation requirement) |
| `/hotel-boat-rides/great-rift-valley-lodge/` | `partners.views.HotelDetailView` | `partners/hotel_detail.html` | `partners.HotelPartner` | 200 | `https://www.novaboatridesnaivasha.co.ke/hotel-boat-rides/great-rift-valley-lodge/` | Index, Follow | Cliff-top lodge shuttle to Karagita Base | `Great Rift Valley Lodge boat ride` | **UPDATE** (Accurately label as ROAD_TRANSFER; property has no lake jetty) |

---

## 4. Accommodation Recommendations (`/stay/*`)

| URL | View Function / Class | Template | Primary Model | HTTP Status | Canonical URL | Indexability | Purpose | Primary Target Keyword | Recommended Action |
|---|---|---|---|---|---|---|---|---|---|
| `/stay/` | `stays.views.StayListView` | `stays/stay_list.html` | `stays.AccommodationProperty` | 200 | `https://www.novaboatridesnaivasha.co.ke/stay/` | Index, Follow | Curated directory of lakeside lodges | `where to stay in Naivasha`, `Lake Naivasha lodges` | **UPDATE** (Position as curated recommendations + enquiry, not instant booking engine) |
| `/stay/lake-naivasha-sopa-resort/` | `stays.views.StayDetailView` | `stays/stay_detail.html` | `stays.AccommodationProperty` | 200 | `https://www.novaboatridesnaivasha.co.ke/stay/lake-naivasha-sopa-resort/` | Index, Follow | Lodge profile + direct boat access notes | `Lake Naivasha Sopa Resort accommodation` | **UPDATE** (Add "Request Availability" CTA, indicative pricing disclaimers) |
| `/stay/enashipai-resort-spa/` | `stays.views.StayDetailView` | `stays/stay_detail.html` | `stays.AccommodationProperty` | 200 | `https://www.novaboatridesnaivasha.co.ke/stay/enashipai-resort-spa/` | Index, Follow | Resort profile + spa & boat combinations | `Enashipai Resort Naivasha stay` | **UPDATE** (Add verified date, disclaimer on third-party room rates) |
| `/stay/kiboko-luxury-camp/` | `stays.views.StayDetailView` | `stays/stay_detail.html` | `stays.AccommodationProperty` | 200 | `https://www.novaboatridesnaivasha.co.ke/stay/kiboko-luxury-camp/` | Index, Follow | Tented camp profile + private safari dock | `Kiboko Luxury Camp Naivasha` | **UPDATE** (Add enquiry funnel, link to private charter) |
| `/stay/camp-carnelleys-cottages/` | `stays.views.StayDetailView` | `stays/stay_detail.html` | `stays.AccommodationProperty` | 200 | `https://www.novaboatridesnaivasha.co.ke/stay/camp-carnelleys-cottages/` | Index, Follow | Rustic eco-camp cottages & restaurant | `Camp Carnelleys Naivasha` | **UPDATE** (Clarify boat access mode via nearby jetty) |

---

## 5. Curated Safari Packages (`/packages/*`)

| URL | View Function / Class | Template | Primary Model | HTTP Status | Canonical URL | Indexability | Purpose | Primary Target Keyword | Recommended Action |
|---|---|---|---|---|---|---|---|---|---|
| `/packages/` | `packages.views.PackageListView` | `packages/package_list.html` | `packages.Package` | 200 | `https://www.novaboatridesnaivasha.co.ke/packages/` | Index, Follow | Multi-day combo package catalog | `Lake Naivasha safari packages`, `Naivasha weekend packages` | **UPDATE** (Ensure all estimates calculate from canonical rate models) |
| `/packages/stay-and-ride/` | `packages.views.PackageDetailView` | `packages/package_detail.html` | `packages.Package` | 200 | `https://www.novaboatridesnaivasha.co.ke/packages/stay-and-ride/` | Index, Follow | 2D/1N Lodge stay + morning boat safari | `Naivasha stay and boat ride package` | **UPDATE** (Server-side quote breakdown with clear exclusions) |
| `/packages/couples-lake-escape/` | `packages.views.PackageDetailView` | `packages/package_detail.html` | `packages.Package` | 200 | `https://www.novaboatridesnaivasha.co.ke/packages/couples-lake-escape/` | Index, Follow | Romantic weekend: sunset cruise + luxury lodge | `Naivasha couples weekend package` | **UPDATE** (Link directly to contextual WhatsApp couples booking) |
| `/packages/family-naivasha-weekend/` | `packages.views.PackageDetailView` | `packages/package_detail.html` | `packages.Package` | 200 | `https://www.novaboatridesnaivasha.co.ke/packages/family-naivasha-weekend/` | Index, Follow | Family package: boat ride + Crescent Island | `Lake Naivasha family weekend package` | **UPDATE** (Explicit adult and child fee separation) |
| `/packages/hells-gate-and-lake/` | `packages.views.PackageDetailView` | `packages/package_detail.html` | `packages.Package` | 200 | `https://www.novaboatridesnaivasha.co.ke/packages/hells-gate-and-lake/` | Index, Follow | Land & water day combo: Gorge cycling + boat | `Hells Gate and Lake Naivasha day tour` | **UPDATE** (Itemize KWS park fees vs bike hire vs boat charter) |

---

## 6. Guides & Field Notes (`/journal/*`)

All 30 published guide articles are indexed under `/journal/`. Key priority articles and their recommended operational alignment:

| URL | View Function / Class | Template | Word Count | Indexability | Purpose | Primary Target Keyword | Recommended Action |
|---|---|---|---|---|---|---|---|
| `/journal/` | `content.views.JournalListView` | `content/journal_list.html` | N/A | Index, Follow | Hub for all trip-planning field notes | `Lake Naivasha guides`, `Naivasha travel advice` | **UPDATE** (Add category filters, maintain pagination, remove jargon) |
| `/journal/lake-naivasha-boat-ride-price-guide/` | `content.views.JournalDetailView` | `content/journal_detail.html` | 2,123 | Index, Follow | Definitive price guide | `Lake Naivasha boat ride price` | **UPDATE** (Pull numbers from ExperienceRate, replace competitor attacks with objective advice) |
| `/journal/crescent-island-boat-ride-price-breakdown/` | `content.views.JournalDetailView` | `content/journal_detail.html` | 1,868 | Index, Follow | Sanctuary fee vs boat fee breakdown | `Crescent Island boat ride price` | **UPDATE** (Update official Crescent Island fees: Citizen KES 800/400; Resident KES 1,100/550; Non-resident $33/$16) |
| `/journal/boat-riding-in-nairobi-vs-lake-naivasha/` | `content.views.JournalDetailView` | `content/journal_detail.html` | 1,764 | Index, Follow | Capture Nairobi search intent | `Boat riding in nairobi` | **KEEP & REFINE** (Maintain strong routing from Nairobi to Naivasha) |
| `/journal/ultimate-one-day-lake-naivasha-boat-ride-itinerary/` | `content.views.JournalDetailView` | `content/journal_detail.html` | 1,759 | Index, Follow | Step-by-step day safari schedule | `Day boat rides naivasha` | **KEEP & REFINE** (Natural links to `/boat-rides/` and `/prices/`) |
| `/journal/lake-naivasha-boat-ride-and-crescent-island-guide/` | `content.views.JournalDetailView` | `content/journal_detail.html` | 1,919 | Index, Follow | Walking safari combo guide | `Lake naivasha boat ride and crescent island` | **KEEP & REFINE** (Remove AI jargon, ensure date-stamped fees) |
| `/journal/lake-naivasha-boat-ride-review-2026/` | `content.views.JournalDetailView` | `content/journal_detail.html` | 1,721 | Index, Follow | Quality & 5-star expectations | `Lake Naivasha boat ride review` | **UPDATE** (Ensure objective tone, zero fabricated testimonials) |
| `/journal/best-boat-rides-naivasha-operator-comparison/` | `content.views.JournalDetailView` | `content/journal_detail.html` | 1,628 | Index, Follow | Launch site comparisons | `Best boat rides naivasha` | **UPDATE** (Refactor into neutral "How to Choose an Operator" guide) |
| `/journal/lake-naivasha-boat-safari-faqs-35-expert-answers/` | `content.views.JournalDetailView` | `content/journal_detail.html` | 2,221 | Index, Follow | Megaguide FAQ addressing top search queries | `Lake Naivasha boat safari FAQs` | **UPDATE** (Update Crescent Island fees to official schedule) |
| `/journal/how-to-choose-best-boat-ride-operator-naivasha/` | `content.views.JournalDetailView` | `content/journal_detail.html` | 1,520 | Index, Follow | Consumer safety checklist | `best boat rides naivasha`, `boat ride operator` | **KEEP & REFINE** (Focus on 10 objective criteria per PRD Section 10) |
| *[Remaining 20 guide articles]* | `content.views.JournalDetailView` | `content/journal_detail.html` | 1,400–1,800 | Index, Follow | In-depth topic coverage (birding, hippos, timing, weather, corporate, etc.) | Various | **KEEP & AUDIT** (Clean jargon, ensure dates and source links) |

---

## 7. Technical, SEO & Crawler Endpoints

| URL | View Function / Class | Output Type | HTTP Status | Purpose | Recommended Action |
|---|---|---|---|---|---|
| `/sitemap.xml` | `django.contrib.sitemaps.views.sitemap` | XML | 200 | Flat canonical XML sitemap for Google Search Console | **KEEP & OPTIMIZE** (Ensure 100% of indexable URLs are included with HTTPS) |
| `/sitemap_index.xml` | `django.contrib.sitemaps.views.index` | XML | 200 | Sectioned sitemap index | **KEEP** (Clean secondary crawler index) |
| `/robots.txt` | `seo.views.robots_txt` | Text/Plain | 200 | Dynamic crawler directives with sitemap references | **KEEP** (Ensure disallows are correct and sitemap URLs are absolute HTTPS) |
| `/questions/` | `content.views.FAQView` | HTML | 200 | Categorized FAQ knowledge base | **UPDATE** (Pull questions from verified data) |
| `/tinymce/*` | TinyMCE editor | HTML/JS | 200 | Admin rich text editor helper endpoints | **KEEP** (Restricted to authenticated staff) |
| `/admin/*` | `django.contrib.admin` | HTML | 200/302 | Staff management console | **KEEP** (Add verification badges and fresh data indicators) |
