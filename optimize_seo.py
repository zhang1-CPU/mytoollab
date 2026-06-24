#!/usr/bin/env python3
import os
import re
import json
from pathlib import Path

BLOG_DIR = Path('/workspace/blog')
TOOLS_DIR = Path('/workspace/tools')

seo_configs = {
    'json-formatter-developers.html': {
        'title': 'JSON Formatter Online Free 2026: Step-by-Step Developer Guide | zlbox',
        'description': 'Free online JSON formatter and validator for developers. Pretty print, validate, minify, and debug JSON instantly. Step-by-step guide with best practices.',
        'keywords': 'json formatter, json validator, pretty print json, online json formatter, json beautifier, debug json, format json online, free json tool, json syntax checker, minify json, json tree view, 2026',
        'article_headline': 'JSON Formatter Online Free 2026: Step-by-Step Developer Guide',
        'article_description': 'Free online JSON formatter and validator for developers. Pretty print, validate, minify, and debug JSON instantly with step-by-step guidance.',
        'breadcrumb_name': 'JSON Formatter Guide 2026',
        'internal_links': [
            {'pattern': r'JSON formatter(?![^<]*</a>)', 'url': '../tools/text/json-formatter.html', 'text': 'JSON formatter', 'first_only': True},
            {'pattern': r'JSON validator(?![^<]*</a>)', 'url': '../tools/text/json-formatter.html', 'text': 'JSON validator', 'first_only': True},
            {'pattern': r'password generator(?![^<]*</a>)', 'url': '../tools/generator/password-generator.html', 'text': 'password generator', 'first_only': True},
        ],
        'lead_keyword': 'JSON formatter'
    },
    'how-to-compress-pdf.html': {
        'title': 'How to Compress PDF Free Online 2026: Step-by-Step Complete Guide | zlbox',
        'description': 'Learn how to compress PDF files without losing quality. Free online tool with step-by-step guide. Reduce PDF size 40-80% instantly for email and web.',
        'keywords': 'how to compress pdf, compress pdf free, reduce pdf size, pdf compression tool, online pdf compressor, shrink pdf, pdf size reducer, compress pdf online, best pdf compressor 2026, reduce pdf file size, pdf quality, email pdf',
        'article_headline': 'How to Compress PDF Free Online 2026: Step-by-Step Complete Guide',
        'article_description': 'Learn how to compress PDF files without losing quality. Free online tool with step-by-step guide to reduce PDF size instantly.',
        'breadcrumb_name': 'Compress PDF Guide 2026',
        'internal_links': [
            {'pattern': r'PDF compressor(?![^<]*</a>)', 'url': '../tools/pdf/compress-pdf.html', 'text': 'PDF compressor', 'first_only': True},
            {'pattern': r'Compress PDF(?![^<]*</a>)', 'url': '../tools/pdf/compress-pdf.html', 'text': 'Compress PDF', 'first_only': True},
            {'pattern': r'Merge PDF(?![^<]*</a>)', 'url': '../tools/pdf/merge-pdf.html', 'text': 'Merge PDF', 'first_only': True},
            {'pattern': r'Split PDF(?![^<]*</a>)', 'url': '../tools/pdf/split-pdf.html', 'text': 'Split PDF', 'first_only': True},
            {'pattern': r'image compressor(?![^<]*<)', 'url': '../tools/image/image-compressor.html', 'text': 'image compressor', 'first_only': True},
        ],
        'lead_keyword': 'compress PDF'
    },
    'password-security-guide.html': {
        'title': 'Strong Password Generator Free 2026: Complete Security Guide | zlbox',
        'description': 'Create strong, secure passwords with our free online generator. Complete security guide with best practices, tips, and step-by-step instructions for 2026.',
        'keywords': 'password generator, strong password, password security, secure password generator, free password maker, random password generator, create strong password, password strength, online password tool, 2026 security guide, password best practices',
        'article_headline': 'Strong Password Generator Free 2026: Complete Security Guide',
        'article_description': 'Create strong, secure passwords with our free online generator. Complete security guide with best practices and step-by-step instructions.',
        'breadcrumb_name': 'Password Security Guide 2026',
        'internal_links': [
            {'pattern': r'Password Generator(?![^<]*</a>)', 'url': '../tools/generator/password-generator.html', 'text': 'Password Generator', 'first_only': True},
            {'pattern': r'password generator(?![^<]*</a>)', 'url': '../tools/generator/password-generator.html', 'text': 'password generator', 'first_only': True},
            {'pattern': r'QR code(?![^<]*</a>)', 'url': '../tools/generator/qr-code-generator.html', 'text': 'QR code', 'first_only': True},
            {'pattern': r'UUID generator(?![^<]*</a>)', 'url': '../tools/generator/uuid-generator.html', 'text': 'UUID generator', 'first_only': True},
        ],
        'lead_keyword': 'strong password'
    },
    'qr-code-business.html': {
        'title': 'QR Code Generator Free for Business 2026: 10 Practical Ideas | zlbox',
        'description': 'Free QR code generator for business. Discover 10 practical ways to use QR codes for marketing, operations, and customer engagement in 2026.',
        'keywords': 'qr code generator, qr code business, qr code marketing, free qr code maker, qr code ideas, qr code uses, business qr codes, qr code generator online, custom qr code, 2026 qr code trends, qr code best practices',
        'article_headline': 'QR Code Generator Free for Business 2026: 10 Practical Ideas',
        'article_description': 'Free QR code generator for business. Discover 10 practical ways to use QR codes for marketing and customer engagement in 2026.',
        'breadcrumb_name': 'QR Code Business Guide 2026',
        'internal_links': [
            {'pattern': r'QR code generator(?![^<]*</a>)', 'url': '../tools/generator/qr-code-generator.html', 'text': 'QR code generator', 'first_only': True},
            {'pattern': r'QR-code scanner(?![^<]*</a>)', 'url': '../tools/generator/qr-code-scanner.html', 'text': 'QR-code scanner', 'first_only': True},
            {'pattern': r'password generator(?![^<]*</a>)', 'url': '../tools/generator/password-generator.html', 'text': 'password generator', 'first_only': True},
        ],
        'lead_keyword': 'QR code'
    },
    'password-security.html': {
        'title': 'Password Security Guide 2026: Strong Password Best Practices | zlbox',
        'description': 'Essential password security guide for 2026. Learn best practices for creating strong passwords, avoiding common mistakes, and protecting your online accounts.',
        'keywords': 'password security, strong password, password best practices, password safety, secure password tips, password protection, online security 2026, password strength guide, create secure password, password manager tips',
        'article_headline': 'Password Security Guide 2026: Strong Password Best Practices',
        'article_description': 'Essential password security guide for 2026. Learn best practices for creating strong passwords and protecting your online accounts.',
        'breadcrumb_name': 'Password Security 2026',
        'internal_links': [
            {'pattern': r'password generator(?![^<]*</a>)', 'url': '../tools/generator/password-generator.html', 'text': 'password generator', 'first_only': True},
            {'pattern': r'Password Generator(?![^<]*</a>)', 'url': '../tools/generator/password-generator.html', 'text': 'Password Generator', 'first_only': True},
            {'pattern': r'QR code(?![^<]*</a>)', 'url': '../tools/generator/qr-code-generator.html', 'text': 'QR code', 'first_only': True},
        ],
        'lead_keyword': 'password security'
    },
    'compress-pdf-email-guide.html': {
        'title': 'Compress PDF for Email Free Online 2026: Step-by-Step Guide | zlbox',
        'description': 'Compress PDF files for email attachments instantly. Free online tool with step-by-step guide. Reduce PDF size without losing quality in 2026.',
        'keywords': 'compress pdf for email, reduce pdf size email, pdf email attachment, compress pdf online, free pdf compressor, shrink pdf for email, pdf size reducer, optimize pdf for email, email pdf guide 2026, pdf compression tool',
        'article_headline': 'Compress PDF for Email Free Online 2026: Step-by-Step Guide',
        'article_description': 'Compress PDF files for email attachments instantly. Free online tool with step-by-step guide to reduce PDF size without losing quality.',
        'breadcrumb_name': 'PDF Email Guide 2026',
        'internal_links': [
            {'pattern': r'Compress PDF(?![^<]*</a>)', 'url': '../tools/pdf/compress-pdf.html', 'text': 'Compress PDF', 'first_only': True},
            {'pattern': r'PDF compressor(?![^<]*</a>)', 'url': '../tools/pdf/compress-pdf.html', 'text': 'PDF compressor', 'first_only': True},
            {'pattern': r'Merge PDF(?![^<]*</a>)', 'url': '../tools/pdf/merge-pdf.html', 'text': 'Merge PDF', 'first_only': True},
            {'pattern': r'image compressor(?![^<]*</a>)', 'url': '../tools/image/image-compressor.html', 'text': 'image compressor', 'first_only': True},
        ],
        'lead_keyword': 'compress PDF for email'
    },
    'image-compression-guide.html': {
        'title': 'Image Compression Free Online 2026: JPG PNG WebP Complete Guide | zlbox',
        'description': 'Free online image compression tool. Complete guide to JPG, PNG, and WebP compression. Reduce image size without losing quality for web use in 2026.',
        'keywords': 'image compression, compress image, image compressor, reduce image size, jpg compression, png optimization, webp guide, free image compressor, online image tool, compress photo, web optimization 2026, image size reducer',
        'article_headline': 'Image Compression Free Online 2026: JPG PNG WebP Complete Guide',
        'article_description': 'Free online image compression tool. Complete guide to JPG, PNG, and WebP compression. Reduce image size without losing quality.',
        'breadcrumb_name': 'Image Compression Guide 2026',
        'internal_links': [
            {'pattern': r'Image Compressor(?![^<]*</a>)', 'url': '../tools/image/image-compressor.html', 'text': 'Image Compressor', 'first_only': True},
            {'pattern': r'image compressor(?![^<]*</a>)', 'url': '../tools/image/image-compressor.html', 'text': 'image compressor', 'first_only': True},
            {'pattern': r'Image Converter(?![^<]*</a>)', 'url': '../tools/image/image-converter.html', 'text': 'Image Converter', 'first_only': True},
            {'pattern': r'Compress PDF(?![^<]*</a>)', 'url': '../tools/pdf/compress-pdf.html', 'text': 'Compress PDF', 'first_only': True},
        ],
        'lead_keyword': 'image compression'
    },
    'image-compression-web.html': {
        'title': 'Image Compression for Web Performance 2026: Free Online Tool Guide | zlbox',
        'description': 'Optimize images for faster website loading. Free online image compression tool with step-by-step guide to boost web performance in 2026.',
        'keywords': 'image compression web, web performance, optimize images, website speed, image optimizer, free online tool, compress images for web, web performance optimization, page speed, image optimization guide 2026, reduce page load time',
        'article_headline': 'Image Compression for Web Performance 2026: Free Online Tool Guide',
        'article_description': 'Optimize images for faster website loading. Free online image compression tool with step-by-step guide to boost web performance.',
        'breadcrumb_name': 'Web Image Optimization 2026',
        'internal_links': [
            {'pattern': r'image compressor(?![^<]*</a>)', 'url': '../tools/image/image-compressor.html', 'text': 'image compressor', 'first_only': True},
            {'pattern': r'image converter(?![^<]*</a>)', 'url': '../tools/image/image-converter.html', 'text': 'image converter', 'first_only': True},
            {'pattern': r'compress pdf(?![^<]*</a>)', 'url': '../tools/pdf/compress-pdf.html', 'text': 'compress PDF', 'first_only': True, 'flags': re.IGNORECASE},
        ],
        'lead_keyword': 'image compression for web'
    },
    'batch-image-processing.html': {
        'title': 'Batch Image Processing Free Online 2026: Complete Productivity Guide | zlbox',
        'description': 'Batch process dozens of images at once. Free online tools and complete guide to save hours on compression, resizing, and conversion in 2026.',
        'keywords': 'batch image processing, batch image compression, resize multiple images, bulk image editor, image processing tools, free online batch tool, productivity guide 2026, batch convert images, image resizer, compress multiple images',
        'article_headline': 'Batch Image Processing Free Online 2026: Complete Productivity Guide',
        'article_description': 'Batch process dozens of images at once. Free online tools and complete guide to save hours on compression and conversion.',
        'breadcrumb_name': 'Batch Image Processing 2026',
        'internal_links': [
            {'pattern': r'Image Compressor(?![^<]*</a>)', 'url': '../tools/image/image-compressor.html', 'text': 'Image Compressor', 'first_only': True},
            {'pattern': r'Image Resizer(?![^<]*</a>)', 'url': '../tools/image/image-resizer.html', 'text': 'Image Resizer', 'first_only': True},
            {'pattern': r'image converter(?![^<]*</a>)', 'url': '../tools/image/image-converter.html', 'text': 'image converter', 'first_only': True},
            {'pattern': r'compress pdf(?![^<]*</a>)', 'url': '../tools/pdf/compress-pdf.html', 'text': 'compress PDF', 'first_only': True, 'flags': re.IGNORECASE},
        ],
        'lead_keyword': 'batch image processing'
    },
    'pdf-tools-guide.html': {
        'title': 'Free PDF Tools Online 2026: Complete Guide for Professionals | zlbox',
        'description': 'Complete guide to free online PDF tools for professionals. Compress, merge, split, and convert PDFs with step-by-step instructions for 2026.',
        'keywords': 'pdf tools, pdf compressor, merge pdf, split pdf, free pdf tools, online pdf editor, pdf converter, professional pdf tools, 2026 pdf guide, pdf toolkit, pdf software free, document management',
        'article_headline': 'Free PDF Tools Online 2026: Complete Guide for Professionals',
        'article_description': 'Complete guide to free online PDF tools for professionals. Compress, merge, split, and convert PDFs with step-by-step instructions.',
        'breadcrumb_name': 'PDF Tools Guide 2026',
        'internal_links': [
            {'pattern': r'Compress PDF(?![^<]*</a>)', 'url': '../tools/pdf/compress-pdf.html', 'text': 'Compress PDF', 'first_only': True},
            {'pattern': r'Merge PDF(?![^<]*</a>)', 'url': '../tools/pdf/merge-pdf.html', 'text': 'Merge PDF', 'first_only': True},
            {'pattern': r'Split PDF(?![^<]*</a>)', 'url': '../tools/pdf/split-pdf.html', 'text': 'Split PDF', 'first_only': True},
            {'pattern': r'image compressor(?![^<]*</a>)', 'url': '../tools/image/image-compressor.html', 'text': 'image compressor', 'first_only': True},
        ],
        'lead_keyword': 'PDF tools'
    },
    'qr-code-types.html': {
        'title': 'QR Code Types Free Generator 2026: Complete Guide to All QR Types | zlbox',
        'description': 'Discover all QR code types and their uses. Free online QR code generator with complete guide for URL, vCard, WiFi, and more in 2026.',
        'keywords': 'qr code types, qr code generator, types of qr codes, url qr code, vcard qr, wifi qr code, free qr generator, qr code guide, qr code uses, custom qr code, 2026 qr guide, qr code data types',
        'article_headline': 'QR Code Types Free Generator 2026: Complete Guide to All QR Types',
        'article_description': 'Discover all QR code types and their uses. Free online QR code generator with complete guide for URL, vCard, WiFi, and more.',
        'breadcrumb_name': 'QR Code Types Guide 2026',
        'internal_links': [
            {'pattern': r'QR code generator(?![^<]*</a>)', 'url': '../tools/generator/qr-code-generator.html', 'text': 'QR code generator', 'first_only': True},
            {'pattern': r'QR code scanner(?![^<]*</a>)', 'url': '../tools/generator/qr-code-scanner.html', 'text': 'QR code scanner', 'first_only': True},
            {'pattern': r'password generator(?![^<]*</a>)', 'url': '../tools/generator/password-generator.html', 'text': 'password generator', 'first_only': True},
        ],
        'lead_keyword': 'QR code types'
    },
    'qr-code-types-guide.html': {
        'title': 'QR Code Types Complete Guide 2026: Free Generator for Every Use | zlbox',
        'description': 'Complete guide to every QR code type. Free online generator for URL, text, vCard, WiFi, email, and more. Step-by-step tutorial for 2026.',
        'keywords': 'qr code types guide, qr generator free, qr code tutorial, all qr code types, dynamic qr code, static qr code, qr code maker, free online qr tool, qr code 2026 guide, qr code explained, qr code use cases',
        'article_headline': 'QR Code Types Complete Guide 2026: Free Generator for Every Use',
        'article_description': 'Complete guide to every QR code type. Free online generator for URL, text, vCard, WiFi, and more with step-by-step tutorial.',
        'breadcrumb_name': 'QR Code Types Complete Guide 2026',
        'internal_links': [
            {'pattern': r'QR code generator(?![^<]*</a>)', 'url': '../tools/generator/qr-code-generator.html', 'text': 'QR code generator', 'first_only': True},
            {'pattern': r'QR code scanner(?![^<]*</a>)', 'url': '../tools/generator/qr-code-scanner.html', 'text': 'QR code scanner', 'first_only': True},
            {'pattern': r'UUID generator(?![^<]*</a>)', 'url': '../tools/generator/uuid-generator.html', 'text': 'UUID generator', 'first_only': True},
        ],
        'lead_keyword': 'QR code types'
    },
    'qr-code-marketing-ideas.html': {
        'title': 'QR Code Marketing Ideas 2026: Free Generator for Campaigns | zlbox',
        'description': 'Creative QR code marketing ideas for 2026. Free online QR code generator to boost engagement, track campaigns, and drive conversions.',
        'keywords': 'qr code marketing, qr code campaign, marketing qr codes, qr code ideas, qr code generator, digital marketing 2026, qr code engagement, qr code tracking, offline to online marketing, free qr maker, marketing strategy',
        'article_headline': 'QR Code Marketing Ideas 2026: Free Generator for Campaigns',
        'article_description': 'Creative QR code marketing ideas for 2026. Free online QR code generator to boost engagement, track campaigns, and drive conversions.',
        'breadcrumb_name': 'QR Code Marketing 2026',
        'internal_links': [
            {'pattern': r'QR code generator(?![^<]*</a>)', 'url': '../tools/generator/qr-code-generator.html', 'text': 'QR code generator', 'first_only': True},
            {'pattern': r'QR code scanner(?![^<]*</a>)', 'url': '../tools/generator/qr-code-scanner.html', 'text': 'QR code scanner', 'first_only': True},
            {'pattern': r'password generator(?![^<]*</a>)', 'url': '../tools/generator/password-generator.html', 'text': 'password generator', 'first_only': True},
        ],
        'lead_keyword': 'QR code marketing'
    },
    'age-calculator-uses.html': {
        'title': 'Age Calculator Online Free 2026: Practical Uses Complete Guide | zlbox',
        'description': 'Free online age calculator with practical uses. Calculate exact age in years, months, days instantly. Complete guide for everyday use in 2026.',
        'keywords': 'age calculator, calculate age, age calculator online, free age tool, age in days, birthday calculator, age finder, online age counter, 2026 age calculator, age difference calculator, exact age calculation',
        'article_headline': 'Age Calculator Online Free 2026: Practical Uses Complete Guide',
        'article_description': 'Free online age calculator with practical uses. Calculate exact age in years, months, days instantly with our complete guide.',
        'breadcrumb_name': 'Age Calculator Uses 2026',
        'internal_links': [
            {'pattern': r'age calculator(?![^<]*</a>)', 'url': '../tools/calculator/age-calculator.html', 'text': 'age calculator', 'first_only': True},
            {'pattern': r'BMI calculator(?![^<]*</a>)', 'url': '../tools/calculator/bmi-calculator.html', 'text': 'BMI calculator', 'first_only': True},
            {'pattern': r'percentage calculator(?![^<]*</a>)', 'url': '../tools/calculator/percentage-calculator.html', 'text': 'percentage calculator', 'first_only': True},
        ],
        'lead_keyword': 'age calculator'
    },
    'age-calculator-practical-uses.html': {
        'title': 'Age Calculator Practical Uses 2026: Free Online Tool Step-by-Step | zlbox',
        'description': 'Discover practical uses for a free online age calculator. Step-by-step guide to calculating age for planning, milestones, and everyday life in 2026.',
        'keywords': 'age calculator uses, practical age calculation, age calculator online, free age tool, birthday calculator, age planner, milestone calculator, age in years months days, 2026 guide, date difference calculator',
        'article_headline': 'Age Calculator Practical Uses 2026: Free Online Tool Step-by-Step',
        'article_description': 'Discover practical uses for a free online age calculator. Step-by-step guide to calculating age for planning and milestones.',
        'breadcrumb_name': 'Age Calculator Practical Uses 2026',
        'internal_links': [
            {'pattern': r'age calculator(?![^<]*</a>)', 'url': '../tools/calculator/age-calculator.html', 'text': 'age calculator', 'first_only': True},
            {'pattern': r'loan calculator(?![^<]*</a>)', 'url': '../tools/calculator/loan-calculator.html', 'text': 'loan calculator', 'first_only': True},
            {'pattern': r'BMI calculator(?![^<]*</a>)', 'url': '../tools/calculator/bmi-calculator.html', 'text': 'BMI calculator', 'first_only': True},
        ],
        'lead_keyword': 'age calculator'
    },
    'bmi-meaning-health.html': {
        'title': 'BMI Calculator Free Online 2026: Meaning and Health Complete Guide | zlbox',
        'description': 'Free online BMI calculator with complete guide. Understand BMI meaning, health ranges, and how to calculate your body mass index in 2026.',
        'keywords': 'bmi calculator, body mass index, bmi meaning, bmi calculator online, free bmi tool, bmi health guide, calculate bmi, bmi ranges, bmi chart 2026, health assessment, weight management tool',
        'article_headline': 'BMI Calculator Free Online 2026: Meaning and Health Complete Guide',
        'article_description': 'Free online BMI calculator with complete guide. Understand BMI meaning, health ranges, and how to calculate your body mass index.',
        'breadcrumb_name': 'BMI Health Guide 2026',
        'internal_links': [
            {'pattern': r'BMI calculator(?![^<]*</a>)', 'url': '../tools/calculator/bmi-calculator.html', 'text': 'BMI calculator', 'first_only': True},
            {'pattern': r'age calculator(?![^<]*</a>)', 'url': '../tools/calculator/age-calculator.html', 'text': 'age calculator', 'first_only': True},
            {'pattern': r'percentage calculator(?![^<]*</a>)', 'url': '../tools/calculator/percentage-calculator.html', 'text': 'percentage calculator', 'first_only': True},
        ],
        'lead_keyword': 'BMI calculator'
    },
    'percent-calculator-everyday.html': {
        'title': 'Percentage Calculator Free Online 2026: Everyday Uses Complete Guide | zlbox',
        'description': 'Free online percentage calculator for everyday use. Complete guide to calculating discounts, tips, interest, and more with step-by-step examples in 2026.',
        'keywords': 'percentage calculator, percent calculator, calculate percentage, discount calculator, tip calculator, interest calculator, free percent tool, online percentage calculator, everyday math 2026, percentage guide, sales tax calculator',
        'article_headline': 'Percentage Calculator Free Online 2026: Everyday Uses Complete Guide',
        'article_description': 'Free online percentage calculator for everyday use. Complete guide to calculating discounts, tips, interest, and more with step-by-step examples.',
        'breadcrumb_name': 'Percentage Calculator Guide 2026',
        'internal_links': [
            {'pattern': r'percentage calculator(?![^<]*</a>)', 'url': '../tools/calculator/percentage-calculator.html', 'text': 'percentage calculator', 'first_only': True},
            {'pattern': r'loan calculator(?![^<]*</a>)', 'url': '../tools/calculator/loan-calculator.html', 'text': 'loan calculator', 'first_only': True},
            {'pattern': r'BMI calculator(?![^<]*</a>)', 'url': '../tools/calculator/bmi-calculator.html', 'text': 'BMI calculator', 'first_only': True},
        ],
        'lead_keyword': 'percentage calculator'
    },
    'percentage-everyday-calculations.html': {
        'title': 'Everyday Percentage Calculations 2026: Free Online Calculator Guide | zlbox',
        'description': 'Master everyday percentage calculations with our free online calculator. Step-by-step guide for discounts, tips, taxes, and finance in 2026.',
        'keywords': 'everyday percentage, percentage calculations, percent calculator, free online tool, discount math, tip calculation, tax percentage, finance math, 2026 percentage guide, easy percentage, percentage formula',
        'article_headline': 'Everyday Percentage Calculations 2026: Free Online Calculator Guide',
        'article_description': 'Master everyday percentage calculations with our free online calculator. Step-by-step guide for discounts, tips, taxes, and finance.',
        'breadcrumb_name': 'Everyday Percentage Guide 2026',
        'internal_links': [
            {'pattern': r'percentage calculator(?![^<]*</a>)', 'url': '../tools/calculator/percentage-calculator.html', 'text': 'percentage calculator', 'first_only': True},
            {'pattern': r'loan calculator(?![^<]*</a>)', 'url': '../tools/calculator/loan-calculator.html', 'text': 'loan calculator', 'first_only': True},
            {'pattern': r'age calculator(?![^<]*</a>)', 'url': '../tools/calculator/age-calculator.html', 'text': 'age calculator', 'first_only': True},
        ],
        'lead_keyword': 'percentage calculations'
    },
    'data-privacy-tools.html': {
        'title': 'Data Privacy Tools Free Online 2026: Complete Security Guide | zlbox',
        'description': 'Protect your data with free online privacy tools. Complete guide to client-side processing, secure tools, and data protection best practices for 2026.',
        'keywords': 'data privacy tools, privacy tools online, data protection, online security tools, client-side processing, privacy guide 2026, secure online tools, data safety, privacy first tools, browser tools, online privacy',
        'article_headline': 'Data Privacy Tools Free Online 2026: Complete Security Guide',
        'article_description': 'Protect your data with free online privacy tools. Complete guide to client-side processing and data protection best practices for 2026.',
        'breadcrumb_name': 'Data Privacy Guide 2026',
        'internal_links': [
            {'pattern': r'password generator(?![^<]*</a>)', 'url': '../tools/generator/password-generator.html', 'text': 'password generator', 'first_only': True},
            {'pattern': r'JSON formatter(?![^<]*</a>)', 'url': '../tools/text/json-formatter.html', 'text': 'JSON formatter', 'first_only': True},
            {'pattern': r'QR code generator(?![^<]*</a>)', 'url': '../tools/generator/qr-code-generator.html', 'text': 'QR code generator', 'first_only': True},
        ],
        'lead_keyword': 'data privacy tools'
    },
    'browser-tools-privacy.html': {
        'title': 'Browser Privacy Tools Free 2026: Complete Online Security Guide | zlbox',
        'description': 'Secure browser-based privacy tools for 2026. Complete guide to protecting your data online with free client-side processing tools you can trust.',
        'keywords': 'browser privacy tools, browser-based tools, online privacy, secure browser tools, client-side tools, free privacy tools, 2026 security guide, online data protection, browser security, web tool privacy',
        'article_headline': 'Browser Privacy Tools Free 2026: Complete Online Security Guide',
        'article_description': 'Secure browser-based privacy tools for 2026. Complete guide to protecting your data online with free client-side processing tools.',
        'breadcrumb_name': 'Browser Privacy Guide 2026',
        'internal_links': [
            {'pattern': r'password generator(?![^<]*</a>)', 'url': '../tools/generator/password-generator.html', 'text': 'password generator', 'first_only': True},
            {'pattern': r'JSON formatter(?![^<]*</a>)', 'url': '../tools/text/json-formatter.html', 'text': 'JSON formatter', 'first_only': True},
            {'pattern': r'compress PDF(?![^<]*</a>)', 'url': '../tools/pdf/compress-pdf.html', 'text': 'compress PDF', 'first_only': True, 'flags': re.IGNORECASE},
        ],
        'lead_keyword': 'browser privacy tools'
    },
    'color-design-basics.html': {
        'title': 'Color Design Basics 2026: Free Online Color Picker Tool Guide | zlbox',
        'description': 'Master color design basics with our free online color picker. Complete guide for non-designers: color theory, palettes, and practical tips for 2026.',
        'keywords': 'color design basics, color picker, color theory, color palette, free color tool, online color picker, design basics 2026, color guide, web design colors, hex color picker, rgb color tool',
        'article_headline': 'Color Design Basics 2026: Free Online Color Picker Tool Guide',
        'article_description': 'Master color design basics with our free online color picker. Complete guide for non-designers: color theory, palettes, and practical tips.',
        'breadcrumb_name': 'Color Design Guide 2026',
        'internal_links': [
            {'pattern': r'color picker(?![^<]*</a>)', 'url': '../tools/image/color-picker.html', 'text': 'color picker', 'first_only': True},
            {'pattern': r'color converter(?![^<]*</a>)', 'url': '../tools/image/color-converter.html', 'text': 'color converter', 'first_only': True},
            {'pattern': r'image converter(?![^<]*</a>)', 'url': '../tools/image/image-converter.html', 'text': 'image converter', 'first_only': True},
        ],
        'lead_keyword': 'color design basics'
    },
}

