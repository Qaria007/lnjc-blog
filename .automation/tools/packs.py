#!/usr/bin/env python3
"""Source pack queue: choose the next pack, list the queue, validate a pack.

    packs.py next                 print the lowest numbered pack whose Output file does not exist
    packs.py list                 show every pack, published or pending, and the queue depth
    packs.py next-number          the next free two digit number for a new pack
    packs.py validate PACK [...]  check a pack's structure; --require-cache also proves every
                                  VERBATIM TEXT paragraph is a substring of the fetched document
                                  (run fetch_source.py on each URL first)

Exit codes: 0 ok, 1 validation errors, 3 queue empty.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import ROOT, SITE, Report, cache_paths, normalise, rp  # noqa: E402

HEADER_FIELDS = ("Language", "Output file", "Template to copy", "Suggested article slug")
NUM_RE = re.compile(r"^(\d{2,3})-")
VERIFIED_RE = re.compile(r"^Verified:\s*(\d{4}-\d{2}-\d{2})\s*\(HTTP\s*(\d{3})\)", re.M)


def parse_pack(path):
    text = open(rp(path), encoding="utf-8").read()
    pack = {"path": path, "text": text, "fields": {}, "sources": [], "title": ""}
    m = re.search(r"^#\s+(.*)$", text, re.M)
    if m:
        pack["title"] = m.group(1).strip()
    for f in HEADER_FIELDS + ("Proposed output file",):
        m = re.search(r"^%s:\s*(.+?)\s*$" % re.escape(f), text, re.M)
        if m:
            pack["fields"][f] = m.group(1).strip()
    pack["verified"] = bool(re.search(r"^STATUS:\s*VERIFIED", text, re.M))
    pack["skeleton"] = bool(re.search(r"SKELETON|DO NOT PUBLISH|NOT VERIFIED", text))
    pack["company_facts"] = "## VERIFIED COMPANY FACTS" in text
    parts = re.split(r"^## SOURCE:\s*", text, flags=re.M)
    for block in parts[1:]:
        name, _, body = block.partition("\n")
        src = {"name": name.strip(), "url": None, "verified": None, "http": None, "text": ""}
        m = re.search(r"^URL to cite:\s*(\S+)", body, re.M)
        if m:
            src["url"] = m.group(1).strip()
        m = VERIFIED_RE.search(body)
        if m:
            src["verified"], src["http"] = m.group(1), m.group(2)
        _, sep, verbatim = body.partition("VERBATIM TEXT:")
        if sep:
            src["text"] = verbatim.strip()
        pack["sources"].append(src)
    return pack


def pack_files():
    d = rp(SITE["sources_dir"])
    out = []
    for name in sorted(os.listdir(d)):
        if name.endswith(".md") and NUM_RE.match(name):
            out.append(os.path.join(SITE["sources_dir"], name))
    return out


def output_exists(pack):
    out = pack["fields"].get("Output file")
    return bool(out) and os.path.isfile(rp(out))


def cmd_next():
    for p in pack_files():
        pack = parse_pack(p)
        if not output_exists(pack):
            f = pack["fields"]
            print("PACK=%s" % p)
            print("LANGUAGE=%s" % f.get("Language", ""))
            print("OUTPUT=%s" % f.get("Output file", ""))
            print("TEMPLATE=%s" % f.get("Template to copy", ""))
            print("SLUG=%s" % f.get("Suggested article slug", ""))
            return 0
    print("QUEUE EMPTY: every pack in %s has an existing Output file" % SITE["sources_dir"])
    return 3


def cmd_list():
    rows, pending = [], 0
    for p in pack_files():
        pack = parse_pack(p)
        done = output_exists(pack)
        pending += 0 if done else 1
        rows.append((os.path.basename(p), pack["fields"].get("Language", "?")[:2].lower(),
                     "published" if done else "PENDING", pack["fields"].get("Output file", "?")))
    for r in rows:
        print("%-45s %-3s %-10s %s" % r)
    print()
    print("queue depth: %d pending pack(s), minimum wanted %d" % (pending, SITE["min_queue"]))
    if pending < SITE["min_queue"]:
        print("REFILL NEEDED")
    return 0


def cmd_next_number():
    nums = [int(NUM_RE.match(os.path.basename(p)).group(1)) for p in pack_files()]
    print("%02d" % (max(nums) + 1 if nums else 1))
    return 0


def cached_text(url):
    txt, meta = cache_paths(url)
    if not os.path.isfile(txt):
        return None, None
    with open(txt, encoding="utf-8") as f:
        t = f.read()
    m = json.load(open(meta, encoding="utf-8")) if os.path.isfile(meta) else {}
    return t, m


def validate(path, require_cache=False):
    r = Report()
    name = os.path.basename(path)
    r.check(NUM_RE.match(name), "file name must start with a two digit number: " + name)
    pack = parse_pack(path)
    f = pack["fields"]
    for field in HEADER_FIELDS:
        r.check(field in f, "missing header line '%s:'" % field)
    if "Proposed output file" in f:
        r.error("still says 'Proposed output file', a finished pack says 'Output file'")
    lang = f.get("Language")
    cfg = SITE["languages"].get(lang)
    r.check(cfg is not None, "Language must be one of %s, got %r" % (list(SITE["languages"]), lang))
    out = f.get("Output file", "")
    if cfg:
        r.check(out.startswith(cfg["output_prefix"]) and out.endswith(".html"),
                "Output file %r should be under %s and end in .html" % (out, cfg["output_prefix"]))
    tpl = f.get("Template to copy", "")
    r.check(os.path.isfile(rp(tpl)), "Template to copy does not exist: %r" % tpl)
    r.check(pack["verified"], "no 'STATUS: VERIFIED' line")
    r.check(not pack["skeleton"], "contains SKELETON / NOT VERIFIED / DO NOT PUBLISH wording")
    # Older packs predate the block; the writer then falls back to company_facts_file.
    r.check(pack["company_facts"], "no '## VERIFIED COMPANY FACTS' block (new packs should copy it from %s)" % SITE.get("company_facts_file"), level="warn")
    cf = SITE.get("company_facts_file")
    if pack["company_facts"] and cf and os.path.isfile(rp(cf)):
        canon = normalise(open(rp(cf), encoding="utf-8").read())
        body = pack["text"].split("## VERIFIED COMPANY FACTS", 1)[1]
        body = re.split(r"^## ", body, maxsplit=1, flags=re.M)[0]
        r.check(normalise("## VERIFIED COMPANY FACTS" + body) == canon,
                "company facts block differs from %s" % cf, level="warn")
    r.check(len(pack["sources"]) >= 1, "no '## SOURCE:' block")
    for i, s in enumerate(pack["sources"], 1):
        tag = "source %d (%s)" % (i, s["name"][:50])
        r.check(s["name"], "source %d has no name after '## SOURCE:'" % i)
        r.check(s["url"] and s["url"].startswith("http"), tag + ": missing 'URL to cite: https://...'")
        r.check(s["verified"], tag + ": missing 'Verified: YYYY-MM-DD (HTTP 200)' line")
        if s["http"]:
            r.check(s["http"] == "200", tag + ": Verified line records HTTP %s, not 200" % s["http"])
        r.check(len(s["text"]) >= 200, tag + ": VERBATIM TEXT is missing or under 200 characters")
        if not s["url"] or not s["text"]:
            continue
        doc, meta = cached_text(s["url"])
        if doc is None:
            msg = tag + ": no fetched copy in %s, verbatim text not mechanically checked (run fetch_source.py)" % SITE["cache_dir"]
            (r.error if require_cache else r.warn)(msg)
            continue
        if meta.get("status") and str(meta["status"]) != "200":
            r.error(tag + ": fetched copy recorded HTTP %s" % meta["status"])
        ndoc = normalise(doc)
        paras = [p for p in re.split(r"\n\s*\n", s["text"]) if normalise(p)]
        checked = missing = 0
        for p in paras:
            # A short label the pack author added on its own line, like "Section 8, starting
            # materials:", is not part of the document and is skipped.
            lines = p.strip().split("\n")
            while lines and len(lines[0]) < 120 and lines[0].rstrip().endswith(":"):
                lines.pop(0)
            rest = "\n".join(lines)
            # "..." between separately quoted passages splits the paragraph into chunks that
            # must each appear verbatim.
            for chunk in re.split(r"\.\.\.|…|\[\.\.\.\]", rest):
                nc = normalise(chunk)
                if len(nc) < 30:
                    continue
                checked += 1
                if nc not in ndoc:
                    missing += 1
                    r.error(tag + ": passage not found verbatim in fetched document: %r" % (nc[:90] + "..."))
        r.check(checked > 0, tag + ": no quotable passage of 30+ characters found in VERBATIM TEXT")
        r.note(tag + ": %d/%d passages matched the fetched document" % (checked - missing, checked))
    for label, ch in SITE["forbidden_chars"].items():
        n = pack["text"].count(ch)
        if n:
            r.warn("%d %s character(s) in the pack; verbatim quotes may keep them, but the article must not" % (n, label))
    return r


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    cmd, args = argv[0], argv[1:]
    if cmd == "next":
        return cmd_next()
    if cmd == "list":
        return cmd_list()
    if cmd == "next-number":
        return cmd_next_number()
    if cmd == "validate":
        require = "--require-cache" in args
        paths = [a for a in args if not a.startswith("--")]
        if not paths:
            print("validate needs at least one pack path")
            return 2
        ok = True
        for p in paths:
            rel = os.path.relpath(os.path.abspath(p), ROOT) if os.path.isabs(p) or os.path.exists(p) else p
            ok = validate(rel, require).print(rel) and ok
        return 0 if ok else 1
    print("unknown command " + cmd)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
