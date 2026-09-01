# 天宜机械独立站 — 长期项目备忘

## 项目背景
- 站点：Tianyi Machinery 独立站（散料输送设备 B2B 出口），部署于 Cloudflare Pages，GitHub Desktop 推送。
- 主域：www.tianyimachine.com（apex 已做 A 记录指向 Cloudflare，_redirects 将 apex→www）。
- 已接入：GA4（G-Z39HGKTTPV）、Google Search Console、Bing Webmaster、Yandex Webmaster（meta 验证 25835e1a228a8afb）。
- 站点为手写的静态多页 HTML（index / products/* / projects / blog / blog/* / factory 等，约 25-30 页）。

## 用户目标 / 方向
- **俄语版本站点（/ru/ 子目录）**：让俄语客户在 Yandex 用俄语搜到网站。用户提出后已完成 pilot 实施。
  - 已建页面（共 17 页）：ru/index.html、11 个产品页（belt/chain/bucket/screw/apron/dust-collector/feeding-equipment/crushing-equipment/screening-equipment/valves/parts）、ru/contact.html、ru/blog.html、ru/projects.html、ru/factory.html、ru/certifications.html。
  - 每页：lang="ru" + 俄语 title/description/keywords/og:locale ru_RU + hreflang ru/en/x-default 互链 + 独立 canonical + GA4 + "EN" 切换。
  - 英文对应页（index + 11 产品 + blog + projects，共 14 页）已加 hreflang ru 互链 + "RU" 切换。
  - sitemap-ru.xml（17 条 RU URL，含 xhtml:link 互链），robots.txt 已引用；待用户提交 Yandex/Google。
  - 全站完全双语：17 个英文页（含 factory/certifications）与 17 个 RU 页语言切换对称，RU 站内链接均指向 /ru/*。
  - 注意：英文站无独立 contact.html（联系方式为 index.html#contact 锚点），故 ru/contact.html 的英文互链与 sitemap 均指向首页 /（而非 /contact.html）。其余 RU 页英文互链均指向对应英文页。

## 常用技术约定
- Cloudflare Pages 区分文件名大小写（Linux）→ 引用与文件名必须完全一致（曾因 main.JPG vs main.jpg 裂图）。
- 图片处理：Pillow 缩放至 max 1400px，JPG q85 / WebP q82；中文/空格文件名需重命名为 ASCII。
- 中文路径用 PowerShell 操作；rm/中文路径在 bash(MSYS) 易出编码/segfault 问题。
- git 在 Windows 默认大小写不敏感：`git rm --cached old.JPG` + `git add new.jpg` 才能正确暂存重命名。
- 推送必须用户手动在 GitHub Desktop 执行；我本地改完会给出 Summary 文案。

## GEO 产品页模板（已完成全部 11 EN + 11 RU）
- 全部产品页已落地 GEO 三件套：① 参数表（已有 `.spec-table` 真实 HTML 表）；② FAQ 区块 + FAQPage JSON-LD（每页 5 条，文字与 schema 逐字一致）；③ Product schema 加 `additionalProperty`（关键规格机器可读）。
- 复用脚本/技能：`.workbuddy/skills/tianyi-geo-product-template/`（SKILL.md + scripts/apply_geo_template.py），新增产品时编辑 CONFIG 重跑即可，脚本内置校验（JSON-LD 合法、FAQ 数==可见数）。
- 后续可选 GEO 动作：选型指南长文（权威科普易被 AI 引用）+ 全站 Organization schema + 根目录 llms.txt（AI 版 robots.txt）。
- RU 全站链接对称性已修复（2026-09-01）：曾发现 RU 页面顶部下拉/页脚/正文里 dust-collector/feeding/crushing/screening/valves/parts + projects/blog 仍指向英文 `/products/*.html`、`/projects.html`、`/blog.html`、`/blog/...`，已全部改为 `/ru/...`；校验后 RU 站 0 处残留英文内部链接。

## 双语链接对称性约定（强制）
- RU 页（nav/页脚/正文/related-card/面包屑等）所有内部链接必须指向 `/ru/...`；仅语言切换按钮 `class="lang-switch"` 指向 `/`（英文首页）。
- EN 页所有内部链接指向根级 `/...`；仅语言切换按钮 `RU` 指向 `/ru/...`。
- 资源类（`/favicon.ico`、`/images/*`）与 `mailto:`/`tel:`/外链不受此约束。
- 修复方法：扫描所有 `href="/..."`（排除 /ru/、http、mailto、tel、/、/#、/favicon.ico、/images/），将其 products/projects/blog 链接补 `/ru/` 前缀；注意 `<nav>` 内的嵌套 `<ul>` 易误判，按整文件字符串替换更稳。MSYS bash 处理中文路径 I/O 偶发 segfault，改用 PowerShell 跑脚本。
