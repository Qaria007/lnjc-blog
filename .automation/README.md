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
      run-log.txt            one line per run, appended by the agent as it works
      sources/
        01-transport-route-qualification.md
        02-returned-medicines.md
        ...

Each pack names its sources, gives the URL to cite, records the date the URL was verified, and
contains the exact wording the article may rely on. Each pack also suggests an article slug.

## Daily selection rule

The agent takes the lowest numbered pack whose suggested slug has no matching `ar/<slug>.html`
yet, writes that article, and publishes it. When every pack is used, the agent has nothing to
write and says so instead of inventing something.

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