def read_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            return f.read()

def write_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def update_title(html, new_title):
    pattern = r'<title>.*?</title>'
    return re.sub(pattern, f'<title>{new_title}</title>', html, flags=re.DOTALL)

def update_meta_description(html, new_description):
    pattern = r'<meta name="description" content=".*?"\s*/?>'
    return re.sub(pattern, f'<meta name="description" content="{new_description}" />', html)

def update_meta_keywords(html, new_keywords):
    pattern = r'<meta name="keywords" content=".*?"\s*/?>'
    return re.sub(pattern, f'<meta name="keywords" content="{new_keywords}" />', html)

def update_article_jsonld(html, headline, description):
    def replace_jsonld(match):
        json_str = match.group(1)
        try:
            data = json.loads(json_str)
            if data.get('@type') == 'Article':
                data['headline'] = headline
                data['description'] = description
            return f'<script type="application/ld+json">\n{json.dumps(data, ensure_ascii=False)}\n</script>'
        except json.JSONDecodeError:
            return match.group(0)
    
    pattern = r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>'
    return re.sub(pattern, replace_jsonld, html, flags=re.DOTALL)

def update_breadcrumb_jsonld(html, new_name):
    def replace_jsonld(match):
        json_str = match.group(1)
        try:
            data = json.loads(json_str)
            if data.get('@type') == 'BreadcrumbList':
                items = data.get('itemListElement', [])
                if items:
                    items[-1]['name'] = new_name
            return f'<script type="application/ld+json">\n{json.dumps(data, ensure_ascii=False)}\n</script>'
        except json.JSONDecodeError:
            return match.group(0)
    
    pattern = r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>'
    return re.sub(pattern, replace_jsonld, html, flags=re.DOTALL)

