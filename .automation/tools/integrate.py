#!/usr/bin/env python3
"""Wire a finished article into the site: index card, index JSON-LD, sitemap, llms.txt.

    integrate.py ARTICLE.html --keyword "Market entry" --summary "One sentence for llms.txt" \
                 [--blurb "Card text, defaults to the meta description"] [--sources "WHO TRS ..."]

Title, description and date are read from the article's own BlogPosting JSON-LD. Every step is
idempotent: a URL that is already present is left alone. Reciprocal links between articles are
editorial and stay manual.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import ROOT, SITE, language_for_output, read, rp, write  # noqa: E402


def article_meta(article):
    html = read(article)
    for b in re.findall(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', html, flags=re.S):
        d = json.loads(b)
        if d.get("@type") == "BlogPosting":
            cites = [c.get("name", "") for c in d.get("citation", []) if isinstance(c, dict)]
            return d["headline"], d.get("description", ""), d.get("datePublished"), cites
    sys.exit("no BlogPosting JSON-LD in " + article)


def add_sitemap(url, date):
    path = SITE["sitemap_file"]
    xml = read(path)
    if "<loc>%s</loc>" % url in xml:
        return "sitemap: already present"
    entry = "  <url>\n    <loc>%s</loc>\n    <lastmod>%s</lastmod>\n    <priority>0.8</priority>\n  </url>\n" % (url, date)
    xml = xml.replace("</urlset>", entry + "</urlset>")
    write(path, xml)
    return "sitemap: added"


def add_llms(url, title, summary, cfg):
    path = SITE["llms_file"]
    txt = read(path)
    if url in txt:
        return "llms.txt: already present"
    heading = cfg["llms_heading"]
    if heading not in txt:
        sys.exit("llms.txt heading not found: " + heading)
    line = "- [%s](%s): %s\n" % (title, url, summary)
    head, _, rest = txt.partition(heading + "\n")
    block, _, tail = rest.partition("\n## ")
    block = block.rstrip("\n") + "\n" + line
    txt = head + heading + "\n" + block + ("\n## " + tail if tail else "")
    write(path, txt)
    return "llms.txt: added"


def add_index_card(article, title, blurb, keyword, cfg):
    path = SITE["index_file"]
    html = read(path)
    href = "/" + article
    if 'href="%s"' % href in html:
        return "index card: already present"
    heading = cfg["index_heading"]
    hpos = html.find(heading)
    if hpos < 0:
        sys.exit("index heading not found: " + heading)
    cards_start = html.find('<div class="cards"', hpos)
    nxt = html.find('class="lang-h"', cards_start)
    end_search = nxt if nxt > 0 else html.find("</section>", cards_start)
    last_a = html.rfind("    </a>\n", cards_start, end_search)
    if last_a < 0:
        sys.exit("could not find the last card under " + heading)
    insert_at = last_a + len("    </a>\n")
    card = ('    <a class="card" href="%s">\n      <span class="kw">%s</span>\n      <h3>%s</h3>\n      <p>%s</p>\n    </a>\n'
            % (href, keyword, title, blurb))
    html = html[:insert_at] + card + html[insert_at:]
    write(path, html)
    return "index card: added"


def add_index_jsonld(url, title, date, cfg):
    path = SITE["index_file"]
    html = read(path)
    if '"url": "%s"' % url in html:
        return "index JSON-LD: already present"
    m = re.search(r'("blogPost": \[\n)(.*?)(\n  \])', html, flags=re.S)
    if not m:
        sys.exit("blogPost array not found in " + path)
    entry = '    { "@type": "BlogPosting", "headline": %s, "inLanguage": "%s", "url": "%s", "datePublished": "%s" }' % (
        json.dumps(title, ensure_ascii=False), cfg["code"], url, date)
    body = m.group(2).rstrip()
    body = body + ",\n" + entry
    html = html[:m.start()] + m.group(1) + body + m.group(3) + html[m.end():]
    # prove every JSON-LD block still parses before writing
    for b in re.findall(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', html, flags=re.S):
        json.loads(b)
    write(path, html)
    return "index JSON-LD: added"


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    article = os.path.relpath(os.path.abspath(argv[0]), ROOT) if os.path.exists(argv[0]) else argv[0]
    article = article.replace("\\", "/")

    def opt(flag, default=None):
        return argv[argv.index(flag) + 1] if flag in argv else default

    lang, cfg = language_for_output(article)
    if not cfg:
        sys.exit("cannot tell language from path " + article)
    title, desc, date, cites = article_meta(article)
    url = SITE["base_url"].rstrip("/") + "/" + article
    keyword = opt("--keyword") or sys.exit("--keyword is required (the short label on the card)")
    summary = opt("--summary") or desc
    sources = opt("--sources") or "; ".join(cites)
    if sources and "Source" not in summary:
        summary = summary.rstrip(".") + ". Source%s: %s." % ("s" if ";" in sources else "", sources)
    blurb = opt("--blurb") or desc
    print(add_sitemap(url, date))
    print(add_llms(url, title, summary, cfg))
    print(add_index_card(article, title, blurb, keyword, cfg))
    print(add_index_jsonld(url, title, date, cfg))
    print("remember: add a link from the new article to one related article, and a link back from it")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
