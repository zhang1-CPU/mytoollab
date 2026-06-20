#!/usr/bin/env python3
"""Comprehensive HTML bug fix script for zlbox website."""
import os
import re
import glob

ROOT = os.path.dirname(os.path.abspath(__file__))

def fix_orphaned_related_heading(filepath):
    """Fix orphaned 'Related tools' heading — move heading from orphan position to just above related-grid."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Pattern 1: The orphan heading before <section class="tool-info" ...>
    # Try various whitespace patterns
    pattern1 = re.compile(
        r'<div class="section">\s*\n\s*<h2>Related tools</h2>\s*\n\s*\n',
        re.MULTILINE
    )
    if pattern1.search(content):
        content = pattern1.sub('', content, count=1)

        # Now wrap the related-grid with a proper section + heading
        pattern2 = re.compile(r'(\n\s*)<div class="related-grid">')
        match2 = pattern2.search(content)
        if match2:
            indent = match2.group(1).rstrip('\n') + ' ' if len(match2.group(1).strip()) == 0 else match2.group(1).rstrip('\n')
            # Find the right indent: use the whitespace before the div
            indent_str = ''
            # Check existing whitespace style by looking at other headings on the page
            m = re.search(r'(\n[ \t]*)<h2>', content)
            if m:
                indent_str = m.group(1)
            else:
                indent_str = '\n '

            replacement = f'{indent_str}<div class="section">{indent_str}<h2>Related tools</h2>{indent_str}<div class="related-grid">'
            content = pattern2.sub(replacement, content, count=1)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def fix_faq_section_class(filepath):
    """Replace 'faq-section' with 'faq' to match the canonical CSS class name."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content
    content = content.replace('class="faq-section"', 'class="faq"')
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def fix_pomodoro_breadcrumb(filepath):
    """Fix pomodoro-timer.html breadcrumb which links to password-generator."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content
    # The breadcrumb links to password-generator.html but we're on pomodoro-timer.html
    # Fix: make the breadcrumb consistent - the last item should point to itself
    content = content.replace(
        'breadcrumb-item">Password Generator',
        'breadcrumb-item">Pomodoro Timer'
    )
    content = content.replace(
        'breadcrumb-item active">Password Generator',
        'breadcrumb-item active">Pomodoro Timer'
    )
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def fix_htmlformatter_style_css(filepath):
    """Fix html-formatter.html which references non-existent 'style.css'."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content
    # Remove any reference to non-existent style.css in the head
    content = re.sub(
        r'<link[^>]*href=["\']style\.css["\'][^>]*>\s*\n?',
        '',
        content
    )
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def fix_content_page_footer(filepath):
    """Fix footer templates on content pages (about, contact, privacy, disclaimer) to be consistent."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content

    # Find the footer section and replace with a consistent one
    # Pattern: any footer with "All rights reserved" type text but incomplete link list
    # Let's look for the footer pattern with minimal links
    footer_pattern = re.compile(
        r'<footer[^>]*>.*?</footer>',
        re.DOTALL
    )

    # Standard footer used across the site
    standard_footer = """<footer class="footer">
<div class="container">
 <p>&copy; 2025 zlbox. All rights reserved.</p>
 <div class="footer-links">
  <a href="about.html">About</a>
  <a href="contact.html">Contact</a>
  <a href="privacy.html">Privacy</a>
  <a href="disclaimer.html">Disclaimer</a>
 </div>
</div>
</footer>"""

    match = footer_pattern.search(content)
    if match:
        old_footer = match.group(0)
        # Check if this footer has minimal links (less than 4)
        if old_footer.count('<a href') < 4 or 'footer-links' not in old_footer:
            content = content.replace(old_footer, standard_footer)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def normalize_doctype(filepath):
    """Change <!doctype html> (lowercase) to <!DOCTYPE html>."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content
    # Only match lowercase doctype at the start
    content = re.sub(
        r'^<!doctype html>',
        '<!DOCTYPE html>',
        content,
        count=1,
        flags=re.IGNORECASE
    )
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def main():
    stats = {
        'related_heading': 0,
        'faq_section': 0,
        'pomodoro_breadcrumb': 0,
        'htmlformatter_css': 0,
        'content_footer': 0,
        'doctype': 0,
    }
    files_fixed = set()

    # Scan all tool pages + content pages + blog pages
    all_html = []
    all_html.extend(glob.glob(os.path.join(ROOT, 'tools/**/*.html'), recursive=True))
    all_html.extend(glob.glob(os.path.join(ROOT, '*.html')))
    all_html.extend(glob.glob(os.path.join(ROOT, 'blog/*.html')))

    print(f"Scanning {len(all_html)} HTML files...\n")

    for fp in sorted(all_html):
        rel = os.path.relpath(fp, ROOT)

        # Fix 1: orphaned Related tools heading (all tool pages typically)
        if fix_orphaned_related_heading(fp):
            stats['related_heading'] += 1
            files_fixed.add(rel)
            print(f"  ✓ {rel} - Fixed Related tools heading position")

        # Fix 2: faq-section -> faq class name
        if fix_faq_section_class(fp):
            stats['faq_section'] += 1
            files_fixed.add(rel)
            print(f"  ✓ {rel} - Renamed faq-section -> faq")

        # Fix 3: pomodoro-timer breadcrumb
        if 'pomodoro-timer' in fp and fix_pomodoro_breadcrumb(fp):
            stats['pomodoro_breadcrumb'] += 1
            files_fixed.add(rel)
            print(f"  ✓ {rel} - Fixed breadcrumb (Password Generator -> Pomodoro Timer)")

        # Fix 4: html-formatter style.css reference
        if 'html-formatter' in fp and fix_htmlformatter_style_css(fp):
            stats['htmlformatter_css'] += 1
            files_fixed.add(rel)
            print(f"  ✓ {rel} - Removed non-existent style.css reference")

        # Fix 5: content page footer templates (about, contact, privacy, disclaimer)
        basename = os.path.basename(fp)
        if basename in ('about.html', 'contact.html', 'privacy.html', 'disclaimer.html'):
            if fix_content_page_footer(fp):
                stats['content_footer'] += 1
                files_fixed.add(rel)
                print(f"  ✓ {rel} - Standardized footer template")

        # Fix 6: normalize DOCTYPE (lowercase to uppercase)
        if normalize_doctype(fp):
            stats['doctype'] += 1
            files_fixed.add(rel)
            print(f"  ✓ {rel} - Normalized DOCTYPE to uppercase")

    print(f"\n{'=' * 60}")
    print("SUMMARY:")
    print(f"  Related tools heading fix:     {stats['related_heading']} files")
    print(f"  faq-section class rename:      {stats['faq_section']} files")
    print(f"  Pomodoro breadcrumb fix:       {stats['pomodoro_breadcrumb']} files")
    print(f"  HTML formatter style.css fix:  {stats['htmlformatter_css']} files")
    print(f"  Content page footer fix:       {stats['content_footer']} files")
    print(f"  DOCTYPE normalization:         {stats['doctype']} files")
    print(f"  Total unique files modified:   {len(files_fixed)} files")
    print(f"{'=' * 60}")


if __name__ == '__main__':
    main()
