# Nova activity price audit

Generated 2026-10-17.

All customer quote paths use ExperienceRate linked to TourOption. Legacy TourPriceTier rows are retained for history but are not a public price fallback. Missing, ambiguous, expired or unsupported rates request a quote.

| Activity / option | Currency | Unit amount / unit | Minimum transaction | Duration / guests | Effective dates | Verification |
|---|---|---|---|---|---|---|
| 1-Hour Boat Ride on Lake Naivasha / 60-minute shared seats | USD | 20.00 per person | 20.00 | 60 min / 1–7 | 2026-09-27 to open | Pending |
| 1-Hour Boat Ride on Lake Naivasha / 60-minute private boat | USD | 45.00 per boat | 45.00 | 60 min / 1–7 | 2026-09-27 to open | Pending |
| 1-Hour Boat Ride on Lake Naivasha / 60-minute shared seats | KES | 1500.00 per person | 1500.00 | 60 min / 1–7 | 2026-09-27 to open | Pending |
| 1-Hour Boat Ride on Lake Naivasha / 60-minute private boat | KES | 4500.00 per boat | 4500.00 | 60 min / 1–7 | 2026-09-27 to open | Pending |
| Lake Naivasha Hippo & Bird Safari / 120-minute private boat | USD | 75.00 per boat | 75.00 | 120 min / 1–7 | 2026-09-27 to open | Pending |
| Lake Naivasha Hippo & Bird Safari / 120-minute private boat | KES | 7500.00 per boat | 7500.00 | 120 min / 1–7 | 2026-09-27 to open | Pending |
| Crescent Island Boat Ride & Walking Safari / 150-minute private boat | USD | 65.00 per boat | 65.00 | 150 min / 1–7 | 2026-09-27 to open | Pending |
| Crescent Island Boat Ride & Walking Safari / 150-minute private boat | KES | 6500.00 per boat | 6500.00 | 150 min / 1–7 | 2026-09-27 to open | Pending |
| Lake Naivasha Sunset Boat Cruise / 90-minute private boat | USD | 70.00 per boat | 70.00 | 90 min / 1–7 | 2026-09-27 to open | Pending |
| Lake Naivasha Sunset Boat Cruise / 90-minute private boat | KES | 7000.00 per boat | 7000.00 | 90 min / 1–7 | 2026-09-27 to open | Pending |
| Private Lake Naivasha Boat Ride / 360-minute private boat | USD | 200.00 per boat | 200.00 | 360 min / 1–7 | 2026-09-27 to open | Pending |
| Private Lake Naivasha Boat Ride / 60-minute private boat | KES | 4500.00 per boat | 4500.00 | 60 min / 1–7 | 2026-09-27 to open | Pending |
| Private Lake Naivasha Boat Ride / 360-minute private boat | KES | 20000.00 per boat | 20000.00 | 360 min / 1–7 | 2026-09-27 to open | Pending |
| Family Boat Ride on Lake Naivasha / 120-minute private boat | USD | 100.00 per boat | 100.00 | 120 min / 1–7 | 2026-09-27 to open | Pending |
| Family Boat Ride on Lake Naivasha / 120-minute private boat | KES | 10000.00 per boat | 10000.00 | 120 min / 1–7 | 2026-09-27 to open | Pending |
| Lake Naivasha Bird Watching & Photography Boat Tour / 180-minute private boat | USD | 120.00 per boat | 120.00 | 180 min / 1–4 | 2026-09-27 to open | Pending |
| Lake Naivasha Bird Watching & Photography Boat Tour / 180-minute private boat | KES | 12000.00 per boat | 12000.00 | 180 min / 1–4 | 2026-09-27 to open | Pending |
| Private Group & Corporate Boat Tour on Lake Naivasha / 90-minute group experience | USD | 15.00 per person | 150.00 | 90 min / 10–50 | 2026-09-27 to open | Pending |
| Private Group & Corporate Boat Tour on Lake Naivasha / 90-minute group experience | KES | 1200.00 per person | 12000.00 | 90 min / 10–50 | 2026-09-27 to open | Pending |

## Historical contradictory sources
The pre-change snapshot contains the following legacy tiers. They no longer drive current quotes.
| Tour ID | Tier | Currency / amount | Unit |
|---|---|---|---|
| 1 | 1-Hour Private Boat Charter (Up to 7 Guests) | KES 4500 | PER_BOAT |
| 1 | 1-Hour Private Boat Charter - USD (Up to 7 Guests) | USD 45 | PER_BOAT |
| 1 | Shared Boat Seat (Per Person) | KES 1500 | PER_PERSON |
| 1 | Shared Boat Seat - USD (Per Person) | USD 20 | PER_PERSON |
| 3 | Private Boat Transfer & Return Standby (Up to 7 Gu | KES 6500 | PER_BOAT |
| 3 | Private Boat Transfer & Return Standby - USD (Up t | USD 65 | PER_BOAT |
| 4 | 1.5-Hour Private Sunset Cruise (Up to 7 Guests) | KES 7000 | PER_BOAT |
| 4 | 1.5-Hour Private Sunset Cruise - USD (Up to 7 Gues | USD 70 | PER_BOAT |
| 2 | 2-Hour Hippo & Bird Watching Safari (Up to 7 Guest | KES 7500 | PER_BOAT |
| 2 | 2-Hour Hippo & Bird Watching Safari - USD (Up to 7 | USD 75 | PER_BOAT |
| 5 | Full-Day Custom Lake Charter (Up to 6 Hours, Up to | KES 20000 | PER_BOAT |
| 5 | Full-Day Custom Lake Charter - USD (Up to 6 Hours) | USD 200 | PER_BOAT |
| 5 | Hourly Private Charter (Per Hour, Up to 7 Guests) | KES 4500 | PER_BOAT |
| 6 | Family Lake Explorer (2 Hours, Up to 7 Guests) | KES 10000 | PER_BOAT |
| 6 | Family Lake Explorer - USD (2 Hours, Up to 7 Guest | USD 100 | PER_BOAT |
| 7 | Birding & Photography Charter (3 Hours, Up to 4 Cr | KES 12000 | PER_BOAT |
| 7 | Birding & Photography Charter - USD (3 Hours, Up t | USD 120 | PER_BOAT |
| 8 | Group Regatta Experience (Per Person, Min 10 Guest | KES 1200 | PER_PERSON |
| 8 | Group Regatta Experience - USD (Per Person, Min 10 | USD 15 | PER_PERSON |

## Runtime monetary literals scan
Tests, migrations and preserved historical copy are excluded. Other products such as stays retain their own configured rates.
No numeric currency literals found in the scanned runtime files.
