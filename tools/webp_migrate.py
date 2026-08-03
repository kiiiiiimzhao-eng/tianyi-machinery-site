#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tianyi Machinery 进阶方案：JPG -> WebP 并改写 HTML 为 <picture>
==========================================================

为什么需要它？
  JPEG 重压缩（optimize_images.py）已经能大幅减小体积且零改动 HTML。
  但若要进一步压榨体积（通常再省 25%~40%），可转 WebP/AVIF，并用
  <picture> 渐进增强，让现代浏览器加载更小的 WebP，老浏览器回退 JPEG。

本脚本做什么（默认 DRY-RUN，不会改任何文件）：
  1. 为 images/ 下每个 .jpg/.jpeg 生成同名的 .webp（quality 可调）。
  2. 扫描所有 .html，把 <img src="x.jpg" ...> 包裹为：
       <picture>
         <source srcset="x.webp" type="image/webp">
         <img src="x.jpg" ...>
       </picture>
     —— 当浏览器支持 WebP 时自动用 WebP，不支持则回退原 JPG，安全无破损。
  3. 可选 --css：把 CSS background-image: url(x.jpg) 一并替换为 x.webp
     （注意：CSS 无法优雅回退，仅在你确认目标浏览器都支持 WebP 时启用）。

用法：
  # 先预览会发生什么（强烈建议先看）
  python webp_migrate.py --dry-run

  # 真正执行（会生成 .webp 并改写 HTML；建议先 git 提交或备份）
  python webp_migrate.py --apply

  # 只生成 webp，不碰 HTML（方便你手动决定如何引用）
  python webp_migrate.py --apply --no-html

依赖：Pillow
  pip install Pillow
"""

import argparse
import io
import os
import re
import sys

try:
    from PIL import Image
except ImportError:
    sys.exit("缺少 Pillow，请先执行: pip install Pillow")

IMG_EXT = (".jpg", ".jpeg", ".JPG", ".JPEG")
HTML_RE = re.compile(r'(<img\b[^>]*\bsrc="([^"]+)"[^>]*>)', re.IGNORECASE)


def gen_webp(src_path, quality):
    with Image.open(src_path) as img:
        if img.mode != "RGB":
            img = img.convert("RGB")
        buf = io.BytesIO()
        img.save(buf, format="WEBP", quality=quality, method=6)
        return buf.getvalue()


def walk_images(root):
    out = []
    for dp, _, fns in os.walk(root):
        for fn in fns:
            if fn.lower().endswith(IMG_EXT):
                out.append(os.path.join(dp, fn))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=None, help="项目根目录（默认脚本上两级）")
    ap.add_argument("--quality", type=int, default=80)
    ap.add_argument("--apply", action="store_true", help="真正写入（默认仅预览）")
    ap.add_argument("--dry-run", action="store_true", help="仅预览，不写入（默认行为，也可不加任何参数）")
    ap.add_argument("--no-html", action="store_true", help="只生成 webp，不改写 HTML")
    ap.add_argument("--css", action="store_true", help="同时替换 CSS 背景图 url（无回退，慎用）")
    args = ap.parse_args()

    if args.root is None:
        here = os.path.dirname(os.path.abspath(__file__))
        args.root = os.path.normpath(os.path.join(here, ".."))

    images_dir = os.path.join(args.root, "images")
    if not os.path.isdir(images_dir):
        sys.exit(f"未找到 images 目录: {images_dir}")

    imgs = walk_images(images_dir)
    print(f"发现图片 {len(imgs)} 张 | quality={args.quality} | mode={'APPLY' if args.apply else 'DRY-RUN'}")
    print("-" * 60)

    plan = []
    for path in imgs:
        webp_path = os.path.splitext(path)[0] + ".webp"
        plan.append((path, webp_path))

    if not args.no_html:
        html_files = []
        for dp, _, fns in os.walk(args.root):
            # 跳过备份/输出目录
            if "_optimized_backup" in dp or "node_modules" in dp:
                continue
            for fn in fns:
                if fn.lower().endswith(".html"):
                    html_files.append(os.path.join(dp, fn))
        print(f"将扫描并改写 HTML 文件 {len(html_files)} 个")

    print("-" * 60)
    print("执行计划预览：" if not args.apply else "开始执行：")
    for path, webp_path in plan[:10]:
        print(f"  + {os.path.relpath(webp_path, args.root)}  (from {os.path.relpath(path, args.root)})")
    if len(plan) > 10:
        print(f"  ... 共 {len(plan)} 个")

    if not args.apply:
        print("\n[DRY-RUN] 未做任何修改。加 --apply 真正执行。")
        return

    # 真正执行
    for path, webp_path in plan:
        data = gen_webp(path, args.quality)
        with open(webp_path, "wb") as f:
            f.write(data)
    print(f"已生成 {len(plan)} 个 .webp 文件")

    if args.no_html:
        return

    # 改写 HTML
    changed = 0
    for hpath in html_files:
        with open(hpath, "r", encoding="utf-8") as f:
            html = f.read()

        def repl(m):
            tag, src = m.group(1), m.group(2)
            # 仅处理本地相对路径的 jpg/jpeg（排除 http/ data/ 已 webp）
            if src.lower().startswith(("http", "data:", "//")):
                return tag
            base, ext = os.path.splitext(src)
            if ext.lower() not in (".jpg", ".jpeg"):
                return tag
            webp_src = base + ".webp"
            # 保持原 img 标签，仅在外层包 picture
            return f'<picture>\n  <source srcset="{webp_src}" type="image/webp">\n  {tag}\n</picture>'

        new_html = HTML_RE.sub(repl, html)
        if args.css:
            new_html = re.sub(r'url\((["\']?)([^)\'"]+\.jpe?g)(\1)\)',
                              lambda m: f'url({m.group(1)}{os.path.splitext(m.group(2))[0]}.webp{m.group(1)})',
                              new_html, flags=re.IGNORECASE)
        if new_html != html:
            with open(hpath, "w", encoding="utf-8") as f:
                f.write(new_html)
            changed += 1
            print(f"  改写 HTML: {os.path.relpath(hpath, args.root)}")

    print(f"完成。改写 HTML {changed} 个，生成 WebP {len(plan)} 个。")
    print("提示：上线前请本地预览，确认 <picture> 回退正常、WebP 显示无误。")


if __name__ == "__main__":
    main()
