#!/usr/bin/env python3
"""
修复文件输入按钮显示中文问题。
使用 CSS 隐藏原生文件输入，创建自定义按钮。
"""
import re
from pathlib import Path

ROOT = Path("/workspace")

FILE_UPLOAD_TOOLS = [
    "tools/pdf/merge-pdf.html",
    "tools/pdf/split-pdf.html",
    "tools/pdf/compress-pdf.html",
    "tools/pdf/jpg-to-pdf.html",
    "tools/image/image-compressor.html",
    "tools/image/image-converter.html",
    "tools/image/image-resizer.html",
    "tools/image/background-remover.html",
    "tools/generator/hash-generator.html",
]


def fix_file_input(filepath):
    html = filepath.read_text(encoding="utf-8")
    
    # 添加 CSS 到现有 style 块末尾
    custom_css = '''
    
    .file-input-wrapper {
      position: relative;
      display: inline-block;
      overflow: hidden;
    }
    .file-input-wrapper input[type="file"] {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      opacity: 0;
      cursor: pointer;
    }
    .file-input-btn {
      display: inline-flex;
      padding: 8px 16px;
      border-radius: 8px;
      font-size: .88rem;
      font-weight: 600;
      background: #2563eb;
      color: #fff;
      border: none;
      cursor: pointer;
      transition: background .2s;
    }
    .file-input-btn:hover {
      background: #1d4ed8;
    }
    '''
    
    if '</style>' in html:
        html = html.replace('</style>', custom_css + '\n</style>')
    else:
        html = html.replace('</head>', '  <style>' + custom_css + '</style>\n</head>')
    
    # 替换 input type="file" 为带包装器的形式
    pattern = r'<input\s+type="file"([^>]*)/?>'
    replacement = r'<div class="file-input-wrapper"><input type="file"\1/><button class="file-input-btn">Choose File</button></div>'
    html = re.sub(pattern, replacement, html)
    
    filepath.write_text(html, encoding="utf-8")
    return True


def main():
    print("=" * 60)
    print("修复文件输入按钮显示中文问题...")
    print("=" * 60)
    
    count = 0
    for tool_path in FILE_UPLOAD_TOOLS:
        filepath = ROOT / tool_path
        if not filepath.exists():
            print(f"  ⚠️  文件不存在: {tool_path}")
            continue
        
        if fix_file_input(filepath):
            count += 1
            print(f"  ✅ {tool_path}")
    
    print(f"\n修复了 {count} 个页面")
    print("\n" + "=" * 60)
    print("完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()