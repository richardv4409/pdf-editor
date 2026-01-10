# PDF Editor Suite - Complete Guide

## Overview

This project contains **TWO** PDF editor applications, each optimized for different use cases:

1. **Interactive PDF Editor** (`pdf_editor_interactive.py`) - NEW! ✨
   - Visual PDF viewer with real-time editing
   - Click-to-add text with floating entry boxes
   - Drag-and-drop text positioning
   - Zoom, pan, and navigate pages
   - Perfect for: Visual editing, adding annotations, form filling

2. **Batch PDF Editor** (`pdf_editor.py`) - Original
   - Batch operations without visual display
   - Merge, split, rotate, crop, encrypt PDFs
   - Text extraction and overlay
   - Perfect for: Bulk operations, automated workflows

---

## 🆕 Interactive PDF Editor Pro

### What's New

The Interactive PDF Editor brings a modern, visual approach to PDF editing with these enhanced features:

#### ✨ Interactive Text Editing
- **Click to add text**: Click anywhere on the PDF to place text
- **Floating entry box**: Small dialog appears near your click for easy typing
- **Drag to reposition**: Select and drag text to fine-tune placement
- **Real-time preview**: See changes instantly as you edit
- **Select existing text**: Click on added text to select and move it

#### 🎨 Advanced Styling
- **Font chooser**: Dropdown with all system fonts (searchable)
- **Size controls**: 6-72 points with +/- buttons or direct entry
- **Color picker**: Full RGB color selection with live preview swatch
- **Settings preserved**: Font/size/color remembered between additions

#### 🔍 Zoom & Navigation
- **Mouse wheel zoom**: Hold Ctrl + scroll to zoom (25% to 500%)
- **Zoom buttons**: Zoom In, Zoom Out, Reset (100%)
- **Fit width/page**: Auto-fit to window size
- **Pan view**: Pan tool for navigating zoomed views
- **Smooth scrolling**: Scroll bars for precise positioning

#### 🔎 Search & Replace
- **Text search** (Ctrl+F): Find text across all pages
- **Text replace** (Ctrl+H): Replace all instances globally
- **Jump to results**: Auto-navigate to first match

### Quick Start

```bash
# Install dependencies
pip install PyMuPDF Pillow

# Launch the interactive editor
python pdf_editor_interactive.py
```

### Basic Workflow

1. **Open PDF**: Ctrl+O or File > Open PDF
2. **Add Text**:
   - Select "Add Text" tool from left panel
   - Choose font, size, and color
   - Click on PDF where you want text
   - Type in floating entry box, press Enter
3. **Reposition Text**:
   - Select "Select/Move Text" tool
   - Click on text to select (blue border appears)
   - Drag to new position
4. **Zoom & Navigate**:
   - Use Ctrl+Mouse Wheel to zoom
   - Use scrollbars or Pan tool to navigate
   - Use page navigation buttons to move between pages
5. **Save**: Ctrl+S or File > Save PDF

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+O` | Open PDF |
| `Ctrl+S` | Save PDF |
| `Ctrl+F` | Search Text |
| `Ctrl+H` | Replace Text |
| `Ctrl++` | Zoom In |
| `Ctrl+-` | Zoom Out |
| `Ctrl+0` | Reset Zoom |
| `Ctrl+Mouse Wheel` | Zoom In/Out |
| `Mouse Wheel` | Scroll |

### Interface Guide

```
┌─────────────────────────────────────────────────────────────┐
│ Menu Bar: File | Edit | View                                │
├──────────────┬──────────────────────────────────────────────┤
│              │                                              │
│  Tools       │                                              │
│  ○ Select    │                                              │
│  ● Add Text  │          PDF Canvas                          │
│  ○ Pan       │       (Rendered PDF Page)                    │
│              │                                              │
│  Font: Arial │                                              │
│  Size: 12    │                                              │
│  Color: ■    │                                              │
│              │                                              │
│  Navigation  │                                              │
│  Page: 1/10  │                                              │
│              │                                              │
│  Zoom: 100%  │                                              │
│              │                                              │
├──────────────┴──────────────────────────────────────────────┤
│ Status: Tool: Add Text              Position: X:123, Y:456 │
└─────────────────────────────────────────────────────────────┘
```

### Example Use Cases

#### 1. Adding Form Field Labels
```
Scenario: PDF form needs field labels
Steps:
1. Open form PDF
2. Select Add Text tool
3. Set font: Arial, size: 10, color: Black
4. Click above each field
5. Type label (Name:, Email:, Phone:, etc.)
6. Use Select tool to fine-tune positions
7. Save
```

#### 2. Adding Watermark
```
Scenario: Add "DRAFT" watermark to all pages
Steps:
1. Open PDF
2. Select Add Text tool
3. Set font: Arial, size: 48, color: Light Gray
4. Click center of page 1
5. Type "DRAFT"
6. Navigate to page 2
7. Repeat steps 4-5 for each page
8. Save
```

#### 3. Filling Out Forms
```
Scenario: Fill PDF form fields with text
Steps:
1. Open PDF form
2. Zoom to 150% for precision
3. Select Add Text tool
4. Click in each field
5. Type values
6. Adjust positions if needed with Select tool
7. Save filled form
```

### Tips & Best Practices

1. **Zoom for Precision**: Use 150-200% zoom when placing text precisely
2. **Color Coding**: Use different colors for different types of annotations
3. **Test Before Saving**: Drag text around to test positioning before saving
4. **Use Fit Width**: Start with "Fit Width" to see full page layout
5. **Save Often**: Save incrementally when adding many annotations

---

## 📦 Batch PDF Editor (Original)

### Features

The batch editor is perfect for operations that don't need visual preview:

- **Merge PDFs**: Combine multiple files into one
- **Split PDFs**: Individual pages or custom ranges
- **Rotate Pages**: 90°, 180°, 270° rotation
- **Crop Pages**: Custom margin cropping
- **Encrypt PDFs**: Password protection (AES-256)
- **Extract Text**: Save text to .txt files
- **Text Overlay**: Add text via coordinates (requires reportlab)

### Quick Start

```bash
# Install dependencies
pip install pypdf reportlab cryptography

