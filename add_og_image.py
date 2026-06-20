#!/usr/bin/env python3
"""
P0: 为所有 HTML 页面添加:
1. og:image + og:image:width + og:image:height meta tags
2. Twitter Card tags (twitter:card, twitter:title, twitter:description, twitter:image)
3. 替换已有的 og:image 如果存在

目标图片URL: https://www.zlbox.site/og-image.png
"""
import os
import re
from pathlib import Path

ROOT = Path("/workspace")
SITE_BASE = "https://www.zlbox.site"
OG_IMAGE_URL = f"{SITE_BASE}/og-image.png"

# 跳过这些文件
SKIP_FILES = {"google4bd1e08685667667.html"}

def get_title_and_desc(filepath, html):
    """从页面提取 title 和 description"""
    m = re.search(r'<title>([^<]+)</title>', html)
    title = m.group(1).strip() if m else "My Tool Lab"

    m = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', html)
    description = m.group(1).strip() if m else title

    # 清理标题中的 | My Tool Lab 后缀（Twitter card 用简化标题）
    short_title = re.sub(r'\s*[|–]\s*My Tool Lab\s*$', '', title).strip()

    return title, short_title, description


def add_og_image_and_twitter(html, filepath):
    """为单个页面添加 og:image 和 twitter card"""
    title, short_title, description = get_title_and_desc(filepath, html)

    # 新的 meta tags
    new_tags = f'''  <meta property="og:image" content="{OG_IMAGE_URL}" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{short_title}" />
  <meta name="twitter:description" content="{description}" />
  <meta name="twitter:image" content="{OG_IMAGE_URL}" />
'''

    # 检查是否已有 og:image，有则替换，没有则添加
    if 'property="og:image"' in html or "property='og:image'" in html:
        # 替换现有的 og:image 及其相关标签
        # 移除已有的 og:image, og:image:width, og:image:height
        html = re.sub(r'\s*<meta[^>]+property="og:image"[^>]*/?\>\s*\n?', '\n', html)
        html = re.sub(r'\s*<meta[^>]+property="og:image:width"[^>]*/?\>\s*\n?', '\n', html)
        html = re.sub(r'\s*<meta[^>]+property="og:image:height"[^>]*/?\>\s*\n?', '\n', html)
        # 移除已有的 twitter tags
        html = re.sub(r'\s*<meta[^>]+name="twitter:card"[^>]*/?\>\s*\n?', '\n', html)
        html = re.sub(r'\s*<meta[^>]+name="twitter:title"[^>]*/?\>\s*\n?', '\n', html)
        html = re.sub(r'\s*<meta[^>]+name="twitter:description"[^>]*/?\>\s*\n?', '\n', html)
        html = re.sub(r'\s*<meta[^>]+name="twitter:image"[^>]*/?\>\s*\n?', '\n', html)
        # 清理多余空行
        html = re.sub(r'\n{3,}', '\n\n', html)

    # 找到 </head> 并插入
    head_end = html.find("</head>")
    if head_end == -1:
        return False

    html = html[:head_end] + new_tags + "\n" + html[head_end:]
    return html


def process_all():
    count = 0
    for html_file in sorted(ROOT.rglob("*.html")):
        rel = str(html_file.relative_to(ROOT))
        if rel.startswith("_") or rel.startswith("pages/") or rel in SKIP_FILES:
            continue

        html = html_file.read_text(encoding="utf-8")
        result = add_og_image_and_twitter(html, html_file)
        if result:
            html_file.write_text(result, encoding="utf-8")
            count += 1
            print(f"  ✅ {rel}")

    print(f"\n共更新 {count} 个页面")


if __name__ == "__main__":
    print("=" * 60)
    print("添加 og:image + Twitter Card...")
    print("=" * 60)
    process_all()