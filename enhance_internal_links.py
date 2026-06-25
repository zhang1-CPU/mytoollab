#!/usr/bin/env python3
"""
增强 zlbox 博客文章的内链结构
"""

import os
import re
import random
from collections import defaultdict

BLOG_DIR = '/workspace/blog'

# 文章分类映射 - 基于文件名和内容
ARTICLE_CATEGORIES = {
    # Development 类
    'regex-tester-guide.html': {'cat': 'Development', 'title': 'Regex Tester: Complete Guide for Developers', 'date': 'June 24, 2026', 'read_time': '8 min read', 'excerpt': 'Master regular expressions with our comprehensive guide to testing and debugging regex patterns.'},
    'base64-encoding-guide.html': {'cat': 'Development', 'title': 'Base64 Encoding Explained: What It Is and When to Use It', 'date': 'June 23, 2026', 'read_time': '7 min read', 'excerpt': 'Learn what Base64 encoding is, how it works, and when to use encode and decode tools.'},
    'jwt-decoder-guide.html': {'cat': 'Development', 'title': 'JWT Decoder: How to Debug JSON Web Tokens', 'date': 'June 21, 2026', 'read_time': '6 min read', 'excerpt': 'Everything you need to know about decoding and debugging JSON Web Tokens safely.'},
    'sql-formatter-guide.html': {'cat': 'Development', 'title': 'SQL Formatter: Readable Queries for Better Database Work', 'date': 'June 20, 2026', 'read_time': '7 min read', 'excerpt': 'How SQL formatting improves readability, debugging, and team collaboration on database code.'},
    'uuid-generator-guide.html': {'cat': 'Development', 'title': 'UUID Generator: Everything You Need to Know', 'date': 'June 22, 2026', 'read_time': '6 min read', 'excerpt': 'Learn about UUID versions, use cases, and how to generate unique identifiers for your applications.'},
    'timestamp-converter-guide.html': {'cat': 'Development', 'title': 'Timestamp Converter: Unix Time Explained for Developers', 'date': 'June 18, 2026', 'read_time': '6 min read', 'excerpt': 'Understand Unix timestamps and how to convert between date formats in development work.'},
    'url-encoder-guide.html': {'cat': 'Development', 'title': 'URL Encoding: Why Spaces Become %20 (Complete Guide)', 'date': 'June 17, 2026', 'read_time': '6 min read', 'excerpt': 'Learn how URL percent-encoding works and why special characters need to be encoded.'},
    
    # Text & Data 类
    'json-formatter-developers.html': {'cat': 'Development', 'title': 'JSON Formatter: Essential Tool for Developers and Data Teams', 'date': 'May 25, 2026', 'read_time': '7 min read', 'excerpt': 'Why every developer needs a good JSON formatter for debugging, API development, and data analysis.'},
    'word-counter-guide.html': {'cat': 'Text Tools', 'title': 'Word Counter Tool: How to Track Writing Progress', 'date': 'June 16, 2026', 'read_time': '6 min read', 'excerpt': 'How word counters help writers, students, and professionals track writing goals and productivity.'},
    'text-case-converter-guide.html': {'cat': 'Text Tools', 'title': 'Text Case Converter: Uppercase, Lowercase, Title Case Explained', 'date': 'June 14, 2026', 'read_time': '5 min read', 'excerpt': 'When and how to use different text case formats for better readability and consistency.'},
    
    # Security & Privacy 类
    'password-security-guide.html': {'cat': 'Security', 'title': 'How to Create Strong Passwords: The Complete Security Guide', 'date': 'June 19, 2026', 'read_time': '9 min read', 'excerpt': 'Learn how to create strong, unique passwords for every account. Security best practices and common mistakes to avoid.'},
    'password-security.html': {'cat': 'Security', 'title': 'Strong Password Security Guide – How to Create Unbreakable Passwords', 'date': 'June 11, 2026', 'read_time': '7 min read', 'excerpt': 'How strong passwords are created, what makes a password secure, and common mistakes to avoid.'},
    'browser-tools-privacy.html': {'cat': 'Security', 'title': 'Browser Privacy Tools: Complete Online Security Guide', 'date': 'June 13, 2026', 'read_time': '7 min read', 'excerpt': 'How browser-based tools protect your privacy compared to cloud services that upload your data.'},
    'data-privacy-tools.html': {'cat': 'Privacy', 'title': 'Why Privacy-First Tools: Keeping Your Data Safe in 2026', 'date': 'June 9, 2026', 'read_time': '6 min read', 'excerpt': 'How browser-based tools protect your privacy compared to cloud services that upload your files.'},
    'data-privacy-tools-guide.html': {'cat': 'Privacy', 'title': 'Data Privacy Tools: How to Protect Your Information Online', 'date': 'June 7, 2026', 'read_time': '6 min read', 'excerpt': 'Essential privacy tools and practices for protecting your personal data online.'},
    
    # Image 类
    'image-compression-guide.html': {'cat': 'Images', 'title': 'Image Compression Guide: JPG vs PNG vs WebP Explained', 'date': 'June 3, 2026', 'read_time': '9 min read', 'excerpt': 'Understand JPG, PNG, and WebP differences, learn when to use each format, and pick the right compression settings.'},
    'image-compression-web.html': {'cat': 'Images', 'title': 'Image Compression for Web Performance: Complete Guide', 'date': 'May 28, 2026', 'read_time': '7 min read', 'excerpt': 'How image compression improves website speed and user experience without losing quality.'},
    'batch-image-processing.html': {'cat': 'Images', 'title': 'Batch Image Processing: Save Hours with These Tips', 'date': 'May 22, 2026', 'read_time': '6 min read', 'excerpt': 'Process dozens or hundreds of images efficiently. Tips for batch compressing, converting, and resizing images.'},
    'image-converter-guide.html': {'cat': 'Images', 'title': 'Image Converter: JPG, PNG, WebP – Which Format to Choose', 'date': 'May 20, 2026', 'read_time': '6 min read', 'excerpt': 'How to choose the right image format and convert between formats without losing quality.'},
    'image-resizer-guide.html': {'cat': 'Images', 'title': 'Image Resizer: How to Resize Images Without Losing Quality', 'date': 'May 18, 2026', 'read_time': '6 min read', 'excerpt': 'Learn the best practices for resizing images while maintaining quality and aspect ratio.'},
    
    # PDF 类
    'how-to-compress-pdf.html': {'cat': 'PDF', 'title': 'How to Compress PDF Files Without Losing Quality', 'date': 'June 10, 2026', 'read_time': '8 min read', 'excerpt': 'Learn how to compress PDF files while maintaining quality — best methods, tools, and tips for reducing file size.'},
    'pdf-tools-guide.html': {'cat': 'PDF', 'title': 'Complete Guide to PDF Tools Every Professional Needs', 'date': 'June 7, 2026', 'read_time': '7 min read', 'excerpt': 'Essential PDF tools every professional should know: compression, merging, splitting, and conversion.'},
    'compress-pdf-email-guide.html': {'cat': 'PDF', 'title': 'Compress PDF for Email: Step-by-Step Guide', 'date': 'June 5, 2026', 'read_time': '6 min read', 'excerpt': 'How to compress PDF files to fit within email attachment limits without losing quality.'},
    
    # Design 类
    'color-design-basics.html': {'cat': 'Design', 'title': 'Color Basics for Designers and Content Creators', 'date': 'May 6, 2026', 'read_time': '6 min read', 'excerpt': 'Understanding HEX, RGB, and HSL color formats. Practical color theory basics for non-designers.'},
    'color-picker-guide.html': {'cat': 'Design', 'title': 'Color Picker Guide: Choosing Colors for Web Design', 'date': 'May 10, 2026', 'read_time': '6 min read', 'excerpt': 'How to choose and use colors effectively in web design with color picker tools.'},
    'favicon-generator-guide.html': {'cat': 'Design', 'title': 'Favicon Generator: Complete Guide for Website Icons', 'date': 'May 12, 2026', 'read_time': '5 min read', 'excerpt': 'Everything you need to know about favicons: why they matter, how to create them, and best practices.'},
    'lorem-ipsum-guide.html': {'cat': 'Design', 'title': 'Lorem Ipsum Generator: Why Designers Use Placeholder Text', 'date': 'May 15, 2026', 'read_time': '5 min read', 'excerpt': 'Why designers and developers use lorem ipsum placeholder text and how to generate it.'},
    
    # Calculator 类
    'loan-calculator-guide.html': {'cat': 'Calculator', 'title': 'Loan Calculator: How to Understand Your Monthly Payments', 'date': 'June 15, 2026', 'read_time': '8 min read', 'excerpt': 'Learn how loan calculators work, how to calculate monthly payments, and understand interest and amortization.'},
    'percent-calculator-everyday.html': {'cat': 'Calculator', 'title': 'Everyday Uses for a Percentage Calculator', 'date': 'June 8, 2026', 'read_time': '5 min read', 'excerpt': 'How percentage calculators help with shopping, budgeting, tips, discounts, and financial planning.'},
    'percentage-everyday-calculations.html': {'cat': 'Calculator', 'title': 'Everyday Percentage Calculations: Complete Guide', 'date': 'May 25, 2026', 'read_time': '6 min read', 'excerpt': 'Practical percentage calculations everyone should know for daily life and personal finance.'},
    'age-calculator-uses.html': {'cat': 'Calculator', 'title': 'Uses for an Age Calculator: More Than Just Birthdays', 'date': 'June 12, 2026', 'read_time': '5 min read', 'excerpt': 'Creative and practical uses for age calculators beyond just finding out how old someone is.'},
    'age-calculator-practical-uses.html': {'cat': 'Calculator', 'title': 'Age Calculator Practical Uses: Complete Step-by-Step Guide', 'date': 'June 6, 2026', 'read_time': '5 min read', 'excerpt': 'Practical applications of age calculators for planning, milestones, and everyday calculations.'},
    'gst-calculator-guide.html': {'cat': 'Calculator', 'title': 'GST Calculator: Complete Guide for Small Businesses', 'date': 'May 30, 2026', 'read_time': '6 min read', 'excerpt': 'How GST calculators help small businesses with tax calculations, invoicing, and financial planning.'},
    'scientific-calculator-guide.html': {'cat': 'Calculator', 'title': 'Scientific Calculator: When to Use Advanced Math Features', 'date': 'May 27, 2026', 'read_time': '6 min read', 'excerpt': 'Understanding scientific calculator functions and when to use advanced math features.'},
    'bmi-meaning-health.html': {'cat': 'Health', 'title': 'BMI Calculator: Meaning and Health Complete Guide', 'date': 'June 4, 2026', 'read_time': '7 min read', 'excerpt': 'What BMI means, how to calculate it, and what it says about your health and fitness.'},
    
    # QR Code & Marketing 类
    'qr-code-marketing-ideas.html': {'cat': 'Marketing', 'title': 'QR Code Marketing for Small Business: 10 Creative Ideas', 'date': 'June 21, 2026', 'read_time': '7 min read', 'excerpt': 'Discover creative ways to use QR codes for small business marketing and customer engagement.'},
    'qr-code-business.html': {'cat': 'Marketing', 'title': '10 Practical Ways Businesses Can Use QR Codes in 2026', 'date': 'June 16, 2026', 'read_time': '7 min read', 'excerpt': 'Practical QR code applications for businesses of all sizes, from retail to services.'},
    'qr-code-types.html': {'cat': 'Marketing', 'title': 'Understanding Different Types of QR Codes: URL vs vCard WiFi and More', 'date': 'June 12, 2026', 'read_time': '7 min read', 'excerpt': 'A complete guide to different QR code types and when to use each one.'},
    'qr-code-types-guide.html': {'cat': 'Marketing', 'title': 'QR Code Types Complete Guide: Free Generator for Every Use', 'date': 'June 14, 2026', 'read_time': '7 min read', 'excerpt': 'Complete guide to QR code types: URL, vCard, WiFi, SMS, email, and more.'},
    
    # SEO & Productivity 类
    'meta-tag-generator-guide.html': {'cat': 'SEO', 'title': 'Meta Tag Generator: Complete SEO Guide for Better Rankings', 'date': 'May 20, 2026', 'read_time': '7 min read', 'excerpt': 'How meta tags affect SEO and how to generate effective meta tags for better search rankings.'},
    'no-signup-tools-guide.html': {'cat': 'Productivity', 'title': 'No Signup Tools: Why Browser-Based Apps Are the Future', 'date': 'June 2, 2026', 'read_time': '6 min read', 'excerpt': 'Why no-signup browser tools are more convenient, more private, and faster than traditional apps.'},
}

