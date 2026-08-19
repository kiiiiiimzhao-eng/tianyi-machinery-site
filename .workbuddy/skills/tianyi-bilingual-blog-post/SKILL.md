---
name: tianyi-bilingual-blog-post
agent_created: true
description: Create and integrate an English plus Russian SEO-optimized blog article pair for the Tianyi Machinery static HTML site, including image processing, hreflang, sitemaps, and index-page cards.
---

# Tianyi Bilingual Blog Post

## Overview

This skill produces a matched pair of English and Russian blog articles for the Tianyi Machinery static multi-page site, optimizes them for search engines, and wires them into the existing navigation, sitemaps, and hreflang clusters.

## When to Use

Use this skill when the user asks to:

- Write a new blog article in English and Russian.
- Add an article to blog.html and ru/blog.html.
- Create a project or case-study article with a photo for the Tianyi site.
- Optimize a new blog post for SEO (title, meta, keywords, schema, hreflang, sitemap).

## Workflow

### 1. Understand the Topic and Assets

- Identify the core topic, target keywords, and intended audience (B2B bulk-material handling, new energy, chemical, mining).
- Collect any photos or diagrams the user provides. Ask for clarification if the image path or intended filename is unclear.
- Decide a URL slug in kebab-case ASCII (for example, `gas-tight-en-masse-conveyor-nitrogen-inerting`). Use the same slug for both EN and RU pages.

### 2. Process the Image

- Create the directory `images/blog/<slug>/` if it does not exist.
- Resize the source image so the longest side is at most 1400 px.
- Export two versions:
  - `main.jpg` - JPEG quality 85, optimized.
  - `main.webp` - WebP quality 82.
- Use the provided `scripts/process_blog_image.py` or an equivalent Pillow one-liner.
- Ensure the filename is ASCII-only (no spaces or non-ASCII characters) to avoid Cloudflare Pages and Git case-sensitivity issues.

### 3. Write the English Article

- Create `blog/<slug>.html`.
- Copy the chrome (header, nav, footer, styles, GA4, mobile menu) from an existing article such as `blog/chlor-alkali-conveying-system.html`.
- Set:
  - `lang="en"`
  - Unique `<title>` (60-70 chars), `<meta name="description">`, `<meta name="keywords">`.
  - `<link rel="canonical">` pointing to the EN URL.
  - `hreflang` alternates: `ru`, `en`, `x-default`.
  - Open Graph and Twitter Card tags.
  - Schema.org `Article` JSON-LD with headline, description, image, datePublished, dateModified, author, publisher, mainEntityOfPage.
- Structure the body:
  - Hero section with category label, H1, and meta (date, read time, author).
  - Lead paragraph with the target keyword.
  - Table of contents linking to H2 sections.
  - H2/H3 sections with bullet lists, tables, and callouts where useful.
  - One `<figure>` with `<picture>` (WebP fallback to JPG) and descriptive alt text and caption.
  - Internal links to relevant product pages, projects, or contact.
  - CTA box at the end.
  - Related Reading grid with 3 relevant links.

### 4. Write the Russian Article

- Create `ru/blog/<slug>.html` as a faithful translation or adaptation of the English article.
- Use `lang="ru"` and Russian title, description, and keywords.
- Keep the same URL slug as the English version.
- Link canonical and `hreflang` alternates to the EN and RU URLs.
- Use Russian navigation labels and point the contact link to `/ru/contact.html`.
- Translate the CTA and related-reading titles.

### 5. Add Cards to the Blog Index Pages

- In `blog.html`, add an EN card under the correct category (usually `Industry Insights`). Place the newest article first.
- In `ru/blog.html`, add a matching RU card under the corresponding Russian category (`Ot raslevye obzory`).
- Use the processed image as the card thumbnail via `background-image` CSS.
- Ensure RU index cards link to RU article URLs, not English URLs. Fix any existing wrong links found while editing.

### 6. Update Sitemaps

- Add the new EN URL to `sitemap.xml` using the same `<url>` format as existing entries (`loc`, `lastmod`, `changefreq`, `priority`).
- Add the new RU URL to `sitemap-ru.xml` with three `xhtml:link` alternates (`ru`, `en`, `x-default`).
- Validate both XML files for well-formedness.

### 7. Verify

- Confirm both HTML files exist and contain reciprocal `hreflang` links.
- Confirm the image files exist in `images/blog/<slug>/`.
- Confirm index-page cards point to the correct URLs and display the thumbnail.
- Confirm sitemap counts increased by one in each file and XML parses successfully.

### 8. Update Project Memory

- Append a summary to `.workbuddy/memory/YYYY-MM-DD.md`.
- Note the slug, files created or modified, SEO elements added, sitemap changes, and the pending GitHub Desktop push.

## Resources

### scripts/process_blog_image.py

Resizes a source image to a max longest-edge of 1400 px and exports optimized JPG (q85) and WebP (q82) versions into `images/blog/<slug>/`.

Usage example:

```bash
python scripts/process_blog_image.py \\
    "path/to/source.jpg" \\
    "E:\\\\path\\\\to\\\\tianyi-site\\\\images\\\\blog\\\\<slug>"
```

## Notes

- Cloudflare Pages is case-sensitive: always reference images with the exact filename casing stored on disk.
- Keep English and Russian articles structurally identical so hreflang clusters remain valid.
- The `X-Frame-Options: DENY` header does not affect external iframes; if adding maps or widgets, update CSP `frame-src` in `_headers` instead.
