"""Shared helpers for the article automation tools. Standard library only."""
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def find_repo_root(start=None):
    """Walk up from start (default: this file) until a directory holding .automation/site.json."""
    d = os.path.abspath(start or HERE)
    while True:
        if os.path.isfile(os.path.join(d, ".automation", "site.json")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            sys.exit("could not find .automation/site.json above " + (start or HERE))
        d = parent


ROOT = find_repo_root()


def load_site():
    with open(os.path.join(ROOT, ".automation", "site.json"), encoding="utf-8") as f:
        site = json.load(f)
    # forbidden characters are written as code points ("U+2014") so the config file itself
    # never contains the characters it bans
    site["forbidden_chars"] = {
        label: chr(int(cp[2:], 16)) if cp.upper().startswith("U+") else cp
        for label, cp in site.get("forbidden_chars", {}).items()
    }
    return site


SITE = load_site()


def rp(path):
    """Repo relative path to absolute."""
    return os.path.join(ROOT, path)


def read(path):
    with open(rp(path), encoding="utf-8") as f:
        return f.read()


def write(path, text):
    with open(rp(path), "w", encoding="utf-8") as f:
        f.write(text)


def url_key(url):
    return hashlib.sha1(url.strip().encode("utf-8")).hexdigest()[:16]


def cache_paths(url):
    d = rp(SITE["cache_dir"])
    k = url_key(url)
    return os.path.join(d, k + ".txt"), os.path.join(d, k + ".json")


_WS = re.compile(r"\s+")
# Written as code points so this file never contains the characters the style rule bans.
_QUOTES = {chr(cp): rep for cp, rep in (
    (0x2018, "'"), (0x2019, "'"), (0x201A, "'"), (0x201B, "'"),
    (0x201C, '"'), (0x201D, '"'), (0x201E, '"'), (0x201F, '"'),
    (0x2010, "-"), (0x2011, "-"), (0x2012, "-"), (0x2013, "-"), (0x2014, "-"), (0x2212, "-"),
    (0x00A0, " "), (0x2009, " "), (0x202F, " "), (0xFEFF, ""),
    (0x00AD, ""),
)}


def normalise(text):
    """Collapse whitespace and unify punctuation variants so that a verbatim excerpt can be
    matched against extracted document text despite PDF line breaks and smart quotes."""
    for a, b in _QUOTES.items():
        text = text.replace(a, b)
    # Hyphenation at line ends in PDFs: "third- party" and "third-\nparty" both become "third-party"
    text = re.sub(r"-\s+", "-", text)
    return _WS.sub(" ", text).strip()


def language_for_output(output_file):
    for name, cfg in SITE["languages"].items():
        if output_file.startswith(cfg["output_prefix"]):
            return name, cfg
    return None, None


class Report:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.notes = []

    def error(self, msg):
        self.errors.append(msg)

    def warn(self, msg):
        self.warnings.append(msg)

    def note(self, msg):
        self.notes.append(msg)

    def check(self, cond, msg, level="error"):
        if not cond:
            (self.error if level == "error" else self.warn)(msg)
        return cond

    def print(self, title):
        print("== " + title)
        for n in self.notes:
            print("   note  " + n)
        for w in self.warnings:
            print("   WARN  " + w)
        for e in self.errors:
            print("   FAIL  " + e)
        print("   %d error(s), %d warning(s)" % (len(self.errors), len(self.warnings)))
        return len(self.errors) == 0
