#!/usr/bin/env python3
"""
P0: 为博客文章添加完善的 Article schema
添加: author, datePublished, dateModified, publisher, image
"""
import os
import re
import json
from datetime import datetime
from pathlib import Path

ROOT = Path("/workspace")
SITE_BASE = "https://www.zlbox.site"
SITE_NAME = "My Tool Lab"
TODAY = datetime.now().strftime("%Y-%m-%d")


BLOG_ARTICLES = {
    "age-calculator-uses.html": {
        "title": "Age Calculator Uses",
        "date": "2026-01-15",
        "image": f"{SITE_BASE}/og-image.png"
    },
    "batch-image-processing.html": {
        "title": "Batch Image Processing",
        "date": "2026-02-10",
        "image": f"{SITE_BASE}/og-image.png"
    },
    "color-design-basics.html": {
        "title": "Color Design Basics",
        "date": "2026-02-20",
        "image": f"{SITE_BASE}/og-image.png"
    },
    "data-privacy-tools.html": {
        "title": "Data Privacy Tools",
        "date": "2026-03-01",
        "image": f"{SITE_BASE}/og-image.png"
    },
    "how-to-compress-pdf.html": {
        "title": "How to Compress PDF",
        "date": "2025-12-10",
        "image": f"{SITE_BASE}/og-image.png"
    },
    "image-compression-guide.html": {
        "title": "Image Compression Guide",
        "date": "2026-01-20",
        "image": f"{SITE_BASE}/og-image.png"
    },
    "json-formatter-developers.html": {
        "title": "JSON Formatter for Developers",
        "date": "2025-11-15",
        "image": f"{SITE_BASE}/og-image.png"
    },
    "password-security.html": {
        "title": "Password Security Best Practices",
        "date": "2025-10-20",
        "image": f"{SITE_BASE}/og-image.png"
    },
    "pdf-tools-guide.html": {
        "title": "PDF Tools Guide",
        "date": "2025-09-10",
        "image": f"{SITE_BASE}/og-image.png"
    },
    "percent-calculator-everyday.html": {
        "title": "Percentage Calculator for Everyday Use",
        "date": "2026-01-05",
        "image": f"{SITE_BASE}/og-image.png"
    },
    "qr-code-business.html": {
        "title": "QR Codes for Business",
        "date": "2026-02-01",
        "image": f"{SITE_BASE}/og-image.png"
    },
    "qr-code-types.html": {
        "title": "Types of QR Codes",
        "date": "2026-02-15",
        "image": f"{SITE_BASE}/og-image.png"
    },
}


def enrich_article_schema(html, filepath, article_info):
    """为博客文章添加完整的 Article schema"""
    url = f"{SITE_BASE}/{filepath.relative_to(ROOT)}"
    title = article_info.get("title", "Article")
    date = article_info.get("date", TODAY)
    image = article_info.get("image", f"{SITE_BASE}/og-image.png")

    # 构建 Article schema
    article_schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": title,
        "url": url,
        "datePublished": date,
        "dateModified": date,
        "image": image,
        "author": {
            "@type": "Organization",
            "name": SITE_NAME,
            "url": SITE_BASE
        },
        "publisher": {
            "@type": "Organization",
            "name": SITE_NAME,
            "url": SITE_BASE,
            "logo": {
                "@type": "ImageObject",
                "url": f"{SITE_BASE}/og-image.png"
            }
        },
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": url
        }
    }

    # 检查是否已有 Article schema
    existing = re.search(r'"@type":\s*"Article"', html)

    # 移除旧的 Article schema（如果有多个）
    html = re.sub(r'\s*<script[^>]*type="application/ld\+json"[^>]*>\s*\{[^}]*?"@type":\s*"Article"[^}]*\}[^<]*</script>\s*\n?', '\n', html, flags=re.DOTALL)

    # 构建新 tag
    json_str = json.dumps(article_schema, ensure_ascii=False, indent=2)
    new_tag = f'\n  <script type="application/ld+json">\n{json_str}\n  </script>\n'

    head_end = html.find("</head>")
    if head_end != -1:
        html = html[:head_end] + new_tag + html[head_end:]

    return html


def process_blog_articles():
    count = 0
    for filename, info in BLOG_ARTICLES.items():
        filepath = ROOT / "blog" / filename
        if not filepath.exists():
            print(f"  ⚠️  跳过: {filepath} 不存在")
            continue

        html = filepath.read_text(encoding="utf-8")
        new_html = enrich_article_schema(html, filepath, info)
        filepath.write_text(new_html, encoding="utf-8")
        count += 1
        print(f"  ✅ blog/{filename}")

    print(f"\n共更新 {count} 篇博客文章 schema")


def main():
    print("=" * 60)
    print("完善博客 Article schema...")
    print("=" * 60)
    process_blog_articles()
    print("\n完成！")


if __name__ == "__main__":
    main()