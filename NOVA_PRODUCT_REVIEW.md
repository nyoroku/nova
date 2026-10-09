# Nova product review and proposed build direction

Reviewed: 8 October 2026 (Africa/Nairobi).

## Recommendation

Use the supplied activities PRD as the foundation for expanding the existing Nova Django website. Resolve commercial inconsistencies before expanding the public catalogue. Retain the planned ten activities, with the two new activities initially in draft. Publish each activity only when its operational details, pricing and imagery are verified.

The user's request is to review, compare international practices, and discuss before building. The document's execution instructions are proposed requirements to evaluate; they do not authorize deployment, Google Business Profile changes, or immediate implementation. This review makes no application or database changes.

## Evidence and review limits

Reviewed the DOCX product content, the local tour and booking models/views/templates, relevant existing audit reports, and selected tour/rate records through a read-only SQLite connection. Also inspected the publicly retrievable boat-rides page and current official platform guidance. This is a product and initial architecture review, not a rendered DOCX layout audit, full application security audit, performance measurement, or end-to-end booking test. Existing reports' claims of completion are historical claims, not fresh verification.

Source document: `C:/Nova_Codex_Activities_PRD_Product_Spec_REBUILT.docx`.

## Strengths to retain

- Ten distinct planned experiences, supported by one reusable product template.
- Preservation of existing indexed slugs when only public names change.
- Django server rendering, small HTMX enhancements and a lightweight accessible gallery.
- Explicit inclusions, exclusions, departure instructions and realistic wildlife expectations.
- Authentic product imagery with rights and consent recorded.
- Versioned prices and separately identified external fees.
- Product-specific enquiries and attribution; a WhatsApp click is not a booking.
- Mapping search intents to real activities instead of creating thin pages for spelling variations.

## Issues to resolve before implementation

### 1. Pricing is still split across competing systems

`Tour.current_rates` reads `ExperienceRate`, but starting-price helpers can fall back to `TourPriceTier`. The detail page, quote endpoint, related cards and booking submission still use legacy tiers in different ways.

The publicly retrieved catalogue displays KES 1,500 as per boat for the classic ride. The local canonical rate record identifies that amount as a shared seat per person. The same public page's FAQ quotes KES 3,000 per resident adult and KES 16,000 per private boat. These are inconsistent customer-facing offers.

The private-charter card also combines a two-hour duration with a KES 4,500 hourly rate and a USD 200 full-day rate. Independently choosing the lowest KES and USD values does not identify the same booking option.

Proposed correction: one quote service selects a specific bookable option and applicable rate using party size, mode, service date, audience and currency. It returns the amount, unit, duration, capacity and cost breakdown together. All pages, estimates, lead quotes and future exports use that result. Missing rates produce a request-for-quote state rather than a fabricated number. Quotes should retain a snapshot of the accepted option, rate and terms.

### 2. Booking calculations can misrepresent the offer

The local booking POST handler selects the lowest active legacy tier and multiplies it by adults and half-price children without checking whether the tier is per boat. It hardcodes a KES 2,000 hotel positioning fee. The tour quote endpoint hardcodes KES 3,000 per guest when no rate matches and can fall back to a tier outside the requested mode/capacity.

Proposed correction: remove monetary fallbacks, confirm child-price rules, enforce option capacity and minimum party size, and derive hotel logistics from verified hotel-access configuration. For groups, distinguish total party capacity from each boat's passenger limit and allocation.

### 3. Product durations and capacity disagree

| Activity | Local tour duration | Local rate duration | PRD proposal |
|---|---:|---:|---:|
| Hippo & Bird Safari | 90 minutes | 120 minutes | 90 minutes |
| Crescent Island | 120 minutes | 150 minutes | 120 minutes |
| Family ride | 72 minutes (`1.2` hours) | 120 minutes | 75 minutes |
| Birding/photography | 150 minutes | 180 minutes | 150 minutes |
| Group/corporate | 120 minutes | 90 minutes | 120 minutes |
| Private charter | 120 minutes | 60-minute and 360-minute options | 120 minutes |

