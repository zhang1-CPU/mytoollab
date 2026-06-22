#!/usr/bin/env python3
"""
全面 Bug 修复脚本
"""
import os
import re
from pathlib import Path

ROOT = Path("/workspace")
SITE_BASE = "https://www.zlbox.site"

# 导航栏 HTML
NAV_HTML = '''
<nav class="site-nav" aria-label="Main navigation">
  <div class="nav-inner">
    <a href="/" class="nav-logo" aria-label="My Tool Lab Home">
      <span class="nav-logo-icon">M</span>
      <span class="nav-logo-text">My Tool Lab</span>
    </a>
    <button class="nav-toggle" aria-label="Toggle navigation" aria-expanded="false">
      <span></span><span></span><span></span>
    </button>
    <div class="nav-links" role="list">
      <a href="/tools/index.html" class="nav-link" role="listitem">All Tools</a>
      <a href="/categories/text.html" class="nav-link" role="listitem">Text</a>
      <a href="/categories/calculator.html" class="nav-link" role="listitem">Calculator</a>
      <a href="/categories/generator.html" class="nav-link" role="listitem">Generator</a>
      <a href="/categories/image.html" class="nav-link" role="listitem">Image</a>
      <a href="/categories/pdf.html" class="nav-link" role="listitem">PDF</a>
      <a href="/blog/index.html" class="nav-link" role="listitem">Blog</a>
    </div>
  </div>
</nav>
'''

# 导航栏 CSS
NAV_CSS = '''
/* Site Navigation */
.site-nav {
  position: sticky;
  top: 0;
  z-index: 1000;
  background: #fff;
  border-bottom: 1px solid #e2e8f0;
  box-shadow: 0 1px 3px rgba(0,0,0,.05);
}
.nav-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 56px;
}
.nav-logo {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 700;
  color: #2563eb;
  text-decoration: none;
}
.nav-logo-icon {
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #2563eb, #1d4ed8);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 18px;
}
.nav-logo-text {
  font-size: 18px;
}
.nav-toggle {
  display: none;
  background: none;
  border: none;
  padding: 8px;
  cursor: pointer;
}
.nav-toggle span {
  display: block;
  width: 24px;
  height: 2px;
  background: #0f172a;
  margin: 5px 0;
  transition: all .2s;
}
.nav-links {
  display: flex;
  gap: 4px;
}
.nav-link {
  padding: 8px 12px;
  font-size: .88rem;
  font-weight: 500;
  color: #64748b;
  text-decoration: none;
  border-radius: 6px;
  transition: all .2s;
}
.nav-link:hover {
  color: #2563eb;
  background: #f1f5f9;
}
@media (max-width: 768px) {
  .nav-toggle { display: block; }
  .nav-links {
    display: none;
    position: absolute;
    top: 56px;
    left: 0;
    right: 0;
    background: #fff;
    border-bottom: 1px solid #e2e8f0;
    padding: 8px 20px;
    flex-direction: column;
    gap: 4px;
  }
  .nav-links.active { display: flex; }
  .nav-link { padding: 12px 16px; }
}
'''


def add_navigation(filepath):
    """添加导航栏"""
    html = filepath.read_text(encoding="utf-8")
    
    if 'site-nav' in html:
        return False
    
    # 添加 CSS
    if '</style>' in html:
        html = html.replace('</style>', NAV_CSS + '\n</style>')
    else:
        head_end = html.find('</head>')
        if head_end != -1:
            html = html[:head_end] + '<style>' + NAV_CSS + '</style>\n' + html[head_end:]
    
    # 添加导航栏 HTML（在 body 开头）
    body_start = html.find('<body')
    if body_start != -1:
        body_end = html.find('>', body_start) + 1
        html = html[:body_end] + '\n' + NAV_HTML + html[body_end:]
    
    # 添加导航栏 JS
    nav_js = '''
<script>
document.addEventListener('DOMContentLoaded',function(){
  var toggle=document.querySelector('.nav-toggle');
  var links=document.querySelector('.nav-links');
  if(toggle&&links){
    toggle.addEventListener('click',function(){
      links.classList.toggle('active');
      toggle.setAttribute('aria-expanded',links.classList.contains('active'));
    });
  }
});
</script>'''
    
    body_end = html.find('</body>')
    if body_end != -1:
        html = html[:body_end] + nav_js + '\n' + html[body_end:]
    
    filepath.write_text(html, encoding="utf-8")
    return True


