#!/usr/bin/env python3
"""
Validate a Tianyi bilingual blog post pair (EN + RU).

Usage:
    python validate_blog_post.py <site_root> <slug>

Example:
    python validate_blog_post.py "E:\\...\\tianyi-site" alumina-conveying-system-indonesia

Checks, for both blog/<slug>.html and ru/blog/<slug>.html:
  - file exists
  - all JSON-LD blocks parse; Article / Organization / BreadcrumbList / FAQPage present
  - visible FAQ items == FAQPage mainEntity items, question and answer text match verbatim
  - hreflang alternates (en / ru / x-default) present and reciprocal
  - canonical points at the page's own URL
  - every referenced image (<img src>, <source srcset>) resolves on disk
  - every site-internal link (relative or "/"-rooted) resolves on disk
  - bilingual symmetry: the only cross-language link is the .lang-switch anchor

Then parses sitemap.xml / sitemap-ru.xml and reports URL counts + slug presence.

IMPORTANT (this host): the PowerShell tool does not echo stdout. Either run this
script and read the generated report file, or pass a report path as argv[3].

    python validate_blog_post.py <site_root> <slug> [report_path]
"""

import json
import os
import re
import sys
import xml.etree.ElementTree as ET

SITE = "https://www.tianyimachine.com"
SITEMAP_NS = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}

RESOURCE_PREFIXES = ("/favicon.ico", "/images/", "/robots.txt", "/sitemap")


def resolve(page_path, root, ref):
    """Map an href/src to an absolute filesystem path, or None if external/ignorable."""
    if not ref:
        return None
    if ref.startswith(("http://", "https://", "//", "mailto:", "tel:", "data:", "#")):
        return None
    ref = ref.split("#")[0].split("?")[0]
    if not ref:
        return None
    if ref.startswith("/"):
        target = os.path.join(root, ref.lstrip("/").replace("/", os.sep))
    else:
        target = os.path.normpath(
            os.path.join(os.path.dirname(page_path), ref.replace("/", os.sep))
        )
    if os.path.isdir(target):
        target = os.path.join(target, "index.html")
    return target


