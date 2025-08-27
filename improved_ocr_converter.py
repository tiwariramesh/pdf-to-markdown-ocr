#!/usr/bin/env python3
"""
Improved OCR-Enabled PDF to Markdown Converter
Converts scanned PDF files to clean, well-formatted Markdown with intelligent text processing
"""

import os
import sys
import argparse
import pathlib
import re
from pathlib import Path
from typing import Optional, List, Dict, Any
import logging
import subprocess

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    import pymupdf4llm
    import fitz  # PyMuPDF
    import pytesseract
    from PIL import Image, ImageEnhance, ImageFilter
except ImportError as e:
    logger.error(f"Required packages not found: {e}")
    logger.info("Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pymupdf4llm", "PyMuPDF", "pytesseract", "pillow"])
    import pymupdf4llm
    import fitz
    import pytesseract
    from PIL import Image, ImageEnhance, ImageFilter

class ImprovedOCRConverter:
    """Improved OCR-enabled PDF to Markdown converter with intelligent text processing"""
    
    def __init__(self, output_dir: str = "improved_output", image_dir: str = "improved_images"):
        """
        Initialize the improved OCR converter
        
        Args:
            output_dir: Directory for output markdown files
            image_dir: Directory for extracted images
        """
        self.output_dir = Path(output_dir)
        self.image_dir = Path(image_dir)
        self.setup_directories()
        
        # Configure Tesseract path for macOS
        if sys.platform == "darwin":
            tesseract_path = "/opt/homebrew/bin/tesseract"
            if os.path.exists(tesseract_path):
                pytesseract.pytesseract.tesseract_cmd = tesseract_path
        
        # Common headers/footers to remove
        self.headers_footers = [
            r'learner guide version \d+\.\d+',
            r'produced \d+ \w+ \d{4}',
            r'© compliant learning resources',
            r'page \d+',
            r'compliant learning resources',
            r'bsbfin\d+',
            r'manage organisational finances',
            r'release \d+',
            r'unit of competency',
            r'competency standards',
            r'© \d{4}',
            r'version \d+\.\d+',
            r'page \d+ of \d+',
            r'confidential',
            r'sample',
            r'watermark',
            r'preview'
        ]
        
    def setup_directories(self):
        """Create necessary directories if they don't exist"""
        self.output_dir.mkdir(exist_ok=True)
        self.image_dir.mkdir(exist_ok=True)
        logger.info(f"Output directory: {self.output_dir.absolute()}")
        logger.info(f"Image directory: {self.image_dir.absolute()}")
    
    def preprocess_image_for_ocr(self, image_path: str) -> Image.Image:
        """
        Preprocess image to improve OCR accuracy and remove watermarks
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Preprocessed PIL Image
        """
        # Open image
        image = Image.open(image_path)
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Enhance contrast to reduce watermark interference
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.5)
        
        # Enhance sharpness
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(1.3)
        
        # Apply slight blur to reduce noise while preserving text
        image = image.filter(ImageFilter.MedianFilter(size=1))
        
        return image
    
    def extract_page_with_improved_ocr(self, pdf_path: str, page_num: int, dpi: int = 300) -> Dict[str, Any]:
        """
        Extract a single page with improved OCR text extraction
        
        Args:
            pdf_path: Path to the input PDF file
            page_num: Page number to extract (0-based)
            dpi: Resolution for extracted images
            
        Returns:
            Dictionary containing page data
        """
        pdf_path = Path(pdf_path)
        doc = fitz.open(str(pdf_path))
        
        if page_num >= len(doc):
            raise ValueError(f"Page {page_num} does not exist. PDF has {len(doc)} pages.")
        
        page = doc[page_num]
        
        # Create high-quality image
        mat = fitz.Matrix(dpi/72, dpi/72)  # Convert DPI to scale factor
        pix = page.get_pixmap(matrix=mat)
        
        # Save image
        image_filename = f"{pdf_path.stem}-page-{page_num:03d}.png"
        image_path = self.image_dir / image_filename
        pix.save(str(image_path))
        
        # Extract text using improved OCR
        logger.info(f"Running improved OCR on page {page_num + 1}...")
        try:
            # Preprocess image
            preprocessed_image = self.preprocess_image_for_ocr(str(image_path))
            
            # Run OCR with optimized parameters
            ocr_text = pytesseract.image_to_string(
                preprocessed_image, 
                lang='eng',
                config='--psm 6 --oem 3'
            )
            
            # Clean and process the OCR text
            cleaned_text = self.clean_and_format_ocr_text(ocr_text)
            
            logger.info(f"Page {page_num + 1}: OCR extracted {len(cleaned_text)} characters")
            logger.info(f"Page {page_num + 1}: OCR preview: {cleaned_text[:100]}...")
            
        except Exception as e:
            logger.error(f"OCR failed for page {page_num + 1}: {e}")
            cleaned_text = ""
        
        # Try to get any native text (though likely none for scanned docs)
        native_text = page.get_text().strip()
        
        extracted_data = {
            'page_num': page_num,
            'image_path': str(image_path),
            'image_filename': image_filename,
            'ocr_text': cleaned_text,
            'native_text': native_text,
            'has_text': bool(cleaned_text.strip() or native_text.strip())
        }
        
        pix = None
        doc.close()
        return extracted_data
    
    def clean_and_format_ocr_text(self, text: str) -> str:
        """
        Clean and format OCR-extracted text with intelligent processing
        
        Args:
            text: Raw OCR text
            
        Returns:
            Cleaned and formatted text
        """
        if not text:
            return ""
        
        # Remove headers and footers
        text = self.remove_headers_footers(text)
        
        # Clean up common OCR artifacts
        text = self.clean_ocr_artifacts(text)
        
        # Normalize whitespace and line breaks
        text = self.normalize_text_formatting(text)
        
        # Detect and format headings, lists, etc.
        text = self.detect_and_format_structure(text)
        
        return text
    
    def remove_headers_footers(self, text: str) -> str:
        """
        Remove common headers and footers from the text
        
        Args:
            text: Raw text
            
        Returns:
            Text with headers/footers removed
        """
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line_lower = line.lower().strip()
            
            # Skip lines that match header/footer patterns
            skip_line = False
            for pattern in self.headers_footers:
                if re.search(pattern, line_lower):
                    skip_line = True
                    break
            
            # Skip very short lines that are likely noise
            if len(line.strip()) < 3:
                continue
                
            # Skip lines that are all numbers or special characters
            if line.strip().isdigit() or not any(c.isalpha() for c in line.strip()):
                continue
            
            if not skip_line:
                cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    def clean_ocr_artifacts(self, text: str) -> str:
        """
        Clean common OCR artifacts and noise
        
        Args:
            text: Raw text
            
        Returns:
            Cleaned text
        """
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove common OCR artifacts
        text = re.sub(r'[|_]{2,}', '', text)  # Remove excessive pipes/underscores
        text = re.sub(r'[^\w\s.,;:!?()[]{}\'"\-–—…•·]', '', text)  # Keep only valid characters
        
        # Fix common OCR mistakes
        text = text.replace('|', 'I')  # Common OCR mistake
        text = text.replace('0', 'O')  # In certain contexts
        text = text.replace('1', 'l')  # In certain contexts
        
        return text
    
    def normalize_text_formatting(self, text: str) -> str:
        """
        Normalize text formatting and remove excessive line breaks
        
        Args:
            text: Raw text
            
        Returns:
            Normalized text
        """
        # Split into lines and clean each line
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        # Join lines intelligently
        normalized_lines = []
        current_paragraph = []
        
        for line in lines:
            # If line starts with uppercase and previous line doesn't end with sentence ending
            if (line and line[0].isupper() and 
                current_paragraph and 
                not current_paragraph[-1].endswith(('.', '!', '?', ':'))):
                # Start new paragraph
                if current_paragraph:
                    normalized_lines.append(' '.join(current_paragraph))
                    current_paragraph = []
            
            current_paragraph.append(line)
        
        # Add the last paragraph
        if current_paragraph:
            normalized_lines.append(' '.join(current_paragraph))
        
        return '\n\n'.join(normalized_lines)
    
    def detect_and_format_structure(self, text: str) -> str:
        """
        Detect and format document structure (headings, lists, etc.)
        
        Args:
            text: Cleaned text
            
        Returns:
            Text with markdown formatting
        """
        lines = text.split('\n')
        formatted_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Detect headings (lines that are short, all caps, or end with numbers)
            if (len(line) < 100 and 
                (line.isupper() or 
                 re.match(r'^[IVX]+\.', line) or
                 re.match(r'^\d+\.', line) or
                 re.match(r'^[A-Z][a-z]+', line))):
                
                # Format as heading
                if line.isupper() and len(line) < 50:
                    formatted_lines.append(f"## {line}")
                else:
                    formatted_lines.append(f"### {line}")
            else:
                # Regular paragraph
                formatted_lines.append(line)
        
        return '\n\n'.join(formatted_lines)
    
    def create_clean_markdown(self, extracted_data: List[Dict[str, Any]], pdf_name: str) -> str:
        """
        Create clean, focused markdown without unnecessary elements
        
        Args:
            extracted_data: List of extracted page data
            pdf_name: Name of the original PDF file
            
        Returns:
            Clean markdown text
        """
        md_content = []
        
        # Simple header
        md_content.append(f"# {pdf_name.replace('.pdf', '').replace('_', ' ').title()}")
        md_content.append("")
        
        # Process each page
        for page_data in extracted_data:
            page_num = page_data['page_num'] + 1  # Convert to 1-based for display
            
            # Add page identifier (minimal)
            md_content.append(f"**Page {page_num}**")
            md_content.append("")
            
            # Add the cleaned text content
            if page_data['ocr_text']:
                md_content.append(page_data['ocr_text'])
            else:
                md_content.append("*No text could be extracted from this page*")
            
            md_content.append("")
            md_content.append("---")
            md_content.append("")
        
        return '\n'.join(md_content)
    
    def convert_pdf_to_markdown(
        self,
        pdf_path: str,
        output_filename: Optional[str] = None,
        pages: Optional[List[int]] = None,
        dpi: int = 300
    ) -> Dict[str, Any]:
        """
        Convert PDF to clean Markdown using improved OCR
        
        Args:
            pdf_path: Path to the input PDF file
            output_filename: Custom output filename (without extension)
            pages: List of specific page numbers to convert
            dpi: Resolution for extracted images
            
        Returns:
            Dictionary containing conversion results and metadata
        """
        pdf_path = Path(pdf_path)
        
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        logger.info(f"Converting PDF: {pdf_path.name}")
        logger.info(f"Pages to convert: {pages if pages else 'All pages'}")
        logger.info(f"Image DPI: {dpi}")
        logger.info(f"Using improved OCR with watermark removal and text cleaning")
        
        try:
            # Open PDF to get total page count
            doc = fitz.open(str(pdf_path))
            total_pages = len(doc)
            doc.close()
            
            if pages is None:
                pages = list(range(total_pages))
            
            logger.info(f"Processing {len(pages)} pages...")
            
            # Extract each page with improved OCR
            extracted_data = []
            for page_num in pages:
                if page_num >= total_pages:
                    logger.warning(f"Skipping page {page_num} (PDF only has {total_pages} pages)")
                    continue
                
                page_data = self.extract_page_with_improved_ocr(str(pdf_path), page_num, dpi)
                extracted_data.append(page_data)
            
            # Create clean markdown
            md_content = self.create_clean_markdown(extracted_data, pdf_path.name)
            
            # Save the markdown
            output_name = output_filename or pdf_path.stem
            output_file = self.output_dir / f"{output_name}_clean.md"
            output_file.write_text(md_content, encoding='utf-8')
            
            # Count pages with successful text extraction
            pages_with_text = sum(1 for p in extracted_data if p['has_text'])
            
            return {
                'success': True,
                'method': 'improved_ocr',
                'output_file': str(output_file),
                'extracted_pages': len(extracted_data),
                'pages_with_text': pages_with_text,
                'total_pages': total_pages
            }
            
        except Exception as e:
            logger.error(f"Conversion failed: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'method': 'failed'
            }

