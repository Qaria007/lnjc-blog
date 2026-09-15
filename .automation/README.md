# How the article automation works

Two scheduled Claude routines and a small toolkit publish the articles on blog.landcarenj.com.
Pushing to `main` deploys the live site.

    refill routine, Wednesdays and Sundays, in an environment WITH internet
        opens the primary documents, saves a text copy, builds numbered packs of verbatim
        excerpts in sources/, proves every excerpt is in the document, pushes
                                  |
                                  v
    writer routine, every second day, no research of any kind
        takes the lowest numbered unused pack, writes one article from that pack only,
        using the search brief the refill routine put in that pack,
        wires it into the site, runs the gates, pushes to main

The prompts are in `ROUTINE-refill.md` and `ROUTINE-daily.md`. `SETUP.md` explains how to
stand the same system up for another site.

## Why the writer has no internet, and why that is the point

The Default cloud environment only reaches GitHub and package registries. `curl`, `wget` and
`WebFetch` all fail there with an egress block from the proxy, for every source host.

That is the right place for the writer. This is a pharmaceutical blog. On 2026-08-11 a draft
written from search snippets stated that the EU Good Distribution Practice guidelines require a
dummy recall when no real recall has happened in twelve months. The guidelines never say that;
the words "dummy" and "mock" do not appear in them at all. The claim comes from consultancy
sites repeating each other. It was caught before publication, but it is exactly the kind of
error that damages a regulated business.

So the writer is not allowed to research. It writes from `sources/`, a library of verbatim
excerpts copied from the primary documents themselves. It may cite only what is in a pack.

## Why there is a refill routine

The library ran dry on 2026-08-27 and the writer published nothing for sixteen days, because
refilling was a manual step that depended on somebody opening a session on a machine with
internet access. The refill routine removes that dependency: it runs twice a week in a cloud
environment whose network policy allows all hosts, fetches each document with
`tools/fetch_source.py`, and may only move a pack into `sources/` once
`tools/packs.py validate --require-cache` has proved that every quoted passage is a substring of
the fetched text. It cannot paraphrase its way past that check.

## Layout

    .automation/
      README.md              this file
      SETUP.md               how to reproduce the system for another site
      ROUTINE-daily.md       prompt of the writer routine
      ROUTINE-refill.md      prompt of the refill routine
      site.json              everything site specific the tools need
      company-facts.md       the only company claims an article may make
      strategy.md            what to publish and why, and the topic queue the refiller works
      run-log.txt            one line per step, appended by both routines as they work
      tools/                 packs.py, fetch_source.py, integrate.py, gates.py (stdlib Python)
      sources/               verified packs, NN-lang-slug.md
      sources/cache/         fetched document text, gitignored, refill side only
      pending-packs/         skeletons: outline, warnings and candidate URLs, not yet fetched

Each pack declares, near the top:

    Language: English | Arabic
    Output file: en/<slug>.html or ar/<slug>.html
    Template to copy: an existing article to match structurally
    Suggested article slug: <slug>
    Target query: the phrase a buyer would type, set by the refill routine from Semrush
    AEO question: that query as a question, becomes the lede answer and the first FAQ item
    Search notes: volume or intent, and secondary phrases worth using as h2 headings

The last three are newer than packs 01 to 29, so older packs do not carry them. The writer
derives its own when they are missing and records in the run log that it did.

then a `STATUS: VERIFIED` line, the audience warning, the VERIFIED COMPANY FACTS block, and one
`## SOURCE:` block per document with `URL to cite:`, `Verified: YYYY-MM-DD (HTTP 200)` and the
`VERBATIM TEXT:`.

## Daily selection rule

`tools/packs.py next` returns the lowest numbered pack whose declared Output file does not yet
exist. When every pack is used the writer says so, notifies the owner, and stops. It never
invents a topic.

## Why the numbering is interleaved

Per `strategy.md`, English articles aimed at manufacturers looking for a Yemen distributor are
the highest value content and were badly under-represented. The queue is ordered roughly one
Arabic piece per two English ones. Keep that shape when refilling.

## Who does the search work, and why it is not the writer

Search research lives in the refill routine, which has the network and the Semrush connector. It
writes the target query and the AEO question into each pack. The writer reads those lines and
never researches anything itself. njmc-site-public splits the same job the same way, and its
writer prompt states the rule plainly: it does not choose or score topics, because the queue order
comes from a separate review that has network access.

The reason is the same reason the source packs exist at all. Keyword tools are a legitimate input
to wording, emphasis and headings. They are not an input to what the article asserts. Keeping them
in a different routine from the writing makes it structurally hard for a keyword to turn into a
claim. Semrush decides how a thing is said; the primary documents decide whether it is true.

## The Yemen regulatory warning

The Yemeni authority's own website (sbd-ye.org) was unreachable when checked on 2026-08-14, and
almost everything published online about its requirements comes from consultancies selling
registration services who contradict each other. No pack states a Yemen specific regulatory
requirement, and articles must not either. Explain the international framework accurately, then
say plainly that local specifics are confirmed case by case, and invite the reader to ask.

## Reading a failed run

Check `run-log.txt` first:

* no new line at all: the session never really started, an infrastructure problem
* a line but no article: it started and stopped partway, the line says where
* `refill blocked: environment has no internet access`: the refill routine is attached to the
  wrong environment, move it to one with full internet access
* a line plus a new `en/*.html` or `ar/*.html` file: it worked

`tools/packs.py list` shows the queue depth at any time.
