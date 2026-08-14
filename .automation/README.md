# How the daily article automation works

A scheduled Claude agent runs in Anthropic's cloud every day at 01:00 UTC and publishes one new
Arabic article to this repo. Pushing to `main` deploys the live site.

## Why there is a source library

The cloud container that runs the daily job **has no outbound internet**. `curl`, `wget` and even
the `WebFetch` tool fail there with an egress block. Only `WebSearch` works, and it returns short
snippets rather than the text of a document.

That matters because this is a pharmaceutical blog. On 2026-08-11 a draft written from search
snippets stated that the EU Good Distribution Practice guidelines require a dummy recall when no
real recall has happened in twelve months. The guidelines never say that; the words "dummy" and
"mock" do not appear in them at all. The claim comes from consultancy sites repeating each other.
It was caught before publication and corrected, but it is exactly the kind of error that damages a
regulated business.

So the cloud agent is no longer allowed to research. Instead it writes from `sources/`, a library of
**verbatim excerpts copied from the primary documents themselves and verified from a machine with
real network access**. The agent may cite only what is in a pack. Nothing else.

## Layout

    .automation/
      README.md              this file
      strategy.md            what to publish and why, from the market research
      run-log.txt            one line per run, appended by the agent as it works
      sources/
        04-en-import-controls.md
        06-ar-shipment-documents.md
        ...

Each pack declares, near the top:

    Language: English | Arabic
    Output file: en/<slug>.html or ar/<slug>.html
    Template to copy: an existing article to match structurally
    Suggested article slug: <slug>

then names its sources, gives the URL to cite, records the date each URL was verified, and
contains the exact wording the article may rely on. Packs also carry a VERIFIED COMPANY FACTS
block, which is the only place company specific claims may come from, and some carry an audience
note or a warning the writer must follow.

## Daily selection rule

The agent takes the lowest numbered pack whose declared Output file does not yet exist, writes
that article, and publishes it. When every pack is used, the agent has nothing to write and says
so instead of inventing something.

## Why the numbering is interleaved

Per `strategy.md`, English articles aimed at manufacturers looking for a Yemen distributor are
the highest value content and were badly under-represented. The queue is ordered to correct that,
roughly one Arabic piece per two English ones, so the ordering is a deliberate editorial decision
rather than the order the packs happened to be built in. Keep that shape when refilling.

## The Yemen regulatory warning

The Yemeni authority's own website (sbd-ye.org) was unreachable when checked on 2026-08-14, and
almost everything published online about its requirements comes from consultancies selling
registration services who contradict each other. No pack states a Yemen specific regulatory
requirement, and articles must not either. Explain the international framework accurately, then
say plainly that local specifics are confirmed case by case, and invite the reader to ask.

## Refilling the library

This is the one recurring human step. When packs run low, a Claude session on a machine with
network access reads the primary documents, extracts verbatim excerpts, and adds new numbered
packs. Good sources: ICH guidelines, WHO Technical Report Series annexes, USP General Chapters,
FDA and eCFR, EMA and EU guidelines, and national regulators.

## Reading a failed run

Check `run-log.txt` first:

* no new line at all, the session never really started, an infrastructure problem
* a line but no article, it started and died partway, the line says where
* a line plus a new `ar/*.html` file, it worked