# 工具映射 - 按类别
TOOLS_BY_CATEGORY = {
    'Development': [
        {'href': '../tools/dev/regex-tester.html', 'name': 'Regex Tester', 'desc': 'Test & debug regex', 'ico': '/* */'},
        {'href': '../tools/dev/base64-encoder.html', 'name': 'Base64 Encoder', 'desc': 'Encode & decode', 'ico': '&#128290;'},
        {'href': '../tools/dev/jwt-decoder.html', 'name': 'JWT Decoder', 'desc': 'Decode JWT tokens', 'ico': '&#128273;'},
        {'href': '../tools/dev/sql-formatter.html', 'name': 'SQL Formatter', 'desc': 'Format SQL queries', 'ico': '&#128196;'},
        {'href': '../tools/text/json-formatter.html', 'name': 'JSON Formatter', 'desc': 'Pretty print JSON', 'ico': '&#123; &#125;'},
        {'href': '../tools/generator/uuid-generator.html', 'name': 'UUID Generator', 'desc': 'Generate unique IDs', 'ico': '&#9733;'},
        {'href': '../tools/dev/url-encoder.html', 'name': 'URL Encoder', 'desc': 'Encode & decode URLs', 'ico': '&#128279;'},
        {'href': '../tools/dev/timestamp-converter.html', 'name': 'Timestamp Converter', 'desc': 'Unix time converter', 'ico': '&#9201;'},
    ],
    'Text Tools': [
        {'href': '../tools/text/word-counter.html', 'name': 'Word Counter', 'desc': 'Count words & chars', 'ico': '&#128203;'},
        {'href': '../tools/text/case-converter.html', 'name': 'Case Converter', 'desc': 'Change text case', 'ico': '&#8597;'},
        {'href': '../tools/text/json-formatter.html', 'name': 'JSON Formatter', 'desc': 'Pretty print JSON', 'ico': '&#123; &#125;'},
        {'href': '../tools/text/lorem-ipsum.html', 'name': 'Lorem Ipsum Generator', 'desc': 'Placeholder text', 'ico': '&#128221;'},
    ],
    'Security': [
        {'href': '../tools/generator/password-generator.html', 'name': 'Password Generator', 'desc': 'Strong random passwords', 'ico': '&#128273;'},
        {'href': '../tools/dev/regex-tester.html', 'name': 'Regex Tester', 'desc': 'Test & debug regex', 'ico': '/* */'},
        {'href': '../tools/dev/jwt-decoder.html', 'name': 'JWT Decoder', 'desc': 'Decode JWT tokens', 'ico': '&#128273;'},
    ],
    'Privacy': [
        {'href': '../tools/generator/password-generator.html', 'name': 'Password Generator', 'desc': 'Strong random passwords', 'ico': '&#128273;'},
        {'href': '../tools/pdf/compress-pdf.html', 'name': 'Compress PDF', 'desc': 'Reduce PDF file size', 'ico': '&#128476;'},
        {'href': '../tools/image/image-compressor.html', 'name': 'Image Compressor', 'desc': 'Shrink photos & screenshots', 'ico': '&#128444;'},
        {'href': '../tools/dev/regex-tester.html', 'name': 'Regex Tester', 'desc': 'Test & debug regex', 'ico': '/* */'},
    ],
    'Images': [
        {'href': '../tools/image/image-compressor.html', 'name': 'Image Compressor', 'desc': 'Shrink images', 'ico': '&#128444;'},
        {'href': '../tools/image/image-resizer.html', 'name': 'Image Resizer', 'desc': 'Resize images', 'ico': '&#128260;'},
        {'href': '../tools/image/image-converter.html', 'name': 'Image Converter', 'desc': 'JPG / PNG / WebP', 'ico': '&#128257;'},
        {'href': '../tools/image/color-picker.html', 'name': 'Color Picker', 'desc': 'HEX / RGB / HSL', 'ico': '&#127912;'},
        {'href': '../tools/image/background-remover.html', 'name': 'Background Remover', 'desc': 'Transparent images', 'ico': '&#128445;'},
        {'href': '../tools/image/favicon-generator.html', 'name': 'Favicon Generator', 'desc': 'Website icons', 'ico': '&#128444;'},
    ],
    'PDF': [
        {'href': '../tools/pdf/compress-pdf.html', 'name': 'Compress PDF', 'desc': 'Reduce PDF file size', 'ico': '&#128476;'},
        {'href': '../tools/pdf/merge-pdf.html', 'name': 'Merge PDF', 'desc': 'Combine multiple PDFs', 'ico': '&#128228;'},
        {'href': '../tools/pdf/split-pdf.html', 'name': 'Split PDF', 'desc': 'Extract pages', 'ico': '&#9986;'},
        {'href': '../tools/image/image-compressor.html', 'name': 'Image Compressor', 'desc': 'Shrink photos & screenshots', 'ico': '&#128444;'},
        {'href': '../tools/image/image-resizer.html', 'name': 'Image Resizer', 'desc': 'Resize images', 'ico': '&#128260;'},
    ],
    'Design': [
        {'href': '../tools/image/color-picker.html', 'name': 'Color Picker', 'desc': 'HEX / RGB / HSL', 'ico': '&#127912;'},
        {'href': '../tools/image/favicon-generator.html', 'name': 'Favicon Generator', 'desc': 'Website icons', 'ico': '&#128444;'},
        {'href': '../tools/text/lorem-ipsum.html', 'name': 'Lorem Ipsum Generator', 'desc': 'Placeholder text', 'ico': '&#128221;'},
        {'href': '../tools/image/image-compressor.html', 'name': 'Image Compressor', 'desc': 'Shrink images', 'ico': '&#128444;'},
        {'href': '../tools/image/image-converter.html', 'name': 'Image Converter', 'desc': 'JPG / PNG / WebP', 'ico': '&#128257;'},
    ],
    'Calculator': [
        {'href': '../tools/calculator/loan-calculator.html', 'name': 'Loan Calculator', 'desc': 'Calculate payments', 'ico': '&#128176;'},
        {'href': '../tools/calculator/percent-calculator.html', 'name': 'Percent Calculator', 'desc': 'Calculate percentages', 'ico': '&#37;'},
        {'href': '../tools/calculator/age-calculator.html', 'name': 'Age Calculator', 'desc': 'Calculate age', 'ico': '&#127874;'},
        {'href': '../tools/calculator/bmi-calculator.html', 'name': 'BMI Calculator', 'desc': 'Calculate BMI', 'ico': '&#9878;'},
        {'href': '../tools/calculator/gst-calculator.html', 'name': 'GST Calculator', 'desc': 'Tax calculator', 'ico': '&#128176;'},
        {'href': '../tools/calculator/scientific-calculator.html', 'name': 'Scientific Calculator', 'desc': 'Advanced math', 'ico': '&#128428;'},
    ],
    'Health': [
        {'href': '../tools/calculator/bmi-calculator.html', 'name': 'BMI Calculator', 'desc': 'Calculate BMI', 'ico': '&#9878;'},
        {'href': '../tools/calculator/age-calculator.html', 'name': 'Age Calculator', 'desc': 'Calculate age', 'ico': '&#127874;'},
        {'href': '../tools/calculator/percent-calculator.html', 'name': 'Percent Calculator', 'desc': 'Calculate percentages', 'ico': '&#37;'},
    ],
    'Marketing': [
        {'href': '../tools/generator/qr-code-generator.html', 'name': 'QR Code Generator', 'desc': 'Create custom QR codes', 'ico': '&#128241;'},
        {'href': '../tools/generator/qr-code-scanner.html', 'name': 'QR Code Scanner', 'desc': 'Scan QR codes online', 'ico': '&#128269;'},
        {'href': '../tools/seo/meta-tag-generator.html', 'name': 'Meta Tag Generator', 'desc': 'SEO meta tags', 'ico': '&#128279;'},
        {'href': '../tools/generator/password-generator.html', 'name': 'Password Generator', 'desc': 'Strong random passwords', 'ico': '&#128273;'},
    ],
    'SEO': [
        {'href': '../tools/seo/meta-tag-generator.html', 'name': 'Meta Tag Generator', 'desc': 'SEO meta tags', 'ico': '&#128279;'},
        {'href': '../tools/text/word-counter.html', 'name': 'Word Counter', 'desc': 'Count words & chars', 'ico': '&#128203;'},
        {'href': '../tools/generator/qr-code-generator.html', 'name': 'QR Code Generator', 'desc': 'Create custom QR codes', 'ico': '&#128241;'},
        {'href': '../tools/image/favicon-generator.html', 'name': 'Favicon Generator', 'desc': 'Website icons', 'ico': '&#128444;'},
    ],
    'Productivity': [
        {'href': '../tools/pdf/compress-pdf.html', 'name': 'Compress PDF', 'desc': 'Reduce PDF file size', 'ico': '&#128476;'},
        {'href': '../tools/image/image-compressor.html', 'name': 'Image Compressor', 'desc': 'Shrink photos & screenshots', 'ico': '&#128444;'},
        {'href': '../tools/text/word-counter.html', 'name': 'Word Counter', 'desc': 'Count words & chars', 'ico': '&#128203;'},
        {'href': '../tools/calculator/percent-calculator.html', 'name': 'Percent Calculator', 'desc': 'Calculate percentages', 'ico': '&#37;'},
        {'href': '../tools/generator/password-generator.html', 'name': 'Password Generator', 'desc': 'Strong random passwords', 'ico': '&#128273;'},
    ],
}

