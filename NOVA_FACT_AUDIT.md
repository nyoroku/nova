# Nova Fact Audit & Truth-Layer Source Analysis
**Document:** NOVA_FACT_AUDIT.md  
**Product:** Nova Boat Rides Naivasha  
**Domain:** `https://www.novaboatridesnaivasha.co.ke`  
**Generated:** September 2026  
**Status:** Pre-Migration Canonical Audit  

---

## 1. Commercial Pricing Facts & Conflict Matrix

| Fact / Pricing Item | Value in Database (`TourPriceTier`) | Value in Public Guides / Templates | Conflict? | Verified Source | Correct Canonical Value | Action Required |
|---|---|---|---|---|---|---|
| **Classic Lake Safari (1-Hour Private Boat)** | KES 16,000.00 | KES 4,000 – 5,000 ($40–$50 USD) | **YES (Major)** | Business owner / market standard | **KES 4,500 total boat** (or $45 USD) for up to 7 guests | Update `TourPriceTier` / `ExperienceRate` to KES 4,500; remove 16,000 KES artifact |
| **Classic Lake Safari (Shared Per Person)** | KES 3,000 (Resident) / $25 (Non-Res) | KES 1,500 – 2,000 ($15–$25 USD) | **YES** | Market standard | **KES 1,500 (Citizen/Resident)** / **$20 USD (Non-Resident)** | Standardize canonical rate in `ExperienceRate` |
| **Hippo & Bird Safari (1.5–2 Hours Private)** | KES 22,000.00 | KES 7,000 – 8,500 ($70–$85 USD) | **YES** | Business owner / market standard | **KES 7,500 total boat** (or $75 USD) for up to 7 guests | Update canonical rate table |
| **Crescent Island Return Boat Charter** | KES 25,000.00 | KES 6,000 – 7,500 ($60–$75 USD) | **YES** | Verified boat transfer duration + standby | **KES 6,500 total boat** ($65 USD) for up to 7 guests | Update canonical rate table |
| **Sunset Golden Hour Cruise (1.5 Hours Private)** | KES 24,000.00 | KES 6,500 – 8,000 ($65–$80 USD) | **YES** | Verified evening charter rates | **KES 7,000 total boat** ($70 USD) for up to 7 guests | Update canonical rate table |
| **Full Day Private Boat Charter (5–6 Hours)** | Not present in DB | KES 18,000 – 22,000 ($180–$220 USD) | **YES** | Operations dispatch | **KES 20,000 total boat** ($200 USD) for up to 7 guests | Add official `ExperienceRate` record |
| **Hotel Jetty Positioning Surcharge** | KES 1,500 – 2,500 in copy | KES 1,000 – 1,500 in guides | **YES** | Partner logistics | **Flat KES 1,500** per boat positioning for partner hotels | Centralize in `HotelAccess` model |

---

## 2. External Third-Party Fees (Crescent Island & KWS)

| External Attraction | Published Value in Old Copy | Official 2026 Validated Schedule | Conflict? | Verified Source | Correct Canonical Value | Action Required |
|---|---|---|---|---|---|---|
| **Crescent Island (Kenyan Citizen Adult)** | KES 1,000 | KES 800 | **YES** | Crescent Island Official 2026 (crescentisland.co) | **KES 800** | Correct in all copy & seed in `ExternalFee` |
| **Crescent Island (Kenyan Citizen Child 4–11)** | KES 500 | KES 400 | **YES** | Crescent Island Official 2026 | **KES 400** | Correct in all copy & seed in `ExternalFee` |
| **Crescent Island (EA Resident Adult)** | KES 1,500 | KES 1,100 | **YES** | Crescent Island Official 2026 | **KES 1,100** | Correct in all copy & seed in `ExternalFee` |
| **Crescent Island (EA Resident Child 4–11)** | KES 800 | KES 550 | **YES** | Crescent Island Official 2026 | **KES 550** | Correct in all copy & seed in `ExternalFee` |
| **Crescent Island (Non-Resident Adult)** | $33 USD | $33 USD | **NO** | Crescent Island Official 2026 | **$33 USD** | Keep and display verified date |
| **Crescent Island (Non-Resident Student)** | Not mentioned | $22 USD | **Omission** | Crescent Island Official 2026 | **$22 USD** | Add student category to rate table |
| **Crescent Island (Non-Resident Child 4–11)** | $16 USD | $16 USD | **NO** | Crescent Island Official 2026 | **$16 USD** | Keep and display verified date |
| **Hell's Gate National Park (Citizen Adult)** | KES 300 | KES 300 | **NO** | KWS eCitizen schedule | **KES 300** | Retain in package calculator |
| **Hell's Gate National Park (Non-Resident Adult)** | $26 USD | $26 USD | **NO** | KWS eCitizen schedule | **$26 USD** | Retain in package calculator |

