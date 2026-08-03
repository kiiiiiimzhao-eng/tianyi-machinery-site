#!/usr/bin/env python3
"""统一全站域名到 tianyimachine.com（apex，无 www）。
- www.tianyi-machinery.com -> tianyimachine.com
- kim@tianyi-machinery.com -> kim@tianyimachine.com
跳过 audit/ 目录（历史报告，不作为线上内容）。
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {"audit", "tools", "images", "_optimized_backup"}

replacements = [
    ("www.tianyi-machinery.com", "tianyimachine.com"),
    ("kim@tianyi-machinery.com", "kim@tianyimachine.com"),
]

total_files = 0
total_repl = 0
changed_files = []

for dirpath, dirnames, filenames in os.walk(ROOT):
    # 原地修改 dirnames 以跳过
    dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
    for fn in filenames:
        if not fn.endswith(".html"):
            continue
        path = os.path.join(dirpath, fn)
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        new_content = content
        file_repl = 0
        for old, new in replacements:
            c = new_content.count(old)
            if c:
                new_content = new_content.replace(old, new)
                file_repl += c
        if file_repl:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_content)
            total_files += 1
            total_repl += file_repl
            changed_files.append((os.path.relpath(path, ROOT), file_repl))

print(f"修改文件数: {total_files}")
print(f"替换总数:   {total_repl}")
for rel, n in changed_files:
    print(f"  {rel}: {n} 处")