# 全局计数器，用于跟踪每篇文章被链接的次数
link_counts = defaultdict(int)

def calculate_related_score(article_file, candidate_file):
    """计算两篇文章的相关性分数（0-100）"""
    article_info = ARTICLE_CATEGORIES.get(article_file, {})
    candidate_info = ARTICLE_CATEGORIES.get(candidate_file, {})
    
    score = 0
    
    # 同类别 +50分
    if article_info.get('cat') == candidate_info.get('cat'):
        score += 50
    
    # 标题关键词重叠度（最多30分）
    article_words = set(article_info.get('title', '').lower().split())
    candidate_words = set(candidate_info.get('title', '').lower().split())
    common_words = article_words & candidate_words
    # 过滤停用词
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'how', 'what', 'why', 'when', 'where', 'who', 'which', 'this', 'that', 'these', 'those', 'it', 'its', 'your', 'you', 'our', 'we', 'they', 'their', 'my', 'i', 'me', 'us', 'him', 'her', 'them', 'his', 'hers', 'ours', 'yours', 'theirs', 'guide', 'complete', 'free', 'online', 'tool', 'tools'}
    meaningful_common = common_words - stop_words
    score += min(30, len(meaningful_common) * 5)
    
    # 描述关键词重叠度（最多20分）
    article_desc_words = set(article_info.get('excerpt', '').lower().split())
    candidate_desc_words = set(candidate_info.get('excerpt', '').lower().split())
    common_desc_words = (article_desc_words & candidate_desc_words) - stop_words
    score += min(20, len(common_desc_words) * 2)
    
    return score

