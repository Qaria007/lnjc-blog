#!/usr/bin/env python3
"""Publication gates for one article. Run before every publish and fix everything it reports.

    gates.py ARTICLE.html [--pack PACK.md] [--no-git]

Checks structure (one title, one h1, lang and dir, canonical, OG tags, three JSON-LD blocks, FAQ,
stats, references), sourcing (every cited URL appears in the pack), integration (index card and
JSON-LD entry, sitemap, llms.txt, reciprocal links), forbidden characters in every changed file,
and word count. Exit 1 on any error.
"""
import datetime
import json
import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import ROOT, SITE, Report, language_for_output, rp  # noqa: E402

try:
    from packs import parse_pack
except ImportError:  # pragma: no cover
    parse_pack = None


def strip_tags(s):
    s = re.sub(r"<script.*?</script>", " ", s, flags=re.S)
    s = re.sub(r"<style.*?</style>", " ", s, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", s)


def changed_files():
    try:
        a = subprocess.run(["git", "diff", "--name-only", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True).stdout
        b = subprocess.run(["git", "ls-files", "--others", "--exclude-standard"], cwd=ROOT, capture_output=True, text=True, check=True).stdout
        return sorted(set(a.split() + b.split()))
    except Exception:  # noqa: BLE001
        return []


def jsonld_blocks(html):
    return re.findall(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', html, flags=re.S)


def run(article, pack_path=None, use_git=True):
    r = Report()
    article = article.replace("\\", "/")
    if not os.path.isfile(rp(article)):
        r.error("article not found: " + article)
        return r
    html = open(rp(article), encoding="utf-8").read()
    lang_name, cfg = language_for_output(article)
    if not r.check(cfg, "cannot tell the language of %s from its path prefix" % article):
        return r
    url = SITE["base_url"].rstrip("/") + "/" + article
    today = datetime.date.today().isoformat()

    # 1. document furniture
    m = re.search(r'<html\s+lang="([^"]+)"\s+dir="([^"]+)"', html)
    r.check(m and m.group(1) == cfg["code"] and m.group(2) == cfg["dir"],
            'expected <html lang="%s" dir="%s">' % (cfg["code"], cfg["dir"]))
    r.check(len(re.findall(r"<title[\s>]", html)) == 1, "exactly one <title> required")
    r.check(len(re.findall(r"<h1[\s>]", html)) == 1, "exactly one <h1> required")
    r.check('<link rel="canonical" href="%s">' % url in html, "canonical link must be exactly " + url)
    for tag in ("og:title", "og:description", "og:url", "og:image"):
        r.check('property="%s"' % tag in html, "missing OG tag " + tag)
    r.check('property="og:url" content="%s"' % url in html, "og:url must equal " + url)
    r.check('<meta name="description"' in html, "missing meta description")
    r.check('class="crumb"' in html, "missing breadcrumb nav")
    r.check('class="eyebrow"' in html, "missing eyebrow")
    r.check('class="lede"' in html, "missing lede paragraph")
    r.check('class="cta"' in html, "missing CTA aside")
    r.check('class="site-footer"' in html, "missing footer")
    r.check('class="site-header"' in html, "missing header")
    r.check(len(re.findall(r'<div class="stat">', html)) == SITE["stats_count"],
            "stats block should hold %d .stat entries" % SITE["stats_count"], level="warn")
    r.check(len(re.findall(r"<details>", html)) == SITE["faq_count"],
            "FAQ should hold %d <details> entries" % SITE["faq_count"])
    r.check(re.search(r'<time datetime="%s"' % today, html), "meta line <time> should carry today's date %s" % today, level="warn")

    # 2. JSON-LD
    blocks = jsonld_blocks(html)
    r.check(len(blocks) == 3, "expected 3 JSON-LD blocks, found %d" % len(blocks))
    types, citations = [], []
    for i, b in enumerate(blocks, 1):
        try:
            d = json.loads(b)
        except json.JSONDecodeError as e:
            r.error("JSON-LD block %d does not parse: %s" % (i, e))
            continue
        types.append(d.get("@type"))
        if d.get("@type") == "BlogPosting":
            r.check(d.get("inLanguage") == cfg["code"], "BlogPosting inLanguage should be %s" % cfg["code"])
            r.check(re.match(r"\d{4}-\d{2}-\d{2}$", str(d.get("datePublished", ""))), "BlogPosting datePublished must be YYYY-MM-DD")
            r.check(d.get("datePublished") == today, "BlogPosting datePublished should be today %s" % today, level="warn")
            r.check(d.get("mainEntityOfPage", {}).get("@id") == url, "BlogPosting mainEntityOfPage @id must equal " + url)
            cit = d.get("citation") or []
            r.check(isinstance(cit, list) and cit, "BlogPosting needs a non-empty citation array")
            citations = [c.get("url") for c in cit if isinstance(c, dict)]
        if d.get("@type") == "FAQPage":
            r.check(len(d.get("mainEntity") or []) == SITE["faq_count"], "FAQPage should list %d questions" % SITE["faq_count"])
    for t in SITE["required_jsonld_types"]:
        r.check(t in types, "missing JSON-LD block of type " + t)

    # 3. references and pack
    refs = re.search(r'<section class="refs"[^>]*>(.*?)</section>', html, flags=re.S)
    ref_urls = []
    if r.check(refs, "missing references section"):
        ref_urls = re.findall(r'href="(https?://[^"]+)"', refs.group(1))
        r.check(len(re.findall(r"<li", refs.group(1))) >= 1, "references list is empty")
    if pack_path and parse_pack:
        pack = parse_pack(pack_path)
        r.check(pack["fields"].get("Output file") == article, "pack's Output file is %r, not %s" % (pack["fields"].get("Output file"), article))
        allowed = {s["url"] for s in pack["sources"] if s["url"]}
        for u in ref_urls:
            r.check(u in allowed, "reference URL not in pack: " + u)
        for u in citations:
            r.check(u in allowed, "citation URL not in pack: " + str(u))
        r.check(set(ref_urls) == set(citations), "references and JSON-LD citation URLs should be the same set", level="warn")
        r.check(bool(set(ref_urls) & allowed), "no pack URL is cited at all")

    # 4. links
    body = re.search(r"<main.*?</main>", html, flags=re.S)
    body_html = body.group(0) if body else html
    internal = re.findall(r'href="(/[^"#?]+)"', body_html)
    for link in set(internal):
        r.check(os.path.isfile(rp(link.lstrip("/"))), "internal link points to a missing file: " + link)
    others = [l for l in set(internal) if l.lstrip("/") != article and re.match(r"/(%s)" % "|".join(re.escape(c["output_prefix"]) for c in SITE["languages"].values()), l)]
    r.check(others, "article should link to at least one related existing article")
    back = []
    for l in others:
        target = rp(l.lstrip("/"))
        if os.path.isfile(target) and ('href="/%s"' % article) in open(target, encoding="utf-8").read():
            back.append(l)
    r.check(back, "no related article links back to /%s" % article)

    # 5. integration
    index = open(rp(SITE["index_file"]), encoding="utf-8").read()
    r.check('href="/%s"' % article in index, "no card for /%s in %s" % (article, SITE["index_file"]))
    idx_ok, idx_has = True, False
    for b in jsonld_blocks(index):
        try:
            d = json.loads(b)
        except json.JSONDecodeError as e:
            idx_ok = False
            r.error("%s JSON-LD does not parse: %s" % (SITE["index_file"], e))
            continue
        for post in d.get("blogPost", []) if isinstance(d, dict) else []:
            if post.get("url") == url:
                idx_has = True
                r.check(post.get("inLanguage") == cfg["code"], "index blogPost entry inLanguage should be " + cfg["code"])
    r.check(idx_has or not idx_ok, "no blogPost entry for %s in %s JSON-LD" % (url, SITE["index_file"]))
    try:
        tree = ET.parse(rp(SITE["sitemap_file"]))
        ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        found = False
        for u in tree.getroot().findall("s:url", ns):
            if u.findtext("s:loc", "", ns) == url:
                found = True
                r.check(u.findtext("s:lastmod", "", ns) == today, "sitemap lastmod for the new URL should be today", level="warn")
        r.check(found, "sitemap has no entry for " + url)
    except ET.ParseError as e:
        r.error("%s is not well formed XML: %s" % (SITE["sitemap_file"], e))
    llms = open(rp(SITE["llms_file"]), encoding="utf-8").read()
    r.check(url in llms, "%s has no line for %s" % (SITE["llms_file"], url))

    # 6. forbidden characters in every changed file
    files = changed_files() if use_git else [article]
    if article not in files:
        files.append(article)
    for f in files:
        p = rp(f)
        # packs hold verbatim quotes that may legitimately contain long dashes; the rule is for
        # text the writer produces, so under .automation/ only the run log is checked
        if not os.path.isfile(p) or (f.startswith(".automation/") and f != SITE["run_log"]):
            continue
        if not f.endswith((".html", ".txt", ".xml", ".md", ".json", ".css")):
            continue
        try:
            text = open(p, encoding="utf-8").read()
        except UnicodeDecodeError:
            continue
        for label, ch in SITE["forbidden_chars"].items():
            for n, line in enumerate(text.split("\n"), 1):
                if ch in line:
                    r.error("%s in %s:%d" % (label, f, n))

    # 7. length and script
    words = len(strip_tags(body_html).split())
    lo, hi = cfg["words"]
    r.check(lo * 0.85 <= words <= hi * 1.15, "word count %d outside %d to %d" % (words, lo, hi), level="warn")
    r.note("word count %d (target %d to %d)" % (words, lo, hi))
    if cfg.get("bdi_required"):
        r.check("<bdi>" in body_html, "Arabic article should wrap Latin words and numerals in <bdi>", level="warn")
    return r


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    pack = argv[argv.index("--pack") + 1] if "--pack" in argv else None
    article = os.path.relpath(os.path.abspath(argv[0]), ROOT) if os.path.exists(argv[0]) else argv[0]
    ok = run(article, pack, use_git="--no-git" not in argv).print(article)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
