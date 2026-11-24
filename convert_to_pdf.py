#!/usr/bin/env python3
"""
Convert HTML files to PDF using weasyprint or wkhtmltopdf
"""

import subprocess
import sys
import os

def convert_with_wkhtmltopdf(html_path, pdf_path):
    """Try wkhtmltopdf"""
    try:
        result = subprocess.run([
            'wkhtmltopdf',
            '--enable-local-file-access',
            '--page-size', 'A4',
            '--margin-top', '20mm',
            '--margin-bottom', '20mm',
            '--margin-left', '15mm',
            '--margin-right', '15mm',
            '--encoding', 'utf-8',
            html_path,
            pdf_path
        ], capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            print(f"✅ Converted with wkhtmltopdf: {pdf_path}")
            return True
        else:
            print(f"❌ wkhtmltopdf failed: {result.stderr}")
            return False
    except FileNotFoundError:
        print("⚠️ wkhtmltopdf not installed")
        return False
    except Exception as e:
        print(f"❌ wkhtmltopdf error: {e}")
        return False

def convert_with_weasyprint(html_path, pdf_path):
    """Try weasyprint"""
    try:
        import weasyprint
        html = weasyprint.HTML(filename=html_path)
        html.write_pdf(pdf_path)
        print(f"✅ Converted with weasyprint: {pdf_path}")
        return True
    except ImportError:
        print("⚠️ weasyprint not installed")
        return False
    except Exception as e:
        print(f"❌ weasyprint error: {e}")
        return False

def convert_with_playwright(html_path, pdf_path):
    """Try playwright"""
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(f'file://{os.path.abspath(html_path)}')
            page.pdf(path=pdf_path, format='A4', margin={'top': '20mm', 'bottom': '20mm', 'left': '15mm', 'right': '15mm'})
            browser.close()
        print(f"✅ Converted with playwright: {pdf_path}")
        return True
    except ImportError:
        print("⚠️ playwright not installed")
        return False
    except Exception as e:
        print(f"❌ playwright error: {e}")
        return False

def main():
    html_files = [
        ('sanatan-master-system.html', 'sanatan-master-system.pdf'),
        ('sanatan-skills-cloud.html', 'sanatan-skills-cloud.pdf')
    ]

    for html_file, pdf_file in html_files:
        html_path = os.path.join(os.path.dirname(__file__), html_file)
        pdf_path = os.path.join(os.path.dirname(__file__), pdf_file)

        if not os.path.exists(html_path):
            print(f"❌ HTML file not found: {html_path}")
            continue

        print(f"\n📄 Converting {html_file} → {pdf_file}")

        # Try methods in order of preference
        success = (convert_with_wkhtmltopdf(html_path, pdf_path) or
                   convert_with_weasyprint(html_path, pdf_path) or
                   convert_with_playwright(html_path, pdf_path))

        if not success:
            print(f"❌ All conversion methods failed for {html_file}")
            print("💡 Install one of: wkhtmltopdf, weasyprint (pip install weasyprint), or playwright (pip install playwright && playwright install)")

if __name__ == '__main__':
    main()