def get_related_articles(article_file):
    """为指定文章获取4篇最相关的文章，同时考虑内链分布均匀性"""
    article_info = ARTICLE_CATEGORIES.get(article_file, {})
    category = article_info.get('cat', '')
    
    # 相关类别映射
    related_categories = {
        'Development': ['Text Tools', 'Security', 'Privacy'],
        'Text Tools': ['Development', 'Productivity', 'Design'],
        'Security': ['Privacy', 'Development', 'Productivity'],
        'Privacy': ['Security', 'Productivity', 'Development'],
        'Images': ['Design', 'PDF', 'Productivity'],
        'PDF': ['Images', 'Productivity', 'Privacy'],
        'Design': ['Images', 'SEO', 'Marketing'],
        'Calculator': ['Productivity', 'Health'],
        'Health': ['Calculator', 'Productivity'],
        'Marketing': ['SEO', 'Design', 'Productivity'],
        'SEO': ['Marketing', 'Design', 'Text Tools'],
        'Productivity': ['Calculator', 'Images', 'PDF', 'Text Tools', 'Privacy'],
    }
    
    # 收集所有候选文章并计算分数
    candidates = []
    for f in ARTICLE_CATEGORIES:
        if f == article_file:
            continue
        
        # 基础相关性分数
        rel_score = calculate_related_score(article_file, f)
        
        # 内链分布调整：被链接次数少的文章加分
        # 每少一次链接加5分，最多加30分
        links = link_counts.get(f, 0)
        distribution_bonus = max(0, 30 - links * 5)
        
        total_score = rel_score + distribution_bonus
        candidates.append((f, total_score, rel_score))
    
    # 按总分排序
    candidates.sort(key=lambda x: (-x[1], -x[2]))
    
    # 选择前4篇
    selected = [c[0] for c in candidates[:4]]
    
    # 更新链接计数
    for f in selected:
        link_counts[f] += 1
    
    return selected

