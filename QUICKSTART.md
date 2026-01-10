# Quick Start Guide

## Installation (5 minutes)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install pypdf reportlab
```

### Step 2: Run the Application
```bash
python pdf_editor.py
```

## First Steps

### 1. Load Your First PDF
- Click **Load PDF** button
- Navigate to any PDF file on your computer
- Click **Open**
- View the PDF information in the right panel

### 2. Try Basic Operations

**Quick Merge**:
1. Click **Merge PDFs**
2. Select 2+ PDF files
3. Choose where to save
4. Done!

**Quick Rotate**:
1. Load a PDF
2. Click **Rotate Pages**
3. Select 90 degrees
4. Enter "all" for pages
5. Save!

**Quick Extract Text**:
1. Load a PDF
2. Click **Extract Text**
3. Enter "all"
4. View extracted text
5. Save to .txt if needed

## Common Use Cases

### Combine Multiple Documents
```
Use Case: Merge 3 reports into one PDF
Steps:
1. Click "Merge PDFs"
2. Select report1.pdf, report2.pdf, report3.pdf
3. Save as "combined_report.pdf"
```

### Fix Rotated Pages
```
Use Case: Rotate upside-down pages
Steps:
1. Load PDF with "Load PDF"
2. Click "Rotate Pages"
3. Choose 180 degrees
4. Enter problematic page numbers (e.g., "2,5,7")
5. Save rotated version
```

### Create Page Range Extracts
```
Use Case: Extract pages 10-20 from a large document
Steps:
1. Load large PDF
2. Click "Split PDF"
3. Choose "Split by page ranges"
4. Enter "10-20"
5. Select output folder
```

### Password Protect Sensitive Documents
```
Use Case: Encrypt confidential PDF
Steps:
1. Load PDF
2. Click "Encrypt PDF"
3. Enter strong password
4. Save encrypted version
```

## Tips

1. **Page Numbers**: Always start from 1 (not 0)
2. **All Pages**: Type "all" to apply to entire document
3. **Ranges**: Use format like "1-5,8,10-15"
4. **Coordinates**: Measured in points (72 points = 1 inch)
5. **Backups**: Original files are never modified

## Keyboard Tips

- Use file dialogs to navigate quickly
- Tab through input fields
- Enter key confirms dialog boxes
- Escape key cancels dialogs

## Next Steps

Check out the full README.md for:
- Detailed feature descriptions
- Advanced usage examples
- Troubleshooting guide
- Technical specifications

## Getting Help

If something doesn't work:
1. Check if PDF is loaded (status bar shows "Loaded: filename.pdf")
2. Verify page numbers are valid
3. Ensure output directory has write permissions
4. Check console for error messages

Enjoy editing your PDFs!
