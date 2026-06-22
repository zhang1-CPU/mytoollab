import os
import re

GA_CODE = '''\n  <script async src="https://www.googletagmanager.com/gtag/js?id=G-9V6L0Z956X"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-9V6L0Z956X');
  </script>'''

FILES = [
    'blog/age-calculator-uses.html',
    'blog/batch-image-processing.html',
    'blog/color-design-basics.html',
    'blog/data-privacy-tools.html',
    'blog/how-to-compress-pdf.html',
    'blog/image-compression-guide.html',
    'blog/json-formatter-developers.html',
    'blog/password-security.html',
    'blog/pdf-tools-guide.html',
    'blog/percent-calculator-everyday.html',
    'blog/qr-code-business.html',
    'blog/qr-code-types.html',
    'tools/calculator/age-calculator.html',
    'tools/generator/qr-code-generator.html',
    'tools/generator/qr-code-scanner.html',
    'tools/image/background-remover.html',
    'tools/image/color-converter.html',
    'tools/image/color-picker.html',
    'tools/image/image-compressor.html',
    'tools/image/image-converter.html',
    'tools/image/image-resizer.html',
    'tools/pdf/compress-pdf.html',
    'tools/pdf/jpg-to-pdf.html',
    'tools/pdf/merge-pdf.html',
    'tools/pdf/split-pdf.html',
    'tools/text/base64.html',
    'tools/text/case-converter.html',
    'tools/text/html-formatter.html',
    'tools/text/json-formatter.html',
    'tools/text/lorem-ipsum.html',
    'tools/text/remove-duplicates.html',
    'tools/text/sql-formatter.html',
    'tools/text/url-encoder.html',
    'tools/text/word-counter.html',
    'categories/calculator.html',
    'categories/generator.html',
    'categories/image.html',
    'categories/pdf.html',
    'categories/text.html',
    'tools/index.html',
    'about.html',
    'contact.html',
    'privacy.html',
    'disclaimer.html',
]

def add_ga_to_file(filepath):
    full_path = os.path.join(os.path.dirname(__file__), filepath)
    if not os.path.exists(full_path):
        print(f"❌ File not found: {filepath}")
        return False
    
    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'googletagmanager.com/gtag/js' in content:
        print(f"✅ GA already exists in: {filepath}")
        return False
    
    ads_pattern = re.compile(r'<script async src="https://pagead2\.googlesyndication\.com/pagead/js/adsbygoogle\.js\?client=ca-pub-5420550088713746"[^>]*></script>', re.DOTALL)
    match = ads_pattern.search(content)
    
    if match:
        new_content = content[:match.end()] + GA_CODE + content[match.end():]
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✓ Added GA to: {filepath}")
        return True
    else:
        head_end = content.find('</head>')
        if head_end != -1:
            new_content = content[:head_end] + GA_CODE + content[head_end:]
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✓ Added GA to: {filepath} (at </head>)")
            return True
        else:
            print(f"⚠️ No adsbygoogle script or </head> found in: {filepath}")
            return False

if __name__ == '__main__':
    print("Adding Google Analytics to HTML files...\n")
    modified_count = 0
    for filepath in FILES:
        if add_ga_to_file(filepath):
            modified_count += 1
    print(f"\n✅ Done! Modified {modified_count} files out of {len(FILES)}")
