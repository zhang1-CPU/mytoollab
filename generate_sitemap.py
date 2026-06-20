#!/usr/bin/env python3
"""
重新生成 sitemap.xml，确保正确的优先级排序：
1. 首页 /
2. tools/index.html
3. categories/*.html
4. tools/*/*.html (工具页面)
5. blog/*.html (博客页面)
6. about, privacy, contact, disclaimer
"""
import datetime

SITE_BASE = "https://www.zlbox.site"
today = datetime.date.today().isoformat()

# 按优先级分组定义
priority_groups = [
    # (paths, changefreq, priority)
    ([("index.html", "/")], "weekly", "1.0"),
    ([("tools/index.html", "/tools/index.html")], "weekly", "0.9"),
    ([
        ("categories/calculator.html", "/categories/calculator.html"),
        ("categories/generator.html", "/categories/generator.html"),
        ("categories/image.html", "/categories/image.html"),
        ("categories/pdf.html", "/categories/pdf.html"),
        ("categories/text.html", "/categories/text.html"),
    ], "weekly", "0.8"),
    ([
        # 工具页面 - 按类别排序
        ("tools/calculator/age-calculator.html", "/tools/calculator/age-calculator.html"),
        ("tools/calculator/basic-calculator.html", "/tools/calculator/basic-calculator.html"),
        ("tools/calculator/bmi-calculator.html", "/tools/calculator/bmi-calculator.html"),
        ("tools/calculator/loan-calculator.html", "/tools/calculator/loan-calculator.html"),
        ("tools/calculator/percentage-calculator.html", "/tools/calculator/percentage-calculator.html"),
        ("tools/calculator/scientific-calculator.html", "/tools/calculator/scientific-calculator.html"),
        ("tools/calculator/unit-converter.html", "/tools/calculator/unit-converter.html"),
        ("tools/generator/hash-generator.html", "/tools/generator/hash-generator.html"),
        ("tools/generator/password-generator.html", "/tools/generator/password-generator.html"),
        ("tools/generator/pomodoro-timer.html", "/tools/generator/pomodoro-timer.html"),
        ("tools/generator/qr-code-generator.html", "/tools/generator/qr-code-generator.html"),
        ("tools/generator/qr-code-scanner.html", "/tools/generator/qr-code-scanner.html"),
        ("tools/generator/random-number-generator.html", "/tools/generator/random-number-generator.html"),
        ("tools/generator/uuid-generator.html", "/tools/generator/uuid-generator.html"),
        ("tools/generator/what-is-my-ip.html", "/tools/generator/what-is-my-ip.html"),
        ("tools/image/background-remover.html", "/tools/image/background-remover.html"),
        ("tools/image/color-converter.html", "/tools/image/color-converter.html"),
        ("tools/image/color-picker.html", "/tools/image/color-picker.html"),
        ("tools/image/image-compressor.html", "/tools/image/image-compressor.html"),
        ("tools/image/image-converter.html", "/tools/image/image-converter.html"),
        ("tools/image/image-resizer.html", "/tools/image/image-resizer.html"),
        ("tools/pdf/compress-pdf.html", "/tools/pdf/compress-pdf.html"),
        ("tools/pdf/jpg-to-pdf.html", "/tools/pdf/jpg-to-pdf.html"),
        ("tools/pdf/merge-pdf.html", "/tools/pdf/merge-pdf.html"),
        ("tools/pdf/split-pdf.html", "/tools/pdf/split-pdf.html"),
        ("tools/text/base64.html", "/tools/text/base64.html"),
        ("tools/text/case-converter.html", "/tools/text/case-converter.html"),
        ("tools/text/csv-to-json.html", "/tools/text/csv-to-json.html"),
        ("tools/text/html-encoder.html", "/tools/text/html-encoder.html"),
        ("tools/text/html-formatter.html", "/tools/text/html-formatter.html"),
        ("tools/text/json-formatter.html", "/tools/text/json-formatter.html"),
        ("tools/text/lorem-ipsum.html", "/tools/text/lorem-ipsum.html"),
        ("tools/text/number-base-converter.html", "/tools/text/number-base-converter.html"),
        ("tools/text/remove-duplicates.html", "/tools/text/remove-duplicates.html"),
        ("tools/text/sql-formatter.html", "/tools/text/sql-formatter.html"),
        ("tools/text/url-encoder.html", "/tools/text/url-encoder.html"),
        ("tools/text/word-counter.html", "/tools/text/word-counter.html"),
    ], "monthly", "0.7"),
    ([
        ("blog/index.html", "/blog/index.html"),
        ("blog/age-calculator-uses.html", "/blog/age-calculator-uses.html"),
        ("blog/batch-image-processing.html", "/blog/batch-image-processing.html"),
        ("blog/color-design-basics.html", "/blog/color-design-basics.html"),
        ("blog/data-privacy-tools.html", "/blog/data-privacy-tools.html"),
        ("blog/how-to-compress-pdf.html", "/blog/how-to-compress-pdf.html"),
        ("blog/image-compression-guide.html", "/blog/image-compression-guide.html"),
        ("blog/json-formatter-developers.html", "/blog/json-formatter-developers.html"),
        ("blog/password-security.html", "/blog/password-security.html"),
        ("blog/pdf-tools-guide.html", "/blog/pdf-tools-guide.html"),
        ("blog/percent-calculator-everyday.html", "/blog/percent-calculator-everyday.html"),
        ("blog/qr-code-business.html", "/blog/qr-code-business.html"),
        ("blog/qr-code-types.html", "/blog/qr-code-types.html"),
    ], "monthly", "0.6"),
    ([
        ("about.html", "/about.html"),
        ("privacy.html", "/privacy.html"),
        ("contact.html", "/contact.html"),
        ("disclaimer.html", "/disclaimer.html"),
    ], "yearly", "0.5"),
]

urls = []
total_count = 0
for path_list, changefreq, priority in priority_groups:
    for _, rel_url in path_list:
        url = SITE_BASE + rel_url
        urls.append(f'  <url>\n    <loc>{url}</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>{changefreq}</changefreq>\n    <priority>{priority}</priority>\n  </url>')
        total_count += 1

sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + \
    "\n".join(urls) + "\n</urlset>\n"

with open("/workspace/sitemap.xml", "w", encoding="utf-8") as f:
    f.write(sitemap)

print(f"✅ sitemap.xml 已生成，共 {total_count} 个 URL")
print(f"   顺序：首页 → tools/index → categories → 工具页面 → 博客 → 信息页")