def main():
    """Main function for command-line usage"""
    parser = argparse.ArgumentParser(
        description="Improved OCR-Enabled PDF to Markdown Converter",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert PDF with improved OCR (all pages)
  python improved_ocr_converter.py input.pdf
  
  # Convert specific pages only
  python improved_ocr_converter.py input.pdf --pages 0 1 2 3 4
  
  # High-quality conversion with custom output
  python improved_ocr_converter.py input.pdf --output-name "converted" --dpi 300
  
  # Test with just first few pages
  python improved_ocr_converter.py input.pdf --pages 0 1 2 3 4
        """
    )
    
    parser.add_argument(
        'input',
        help='Input PDF file'
    )
    
    parser.add_argument(
        '--output-name',
        help='Custom output filename (without extension)'
    )
    
    parser.add_argument(
        '--output-dir',
        default='improved_output',
        help='Output directory for markdown files (default: improved_output)'
    )
    
    parser.add_argument(
        '--image-dir',
        default='improved_images',
        help='Directory for extracted images (default: improved_images)'
    )
    
    parser.add_argument(
        '--pages',
        type=int,
        nargs='+',
        help='Specific page numbers to convert (0-based)'
    )
    
    parser.add_argument(
        '--dpi',
        type=int,
        default=300,
        help='Resolution for extracted images (default: 300)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        converter = ImprovedOCRConverter(
            output_dir=args.output_dir,
            image_dir=args.image_dir
        )
        
        result = converter.convert_pdf_to_markdown(
            args.input,
            output_filename=args.output_name,
            pages=args.pages,
            dpi=args.dpi
        )
        
        if result['success']:
            logger.info("Improved OCR conversion completed successfully!")
            logger.info(f"Method used: {result['method']}")
            logger.info(f"Output file: {result['output_file']}")
            logger.info(f"Pages processed: {result['extracted_pages']}")
            logger.info(f"Pages with extracted text: {result['pages_with_text']}")
            logger.info(f"Total pages in PDF: {result['total_pages']}")
        else:
            logger.error(f"Conversion failed: {result.get('error', 'Unknown error')}")
            sys.exit(1)
    
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
