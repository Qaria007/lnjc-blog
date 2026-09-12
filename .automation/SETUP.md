# Setting this article system up for another site

The system is two routines and a small toolkit. Nothing in `.automation/tools/` knows about
LNJC; everything site specific lives in `.automation/site.json`, `.automation/company-facts.md`,
`.automation/strategy.md` and the two routine prompts.

## The model

    refill routine (twice a week, environment WITH internet)
        opens primary documents, saves a text copy, builds numbered packs of verbatim excerpts,
        proves every excerpt is in the document, pushes packs to .automation/sources/
                                  |
                                  v
    writer routine (daily or weekly, environment WITHOUT internet)
        takes the lowest numbered unused pack, writes the article from that pack only,
        wires it into the site, runs the gates, pushes to main

The writer is deliberately locked out of the internet. A writer that can browse will, sooner or
later, quote a consultancy page as if it were the regulation. The refiller is the only place
where a URL is opened, and it may only copy, never summarise.

## One time, per account

1. In claude.ai/code, open Environments and create one with the network policy set to full
   internet access. Name it something like "Research". The existing "Default" environment only
   reaches GitHub and package registries, which is right for the writer and useless for the
   refiller. (Docs: https://code.claude.com/docs/en/claude-code-on-the-web)
2. Keep the Default environment for every writer routine.

## Per site

1. Copy `.automation/tools/` and `.automation/SETUP.md` into the site repo.
2. Write `.automation/site.json`. The fields:
   - `base_url`, `site_name`, `author`
   - `index_file`, `sitemap_file`, `llms_file`: the files integrate.py edits
   - `languages`: one entry per language with the html `code` and `dir`, the `output_prefix`
     directory, the `template` article to copy, the `index_heading` text that opens that
     language's card block in the index, the `llms_heading` line in llms.txt, the target
     `words` range, and whether `<bdi>` is required
   - `forbidden_chars` as code points, `faq_count`, `stats_count`, `required_jsonld_types`
   - `min_queue` (the writer warns below this) and `refill_target` (the refiller stops at this)
3. Write `.automation/company-facts.md`: the only company claims any article may make.
4. Write `.automation/strategy.md`: audiences, language mix, and a numbered topic queue with a
   candidate primary document for each topic. The refiller works this list in order.
5. Write one template article per language by hand, with the furniture the gates expect: one
   title, one h1, breadcrumb, eyebrow, lede, stats block, FAQ details, CTA aside, references
   section, header, footer, three JSON-LD blocks (BlogPosting with a citation array,
   BreadcrumbList, FAQPage), canonical and OG tags. Run `gates.py` on it until it is clean; the
   template is the contract.
6. Add `.automation/sources/cache/` to `.gitignore`.
7. Create the two routines from `ROUTINE-refill.md` (Research environment) and
   `ROUTINE-daily.md` (Default environment), with the repo, owner and site name changed.
8. Run the refill routine once by hand and check the first packs yourself before letting the
   writer loose.

## The tools

    packs.py next                      lowest numbered pack whose Output file does not exist
    packs.py list                      queue depth, REFILL NEEDED below min_queue
    packs.py next-number               next free number
    packs.py validate [--require-cache] PACK...
                                       structure, then every VERBATIM TEXT passage is proved to be
                                       a substring of the fetched document (whitespace, smart
                                       quotes and PDF hyphenation normalised)
    fetch_source.py get URL --name N   fetch, record HTTP status and date, save extracted text
    fetch_source.py find URL "phrase"  locate the paragraphs to quote
    integrate.py ARTICLE --keyword K --summary S
                                       index card, index JSON-LD, sitemap, llms.txt; idempotent
    gates.py ARTICLE --pack PACK       every publication gate; exit 1 on any failure

Python 3 standard library only, except `pypdf` for PDFs on the refill side.

## Pack format

    # Verified source pack: <title>

    Language: English
    Output file: en/<slug>.html
    Template to copy: en/<template>.html
    Suggested article slug: <slug>

    STATUS: VERIFIED. <date and the rule that nothing outside this file may be cited>

    <warning block for the audience, if any>

    ## VERIFIED COMPANY FACTS
    <copied from company-facts.md>

    ## SOURCE: <Issuing body, document title, series and year>
    URL to cite: https://...
    Verified: YYYY-MM-DD (HTTP 200)

    VERBATIM TEXT:

    <paragraphs copied exactly; "..." between separate passages>

## What to watch

- `run-log.txt` gets one line per step. No line means the routine never started; a line and no
  article means it stopped and the line says where.
- The writer notifies when the queue is empty or below `min_queue`. The refiller notifies when
  it cannot reach the internet, which means it is in the wrong environment.
- Read the first few packs and articles of a new site yourself. The tools prove that a quote is
  in the document; they cannot tell whether the document is the right one to be quoting.
