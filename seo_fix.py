#!/usr/bin/env python3
"""
批量 SEO / AdSense 优化脚本：
1. 给所有工具页面添加 OG tags (og:title, og:description, og:type)
2. 给所有工具页面添加 schema.org WebApplication 结构化数据
3. 给所有页面添加 favicon 引用
4. 生成完整的 sitemap.xml
"""
import os
import re
import datetime
from pathlib import Path

ROOT = Path("/workspace")
SITE_BASE = "https://www.zlbox.site"
SITE_NAME = "My Tool Lab"
ADSENSE_PUB_ID = "pub-5420550088713746"

# 页面类别到描述的映射 (用于 schema.org)
CATEGORY_TYPES = {
    "calculator": "calculator tool",
    "generator": "generator tool",
    "image": "image tool",
    "pdf": "PDF tool",
    "text": "text tool",
}

DEFAULT_CATEGORY = "utility tool"

def extract_from_html(filepath, html):
    """从 HTML 中提取 title, description, canonical URL"""
    # title
    m = re.search(r'<title>([^<]+)</title>', html)
    title = m.group(1).strip() if m else SITE_NAME
    
    # description
    m = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', html)
    description = m.group(1).strip() if m else title
    
    # canonical
    m = re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"', html)
    canonical = m.group(1).strip() if m else build_canonical(filepath)
    
    return title, description, canonical


def build_canonical(filepath):
    """根据文件路径构建 canonical URL"""
    rel = str(filepath.relative_to(ROOT))
    if rel == "index.html":
        return f"{SITE_BASE}/"
    # pages/xxx.html -> /xxx.html (因为我们保持根目录的版本)
    if rel.startswith("pages/"):
        rel = rel[len("pages/"):]
    return f"{SITE_BASE}/{rel}"


def get_page_type(filepath, html):
    """确定页面 schema.org 类型"""
    rel = str(filepath.relative_to(ROOT))
    
    if rel == "index.html":
        return "WebSite"
    if "tools/" in rel:
        return "WebApplication"
    if "blog/" in rel and "index.html" not in rel:
        return "Article"
    return "WebPage"


def get_category(filepath):
    """从路径推断工具类别"""
    parts = str(filepath.relative_to(ROOT)).split("/")
    if len(parts) >= 2 and parts[0] == "tools":
        return CATEGORY_TYPES.get(parts[1], DEFAULT_CATEGORY)
    return DEFAULT_CATEGORY


def has_favicon(html):
    return 'rel="icon"' in html or "rel='icon'" in html


def has_og(html):
    return 'property="og:' in html or "property='og:" in html


def has_schema_ld(html):
    return 'application/ld+json' in html


def build_og_tags(title, description, canonical):
    return f'''
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{description}" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:site_name" content="{SITE_NAME}" />'''


def build_favicon_link():
    return '\n  <link rel="icon" type="image/svg+xml" href="/favicon.svg" />'


def build_schema_ld(page_type, title, description, canonical, filepath):
    """构建 JSON-LD 结构化数据"""
    import json
    
    if page_type == "WebSite":
        data = {
            "@context": "https://schema.org",
            "@type": "WebSite",
            "name": SITE_NAME,
            "url": SITE_BASE + "/",
            "description": description,
            "potentialAction": {
                "@type": "SearchAction",
                "target": f"{SITE_BASE}/tools/index.html?q={{search_term_string}}",
                "query-input": "required name=search_term_string"
            }
        }
    elif page_type == "WebApplication":
        category = get_category(filepath)
        data = {
            "@context": "https://schema.org",
            "@type": "WebApplication",
            "name": title.replace(f" | {SITE_NAME}", "").replace(f" – {SITE_NAME}", "").strip(),
            "description": description,
            "url": canonical,
            "applicationCategory": category.title(),
            "operatingSystem": "Any (browser-based)",
            "offers": {
                "@type": "Offer",
                "price": "0",
                "priceCurrency": "USD"
            },
            "browserRequirements": "Requires a modern web browser with JavaScript enabled."
        }
    elif page_type == "Article":
        data = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": title.replace(f" | {SITE_NAME}", "").replace(f" – {SITE_NAME}", "").strip(),
            "description": description,
            "url": canonical,
            "author": {
                "@type": "Organization",
                "name": SITE_NAME
            },
            "publisher": {
                "@type": "Organization",
                "name": SITE_NAME
            },
            "mainEntityOfPage": {
                "@type": "WebPage",
                "@id": canonical
            }
        }
    else:  # WebPage
        data = {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": title,
            "description": description,
            "url": canonical,
            "isPartOf": {
                "@type": "WebSite",
                "name": SITE_NAME,
                "url": SITE_BASE + "/"
            }
        }
    
    json_str = json.dumps(data, ensure_ascii=False)
    return f'\n  <script type="application/ld+json">{json_str}</script>'


