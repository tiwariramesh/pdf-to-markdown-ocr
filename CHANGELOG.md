# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2024-08-27

### Added
- ✨ **Initial Release**: PDF to Markdown OCR Converter
- 🔧 **Advanced OCR Processing**: Tesseract integration with optimized settings
- 🖼️ **Image Preprocessing**: Contrast, sharpness, and noise reduction
- 🧹 **Intelligent Text Cleaning**: 
  - Header and footer removal
  - Watermark filtering
  - OCR artifact cleanup
  - Smart paragraph reconstruction
- 📝 **Structure Detection**: Automatic heading and formatting detection
- 📊 **Clean Output**: Minimal, focused Markdown generation
- 📖 **Comprehensive Documentation**: Installation, usage, and examples
- 🧪 **Example Script**: Ready-to-run demonstration
- 📦 **Sample PDF**: Test file included for immediate testing
- ⚖️ **MIT License**: Open source and free to use

### Features
- Support for scanned PDF documents
- Configurable DPI settings (default: 300)
- Selective page processing
- Verbose logging options
- Cross-platform compatibility (Windows, macOS, Linux)
- Organized output structure

### Technical Details
- **Python 3.9+** compatibility
- **Dependencies**: PyMuPDF, Tesseract, Pillow
- **OCR Engine**: Tesseract with PSM 6 and OEM 3 settings
- **Image Processing**: PIL-based preprocessing pipeline
- **Text Processing**: Regex-based cleaning and formatting
