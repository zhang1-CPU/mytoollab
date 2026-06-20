#!/usr/bin/env python3
"""
Add HowTo structured data to all tool pages for rich snippets.
"""

import os
import re

# HowTo schemas for each tool category
HOWTO_SCHEMAS = {
    "json-formatter": {
        "name": "How to Use JSON Formatter",
        "steps": [
            {"name": "Paste your JSON", "text": "Copy your JSON data and paste it into the input box above."},
            {"name": "Click Format", "text": "Click the 'Format' button to beautify your JSON with proper indentation."},
            {"name": "Copy the result", "text": "Click 'Copy' to copy the formatted JSON to your clipboard."}
        ]
    },
    "word-counter": {
        "name": "How to Use Word Counter",
        "steps": [
            {"name": "Paste or type text", "text": "Enter or paste your text into the input box."},
            {"name": "View statistics", "text": "Instantly see word count, character count, sentence count, and paragraph count."},
            {"name": "Copy or clear", "text": "Copy your text or clear the input to start over."}
        ]
    },
    "html-formatter": {
        "name": "How to Use HTML Formatter",
        "steps": [
            {"name": "Paste HTML code", "text": "Paste your HTML code into the input box."},
            {"name": "Format or minify", "text": "Click 'Format' for pretty-printed code or 'Minify' for compact output."},
            {"name": "Copy the result", "text": "Click 'Copy' to copy the formatted HTML to your clipboard."}
        ]
    },
    "sql-formatter": {
        "name": "How to Use SQL Formatter",
        "steps": [
            {"name": "Paste SQL query", "text": "Paste your SQL query into the input box."},
            {"name": "Format your SQL", "text": "Click 'Format' to beautify your SQL with proper indentation."},
            {"name": "Copy the result", "text": "Click 'Copy' to copy the formatted SQL query."}
        ]
    },
    "base64": {
        "name": "How to Use Base64 Encoder/Decoder",
        "steps": [
            {"name": "Enter text", "text": "Enter the text you want to encode or decode."},
            {"name": "Choose action", "text": "Click 'Encode' to convert to Base64 or 'Decode' to convert from Base64."},
            {"name": "Copy result", "text": "Click 'Copy' to copy the result to your clipboard."}
        ]
    },
    "url-encoder": {
        "name": "How to Use URL Encoder/Decoder",
        "steps": [
            {"name": "Enter URL or text", "text": "Enter the URL or text string you want to encode or decode."},
            {"name": "Choose action", "text": "Click 'Encode' for URL encoding or 'Decode' to reverse it."},
            {"name": "Copy result", "text": "Click 'Copy' to copy the result to your clipboard."}
        ]
    },
    "html-encoder": {
        "name": "How to Use HTML Encoder/Decoder",
        "steps": [
            {"name": "Enter HTML", "text": "Enter the HTML content you want to encode or decode."},
            {"name": "Choose action", "text": "Click 'Encode' to convert special characters to HTML entities or 'Decode' to reverse."},
            {"name": "Copy result", "text": "Click 'Copy' to copy the result to your clipboard."}
        ]
    },
    "case-converter": {
        "name": "How to Use Case Converter",
        "steps": [
            {"name": "Enter text", "text": "Enter the text you want to convert to different cases."},
            {"name": "Choose case type", "text": "Select the desired case: uppercase, lowercase, camelCase, snake_case, etc."},
            {"name": "Copy result", "text": "Click 'Copy' to copy the converted text."}
        ]
    },
    "lorem-ipsum": {
        "name": "How to Use Lorem Ipsum Generator",
        "steps": [
            {"name": "Set parameters", "text": "Choose the number of paragraphs, sentences, or words you need."},
            {"name": "Generate text", "text": "Click 'Generate' to create placeholder text."},
            {"name": "Copy or customize", "text": "Copy the generated text or regenerate with different settings."}
        ]
    },
    "remove-duplicates": {
        "name": "How to Remove Duplicate Lines",
        "steps": [
            {"name": "Paste your text", "text": "Paste your text containing duplicate lines into the input box."},
            {"name": "Remove duplicates", "text": "Click 'Remove Duplicates' to automatically remove duplicate lines."},
            {"name": "Copy result", "text": "Click 'Copy' to copy the deduplicated text."}
        ]
    },
    "csv-to-json": {
        "name": "How to Convert CSV to JSON",
        "steps": [
            {"name": "Paste CSV data", "text": "Paste your CSV data into the input box."},
            {"name": "Convert to JSON", "text": "Click 'Convert' to transform CSV to JSON format."},
            {"name": "Copy or format", "text": "Copy the JSON result or use the formatter for pretty-printing."}
        ]
    },
    "number-base-converter": {
        "name": "How to Use Number Base Converter",
        "steps": [
            {"name": "Enter number", "text": "Enter the number you want to convert."},
            {"name": "Select base", "text": "Choose the source base (Binary, Decimal, Hex, Octal)."},
            {"name": "View conversions", "text": "Instantly see the number converted to all bases."}
        ]
    },
    # Calculator tools
    "age-calculator": {
        "name": "How to Calculate Age",
        "steps": [
            {"name": "Enter birth date", "text": "Enter your birth date using the date picker."},
            {"name": "View your age", "text": "See your exact age in years, months, days, hours, and minutes."},
            {"name": "Calculate another", "text": "Clear and enter a different date to calculate another age."}
        ]
    },
    "percentage-calculator": {
        "name": "How to Calculate Percentages",
        "steps": [
            {"name": "Enter values", "text": "Enter the numbers for your percentage calculation."},
            {"name": "Choose calculation type", "text": "Select: X is what % of Y, X% of Y is, or percentage change."},
            {"name": "View result", "text": "See the calculated result instantly."}
        ]
    },
    "basic-calculator": {
        "name": "How to Use Basic Calculator",
        "steps": [
            {"name": "Enter numbers", "text": "Click number buttons or use your keyboard to enter numbers."},
            {"name": "Select operation", "text": "Choose addition, subtraction, multiplication, or division."},
            {"name": "Get result", "text": "Click '=' to see the calculation result."}
        ]
    },
    "scientific-calculator": {
        "name": "How to Use Scientific Calculator",
        "steps": [
            {"name": "Enter calculation", "text": "Use the keypad or keyboard to enter your mathematical expression."},
            {"name": "Use advanced functions", "text": "Access trigonometric, logarithmic, and other scientific functions."},
            {"name": "Get result", "text": "Press Enter or '=' to calculate the result."}
        ]
    },
    "bmi-calculator": {
        "name": "How to Calculate BMI",
        "steps": [
            {"name": "Enter measurements", "text": "Enter your height and weight using your preferred unit system."},
            {"name": "Select unit system", "text": "Choose metric (kg/cm) or imperial (lb/ft-in)."},
            {"name": "View BMI result", "text": "See your BMI value and health category."}
        ]
    },
    "loan-calculator": {
        "name": "How to Calculate Loan Payments",
        "steps": [
            {"name": "Enter loan details", "text": "Enter the loan amount, interest rate, and loan term."},
            {"name": "Calculate", "text": "Click 'Calculate' to see monthly payment and total cost."},
            {"name": "Adjust and compare", "text": "Modify values to compare different loan scenarios."}
        ]
    },
    "unit-converter": {
        "name": "How to Use Unit Converter",
        "steps": [
            {"name": "Select category", "text": "Choose the type of units: length, weight, temperature, etc."},
            {"name": "Enter value", "text": "Enter the value you want to convert."},
            {"name": "View conversions", "text": "See instant conversions across multiple unit systems."}
        ]
    },
    # Generator tools
    "password-generator": {
        "name": "How to Generate a Strong Password",
        "steps": [
            {"name": "Set password length", "text": "Choose the length of your password (12-64 characters recommended)."},
            {"name": "Choose options", "text": "Select character types: uppercase, lowercase, numbers, symbols."},
            {"name": "Generate and copy", "text": "Click 'Generate' to create a password, then copy it."}
        ]
    },
    "qr-code-generator": {
        "name": "How to Generate a QR Code",
        "steps": [
            {"name": "Enter content", "text": "Enter the URL, text, or data you want in the QR code."},
            {"name": "Customize (optional)", "text": "Adjust size, color, and error correction level."},
            {"name": "Download QR code", "text": "Click 'Download' to save the QR code image."}
        ]
    },
    "qr-code-scanner": {
        "name": "How to Scan a QR Code",
        "steps": [
            {"name": "Upload image", "text": "Upload an image file containing a QR code."},
            {"name": "Scan automatically", "text": "The QR code content is automatically detected and decoded."},
            {"name": "Copy or open", "text": "Copy the decoded content or open URLs directly."}
        ]
    },
    "uuid-generator": {
        "name": "How to Generate UUIDs",
        "steps": [
            {"name": "Set quantity", "text": "Choose how many UUIDs you want to generate (1-100)."},
            {"name": "Select version", "text": "Choose UUID version (v4 recommended for random UUIDs)."},
            {"name": "Generate and copy", "text": "Click 'Generate' and copy the UUIDs."}
        ]
    },
    "hash-generator": {
        "name": "How to Generate Hashes",
        "steps": [
            {"name": "Enter text", "text": "Enter the text you want to hash."},
            {"name": "Select algorithm", "text": "Choose hash algorithm: MD5, SHA-1, SHA-256, SHA-512."},
            {"name": "View hash", "text": "See the generated hash value."}
        ]
    },
    "random-number-generator": {
        "name": "How to Generate Random Numbers",
        "steps": [
            {"name": "Set range", "text": "Define the minimum and maximum values for your random number."},
            {"name": "Set quantity", "text": "Choose how many random numbers to generate."},
            {"name": "Generate", "text": "Click 'Generate' to get your random numbers."}
        ]
    },
    "pomodoro-timer": {
        "name": "How to Use Pomodoro Timer",
        "steps": [
            {"name": "Set timer", "text": "Set work duration (default 25 min) and break duration (default 5 min)."},
            {"name": "Start timer", "text": "Click 'Start' to begin the Pomodoro session."},
            {"name": "Take breaks", "text": "Timer alerts you when to work and when to take breaks."}
        ]
    },
    "what-is-my-ip": {
        "name": "How to Find Your IP Address",
        "steps": [
            {"name": "Visit this page", "text": "This page automatically displays your public IP address."},
            {"name": "View details", "text": "See additional connection information including ISP and location."},
            {"name": "Copy IP", "text": "Click 'Copy' to copy your IP address."}
        ]
    },
    # Image tools
    "image-compressor": {
        "name": "How to Compress Images",
        "steps": [
            {"name": "Upload image", "text": "Drag and drop or select an image file (JPG, PNG, WebP)."},
            {"name": "Adjust quality", "text": "Use the slider to set compression level."},
            {"name": "Download compressed", "text": "Click 'Download' to save the compressed image."}
        ]
    },
    "image-converter": {
        "name": "How to Convert Images",
        "steps": [
            {"name": "Upload image", "text": "Select an image file to convert."},
            {"name": "Choose format", "text": "Select the output format: JPG, PNG, WebP, or GIF."},
            {"name": "Download converted", "text": "Click 'Download' to save the converted image."}
        ]
    },
    "image-resizer": {
        "name": "How to Resize Images",
        "steps": [
            {"name": "Upload image", "text": "Select an image file to resize."},
            {"name": "Set dimensions", "text": "Enter new width and height, or choose a preset."},
            {"name": "Download resized", "text": "Click 'Download' to save the resized image."}
        ]
    },
    "background-remover": {
        "name": "How to Remove Image Background",
        "steps": [
            {"name": "Upload image", "text": "Select an image with a background you want to remove."},
            {"name": "Automatic removal", "text": "The tool automatically detects and removes the background."},
            {"name": "Download result", "text": "Click 'Download' to save the image with transparent background."}
        ]
    },
    "color-picker": {
        "name": "How to Use Color Picker",
        "steps": [
            {"name": "Pick a color", "text": "Click anywhere on the color wheel or enter color values."},
            {"name": "View color codes", "text": "See HEX, RGB, HSL, and other color format values."},
            {"name": "Copy color code", "text": "Click any color code to copy it to your clipboard."}
        ]
    },
    "color-converter": {
        "name": "How to Convert Colors",
        "steps": [
            {"name": "Enter color", "text": "Enter a color in any format: HEX, RGB, or HSL."},
            {"name": "View conversions", "text": "Instantly see the color converted to all formats."},
            {"name": "Copy formats", "text": "Click 'Copy' next to any format to copy it."}
        ]
    },
    # PDF tools
    "compress-pdf": {
        "name": "How to Compress PDF",
        "steps": [
            {"name": "Upload PDF", "text": "Select or drag and drop your PDF file."},
            {"name": "Choose compression", "text": "Select compression level: low, medium, or high."},
            {"name": "Download compressed", "text": "Click 'Download' to save the compressed PDF."}
        ]
    },
    "merge-pdf": {
        "name": "How to Merge PDF Files",
        "steps": [
            {"name": "Upload PDFs", "text": "Select multiple PDF files to merge."},
            {"name": "Reorder files", "text": "Drag to reorder the files in your preferred sequence."},
            {"name": "Download merged", "text": "Click 'Download' to save the combined PDF."}
        ]
    },
    "split-pdf": {
        "name": "How to Split PDF",
        "steps": [
            {"name": "Upload PDF", "text": "Select a PDF file to split."},
            {"name": "Choose pages", "text": "Select specific pages or page ranges to extract."},
            {"name": "Download split", "text": "Click 'Download' to save the extracted pages."}
        ]
    },
    "jpg-to-pdf": {
        "name": "How to Convert JPG to PDF",
        "steps": [
            {"name": "Upload images", "text": "Select one or more JPG images to convert."},
            {"name": "Arrange order", "text": "Drag to reorder images if needed."},
            {"name": "Download PDF", "text": "Click 'Download' to save images as a PDF."}
        ]
    }
}

