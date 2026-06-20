#!/usr/bin/env python3
"""
P1: 为每个工具页面添加 SEO 内容区块:
1. "What is [Tool]?" - 工具说明
2. "How to use" - 使用步骤
3. "Use cases" - 使用场景
4. FAQ section (3-5 个问题)
5. 每个工具页末尾添加 FAQPage schema

这些内容会插入到 "Related tools" 区块之前。
使用 details/summary HTML 元素（可折叠 FAQ）。
"""
import os
import re
import json
from pathlib import Path

ROOT = Path("/workspace")
SITE_BASE = "https://www.zlbox.site"

# 每个工具的专属内容
TOOL_CONTENT = {
    # ===== CALCULATOR =====
    "age-calculator.html": {
        "category": "Calculator",
        "what": "An age calculator determines the exact age of a person or entity from a given birth date to today's date or any target date. It calculates the total years, months, days, and even hours or minutes between two dates.",
        "how": [
            "Enter the birth date in the day, month, and year fields.",
            "Optionally enter today's date or a target date.",
            "The calculator instantly displays your exact age in years, months, and days.",
        ],
        "usecases": [
            "Calculating a person's exact age for official documents and forms.",
            "Finding out how many days until a birthday, anniversary, or event.",
            "Verifying age eligibility for services, subscriptions, or legal requirements.",
            "Tracking the age of historical landmarks, buildings, or companies.",
        ],
        "faqs": [
            {"q": "Is the age calculation accurate for leap years?", "a": "Yes. The calculator accounts for leap years and all calendar variations to provide an exact age in years, months, and days."},
            {"q": "Can I calculate age at a future date?", "a": "Yes. Simply enter the birth date and a future target date to see how old someone will be on that specific day."},
            {"q": "How do I calculate age in months or days only?", "a": "The result shows years, months, and days together. The total number of days is also displayed for precision."},
        ]
    },
    "basic-calculator.html": {
        "category": "Calculator",
        "what": "A basic online calculator performs fundamental arithmetic operations — addition, subtraction, multiplication, and division — directly in your browser. No app download or internet connection required after the page loads.",
        "how": [
            "Click the number buttons or use your keyboard to enter a value.",
            "Click an operation (+, -, ×, ÷) to set the calculation.",
            "Click '=' or press Enter to see the result.",
            "Use 'C' to clear and 'CE' to backspace.",
        ],
        "usecases": [
            "Quick everyday math — shopping totals, splitting bills, tip calculations.",
            "Home improvement and construction measurements.",
            "Budget planning and expense tracking.",
            "Homework and study assistance for students.",
        ],
        "faqs": [
            {"q": "Can I use keyboard shortcuts?", "a": "Yes. Use your number pad or keyboard numbers, and standard operators (+, -, *, /) for calculations. Press Enter for '=' and Escape to clear."},
            {"q": "Does it handle decimal numbers?", "a": "Yes. Click the '.' button or press '.' on your keyboard to enter decimal values."},
            {"q": "What happens if I divide by zero?", "a": "The calculator displays an error message. Dividing by zero is mathematically undefined."},
        ]
    },
    "bmi-calculator.html": {
        "category": "Calculator",
        "what": "A BMI (Body Mass Index) calculator estimates body fat based on your height and weight. It provides a numerical score that categorizes you as underweight, normal weight, overweight, or obese, serving as a general health screening tool.",
        "how": [
            "Select your measurement unit system (Metric or Imperial).",
            "Enter your height and weight.",
            "Click 'Calculate' to see your BMI score and category.",
            "Review the BMI chart for context and understanding.",
        ],
        "usecases": [
            "General health and fitness assessment during wellness checkups.",
            "Setting fitness goals and tracking weight management progress.",
            "Pre-insurance or pre-employment health screening reference.",
            "Educational purposes for understanding body composition metrics.",
        ],
        "faqs": [
            {"q": "Is BMI an accurate measure of health?", "a": "BMI is a general screening tool. It doesn't distinguish between muscle and fat mass, so athletes and elderly individuals may have misleading scores. Always consult a healthcare professional for personal health assessment."},
            {"q": "What are the BMI categories?", "a": "Under 18.5: Underweight | 18.5–24.9: Normal | 25–29.9: Overweight | 30+: Obese. These ranges apply to most adults aged 20+."},
            {"q": "Does the calculator work for children?", "a": "This calculator uses standard adult BMI categories. For children and teens (under 20), age and gender-specific percentiles should be used instead."},
        ]
    },
    "loan-calculator.html": {
        "category": "Calculator",
        "what": "A loan calculator computes monthly mortgage or loan payments based on the loan amount, interest rate, and loan term. It also generates a full amortization schedule showing how each payment splits between principal and interest over time.",
        "how": [
            "Enter the loan amount (principal).",
            "Input the annual interest rate as a percentage.",
            "Set the loan term in months or years.",
            "Click 'Calculate' to see the monthly payment and full schedule.",
        ],
        "usecases": [
            "Estimating monthly mortgage payments before buying a home.",
            "Comparing different loan offers from multiple lenders.",
            "Planning refinancing strategies and payoff timelines.",
            "Understanding total interest paid over the life of a loan.",
        ],
        "faqs": [
            {"q": "Is the interest rate monthly or annual?", "a": "The calculator uses an annual interest rate. It divides this by 12 months to calculate the monthly payment."},
            {"q": "Does the schedule include property tax or insurance?", "a": "No, this calculator shows principal and interest only. For a full mortgage estimate, add estimated annual property tax and insurance to your annual costs."},
            {"q": "How accurate is the result?", "a": "This uses the standard amortization formula. Actual payments may vary slightly due to rounding, PMI, or lender-specific terms."},
        ]
    },
    "percentage-calculator.html": {
        "category": "Calculator",
        "what": "A percentage calculator solves common percentage problems: find X% of Y, what percent is X of Y, or what is the percentage change between two numbers. It handles all three core percentage calculations in one place.",
        "how": [
            "Select the calculation type: X% of Y, X is what % of Y, or % change.",
            "Enter the relevant numbers in the input fields.",
            "Click 'Calculate' for the instant result.",
        ],
        "usecases": [
            "Calculating discounts and sale prices while shopping.",
            "Computing tip amounts at restaurants.",
            "Analyzing business growth rates and percentage changes in data.",
            "Working out grade percentages in school or university.",
        ],
        "faqs": [
            {"q": "How do I calculate a discount?", "a": "Multiply the original price by the discount percentage, then divide by 100. Subtract the result from the original price for the final sale price."},
            {"q": "What's the formula for percentage increase?", "a": "Percentage increase = ((New Value - Original Value) / Original Value) × 100."},
            {"q": "Can I reverse-calculate the original number?", "a": "Yes. If you know the result and the percentage, divide the result by the percentage and multiply by 100."},
        ]
    },
    "scientific-calculator.html": {
        "category": "Calculator",
        "what": "A scientific calculator performs advanced mathematical operations including trigonometry (sin, cos, tan), logarithms, exponents, roots, factorials, and more. It supports both degrees and radians for trigonometric calculations.",
        "how": [
            "Use the numeric pad for basic input.",
            "Select DEG or RAD mode for trigonometric functions.",
            "Click function buttons (sin, cos, log, etc.) for advanced operations.",
            "Use parentheses for complex expressions.",
            "Press '=' to evaluate.",
        ],
        "usecases": [
            "Engineering and physics homework and coursework.",
            "Scientific research calculations and data analysis.",
            "Financial modeling with exponential functions.",
            "Programming and computer science calculations.",
        ],
        "faqs": [
            {"q": "What's the difference between DEG and RAD?", "a": "DEG (Degrees) uses 0-360° for angles. RAD (Radians) uses 0-2π. Use DEG for everyday use; RAD for advanced math and calculus."},
            {"q": "Can I use constants like π and e?", "a": "Yes. Click the π button for Pi (3.14159...) and the e button for Euler's number (2.71828...)."},
            {"q": "Does it support parentheses?", "a": "Yes, you can nest multiple levels of parentheses for complex expressions."},
        ]
    },
    "unit-converter.html": {
        "category": "Calculator",
        "what": "A unit converter translates measurements between different unit systems — length, weight, temperature, area, volume, and more. It provides instant, accurate conversions without manual formula calculation.",
        "how": [
            "Select the measurement category (length, weight, temperature, etc.).",
            "Choose the source unit and enter the value.",
            "Select the target unit.",
            "See the converted result instantly.",
        ],
        "usecases": [
            "Converting between metric and imperial units for international travel.",
            "Cooking measurements when a recipe uses different units.",
            "Construction and engineering unit conversions.",
            "Academic and scientific unit calculations.",
        ],
        "faqs": [
            {"q": "What unit categories are supported?", "a": "Common categories include length (m, ft, in, km, miles), weight (kg, lb, oz), temperature (°C, °F, K), area, volume, and more."},
            {"q": "Is the conversion precise?", "a": "Yes. The converter uses standard conversion factors and displays results to a high decimal precision."},
            {"q": "Can I convert between metric and imperial?", "a": "Absolutely. The converter supports both systems and provides accurate cross-system conversions."},
        ]
    },

    # ===== GENERATOR =====
    "hash-generator.html": {
        "category": "Generator",
        "what": "A hash generator computes a fixed-length string (hash) from any input text or file using cryptographic algorithms like MD5, SHA-1, SHA-256, SHA-384, and SHA-512. Hashes are one-way functions — you can't reverse a hash to get the original input.",
        "how": [
            "Type or paste text into the input field, or click 'Choose File' to hash a file.",
            "Click 'Compute Hashes' to generate all hash values.",
            "Copy any hash (hex or Base64) with one click.",
            "Hashes are computed entirely in your browser — no data is uploaded.",
        ],
        "usecases": [
            "Verifying file integrity after downloads or transfers.",
            "Storing password representations in databases.",
            "Generating checksums for digital forensics and IT audits.",
            "Creating unique identifiers for documents and records.",
        ],
        "faqs": [
            {"q": "Is MD5 still secure for passwords?", "a": "No. MD5 is considered cryptographically broken for security purposes. It's too fast and vulnerable to collision attacks. Use SHA-256 or stronger for security-sensitive applications."},
            {"q": "Can I reverse a hash?", "a": "No. Hashing is a one-way function. There's no way to recover the original input from a hash. This is by design for security."},
            {"q": "What is the difference between hex and Base64?", "a": "Hex uses 0-9 and a-f (base 16), producing longer strings. Base64 uses 64 ASCII characters, producing shorter but less human-readable output."},
        ]
    },
    "password-generator.html": {
        "category": "Generator",
        "what": "A password generator creates strong, random passwords with customizable options for length, character types (uppercase, lowercase, numbers, symbols), and exclusions. Truly random passwords are far more secure than human-chosen ones.",
        "how": [
            "Set the password length using the slider or input field.",
            "Toggle character types: uppercase, lowercase, numbers, symbols.",
            "Click 'Generate' to create a new password.",
            "Use the copy button to copy it to your clipboard.",
        ],
        "usecases": [
            "Creating secure passwords for new online accounts.",
            "Generating master passwords for password managers.",
            "Creating Wi-Fi passwords for router setup.",
            "Generating API keys and access tokens for developers.",
        ],
        "faqs": [
            {"q": "Are the generated passwords truly random?", "a": "Yes. The generator uses your browser's built-in cryptographic random number generator (crypto.getRandomValues), which provides high-quality randomness."},
            {"q": "How long should my password be?", "a": "Minimum 12 characters for general use. For critical accounts, 16-20+ characters with all character types is recommended."},
            {"q": "Do you store or transmit my passwords?", "a": "No. All password generation happens locally in your browser. Nothing is sent to any server."},
        ]
    },
    "pomodoro-timer.html": {
        "category": "Generator",
        "what": "The Pomodoro Technique is a time management method that breaks work into 25-minute focused sessions ('Pomodoros') followed by 5-minute breaks. A Pomodoro timer tracks these intervals and signals when to work and when to rest.",
        "how": [
            "Click 'Start' to begin a 25-minute work session.",
            "The timer counts down automatically.",
            "When the session ends, a notification sounds and the break timer starts.",
            "Click 'Skip' to move to the next phase, or 'Reset' to start over.",
        ],
        "usecases": [
            "Beating procrastination and maintaining focus on tasks.",
            "Managing ADHD and improving concentration.",
            "Breaking large projects into manageable time blocks.",
            "Preventing burnout by enforcing regular breaks.",
        ],
        "faqs": [
            {"q": "Can I customize the timer lengths?", "a": "Yes. Most Pomodoro timers allow you to adjust the work session (default 25 min), short break (5 min), and long break (15 min) durations."},
            {"q": "Does the timer work if I switch tabs?", "a": "Yes. The timer runs in the background using JavaScript intervals. However, for best results, keep the tab open."},
            {"q": "What is a long break?", "a": "After every 4 Pomodoro sessions, take a longer break of 15-30 minutes to rest and recharge."},
        ]
    },
    "qr-code-generator.html": {
        "category": "Generator",
        "what": "A QR code generator creates scannable QR codes from text, URLs, email addresses, phone numbers, Wi-Fi credentials, or any other data. QR codes can store hundreds to thousands of characters and are scannable by any smartphone camera.",
        "how": [
            "Select the content type (URL, text, Wi-Fi, vCard, etc.).",
            "Enter or paste your content.",
            "Choose a QR code color and size.",
            "Click 'Generate QR Code' to create the image.",
            "Download or copy the QR code.",
        ],
        "usecases": [
            "Linking physical marketing materials to websites or promotions.",
            "Sharing Wi-Fi credentials without typing passwords.",
            "Creating digital business cards and contact cards.",
            "Adding QR codes to restaurant menus and event tickets.",
        ],
        "faqs": [
            {"q": "How much data can a QR code hold?", "a": "It depends on the error correction level and version. A standard QR code can store up to 4,296 alphanumeric characters. The more data, the denser the code becomes."},
            {"q": "Will the QR code still work if part of it is damaged?", "a": "Yes. QR codes use Reed-Solomon error correction. Depending on the version and error level, up to 30% of the code can be damaged and still scan successfully."},
            {"q": "Can I customize the QR code colors?", "a": "Yes, but avoid very light colors for the foreground as they won't scan well. Use dark colors on light backgrounds for best reliability."},
        ]
    },
    "qr-code-scanner.html": {
        "category": "Generator",
        "what": "A QR code scanner uses your device's camera to read QR codes in real-time. Simply point your camera at a QR code to instantly decode its content — whether it's a URL, text, phone number, or Wi-Fi credentials.",
        "how": [
            "Click 'Start Camera' to activate your device camera.",
            "Point the camera at a QR code.",
            "The scanner detects and decodes the QR code automatically.",
            "The decoded content is displayed — click links to open them.",
        ],
        "usecases": [
            "Scanning QR codes on product packaging and labels.",
            "Opening restaurant menus, event details, or concert tickets.",
            "Connecting to Wi-Fi networks without entering passwords.",
            "Verifying authenticity of documents and certificates.",
        ],
        "faqs": [
            {"q": "Does the scanner save or store QR codes?", "a": "No. The scanner only reads and displays the QR code content. Nothing is stored, uploaded, or shared."},
            {"q": "Why can't my camera detect the QR code?", "a": "Ensure good lighting, hold the camera steady, and make sure the entire QR code is visible in the frame. Clean the camera lens and the QR code surface if needed."},
            {"q": "Is camera access required?", "a": "Yes. The browser will ask for camera permission. You can deny this permission and close the scanner at any time."},
        ]
    },
    "random-number-generator.html": {
        "category": "Generator",
        "what": "A random number generator (RNG) produces unpredictable numbers within a specified range. It uses cryptographic randomness to ensure each number is truly unpredictable, suitable for games, statistical sampling, and security applications.",
        "how": [
            "Enter the minimum and maximum range.",
            "Set the quantity of numbers to generate.",
            "Choose whether to allow or disallow duplicates.",
            "Click 'Generate' to get your random numbers.",
            "Copy the results or generate again.",
        ],
        "usecases": [
            "Selecting random winners for giveaways and contests.",
            "Generating random samples for statistics and research.",
            "Rolling dice and shuffling in online games.",
            "Creating random test data for software development.",
        ],
        "faqs": [
            {"q": "How random are the numbers?", "a": "The generator uses cryptographically secure random number generation (crypto.getRandomValues), suitable for security-sensitive applications."},
            {"q": "Can I generate multiple numbers at once?", "a": "Yes. Enter the quantity you need and all numbers will be generated at once."},
            {"q": "Can I prevent duplicate numbers?", "a": "Yes. Toggle the 'No duplicates' option to ensure all generated numbers are unique within the specified range."},
        ]
    },
    "uuid-generator.html": {
        "category": "Generator",
        "what": "A UUID (Universally Unique Identifier) generator creates 128-bit identifiers that are statistically guaranteed to be unique across all devices and time. UUIDs v4 are randomly generated and look like: 93b6f2e8-18f2-49c2-9eef-9dd1c6cafa83.",
        "how": [
            "Set the number of UUIDs to generate (1-100).",
            "Click 'Generate' to create UUIDs.",
            "Click any UUID to copy it to your clipboard.",
            "Click 'Regenerate' for a fresh set.",
        ],
        "usecases": [
            "Assigning unique IDs to database records and entities.",
            "Generating session tokens and API keys.",
            "Creating unique filenames for uploaded files.",
            "Generating transaction IDs and invoice references.",
        ],
        "faqs": [
            {"q": "What UUID version is generated?", "a": "UUID v4 (random). Version 4 UUIDs are generated using 122 random bits and are the most common type for general-purpose unique identifiers."},
            {"q": "Can UUIDs collide (be the same)?", "a": "Theoretically possible but statistically negligible. The probability of generating a duplicate UUID v4 is approximately 1 in 5.3×10³⁶."},
            {"q": "What format are the UUIDs in?", "a": "Standard 8-4-4-4-12 hexadecimal format (e.g., 550e8400-e29b-41d4-a716-446655440000)."},
        ]
    },
    "what-is-my-ip.html": {
        "category": "Generator",
        "what": "A 'What Is My IP' tool reveals your public IP address, location, ISP, browser user agent, and connection details. It runs entirely in your browser and fetches public IP from an external API.",
        "how": [
            "Open the page — your public IP is displayed automatically.",
            "View your location (country, city), ISP, and connection type.",
            "Check your browser's User Agent string.",
            "Refresh to see updated information.",
        ],
        "usecases": [
            "Checking if you're using a VPN or proxy correctly.",
            "Troubleshooting network connectivity issues.",
            "Verifying your apparent geographic location for geo-restricted services.",
            "Testing whether your ISP assigns static or dynamic IPs.",
        ],
        "faqs": [
            {"q": "What is the difference between public and private IP?", "a": "A public IP is assigned by your ISP and is visible on the internet. A private IP (e.g., 192.168.x.x) is assigned by your router and only works within your local network."},
            {"q": "Does this tool log my IP address?", "a": "No personal data is stored. The tool only reads your IP for display purposes."},
            {"q": "Why is the shown location inaccurate?", "a": "IP geolocation is approximate and can be off by tens to hundreds of kilometers. It identifies your ISP's region, not your exact address."},
        ]
    },

    # ===== IMAGE =====
    "background-remover.html": {
        "category": "Image",
        "what": "A background remover uses browser-based AI to detect and remove the background from images, leaving only the subject with a transparent background. All processing happens locally in your browser — your images never leave your device.",
        "how": [
            "Drag and drop an image or click 'Select Image'.",
            "The AI processes the image and removes the background automatically.",
            "Preview the result with the background removed.",
            "Download the image with a transparent background (PNG).",
        ],
        "usecases": [
            "Creating product photos for e-commerce listings.",
            "Removing backgrounds from profile pictures and portraits.",
            "Preparing clean images for graphic design projects.",
            "Removing cluttered backgrounds from logos and icons.",
        ],
        "faqs": [
            {"q": "Is my image uploaded to a server?", "a": "No. All processing uses TensorFlow.js running entirely in your browser. Your images never leave your device."},
            {"q": "What image formats are supported?", "a": "JPEG, PNG, WebP, and most common image formats are supported. Output is always PNG to preserve transparency."},
            {"q": "What's the maximum image size?", "a": "The tool works best with images up to 2048×2048 pixels. Very large images may take longer to process."},
        ]
    },
    "color-converter.html": {
        "category": "Image",
        "what": "A color converter translates colors between HEX, RGB, HSL, HSV, CMYK, and other formats. Designers and developers use it to match colors across different design tools and codebases.",
        "how": [
            "Enter a color in any format (HEX, RGB, HSL, etc.).",
            "All other formats update instantly.",
            "Use the color picker to select a color visually.",
            "Click any format to copy it to your clipboard.",
        ],
        "usecases": [
            "Converting design mockup colors to CSS code.",
            "Matching brand colors across different media.",
            "Preparing print-ready CMYK values from digital designs.",
            "Generating accessible color contrast combinations.",
        ],
        "faqs": [
            {"q": "What's the difference between HSL and HSV?", "a": "HSL (Hue, Saturation, Lightness) describes colors as humans perceive them. HSV (Hue, Saturation, Value) describes colors as light mixes. Both are useful for different design workflows."},
            {"q": "Can I convert CMYK for print?", "a": "Yes. CMYK values are provided for print preparation. Note that screen RGB and print CMYK color spaces differ, so exact matching requires color profiling."},
            {"q": "How do I use these colors in CSS?", "a": "Copy the HEX value (#RRGGBB) or RGB/RGBA value for use in CSS background-color, color, or border-color properties."},
        ]
    },
    "color-picker.html": {
        "category": "Image",
        "what": "A color picker lets you select any color visually from a spectrum or by entering values. It provides HEX, RGB, HSL, and other formats instantly, making it a designer's essential everyday tool.",
        "how": [
            "Click or drag anywhere on the color spectrum to pick a hue.",
            "Adjust saturation and lightness/brightness using the sliders.",
            "Copy any color format with one click.",
            "Use the eyedropper tool to pick a color from anywhere on screen (if supported).",
        ],
        "usecases": [
            "Selecting colors for web design and CSS development.",
            "Matching existing brand or design colors.",
            "Creating color palettes for UI/UX projects.",
            "Testing color accessibility and contrast ratios.",
        ],
        "faqs": [
            {"q": "Does the eyedropper work on any website?", "a": "The built-in eyedropper uses the browser's native API and may not be supported in all browsers. Try Chrome for the best compatibility."},
            {"q": "How do I get complementary or analogous colors?", "a": "Use the HSL sliders. Complementary colors are 180° apart in hue. Analogous colors are within 30° of each other."},
        ]
    },
    "image-compressor.html": {
        "category": "Image",
        "what": "An image compressor reduces the file size of JPG, PNG, and WebP images without significantly visible quality loss. Smaller images load faster on websites and save storage and bandwidth.",
        "how": [
            "Drag and drop images or click 'Select Images'.",
            "Adjust the quality slider to control compression level.",
            "Preview the original vs compressed size.",
            "Download individual images or all at once.",
        ],
        "usecases": [
            "Optimizing website images for faster page load times.",
            "Reducing file sizes for email attachments.",
            "Preparing images for social media upload limits.",
            "Saving storage space on devices and cloud storage.",
        ],
        "faqs": [
            {"q": "Is the compression lossless?", "a": "JPEG compression is lossy by nature. PNG compression is lossless. You can balance quality and file size using the quality slider. The preview shows the actual reduction."},
            {"q": "What formats are supported?", "a": "JPEG/JPG, PNG, and WebP input and output are fully supported."},
            {"q": "How much can I reduce file size?", "a": "Typical reductions range from 30% to 80%, depending on the original image's compression state and the quality setting you choose."},
        ]
    },
    "image-converter.html": {
        "category": "Image",
        "what": "An image converter transforms images between JPG, PNG, WebP, and GIF formats. Different formats serve different purposes — JPEG for photos, PNG for graphics, WebP for web optimization, GIF for animations.",
        "how": [
            "Upload one or more images by dragging or clicking.",
            "Select the target output format (JPG, PNG, WebP, GIF).",
            "Adjust quality and settings for the target format.",
            "Download converted images individually or as a ZIP.",
        ],
        "usecases": [
            "Converting camera RAW/JPEG to WebP for faster websites.",
            "Creating PNG versions of graphics for transparency support.",
            "Converting images to JPEG for smaller file sizes.",
            "Creating GIF animations from image sequences.",
        ],
        "faqs": [
            {"q": "What's the best format for web?", "a": "WebP offers the best compression and quality. JPEG is universally supported. PNG is best for graphics with transparency. Use JPG for photos and PNG/WebP for UI elements."},
            {"q": "Does conversion reduce quality?", "a": "Repeatedly converting between formats can degrade quality. Convert directly from the original format when possible."},
        ]
    },
    "image-resizer.html": {
        "category": "Image",
        "what": "An image resizer changes the pixel dimensions of images — scaling them up or down while maintaining aspect ratio. Resizing is essential for preparing images for specific display sizes.",
        "how": [
            "Upload an image by dragging or clicking.",
            "Enter the target width or height (aspect ratio is maintained).",
            "Preview the new dimensions.",
            "Download the resized image.",
        ],
        "usecases": [
            "Preparing images for specific social media dimensions.",
            "Creating thumbnails for website galleries.",
            "Scaling down large photos for email attachments.",
            "Resizing for presentations and documents.",
        ],
        "faqs": [
            {"q": "Does resizing affect quality?", "a": "Upscaling (making an image larger) can result in blurriness. Downscaling is generally safe and maintains quality well."},
            {"q": "How do I change both width and height independently?", "a": "Uncheck 'Maintain aspect ratio' to set both dimensions freely. This may stretch or distort the image."},
        ]
    },

    # ===== PDF =====
    "compress-pdf.html": {
        "category": "PDF",
        "what": "A PDF compressor reduces the file size of PDF documents using advanced compression algorithms. Smaller PDFs are easier to email, upload, and archive while maintaining readable quality.",
        "how": [
            "Drag and drop your PDF or click 'Select PDF'.",
            "Choose a compression level (extreme, recommended, or low).",
            "Preview the original and compressed file sizes.",
            "Download the compressed PDF.",
        ],
        "usecases": [
            "Reducing PDF sizes for email attachments.",
            "Optimizing scanned document PDFs for storage.",
            "Preparing PDFs for online upload limits.",
            "Compressing presentations and reports for faster sharing.",
        ],
        "faqs": [
            {"q": "Is my PDF data kept private?", "a": "Yes. All compression happens in your browser. Your PDF is never uploaded to any server."},
            {"q": "How much can I reduce a PDF?", "a": "Text-based PDFs can often be reduced by 50-80%. Image-heavy PDFs may see 30-60% reduction depending on the compression level chosen."},
            {"q": "Will the compressed PDF look different?", "a": "With 'Recommended' compression, the visual quality is nearly identical. 'Extreme' compression may reduce image quality slightly to achieve maximum size reduction."},
        ]
    },
    "jpg-to-pdf.html": {
        "category": "PDF",
        "what": "A JPG to PDF converter turns one or more image files into a single PDF document. It's perfect for combining scanned pages, photos, or design files into a single shareable document.",
        "how": [
            "Upload one or more JPG/PNG images.",
            "Arrange the order by dragging images.",
            "Set page orientation and margins.",
            "Click 'Create PDF' to generate and download.",
        ],
        "usecases": [
            "Combining scanned documents into one PDF file.",
            "Creating a PDF portfolio from design images.",
            "Converting photo albums to PDF for sharing.",
            "Preparing documents for digital signatures.",
        ],
        "faqs": [
            {"q": "Can I convert multiple images to one PDF?", "a": "Yes. Upload all your images and they will be combined into a single multi-page PDF."},
            {"q": "What image formats are supported?", "a": "JPG/JPEG, PNG, WebP, GIF, BMP, and TIFF formats are all supported."},
            {"q": "Is the conversion lossless?", "a": "The PDF generation itself is lossless. JPEG images embedded in PDFs retain their compression."},
        ]
    },
    "merge-pdf.html": {
        "category": "PDF",
        "what": "A PDF merger combines multiple PDF files into a single document in any order you choose. It keeps all original formatting, bookmarks, and links intact.",
        "how": [
            "Upload two or more PDF files.",
            "Drag and drop to arrange the order.",
            "Click 'Merge PDFs' to combine them.",
            "Download the merged PDF.",
        ],
        "usecases": [
            "Combining chapters of a report or eBook.",
            "Merging multi-part contracts or applications.",
            "Assembling portfolio pieces into one presentation.",
            "Combining scanned pages into complete documents.",
        ],
        "faqs": [
            {"q": "Is there a limit on file size or number of pages?", "a": "The tool handles files up to 50MB and 100+ pages. Very large files may take longer to process."},
            {"q": "Does it preserve bookmarks and links?", "a": "Basic links are preserved. Complex bookmarks and annotations may not always carry over perfectly in browser-based processing."},
        ]
    },
    "split-pdf.html": {
        "category": "PDF",
        "what": "A PDF splitter extracts specific pages or page ranges from a PDF document. You can split a PDF into individual pages, extract a range, or remove unwanted pages.",
        "how": [
            "Upload a PDF document.",
            "Select pages to extract by range (e.g., 1-5, 10, 15-20).",
            "Preview the selected pages.",
            "Download the extracted pages as a new PDF.",
        ],
        "usecases": [
            "Extracting a chapter or section from a large PDF.",
            "Splitting a scanned document into individual pages.",
            "Removing unwanted pages from documents.",
            "Extracting specific forms or pages from a multi-page form PDF.",
        ],
        "faqs": [
            {"q": "Can I extract non-contiguous pages?", "a": "Yes. Enter page numbers separated by commas, or use ranges like '1-3, 5, 7-10'."},
            {"q": "Is the original PDF modified?", "a": "No. The original file remains unchanged. A new PDF with only the selected pages is created."},
        ]
    },

    # ===== TEXT =====
    "word-counter.html": {
        "category": "Text",
        "what": "A word counter counts words, characters (with and without spaces), sentences, and paragraphs in real-time as you type or paste text. It's a fundamental tool for writers, students, and anyone who needs to meet character or word limits.",
        "how": [
            "Type or paste your text into the text area.",
            "Statistics update in real-time — no need to click anything.",
            "View word count, character count, and trimmed length.",
            "Click 'Clear' to reset and start over.",
        ],
        "usecases": [
            "Meeting essay, article, or blog post word count requirements.",
            "Checking character limits for social media posts and meta descriptions.",
            "Estimating reading time for articles and documents.",
            "Tracking writing progress during content creation.",
        ],
        "faqs": [
            {"q": "Does it count words in multiple languages?", "a": "Yes. The word counter uses space and punctuation boundaries, so it works with any language that uses spaces between words."},
            {"q": "What's the difference between character count and trimmed length?", "a": "Character count includes all characters. Trimmed length excludes leading and trailing whitespace."},
        ]
    },
    "base64.html": {
        "category": "Text",
        "what": "Base64 encoding converts binary data into ASCII text format using 64 characters (A-Z, a-z, 0-9, +, /). It's commonly used to encode images for embedding in HTML/CSS, transmit binary data over text protocols, or obfuscate simple text.",
        "how": [
            "Paste or type text into the input field.",
            "Click 'Encode' to convert to Base64 or 'Decode' to reverse.",
            "View and copy the result.",
            "Use the mode toggle to switch between encode and decode.",
        ],
        "usecases": [
            "Embedding small images directly in HTML or CSS files.",
            "Encoding API credentials for safe transmission.",
            "Encoding email attachments in MIME format.",
            "Creating data URLs for faster page loading.",
        ],
        "faqs": [
            {"q": "Is Base64 encoding encryption?", "a": "No. Base64 is not encryption — it's encoding. Anyone can decode a Base64 string easily. Don't use it to hide sensitive data."},
            {"q": "Does encoding increase file size?", "a": "Yes. Base64 encoding increases size by approximately 33%. A 100KB file becomes ~133KB when Base64 encoded."},
        ]
    },
    "case-converter.html": {
        "category": "Text",
        "what": "A case converter transforms text between different letter casing conventions: UPPERCASE, lowercase, Title Case, Sentence case, camelCase, PascalCase, snake_case, kebab-case, and more. It's essential for developers and writers working with code and documents.",
        "how": [
            "Paste or type your text into the input area.",
            "Click any case style button to convert instantly.",
            "Copy the result with one click.",
            "The original text is preserved for trying different styles.",
        ],
        "usecases": [
            "Converting variable names for programming (camelCase, snake_case).",
            "Formatting titles and headings for documents.",
            "Converting messy copied text to proper formatting.",
            "Preparing text for URLs, filenames, or identifiers.",
        ],
        "faqs": [
            {"q": "What case types are supported?", "a": "Uppercase, lowercase, Title Case, Sentence case, camelCase, PascalCase, snake_case, kebab-case, constant case, dot.case, and path/case."},
            {"q": "Does it preserve special characters?", "a": "Yes. Numbers, symbols, and punctuation are preserved exactly as entered."},
        ]
    },
    "csv-to-json.html": {
        "category": "Text",
        "what": "A CSV to JSON converter transforms spreadsheet data (CSV format) into JSON objects. JSON is the standard data format for APIs and web applications, making this converter essential for developers and data analysts.",
        "how": [
            "Paste or upload a CSV file with headers.",
            "Review the parsed column headers.",
            "Click 'Convert to JSON' to generate the output.",
            "Copy the JSON or download it as a .json file.",
        ],
        "usecases": [
            "Converting Excel or Google Sheets data for API integration.",
            "Preparing datasets for web applications and JavaScript projects.",
            "Migrating data from legacy CSV systems to modern JSON APIs.",
            "Creating configuration files from spreadsheet data.",
        ],
        "faqs": [
            {"q": "Does the CSV need headers?", "a": "Yes. The first row of the CSV must contain column headers, which become the JSON object keys."},
            {"q": "Can I convert nested or complex CSV?", "a": "Simple flat CSV files work best. For nested data, consider preprocessing your CSV or using a more advanced data transformation tool."},
        ]
    },
    "html-encoder.html": {
        "category": "Text",
        "what": "An HTML encoder converts special characters into their HTML entity equivalents. For example, < becomes &lt; and > becomes &gt;. This prevents XSS attacks and ensures content displays correctly in HTML documents.",
        "how": [
            "Paste or type HTML or special characters into the input.",
            "Click 'Encode' to convert to HTML entities.",
            "Click 'Decode' to reverse the process.",
            "Copy the encoded or decoded output.",
        ],
        "usecases": [
            "Safely displaying user input on websites (preventing XSS).",
            "Embedding code snippets in HTML documents.",
            "Converting special characters for use in XML and HTML.",
            "Preparing text content for CMS and blog platforms.",
        ],
        "faqs": [
            {"q": "What's the difference between HTML encoding and escaping?", "a": "They refer to the same process. Special characters are converted to HTML entities so browsers render them as text rather than interpreting them as HTML."},
            {"q": "Is HTML encoding the same as encryption?", "a": "No. HTML encoding is not encryption — the encoded text can be decoded easily. Use HTTPS and proper authentication for security."},
        ]
    },
    "html-formatter.html": {
        "category": "Text",
        "what": "An HTML formatter (beautifier) cleans up and indents messy HTML code. It adds consistent indentation, removes unnecessary whitespace, and formats nested tags for maximum readability. Essential for debugging and reviewing HTML.",
        "how": [
            "Paste messy or minified HTML into the input.",
            "Click 'Format' to beautify the code.",
            "Review the formatted output with proper indentation.",
            "Copy the clean HTML or download it.",
        ],
        "usecases": [
            "Debugging and reading minified HTML from CMS platforms.",
            "Formatting raw HTML templates for easier editing.",
            "Prettifying HTML copied from web inspection tools.",
            "Standardizing HTML code across a project.",
        ],
        "faqs": [
            {"q": "Does formatting change my HTML?", "a": "It only changes whitespace and indentation. All tags, attributes, and content remain exactly the same."},
            {"q": "Can I format inline CSS and JavaScript too?", "a": "The HTML formatter focuses on HTML structure. For CSS/JS formatting, use a dedicated code formatter for best results."},
        ]
    },
    "json-formatter.html": {
        "category": "Text",
        "what": "A JSON formatter validates, beautifies, and prettifies JSON data. It checks for syntax errors, formats the structure with proper indentation, and can minify JSON for production use. A developer's everyday essential tool.",
        "how": [
            "Paste JSON data into the editor.",
            "The JSON validates automatically and highlights errors.",
            "Click 'Beautify' for formatted output or 'Minify' for compact output.",
            "Copy the result or use the tree view for navigation.",
        ],
        "usecases": [
            "Debugging JSON responses from APIs.",
            "Formatting configuration files and data exports.",
            "Validating JSON syntax before deployment.",
            "Comparing JSON structures between different sources.",
        ],
        "faqs": [
            {"q": "Does it validate JSON?", "a": "Yes. Invalid JSON is highlighted with the specific error location and message."},
            {"q": "What is JSON used for?", "a": "JSON (JavaScript Object Notation) is the standard data format for web APIs, configuration files, and data exchange between systems."},
        ]
    },
    "lorem-ipsum.html": {
        "category": "Text",
        "what": "Lorem Ipsum generates placeholder text for design mockups, wireframes, and layouts. It uses a Latin-based dummy text that looks like real content without distracting from the design itself.",
        "how": [
            "Choose the number of paragraphs, sentences, or words.",
            "Click 'Generate' to create the placeholder text.",
            "Copy the text with one click.",
            "Regenerate for new content.",
        ],
        "usecases": [
            "Filling in text placeholders during web and app design.",
            "Creating wireframes and prototypes for client presentations.",
            "Testing typography, layout, and font rendering.",
            "Producing realistic-looking mockups for pitching and proposals.",
        ],
        "faqs": [
            {"q": "Is Lorem Ipsum actual Latin?", "a": "It's derived from a 1st-century BC Roman philosopher's text but scrambled and modified. It looks like Latin but isn't grammatically meaningful."},
            {"q": "Can I generate specific amounts?", "a": "Yes. Choose between paragraphs, sentences, or words, and specify exactly how many you need."},
        ]
    },
    "number-base-converter.html": {
        "category": "Text",
        "what": "A number base converter translates numbers between binary (base 2), octal (base 8), decimal (base 10), hexadecimal (base 16), and other number systems. Essential for programmers, engineers, and computer science students.",
        "how": [
            "Enter a number in any base (BIN, OCT, DEC, HEX).",
            "All other bases update instantly.",
            "Click any value to copy it to your clipboard.",
        ],
        "usecases": [
            "Converting between decimal and hexadecimal for color codes.",
            "Understanding binary and hexadecimal in computer systems.",
            "Debugging memory addresses and network subnet calculations.",
            "Computer science education and programming tasks.",
        ],
        "faqs": [
            {"q": "What bases are supported?", "a": "Binary (2), Octal (8), Decimal (10), Hexadecimal (16), and Base32 are commonly supported."},
            {"q": "Why use hexadecimal instead of decimal?", "a": "Hex maps perfectly to binary (each hex digit = 4 binary digits), making it compact and easy to read for computer professionals."},
        ]
    },
    "remove-duplicates.html": {
        "category": "Text",
        "what": "A remove duplicates tool eliminates duplicate lines, words, or numbers from text. It instantly cleans lists, removes repeated entries, and sorts results — saving hours of manual editing.",
        "how": [
            "Paste or type text with duplicates.",
            "Choose whether to remove duplicate lines, words, or numbers.",
            "Click 'Remove Duplicates' to process.",
            "Copy the clean, unique results.",
        ],
        "usecases": [
            "Cleaning email lists and contact databases.",
            "Removing duplicate entries from CSV exports and spreadsheets.",
            "Deduplicating keyword lists for SEO campaigns.",
            "Cleaning scraped data for analysis and reporting.",
        ],
        "faqs": [
            {"q": "Does it preserve the original order?", "a": "Yes. The first occurrence of each item is kept in its original position. Duplicate subsequent occurrences are removed."},
            {"q": "Is the comparison case-sensitive?", "a": "Yes, by default. You can choose to ignore case when comparing items."},
        ]
    },
    "sql-formatter.html": {
        "category": "Text",
        "what": "A SQL formatter beautifies and indents SQL queries for readability. It handles complex multi-table JOINs, subqueries, and nested conditions, making it essential for database developers and analysts.",
        "how": [
            "Paste a SQL query into the editor.",
            "Click 'Format SQL' to beautify.",
            "Review the properly indented and structured query.",
            "Copy or download the formatted SQL.",
        ],
        "usecases": [
            "Debugging complex SQL queries from legacy systems.",
            "Formatting SQL for code reviews and documentation.",
            "Understanding poorly formatted SQL from database tools.",
            "Preparing SQL for presentations and teaching.",
        ],
        "faqs": [
            {"q": "What SQL dialects are supported?", "a": "The formatter handles standard ANSI SQL syntax, including SELECT, INSERT, UPDATE, DELETE, JOIN, GROUP BY, HAVING, subqueries, and CTEs."},
            {"q": "Does it validate SQL syntax?", "a": "The formatter focuses on beautification. For full syntax validation, use a database-specific linter or run the query in your database engine."},
        ]
    },
    "url-encoder.html": {
        "category": "Text",
        "what": "A URL encoder converts special characters into their percent-encoded equivalents for safe inclusion in URLs. For example, spaces become %20 and & becomes %26. All URLs must be properly encoded to work correctly.",
        "how": [
            "Paste or type a URL or text into the input.",
            "Click 'Encode' to convert special characters to percent encoding.",
            "Click 'Decode' to reverse the process.",
            "Copy the encoded or decoded result.",
        ],
        "usecases": [
            "Encoding URL query parameters with special characters.",
            "Preparing search queries for URLs and API endpoints.",
            "Decoding URLs from browser address bars or server logs.",
            "Ensuring special characters display correctly in shared links.",
        ],
        "faqs": [
            {"q": "Why do URLs need encoding?", "a": "URLs can only contain a limited set of characters (A-Z, a-z, 0-9, -, _, ., ~). All other characters must be percent-encoded to avoid ambiguity and errors."},
            {"q": "What's the difference between encodeURI and encodeURIComponent?", "a": "encodeURI encodes fewer characters (keeps :///?), while encodeURIComponent encodes everything non-alphanumeric. Use encodeURIComponent for query parameter values."},
        ]
    },
}


