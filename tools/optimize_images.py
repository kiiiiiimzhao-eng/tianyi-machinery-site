#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tianyi Machinery 图片批量压缩工具
=================================

功能：
  1. 递归扫描指定目录下的所有 JPG/JPEG 图片（含 .JPG 大写扩展名）。
  2. 自动转为 RGB（处理 CMYK / P / RGBA / L 等模式，避免保存 JPEG 报错）。
  3. 若图片最长边超过 --max-size，则等比缩放到最长边 = max-size（不拉伸短边）。
  4. 以 quality 压缩后重新保存为 JPEG（optimize + progressive）。
  5. 仅当压缩后体积 <= 原图 98% 时才覆盖，否则保留原图（避免“越压越大”）。
  6. 可选 --backup：先把原图备份到 <root>/_optimized_backup/ 再覆盖。

用法：
  # 预览（不改动任何文件，只打印可节省量）
  python optimize_images.py --dry-run

  # 实际压缩（带备份）
  python optimize_images.py --backup

  # 自定义参数
  python optimize_images.py --root ../images --max-size 1400 --quality 80 --backup

依赖：Pillow
  pip install Pillow
"""

import argparse
import io
import os
import shutil
import sys

try:
    from PIL import Image
except ImportError:
    sys.exit("缺少 Pillow，请先执行: pip install Pillow")

# 支持的扩展名（大小写都处理）
EXTENSIONS = (".jpg", ".jpeg", ".JPG", ".JPEG")


def collect_images(root):
    files = []
    for dirpath, _, filenames in os.walk(root):
        for fn in filenames:
            if fn.lower().endswith((".jpg", ".jpeg")):
                files.append(os.path.join(dirpath, fn))
    return sorted(files)


def optimize_one(path, max_size, quality):
    """返回 (old_bytes, new_bytes, status)；status: 'saved' | 'skipped' | 'error'
    new_bytes 为编码后的字节（saved 时有效），调用方直接写入，避免二次打开文件。"""
    try:
        with Image.open(path) as img:
            # 转为 RGB（JPEG 不支持透明/CMYK）
            if img.mode not in ("RGB",):
                img = img.convert("RGB")
            # 等比缩放
            if max(img.size) > max_size:
                img.thumbnail((max_size, max_size), Image.LANCZOS)

            buf = io.BytesIO()
            img.save(buf, format="JPEG", quality=quality, optimize=True, progressive=True)
            new_data = buf.getvalue()

        old_size = os.path.getsize(path)
        # 只有明显变小才覆盖
        if len(new_data) < old_size * 0.98:
            return old_size, new_data, "saved"
        else:
            return old_size, None, "skipped"
    except Exception as e:  # noqa
        return (os.path.getsize(path) if os.path.exists(path) else 0), None, f"error:{e}"


def main():
    parser = argparse.ArgumentParser(description="Tianyi 图片批量压缩")
    parser.add_argument("--root", default=None, help="扫描根目录（默认：脚本上两级目录的 images/，即项目 images 文件夹）")
    parser.add_argument("--max-size", type=int, default=1600, help="最长边最大像素（默认 1600）")
    parser.add_argument("--quality", type=int, default=82, help="JPEG 质量（默认 82）")
    parser.add_argument("--backup", action="store_true", help="覆盖前备份原图到 _optimized_backup/")
    parser.add_argument("--dry-run", action="store_true", help="只统计，不修改文件")
    args = parser.parse_args()

    # 默认 root = 项目 images 目录（脚本位于 <project>/tools/）
    if args.root is None:
        here = os.path.dirname(os.path.abspath(__file__))
        args.root = os.path.normpath(os.path.join(here, "..", "images"))

    if not os.path.isdir(args.root):
        sys.exit(f"目录不存在: {args.root}")

    files = collect_images(args.root)
    if not files:
        print("未发现任何 JPG/JPEG 图片。")
        return

    print(f"扫描目录: {args.root}")
    print(f"图片数量: {len(files)} | max-size={args.max_size}px | quality={args.quality} | "
          f"{'DRY-RUN(不写入)' if args.dry_run else ('备份模式' if args.backup else '直接覆盖')}")
    print("-" * 64)

    total_old = 0
    total_new = 0
    saved = skipped = errors = 0

    for path in files:
        old, new_data, status = optimize_one(path, args.max_size, args.quality)
        total_old += old
        if status == "saved":
            saved += 1
            total_new += len(new_data)
            if not args.dry_run:
                if args.backup:
                    rel = os.path.relpath(path, args.root)
                    bak = os.path.join(args.root, "_optimized_backup", rel)
                    os.makedirs(os.path.dirname(bak), exist_ok=True)
                    if not os.path.exists(bak):
                        shutil.copy2(path, bak)
                with open(path, "wb") as f:
                    f.write(new_data)
            print(f"  [压缩] {os.path.relpath(path, args.root):55s} {old/1024:8.1f}KB -> {len(new_data)/1024:8.1f}KB")
        elif status == "skipped":
            skipped += 1
            total_new += old
        else:
            errors += 1
            print(f"  [失败] {os.path.relpath(path, args.root)} -> {status}")

    print("-" * 64)
    saved_kb = (total_old - total_new) / 1024
    pct = (1 - total_new / total_old) * 100 if total_old else 0
    print(f"总计: 原图 {total_old/1024/1024:.2f}MB -> 现图 {total_new/1024/1024:.2f}MB")
    print(f"节省: {saved_kb/1024:.2f}MB ({pct:.1f}%) | 已压缩 {saved} | 已跳过 {skipped} | 失败 {errors}")
    if args.dry_run:
        print("（DRY-RUN 模式：未做任何修改。去掉 --dry-run 并加 --backup 再执行）")


if __name__ == "__main__":
    main()