def get_tool_key(filename):
    """Extract tool key from filename."""
    return filename.replace('.html', '')

def create_howto_jsonld(schema):
    """Create HowTo JSON-LD script."""
    steps = []
    for i, step in enumerate(schema['steps'], 1):
        steps.append({
            "@type": "HowToStep",
            "name": step['name'],
            "text": step['text'],
            "position": i
        })

    howto = {
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": schema['name'],
        "description": f"Step by step guide: {schema['name']}",
        "step": steps
    }

    import json
    return f'<script type="application/ld+json">{json.dumps(howto, indent=2)}</script>'

def add_howto_to_file(filepath, tool_key):
    """Add HowTo schema to a single file."""
    if tool_key not in HOWTO_SCHEMAS:
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if HowTo schema already exists
    if '"@type": "HowTo"' in content:
        return False

    schema = HOWTO_SCHEMAS[tool_key]
    howto_jsonld = create_howto_jsonld(schema)

    # Find the closing </head> tag and insert before it
    if '</head>' in content:
        content = content.replace('</head>', f'\n  {howto_jsonld}\n</head>')

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True

    return False

def main():
    """Main function to add HowTo schemas to all tool pages."""
    tools_dir = '/workspace/tools'

    # Process all tool pages
    count = 0
    for root, dirs, files in os.walk(tools_dir):
        for filename in files:
            if filename.endswith('.html'):
                filepath = os.path.join(root, filename)
                tool_key = get_tool_key(filename)

                if add_howto_to_file(filepath, tool_key):
                    print(f"Added HowTo schema: {filename}")
                    count += 1

    print(f"\nTotal: {count} files updated with HowTo schema")

if __name__ == '__main__':
    main()
