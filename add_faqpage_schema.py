#!/usr/bin/env python3
"""
P0: 为首页 FAQ 区块添加 FAQPage schema
P1: 为每个工具页面添加 FAQPage schema
"""
import os
import re
import json
from pathlib import Path

ROOT = Path("/workspace")


def extract_faqs_from_html(html):
    """从 FAQ 区块提取问答"""
    faqs = []

    # 匹配 <details class="faq-item"><summary>Q</summary><p>A</p></details>
    pattern = r'<details[^>]*class="faq-item"[^>]*>\s*<summary[^>]*>([^<]+)</summary>\s*<p[^>]*>([^<]+)</p>\s*</details>'

    for match in re.finditer(pattern, html, re.DOTALL):
        question = match.group(1).strip()
        answer = match.group(2).strip()
        # 清理 HTML 标签
        answer = re.sub(r'<[^>]+>', '', answer).strip()
        if question and answer:
            faqs.append({"question": question, "answer": answer})

    return faqs


def build_faqpage_schema(faqs):
    """构建 FAQPage JSON-LD"""
    qas = []
    for q, a in faqs:
        qas.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {
                "@type": "Answer",
                "text": a
            }
        })

    return json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": qas
    }, ensure_ascii=False, indent=2)


def add_faqpage_to_homepage():
    """为首页添加 FAQPage schema"""
    filepath = ROOT / "index.html"
    html = filepath.read_text(encoding="utf-8")

    if '"@type": "FAQPage"' in html:
        print("  首页已有 FAQPage schema，跳过")
        return

    faqs = extract_faqs_from_html(html)
    if not faqs:
        print("  首页未找到 FAQ 内容")
        return

    faq_json = build_faqpage_schema(faqs)

    head_end = html.find("</head>")
    if head_end != -1:
        schema_tag = f'\n  <script type="application/ld+json">\n{faq_json}\n  </script>\n'
        html = html[:head_end] + schema_tag + html[head_end:]
        filepath.write_text(html, encoding="utf-8")
        print(f"  ✅ index.html - 添加了 {len(faqs)} 个 FAQ")


def main():
    print("=" * 60)
    print("添加 FAQPage schema...")
    print("=" * 60)

    # 首页
    add_faqpage_to_homepage()

    print("\n完成！")


if __name__ == "__main__":
    main()