#!/usr/bin/env python3
"""
SEO 全面修复脚本：
1. 添加 og:image + twitter:card 到所有页面
2. 添加 meta robots 到所有页面
3. 添加 favicon 引用到所有页面
4. 添加 JSON-LD schema 到所有页面
5. 添加 GA4 到缺失页面
6. 添加 AdSense 到缺失页面
7. 创建 404.html
8. 生成完整的 sitemap.xml
"""
import os
import re
import json
from datetime import date
from pathlib import Path

ROOT = Path("/workspace")
SITE_BASE = "https://www.zlbox.site"
OG_IMAGE_URL = f"{SITE_BASE}/og-image.png"
GA4_ID = "G-9V6L0Z956X"
ADSENSE_ID = "ca-pub-5420550088713746"
TODAY = str(date.today())

SKIP_FILES = {"google4bd1e08685667667.html"}

# 工具页面信息
TOOL_INFO = {
    # Calculator
    "tools/calculator/age-calculator.html": {"name": "Age Calculator", "desc": "Calculate exact age from birth date"},
    "tools/calculator/basic-calculator.html": {"name": "Basic Calculator", "desc": "Simple arithmetic calculator"},
    "tools/calculator/bmi-calculator.html": {"name": "BMI Calculator", "desc": "Body mass index calculator"},
    "tools/calculator/loan-calculator.html": {"name": "Loan Calculator", "desc": "Calculate monthly loan payments"},
    "tools/calculator/percentage-calculator.html": {"name": "Percentage Calculator", "desc": "Calculate percentages easily"},
    "tools/calculator/scientific-calculator.html": {"name": "Scientific Calculator", "desc": "Advanced math calculator"},
    "tools/calculator/unit-converter.html": {"name": "Unit Converter", "desc": "Convert between units"},
    # Generator
    "tools/generator/hash-generator.html": {"name": "Hash Generator", "desc": "MD5, SHA-1, SHA-256 hash generator"},
    "tools/generator/password-generator.html": {"name": "Password Generator", "desc": "Create strong random passwords"},
    "tools/generator/pomodoro-timer.html": {"name": "Pomodoro Timer", "desc": "Focus timer for productivity"},
    "tools/generator/qr-code-generator.html": {"name": "QR Code Generator", "desc": "Generate QR codes instantly"},
    "tools/generator/qr-code-scanner.html": {"name": "QR Code Scanner", "desc": "Scan QR codes from image"},
    "tools/generator/random-number-generator.html": {"name": "Random Number Generator", "desc": "Generate random numbers"},
    "tools/generator/uuid-generator.html": {"name": "UUID Generator", "desc": "Generate unique UUIDs"},
    "tools/generator/what-is-my-ip.html": {"name": "What Is My IP", "desc": "Show your public IP address"},
    # Image
    "tools/image/background-remover.html": {"name": "Background Remover", "desc": "Remove image background"},
    "tools/image/color-converter.html": {"name": "Color Converter", "desc": "Convert colors between formats"},
    "tools/image/color-picker.html": {"name": "Color Picker", "desc": "Pick and adjust colors"},
    "tools/image/image-compressor.html": {"name": "Image Compressor", "desc": "Compress images online"},
    "tools/image/image-converter.html": {"name": "Image Converter", "desc": "Convert image formats"},
    "tools/image/image-resizer.html": {"name": "Image Resizer", "desc": "Resize images to any size"},
    # PDF
    "tools/pdf/compress-pdf.html": {"name": "Compress PDF", "desc": "Reduce PDF file size"},
    "tools/pdf/jpg-to-pdf.html": {"name": "JPG to PDF", "desc": "Convert images to PDF"},
    "tools/pdf/merge-pdf.html": {"name": "Merge PDF", "desc": "Combine multiple PDFs"},
    "tools/pdf/split-pdf.html": {"name": "Split PDF", "desc": "Extract pages from PDF"},
    # Text
    "tools/text/base64.html": {"name": "Base64 Encoder", "desc": "Encode and decode Base64"},
    "tools/text/case-converter.html": {"name": "Case Converter", "desc": "Convert text case"},
    "tools/text/csv-to-json.html": {"name": "CSV to JSON", "desc": "Convert CSV to JSON"},
    "tools/text/html-encoder.html": {"name": "HTML Encoder", "desc": "Encode HTML entities"},
    "tools/text/html-formatter.html": {"name": "HTML Formatter", "desc": "Format HTML code"},
    "tools/text/json-formatter.html": {"name": "JSON Formatter", "desc": "Format and validate JSON"},
    "tools/text/lorem-ipsum.html": {"name": "Lorem Ipsum", "desc": "Generate placeholder text"},
    "tools/text/number-base-converter.html": {"name": "Number Base Converter", "desc": "Convert number bases"},
    "tools/text/remove-duplicates.html": {"name": "Remove Duplicates", "desc": "Remove duplicate lines"},
    "tools/text/sql-formatter.html": {"name": "SQL Formatter", "desc": "Format SQL queries"},
    "tools/text/url-encoder.html": {"name": "URL Encoder", "desc": "Encode URL strings"},
    "tools/text/word-counter.html": {"name": "Word Counter", "desc": "Count words and characters"},
}

