# Refill kit: turning a skeleton into a verified source pack

Written 2026-09-10 from the cloud container, which has no outbound internet. Everything in this
directory is preparation. Nothing here is verified and nothing here may be published.

## Why this directory exists and why it is not `sources/`

The daily job selects work by running `ls .automation/sources/` and taking the lowest numbered
pack whose declared `Output file:` does not yet exist. If these skeletons lived in `sources/`,
tomorrow's run would pick one up and write an article from unverified scaffolding, which is the
exact failure the source library was built to prevent.

So they live here instead, and they deliberately say `Proposed output file:` rather than
`Output file:`. The daily job cannot see them and cannot act on them. It will keep reporting that
the library needs refilling until real packs land in `sources/`. That is correct behaviour, not a
bug.

## What is missing from every file here

The verbatim excerpts. That is the whole job. A pack is only a pack when the person building it
has opened each primary document, copied its own words, and recorded the HTTP status and the date.
Search snippets are not acceptable and never have been: the incident recorded in
`.automation/README.md`, where the blog nearly published a Good Distribution Practice requirement
that does not exist in the guidelines, came from exactly that shortcut.

The candidate URLs below came from a search index, not from opening the pages. Treat every one of
them as a lead to check, not as a citation. If a URL redirects, 404s, or turns out to be a mirror
rather than the issuing body, find the official location and record that instead.

## Procedure

For each skeleton in this directory:

1. Open every candidate URL. Record the real HTTP status and the date you checked.
2. Read the sections the skeleton names. If a section does not say what the skeleton assumed it
   says, change the article outline, never the source.
3. Copy the relevant passages verbatim into a `VERBATIM TEXT:` block under a `## SOURCE:` heading,
   matching the layout of any file in `.automation/sources/`.
4. Drop any candidate source that did not survive step 2, and any outline section left without
   support.
5. Rename the file to the next free number in the queue, change `Proposed output file:` to
   `Output file:`, change the status line to VERIFIED with the date, and move it into
   `.automation/sources/`.
6. Delete the `CANDIDATE SOURCES, NOT YET VERIFIED` heading and the checklist at the bottom. A
   finished pack should read like the ones already in `sources/`.

A skeleton that loses all its sources in step 2 should be deleted rather than padded out. Fewer
honest packs beat more thin ones.

## Numbering and the language ratio

Packs 01 to 17 are used. Start new ones at 18.

As of 2026-09-10 the published split is 7 English to 27 Arabic. `.automation/strategy.md` calls for
roughly one Arabic piece per two English ones, because the English manufacturer facing articles are
the commercially valuable ones and are badly under-represented. This batch is four English to two
Arabic. Interleave them in that ratio when numbering, so a run of consecutive Arabic days cannot
happen again.

## What remains from the strategy queue

Of the ten items in `.automation/strategy.md`, these are already published: 2, 4, 6, 7, 8, 10.
Item 9 is partly covered by `en/ivf-lab-air-quality.html` and `ar/ivf-lab-equipment.html`.

Items 1, 3 and 5 are the Yemen registration topics. Items 1 and 3 carry the accuracy warning in
`strategy.md` and should stay unbuilt until a Yemeni primary source is actually in hand. Item 5,
the distribution agreement, is mostly commercial rather than regulatory and is included in this
batch on that basis.

The queue is nearly spent. Whoever refills the library should add new topics to `strategy.md` at
the same time, or the next exhaustion is only six days away.

## Source documents worth mining

All 17 existing packs draw on only three documents, and they are close to worked out:

- European Commission, Guidelines of 5 November 2013 on Good Distribution Practice
  (2013/C 343/01)
- WHO Technical Report Series No. 961, Annex 9 (2011)
- WHO Technical Report Series No. 1019, Annex 5 (2019)

Fresh material that the skeletons below point at, all candidate URLs, none opened:

- WHO Technical Report Series No. 1025, Annex 7, Good storage and distribution practices for
  medical products. Landing page https://www.who.int/publications/m/item/trs-1025-annex-7 and PDF
  https://cdn.who.int/media/docs/default-source/medicines/who-technical-report-series-who-expert-committee-on-specifications-for-pharmaceutical-preparations/trs1025-annex7.pdf
- WHO Technical Report Series No. 957, Annex 5, WHO good distribution practices for pharmaceutical
  products. https://www.who.int/docs/default-source/medicines/norms-and-standards/guidelines/distribution/trs957-annex5-who-good-distribution-practices-for-pharmaceutical-products.pdf
- WHO Technical Report Series No. 961, Annex 9, Supplement 7, Qualification of temperature
  controlled storage areas. https://cdn.who.int/media/docs/default-source/medicines/norms-and-standards/guidelines/distribution/trs961-annex9-supp7.pdf
- PIC/S Guide to Good Distribution Practice for Medicinal Products, PE 011. Candidate document
  views https://picscheme.org/docview/3450 and https://picscheme.org/docview/2466

Check the PIC/S links carefully. The search index returned several PE 011 and PI 041 documents at
similar paths and at least one was a superseded 2014 revision, so confirm the document number and
the revision date on the page itself before citing anything from it.
