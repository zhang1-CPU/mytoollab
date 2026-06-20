#!/usr/bin/env python3
"""
Fix bug: inline navigation JavaScript not wrapped in <script> tags.
This appears in ALL HTML files - the JS is rendered as plain text.
"""
import os
import sys

# The buggy pattern and the fix
BUGGY = '''  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5420550088713746" crossorigin="anonymous"></script>
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
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-9V6L0Z956X"></script>'''

FIXED = '''  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5420550088713746" crossorigin="anonymous"></script>
  <script>
(function() {
  var toggle = document.querySelector('.nav-toggle');
  var navLinks = document.querySelector('.nav-links');
  if (!toggle || !navLinks) return;
  toggle.addEventListener('click', function() {
    var isOpen = navLinks.classList.toggle('open');
    toggle.setAttribute('aria-expanded', isOpen);
  });
  var path = location.pathname;
  document.querySelectorAll('.nav-link').forEach(function(link) {
    var href = link.getAttribute('href');
    if (href && (path === href || path.indexOf(href.replace('/index.html','')) > -1)) {
      link.classList.add('active');
    }
  });
})();
  </script>
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-9V6L0Z956X"></script>'''

# Alternative version without the nav-toggle comment (for files that might have slightly different formatting)
BUGGY_ALT = '''  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5420550088713746" crossorigin="anonymous"></script>
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
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-9V6L0Z956X"></script>'''

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Try primary pattern
    if BUGGY in content:
        content = content.replace(BUGGY, FIXED)
        changed = True
    elif BUGGY_ALT in content:
        content = content.replace(BUGGY_ALT, FIXED)
        changed = True
    else:
        # Check if it's already fixed (has <script> before the IIFE)
        # Look for the bare comment without a <script> tag before it
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if '/* Navigation toggle for mobile */' in line:
                # Check if previous line ends with </script> or this is inside a <script> tag
                prev_line = lines[i-1] if i > 0 else ''
                if '</script>' not in prev_line and not prev_line.strip().startswith('<script'):
                    # Found the bug - need to find the full block and wrap it
                    # Find the end of the IIFE block
                    # Look for the next script tag (GA)
                    for j in range(i+1, len(lines)):
                        if 'www.googletagmanager.com' in lines[j]:
                            # Wrap from line i to line j-2 (the })(); line)
                            lines[i-1] = lines[i-1]  # this should be the adsense script end
                            # Insert <script> before the comment
                            lines[i] = '  <script>\n' + lines[i].replace('/* Navigation toggle for mobile */\n', '')
                            # Find the })(); line and add </script>
                            for k in range(i, j):
                                if lines[k].strip().startswith('})();'):
                                    lines[k] = lines[k] + '\n  </script>'
                                    break
                            break
                    changed = True
                    content = '\n'.join(lines)
                    break
        else:
            changed = False

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def find_html_files(root):
    html_files = []
    for dirpath, dirnames, filenames in os.walk(root):
        # Skip .git directory
        if '.git' in dirnames:
            dirnames.remove('.git')
        for filename in filenames:
            if filename.endswith('.html'):
                html_files.append(os.path.join(dirpath, filename))
    return sorted(html_files)

def main():
    root = '/workspace'
    files = find_html_files(root)
    print(f"Found {len(files)} HTML files to check\n")

    fixed_count = 0
    skipped = []
    for filepath in files:
        try:
            if fix_file(filepath):
                rel = os.path.relpath(filepath, root)
                print(f"  FIXED: {rel}")
                fixed_count += 1
            else:
                skipped.append(os.path.relpath(filepath, root))
        except Exception as e:
            print(f"  ERROR: {os.path.relpath(filepath, root)} - {e}")

    print(f"\nTotal files fixed: {fixed_count}")
    print(f"Files without bug pattern: {len(skipped)}")

if __name__ == '__main__':
    main()
