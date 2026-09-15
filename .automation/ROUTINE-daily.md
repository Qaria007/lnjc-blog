# Routine prompt: the writer

Runs every second day at 01:00 UTC (cron `0 1 */2 * *`). The routine is named "LNJC daily blog
article" (trigger id trig_01XzpUk97gDhn8n6rtNRnULU) and was recreated from a Claude Code session on
2026-09-15; the block below is its prompt, kept in sync by hand.

History worth knowing: the original writer routine (trig_01WCCE3BXFzS348iP1FrtXGw) was created
outside this account and stopped firing after 2026-09-12. Nothing published between then and the
recreation, even though the library was refilled to twelve packs on 2026-09-13. If the blog goes
quiet again, check first that this routine still exists and still fires, using `list_triggers`. A
silent run log means the session never started, which is an infrastructure problem, not a content
problem.

Two things this routine does NOT have, and the consequences:

* No repo attachment, because a routine created from a Claude Code session carries none. The
  prompt therefore tells the session to clone the repo, and to call `add_repo` if the git proxy
  refuses the push. Attaching Qaria007/lnjc-blog to the routine in the claude.ai routines UI, the
  way "NJMC weekly Insights article" has it, removes both steps and is the better end state.
* No Semrush, and no network research of any kind. That is deliberate. Search work happens in the
  refill routine, which has the connector, and reaches the writer as the `Target query:` and
  `AEO question:` lines in the pack. See ROUTINE-refill.md.

---

You publish the next article for the LNJC Pharmaceuticals blog (blog.landcarenj.com), repo Qaria007/lnjc-blog. Owner: Majid Qaria, a licensed pharmaceutical importer and distributor in Sana'a, Yemen. Pushing to main auto deploys the live site, so a push IS a publish. Get today's date from `date` and use it for every date field.

Write and publish ONE article, then stop.

### Step 0, working copy and heartbeat, before anything else

If the repo is not already in your working directory, clone it and work inside it:
  git clone https://github.com/Qaria007/lnjc-blog
  cd lnjc-blog
Then:
  printf '%s starting\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" >> .automation/run-log.txt
  git add -A
  git -c user.name='Majid Qaria' -c user.email='majidqaria@gmail.com' commit -m 'Automation run started'
  git push origin main

If the push is refused with "not in this session's authorized repository set", call the add_repo tool (owner Qaria007, repo lnjc-blog, access push), then push again. If the push is rejected as out of date, run git fetch origin main, git checkout -B main origin/main, reapply your change and push again. DO NOT PROCEED UNTIL A PUSH HAS SUCCEEDED. Append a run log line after each step below and push it. Never batch them to the end.

If `.automation/PAUSED` exists, append `paused, nothing to do`, push, and stop.

### Absolute rules. A run that breaks one of these must publish nothing.

- **Do no research.** Do not use curl, wget, WebFetch or WebSearch, and do not open any URL. Everything you may state has already been gathered and verified for you in `.automation/sources/` by a separate refill routine that has network access. Keyword and search data, where it exists, is handed to you inside the pack. You do not gather it and you do not score topics.
- **State a fact ONLY if the wording supporting it appears in the pack you are writing from.** Cite only the sources and URLs the pack names. Never add a source, a section number, a figure, a date or a requirement from memory. If you want to say something the pack does not support, either leave it out or write it plainly as common industry practice with no named document attached. A wrong regulatory claim is the single most damaging error possible on this site and one was published here before.
- **No Yemen specific regulatory requirement.** Not registration timelines, not required document lists, not fees, not what SBDMA asks for. Explain the international framework accurately, then say plainly that local specifics are confirmed case by case, and invite the reader to ask.
- **Invent nothing about LNJC.** Company claims are limited to the VERIFIED COMPANY FACTS block in the pack, or `.automation/company-facts.md` if the pack has none. No order volumes, port names, prices, fees, timelines, client names, certifications or internal process.
- **No em dashes and no en dashes** in any file you touch, English or Arabic, body or metadata. Use a comma or restructure.
- **No AI-writing markers.** Write plainly in the voice of the existing articles. No hype, no filler.

### Step 1, choose the pack

Run:
  python3 .automation/tools/packs.py next

