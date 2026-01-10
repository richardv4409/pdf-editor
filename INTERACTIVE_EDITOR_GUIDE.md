# Interactive PDF Editor Pro - User Guide

## Overview

An advanced interactive PDF editor with visual display, click-to-edit text, zoom/pan capabilities, and real-time preview. Built with Tkinter and PyMuPDF (fitz).

## Features

### Visual PDF Viewing
- **High-quality rendering**: PDF pages rendered as images with PyMuPDF
- **Page navigation**: First, Previous, Next, Last page buttons
- **Page counter**: Shows current page number and total pages

### Zoom & Pan
- **Zoom in/out**: Ctrl+Plus/Minus or dedicated buttons (25% to 500%)
- **Mouse wheel zoom**: Hold Ctrl + scroll to zoom
- **Reset zoom**: Ctrl+0 or Reset button (100%)
- **Fit width**: Automatically fit page width to window
- **Fit page**: Fit entire page in window
- **Pan view**: Pan tool or scroll when zoomed in

### Interactive Text Editing

#### Add Text Mode
1. Select "Add Text" tool from the left panel
2. Click anywhere on the PDF page
3. A floating entry box appears near your click
4. Type your text and click OK
5. Text appears at the clicked position with current font settings

#### Select/Move Text Mode
1. Select "Select/Move Text" tool
2. Click on any added text to select it (blue border appears)
3. Drag the text to reposition it
4. Click empty space to deselect

#### Text Properties
- **Font**: Choose from all system fonts via dropdown
- **Size**: 6-72 points (use +/- buttons or spinbox)
- **Color**: RGB color chooser with live preview

### Text Search & Replace
- **Search** (Ctrl+F): Find text across all pages, jump to first match
- **Replace** (Ctrl+H): Find and replace all occurrences globally

### Pan View Tool
- Select "Pan View" tool
- Click and drag to move the view (useful when zoomed in)

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl+O | Open PDF |
| Ctrl+S | Save PDF |
| Ctrl+F | Search Text |
| Ctrl+H | Replace Text |
| Ctrl++ | Zoom In |
| Ctrl+- | Zoom Out |
| Ctrl+0 | Reset Zoom (100%) |

## User Interface Layout

### Left Panel (Tools & Controls)

**Tools Section:**
- Radio buttons for Select/Move, Add Text, Pan View

**Text Properties:**
- Font dropdown (searchable)
- Size controls (+/- buttons and spinbox)
- Color picker with preview swatch

**Navigation:**
- First Page / Previous Page
- Current page display (e.g., "3 / 10")
- Next Page / Last Page

**Zoom:**
- Zoom In / Zoom Out / Reset buttons
- Current zoom percentage display

### Center Panel (PDF Viewer)
- Large canvas with scrollbars
- Displays rendered PDF page
- Shows all added text annotations
- Selected text highlighted with blue border

### Bottom Status Bar
- Left: Status messages and current tool
- Right: Mouse cursor coordinates (PDF space)

## Workflow Examples

### Example 1: Add Watermark to All Pages

1. Open PDF (Ctrl+O)
2. Select "Add Text" tool
3. Choose font: Arial, Size: 48, Color: Light Gray
4. Click center of page, type "DRAFT"
5. Navigate to next page
6. Repeat steps 4-5 for each page
7. Save PDF (Ctrl+S)

### Example 2: Add Form Field Labels

1. Open PDF form
2. Select "Add Text" tool
3. Set font: Helvetica, Size: 10, Color: Black
4. Click near each field and type label
5. Use Select tool to fine-tune positions
6. Save

### Example 3: Replace Company Name

1. Open PDF (Ctrl+O)
2. Press Ctrl+H (Replace Text)
3. Find: "Old Company Inc."
4. Replace with: "New Company LLC"
5. Click "Replace All"
6. Save PDF

### Example 4: Review Document with Zoom

1. Open PDF
2. Use Ctrl+Mouse Wheel to zoom to 200%
3. Use Pan tool to navigate zoomed view
4. Or use scrollbars to move around
5. Add review comments with Add Text tool

## Technical Details

### Coordinate System
- Origin: Top-left corner (0, 0)
- X increases to the right
- Y increases downward
- Units: Points (72 points = 1 inch)
- Cursor coordinates shown in status bar

### Text Annotations
- Stored in memory until saved
- Applied to PDF on save
- Support all PyMuPDF-compatible fonts
- RGB color (0-1 normalized internally)
- Font size scaled with zoom for display