def check_page(label, path, root, own_url, other_url, lang_switch_prefix, report):
    report.append("=" * 72)
    report.append(f"[{label}] {path}")

    if not os.path.exists(path):
        report.append("  !! FILE MISSING")
        return False

    html = open(path, encoding="utf-8").read()
    ok = True

    # --- JSON-LD ---
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
    types = []
    faq_schema = None
    found = set()
    for i, b in enumerate(blocks):
        try:
            d = json.loads(b)
        except Exception as exc:
            report.append(f"  !! JSON-LD block #{i + 1} is invalid JSON: {exc}")
            ok = False
            continue
        t = d.get("@type")
        types.append(t)
        found.add(t)
        if t == "FAQPage":
            faq_schema = d
    report.append(f"  JSON-LD blocks: {len(blocks)} -> {types}")
    for need in ("Article", "Organization", "BreadcrumbList", "FAQPage"):
        if need not in found:
            report.append(f"  !! missing {need} JSON-LD")
            ok = False

    # --- FAQ verbatim match ---
    visible = re.findall(
        r'<div class="faq-item">\s*<h4>(.*?)</h4>\s*<p>(.*?)</p>\s*</div>', html, re.S
    )
    if faq_schema:
        items = faq_schema.get("mainEntity", [])
        report.append(f"  FAQ: visible {len(visible)} / schema {len(items)}")
        faq_ok = len(visible) == len(items) and len(items) > 0
        if len(visible) != len(items):
            report.append("  !! FAQ count mismatch")
            ok = False
        for idx, (q, a) in enumerate(visible):
            if idx >= len(items):
                break
            if q.strip() != items[idx].get("name", "").strip():
                report.append(f"  !! FAQ question #{idx + 1} differs from schema")
                faq_ok = ok = False
            if a.strip() != items[idx].get("acceptedAnswer", {}).get("text", "").strip():
                report.append(f"  !! FAQ answer #{idx + 1} differs from schema")
                faq_ok = ok = False
        report.append(f"  FAQ verbatim match: {faq_ok}")

    # --- hreflang + canonical ---
    hl = dict(
        (l, h)
        for l, h in re.findall(
            r'<link rel="alternate" hreflang="([\w-]+)" href="([^"]+)">', html
        )
    )
    report.append(f"  hreflang: {hl}")
    if hl.get("en") != (own_url if label == "EN" else other_url):
        report.append("  !! hreflang 'en' is wrong")
        ok = False
    if hl.get("ru") != (own_url if label == "RU" else other_url):
        report.append("  !! hreflang 'ru' is wrong")
        ok = False
    if "x-default" not in hl:
        report.append("  !! hreflang 'x-default' missing")
        ok = False

    canon = re.search(r'<link rel="canonical" href="([^"]+)">', html)
    report.append(f"  canonical: {canon.group(1) if canon else None}")
    if not canon or canon.group(1) != own_url:
        report.append("  !! canonical does not match the page's own URL")
        ok = False

    # --- images ---
    imgs = set(re.findall(r'<img[^>]+src="([^"]+)"', html))
    imgs.update(re.findall(r'<source[^>]+srcset="([^"]+)"', html))
    missing_img = [i for i in sorted(imgs) if (t := resolve(path, root, i)) and not os.path.exists(t)]
    report.append(f"  images referenced: {len(imgs)}, missing: {len(missing_img)}")
    for m in missing_img:
        report.append(f"  !! MISSING IMAGE: {m}")
        ok = False

    # --- links ---
    links = set(re.findall(r'href="([^"]+)"', html))
    broken = []
    checked = 0
    for l in sorted(links):
        t = resolve(path, root, l)
        if t is None:
            continue
        checked += 1
        if not os.path.exists(t):
            broken.append(l)
    report.append(f"  internal links checked: {checked}, broken: {len(broken)}")
    for b in broken:
        report.append(f"  !! BROKEN LINK: {b}")
        ok = False

    # --- bilingual symmetry: only the lang-switch may cross languages ---
    lang_switch = re.findall(r'<a href="([^"]+)" class="lang-switch"', html)
    root_abs = [
        h
        for h in links
        if h.startswith("/") and not h.startswith(RESOURCE_PREFIXES) and h not in lang_switch
    ]
    if label == "RU":
        offenders = [h for h in root_abs if not h.startswith("/ru/")]
    else:
        offenders = [h for h in root_abs if h.startswith("/ru/")]
    report.append(
        f"  root-absolute links checked for symmetry: {len(root_abs)}, "
        f"offenders: {len(offenders)}"
    )
    for o in offenders:
        report.append(f"  !! cross-language link outside lang-switch: {o}")
        ok = False
    report.append(f"  lang-switch -> {lang_switch}")

    report.append(f"  RESULT: {'PASS' if ok else 'FAIL'}")
    return ok


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    root = sys.argv[1]
    slug = sys.argv[2]
    report_path = sys.argv[3] if len(sys.argv) > 3 else None

    en_path = os.path.join(root, "blog", f"{slug}.html")
    ru_path = os.path.join(root, "ru", "blog", f"{slug}.html")
    en_url = f"{SITE}/blog/{slug}.html"
    ru_url = f"{SITE}/ru/blog/{slug}.html"

    report = []
    a = check_page("EN", en_path, root, en_url, ru_url, "/ru/", report)
    b = check_page("RU", ru_path, root, ru_url, en_url, "/blog/", report)

    # --- sitemaps ---
    for sm in ("sitemap.xml", "sitemap-ru.xml"):
        fp = os.path.join(root, sm)
        try:
            tree = ET.parse(fp)
            locs = [
                e.text for e in tree.getroot().findall("s:url/s:loc", SITEMAP_NS)
            ]
            hits = [l for l in locs if slug in l]
            report.append(f"{sm}: parses OK, {len(locs)} URLs, slug entries: {hits}")
            if not hits:
                report.append(f"  !! slug not present in {sm}")
                a = b = False
        except Exception as exc:
            report.append(f"{sm}: !! PARSE ERROR {exc}")
            a = b = False

    report.append("=" * 72)
    report.append(f"OVERALL: {'PASS' if (a and b) else 'FAIL'}")

    text = "\n".join(report) + "\n"
    if report_path:
        open(report_path, "w", encoding="utf-8").write(text)
        print(f"report written to {report_path}")
    else:
        print(text)

    sys.exit(0 if (a and b) else 2)


if __name__ == "__main__":
    main()