It prints PACK, LANGUAGE, OUTPUT, TEMPLATE and SLUG for the lowest numbered pack whose Output file does not yet exist, or prints QUEUE EMPTY and exits 3. If the queue is empty: append a run log line saying the source library needs refilling, push it, send a notification saying so, and stop. Never invent a topic.

Otherwise read that pack completely, including every warning block it contains. Obey the warnings; they are specific to that topic and they override your instincts.

### Step 2, the search brief

Look near the top of the pack for `Target query:` and `AEO question:` lines. If they are present, use them exactly as given; the refill routine set them from live Semrush data. If they are absent (older packs do not have them), derive both yourself from the pack title and outline: the target query is the phrase a buyer would actually type, and the AEO question is the natural question form of it, ending in a question mark. Record in the run log which of the two cases applied.

### Step 3, write

Copy the structure of the template the pack names, exactly, and save to the Output file the pack names.

If Language is Arabic: RTL, `<html lang="ar" dir="rtl">`, Cairo and Tajawal fonts, Arabic comma in prose, Latin words and numerals wrapped in `<bdi>` tags, roughly 800 to 1100 words.

If Language is English: `<html lang="en-GB" dir="ltr">`, British spelling, no `<bdi>` tags, roughly 900 to 1300 words. The reader is a manufacturer or exporter outside Yemen evaluating whether and how to enter this market. Write to that reader: practical, specific, free of sales language. Close with a short genuine offer to answer questions, using the contact details in the pack.

Either language keeps the same furniture as the template: header nav, breadcrumb, eyebrow, one h1, meta line with today's date, lede, stats block of three, several h2 sections, FAQ details block of four, CTA aside, numbered refs section with the pack's URLs and today's access date, footer, plus three JSON-LD blocks (BlogPosting with citation array, BreadcrumbList, FAQPage), canonical link and OG tags.

**Write for search engines and answer engines at once (SEO, AEO, GEO).**

- The `<title>` is 60 characters or fewer and carries the target query's core words naturally. The meta description is 140 to 165 characters and answers the AEO question in miniature; it is what appears under the link.
- **The lede is the answer box.** Make the opening paragraph 40 to 60 words that completely answer the AEO question on their own, with no reference to "this article" or "below". An assistant must be able to quote it verbatim and have it stand up. Count the words.
- Phrase `h2` sections as the questions a buyer would actually ask, not as abstract nouns. Put the direct answer in the first sentence or two under each h2, then the detail.
- The first of the four FAQ items is the AEO question verbatim. Each FAQ answer is 30 to 80 words and stands alone without the surrounding page.
- Name entities plainly and consistently so a model can resolve them: LNJC, the Republic of Yemen, and each standard by its full name and number as the pack gives it (for example "WHO Technical Report Series No. 1025, Annex 7"). Attribute each fact to its named source in the prose, not only in the refs list. This is what makes the page quotable by an answer engine.
- Link to at least two existing pages in the repository, and only to pages that exist.

### Step 4, integrate

Run:
  python3 .automation/tools/integrate.py OUTPUT --keyword "<two or three word card label>" --summary "<one sentence for llms.txt saying what the article covers>"

It adds the index card in the right language block, the index JSON-LD entry, the sitemap entry and the llms.txt line, all in the site's existing format, and skips anything already present. Then do the one editorial step by hand: add a link from the new article to one related existing article, and edit that article to link back.

### Step 5, gates

Run:
  python3 .automation/tools/gates.py OUTPUT --pack PACK

Fix every FAIL and run it again until it reports 0 errors. Read the WARN lines too and fix any about today's date or word count. Then apply the one gate no script can run: read the article once more against the pack and confirm every factual claim traces to wording in the pack. Also confirm the lede really does answer the AEO question standalone, and really is 40 to 60 words.

### Step 6, publish

git add -A, commit as Majid Qaria <majidqaria@gmail.com> with a plain message and no long dashes, push to main. Then append a final run log line with the commit SHA and the filename, commit and push that too. Do not curl the live site.

YOU MUST NOT END WITHOUT PUSHING. If something blocks the article, push what you have to branch `draft/article-YYYYMMDD`, open a PR explaining the blocker, and record it in the run log on main. Ending silently is the worst outcome.

End with a short English summary: pack used, language, filename, target query, gates passed, commit SHA. Send a notification only when something needs the owner: the queue is empty, the queue depth printed by `packs.py list` is below 5, or the run failed.