# 分类页面
CATEGORY_INFO = {
    "categories/calculator.html": {"name": "Calculator Tools", "desc": "Online calculator tools"},
    "categories/generator.html": {"name": "Generator Tools", "desc": "Online generator tools"},
    "categories/image.html": {"name": "Image Tools", "desc": "Online image tools"},
    "categories/pdf.html": {"name": "PDF Tools", "desc": "Online PDF tools"},
    "categories/text.html": {"name": "Text Tools", "desc": "Online text tools"},
}

# 博客页面
BLOG_INFO = {
    "blog/age-calculator-uses.html": {"name": "Age Calculator Uses", "desc": "How to use age calculator"},
    "blog/batch-image-processing.html": {"name": "Batch Image Processing", "desc": "Process multiple images"},
    "blog/color-design-basics.html": {"name": "Color Design Basics", "desc": "Color theory basics"},
    "blog/data-privacy-tools.html": {"name": "Data Privacy Tools", "desc": "Protect your data"},
    "blog/how-to-compress-pdf.html": {"name": "How to Compress PDF", "desc": "PDF compression guide"},
    "blog/image-compression-guide.html": {"name": "Image Compression Guide", "desc": "Image compression tips"},
    "blog/json-formatter-developers.html": {"name": "JSON Formatter for Developers", "desc": "JSON formatting tips"},
    "blog/password-security.html": {"name": "Password Security", "desc": "Password best practices"},
    "blog/pdf-tools-guide.html": {"name": "PDF Tools Guide", "desc": "Complete PDF guide"},
    "blog/percent-calculator-everyday.html": {"name": "Percentage Calculator for Everyday", "desc": "Everyday percentage calculations"},
    "blog/qr-code-business.html": {"name": "QR Codes for Business", "desc": "Business QR code uses"},
    "blog/qr-code-types.html": {"name": "Types of QR Codes", "desc": "QR code varieties"},
}


def get_page_info(filepath):
    """获取页面信息"""
    rel = str(filepath.relative_to(ROOT))
    
    if rel == "index.html":
        return {"name": "My Tool Lab", "desc": "Free online tools for everyone", "type": "WebSite"}
    if rel == "tools/index.html":
        return {"name": "All Tools", "desc": "Browse all online tools", "type": "WebPage"}
    if rel in TOOL_INFO:
        info = TOOL_INFO[rel]
        return {**info, "type": "WebApplication"}
    if rel in CATEGORY_INFO:
        info = CATEGORY_INFO[rel]
        return {**info, "type": "WebPage"}
    if rel in BLOG_INFO:
        info = BLOG_INFO[rel]
        return {**info, "type": "Article"}
    if rel in ("about.html", "privacy.html", "contact.html", "disclaimer.html"):
        return {"name": rel.replace(".html", "").capitalize(), "desc": f"{rel.replace('.html', '').capitalize()} page", "type": "WebPage"}
    
    return {"name": "My Tool Lab", "desc": "Free online tools", "type": "WebPage"}


def build_og_tags(name, desc, url):
    """构建 OG tags"""
    return f'''
  <meta property="og:image" content="{OG_IMAGE_URL}" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{name}" />
  <meta name="twitter:description" content="{desc}" />
  <meta name="twitter:image" content="{OG_IMAGE_URL}" />'''


def build_favicon_link():
    return '\n  <link rel="icon" type="image/svg+xml" href="/favicon.svg" />'


def build_meta_robots():
    return '\n  <meta name="robots" content="index, follow" />'


