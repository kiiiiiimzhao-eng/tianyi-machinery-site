---
name: tianyi-geo-product-template
description: Add GEO (Generative Engine Optimization) template to Tianyi Machinery product pages — FAQ section + FAQPage JSON-LD + enhanced Product schema (additionalProperty). Use when rolling FAQ/schema onto products/ or ru/products/ pages to make them citable by AI search engines.
---

# GEO Product Template for Tianyi Site

Generative Engine Optimization = making product pages citable by ChatGPT / Perplexity /
Gemini / Google AI Overviews. For this static bilingual site the highest-leverage move is a
**parameter table + FAQ + structured data** on every product page.

## What gets added per page
1. **FAQ CSS** — `.faq-list` / `.faq-item` styles (appended after the `.feature-item p` rule).
2. **Enhanced Product schema** — adds `additionalProperty` (machine-readable specs) to the existing `Product` JSON-LD.
3. **FAQPage JSON-LD** — `application/ld+json` with Question/acceptedAnswer matching the visible FAQ text exactly.
4. **FAQ HTML section** — `<section id="faq">` inserted right before the CTA (`<div class="cta-box">`).

## Critical rules
- **FAQ text must be byte-identical** in the visible HTML and the JSON-LD `name`/`text`. Build both
  from the same source list so they can't drift. Google/AI reject mismatched FAQ markup.
- **Avoid double quotes `"` inside FAQ text.** JSON escapes them to `\"` which then won't match the
  HTML. Use single quotes or no quotes. Non-ASCII (°, – , ², Cyrillic) is fine — dump JSON with
  `ensure_ascii=False` and keep the HTML file UTF-8.
- **Idempotent**: script skips if `id="faq"`, `/* FAQ (GEO template) */`, `additionalProperty`, or
  `FAQPage` already present. Safe to re-run.

## Injection anchors (stable across all product pages)
- CSS: `.feature-item p { font-size:13px; color:var(--text-muted); margin:0; }`
- CTA: `<section class="container">\n  <div class="cta-box">`
- Product schema: first `<script type="application/ld+json">...</script>` whose `@type` == `Product`.
  Parse with `json.loads`, add `additionalProperty`, re-dump with `indent=2, ensure_ascii=False`,
  then append the FAQPage script right after it (before `<style>`).
- RU pages use `../../images/...` (two levels up) for images and `ru/products/` path; anchors above
  are identical, so the same script handles EN and RU.

## Reusable script
`scripts/apply_geo_template.py` — a `CONFIG` dict keyed by product slug, each with `en`/`ru` keys
holding `props` (list of [name, value]) and `faq` (list of [question, answer]). Edit `CONFIG` per
product, then run:

```
python .workbuddy/skills/tianyi-geo-product-template/scripts/apply_geo_template.py
```

The script applies changes AND runs a validation pass (JSON-LD parses, FAQ count == visible
faq-items, every Q/A string present in HTML). All pages must print `VALID`.

## Typical content per product
- 5–6 FAQ covering: what it is / what materials / model-series differences / max capacity or
  size / dust-tight or explosion-proof / comparison to sibling equipment.
- `additionalProperty`: 5–6 key specs pulled from the existing `.spec-table`.

## Site-wide Organization schema (done 2026-09-02)
A single `Organization` JSON-LD block (name, url, logo, description, foundingDate, address,
contactPoint, numberOfEmployees) is injected into **every** HTML page so AI engines resolve the
company entity consistently. `index.html` already had one; 56 other pages got it added.

- `scripts/inject_org_schema.py` — scans all `*.html` (excluding `.workbuddy`/`audit`), skips pages
  that already have a top-level `"@type":"Organization"`, injects the block right before `</head>`.
  Idempotent. Re-run after adding new pages.
- Verify with a second pass counting top-level Organization blocks == 1 per page and JSON valid.

## Selection-guide long-form article (done 2026-09-02)
`blog/bulk-material-handling-equipment-selection-guide.html` (+ RU mirror in `ru/blog/`) is the
flagship GEO asset: comprehensive, fact-dense, with `Article` + `FAQPage` JSON-LD, TOC, internal
links to every product page, and a hero image. Pattern to copy for future guides:
- Copy the TDG blog-post template (`blog/tdg-gas-tight-explosion-proof-bucket-elevator.html`).
- Use real `spec-table`/`faq` content; keep FAQ text byte-identical to `FAQPage` schema.
- Add a card to `blog.html` (Industry Insights) + `ru/blog.html` (Отраслевые обзоры), and add the
  URL to `sitemap.xml` (EN) + `sitemap-ru.xml` (RU, with xhtml:link alternates).
- Hero image: generate with ImageGen, then run `tianyi-bilingual-blog-post` `process_blog_image.py`
  to emit `main.jpg` (q85) + `main.webp` (q82).

## Root llms.txt (done 2026-09-02)
`llms.txt` at site root is the AI-version of robots.txt: `# Title`, `> description`, then `##`
sections listing Products / Project Solutions / Technical Guides & Blog / Company, each as
`- [Label](url): description`. Points AI crawlers to the canonical EN pages and notes the `/ru/`
mirror. No robots.txt change needed (`Allow: /` already covers it).

## Full GEO rollout status (2026-09-02)
- [x] Product pages: FAQ + FAQPage + Product additionalProperty (11 EN + 11 RU)
- [x] Selection-guide long-form article (EN + RU) with FAQPage + sitemaps
- [x] Site-wide `Organization` schema (58 pages, 1 each)
- [x] Root `llms.txt`
