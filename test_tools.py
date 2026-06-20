#!/usr/bin/env python3
"""
Tool Testing Suite - 深成分析每个工具页面
"""
import os, re, sys

tools_root = './tools'
categories_root = './categories'
blog_root = './blog'

tool_files = []
for root, dirs, files in os.walk(tools_root):
    for f in files:
        if f.endswith('.html') and f != 'index.html':
            tool_files.append(os.path.join(root, f))
tool_files.sort()

# Also include the tools index
tool_files.insert(0, './tools/index.html')

ALL_BUGS = []

def read_file(path):
    with open(path, encoding='utf-8') as f:
        return f.read()

def test_tool(filepath, expected_type, expected_id):
    """Test a single tool page for issues"""
    bugs = []
    warnings = []
    info = []
    content = read_file(filepath)

    # 1. DOCTYPE
    if '<!DOCTYPE html>' not in content[:300]:
        bugs.append("❌ 缺少 DOCTYPE")

    # 2. 检查 CSS 引用
    has_css = False
    css_refs = []
    for m in re.finditer(r'<link[^>]+href=[\'"]([^\'"]*\.css)[\'"][^>]*>', content):
        has_css = True
        css_refs.append(m.group(1))
    if not has_css:
        # Check if there's inline style
        if '<style' not in content:
            bugs.append("❌ 无 CSS 样式（既无外部引用也无内联）")
        else:
            info.append("✅ 有内联 CSS 样式")
    else:
        info.append(f"✅ CSS 引用: {', '.join(css_refs)}")
        # Check if these CSS files exist
        base_dir = os.path.dirname(filepath)
        for ref in css_refs:
            if ref.startswith('/'):
                full = os.path.normpath(os.path.join('.', ref.lstrip('/')))
            else:
                full = os.path.normpath(os.path.join(base_dir, ref))
            if not os.path.exists(full):
                bugs.append(f"❌ CSS 文件不存在: {ref}")

    # 3. 检查 JS 引用
    js_refs = []
    has_inline_js = False
    for m in re.finditer(r'<script[^>]+src=[\'"]([^\'"]+)[\'"][^>]*>', content):
        js_refs.append(m.group(1))
    if '<script>' in content or '<script>' in content:
        has_inline_js = True
    info.append(f"✅ JS 引用: {', '.join(js_refs) if js_refs else '(无外部 JS)'}")
    info.append(f"✅ 内联 JS: {'有' if has_inline_js else '无'}")

    # 4. 检查是否有按钮/输入
    has_button = bool(re.search(r'<button|type="button"', content))
    has_input = bool(re.search(r'<input|<textarea|<select', content))
    has_output = bool(re.search(r'<div[^>]*id=["\'].*(output|result|count|display)["\']|class=["\'][^"\']*(output|result|display)["\']', content, re.I))

    if not has_button:
        bugs.append("❌ 无操作按钮（用户无法交互）")
    if not has_input:
        bugs.append("❌ 无输入元素")
    info.append(f"✅ 元素: button={has_button}, input={has_input}, output={has_output}")

    # 5. 检查 JS 函数定义
    function_names = re.findall(r'function\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(', content)
    if function_names:
        info.append(f"✅ JS 函数: {len(function_names)} 个 ({', '.join(function_names[:5])}{'...' if len(function_names) > 5 else ''})")
    else:
        bugs.append("❌ 无 JavaScript 函数定义（工具无法工作）")

    # 6. 检查按钮是否有 onclick 或事件绑定
    onclick_matches = re.findall(r'onclick\s*=\s*["\']([^"\']+)', content)
    if onclick_matches:
        # Check if the function called actually exists
        for onclick in onclick_matches[:5]:
            func_match = re.match(r'([A-Za-z_][A-Za-z0-9_]*)\s*\(', onclick)
            if func_match:
                called_func = func_match.group(1)
                if called_func not in function_names and not (called_func in ('document','window')):
                    # Check if this function is defined elsewhere (external JS)
                    warnings.append(f"⚠️  按钮调用 {called_func}() 但在本文件内未找到定义（可能在外部 JS 中）")
    else:
        # Check if there are addEventListener calls in JS
        has_event = bool(re.search(r'addEventListener|querySelector\(.+?\)\.(onclick|addEventListener)', content))
        if not has_event and has_button:
            warnings.append("⚠️  按钮没有 onclick 或事件绑定")

    # 7. 检查基本结构
    missing_elements = []
    if '<nav' not in content and 'class="nav"' not in content:
        missing_elements.append("❌ 无导航栏")
    if '<footer' not in content and 'class="footer"' not in content:
        missing_elements.append("⚠️  无页脚")
    if missing_elements:
        bugs.extend(missing_elements)

    # 8. 检查 meta robots
    if 'name="robots"' not in content:
        warnings.append("⚠️  缺少 meta robots")

    # 9. 检查 title
    title_match = re.search(r'<title>(.+?)</title>', content)
    if title_match:
        info.append(f"✅ title: {title_match.group(1)[:60]}")
    else:
        bugs.append("❌ 无 <title>")

    # 10. 检查 meta description
    desc_match = re.search(r'<meta[^>]+name=[\'"]description[\'"][^>]+content=[\'"]([^\'"]+)[\'"][^>]*>', content)
    if desc_match:
        info.append(f"✅ description: {desc_match.group(1)[:80]}")
    else:
        warnings.append("⚠️  缺少 meta description")

    # 11. 检查 Schema.org 结构化数据
    if 'application/ld+json' in content:
        info.append(f"✅ 有 Schema.org 结构化数据")
    else:
        warnings.append("⚠️  缺少 Schema.org")

    return {
        'bugs': bugs,
        'warnings': warnings,
        'info': info
    }

# Test all tool files
total_bugs = 0
total_warnings = 0
for f in tool_files:
    result = test_tool(f, None, None)
    if result['bugs'] or result['warnings']:
        print(f"\n{'='*60}")
        print(f"🔍 {f}")
        print(f"{'='*60}")
        for b in result['bugs']:
            print(f"  {b}")
            total_bugs += 1
        for w in result['warnings']:
            print(f"  {w}")
            total_warnings += 1
        for i in result['info']:
            print(f"  {i}")

# Also test index.html
print(f"\n{'='*60}")
print(f"🔍 ./index.html (首页)")
print(f"{'='*60}")
content = read_file('./index.html')
bugs = []
if '<!DOCTYPE html>' not in content[:200]:
    bugs.append("❌ 无 DOCTYPE")
if '<title>' not in content:
    bugs.append("❌ 无 title")
if 'application/ld+json' not in content:
    bugs.append("❌ 无 schema")
for b in bugs: print(f"  {b}")
total_bugs += len(bugs)

print(f"\n\n{'='*60}")
print("📊 统计汇总")
print(f"{'='*60}")
print(f"  测试页面数: {len(tool_files)}")
print(f"  Bug 总数:    {total_bugs}")
print(f"  警告总数:    {total_warnings}")