def build_schema_jsonld(page_type, name, desc, url):
    """构建 JSON-LD"""
    if page_type == "WebApplication":
        data = {
            "@context": "https://schema.org",
            "@type": "WebApplication",
            "name": name,
            "description": desc,
            "url": url,
            "applicationCategory": "UtilityApplication",
            "operatingSystem": "Any",
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}
        }
    elif page_type == "Article":
        data = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": name,
            "description": desc,
            "url": url,
            "author": {"@type": "Organization", "name": "My Tool Lab"},
            "publisher": {"@type": "Organization", "name": "My Tool Lab"},
            "datePublished": TODAY,
            "dateModified": TODAY
        }
    elif page_type == "WebSite":
        data = {
            "@context": "https://schema.org",
            "@type": "WebSite",
            "name": name,
            "url": url,
            "description": desc
        }
    else:
        data = {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": name,
            "description": desc,
            "url": url
        }
    
    return f'\n  <script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'


def build_ga4_script():
    return f'''
  <script async src="https://www.googletagmanager.com/gtag/js?id={GA4_ID}"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','{GA4_ID}');</script>'''


def build_adsense_script():
    return f'''
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_ID}" crossorigin="anonymous"></script>'''


def fix_html_file(filepath):
    """修复单个 HTML 文件"""
    rel = str(filepath.relative_to(ROOT))
    if rel in SKIP_FILES or rel.startswith("_") or rel.startswith("pages/"):
        return False
    
    html = filepath.read_text(encoding="utf-8")
    original = html
    
    info = get_page_info(filepath)
    url = f"{SITE_BASE}/{rel}"
    
    # 1. 添加 og:image + twitter:card
    if 'property="og:image"' not in html:
        og_tags = build_og_tags(info["name"], info["desc"], url)
        head_end = html.find("</head>")
        if head_end != -1:
            html = html[:head_end] + og_tags + "\n" + html[head_end:]
    
    # 2. 添加 favicon
    if 'rel="icon"' not in html:
        favicon = build_favicon_link()
        head_end = html.find("</head>")
        if head_end != -1:
            html = html[:head_end] + favicon + "\n" + html[head_end:]
    
    # 3. 添加 meta robots
    if 'name="robots"' not in html:
        robots = build_meta_robots()
        head_end = html.find("</head>")
        if head_end != -1:
            html = html[:head_end] + robots + "\n" + html[head_end:]
    
    # 4. 添加 JSON-LD schema
    if 'application/ld+json' not in html:
        schema = build_schema_jsonld(info["type"], info["name"], info["desc"], url)
        head_end = html.find("</head>")
        if head_end != -1:
            html = html[:head_end] + schema + "\n" + html[head_end:]
    
    # 5. 添加 GA4
    if GA4_ID not in html:
        ga4 = build_ga4_script()
        head_end = html.find("</head>")
        if head_end != -1:
            html = html[:head_end] + ga4 + "\n" + html[head_end:]
    
    # 6. 添加 AdSense
    if ADSENSE_ID not in html:
        adsense = build_adsense_script()
        head_end = html.find("</head>")
        if head_end != -1:
            html = html[:head_end] + adsense + "\n" + html[head_end:]
    
    if html != original:
        filepath.write_text(html, encoding="utf-8")
        return True
    return False


