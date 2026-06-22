#!/usr/bin/env python3
"""
修复浏览器本地化导致的文件选择器显示中文问题。
解决方案：用 CSS 隐藏原生文件输入框，创建自定义按钮覆盖在上面。
"""
import re
from pathlib import Path

ROOT = Path("/workspace")

# 需要修复的工具页面
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
    """修复单个文件的文件输入按钮"""
    html = filepath.read_text(encoding="utf-8")
    
    # 查找原生文件输入
    # 模式: <input type="file" ... />
    pattern = r'<input\s+type="file"[^>]*\/?>'
    
    matches = list(re.finditer(pattern, html))
    if not matches:
        return False
    
    # 创建自定义文件输入包装器
    for match in matches:
        original_input = match.group(0)
        
        # 创建包装器
        wrapped = f'''
<div class="custom-file-input">
  {original_input}
  <button type="button" class="file-input-btn">Choose File</button>
  <span class="file-input-label">No file chosen</span>
</div>'''
        
        html = html.replace(original_input, wrapped, 1)
    
    # 添加 CSS 样式
    custom_css = '''
/* Custom File Input */
.custom-file-input {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  position: relative;
}
.custom-file-input input[type="file"] {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
}
.file-input-btn {
  padding: 8px 16px;
  border-radius: var(--radius-sm);
  font-size: .88rem;
  font-weight: 600;
  background: var(--brand);
  color: #fff;
  border: none;
  cursor: pointer;
  transition: background .2s;
}
.file-input-btn:hover {
  background: var(--brand-hover);
}
.file-input-label {
  font-size: .88rem;
  color: var(--muted);
  min-width: 120px;
  text-align: left;
}
'''
    
    # 添加 CSS 到 style 块末尾
    if '<style>' in html and '</style>' in html:
        html = html.replace('</style>', '\n' + custom_css + '\n</style>', 1)
    else:
        # 添加到 head 末尾
        head_end = html.find("</head>")
        if head_end != -1:
            html = html[:head_end] + f'\n  <style>\n{custom_css}</style>\n' + html[head_end:]
    
    # 添加 JavaScript 更新标签文本
    update_js = '''
/* Update file input label */
document.querySelectorAll('.custom-file-input').forEach(function(wrapper) {
  var input = wrapper.querySelector('input[type="file"]');
  var label = wrapper.querySelector('.file-input-label');
  var btn = wrapper.querySelector('.file-input-btn');
  
  if (input && label) {
    input.addEventListener('change', function() {
      if (this.files && this.files.length > 0) {
        if (this.files.length === 1) {
          label.textContent = this.files[0].name;
        } else {
          label.textContent = this.files.length + ' files selected';
        }
      } else {
        label.textContent = 'No file chosen';
      }
    });
    
    if (btn) {
      btn.addEventListener('click', function() {
        input.click();
      });
    }
  }
});
'''
    
    # 添加 JS
    if '</script>' in html:
        html = html.replace('</script>', '</script>\n' + update_js, 1)
    else:
        head_end = html.find("</head>")
        if head_end != -1:
            html = html[:head_end] + f'\n  <script>{update_js}</script>\n' + html[head_end:]
    
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