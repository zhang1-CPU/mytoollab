#!/usr/bin/env python3
"""
为所有页面添加顶部 sticky navigation bar
导航包含: Home | All Tools | Text | Calculator | Generator | Image | PDF | Blog
"""
import re
from pathlib import Path

ROOT = Path("/workspace")
SITE_BASE = "https://www.zlbox.site"

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

NAV_CSS = '''
/* ── Site Navigation ── */
.site-nav {
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(255,255,255,.97);
  backdrop-filter: blur(8px);
  border-bottom: 1px solid var(--border);
  box-shadow: 0 1px 4px rgba(0,0,0,.05);
}
.nav-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  align-items: center;
  gap: 8px;
  height: 52px;
}
.nav-logo {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 700;
  font-size: 1rem;
  color: var(--brand);
  text-decoration: none;
  flex-shrink: 0;
  margin-right: 12px;
}
.nav-logo:hover { text-decoration: none; }
.nav-logo-icon {
  width: 30px;
  height: 30px;
  background: var(--brand);
  color: #fff;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 900;
  font-size: .9rem;
  flex-shrink: 0;
}
.nav-logo-text { font-size: .95rem; }
.nav-links {
  display: flex;
  align-items: center;
  gap: 2px;
  flex-wrap: nowrap;
  overflow-x: auto;
  scrollbar-width: none;
  -ms-overflow-style: none;
  flex: 1;
}
.nav-links::-webkit-scrollbar { display: none; }
.nav-link {
  display: inline-flex;
  align-items: center;
  padding: 5px 10px;
  font-size: .82rem;
  font-weight: 500;
  color: var(--text);
  border-radius: 6px;
  white-space: nowrap;
  transition: all .15s;
  flex-shrink: 0;
}
.nav-link:hover {
  background: var(--brand);
  color: #fff;
  text-decoration: none;
}
.nav-link.active {
  background: #eff6ff;
  color: var(--brand);
}
.nav-toggle {
  display: none;
  flex-direction: column;
  justify-content: center;
  gap: 4px;
  width: 32px;
  height: 32px;
  padding: 4px;
  background: none;
  border: 1px solid var(--border);
  border-radius: 6px;
  cursor: pointer;
  flex-shrink: 0;
  margin-left: auto;
}
.nav-toggle span {
  display: block;
  width: 100%;
  height: 2px;
  background: var(--text);
  border-radius: 1px;
}
@media (max-width: 768px) {
  .nav-logo-text { display: none; }
  .nav-inner { gap: 6px; }
  .nav-toggle { display: flex; }
  .nav-links {
    display: none;
    position: absolute;
    top: 52px;
    left: 0;
    right: 0;
    background: #fff;
    border-bottom: 1px solid var(--border);
    box-shadow: 0 4px 12px rgba(0,0,0,.1);
    flex-direction: column;
    align-items: flex-start;
    padding: 8px 0;
    z-index: 99;
    overflow: visible;
  }
  .nav-links.open { display: flex; }
  .nav-link {
    width: 100%;
    padding: 10px 20px;
    font-size: .9rem;
    border-radius: 0;
  }
}
'''

NAV_JS = '''
/* Navigation toggle for mobile */
(function() {
  var toggle = document.querySelector('.nav-toggle');
  var navLinks = document.querySelector('.nav-links');
  if (!toggle || !navLinks) return;
  toggle.addEventListener('click', function() {
    var isOpen = navLinks.classList.toggle('open');
    toggle.setAttribute('aria-expanded', isOpen);
  });
  // Highlight active link
  var path = location.pathname;
  document.querySelectorAll('.nav-link').forEach(function(link) {
    var href = link.getAttribute('href');
    if (href && (path === href || path.indexOf(href.replace('/index.html','')) > -1)) {
      link.classList.add('active');
    }
  });
})();
'''

SKIP_FILES = {"google4bd1e08685667667.html", "404.html"}


def add_nav_to_html(html):
    """为单个 HTML 添加导航"""
    # 检查是否已有导航
    if 'class="site-nav"' in html or 'class="nav-inner"' in html:
        return False
    
    # 添加 CSS 到 <style> 末尾或创建 style
    if '<style>' in html and '</style>' in html:
        # 追加到现有 style
        html = html.replace('</style>', '\n' + NAV_CSS.strip() + '\n  </style>', 1)
    else:
        # 在 </head> 前插入 style
        head_end = html.find('</head>')
        if head_end != -1:
            html = html[:head_end] + f'\n  <style>\n{NAV_CSS.strip()}\n  </style>\n' + html[head_end:]
    
    # 添加 JS
    if '<script>' in html or '<script type="text/javascript">' in html:
        # 追加到最后一个 </script> 后
        html = html.replace('</script>', '</script>\n' + NAV_JS.strip(), 1)
    else:
        head_end = html.find('</head>')
        if head_end != -1:
            html = html[:head_end] + f'\n  <script>{NAV_JS.strip()}</script>\n' + html[head_end:]
    
    # 插入 nav 到 body 开始后
    body_start = html.find('<body')
    if body_start == -1:
        return False
    body_tag_end = html.find('>', body_start)
    if body_tag_end == -1:
        return False
    html = html[:body_tag_end+1] + '\n' + NAV_HTML + html[body_tag_end+1:]
    
    return html


def process_all():
    count = 0
    for html_file in sorted(ROOT.rglob("*.html")):
        rel = str(html_file.relative_to(ROOT))
        if rel.startswith("_") or rel.startswith("pages/") or rel in SKIP_FILES:
            continue
        
        content = html_file.read_text(encoding="utf-8")
        result = add_nav_to_html(content)
        if result:
            html_file.write_text(result, encoding="utf-8")
            count += 1
            print(f"  ✅ {rel}")
    
    print(f"\n共更新 {count} 个页面")


if __name__ == "__main__":
    print("=" * 60)
    print("添加顶部导航栏...")
    print("=" * 60)
    process_all()