Several tour records allow eight passengers while their rate records allow seven; the photography tour allows six while its rate allows four. These values require an operational decision, not a display-only rename. Store exact integer minutes, and distinguish total experience duration from boat time where relevant. Do not discard genuine hourly or full-day options to fit a new public title.

### 4. Google readiness needs separate checks

Manual Business Profile activities and connectivity feeds are separate management paths. Google's Business Profile help explicitly tells operators to follow Things to do general and price policies. Its manual activity editor requires a name and booking URL; the PRD's six-image minimum is Nova's editorial quality rule, not a stated manual-editor requirement. [Google activity guidance](https://support.google.com/business/answer/12944910)

Google price policy requires submitted prices to include mandatory taxes and fees, including charges collected at the activity. It also sets rules for standard adult pricing and minimum transaction costs for group products. For Crescent Island, retain an itemized fee breakdown, but determine whether each advertised option is transfer-only or a combined island experience and which fees are mandatory for that option. Local-resident rates should not automatically become the general Google feed price. [Google price policy](https://support.google.com/google-ads/answer/11387663)

Google requires distinct, accurately represented products, concise titles, matching durations and authorized imagery. The current image policy specifies dimensions from 300 x 300 through 4000 x 4000 pixels. [Google content and referral policy](https://support.google.com/google-ads/answer/10723240)

A readiness boolean cannot establish that Google accepts a product or an enquiry-only booking path. Use a computed checklist and store external submission/acceptance status separately. Google recommends a connectivity partner for an individual operator. Evaluate providers only after confirming Kenyan coverage, inventory model, payment support, costs and export requirements. [Approved connectivity guidance](https://support.google.com/hotelprices/answer/13189190)

### 5. Thirty service intents should become clear navigation

The PRD correctly avoids thirty thin URLs, but displaying every close keyword variant as a separate service still risks repetitive navigation. Preserve all thirty proposed intents in the content/admin mapping while presenting customer groups such as wildlife, Crescent Island, private rides, families, sunrise/sunset, photography, groups and hotel departures.

Do not export birthday decorations, hotel pickups or other capabilities as available services until operations confirm them. Google's service editor availability depends on category; confirm the actual Nova profile supports it. Prices and phone numbers are prohibited in custom service names, while separate descriptions/prices are supported. [Google services guidance](https://support.google.com/business/answer/9455399)

### 6. The mobile product template needs a shorter decision path

Keep the specified content depth, but move booking-critical information near the top: title, duration, private/shared option, price and unit, mandatory fees, confirmation mode and CTA. Follow with the gallery and a compact inclusions/exclusions summary. Put longer itinerary, wildlife interpretation and detailed FAQs below. Present cancellation, weather, arrival and boarding constraints before commitment.

Use progressive disclosure where useful, but keep essential product details server-rendered and available without JavaScript. Gallery interactions should support keyboard and touch, visible focus, reduced motion and no autoplay. [W3C carousel guidance](https://www.w3.org/WAI/tutorials/carousels/)

### 7. Operational ownership and measurement need more detail

Assign a person responsible for responding to leads, approving product facts, updating fees and confirming hotel access. Record explicit verification dates and evidence: an automatic date update on saving a record is not evidence that its facts were checked.

Existing leads already have useful statuses. Extend them rather than creating another lead system. Capture `utm_content`, preserve the original landing attribution through navigation, and keep enquiry, quote, confirmed booking, completion and revenue distinct. Measure response time and quote-to-booking conversion alongside traffic and CTA clicks.

Clarify guest cancellation deadlines, deposits, refunds, late arrival/no-show handling, languages actually supported, minimum ages or equipment constraints, and boarding accessibility. Add payment processing only once fulfilment and refund workflows are defined. Keep customer details out of analytics events.

## International practices and their application

These are selected examples, not an exhaustive ranking or evidence that one platform converts best.

| Benchmark | Observed practice | Proposed Nova application |
|---|---|---|
| GetYourGuide, Europe/global | Cancellation and payment conditions attach to the specific activity; selected products support reserve-now/pay-later. | Show Nova's actual cancellation and payment terms beside booking actions. Introduce deferred/deposit payment only when operationally supported. |
| Viator, US/global | Booking details connect tour options, inclusions/exclusions, departure details, cancellation and tickets. | Carry a chosen option and departure context from product page through quote and confirmation. |
| Klook, Asia/global | Distinguishes instant confirmation from activities requiring later confirmation. | Say whether the guest is requesting availability or receiving a confirmed booking; use an owner-approved response expectation. |
| RealNZ, New Zealand | Explains weather, what to bring, food inclusion and cancellation; wildlife is explicitly unpredictable. | Provide practical preparation and safety/weather explanations, and avoid guaranteed sightings. |
| SafariBookings, African travel | Reviews listing quality and emphasizes realistic itineraries, clear inclusions/exclusions and operator verification. | Require evidence for licences, relationships and inclusions before publishing trust claims. |

Sources: [GetYourGuide terms](https://www.getyourguide.com/c/general-terms-and-conditions/), [Viator booking management](https://agentcenter.viator.com/resources/manage-booking/), [Klook help](https://www.klook.com/en-SG/help-center/), [RealNZ cruise product](https://www.realnz.com/en/experiences/day-cruises/milford-sound-signature-cruise/), [SafariBookings quality and transparency](https://www.safaribookings.com/tour-quality-and-transparency).

## Proposed architecture

Extend `Tour`, `ExperienceRate`, `ExternalFee`, `HotelAccess` and `BookingLead` rather than introducing parallel replacements. Add explicit tour booking options where duration, shared/private mode or capacity changes the offer. Link each rate to its option. Add structured highlights, itinerary steps, inclusions/exclusions, product FAQs, ordered gallery media, publication states and intent mappings.

Derive canonical URLs from named routes and the configured site origin. Treat third-party booking URLs as separate fields. Preserve originals and produce responsive image derivatives. Publication validation should distinguish website quality rules, Google data requirements and externally confirmed operational facts.

Keep Django, HTMX and Alpine. The current framework is sufficient for this scope.

## Proposed build sequence

1. Inventory routes, content, media, pricing and booking paths. Confirm an owner-approved option/duration/capacity/rate matrix. Preserve the eight existing slugs.
2. Unify pricing and quote calculations, remove stale monetary literals, and verify fee breakdowns across cards, details, enquiries and confirmations.
3. Add publication states, structured content and galleries with additive migrations and an admin readiness checklist.
4. Build one representative activity page and mobile enquiry flow for review, then apply the shared template to the existing catalogue.
5. Create sunrise and extended-explorer drafts. Define actual routes, operating windows, prices and authentic imagery before publication.
6. Rebuild the boat-rides hub and service navigation; preserve the thirty intent mappings without creating duplicate pages.
7. Complete attribution, lead outcomes, Google export preparation, accessibility, mobile and URL checks. Publish Google listings only after channel checks pass.
8. Evaluate deposits/payments and an approved connectivity provider as a subsequent phase.

## Acceptance checks to add to the PRD

- The same selected option has the same unit, duration, capacity, currency and valid price in every customer and export path.
- Rate resolution uses the intended service date; expired, future-inapplicable and ambiguous rates cannot silently become an offer.
- Per-boat amounts are not multiplied by guest count; child discounts exist only when configured.
- Missing rates and unsupported party sizes request a quote without fabricated totals.
- External mandatory costs are itemized and included in channel totals where required.
- Unverified drafts cannot enter public catalogues, sitemaps or Google exports.
- Existing URLs remain valid; redirects are explicitly tested if any become necessary.
- Gallery and enquiry flows work with keyboard, touch, reduced motion and JavaScript unavailable.
- Performance targets are assessed using real-user data at the 75th percentile by mobile/desktop, with laboratory tests used for regression checks. [Web Vitals guidance](https://web.dev/articles/vitals)
- Enquiry submission creates one lead with the chosen product context and preserved attribution; confirmed booking reporting requires an actual operational status change.

## Discussion decisions

The first-release booking model, priority customer audience and progressive publication approach are awaiting the user's preference. Recommended starting point: equal clarity for domestic and international guests, availability enquiry plus WhatsApp confirmation, and progressive publication toward the ten-activity catalogue. Exact rates, durations, capacities, policies and permissions still need business verification; no prices in this review are treated as owner-approved merely because they exist in code.