def get_tools_for_article(article_file):
    """为指定文章获取至少3个相关工具"""
    article_info = ARTICLE_CATEGORIES.get(article_file, {})
    category = article_info.get('cat', '')
    
    tools = TOOLS_BY_CATEGORY.get(category, [])
    
    # 如果工具少于3个，从相关类别补充
    if len(tools) < 3:
        related_cats = {
            'Health': ['Calculator'],
            'SEO': ['Marketing', 'Text Tools'],
        }
        for rel_cat in related_cats.get(category, []):
            tools.extend(TOOLS_BY_CATEGORY.get(rel_cat, []))
            if len(tools) >= 3:
                break
    
    return tools[:5]  # 最多5个

def build_related_articles_html(related_files):
    """构建 Related Articles 区块的 HTML"""
    html = '    <div class="related-articles">\n'
    for f in related_files:
        info = ARTICLE_CATEGORIES[f]
        html += f'      <a class="article-card" href="{f}"><span class="article-card__cat">{info["cat"]}</span><h3 class="article-card__title">{info["title"]}</h3><div class="article-card__date">{info["date"]} &middot; {info["read_time"]}</div><p class="article-card__excerpt">{info["excerpt"]}</p><span class="article-card__read">Read article &rarr;</span></a>\n'
    html += '    </div>'
    return html

