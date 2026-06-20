#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量清理工具页面内联 style、删除死代码、统一面包屑链接
"""
import os
import re
import sys

TOOLS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tools')

# 需要保留的样式属性（仅这些会被保留在 style 属性中）
KEEP_PROPS = {
    # --- 控制可见性 / 布局结构 ---
    'display',        # display:none / display:block 等控制可见性
    'margin-left',    # 用于 row 内部按钮右对齐
    'flex',           # flex:1 等 flex 布局
    'overflow-x',     # 表格横向滚动
    'overflow',       # 通用 overflow 控制
    'white-space',    # 按钮 nowrap
    'min-width',      # 需要的最小宽度
    'max-width',      # 需要的最大宽度
    'min-height',     # textarea 高度
    'height',         # 特殊高度
    'gap',            # flex/grid gap
    'justify-content',
    'align-items',
    'flex-wrap',
    'background',     # 按钮激活态背景
    'font-family',    # 等宽字体设置
}

# 对特定样式值做白名单（property -> 允许的 value 正则）
ALLOWED_VALUE_PATTERNS = {
    # margin-left 仅保留 "auto" 这种对齐控制
    'margin-left': r'^auto$',
    # display 仅保留 none / block / flex / grid（不做限制，通常都保留）
    # 其他：不作限制，使用 prop 是否在 KEEP_PROPS 中判断
}

# 无论如何都必须删除的属性（在 KEEP_PROPS 中但值不值得保留的）
FORCE_REMOVE_VALUES = {
    ('padding', '0'),
    ('padding', '0px'),
}

# --- 工具函数：清理 style 属性内容 ---
def clean_style_attr(style_val, context_tag, context_classes):
    """
    清理单个 style 属性值。返回清理后的 style 字符串，若为空则返回 ''。
    context_tag/context_classes 用于特殊判断。
    """
    # 首先，针对广告位 (adsbygoogle) - 完全不处理，原样返回
    # 这个会在调用方判断，此处不需要

    # 解析声明
    declarations = []
    for raw in style_val.split(';'):
        raw = raw.strip()
        if not raw or ':' not in raw:
            continue
        prop, val = [x.strip() for x in raw.split(':', 1)]
        prop_l = prop.lower()
        # --- 全局必须删除的情况 ---
        # margin-top:XXpx / margin-top:XXpx;
        if prop_l == 'margin-top':
            continue
        # margin-bottom
        if prop_l == 'margin-bottom':
            continue
        # padding:0 类型的复位
        if prop_l == 'padding' and re.match(r'^0(\s*px)?$', val):
            continue
        # 只含 padding:0 的其他变体（例如 "padding:0;margin-top:20px" 会分开判断）
        # stat__value 元素上的 font-size / word-break / letter-spacing
        if 'stat__value' in context_classes:
            if prop_l in ('font-size', 'word-break', 'letter-spacing', 'color'):
                continue
        # --- 根据 KEEP_PROPS 决定是否保留 ---
        if prop_l in KEEP_PROPS:
            # 对特定属性进一步用 value 白名单过滤
            if prop_l in ALLOWED_VALUE_PATTERNS:
                if not re.match(ALLOWED_VALUE_PATTERNS[prop_l], val):
                    continue
            # 检查强制删除值
            if (prop_l, val) in FORCE_REMOVE_VALUES:
                continue
            declarations.append((prop, val))
        # 否则删除

    if not declarations:
        return ''
    return ';'.join(f'{p}:{v}' for p, v in declarations)


# --- 处理单行中所有 style="..." 属性（简单正则） ---
STYLE_RE = re.compile(r'style="([^"]*)"', re.IGNORECASE)

def process_line(line, filepath):
    """处理单行 HTML，返回修改后的行（可能没变化）"""

    # 判断是否是 adsbygoogle 广告位的 ins 元素 - 这类行不做任何 style 处理
    # 同时对 span 分隔符（|）也原样保留
    is_adsbygoogle = 'adsbygoogle' in line

    # 对 <span>|</span> 分隔符行（内容是 "|"），保留 style
    # 例如：<span style="color:var(--border);margin:0 6px">|</span>
    # 检测：行内有 ">" 后跟 "|" 或 "<span" + "|" 特征
    is_separator_span = bool(re.search(r'<span[^>]*>\s*\|\s*</span>', line))

    def _replace(m):
        style_val = m.group(1)
        # 广告位和分隔符不清理
        if is_adsbygoogle or is_separator_span:
            return m.group(0)

        # 获取上下文：tag name 和 class（从整行简单抓取）
        # 从该行抓取最近的 class 属性（粗粒度判断）
        tag_match = re.search(r'<(\w+)', line)
        tag = tag_match.group(1).lower() if tag_match else ''
        class_match = re.search(r'class="([^"]*)"', line)
        classes = class_match.group(1) if class_match else ''

        new_style = clean_style_attr(style_val, tag, classes)
        if not new_style:
            # 删除 style 属性后，避免留下难看的连续空白：
            # 若原匹配前后是空白/引号，外部已有的空格会让结果变成 " attr  >"
            # 在这里返回空字符串，调用方会产生 " class='x'  >"，后续统一清理双空格
            return ''
        return f'style="{new_style}"'

    result = STYLE_RE.sub(_replace, line)
    # 清理由于删除 style 属性后留下的多余连续空白
    # 例如 '<div class="x"  >'  -> '<div class="x">'
    #       '<div  style="x">' 原先是正常的，这里不处理（只有删除才会产生双空格）
    result = re.sub(r'[ \t]{2,}', ' ', result)
    # 清理标签内部的 "> " 之前的多余空格，即 "  >"  -> ">"
    result = re.sub(r' >', '>', result)
    return result


# --- 死代码删除：scientific-calculator.html 中 function appendToCurOrExpr ---
def remove_dead_function(html_text, func_name):
    """删除形如 "  function funcname(...){...}" 的整段函数"""
    # 用正则匹配从 "  function funcname(" 开始，到下一个 "  function " 或 </script>
    # 更稳妥：逐行处理括号平衡
    lines = html_text.split('\n')
    out_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        # 检测 "function funcname("
        m = re.match(r'^(\s*)function\s+' + re.escape(func_name) + r'\s*\(', line)
        if m:
            # 找到这个函数的结束：从这行开始，到括号平衡结束
            start_i = i
            indent = m.group(1)
            # 计算括号平衡
            brace_count = 0
            started = False
            j = i
            while j < len(lines):
                for ch in lines[j]:
                    if ch == '{':
                        brace_count += 1
                        started = True
                    elif ch == '}':
                        brace_count -= 1
                if started and brace_count <= 0:
                    break
                j += 1
            # 函数结束于行 j，跳过 [i, j]
            i = j + 1
            continue
        out_lines.append(line)
        i += 1
    return '\n'.join(out_lines)


# --- 面包屑修复 ---
def fix_breadcrumb(html_text, filepath):
    """根据文件所在子目录修改 breadcrumb 中的 <a href="../../index.html">XXX Tools</a>"""
    # 判断目录名
    dir_name = os.path.basename(os.path.dirname(filepath))
    mapping = {
        'calculator': ('Calculator Tools', '../../categories/calculator.html'),
        'generator': ('Generator Tools', '../../categories/generator.html'),
        'image': ('Image Tools', '../../categories/image.html'),
        'pdf': ('PDF Tools', '../../categories/pdf.html'),
        'text': ('Text Tools', '../../categories/text.html'),
    }
    if dir_name not in mapping:
        return html_text
    expected_text, new_href = mapping[dir_name]

    # 模式：<a href="../../index.html">XXX Tools</a>  → 改成对应分类页
    pattern = re.compile(
        r'<a\s+href="\.\./\.\./index\.html">(' + re.escape(expected_text) + r')</a>'
    )
    new_html = pattern.sub(f'<a href="{new_href}">{expected_text}</a>', html_text)

    # 额外：如果目录是 calculator/generator/image/pdf/text，
    # 但该文件本来就正确写了 "../../categories/XXX.html"（有些文件已正确），保持不变
    return new_html


# --- 处理单个 HTML 文件 ---
def process_html_file(filepath):
    """返回 (filepath, changed, notes)"""
    with open(filepath, 'r', encoding='utf-8') as f:
        original = f.read()

    html = original

    # 1) 删除 scientific-calculator.html 中死代码函数
    if filepath.endswith('scientific-calculator.html'):
        before = html
        html = remove_dead_function(html, 'appendToCurOrExpr')
        # 去掉被删除函数留下的连续空行（保持美观）
        html = re.sub(r'\n{3,}', '\n\n', html)
        dead_removed = (before != html)
    else:
        dead_removed = False

    # 2) 清理所有 style="..."
    before = html
    lines = html.split('\n')
    new_lines = [process_line(l, filepath) for l in lines]
    html = '\n'.join(new_lines)
    style_changed = (before != html)

    # 3) 修复面包屑链接
    before = html
    html = fix_breadcrumb(html, filepath)
    breadcrumb_changed = (before != html)

    changed = dead_removed or style_changed or breadcrumb_changed

    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)

    notes = []
    if dead_removed:
        notes.append('删除了死代码函数 appendToCurOrExpr')
    if style_changed:
        notes.append('清理了内联 style 属性')
    if breadcrumb_changed:
        notes.append('修复了面包屑分类链接')

    return filepath, changed, notes


# --- 遍历所有工具页面 html 文件 ---
def find_all_htmls():
    results = []
    for root, dirs, files in os.walk(TOOLS_DIR):
        # 仅处理具体分类子目录下的 html（跳过 tools/index.html）
        for name in files:
            if not name.endswith('.html'):
                continue
            full = os.path.join(root, name)
            # 过滤：只有在 calculator/generator/image/pdf/text 下的才算工具页面
            parent = os.path.basename(os.path.dirname(full))
            if parent in ('calculator', 'generator', 'image', 'pdf', 'text'):
                results.append(full)
    results.sort()
    return results


def main():
    htmls = find_all_htmls()
    print(f'共发现 {len(htmls)} 个工具页面 HTML 文件')
    changed_files = []
    for fp in htmls:
        filepath, changed, notes = process_html_file(fp)
        if changed:
            rel = os.path.relpath(filepath, os.path.dirname(TOOLS_DIR))
            print(f'  [修改] {rel}: {", ".join(notes)}')
            changed_files.append((rel, notes))
        else:
            rel = os.path.relpath(filepath, os.path.dirname(TOOLS_DIR))
            print(f'  [无变化] {rel}')
    print(f'\n合计修改 {len(changed_files)} 个文件')
    return 0


if __name__ == '__main__':
    sys.exit(main())