def add_internal_links(html, links_config):
    article_match = re.search(r'<article>(.*?)</article>', html, re.DOTALL)
    if not article_match:
        return html
    
    article_content = article_match.group(1)
    original_article = article_content
    
    for link_conf in links_config:
        pattern = link_conf['pattern']
        url = link_conf['url']
        text = link_conf['text']
        first_only = link_conf.get('first_only', True)
        flags = link_conf.get('flags', 0)
        
        count = 0
        def replace_link(match):
            nonlocal count
            if first_only and count > 0:
                return match.group(0)
            count += 1
            return f'<a href="{url}">{match.group(0)}</a>'
        
        try:
            article_content = re.sub(pattern, replace_link, article_content, flags=flags)
        except re.error:
            continue
    
    if article_content != original_article:
        html = html.replace(original_article, article_content)
    
    return html

def update_lead_paragraph(html, keyword):
    lead_match = re.search(r'(<p class="lead">)(.*?)(</p>)', html, re.DOTALL)
    if not lead_match:
        return html
    
    lead_content = lead_match.group(2)
    if keyword.lower() in lead_content.lower():
        return html
    
    words = lead_content.split()
    if len(words) > 10:
        insert_pos = len(words) // 3
        words.insert(insert_pos, f'A free {keyword} tool is essential —')
        new_lead = ' '.join(words)
    else:
        new_lead = lead_content + f' Use our free {keyword} for instant results.'
    
    html = html.replace(lead_match.group(0), f'{lead_match.group(1)}{new_lead}{lead_match.group(3)}')
    return html