def build_tools_html(tools):
    """构建 Tools Mentioned 区块的 HTML"""
    html = '    <div class="related-tools">\n'
    for tool in tools:
        html += f'      <a class="tool-card" href="{tool["href"]}"><span class="ico">{tool["ico"]}</span><span class="txt">{tool["name"]}<small>{tool["desc"]}</small></span></a>\n'
    html += '    </div>'
    return html

def update_article(file_path):
    """更新单篇文章的 Related Articles 和 Tools Mentioned 区块"""
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        content = f.read()
    
    filename = os.path.basename(file_path)
    if filename not in ARTICLE_CATEGORIES:
        return False
    
    # 获取相关文章
    related = get_related_articles(filename)
    related_html = build_related_articles_html(related)
    
    # 获取工具
    tools = get_tools_for_article(filename)
    tools_html = build_tools_html(tools)
    
    # 替换 Related Articles 区块
    related_pattern = r'<div class="container"><hr class="section-divider"><h2 class="section-title">Related Articles</h2>\s*<div class="related-articles">.*?</div>\s*</div>'
    related_replacement = f'<div class="container"><hr class="section-divider"><h2 class="section-title">Related Articles</h2>\n{related_html}\n  </div>'
    
    if re.search(related_pattern, content, re.DOTALL):
        content = re.sub(related_pattern, related_replacement, content, flags=re.DOTALL)
    else:
        print(f"  Warning: Could not find Related Articles section in {filename}")
        return False
    
    # 替换 Tools 区块 - 匹配各种可能的标题
    tools_pattern = r'<div class="container"><h2 class="section-title">(?:Tools Mentioned in This Article|Tools That Handle Batches|Tools .*?|Percentage Tools|QR Code Tools)</h2>\s*<div class="related-tools">.*?</div>\s*</div>'
    tools_replacement = f'<div class="container"><h2 class="section-title">Tools Mentioned in This Article</h2>\n{tools_html}\n  </div>'
    
    if re.search(tools_pattern, content, re.DOTALL):
        content = re.sub(tools_pattern, tools_replacement, content, flags=re.DOTALL)
    else:
        print(f"  Warning: Could not find Tools section in {filename}")
        return False
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def optimize_related_articles():
    """优化相关文章选择，确保内链分布均匀"""
    global link_counts
    
    best_related_map = None
    best_min_links = defaultdict(int)
    best_min_count = 0
    
    # 多轮迭代，寻找最佳分布
    for iteration in range(10):
        link_counts = defaultdict(int)
        
        # 每轮使用不同的随机种子
        random.seed(iteration)
        
        category_sizes = defaultdict(list)
        for f in ARTICLE_CATEGORIES:
            cat = ARTICLE_CATEGORIES[f]['cat']
            category_sizes[cat].append(f)
        
        # 随机打乱类别顺序和类别内的文章顺序
        categories = list(category_sizes.keys())
        random.shuffle(categories)
        
        processing_order = []
        for cat in categories:
            articles = category_sizes[cat][:]
            random.shuffle(articles)
            processing_order.extend(articles)
        
        related_map = {}
        for filename in processing_order:
            related_map[filename] = get_related_articles(filename)
        
        # 计算这一轮的分布
        current_counts = defaultdict(int)
        for filename in related_map:
            for r in related_map[filename]:
                current_counts[r] += 1
        
        min_count = min(current_counts.values()) if current_counts else 0
        
        # 如果这一轮的最小被链数更好，保存结果
        if min_count > best_min_count:
            best_min_count = min_count
            best_related_map = related_map
            best_min_links = current_counts
            
            # 如果已经达到3次以上，可以提前退出
            if min_count >= 3:
                break
    
    # 如果最佳结果不够好，进行后处理：为被链少的文章手动添加链接
    if best_min_count < 3:
        # 多轮后处理，直到所有文章都达到3次或无法再优化
        for round_num in range(5):
            low_linked = [f for f in best_min_links if best_min_links[f] < 3]
            if not low_linked:
                break
            
            # 按被链次数从少到多排序
            low_linked.sort(key=lambda f: best_min_links[f])
            
            for low_article in low_linked:
                if best_min_links[low_article] >= 3:
                    continue
                    
                needed = 3 - best_min_links[low_article]
                
                # 找出可以添加链接的文章
                # 优先从那些有很多链接的文章中替换
                candidates = []
                for filename in best_related_map:
                    if low_article in best_related_map[filename]:
                        continue
                        
                    current_related = best_related_map[filename]
                    if len(current_related) < 4:
                        continue
                        
                    # 计算当前列表中最后一篇的相关性
                    lowest_rel = calculate_related_score(filename, current_related[-1])
                    new_rel = calculate_related_score(filename, low_article)
                    
                    # 计算被替换文章的被链次数（高的优先替换
                    replace_count = best_min_links[current_related[-1]]
                    
                    # 评分：相关性差异越小越好，被替换文章被链次数越多越好
                    score = (replace_count * 2) - max(0, lowest_rel - new_rel)
                    candidates.append((filename, score, lowest_rel - new_rel))
                
                # 按评分排序
                candidates.sort(key=lambda x: (-x[1], x[2]))
                
                for filename, _, rel_diff in candidates:
                    if needed <= 0:
                        break
                        
                    # 只要相关性差异不超过25分，就替换
                    if rel_diff <= 25:
                        current_related = best_related_map[filename]
                        replaced = current_related[-1]
                        best_related_map[filename][-1] = low_article
                        best_min_links[low_article] += 1
                        best_min_links[replaced] -= 1
                        needed -= 1
    
    link_counts = best_min_links
    return best_related_map