def process_html_file(filepath):
    """处理单个 HTML 文件"""
    html = filepath.read_text(encoding="utf-8")
    
    # 跳过 Google 验证文件（只有几行，不需要 SEO tags）
    if "google4bd1e08685667667.html" in str(filepath):
        return False
    
    title, description, canonical = extract_from_html(filepath, html)
    page_type = get_page_type(filepath, html)
    
    # 如果 canonical 不存在，添加它
    needs_canonical = 'rel="canonical"' not in html
    
    # 需要添加的内容
    additions = []
    
    if not has_favicon(html):
        additions.append(build_favicon_link())
    
    if not has_og(html):
        additions.append(build_og_tags(title, description, canonical))
    
    if not has_schema_ld(html):
        additions.append(build_schema_ld(page_type, title, description, canonical, filepath))
    
    if needs_canonical:
        # 在 </title> 之后添加 canonical
        additions.insert(0, f'\n  <link rel="canonical" href="{canonical}" />')
    
    if not additions:
        return False
    
    # 将 additions 插入到 </head> 之前
    combined = "".join(additions)
    
    # 找到 </head>
    head_end = html.find("</head>")
    if head_end == -1:
        return False
    
    new_html = html[:head_end] + combined + "\n" + html[head_end:]
    
    filepath.write_text(new_html, encoding="utf-8")
    return True


def find_all_html_files():
    """找到所有需要处理的 HTML 文件"""
    files = []
    for html_file in sorted(ROOT.rglob("*.html")):
        # 跳过 _js 目录（如果还存在的话）
        rel = str(html_file.relative_to(ROOT))
        if rel.startswith("_"):
            continue
        # 跳过 pages/ 目录（现在为空，但以防万一）
        if rel.startswith("pages/"):
            continue
        files.append(html_file)
    return files


def generate_sitemap(files):
    """生成完整的 sitemap.xml"""
    today = datetime.date.today().isoformat()
    
    urls = []
    
    # 首页（最高优先级）
    for f in files:
        rel = str(f.relative_to(ROOT))
        
        if rel == "index.html":
            url = f"{SITE_BASE}/"
            priority = "1.0"
            changefreq = "weekly"
        elif rel == "tools/index.html":
            url = f"{SITE_BASE}/tools/index.html"
            priority = "0.9"
            changefreq = "weekly"
        elif rel.startswith("categories/"):
            url = f"{SITE_BASE}/{rel}"
            priority = "0.8"
            changefreq = "weekly"
        elif rel.startswith("tools/"):
            url = f"{SITE_BASE}/{rel}"
            priority = "0.7"
            changefreq = "monthly"
        elif rel.startswith("blog/"):
            url = f"{SITE_BASE}/{rel}"
            priority = "0.6"
            changefreq = "monthly"
        else:
            # about, privacy, contact, disclaimer
            url = f"{SITE_BASE}/{rel}"
            priority = "0.5"
            changefreq = "yearly"
        
        urls.append(f'  <url>\n    <loc>{url}</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>{changefreq}</changefreq>\n    <priority>{priority}</priority>\n  </url>')
    
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(urls) + "\n</urlset>\n"
    return sitemap


def main():
    print("=" * 60)
    print("开始批量 SEO 优化...")
    print("=" * 60)
    
    files = find_all_html_files()
    print(f"共找到 {len(files)} 个 HTML 文件")
    
    modified = 0
    for f in files:
        if process_html_file(f):
            rel = str(f.relative_to(ROOT))
            modified += 1
            print(f"  ✅ 更新: {rel}")
    
    print(f"\n修改了 {modified} 个文件")
    
    # 生成 sitemap
    sitemap = generate_sitemap(files)
    (ROOT / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    print(f"\n✅ sitemap.xml 已生成 ({len(files)} 个 URL)")
    
    # 更新 robots.txt（确保 sitemap 引用正确）
    robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
    if "Sitemap:" not in robots:
        robots += f"\n\nSitemap: {SITE_BASE}/sitemap.xml\n"
        (ROOT / "robots.txt").write_text(robots, encoding="utf-8")
        print("✅ robots.txt 已更新（添加 Sitemap 引用）")
    
    print("\n" + "=" * 60)
    print("完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
