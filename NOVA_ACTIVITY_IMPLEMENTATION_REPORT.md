# Nova activities rebuild: implementation and launch status

Date: 9 October 2026 (Africa/Nairobi). Branch: `codex/nova-activities`.

## Outcome

The existing Django application now has a structured ten-activity plan, a single pricing/quote path, richer reusable product pages, a responsive gallery, improved availability enquiries, service-intent mappings, lead outcome reporting, and internal Google distribution readiness exports.

The local and production catalogues contain eight existing public activities and two new drafts. No existing activity slug changed. Sunrise and Full Lake Explorer remain unpublished pending business verification. The application was pushed to GitHub and deployed to PythonAnywhere on 9 October 2026; see `NOVA_ACTIVITY_DEPLOYMENT_REPORT.md`. Google publication has not been performed.

## Catalogue and pricing

- Existing eight public names were updated while their legacy names and descriptions were retained internally for reference.
- Two draft products were added without invented rates, routes, operating windows or photos.
- `TourOption` separates shared/private/group arrangements and durations. Existing `ExperienceRate` amounts were retained and mapped to the matching option.
- A shared quote service now drives tour estimates, booking submissions and package boat estimates. Legacy `TourPriceTier` rows remain as read-only history and are no longer a public fallback.
- Rates must be active, applicable to the service date, unambiguous and consistent with their option. Missing or mismatched rates request a quote.
- Per-boat totals are not multiplied by passengers. Per-person child prices require an explicit configured amount; no automatic half-price discount remains.
- Minimum party sizes and minimum transaction costs are displayed for group offers.
- Mandatory attraction charges are itemized and included in complete same-currency estimates. Unknown eligibility, expired fees, unsupported currency combinations and unverified hotel logistics leave the full total pending confirmation.
- Hourly KES rates are no longer paired with unrelated full-day USD prices.

The PRD's proposed duration suffixes were withheld where business facts conflict. For example, the family product's historical tour record says 72 minutes, its rate says 120 minutes, and the PRD proposes 75 minutes. Current option/rate information is presented consistently; a new commercial duration or price has not been invented to resolve that disagreement.

## Customer experience

- Rebuilt the activity hub, shared detail template and prices page using the existing Nova design system.
- Product pages include a clear summary, price/unit/option information, highlights, inclusions/exclusions, typical itinerary, fee breakdown, departure information, wildlife expectations, preparation, safety/weather/cancellation information, suitability, FAQs and related activities.
- Galleries render images server-side and support Alpine navigation, thumbnails, keyboard controls and native horizontal scrolling. Single-image legacy pages show a photo without redundant carousel controls.
- Originals are retained; derivatives are limited to 1280 and 480 pixels with responsive selection, dimensions, priority for the first image and lazy loading afterward.
- Existing image references were migrated without declaring their rights or authenticity verified. Seven available legacy gallery images were optimized. The missing family image was withheld and a clear placeholder is shown. Additional genuine photos are still required.
- New image publication through admin requires recorded rights/guest consent. Google use also requires a unique eligible primary image.
- Enquiries preserve the chosen option, party and date. Changing an activity refreshes its option choices with HTMX; the form also works with ordinary server submission.
- Duplicate submissions use a session-authorized unique submission key and create one lead. Quote snapshots preserve the original selected option, amounts and displayed terms.
- No account or online payment is required. An enquiry is explicitly distinct from a confirmed booking.

## Services and search

All 15 primary and 15 secondary search intents are stored as structured mappings. Public service navigation groups needs and deduplicates close variants by destination. No thirty-page service expansion was created, and draft activities do not appear as available service destinations.

Canonical URLs use the configured site origin and omit tracking/filter parameters. Draft and paused activities are excluded from public routing and sitemaps. Booking/estimate helper responses are not intended for indexing. Product JSON-LD is serialized safely and reflects visible names/descriptions without fabricated reviews or offers.

Price-bearing guide and FAQ copy now directs customers to the current rate/fee source. Original guide structure, images and non-price explanation were preserved where appropriate, and earlier copy was archived internally. Unsupported review totals and certification claims were replaced with evidence-backed displays. Explicit verification dates do not advance merely because a record is saved.

## Attribution and operations

The URL builder distinguishes `gbp_profile`, `gbp_activities`, `gbp_posts` and `things_to_do`, using organic Google attribution and activity-specific content. Internal links do not carry UTMs. All four UTM fields are preserved for submitted leads.

The enquiry lifecycle now supports a separate CONTACTED stage and records response, confirmation and completion timestamps. The staff-only outcomes page at `/book/operations/` reports recent enquiries, activity/campaign/content, recorded response time, and explicitly entered confirmed/completed revenue by currency. It does not count WhatsApp clicks as bookings.

GA4 hooks are implemented for product views, galleries, price/itinerary visibility, availability/WhatsApp/phone/directions, service links, related activities and enquiry submission. Optional analytics require visitor opt-in and a configured, verified GA4 stream. Names, phone numbers, form values and WhatsApp URLs are not included in Nova's manual event payloads. Page URLs/referrers omit query parameters.

