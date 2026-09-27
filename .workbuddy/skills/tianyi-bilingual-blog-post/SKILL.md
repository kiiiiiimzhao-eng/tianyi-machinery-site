---
name: tianyi-bilingual-blog-post
agent_created: true
description: Create and integrate an English plus Russian SEO/GEO-optimized blog article pair for the Tianyi Machinery static HTML site, including image processing, hreflang, four JSON-LD blocks, FAQ schema, sitemaps, llms.txt, and index-page cards.
---

# Tianyi Bilingual Blog Post

## Overview

This skill produces a matched pair of English and Russian blog articles for the Tianyi Machinery static multi-page site (`E:\赵雯\独立站\Kim网站\tianyi-site`), optimizes them for search engines and generative engines, and wires them into the navigation, sitemaps, `llms.txt`, and hreflang cluster.

## When to Use

Use this skill when the user asks to:

- Write a new blog article in English and Russian ("同步更新英文站和俄语站").
- Add an article to `blog.html` and `ru/blog.html`.
- Create a project / case-study article with a supplied photo.
- Optimize a blog post for SEO (title, meta, keywords, schema, hreflang, sitemap).

## Site Conventions You Must Respect

- **Root = English**, `ru/` = Russian mirror. Site root: `E:\赵雯\独立站\Kim网站\tianyi-site`.
- **EN page** lives at `blog/<slug>.html`; **RU page** at `ru/blog/<slug>.html`. Same slug in both.
- **Path depth differs between the two pages** — this is the #1 source of broken RU pages:
  | Reference | EN `blog/<slug>.html` | RU `ru/blog/<slug>.html` |
  |---|---|---|
  | Images | `../images/...` | `../../images/...` |
  | Product pages | `../products/x.html` | `../products/x.html` (resolves to `ru/products/`) |
  | Projects | `../projects.html` | `../projects.html` (resolves to `ru/projects.html`) |
  | Home | `../index.html` | `/ru/` |
  | Blog index | `../blog.html` | `/ru/blog.html` |
  | Contact CTA | `../index.html#contact` | `/ru/contact.html` |
  | Related post | `<other-slug>.html` | `<other-slug>.html` |
- **Bilingual link symmetry (mandatory):** every internal link on a RU page points to `/ru/...` (or relatively inside `ru/`); every internal link on an EN page points to root-level `/...`. The **only** cross-language links are:
  - RU page: `<a href="/blog/<slug>.html" class="lang-switch">EN</a>`
  - EN page: `<a href="/ru/blog/<slug>.html" class="lang-switch">RU</a>`
  Resources (`/favicon.ico`, `/images/*`), `mailto:`, `tel:` and external links are exempt.
- Cloudflare Pages is case-sensitive — reference images with the exact on-disk filename casing.
- Category buckets on the index pages are only: `Maintenance Guides` / `Company News` / `Industry Insights` (RU: `Руководства по обслуживанию` / `Новости компании` / `Отраслевые обзоры`). **Project case studies and industry/technical guides both go under `Industry Insights` / `Отраслевые обзоры`** — there is no separate case-study bucket.

## Workflow

### 1. Understand the Topic and Assets

- Identify the core topic, target keywords, and audience (B2B bulk-material handling).
- Collect the photos or diagrams the user provides. Source images often live on the Desktop with Chinese names/spaces — copy them into an ASCII-named temp path before processing.
- Pick a kebab-case ASCII slug, e.g. `alumina-conveying-system-indonesia`. Use it for both pages.

### 2. Process the Image(s)

- Create `images/blog/<slug>/`.
- Resize so the longest side is at most 1400 px, then export:
  - `main.jpg` — JPEG quality 85, optimized, progressive.
  - `main.webp` — WebP quality 82.
- Use `scripts/process_blog_image.py <source_image> <output_dir> [base_name]`. `base_name` defaults to `main`.
- **Multi-image posts:** the user frequently supplies several photos. Export the hero as `main`, and the extra figures under descriptive ASCII names (`gallery`, `plant`, `transfer-point`, …), each as `<name>.jpg` + `<name>.webp`. Reference each with its own `<figure><picture>` in the body — one hero right after the lead or the system-architecture section, plus one supporting figure per relevant section — and give every one a descriptive `alt` and a caption.
- Source photos are often on a Chinese-named path (e.g. `E:\赵雯\图片\按分类\...`). Copy them into an ASCII-named temp dir (`.workbuddy/tmp_<slug>/`) first, then process; MSYS bash segfaults on Chinese paths, so drive PowerShell for the copy and the run.
- Verify the outputs exist and read their dimensions/sizes back before moving on.

```bash
"C:/Users/Administrator/.workbuddy/binaries/python/envs/default/Scripts/python.exe" \
  .workbuddy/skills/tianyi-bilingual-blog-post/scripts/process_blog_image.py \
  "E:/.../tmp_dir/src.jpg" \
  "E:/.../tianyi-site/images/blog/<slug>"
```

### 3. Write the English Article

- Create `blog/<slug>.html`.
- Copy the full chrome (head, styles, GA4 block, header/nav, mobile-menu script, footer) from the **most recent** article, e.g. `blog/coal-fired-power-plant-conveying-equipment-selection.html` — it carries the current CSS and nav markup.
- Head must contain:
  - `lang="en"`, unique `<title>`, `<meta name="description">`, `<meta name="keywords">` (English + Chinese/Indonesian trade terms where relevant).
  - `<link rel="canonical">` → the EN URL.
  - `hreflang` alternates: `ru`, `en`, `x-default`.
  - Open Graph + Twitter Card tags.
