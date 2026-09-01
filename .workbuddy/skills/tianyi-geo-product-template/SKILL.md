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

## Rollout completed (2026-09-01)
All 11 EN + 11 RU product pages done (chain-conveyor & bucket-elevator EN done first as samples).
Remaining GEO steps (not yet done): selection-guide long-form article, site-wide `Organization`
schema, root `llms.txt`.