### Zoom Behavior
- Visual only (doesn't affect PDF coordinates)
- Range: 0.25x (25%) to 5.0x (500%)
- Step: 0.25x (25%) per zoom in/out
- Mouse wheel: Hold Ctrl to zoom, release to scroll

### Saving
- **Save** (Ctrl+S): Overwrites original file (incremental save)
- **Save As**: Creates new file with all annotations
- Annotations permanently written to PDF

## Tips & Tricks

### Precise Text Placement
1. Zoom to 200-300% for fine positioning
2. Use coordinates in status bar as reference
3. Click to place, then use Select tool to adjust

### Quick Font Changes
- Font dropdown is searchable - just start typing
- Common fonts: Arial, Helvetica, Times New Roman
- Size spinbox accepts direct typing

### Color Preview
- Color swatch shows current color before applying
- Choose colors before adding text
- All new text uses current settings

### Navigating Large Documents
1. Use Fit Width initially to see full page
2. Zoom in to read/edit details
3. Use Pan tool or scrollbars when zoomed
4. Use page navigation buttons to move between pages

### Performance
- Large PDFs may take time to render at high zoom
- Recommended: Keep zoom below 300% for smooth performance
- Many annotations? Consider saving incrementally

## Limitations

### Current Limitations
1. **Direct text editing**: Cannot edit existing PDF text (only add new text)
2. **Complex fonts**: Some PDF embedded fonts not accessible
3. **Rendering speed**: Very large pages (>A3) may render slowly at high zoom
4. **Images**: Cannot add/edit images (text only)
5. **Forms**: Cannot edit PDF form fields directly

### Workarounds
- **Existing text**: Use Replace feature to cover with white background and add new text
- **Complex edits**: Use PyMuPDF's replace feature or redact + add annotation
- **Forms**: Add text labels/instructions, not field editing

## Troubleshooting

### Application won't start
```
Error: No module named 'fitz'
Solution: pip install PyMuPDF
```

### PDF won't open
- Check if PDF is corrupted
- Check if PDF is password-protected
- Try opening in another PDF viewer first

### Text appears in wrong position
- Coordinate system starts at top-left
- Y coordinate: Distance from top
- Check cursor coordinates in status bar

### Colors look wrong
- Ensure using RGB color (0-255)
- Check color preview swatch before applying
- Try standard colors first (black, red, blue)

### Cannot save PDF
- Check write permissions for file
- Check if file is open in another program
- Try Save As to different location

### Zoom is too slow
- Reduce zoom level (below 200%)
- Close other applications
- Navigate to simpler pages first

## Advanced Usage

### Batch Adding Similar Text
1. Set font properties once
2. Add text to page 1
3. Navigate to next page
4. Add same text (properties preserved)
5. Repeat for all pages

### Creating Templates
1. Add common text elements (headers, footers)
2. Save as template PDF
3. Open template, add variable content
4. Save as new file

### Review Workflow
1. Open PDF at 100%
2. Add review comments with Add Text
3. Use different colors for different comment types:
   - Red: Errors
   - Blue: Suggestions
   - Green: Approved
4. Save with comments embedded

## Dependencies

```bash
pip install PyMuPDF Pillow
```

- **PyMuPDF** (fitz): PDF rendering and manipulation
- **Pillow** (PIL): Image handling
- **Tkinter**: Built-in with Python (GUI)

## File Structure

```
pdf_editor_interactive.py    # Main application
INTERACTIVE_EDITOR_GUIDE.md  # This guide
```

## Comparison: Interactive vs. Batch Editor

| Feature | Interactive Editor | Batch Editor (pypdf) |
|---------|-------------------|---------------------|
| PDF Viewing | ✓ Visual display | ✗ No display |
| Click to add text | ✓ Yes | ✗ No |
| Zoom/Pan | ✓ Yes | ✗ No |
| Text dragging | ✓ Yes | ✗ No |
| Real-time preview | ✓ Yes | ✗ No |
| Page navigation | ✓ Visual | ✗ N/A |
| Merge PDFs | ✗ No | ✓ Yes |
| Split PDFs | ✗ No | ✓ Yes |
| Rotate pages | ✗ No | ✓ Yes |
| Crop pages | ✗ No | ✓ Yes |
| Encrypt PDFs | ✗ No | ✓ Yes |
| Best for | Interactive editing | Batch operations |

**Recommendation**: Use Interactive Editor for visual text placement and editing. Use Batch Editor (pdf_editor.py) for bulk operations like merging, splitting, rotating, etc.

## System Requirements

- **Python**: 3.7 or higher
- **OS**: Windows, macOS, Linux
- **Memory**: 4GB RAM minimum (8GB recommended for large PDFs)
- **Display**: 1024x768 minimum (1920x1080 recommended)

## Support

For issues or questions:
1. Check this guide first
2. Verify PyMuPDF is installed: `python -c "import fitz; print(fitz.__version__)"`
3. Test with sample PDF files first
4. Check console output for error messages

## Version History

**v1.0** (2026-01-07)
- Initial release
- Visual PDF viewing
- Click-to-add text with floating entry
- Zoom/pan functionality
- Text dragging and repositioning
- Font/size/color choosers
- Search and replace
- Real-time preview
- Mouse wheel zoom

---

*Created with Python, Tkinter, and PyMuPDF*
