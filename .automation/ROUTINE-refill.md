# Routine prompt: twice weekly refill

Runs Wednesday and Sunday at 02:00 UTC (cron 0 2 * * 0,3) in an environment WITH full internet
access. It is the only part of the system that opens URLs. The routine is named "LNJC source
refill" and was created from a Claude Code session on 2026-09-12; the block below is its prompt.
Twice a week with up to six packs per run keeps ahead of a daily writer (capacity 12 a week
against 7 consumed).

If the environment it runs in has no internet access, every run stops at STEP 1 and notifies
the owner; nothing is invented. Fix: in claude.ai/code, Environments, set the environment's
network access to full internet, or create a "Research" environment with full access and
recreate the routine there.

---

You refill the verified source library for the LNJC Pharmaceuticals blog (blog.landcarenj.com). The repo Qaria007/lnjc-blog should be cloned in your working directory; if it is not, clone https://github.com/Qaria007/lnjc-blog and work inside it. Owner: Majid Qaria. You are the only part of this system that is allowed to open URLs. A separate daily writer runs in a container with no internet and writes only from the packs in .automation/sources/. If a pack you build contains a claim the primary document does not make, that claim gets published under a pharmaceutical company's name. Read .automation/README.md, .automation/strategy.md and .automation/pending-packs/README.md before doing anything.

STEP 0, HEARTBEAT, FIRST:
  printf '%s refill starting\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" >> .automation/run-log.txt
  git add -A
  git -c user.name='Majid Qaria' -c user.email='majidqaria@gmail.com' commit -m 'Refill run started'
  git push origin main
If the push is rejected, fetch origin main, reattach to main, merge and push again. Append a run log line after each pack and push it. Never batch these to the end.

STEP 1, NETWORK CHECK. Run: python3 .automation/tools/fetch_source.py get https://www.who.int/ --name probe
If it reports a proxy 403, a CONNECT failure, or any connection error, this routine is running in the wrong environment. Append a run log line saying 'refill blocked: environment has no internet access, this routine must run in an environment with full internet access', push, send a notification saying exactly that, and stop. NEVER build a pack from memory, from search snippets, or from a page you could not open.

STEP 2, ASSESS. Run: python3 .automation/tools/packs.py list
If the queue depth is at or above refill_target in .automation/site.json, log 'queue full, nothing to do' and stop. Otherwise build packs until the queue reaches refill_target or you have built six packs this run, whichever comes first.

STEP 3, PICK THE TOPIC. Take the next unbuilt item of the 'Queue, refilled' list in .automation/strategy.md, in order. Items with a skeleton in .automation/pending-packs/ come with their outline, warnings and candidate URLs; use them. Keep the ordering the strategy asks for, roughly two English packs to one Arabic, when you number them. Never invent a topic that is not in the strategy queue.

STEP 4, FETCH. Once per run: pip install pypdf. Then for every candidate URL:
  python3 .automation/tools/fetch_source.py get URL --name "Issuing body, document title, series and year"
Read the first pages of the saved text and confirm it is the issuing body's own copy and the current revision (document number, revision date, title). If the status is not 200, if it redirects to another host, if it is a mirror, a consultancy page, a search result or a superseded revision, do not cite it: find the official location on the issuing body's own site, fetch that, and cite that. Drop any source you cannot verify. A pack with fewer honest sources beats a pack with a doubtful one.

STEP 5, EXTRACT. Use python3 .automation/tools/fetch_source.py find URL "keyword" to locate the sections the outline needs, then copy the passages from the saved text file exactly as they are. No paraphrase, no tidying, no fixing typos, no reordering. Put "..." on its own between separately quoted passages. If a section does not say what the skeleton assumed, change the outline, never the quote.

STEP 6, ASSEMBLE. Copy the layout of an existing pack in .automation/sources/ exactly. In order: the title line, Language, Output file (the skeleton's proposed one; check it does not exist yet), Template to copy, Suggested article slug, a STATUS: VERIFIED line with today's date, the IMPORTANT warning block (copy it from an existing pack of the same language and audience), the VERIFIED COMPANY FACTS block copied verbatim from .automation/company-facts.md, then one '## SOURCE:' block per source with 'URL to cite:', 'Verified: YYYY-MM-DD (HTTP 200)' and 'VERBATIM TEXT:'. Number it with python3 .automation/tools/packs.py next-number and save it as NN-lang-slug.md in .automation/sources/.

STEP 7, VALIDATE. Run: python3 .automation/tools/packs.py validate --require-cache PACK
Fix until it reports 0 errors. Every passage must be found in the fetched document. If one is not, you did not copy it exactly: recopy it from the saved text. Never edit a quote to make it match, and never delete the fetched copy to skip the check.

STEP 8, RULES THAT ALWAYS APPLY. No Yemen specific regulatory requirement anywhere in a pack; the Yemeni authority's own site has not been reachable and consultancy pages contradict each other. No company claim beyond .automation/company-facts.md. No em dashes or en dashes in prose you write yourself (verbatim quotes keep whatever the document has). Delete the used skeleton from .automation/pending-packs/ and mark the item as built in .automation/strategy.md. Do not commit .automation/sources/cache/, it is gitignored.

STEP 9, COMMIT after every pack: git add -A, commit as Majid Qaria <majidqaria@gmail.com> with a plain message, push to main. When done, append a run log line listing the packs built and the queue depth, push it, and send a notification with the same summary. If you built nothing, say why in the log and in the notification.

End with a short English summary: packs built, sources used with their HTTP status, queue depth, commit SHAs.
