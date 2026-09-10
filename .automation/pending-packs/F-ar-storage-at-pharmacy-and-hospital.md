# SKELETON: تخزين الأدوية في الصيدلية والمستشفى, storage at the pharmacy and the hospital

Language: Arabic
Proposed output file: ar/storage-at-pharmacy-and-hospital.html
Template to copy: ar/product-recall-and-withdrawal.html
Suggested article slug: storage-at-pharmacy-and-hospital

STATUS: SKELETON, NOT VERIFIED, DO NOT PUBLISH. No verbatim source text yet. See
`.automation/pending-packs/README.md`.

## Why this topic

Every storage article in the library is written for the distributor's warehouse:
`ar/premises-and-equipment.html`, `ar/warehouse-temperature-mapping.html`,
`ar/operations-and-stock-control.html`. Nothing is written for the buyer who takes delivery, which
is the pharmacy and hospital audience `.automation/strategy.md` names as the enquiries and sales
support reader. The last link in the chain is usually the weakest and it is the one LNJC's own
customers control.

This is buyer facing and practical. Keep it useful rather than technical.

## Arabic formatting requirements

RTL, `<html lang="ar" dir="rtl">`, Cairo and Tajawal fonts, Arabic comma in prose, Latin words and
numerals wrapped in `<bdi>` tags, roughly 800 to 1100 words. Same furniture as the template.

## IMPORTANT, READ BEFORE WRITING

No Yemen specific regulatory requirement. Do not state what Yemeni pharmacies are required to do,
what inspections they face, or what licence conditions apply. The guidelines cited are
international. Say plainly that local requirements are confirmed with the authority.

Do not state numeric storage conditions unless the verbatim text states them. Ranges such as
2 to 8 degrees may be quoted where the source gives them, but do not assign a range to a product
class from memory, and do not tell a reader how long a product remains usable after an excursion.
Refer that question to the product's own labelling and to the manufacturer.

Do not describe LNJC's delivery process, vehicles, or what LNJC does on arrival. There is no
verified source for any of it.

## VERIFIED COMPANY FACTS

The ONLY company specific claims permitted.

- Licensed importer and distributor of pharmaceuticals, medical supplies, laboratory equipment,
  pharmaceutical raw materials and packaging materials in the Republic of Yemen.
- Exclusive distributor in the Republic of Yemen, under signed agreements and for the products
  named in those agreements, for Shivani Scientific Industries Pvt. Ltd. (India) and Zhanjiang
  Bokang Marine Biological Co., Ltd. (BOKANG BIO, China).
- Based in Sana'a, Shu'ub Directorate, Sa'wan.
- Contact: +967 775 559 781, contact@landcarenj.com, https://landcarenj.com/

## CANDIDATE SOURCES, NOT YET VERIFIED

1. WHO Technical Report Series No. 1025, Annex 7, Good storage and distribution practices for
   medical products. Primary source for this article.
   Candidate: https://www.who.int/publications/m/item/trs-1025-annex-7
   PDF candidate: https://cdn.who.int/media/docs/default-source/medicines/who-technical-report-series-who-expert-committee-on-specifications-for-pharmaceutical-preparations/trs1025-annex7.pdf
   Extract: sections on storage conditions and monitoring, on stock rotation and expiry, on
   segregation of returned, rejected, recalled and expired stock, and on cleanliness and pest
   control. These map almost one to one onto the outline below.

2. WHO Technical Report Series No. 961, Annex 9, Model guidance for the storage and transport of
   time and temperature sensitive pharmaceutical products. URL verified HTTP 200 on 2026-08-14.
   URL: https://www.who.int/docs/default-source/medicines/norms-and-standards/guidelines/distribution/trs961-annex9-modelguidanceforstoragetransport.pdf
   Extract: whatever it gives on refrigerator monitoring, alarms, and what to do when a reading
   goes out of range. Use the receiving end material, not the vehicle material.

3. WHO Technical Report Series No. 961, Annex 9, Supplement 7, Qualification of temperature
   controlled storage areas.
   Candidate: https://cdn.who.int/media/docs/default-source/medicines/norms-and-standards/guidelines/distribution/trs961-annex9-supp7.pdf
   Optional. Likely too technical for this audience, but check whether it has anything simple about
   where to place a thermometer, which is a genuinely useful practical point.

## PROPOSED OUTLINE

Section headings to be written in Arabic. Given here in English for the builder.

- Lede: the cold chain does not end when the delivery is signed for.
- Stats block of three, from verified text only.
- h2: Checking the delivery before you accept it
- h2: The refrigerator, and where the thermometer should actually sit
- h2: What to do when a reading is out of range, and what not to do
- h2: Rotation and expiry on the shelf
- h2: Keeping expired, returned and recalled stock physically apart
- FAQ, four questions
- CTA aside and closing

## RECIPROCAL LINK

Link to `ar/buying-cold-chain-stock.html` and add a link back from it.

## BEFORE FLIPPING TO VERIFIED

- Every claim traces to verbatim text here.
- No numeric range or shelf life that the source does not state.
- No Yemen specific requirement, no description of LNJC's delivery process.
- Arabic formatting rules above respected, `<bdi>` around Latin text and numerals.
- Renumber, move to `.automation/sources/`, change `Proposed output file:` to `Output file:`.
