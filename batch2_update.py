#!/usr/bin/env python3
"""
批次 2：核心体验升级 - 批量更新脚本
- 添加全局深色模式 CSS/JS
- 添加主题切换按钮到导航栏
- 添加搜索组件到首页和分类页
- 添加 Toast 容器
"""
import re
from pathlib import Path

ROOT = Path("/workspace")

# 需要添加的 CSS 引用
THEME_CSS_LINK = '<link rel="stylesheet" href="/css/theme.css" />'

# 需要添加的 JS 引用
THEME_JS_SCRIPT = '<script src="/js/theme.js"></script>'
SEARCH_JS_SCRIPT = '<script src="/js/search.js"></script>'

# 主题切换按钮（添加到导航栏）
THEME_TOGGLE_BTN = '<button class="theme-toggle" aria-label="Toggle theme">🌙</button>'

# 搜索组件 HTML
SEARCH_HTML = '''
<div class="search-container" style="margin-bottom:16px;">
  <span class="search-icon">🔍</span>
  <input type="search" id="tool-search" class="search-input" placeholder="Search 40+ tools..." autocomplete="off" />
  <div id="search-results" class="search-results"></div>
</div>
'''

# Toast 容器
TOAST_CONTAINER = '<div id="toast-container" class="toast-container"></div>'


def update_html_file(filepath, add_search=False):
    """更新单个 HTML 文件"""
    html = filepath.read_text(encoding="utf-8")
    original = html
    
    # 1. 添加 theme.css（在现有 CSS 之后）
    if 'css/theme.css' not in html:
        # 找到最后一个 CSS link
        css_pattern = r'<link[^>]*rel="stylesheet"[^>]*>'
        css_matches = list(re.finditer(css_pattern, html))
        if css_matches:
            last_css = css_matches[-1]
            html = html[:last_css.end()] + '\n  ' + THEME_CSS_LINK + html[last_css.end():]
        else:
            # 添加到 head 末尾
            head_end = html.find('</head>')
            if head_end != -1:
                html = html[:head_end] + '  ' + THEME_CSS_LINK + '\n' + html[head_end:]
    
    # 2. 添加 theme.js（在 </body> 之前）
    if 'js/theme.js' not in html:
        body_end = html.find('</body>')
        if body_end != -1:
            html = html[:body_end] + '  ' + THEME_JS_SCRIPT + '\n' + html[body_end:]
    
    # 3. 添加搜索组件（首页和分类页）
    if add_search and 'tool-search' not in html:
        # 添加 search.js
        if 'js/search.js' not in html:
            body_end = html.find('</body>')
            if body_end != -1:
                html = html[:body_end] + '  ' + SEARCH_JS_SCRIPT + '\n' + html[body_end:]
        
        # 在 hero 区域后添加搜索框
        hero_end_pattern = r'</section>\s*</div>\s*<section class="tools-section">'
        match = re.search(hero_end_pattern, html)
        if match:
            html = html[:match.start()] + SEARCH_HTML + '\n  ' + html[match.start():]
        else:
            # 尝试在 container-md 中的 hero 后添加
            hero_div_pattern = r'<div class="hero">.*?</div>\s*</div>'
            match = re.search(hero_div_pattern, html, re.DOTALL)
            if match:
                html = html[:match.end()] + '\n  ' + SEARCH_HTML + html[match.end():]
    
    # 4. 添加主题切换按钮到导航栏
    if 'theme-toggle' not in html:
        # 在 nav-links 后添加
        nav_pattern = r'<div class="nav-links"[^>]*>.*?</div>\s*</div>\s*</nav>'
        match = re.search(nav_pattern, html, re.DOTALL)
        if match:
            # 在 nav-inner 结束前添加
            nav_inner_end = html.find('</div>', match.start() + 50)
            if nav_inner_end != -1:
                html = html[:nav_inner_end] + '  ' + THEME_TOGGLE_BTN + '\n    ' + html[nav_inner_end:]
    
    # 5. 添加 Toast 容器
    if 'toast-container' not in html and 'id="toast-container"' not in html:
        body_end = html.find('</body>')
        if body_end != -1:
            html = html[:body_end] + '  ' + TOAST_CONTAINER + '\n' + html[body_end:]
    
    # 6. 更新现有样式使用 CSS 变量
    # 替换硬编码的颜色为 CSS 变量
    color_replacements = {
        'background: #fff': 'background: var(--bg)',
        'background: #ffffff': 'background: var(--bg)',
        'background: #f8fafc': 'background: var(--bg-subtle)',
        'background: #f1f5f9': 'background: var(--bg-subtle)',
        'background-color: #fff': 'background-color: var(--bg)',
        'background-color: #ffffff': 'background-color: var(--bg)',
        'color: #0f172a': 'color: var(--text)',
        'color: #1f2937': 'color: var(--text)',
        'color: #64748b': 'color: var(--text-muted)',
        'color: #94a3b8': 'color: var(--text-muted)',
        'border-color: #e2e8f0': 'border-color: var(--border)',
        'border-color: #e5e7eb': 'border-color: var(--border)',
        'border: 1px solid #e2e8f0': 'border: 1px solid var(--border)',
        'border: 1px solid #e5e7eb': 'border: 1px solid var(--border)',
        'border: 2px dashed #e2e8f0': 'border: 2px dashed var(--dropzone-border)',
        'border: 2px dashed #e5e7eb': 'border: 2px dashed var(--dropzone-border)',
    }
    
    for old, new in color_replacements.items():
        # 只替换在 style 标签内的
        html = re.sub(
            r'(<style[^>]*>.*?)' + re.escape(old) + r'(.*?</style>)',
            r'\1' + new + r'\2',
            html,
            flags=re.DOTALL
        )
    
    if html != original:
        filepath.write_text(html, encoding="utf-8")
        return True
    return False


def main():
    print("=" * 60)
    print("批次 2：核心体验升级 - 批量更新")
    print("=" * 60)
    
    # 更新首页（添加搜索）
    print("\n[1] 更新首页...")
    index_file = ROOT / "index.html"
    if update_html_file(index_file, add_search=True):
        print("  ✅ index.html")
    
    # 更新分类页（添加搜索）
    print("\n[2] 更新分类页...")
    for cat_file in ROOT.glob("categories/*.html"):
        if update_html_file(cat_file, add_search=True):
            print(f"  ✅ {cat_file.relative_to(ROOT)}")
    
    # 更新工具页
    print("\n[3] 更新工具页...")
    tool_count = 0
    for tool_file in ROOT.rglob("tools/**/*.html"):
        if tool_file.name == "index.html":
            continue
        if update_html_file(tool_file, add_search=False):
            tool_count += 1
            print(f"  ✅ {tool_file.relative_to(ROOT)}")
    print(f"  共更新 {tool_count} 个工具页")
    
    # 更新博客页
    print("\n[4] 更新博客页...")
    for blog_file in ROOT.glob("blog/*.html"):
        if update_html_file(blog_file, add_search=False):
            print(f"  ✅ {blog_file.relative_to(ROOT)}")
    
    # 更新信息页
    print("\n[5] 更新信息页...")
    for info_file in ["about.html", "privacy.html", "contact.html", "disclaimer.html", "404.html"]:
        info_path = ROOT / info_file
        if info_path.exists():
            if update_html_file(info_path, add_search=False):
                print(f"  ✅ {info_file}")
    
    print("\n" + "=" * 60)
    print("完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()