def main():
    print("开始增强博客文章内链结构...")
    print(f"共有 {len(ARTICLE_CATEGORIES)} 篇文章需要处理")
    print()
    
    # 先优化相关文章选择
    print("优化内链分布...")
    related_map = optimize_related_articles()
    
    # 统计分布
    final_counts = defaultdict(int)
    for filename in related_map:
        for r in related_map[filename]:
            final_counts[r] += 1
    
    min_links = min(final_counts.values()) if final_counts else 0
    max_links = max(final_counts.values()) if final_counts else 0
    avg_links = sum(final_counts.values()) / len(final_counts) if final_counts else 0
    
    print(f"  最少被链次数: {min_links}")
    print(f"  最多被链次数: {max_links}")
    print(f"  平均被链次数: {avg_links:.1f}")
    print()
    
    # 现在实际更新文件
    updated = 0
    for filename in sorted(ARTICLE_CATEGORIES.keys()):
        file_path = os.path.join(BLOG_DIR, filename)
        if os.path.exists(file_path):
            # 直接使用优化后的相关文章
            related = related_map.get(filename, [])
            tools = get_tools_for_article(filename)
            
            # 读取文件
            with open(file_path, 'r', encoding='utf-8-sig') as f:
                content = f.read()
            
            # 构建 HTML
            related_html = build_related_articles_html(related)
            tools_html = build_tools_html(tools)
            
            # 替换 Related Articles 区块
            related_pattern = r'<div class="container"><hr class="section-divider"><h2 class="section-title">Related Articles</h2>\s*<div class="related-articles">.*?</div>\s*</div>'
            related_replacement = f'<div class="container"><hr class="section-divider"><h2 class="section-title">Related Articles</h2>\n{related_html}\n  </div>'
            
            if re.search(related_pattern, content, re.DOTALL):
                content = re.sub(related_pattern, related_replacement, content, flags=re.DOTALL)
            else:
                print(f"✗ {filename} - 找不到 Related Articles 区块")
                continue
            
            # 替换 Tools 区块 - 匹配各种可能的标题
            tools_pattern = r'<div class="container"><h2 class="section-title">(?:Tools Mentioned in This Article|Tools That Handle Batches|Tools .*?|Percentage Tools|QR Code Tools|Privacy-First Tools on This Site)</h2>\s*<div class="related-tools">.*?</div>\s*</div>'
            tools_replacement = f'<div class="container"><h2 class="section-title">Tools Mentioned in This Article</h2>\n{tools_html}\n  </div>'
            
            if re.search(tools_pattern, content, re.DOTALL):
                content = re.sub(tools_pattern, tools_replacement, content, flags=re.DOTALL)
            else:
                print(f"✗ {filename} - 找不到 Tools 区块")
                continue
            
            # 写入文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            updated += 1
            print(f"✓ {filename}")
            print(f"  相关文章: {len(related)} 篇, 工具: {len(tools)} 个")
        else:
            print(f"? {filename} - 文件不存在")
    
    print()
    print(f"完成！共更新了 {updated} 篇文章")
    
    # 列出被链次数少于3次的文章
    low_links = [f for f in final_counts if final_counts[f] < 3]
    if low_links:
        print()
        print(f"注意：仍有 {len(low_links)} 篇文章被链次数少于3次:")
        for f in sorted(low_links, key=lambda x: final_counts[x]):
            print(f"  - {f}: {final_counts[f]} 次")
    else:
        print()
        print("✓ 所有文章都至少被链接了3次！")

if __name__ == '__main__':
    main()