def build_content_html(tool_name, info):
    """为单个工具构建内容 HTML"""
    category = info["category"]
    what = info["what"]
    how = info["how"]
    usecases = info["usecases"]
    faqs = info["faqs"]
    
    # How steps as numbered list
    how_items = "\n".join([f'<li>Step {i+1}: {step}</li>' for i, step in enumerate(how)])
    
    # Use cases as bullet list
    usecase_items = "\n".join([f'<li>{uc}</li>' for uc in usecases])
    
    # FAQ as details/summary
    faq_items = "\n".join([
        f'''<details class="faq-item">
  <summary>{faq["q"]}</summary>
  <p>{faq["a"]}</p>
</details>''' for faq in faqs
    ])
    
    # Build FAQPage schema
    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": faq["q"],
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": faq["a"]
                }
            } for faq in faqs
        ]
    }
    
    faq_schema_json = json.dumps(faq_schema, ensure_ascii=False)
    
    return f'''
<section class="tool-info" aria-label="Tool information">
  <h2>What is {tool_name}?</h2>
  <p>{what}</p>

  <h2>How to use</h2>
  <ol class="steps-list">
{how_items}
  </ol>

  <h2>Use cases</h2>
  <ul class="usecase-list">
{usecase_items}
  </ul>

  <h2>Frequently Asked Questions</h2>
  <div class="faq-section">
{faq_items}
  </div>
</section>

<script type="application/ld+json">
{faq_schema_json}
</script>
'''


