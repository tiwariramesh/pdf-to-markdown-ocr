# PDF to Markdown OCR Converter

A powerful Python script that converts scanned PDF documents to clean, well-formatted Markdown using advanced OCR (Optical Character Recognition) technology. Perfect for digitizing scanned documents, books, and image-based PDFs.

## 🌟 Features

- **Advanced OCR Processing**: Uses Tesseract OCR with image preprocessing for maximum accuracy
- **Intelligent Text Cleaning**: Removes headers, footers, watermarks, and OCR artifacts
- **Smart Formatting**: Detects and formats headings, paragraphs, and document structure
- **Watermark Removal**: Enhanced image processing to reduce watermark interference
- **Clean Output**: Generates minimal, focused Markdown without unnecessary elements
- **Batch Processing**: Process multiple pages or entire documents
- **Cross-Platform**: Works on Windows, macOS, and Linux

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Tesseract OCR installed on your system

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/tiwariramesh/pdf-to-markdown-ocr.git
   cd pdf-to-markdown-ocr
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Tesseract OCR**:
   
   **macOS** (using Homebrew):
   ```bash
   brew install tesseract
   ```
   
   **Ubuntu/Debian**:
   ```bash
   sudo apt update
   sudo apt install tesseract-ocr
   ```
   
   **Windows**:
   - Download from: https://github.com/UB-Mannheim/tesseract/wiki
   - Add to PATH or update the script with your installation path

### Basic Usage

```bash
# Convert entire PDF
python improved_ocr_converter.py input.pdf

# Convert specific pages (0-based indexing)
python improved_ocr_converter.py input.pdf --pages 0 1 2 3 4

# High-quality conversion
python improved_ocr_converter.py input.pdf --dpi 300

# Verbose output
python improved_ocr_converter.py input.pdf --verbose
```

## 📖 Detailed Usage

### Command Line Options

```bash
python improved_ocr_converter.py [PDF_FILE] [OPTIONS]

Arguments:
  PDF_FILE              Input PDF file path

Options:
  --output-name NAME    Custom output filename (without extension)
  --output-dir DIR      Output directory (default: improved_output)
  --image-dir DIR       Directory for extracted images (default: improved_images)
  --pages N [N ...]     Specific page numbers to convert (0-based)
  --dpi DPI            Resolution for image extraction (default: 300)
  --verbose, -v        Enable verbose logging
  --help, -h           Show help message
```

### Examples

```bash
# Convert first 5 pages with custom output name
python improved_ocr_converter.py document.pdf --pages 0 1 2 3 4 --output-name "my_document"

# High-resolution conversion with custom directories
python improved_ocr_converter.py scan.pdf --dpi 400 --output-dir "results" --image-dir "extracted_images"

# Process with detailed logging
python improved_ocr_converter.py file.pdf --verbose
```

## 🔧 How It Works

1. **Image Extraction**: Extracts high-resolution images from PDF pages
2. **Image Preprocessing**: Enhances contrast, sharpness, and applies noise reduction
3. **OCR Processing**: Uses Tesseract with optimized settings for text extraction
4. **Text Cleaning**: Removes headers, footers, watermarks, and OCR artifacts
5. **Structure Detection**: Identifies headings, paragraphs, and formatting
6. **Markdown Generation**: Creates clean, readable Markdown output

## 📊 Output Structure

The script creates organized output:

```
improved_output/
├── document_clean.md          # Main converted document
└── ...

improved_images/
├── document-page-001.png      # Extracted page images
├── document-page-002.png
└── ...
```

## 🎯 Best Practices

### For Best OCR Results:
- Use PDFs with clear, high-contrast text
- Ensure DPI is at least 300 for good quality
- For poor quality scans, try higher DPI (400-600)

### Text Quality Optimization:
- The script automatically handles common OCR issues
- Watermarks and background text are filtered out
- Headers and footers are automatically removed

## 🛠️ Troubleshooting

### Common Issues:

**"Tesseract not found"**:
- Ensure Tesseract is installed and in your PATH
- On macOS, try: `brew install tesseract`
- On Windows, add Tesseract to your system PATH

**Poor OCR quality**:
- Try increasing DPI: `--dpi 400`
- Ensure your PDF has clear, readable text
- Check that the PDF isn't password protected

**Memory issues with large PDFs**:
- Process specific pages: `--pages 0 1 2 3 4`
- Use lower DPI for very large documents

## 🤝 Contributing

Contributions are welcome! Please feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) for OCR capabilities
- [PyMuPDF](https://github.com/pymupdf/PyMuPDF) for PDF processing
- [Pillow](https://github.com/python-pillow/Pillow) for image processing

## 📞 Support

If you find this tool useful, please ⭐ star the repository!

For issues and questions, please use the [GitHub Issues](https://github.com/your-username/pdf-to-markdown-ocr/issues) page.

---

**Made with ❤️ for the open source community**
