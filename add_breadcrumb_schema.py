#!/usr/bin/env python3
"""
P0: 为工具页面、分类页面、博客页面添加 BreadcrumbList schema.org 结构化数据
"""
import os
import re
import json
from pathlib import Path

ROOT = Path("/workspace")
SITE_BASE = "https://www.zlbox.site"

# 面包屑配置：(URL路径, 显示名称)
BREADCRUMB_CONFIG = {
    # 首页不需要面包屑

    # 工具页面的面包屑
    "tools/calculator/": [
        ("https://www.zlbox.site/", "Home"),
        ("https://www.zlbox.site/categories/calculator.html", "Calculator Tools"),
    ],
    "tools/generator/": [
        ("https://www.zlbox.site/", "Home"),
        ("https://www.zlbox.site/categories/generator.html", "Generator Tools"),
    ],
    "tools/image/": [
        ("https://www.zlbox.site/", "Home"),
        ("https://www.zlbox.site/categories/image.html", "Image Tools"),
    ],
    "tools/pdf/": [
        ("https://www.zlbox.site/", "Home"),
        ("https://www.zlbox.site/categories/pdf.html", "PDF Tools"),
    ],
    "tools/text/": [
        ("https://www.zlbox.site/", "Home"),
        ("https://www.zlbox.site/categories/text.html", "Text Tools"),
    ],

    # 分类页面的面包屑
    "categories/calculator.html": [
        ("https://www.zlbox.site/", "Home"),
        ("https://www.zlbox.site/tools/index.html", "All Tools"),
    ],
    "categories/generator.html": [
        ("https://www.zlbox.site/", "Home"),
        ("https://www.zlbox.site/tools/index.html", "All Tools"),
    ],
    "categories/image.html": [
        ("https://www.zlbox.site/", "Home"),
        ("https://www.zlbox.site/tools/index.html", "All Tools"),
    ],
    "categories/pdf.html": [
        ("https://www.zlbox.site/", "Home"),
        ("https://www.zlbox.site/tools/index.html", "All Tools"),
    ],
    "categories/text.html": [
        ("https://www.zlbox.site/", "Home"),
        ("https://www.zlbox.site/tools/index.html", "All Tools"),
    ],

    # 博客页面的面包屑
    "blog/": [
        ("https://www.zlbox.site/", "Home"),
        ("https://www.zlbox.site/blog/index.html", "Blog"),
    ],
}

# 工具名映射（从 URL 文件名到显示名）
TOOL_NAME_MAP = {
    "age-calculator.html": "Age Calculator",
    "basic-calculator.html": "Basic Calculator",
    "bmi-calculator.html": "BMI Calculator",
    "loan-calculator.html": "Loan Calculator",
    "percentage-calculator.html": "Percentage Calculator",
    "scientific-calculator.html": "Scientific Calculator",
    "unit-converter.html": "Unit Converter",
    "hash-generator.html": "Hash Generator",
    "password-generator.html": "Password Generator",
    "pomodoro-timer.html": "Pomodoro Timer",
    "qr-code-generator.html": "QR Code Generator",
    "qr-code-scanner.html": "QR Code Scanner",
    "random-number-generator.html": "Random Number Generator",
    "uuid-generator.html": "UUID Generator",
    "what-is-my-ip.html": "What Is My IP",
    "background-remover.html": "Background Remover",
    "color-converter.html": "Color Converter",
    "color-picker.html": "Color Picker",
    "image-compressor.html": "Image Compressor",
    "image-converter.html": "Image Converter",
    "image-resizer.html": "Image Resizer",
    "compress-pdf.html": "Compress PDF",
    "jpg-to-pdf.html": "JPG to PDF",
    "merge-pdf.html": "Merge PDF",
    "split-pdf.html": "Split PDF",
    "base64.html": "Base64 Encoder/Decoder",
    "case-converter.html": "Case Converter",
    "csv-to-json.html": "CSV to JSON",
    "html-encoder.html": "HTML Encoder",
    "html-formatter.html": "HTML Formatter",
    "json-formatter.html": "JSON Formatter",
    "lorem-ipsum.html": "Lorem Ipsum Generator",
    "number-base-converter.html": "Number Base Converter",
    "remove-duplicates.html": "Remove Duplicates",
    "sql-formatter.html": "SQL Formatter",
    "url-encoder.html": "URL Encoder/Decoder",
    "word-counter.html": "Word Counter",
}


def build_breadcrumb_json(items, page_name=None):
    """构建 BreadcrumbList JSON-LD"""
    item_list = []
    for i, (url, name) in enumerate(items, 1):
        item = {
            "@type": "ListItem",
            "position": i,
            "name": name,
            "item": url
        }
        item_list.append(item)

    # 最后一页（当前页面）不需要完整 item URL
    if page_name:
        item_list[-1]["item"] = None  # 清除，Google 会用当前 URL

    data = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": item_list
    }

    return json.dumps(data, ensure_ascii=False)


def build_breadcrumb_html(items, page_name):
    """构建面包屑 HTML（用于替换现有的面包屑 div）"""
    crumbs = []
    for url, name in items:
        crumbs.append(f'<a href="{url}">{name}</a>')
    crumbs.append(page_name)

    separator = ' <span aria-hidden="true">&rsaquo;</span> '
    html = '<div class="breadcrumb" aria-label="Breadcrumb">' + separator.join(crumbs) + '</div>'
    return html


def process_breadcrumb_pages():
    count = 0

    for html_file in sorted(ROOT.rglob("*.html")):
        rel = str(html_file.relative_to(ROOT))

        # 跳过首页、工具列表页、信息页
        if rel in ("index.html", "tools/index.html", "about.html", "privacy.html",
                   "contact.html", "disclaimer.html", "blog/index.html",
                   "google4bd1e08685667667.html"):
            continue
        if rel.startswith("_") or rel.startswith("pages/"):
            continue

        html = html_file.read_text(encoding="utf-8")
        modified = False

        # 1. 确定这个页面属于哪个分类
        breadcrumb_items = None
        page_name = None

        # 检查是否在某个工具目录下
        for prefix, items in BREADCRUMB_CONFIG.items():
            if prefix.endswith("/") and rel.startswith(prefix):
                breadcrumb_items = list(items)
                # 获取工具名
                filename = os.path.basename(rel)
                page_name = TOOL_NAME_MAP.get(filename, filename.replace(".html", "").replace("-", " ").title())
                break
            elif rel == prefix:
                breadcrumb_items = list(items)
                page_name = rel.split("/")[-1].replace(".html", "").replace("-", " ").title()
                break

        if breadcrumb_items and page_name:
            # 构建 JSON-LD
            bc_json = build_breadcrumb_json(breadcrumb_items, page_name)

            # 检查是否已有 BreadcrumbList schema
            if '"@type": "BreadcrumbList"' not in html:
                # 添加到 </head> 前
                head_end = html.find("</head>")
                if head_end != -1:
                    schema_tag = f'\n  <script type="application/ld+json">{bc_json}</script>\n'
                    html = html[:head_end] + schema_tag + html[head_end:]
                    modified = True

        if modified:
            html_file.write_text(html, encoding="utf-8")
            count += 1
            print(f"  ✅ {rel}")

    print(f"\n共更新 {count} 个页面的面包屑 schema")


if __name__ == "__main__":
    print("=" * 60)
    print("添加 BreadcrumbList schema...")
    print("=" * 60)
    process_breadcrumb_pages()