def process_tool_pages():
    """处理所有工具页面"""
    count = 0
    
    for filename, info in TOOL_CONTENT.items():
        # 找到这个文件
        filepath = None
        for subdir in ["calculator", "generator", "image", "pdf", "text"]:
            candidate = ROOT / "tools" / subdir / filename
            if candidate.exists():
                filepath = candidate
                break
        
        if not filepath:
            print(f"  ⚠️  未找到: {filename}")
            continue
        
        html = filepath.read_text(encoding="utf-8")
        
        # 获取工具名
        tool_name = filename.replace(".html", "").replace("-", " ").title()
        for key, val in TOOL_CONTENT.items():
            if key == filename:
                # 从 H1 获取实际名称
                m = re.search(r'<h1[^>]*>([^<]+)</h1>', html)
                if m:
                    tool_name = m.group(1).strip()
                break
        
        # 检查是否已添加内容（避免重复）
        if 'class="tool-info"' in html:
            print(f"  ⏭  跳过(已有内容): {filename}")
            continue
        
        # 构建内容
        content_html = build_content_html(tool_name, info)
        
        # 插入到 "Related tools" 区块之前，或 body 末尾之前
        marker = 'class="related-tools"'
        marker_alt = 'class="related-tools"'
        
        if marker in html:
            parts = html.split(marker, 1)
            html = parts[0] + content_html + '\n<div class="related-tools"' + parts[1]
        elif 'Related tools' in html or 'related-tools' in html.lower():
            # 尝试找到 related tools section
            pattern = r'(<div[^>]*class="[^"]*related[^"]*"[^>]*>)'
            match = re.search(pattern, html, re.IGNORECASE)
            if match:
                pos = match.start()
                html = html[:pos] + content_html + '\n' + html[pos:]
        else:
            # 插入到 footer 之前
            if '<footer' in html:
                parts = html.split('<footer', 1)
                html = parts[0] + content_html + '\n<footer' + parts[1]
            else:
                # 插入到 body 末尾附近
                body_end = html.rfind('</body>')
                if body_end != -1:
                    html = html[:body_end] + content_html + '\n' + html[body_end:]
        
        filepath.write_text(html, encoding="utf-8")
        count += 1
        print(f"  ✅ {filename}")
    
    return count


def main():
    print("=" * 60)
    print("添加工具页 SEO 内容区块...")
    print("=" * 60)
    count = process_tool_pages()
    print(f"\n共更新 {count} 个工具页面")


if __name__ == "__main__":
    main()
