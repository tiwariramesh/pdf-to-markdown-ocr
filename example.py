#!/usr/bin/env python3
"""
Example usage of the PDF to Markdown OCR Converter
"""

import subprocess
import sys
from pathlib import Path

def run_example():
    """Run example conversion on sample PDF"""
    
    # Check if sample PDF exists
    sample_pdf = Path("sample.pdf")
    if not sample_pdf.exists():
        print("❌ sample.pdf not found. Please add a sample PDF file to test.")
        return
    
    print("🚀 Running PDF to Markdown OCR Converter Example...")
    print(f"📄 Converting: {sample_pdf}")
    
    try:
        # Run the converter on first 2 pages
        cmd = [
            sys.executable, 
            "improved_ocr_converter.py", 
            str(sample_pdf),
            "--pages", "0", "1",
            "--verbose"
        ]
        
        print(f"🔧 Command: {' '.join(cmd)}")
        print("-" * 50)
        
        result = subprocess.run(cmd, check=True)
        
        print("-" * 50)
        print("✅ Conversion completed successfully!")
        print("📁 Check the 'improved_output' directory for results")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Conversion failed with error code: {e.returncode}")
        print("💡 Make sure you have installed all requirements:")
        print("   pip install -r requirements.txt")
        print("💡 And Tesseract OCR is installed on your system")
        
    except FileNotFoundError:
        print("❌ Python or the converter script not found")
        print("💡 Make sure you're in the correct directory")

if __name__ == "__main__":
    run_example()