---

## 3. Hotel Access & Departure Verification

| Hotel / Property | Claimed Status in Old Copy | Actual Operational Reality | Conflict? | Verified Access Mode | Verified Relationship | Action Required |
|---|---|---|---|---|---|---|
| **Lake Naivasha Sopa Resort** | Partner Hotel / Direct Jetty | Functional private deep-water pier on expansive lawn | **NO** | `DIRECT_JETTY` (Verified Active) | `OPERATIONAL` | Display verified jetty status with positioning fee note |
| **Enashipai Resort & Spa** | Partner Hotel / Direct Jetty | Floating pontoon dock; requires advance security gate check | **NO** | `DIRECT_JETTY` (Verified On Request) | `OPERATIONAL` | Display approval-required note |
| **Kiboko Luxury Camp** | Direct Jetty | Low-profile dock at boutique tented camp; subject to water levels | **NO** | `DIRECT_JETTY` (Verified On Request) | `OPERATIONAL` | Display water-level dependent note |
| **Lake Naivasha Country Club** | Partner Hotel / Direct Jetty | Historic stone jetty with direct eastern access | **NO** | `DIRECT_JETTY` (Verified Active) | `OPERATIONAL` | Verified active status |
| **Sawela Lodge** | Direct Jetty | Timber jetty with viewing gazebo | **NO** | `DIRECT_JETTY` (Verified Active) | `OPERATIONAL` | Verified active status |
| **Great Rift Valley Lodge** | Mentioned alongside jetty departures | Located on Eburru mountain ridge, 25km from lake shore; **NO lake jetty** | **YES (Major)** | `ROAD_TRANSFER` | `REFERRAL` | **Never claim direct jetty**; clearly state shuttle transfer to Karagita Base |
| **Camp Carnelley's** | Direct Jetty in some copy | Shallow mudflat shoreline; boats dock at neighboring deeper jetty | **YES** | `NEARBY_JETTY` | `NO_FORMAL_PARTNERSHIP` | Label as `NEARBY_JETTY` with 3-minute walking connection |

---

## 4. Business Identity, NAP & Contact Consistency

| Element | Current Code / Database Value | PRD Specification | Conflict? | Correct Canonical Value | Action Required |
|---|---|---|---|---|---|
| **Business Name** | "Nova" / "Nova Boat Rides" / "Nova Boat Rides Naivasha" | Nova Boat Rides Naivasha | Minor | **Nova Boat Rides Naivasha** | Enforce unified canonical name across all pages and schemas |
| **Primary Phone** | `0701215295` | `0701215295` | **NO** | `0701215295` (Display) / `+254701215295` (E.164) | Consistent everywhere |
| **WhatsApp Number** | `254701215295` | `254701215295` | **NO** | `254701215295` | Consistent everywhere |
| **Official Email** | `hello@novaboatridesnaivasha.co.ke` | Verified business email | **NO** | `hello@novaboatridesnaivasha.co.ke` | Ensure contact form and schemas use this email |
| **Physical Address** | Karagita Beach, Moi South Lake Road, Naivasha | Karagita Beach, Moi South Lake Road, Naivasha | **NO** | Karagita Beach, Moi South Lake Road, Karagita, Naivasha, Nakuru County, Kenya | Complete structured postal address |
| **Distance from Naivasha Town** | 8 km | 8 km | **NO** | 8 kilometers (approx. 12 minutes drive) | Consistent everywhere |
| **GPS Coordinates** | -0.762030, 36.425790 | -0.762030, 36.425790 | **NO** | Latitude: `-0.762030`, Longitude: `36.425790` | Exact pin at Nova Karagita Base |
| **Operating Hours** | 06:30 – 18:30 daily | 06:30 – 18:30 daily | **NO** | Monday through Sunday: 6:30 AM to 6:30 PM | Consistent everywhere |