- Body must contain **four** JSON-LD blocks:
  1. `Article` (headline, description, image, datePublished, dateModified, author, publisher, mainEntityOfPage)
  2. `Organization` (copy verbatim from an existing page — the whole site carries the same block)
  3. `BreadcrumbList` (Home → Blog → article)
  4. `FAQPage` (inside the article body, next to the visible FAQ)
- Structure the visible body:
  - Hero: category label, H1, meta (date, read time, author).
  - Lead paragraph containing the primary keyword.
  - TOC with anchor links to every H2.
  - 8–10 H2 sections with bullet lists, comparison tables and `.callout` boxes where useful.
  - At least one `<figure>` with `<picture>` (WebP source + JPG `img` fallback), descriptive `alt`, and a caption. Keep the existing `onerror` inline fallback from the template.
  - Internal links to relevant `../products/*.html` pages.
  - **FAQ section of 5 items**, each `<div class="faq-item"><h4>Q</h4><p>A</p></div>`.
  - `.cta-box` linking to `../index.html#contact`.
  - `.related-posts` grid with 4 links to existing articles/products (verify each target file exists).

### 4. Write the Russian Article

- Create `ru/blog/<slug>.html` as a full, natural Russian adaptation (not a word-for-word machine translation).
- Apply **every** rule from the "Site Conventions" table above — especially `../../images/` and `/ru/...` links.
- `lang="ru"`, Russian title/description/keywords/OG, independent canonical to the RU URL, and reciprocal hreflang.
- Translate headings, TOC, table headers, callouts, FAQ, CTA and related-reading titles.
- Keep the heading structure identical to the EN page so the two stay in sync.

### 5. Add Cards to the Blog Index Pages

- `blog.html`: add an EN card at the **top** of the `Industry Insights` grid.
- `ru/blog.html`: add the matching RU card at the top of the `Отраслевые обзоры` grid.
- Card format: `<a href="blog/<slug>.html" class="blog-card">` with a `thumb` using `background-image:url('images/blog/<slug>/main.jpg')` (EN) or `url('../images/blog/<slug>/main.jpg')` (RU), plus date, `<h3>` title, `<p>` summary, and the category `<span class="tag">`.
- Escape `&` as `&amp;` in card titles.

### 6. Update Sitemaps and llms.txt

- `sitemap.xml`: append a `<url>` with `loc` / `lastmod` (today, `YYYY-MM-DD`) / `changefreq` (`monthly`) / `priority` (`0.7`). Also bump the `blog.html` entry's `lastmod` to today.
- `sitemap-ru.xml`: append a `<url>` with the RU `loc` plus three `xhtml:link` alternates (`ru`, `en`, `x-default`). This file has no `lastmod` tags — match the existing format.
- `llms.txt`: add the new article under `## Project Solutions` (case studies) or `## Technical Guides & Blog`, and append the RU URL to the `## Russian-language site` paragraph.

### 7. Verify (run the script, do not eyeball)

```bash
"C:/Users/Administrator/.workbuddy/binaries/python/envs/default/Scripts/python.exe" \
  .workbuddy/skills/tianyi-bilingual-blog-post/scripts/validate_blog_post.py \
  "E:/赵雯/独立站/Kim网站/tianyi-site" "<slug>" "<report_path>"
```

The script checks: both files exist; all JSON-LD parses and all four types are present; visible FAQ count equals the FAQPage `mainEntity` count and the text matches verbatim; hreflang is reciprocal; canonical is self-referencing; every image and internal link resolves on disk; no cross-language link exists outside the `.lang-switch`; both sitemaps parse and contain the slug. It exits non-zero and prints `OVERALL: FAIL` on any problem.

> **This host's PowerShell tool does not echo stdout.** Always pass a `<report_path>` and read the report file with the Read tool, or the run will look like it produced nothing.

### 8. Clean Up and Update Project Memory

- Delete any temp working directory (`.workbuddy/tmp_*/`) and intermediate scripts/logs.
- Append a summary to `.workbuddy/memory/YYYY-MM-DD.md` (create the file if missing): slug, files created, images, index/sitemap/llms changes, validation result.
- Update `.workbuddy/memory/MEMORY.md` if a new convention or page was added.
- Tell the user that the GitHub Desktop push is manual, and suggest a commit Summary line.

## Resources

### scripts/process_blog_image.py

Resizes a source image to a max longest edge of 1400 px and exports optimized JPG (q85) + WebP (q82) as `main.jpg` / `main.webp`. Also applies EXIF orientation correction.

### scripts/validate_blog_post.py

Validates a completed EN+RU article pair plus both sitemaps. Usage: `validate_blog_post.py <site_root> <slug> [report_path]`. Exit code 0 = pass, 2 = fail.

## Notes

- Keep English and Russian articles structurally identical so the hreflang cluster stays valid.
- The recurring RU failure mode is `../images/` on a `ru/blog/` page, which resolves to `/ru/images/` (which does not exist) and produces 404 images. If you ever find this on existing pages, fix the whole directory, not just the new file.
- The `X-Frame-Options: DENY` header does not affect external iframes; if adding maps or widgets, update CSP `frame-src` in `_headers` instead.
- The site is deployed on Cloudflare Pages; the apex-domain 301 depends on `tianyimachine.com` being bound as a Custom Domain in the Pages project.