# Launch the batch editor
python pdf_editor.py
```

### When to Use Batch Editor

- Merging multiple PDFs
- Splitting large PDFs into sections
- Rotating pages in bulk
- Cropping margins from all pages
- Encrypting sensitive documents
- Extracting text from many pages
- Automated/scripted workflows

---

## Comparison: Which Editor to Use?

| Task | Interactive Editor | Batch Editor |
|------|-------------------|--------------|
| Add text to specific locations | ✓ Best choice | ○ Possible |
| Visual positioning | ✓ Drag & drop | ✗ No display |
| Fill PDF forms | ✓ Click & type | ○ Coordinates |
| Merge 10 PDFs | ✗ Not available | ✓ Best choice |
| Split 100-page PDF | ✗ Not available | ✓ Best choice |
| Rotate all pages | ✗ Not available | ✓ Best choice |
| Add watermarks | ✓ Visual | ○ Programmatic |
| Review/annotate | ✓ Interactive | ✗ No display |
| Encrypt files | ✗ Not available | ✓ Available |

**Rule of thumb**: Use **Interactive** for visual editing, **Batch** for bulk operations.

---

## Installation

### Complete Installation (Both Editors)

```bash
# Install all dependencies
pip install -r requirements.txt

# Or install individually
pip install pypdf PyMuPDF reportlab cryptography Pillow
```

### requirements.txt

```
pypdf>=3.0.0
reportlab>=3.6.0
cryptography>=3.1
PyMuPDF>=1.23.0
Pillow>=9.0.0
```

### Minimal Installation

**Interactive Editor Only**:
```bash
pip install PyMuPDF Pillow
```

**Batch Editor Only**:
```bash
pip install pypdf reportlab
```

---

## Project Structure

```
26_Pdf_Editor/
│
├── pdf_editor_interactive.py      # Interactive visual editor (NEW!)
├── pdf_editor.py                  # Batch operations editor
│
├── test_interactive_features.py   # Interactive editor tests
├── test_pdf_editor.py             # Batch editor tests
├── demo_test.py                   # Functional demos
│
├── INTERACTIVE_EDITOR_GUIDE.md    # Detailed interactive guide
├── FEATURES_SHOWCASE.md           # Feature implementation details
├── README_INTERACTIVE.md          # This file
├── README.md                      # Original batch editor guide
├── QUICKSTART.md                  # Quick start guide
├── TEST_RESULTS.md                # Test results
│
├── requirements.txt               # All dependencies
│
└── test_*.pdf                     # Sample PDF files
```

---

## Testing

### Test Interactive Editor

```bash
# Run feature verification
python test_interactive_features.py

# Should show:
# ✓ All 13 features implemented
# ✓ 22 methods verified
# ✓ PyMuPDF operations successful
```

### Test Batch Editor

```bash
# Run unit tests
python test_pdf_editor.py

# Run functional demos
python demo_test.py

# Should create multiple test PDFs
```

### Manual Testing Workflow

```bash
# 1. Generate test PDFs
python demo_test.py

# 2. Test interactive editor
python pdf_editor_interactive.py
# - Open test_sample.pdf
# - Add text
# - Drag text
# - Test zoom
# - Save