Before enabling the stream, disable GA4 Enhanced Measurement, particularly automatic outbound/form tracking, then confirm the setup in SiteSettings. Automatic outbound tracking can otherwise collect complete link URLs. Nova supplies manual events and pageviews to avoid that collection and duplicate pageviews. See [Google's enhanced-measurement guidance](https://support.google.com/analytics/answer/9216061?hl=en) and [manual pageview guidance](https://developers.google.com/analytics/devguides/collection/ga4/views).

## Publication controls

New READY/PUBLISHED activities must pass the content, media, pricing and operational checklist. The eight previously public records are explicitly grandfathered to preserve their existing routes; this does not mark them Google-ready. A paused legacy activity cannot be republished through the verified publication action without completing its checklist.

Google readiness is computed, not assumed from a checkbox. Submission/acceptance status is recorded separately. The internal export currently reports **zero Google-ready activities** because required evidence, photos and booking-path confirmation are incomplete. Six photos is Nova's editorial threshold, not a claimed requirement of Google's manual activity editor.

New hotel-access records default to unverified/unpublished, without an invented positioning fee. Hotel publication and complete quotes require actual verification data. External admission fees remain separate from Nova charges, while channel totals must include mandatory costs. [Google price policy](https://support.google.com/google-ads/answer/11387663)

## Validation

- 51 Django tests passed across the project.
- Django system checks passed; no ungenerated model migrations remain.
- Static collection completed using the existing manifest pipeline.
- Smoke checks covered 14 normal pages: all returned HTTP 200, one H1 and valid JSON-LD; canonical URLs excluded queries. The two new public draft URLs returned the expected 404.
- No numeric legacy pricing remained in active guide/FAQ copy scanned by the smoke verifier.
- Actual browser checks verified a three-adult private estimate stays at the boat amount, and option/date/party carry into the enquiry form.
- An isolated six-image test database verified next/previous, keyboard and thumbnail navigation, responsive layout and native horizontal scrolling with synchronized counters. Artificial test images were never added to Nova's normal catalogue.
- Gallery logic tests cover wrapping, swipe synchronization, reduced motion and event context.

Live analytics delivery, Google acceptance, production performance/Core Web Vitals and real-device checks with the final photo collections remain unverified. No field-performance pass or search-ranking improvement is claimed.

## Models and migrations

Extended `Tour`, `ExperienceRate`, `BookingLead`, `SiteSettings`, `ExternalFee`, `HotelAccess`, `Captain`, `ReviewSnapshot`, `Testimonial`, `GuideArticle` and `QuestionAnswer`. Added `TourOption`, `ActivityImage`, `ActivityDetail`, `ItineraryStep`, `ActivityFAQ` and `ServiceIntent`.

Thirteen migrations were added: tours 0003–0005, bookings 0008–0009, core 0003–0005, content 0003–0005 and partners 0003–0004. A pre-change database backup and catalogue snapshot are retained in the ignored `outputs/activity-rebuild/` directory. Data migrations preserve historical content internally and are intended to move forward; use a verified backup for full rollback.

## Owner workflow and release steps

1. Review `NOVA_ACTIVITY_FACT_MATRIX.md` and confirm durations, guest limits, modes, prices, routes and operating windows. Manage live duration/capacity on booking options; match rate bounds/durations before using a price.
2. Complete operations ownership, actual verification dates/evidence, meeting details and the applicable cancellation/weather/boarding policies in admin.
3. Upload genuine relevant photos, confirm rights/consent, choose one primary, and complete the gallery. Verify imagery and fees against current sources. Missing facts remain drafts or quote requests.
4. Verify hotel access/permission/positioning records and evidence for any public crew credentials, reviews or testimonials.
5. Configure the GA4 measurement ID only after checking the stream settings; mark setup verified, test opt-in/events and designate enquiry submission appropriately. Confirmed bookings/revenue are recorded from operational outcomes.
6. Back up the production database and media, release the reviewed branch through the hosting workflow, run migrations, optimize gallery images and collect static assets, then reload the app and repeat route/quote checks. The normal local app can be started with `python manage.py runserver` from the existing virtual environment.
7. Regenerate the internal Google export and submit only ready products through the actual profile/provider. Complete partner verification before treating a product as accepted.

Payments/deposits and a Things to do connectivity integration remain subsequent phases after catalogue/fulfilment verification. Evaluate Kenyan coverage, payment/payout currencies, inventory and price parity, refunds, data ownership, export portability and costs before selecting a provider. No paid service or connectivity contract was purchased.

## Deliverables

- `NOVA_ACTIVITY_CURRENT_STATE.md`: before/after names, retained URLs, duration sources, image counts and state.
- `NOVA_ACTIVITY_PRICE_AUDIT.md`: canonical rates, historical contradictions and runtime literal scan.
- `NOVA_ACTIVITY_FACT_MATRIX.md`: proposed versus stored operational values needing confirmation.
- `NOVA_ACTIVITY_GBP_EXPORT.md`: names, clean/tracking URLs, primary image candidates and readiness issues.
- `NOVA_ACTIVITY_SERVICE_EXPORT.md`: all thirty intent mappings and their verification state.
- `NOVA_ACTIVITY_REDIRECT_MAP.md`: URL preservation status.
- `NOVA_ACTIVITY_CHANNEL_CANDIDATES.json`: internal future-adapter candidates, not an approved Google feed.
- `scripts/verify_activity_rebuild.py`, `scripts/test_activity_gallery.cjs`, and `scripts/run_activity_ui_fixture.py`: reproducible smoke/component/isolated UI checks.

Regenerate reports with `python manage.py activity_reports`. Use `--optimize-images` to process available gallery originals without inventing missing files.
