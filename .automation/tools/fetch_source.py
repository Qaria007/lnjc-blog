#!/usr/bin/env python3
"""Fetch a primary document and keep a local text copy that packs.py can check excerpts against.

    fetch_source.py get URL [--name "Issuing body, title, series"]
        Downloads URL, records the HTTP status and date, extracts plain text (HTML or PDF), saves
        it under the cache directory named in site.json, and prints a ready '## SOURCE:' header.
    fetch_source.py find URL|CACHEFILE "phrase" [--context 400]
        Prints every paragraph of the fetched text containing the phrase (case insensitive), so
        you can locate the section to quote and copy it exactly.
    fetch_source.py show URL|CACHEFILE [--start N --length M]
        Prints a slice of the fetched text.

Needs network access. In a container whose egress policy blocks the host you will see an HTTP
403 from the proxy or a connection error; that is an environment problem, not a source problem.
PDF text extraction uses the pdftotext binary if present, otherwise the pypdf package
(pip install pypdf).
"""
import datetime
import hashlib
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from html.parser import HTMLParser

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import SITE, cache_paths, rp  # noqa: E402

UA = "Mozilla/5.0 (compatible; source-pack-fetcher/1.0; +%s)" % SITE.get("base_url", "")


class _Text(HTMLParser):
    SKIP = {"script", "style", "noscript", "svg", "head", "nav", "footer", "header", "form"}
    BLOCK = {"p", "div", "li", "h1", "h2", "h3", "h4", "h5", "h6", "tr", "br", "section",
             "article", "table", "ul", "ol", "blockquote", "pre", "dd", "dt"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.skip = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self.skip += 1
        elif tag in self.BLOCK:
            self.out.append("\n")

    def handle_endtag(self, tag):
        if tag in self.SKIP and self.skip:
            self.skip -= 1
        elif tag in self.BLOCK:
            self.out.append("\n")

    def handle_data(self, data):
        if not self.skip:
            self.out.append(data)


def html_to_text(raw):
    p = _Text()
    p.feed(raw)
    t = "".join(p.out)
    t = re.sub(r"[ \t\r\f\v]+", " ", t)
    t = re.sub(r" *\n *", "\n", t)
    t = re.sub(r"\n{3,}", "\n\n", t)
    return t.strip()


def pdf_to_text(data):
    if shutil.which("pdftotext"):
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            f.write(data)
            path = f.name
        try:
            out = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, check=True)
            return out.stdout.decode("utf-8", "replace")
        finally:
            os.unlink(path)
    try:
        import io
        import pypdf
    except ImportError:
        sys.exit("PDF received but neither pdftotext nor pypdf is available. Run: pip install pypdf")
    reader = pypdf.PdfReader(io.BytesIO(data))
    return "\n\n".join((page.extract_text() or "") for page in reader.pages)


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            return resp.status, resp.geturl(), resp.headers.get("Content-Type", ""), resp.read()
    except urllib.error.HTTPError as e:
        return e.code, e.geturl(), e.headers.get("Content-Type", "") if e.headers else "", e.read()
    except Exception as e:  # noqa: BLE001
        sys.exit("fetch failed for %s: %s (if this is a proxy 403, the environment's network policy blocks the host)" % (url, e))


def cmd_get(url, name):
    status, final, ctype, data = fetch(url)
    today = datetime.date.today().isoformat()
    if status != 200:
        print("HTTP %s for %s" % (status, url))
        print("Do not cite this URL until it returns 200. Find the issuing body's current location.")
        return 1
    is_pdf = "pdf" in ctype.lower() or data[:5] == b"%PDF-" or final.lower().endswith(".pdf")
    text = pdf_to_text(data) if is_pdf else html_to_text(data.decode("utf-8", "replace"))
    txt_path, meta_path = cache_paths(url)
    os.makedirs(os.path.dirname(txt_path), exist_ok=True)
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(text)
    meta = {"url": url, "final_url": final, "status": status, "content_type": ctype, "fetched": today,
            "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(), "kind": "pdf" if is_pdf else "html",
            "chars": len(text)}
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=1)
    print("fetched %s" % url)
    if final != url:
        print("  redirected to %s (cite the URL you asked for only if the redirect is the issuing body's own)" % final)
    print("  HTTP %s, %s, %d bytes, %d characters of text" % (status, meta["kind"], len(data), len(text)))
    print("  text saved to %s" % os.path.relpath(txt_path, rp(".")))
    if len(text) < 500:
        print("  WARNING: very little text extracted. A landing page, a scanned PDF, or a bot wall. Open it and check.")
    print()
    print("Paste this header into the pack, then copy paragraphs from the saved text file exactly:")
    print()
    print("## SOURCE: %s" % (name or "<Issuing body, document title, series and year>"))
    print("URL to cite: %s" % url)
    print("Verified: %s (HTTP %s)" % (today, status))
    print()
    print("VERBATIM TEXT:")
    print()
    return 0


def load_cached(ref):
    if os.path.isfile(ref):
        return open(ref, encoding="utf-8").read()
    txt, _ = cache_paths(ref)
    if not os.path.isfile(txt):
        sys.exit("no fetched copy for %s, run: fetch_source.py get URL" % ref)
    return open(txt, encoding="utf-8").read()


def cmd_find(ref, phrase, context):
    text = load_cached(ref)
    paras = re.split(r"\n\s*\n", text)
    hits = 0
    for i, p in enumerate(paras):
        if phrase.lower() in p.lower():
            hits += 1
            print("--- paragraph %d ---" % i)
            print(p.strip()[:context])
            print()
    print("%d paragraph(s) contain %r" % (hits, phrase))
    return 0


def cmd_show(ref, start, length):
    text = load_cached(ref)
    print(text[start:start + length])
    return 0


def main(argv):
    if not argv or argv[0] not in ("get", "find", "show"):
        print(__doc__)
        return 2
    cmd = argv[0]

    def opt(flag, default=None):
        if flag in argv:
            return argv[argv.index(flag) + 1]
        return default

    if cmd == "get":
        return cmd_get(argv[1], opt("--name"))
    if cmd == "find":
        return cmd_find(argv[1], argv[2], int(opt("--context", 400)))
    if cmd == "show":
        return cmd_show(argv[1], int(opt("--start", 0)), int(opt("--length", 3000)))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