# 3. Test batch editor
python pdf_editor.py
# - Load test_doc1.pdf
# - Merge with test_doc2.pdf
# - Split merged PDF
# - Test other operations
```

---

## Troubleshooting

### Interactive Editor Issues

**ImportError: No module named 'fitz'**
```bash
pip install PyMuPDF
```

**PDF won't render**
- Check if PDF is corrupted
- Try with test_sample.pdf first
- Check console for error messages

**Text appears in wrong position**
- Check zoom level (100% recommended for accuracy)
- Verify coordinates in status bar
- Try Fit Width view first

**Slow rendering**
- Reduce zoom below 200%
- Navigate to simpler pages
- Close other applications

### Batch Editor Issues

**Cannot encrypt PDF**
```bash
pip install cryptography
```

**Text overlay not working**
```bash
pip install reportlab
```

**PDF won't open**
- Check file permissions
- Verify PDF is not password-protected
- Try with test PDFs first

---

## Advanced Usage

### Combining Both Editors

Workflow example: Bulk process then fine-tune

```bash
# Step 1: Use Batch Editor
1. Merge 5 PDFs into one
2. Rotate specific pages
3. Crop margins

# Step 2: Use Interactive Editor
1. Open merged/processed PDF
2. Add titles and labels visually
3. Add form field labels
4. Add review comments
5. Save final version
```

### Scripting with Batch Editor

The batch editor can be imported and used in scripts:

```python
from pdf_editor import PDFEditorApp

# Programmatic usage possible
# See pdf_editor.py for method signatures
```

### Extending Interactive Editor

The interactive editor can be customized:

```python
# Modify pdf_editor_interactive.py

# Example: Add custom font presets
FONT_PRESETS = {
    "Title": ("Arial", 24, (0, 0, 0)),
    "Body": ("Helvetica", 12, (0, 0, 0)),
    "Highlight": ("Arial", 14, (255, 0, 0))
}

# Example: Add annotation layers
# Example: Add undo/redo stack
# See FEATURES_SHOWCASE.md for ideas
```

---

## Performance Tips

### Interactive Editor
- Keep zoom ≤ 200% for smooth performance
- Navigate to simpler pages first
- Save incrementally with many annotations
- Close other applications if rendering slow

### Batch Editor
- Process large PDFs in chunks
- Use specific page ranges when possible
- Close PDFs after processing
- Consider memory usage with 100+ page PDFs

---

## Known Limitations

### Interactive Editor
- Cannot edit existing PDF text (only add new)
- Cannot add images (text only)
- No undo/redo (yet)
- One annotation at a time

### Batch Editor
- No visual display
- Coordinates required for text placement
- Cannot preview before saving
- Sequential processing only

### Both Editors
- Password-protected PDFs need decryption first
- Some complex PDF features not supported
- Embedded fonts may not be accessible
- Very large PDFs (>500 pages) may be slow

---

## Future Enhancements

### Planned Features (Interactive Editor)
- [ ] Undo/Redo stack
- [ ] Multi-select annotations
- [ ] Annotation layers
- [ ] Image insertion
- [ ] Shape drawing (rectangles, circles, arrows)
- [ ] Text highlighting tool
- [ ] Signature tool
- [ ] Template system
- [ ] Export annotations separately

### Planned Features (Batch Editor)
- [ ] GUI preview mode
- [ ] Batch processing queue
- [ ] Command-line interface
- [ ] PDF comparison tool
- [ ] Metadata editor

---

## Getting Help

1. **Read the guides**:
   - INTERACTIVE_EDITOR_GUIDE.md - Detailed interactive editor guide
   - README.md - Batch editor guide
   - FEATURES_SHOWCASE.md - Implementation details

2. **Run tests**:
   ```bash
   python test_interactive_features.py
   python test_pdf_editor.py
   ```

3. **Try sample PDFs**:
   - Use test_sample.pdf, test_doc1.pdf, etc.
   - These are small, simple PDFs for testing

4. **Check console output**:
   - Look for error messages
   - Verify dependencies installed

---

## Contributing

This is an educational project. Feel free to:
- Fork and modify for your needs
- Add new features
- Report issues or suggestions
- Share improvements

---

## License

Provided as-is for educational and personal use.

---

## Acknowledgments

- **PyMuPDF** (fitz): PDF rendering and manipulation
- **pypdf**: PDF manipulation
- **reportlab**: PDF generation
- **Pillow**: Image processing
- **Tkinter**: GUI framework (Python standard library)

---

## Version History

### v2.0 (2026-01-07) - Interactive Editor Release
- ✨ NEW: Interactive PDF Editor with visual display
- ✨ Click-to-add text with floating entry boxes
- ✨ Drag-and-drop text positioning
- ✨ Font/size/color choosers
- ✨ Zoom and pan with mouse wheel
- ✨ Text search and replace
- ✨ Real-time preview
- ✨ Page navigation

### v1.0 (2026-01-07) - Batch Editor Release
- Initial release
- Merge, split, rotate, crop PDFs
- Encrypt PDFs
- Extract text
- Text overlay

---

**Both editors are fully functional and ready to use!** 🎉

Choose the Interactive Editor for visual editing tasks, and the Batch Editor for bulk operations. Together, they provide a complete PDF editing solution.

---

*Built with Python 3.12, Tkinter, PyMuPDF, and pypdf*
