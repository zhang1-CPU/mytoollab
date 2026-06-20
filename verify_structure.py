#!/usr/bin/env python3
import os
import re
from urllib.parse import urlparse

TARGET_FILES = [
    "blog/index.html",
    "blog/age-calculator-uses.html",
    "blog/pdf-tools-guide.html",
    "blog/password-security.html",
    "blog/qr-code-business.html",
    "blog/qr-code-types.html",
    "blog/percent-calculator-everyday.html",
    "blog/image-compression-guide.html",
    "blog/how-to-compress-pdf.html",
    "blog/data-privacy-tools.html",
    "blog/batch-image-processing.html",
    "blog/color-design-basics.html",
    "blog/json-formatter-developers.html",
    "categories/text.html",
    "categories/calculator.html",
    "categories/generator.html",
    "categories/image.html",
    "categories/pdf.html",
    "about.html",
    "contact.html",
    "privacy.html",
    "disclaimer.html",
    "tools/index.html",
]

REQUIRED_NAV_KEYWORDS = ["All Tools", "Text", "Calculator", "Generator", "Image", "PDF", "Blog"]
REQUIRED_FOOTER_KEYWORDS = ["About", "Contact", "Privacy", "Disclaimer"]

VALID_FILES = set()
for root, dirs, files in os.walk("/workspace"):
    for f in files:
        full = os.path.join(root, f)
        rel = os.path.relpath(full, "/workspace").replace("\\", "/")
        VALID_FILES.add(rel)
        VALID_FILES.add("/" + rel)

def file_exists_relative(rel_path, source_file):
    """Check if a relative path exists, given source file location."""
    rel_path = rel_path.strip()
    if rel_path.startswith("http://") or rel_path.startswith("https://") or rel_path.startswith("#") or rel_path.startswith("mailto:") or rel_path.startswith("tel:"):
        return True
    if rel_path.startswith("/"):
        check = rel_path.lstrip("/")
        return check in [f.lstrip("/") for f in VALID_FILES] or os.path.exists(os.path.join("/workspace", check))
    source_dir = os.path.dirname(os.path.join("/workspace", source_file))
    candidate = os.path.normpath(os.path.join(source_dir, rel_path)).replace("\\", "/")
    workspace = os.path.normpath("/workspace").replace("\\", "/")
    if candidate.startswith(workspace):
        rel = candidate[len(workspace):].lstrip("/")
        return rel in VALID_FILES or os.path.exists(candidate)
    return False