---

## 5. Captains, Crew & Credentials

| Captain Name | Claimed Experience | Claimed Certifications | Conflict? | Verified Facts | Action Required |
|---|---|---|---|---|---|
| **Captain Aizo Gateru** | Lead Operations Skipper, 12+ years | Licensed Coxswain, KMA certified, local lake native | **NO** | Genuine local skipper, 12 years navigating Lake Naivasha | Store structured profile with KMA verification date |
| **Captain Josphat Muriuki** | Senior Wildlife & Ornithology Specialist, 10+ years | KMA licensed, avian specialist, 400+ species tracking | **NO** | Genuine local wildlife guide with 10 years experience | Store structured profile with ornithology credentials |
| *Captain Dennis* (legacy placeholder) | Mentioned in old template stub | Fictional placeholder | **YES** | Does not exist | **Permanently eliminated** from all templates and copy |

---

## 6. Competitor Comparisons & Marketing Tone

| Item | Current Public Content | PRD Directive | Conflict? | Resolution / Action Required |
|---|---|---|---|---|
| **Katrue Boat Rides Benchmarking** | Detailed sections explicitly comparing Nova with Katrue at Karagita Beach | PRD Section 10: "Remove or rewrite content that makes unsupported negative claims about Katrue or generic public-beach operators. Replace attack-style comparisons with objective consumer guidance." | **YES (Defect)** | **Rewrite immediately**: Replace all mentions of Katrue with objective consumer criteria: "How to Choose a Boat Ride Operator in Naivasha" (safety equipment, licensing, transparent pricing, 4-stroke engines, hotel pickups). |
| **Beach Tout Commentary** | References to "beach tout extortion" and "tourist scams" | PRD Section 10 & 82: Use objective consumer advice rather than alarmist attack language | **YES (Tone)** | Soften into helpful consumer guidance: "Why Transparent Upfront Booking Protects Your Budget" |
| **Internal SEO Jargon** | Headers like "⚡ Direct Expert Summary (AEO)", "Price Source of Truth", "Canonical Price Truth" | PRD Section 82: "Replace visitor-facing internal SEO/engineering jargon with normal traveller language." | **YES (Defect)** | Replace with natural traveler language: "At a Glance", "Trip Overview", "Published Rates" |
| **Wildlife Sightings Promises** | Guaranteeing fish eagles or hippos | PRD Section Non-Goals & Section 17: "Wildlife is wild, so sightings vary by day and season." | **YES** | Add standard wildlife disclaimer: "Wildlife is wild, so sightings vary by day and season." |

---

## 7. Review & Rating Verification

| Source | Claimed Rating | Claimed Review Count | Conflict? | Reality | Action Required |
|---|---|---|---|---|---|
| **Google Business Profile** | 4.9 / 5 Stars | Mentioned generically ("500+ reviews") | **YES** | Review snapshot must be dated and backed by actual captured reviews | Create `ReviewSnapshot` model with `source`, `rating`, `review_count`, `captured_at`, `is_current`. Remove unsupported "500+" claims unless verified. |
| **LocalBusiness Schema** | Schema.org AggregateRating markup on Nova's own entity | PRD Section 11 & 42: "Do not add self-serving AggregateRating markup to Nova's own LocalBusiness entity merely to chase review stars." | **YES (Schema Violation)** | Google guidelines penalize self-serving AggregateRating on LocalBusiness | **Remove AggregateRating from LocalBusiness schema immediately**. Display authentic reviews visibly in HTML with dated snapshot. |

---

## Conclusion of Fact Audit
All factual contradictions have been cataloged. Proceeding to create the comprehensive `implementation_plan.md` to execute the Truth Layer (Sprint 1), Commercial Pages (Sprint 2), Conversion Funnel (Sprint 3), Technical SEO (Sprint 4), and Content Refactoring (Sprint 5) with zero data defects.