def create_404_page():
    """创建 404.html"""
    content = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>404 – Page Not Found | My Tool Lab</title>
  <meta name="description" content="The page you are looking for does not exist. Browse our free online tools instead." />
  <meta name="robots" content="noindex, nofollow" />
  <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
  <meta property="og:title" content="404 – Page Not Found | My Tool Lab" />
  <meta property="og:description" content="The page you are looking for does not exist." />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="https://www.zlbox.site/404.html" />
  <meta property="og:image" content="https://www.zlbox.site/og-image.png" />
  <meta name="twitter:card" content="summary_large_image" />
  <script type="application/ld+json">{"@context":"https://schema.org","@type":"WebPage","name":"404 – Page Not Found","url":"https://www.zlbox.site/404.html"}</script>
  <style>
    :root{--brand:#2563eb;--text:#0f172a;--muted:#64748b;--border:#e2e8f0;--bg:#fff;--bg-subtle:#f8fafc}
    body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;background:var(--bg-subtle);color:var(--text);min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:24px}
    .error-code{font-size:8rem;font-weight:900;color:var(--brand);opacity:.15;line-height:1}
    .error-title{font-size:2rem;font-weight:700;margin:12px 0}
    .error-desc{font-size:1rem;color:var(--muted);max-width:400px;text-align:center;margin-bottom:24px}
    .btn{display:inline-flex;padding:12px 24px;border-radius:8px;font-weight:600;text-decoration:none;transition:all .2s}
    .btn-primary{background:var(--brand);color:#fff}
    .btn-primary:hover{background:#1d4ed8}
    .quick-links{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;max-width:500px;margin-top:24px}
    .ql-card{background:var(--bg);border:1px solid var(--border);border-radius:8px;padding:12px;text-decoration:none;transition:all .2s}
    .ql-card:hover{border-color:var(--brand);box-shadow:0 2px 8px rgba(0,0,0,.1)}
    .ql-card h3{font-size:.9rem;font-weight:600;color:var(--text);margin-bottom:4px}
    .ql-card p{font-size:.75rem;color:var(--muted)}
    @media(max-width:480px){.error-code{font-size:5rem}.quick-links{grid-template-columns:1fr}}
  </style>
</head>
<body>
  <div class="error-code">404</div>
  <h1 class="error-title">Page Not Found</h1>
  <p class="error-desc">The page you're looking for has moved or doesn't exist. Try one of our popular tools below.</p>
  <a href="/" class="btn btn-primary">← Back to Home</a>
  <div class="quick-links">
    <a href="/tools/text/word-counter.html" class="ql-card"><h3>📝 Word Counter</h3><p>Count words instantly</p></a>
    <a href="/tools/generator/password-generator.html" class="ql-card"><h3>🔐 Password Generator</h3><p>Create strong passwords</p></a>
    <a href="/tools/pdf/compress-pdf.html" class="ql-card"><h3>📄 Compress PDF</h3><p>Reduce PDF size</p></a>
    <a href="/tools/generator/qr-code-generator.html" class="ql-card"><h3>📱 QR Generator</h3><p>Create QR codes</p></a>
  </div>
</body>
</html>'''
    (ROOT / "404.html").write_text(content, encoding="utf-8")
    print("  ✅ 404.html created")


def generate_sitemap():
    """生成完整的 sitemap.xml"""
    urls = []
    
    # 首页
    urls.append({"url": f"{SITE_BASE}/", "priority": "1.0", "freq": "weekly"})
    
    # 工具索引
    urls.append({"url": f"{SITE_BASE}/tools/index.html", "priority": "0.9", "freq": "weekly"})
    
    # 分类页
    for cat in ["calculator", "generator", "image", "pdf", "text"]:
        urls.append({"url": f"{SITE_BASE}/categories/{cat}.html", "priority": "0.8", "freq": "weekly"})
    
    # 工具页
    for tool_path in sorted(TOOL_INFO.keys()):
        urls.append({"url": f"{SITE_BASE}/{tool_path}", "priority": "0.7", "freq": "monthly"})
    
    # 博客
    urls.append({"url": f"{SITE_BASE}/blog/index.html", "priority": "0.6", "freq": "weekly"})
    for blog_path in sorted(BLOG_INFO.keys()):
        urls.append({"url": f"{SITE_BASE}/{blog_path}", "priority": "0.6", "freq": "monthly"})
    
    # 信息页
    for page in ["about", "privacy", "contact", "disclaimer"]:
        urls.append({"url": f"{SITE_BASE}/{page}.html", "priority": "0.5", "freq": "yearly"})
    
    # 404
    urls.append({"url": f"{SITE_BASE}/404.html", "priority": "0.1", "freq": "yearly"})
    
    # 生成 XML
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u in urls:
        xml_content += f'  <url>\n    <loc>{u["url"]}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <changefreq>{u["freq"]}</changefreq>\n    <priority>{u["priority"]}</priority>\n  </url>\n'
    xml_content += '</urlset>\n'
    
    (ROOT / "sitemap.xml").write_text(xml_content, encoding="utf-8")
    print(f"  ✅ sitemap.xml generated ({len(urls)} URLs)")


def main():
    print("=" * 60)
    print("SEO 全面修复...")
    print("=" * 60)
    
    # 修复所有 HTML 文件
    count = 0
    for html_file in sorted(ROOT.rglob("*.html")):
        if fix_html_file(html_file):
            rel = str(html_file.relative_to(ROOT))
            count += 1
            print(f"  ✅ {rel}")
    
    print(f"\n修复了 {count} 个页面")
    
    # 创建 404
    create_404_page()
    
    # 生成 sitemap
    generate_sitemap()
    
    print("\n" + "=" * 60)
    print("完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()