def fix_brand_name(filepath):
    """修复品牌名 zlbox → My Tool Lab"""
    html = filepath.read_text(encoding="utf-8")
    
    if 'zlbox' not in html:
        return False
    
    # 替换标题中的 zlbox
    html = re.sub(r'<title>([^<]*)\| zlbox</title>', r'<title>\1| My Tool Lab</title>', html)
    html = re.sub(r'<title>([^<]*)– ([^<]*) \| zlbox</title>', r'<title>\1– \2 | My Tool Lab</title>', html)
    
    filepath.write_text(html, encoding="utf-8")
    return True


def fix_double_h1(filepath):
    """修复多个 H1 标签"""
    html = filepath.read_text(encoding="utf-8")
    
    h1_count = len(re.findall(r'<h1', html))
    if h1_count <= 1:
        return False
    
    # 将第二个 H1 改为 H2
    html = re.sub(r'<h1([^>]*)>', r'<h2\1>', html, count=1)
    html = re.sub(r'</h1>', r'</h2>', html, count=1)
    
    filepath.write_text(html, encoding="utf-8")
    return True


def add_article_schema(filepath):
    """添加 Article schema 到博客"""
    html = filepath.read_text(encoding="utf-8")
    
    if '"@type":"Article"' in html or '"@type": "Article"' in html:
        return False
    
    # 获取标题和描述
    title_match = re.search(r'<title>([^<]+)</title>', html)
    desc_match = re.search(r'<meta name="description" content="([^"]+)"', html)
    
    title = title_match.group(1) if title_match else "Blog Post"
    desc = desc_match.group(1) if desc_match else ""
    
    rel = str(filepath.relative_to(ROOT))
    url = f"{SITE_BASE}/{rel}"
    
    schema = f'''
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Article","headline":"{title}","description":"{desc}","url":"{url}","author":{{"@type":"Organization","name":"My Tool Lab"}},"publisher":{{"@type":"Organization","name":"My Tool Lab"}},"datePublished":"2024-01-01","dateModified":"2024-01-01"}}
</script>'''
    
    head_end = html.find('</head>')
    if head_end != -1:
        html = html[:head_end] + schema + '\n' + html[head_end:]
    
    filepath.write_text(html, encoding="utf-8")
    return True


def main():
    print("=" * 60)
    print("全面 Bug 修复...")
    print("=" * 60)
    
    # 1. 删除备份文件
    print("\n[1] 删除备份文件...")
    bak_count = 0
    for bak_file in ROOT.rglob("*.bak"):
        bak_file.unlink()
        bak_count += 1
    print(f"  删除了 {bak_count} 个 .bak 文件")
    
    # 2. 删除 sitemap.html
    print("\n[2] 删除冗余文件...")
    sitemap_html = ROOT / "sitemap.html"
    if sitemap_html.exists():
        sitemap_html.unlink()
        print("  删除了 sitemap.html")
    
    # 3. 添加导航栏
    print("\n[3] 添加导航栏...")
    nav_count = 0
    for html_file in ROOT.rglob("*.html"):
        if str(html_file).startswith(str(ROOT / "_")) or str(html_file).startswith(str(ROOT / "pages")):
            continue
        if html_file.name == "google4bd1e08685667667.html":
            continue
        if add_navigation(html_file):
            nav_count += 1
            print(f"  ✅ {html_file.relative_to(ROOT)}")
    print(f"  添加了 {nav_count} 个导航栏")
    
    # 4. 修复品牌名
    print("\n[4] 修复品牌名...")
    brand_count = 0
    for html_file in ROOT.rglob("*.html"):
        if fix_brand_name(html_file):
            brand_count += 1
            print(f"  ✅ {html_file.relative_to(ROOT)}")
    print(f"  修复了 {brand_count} 个品牌名")
    
    # 5. 修复多个 H1
    print("\n[5] 修复多个 H1...")
    h1_file = ROOT / "tools/text/html-formatter.html"
    if h1_file.exists():
        if fix_double_h1(h1_file):
            print("  ✅ html-formatter.html")
    
    # 6. 添加 Article schema
    print("\n[6] 添加 Article schema...")
    schema_count = 0
    for blog_file in ROOT.glob("blog/*.html"):
        if blog_file.name == "index.html":
            continue
        if add_article_schema(blog_file):
            schema_count += 1
            print(f"  ✅ {blog_file.relative_to(ROOT)}")
    print(f"  添加了 {schema_count} 个 Article schema")
    
    print("\n" + "=" * 60)
    print("修复完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()