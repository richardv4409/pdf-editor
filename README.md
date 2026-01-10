# PDF Editor Pro

A comprehensive desktop GUI application for editing PDF files built with Python, Tkinter, and pypdf.

## Features

- **Load PDF**: Load and display detailed information about PDF files including metadata, page sizes, and text previews
- **Merge PDFs**: Combine multiple PDF files into a single document
- **Split PDF**: Split PDFs into individual pages or custom page ranges
- **Rotate Pages**: Rotate pages by 90, 180, or 270 degrees
- **Crop Pages**: Crop pages with custom margin values
- **Encrypt PDF**: Password-protect PDFs with AES-256 encryption
- **Extract Text**: Extract text from selected pages and save to file
- **Add Text Overlay**: Add custom text overlays to pages (requires reportlab)
- **Save PDF**: Save modified PDFs to new files

## Requirements

### Python Version
- Python 3.7 or higher

### Required Dependencies
```bash
pip install pypdf
```

### Optional Dependencies
For text overlay functionality:
```bash
pip install reportlab
```

## Installation

1. Ensure Python 3.7+ is installed
2. Install required dependencies:
   ```bash
   pip install pypdf
   ```
3. Optionally install reportlab for text overlay:
   ```bash
   pip install reportlab
   ```
4. Run the application:
   ```bash
   python pdf_editor.py
   ```

## Usage Guide

### Loading a PDF
1. Click **Load PDF** button
2. Select a PDF file from your system
3. View detailed information in the right panel including:
   - Total pages
   - Metadata (title, author, etc.)
   - Page dimensions
   - Text previews

### Merging PDFs
1. Click **Merge PDFs**
2. Select 2 or more PDF files (hold Ctrl/Cmd to select multiple)
3. Choose output location and filename
4. All pages from selected PDFs will be combined in order

### Splitting PDFs
1. Load a PDF first
2. Click **Split PDF**
3. Choose split mode:
   - **Individual pages**: Creates separate PDF for each page
   - **Page ranges**: Split into custom ranges (e.g., 1-5, 6-10)
4. Select output directory
5. Split files will be saved with descriptive names

### Rotating Pages
1. Load a PDF first
2. Click **Rotate Pages**
3. Select rotation angle: 90, 180, 270, or -90 degrees
4. Specify pages to rotate:
   - `all` - rotate all pages
   - `1-5` - rotate pages 1 through 5
   - `1,3,5` - rotate specific pages
5. Save rotated PDF to new file

### Cropping Pages
1. Load a PDF first
2. Click **Crop Pages**
3. Enter crop margins in points (72 points = 1 inch):
   - **Left**: crop from left edge
   - **Bottom**: crop from bottom edge
   - **Right**: crop from right edge
   - **Top**: crop from top edge
4. Specify pages to crop (same format as rotate)
5. Save cropped PDF to new file

### Encrypting PDFs
1. Load a PDF first
2. Click **Encrypt PDF**
3. Enter user password (required)
4. Optionally enter owner password (for additional permissions)
5. Save encrypted PDF with AES-256 encryption

### Extracting Text
1. Load a PDF first
2. Click **Extract Text**
3. Enter page range to extract:
   - `all` - extract from all pages
   - `1-5` - extract from pages 1 through 5
   - `1,3,5` - extract from specific pages
4. View extracted text in the info panel
5. Optionally save to .txt file

### Adding Text Overlay
1. Load a PDF first
2. Click **Add Text Overlay**
3. Enter text to overlay
4. Set position (X, Y coordinates in points from bottom-left)
5. Set font size
6. Specify pages to apply overlay
7. Save PDF with text overlay

**Note**: Text overlay requires reportlab. If not installed, you'll receive a notification.

## Technical Details

### PDF Coordinate System
- PDFs use a coordinate system with origin at bottom-left corner
- Measurements are in points (1 inch = 72 points)
- X increases to the right, Y increases upward

### Page Range Format
When specifying pages, use:
- `all` - all pages
- `1-5` - pages 1 through 5 (inclusive)
- `1,3,5` - specific pages 1, 3, and 5
- `1-3,5,7-9` - combination of ranges and individual pages

### Limitations
- Direct text editing is not supported by pypdf (text overlay is used as workaround)
- Some complex PDFs with special features may not process correctly
- Very large PDFs may take time to process

## Error Handling

The application includes comprehensive error handling:
- Invalid file format detection
- Password-protected PDF warnings
- Page range validation
- Numeric input validation
- File access error handling

## Project Structure

```
pdf_editor.py           # Main application file
README.md              # This file
```

### Main Components

**PDFEditorApp**: Main application class
- Manages UI and application state
- Coordinates all PDF operations

**Dialog Classes**:
- `SplitDialog`: Split options
- `RotateDialog`: Rotation options
- `CropDialog`: Crop options
- `EncryptDialog`: Encryption options
- `TextOverlayDialog`: Text overlay options

## Troubleshooting

### pypdf import error
```
pip install pypdf
```

### reportlab not found (text overlay)
```
pip install reportlab
```

### PDF won't load
- Ensure file is a valid PDF
- Check if PDF is password-protected
- Try opening in another PDF viewer first

### Operations not working
- Ensure PDF is loaded first (click Load PDF)
- Check page numbers are within valid range
- Verify write permissions for output directory

## Contributing

This is a standalone educational project. Feel free to modify and extend for your needs.

## License

This project is provided as-is for educational and personal use.

## Acknowledgments

- Built with Python's Tkinter (standard library)
- PDF manipulation powered by pypdf
- Optional text overlay using reportlab