def optimize_article(filepath, config):
    html = read_file(filepath)
    
    html = update_title(html, config['title'])
    html = update_meta_description(html, config['description'])
    html = update_meta_keywords(html, config['keywords'])
    html = update_article_jsonld(html, config['article_headline'], config['article_description'])
    html = update_breadcrumb_jsonld(html, config['breadcrumb_name'])
    html = add_internal_links(html, config['internal_links'])
    html = update_lead_paragraph(html, config['lead_keyword'])
    
    write_file(filepath, html)
    return True

def main():
    optimized_count = 0
    optimized_articles = []
    
    blog_files = sorted(BLOG_DIR.glob('*.html'))
    
    for filepath in blog_files:
        filename = filepath.name
        if filename == 'index.html':
            continue
        
        if filename in seo_configs:
            print(f'Optimizing: {filename}')
            try:
                optimize_article(filepath, seo_configs[filename])
                optimized_count += 1
                optimized_articles.append(seo_configs[filename]['article_headline'])
                print(f'  ✓ Done')
            except Exception as e:
                print(f'  ✗ Error: {e}')
        else:
            print(f'Skipping (no config): {filename}')
    
    print(f'\n{"="*60}')
    print(f'Total optimized articles: {optimized_count}')
    print(f'{"="*60}')
    for i, title in enumerate(optimized_articles, 1):
        print(f'{i}. {title}')

if __name__ == '__main__':
    main()
