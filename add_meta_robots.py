#!/usr/bin/env python3
"""
批量为所有页面添加 meta robots 标签
"""
import re
from pathlib import Path

ROOT = Path("/workspace")
SKIP_FILES = {"google4bd1e08685667667.html", "404.html"}


def add_robots(html):
    if 'name="robots"' in html:
        return False
    
    head_end = html.find("</head>")
    if head_end == -1:
        return False
    
    new_tag = '\n  <meta name="robots" content="index, follow" />'
    html = html[:head_end] + new_tag + html[head_end:]
    return html


def process_all():
    count = 0
    for html_file in sorted(ROOT.rglob("*.html")):
        rel = str(html_file.relative_to(ROOT))
        if rel.startswith("_") or rel.startswith("pages/") or rel in SKIP_FILES:
            continue
        
        content = html_file.read_text(encoding="utf-8")
        result = add_robots(content)
        if result:
            html_file.write_text(result, encoding="utf-8")
            count += 1
            print(f"  ✅ {rel}")
    
    print(f"\n共更新 {count} 个页面")


if __name__ == "__main__":
    print("=" * 60)
    print("添加 meta robots...")
    print("=" * 60)
    process_all()