def check_file(rel_path):
    findings = []
    full_path = os.path.join("/workspace", rel_path)
    if not os.path.exists(full_path):
        findings.append("FILE NOT FOUND")
        return findings
    with open(full_path, "r", encoding="utf-8") as f:
        content = f.read()
    lower = content.lower()

    # 1. DOCTYPE
    doctype_match = re.search(r'<!\s*doctype\s+html[^>]*>', content, re.IGNORECASE)
    if not doctype_match:
        findings.append("No DOCTYPE declaration")
    elif doctype_match.group(0) != "<!DOCTYPE html>":
        findings.append(f"DOCTYPE case/style issue: '{doctype_match.group(0)[:50]}'")

    # 2. HTML structure
    if not re.search(r'<html[\s>]', content, re.IGNORECASE):
        findings.append("Missing <html> tag")
    if not re.search(r'<head[\s>]', content, re.IGNORECASE):
        findings.append("Missing <head> tag")
    if not re.search(r'<body[\s>]', content, re.IGNORECASE):
        findings.append("Missing <body> tag")

    # 3. Navigation bar with 7 links
    nav_found = False
    for kw in REQUIRED_NAV_KEYWORDS:
        if kw.lower() not in lower:
            findings.append(f"Navigation missing keyword: '{kw}'")
            nav_found = True
    if not nav_found:
        pass

    # 4. CSS references
    css_refs = re.findall(r'<link[^>]+href=["\']([^"\']+\.css[^"\']*)["\'][^>]*>', content, re.IGNORECASE)
    for css in css_refs:
        clean = css.split("?")[0]
        if not file_exists_relative(clean, rel_path):
            findings.append(f"Broken CSS reference: '{css}'")

    # 5. meta robots
    if not re.search(r'<meta[^>]+name=["\']robots["\'][^>]*/?>', content, re.IGNORECASE):
        findings.append("Missing meta robots tag")

    # 6. meta description
    if not re.search(r'<meta[^>]+name=["\']description["\'][^>]*/?>', content, re.IGNORECASE):
        findings.append("Missing meta description tag")

    # 7. Footer with correct links
    footer_section = re.search(r'<footer[^>]*>(.*?)</footer>', content, re.IGNORECASE | re.DOTALL)
    if footer_section:
        footer_text = footer_section.group(1).lower()
        for kw in REQUIRED_FOOTER_KEYWORDS:
            if kw.lower() not in footer_text:
                findings.append(f"Footer missing keyword: '{kw}'")
    else:
        findings.append("Missing <footer> tag")

    # 8. Broken relative links
    all_links = re.findall(r'<a[^>]+href=["\']([^"\']*)["\'][^>]*>', content, re.IGNORECASE)
    for link in all_links:
        if not link:
            continue
        if link.startswith("http") or link.startswith("#") or link.startswith("mailto:") or link.startswith("tel:") or link.startswith("javascript:"):
            continue
        if link.startswith("/"):
            check = link.lstrip("/").split("#")[0].split("?")[0]
            if check and not os.path.exists(os.path.join("/workspace", check)):
                findings.append(f"Broken absolute link: '{link}'")
        else:
            clean_link = link.split("#")[0].split("?")[0]
            if clean_link and not file_exists_relative(clean_link, rel_path):
                findings.append(f"Broken relative link: '{link}'")

    # 9. HTML entity issues
    # Check text content for naked & and < that aren't tags
    # Remove HTML tags first to be safe
    text_only = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
    text_only = re.sub(r'<script[^>]*>.*?</script>', '', text_only, flags=re.IGNORECASE | re.DOTALL)
    text_only = re.sub(r'<style[^>]*>.*?</style>', '', text_only, flags=re.IGNORECASE | re.DOTALL)
    
    # Find potential naked & (not part of &entity;)
    bad_ampersand = re.findall(r'&(?!#?[a-zA-Z0-9]+;)(?![\w\s;])', text_only)
    # Check for stray < not followed by letter/!/?
    bad_lt = re.findall(r'<(?![a-zA-Z!/\?])', text_only)
    
    if bad_ampersand:
        # Be more specific - find in real text, not in URLs or attributes
        # Check in attribute values
        attr_bad = re.findall(r'="([^"]*[^&][^"]*&[^"][^"]*)"', text_only)
        findings.append(f"Potential unescaped '&' characters ({len(bad_ampersand)} matches)")
    if bad_lt:
        findings.append(f"Potential unescaped '<' characters ({len(bad_lt)} matches)")

    # 10. Canonical URL
    if not re.search(r'<link[^>]+rel=["\']canonical["\'][^>]*/?>', content, re.IGNORECASE):
        findings.append("Missing canonical URL")

    return findings

print("=" * 80)
print("AUTOMATED STRUCTURE & SEO VERIFICATION REPORT")
print("=" * 80)
print()

total_issues = 0
files_with_issues = 0

for rel in TARGET_FILES:
    issues = check_file(rel)
    if issues:
        print(f"\n[{rel}]")
        for issue in issues:
            print(f"  - {issue}")
        total_issues += len(issues)
        files_with_issues += 1
    else:
        print(f"\n[{rel}] - OK")

print()
print("=" * 80)
print(f"SUMMARY: {files_with_issues} files with issues, {total_issues} total issues")
print(f"Checked {len(TARGET_FILES)} files")
print("=" * 80)
