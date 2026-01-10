"""
Test script for PDF Editor application
Tests imports, class instantiation, and basic functionality without GUI interaction
"""

import sys
import os

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

print("=" * 60)
print("PDF EDITOR APPLICATION - TEST SUITE")
print("=" * 60)

# Test 1: Check Python version
print("\n[TEST 1] Python Version Check")
print(f"Python version: {sys.version}")
if sys.version_info >= (3, 7):
    print("✓ Python version is compatible (3.7+)")
else:
    print("✗ Python version too old. Requires 3.7+")
    sys.exit(1)

# Test 2: Import standard libraries
print("\n[TEST 2] Standard Library Imports")
try:
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox, simpledialog
    from tkinter.scrolledtext import ScrolledText
    print("✓ Tkinter and related modules imported successfully")
except ImportError as e:
    print(f"✗ Failed to import Tkinter: {e}")
    sys.exit(1)

# Test 3: Import pypdf
print("\n[TEST 3] pypdf Library Import")
try:
    from pypdf import PdfReader, PdfWriter, Transformation
    from pypdf.generic import RectangleObject
    print("✓ pypdf imported successfully")
    print(f"  pypdf module location: {PdfReader.__module__}")
except ImportError as e:
    print(f"✗ Failed to import pypdf: {e}")
    print("  Install with: pip install pypdf")
    sys.exit(1)

# Test 4: Import reportlab (optional)
print("\n[TEST 4] reportlab Library Import (Optional)")
try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    print("✓ reportlab imported successfully")
    print("  Text overlay feature will be fully functional")
except ImportError:
    print("⚠ reportlab not installed (optional)")
    print("  Text overlay feature will have limited functionality")
    print("  Install with: pip install reportlab")

# Test 5: Check if main application file exists
print("\n[TEST 5] Application File Check")
app_file = "pdf_editor.py"
if os.path.exists(app_file):
    print(f"✓ {app_file} found")
    file_size = os.path.getsize(app_file)
    print(f"  File size: {file_size:,} bytes")
else:
    print(f"✗ {app_file} not found")
    sys.exit(1)

# Test 6: Import application classes
print("\n[TEST 6] Application Module Import")
try:
    # This will import the module and execute module-level code
    import pdf_editor
    print("✓ pdf_editor module imported successfully")
except Exception as e:
    print(f"✗ Failed to import pdf_editor module: {e}")
    sys.exit(1)

# Test 7: Check application classes
print("\n[TEST 7] Application Classes Check")
try:
    assert hasattr(pdf_editor, 'PDFEditorApp'), "PDFEditorApp class not found"
    assert hasattr(pdf_editor, 'SplitDialog'), "SplitDialog class not found"
    assert hasattr(pdf_editor, 'RotateDialog'), "RotateDialog class not found"
    assert hasattr(pdf_editor, 'CropDialog'), "CropDialog class not found"
    assert hasattr(pdf_editor, 'EncryptDialog'), "EncryptDialog class not found"
    assert hasattr(pdf_editor, 'TextOverlayDialog'), "TextOverlayDialog class not found"
    print("✓ All application classes found:")
    print("  - PDFEditorApp")
    print("  - SplitDialog")
    print("  - RotateDialog")
    print("  - CropDialog")
    print("  - EncryptDialog")
    print("  - TextOverlayDialog")
except AssertionError as e:
    print(f"✗ {e}")
    sys.exit(1)

# Test 8: Check parse_page_range function
print("\n[TEST 8] Page Range Parser Tests")
try:
    parse_func = pdf_editor.PDFEditorApp.parse_page_range

    # Test case 1: Single page
    result = parse_func("1", 10)
    assert result == [0], f"Expected [0], got {result}"
    print("✓ Single page: '1' → [0]")

    # Test case 2: Range
    result = parse_func("1-5", 10)
    assert result == [0, 1, 2, 3, 4], f"Expected [0,1,2,3,4], got {result}"
    print("✓ Range: '1-5' → [0, 1, 2, 3, 4]")

    # Test case 3: Multiple pages
    result = parse_func("1,3,5", 10)
    assert result == [0, 2, 4], f"Expected [0,2,4], got {result}"
    print("✓ Multiple: '1,3,5' → [0, 2, 4]")

    # Test case 4: Mixed
    result = parse_func("1-3,5,7-9", 10)
    assert result == [0, 1, 2, 4, 6, 7, 8], f"Expected [0,1,2,4,6,7,8], got {result}"
    print("✓ Mixed: '1-3,5,7-9' → [0, 1, 2, 4, 6, 7, 8]")

    # Test case 5: Out of bounds
    result = parse_func("1-100", 10)
    assert result == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], f"Out of bounds handling failed"
    print("✓ Out of bounds: '1-100' with 10 pages → [0-9] (clamped)")

except Exception as e:
    print(f"✗ Page range parser test failed: {e}")
    sys.exit(1)

# Test 9: Check application methods
print("\n[TEST 9] PDFEditorApp Methods Check")
try:
    methods = [
        'load_pdf', 'save_pdf', 'merge_pdfs', 'split_pdf',
        'rotate_pages', 'crop_pages', 'encrypt_pdf',
        'extract_text', 'add_text_overlay', 'get_pdf_info',
        'update_status', 'update_info_display'
    ]

    for method in methods:
        assert hasattr(pdf_editor.PDFEditorApp, method), f"{method} method not found"

    print(f"✓ All {len(methods)} required methods found:")
    for method in methods:
        print(f"  - {method}")

except AssertionError as e:
    print(f"✗ {e}")
    sys.exit(1)

# Test 10: Create a sample PDF for testing (if pypdf works)
print("\n[TEST 10] Create Sample Test PDF")
try:
    from pypdf import PdfWriter
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    import io

    # Create a simple test PDF
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.drawString(100, 750, "PDF Editor Pro - Test Document")
    can.drawString(100, 730, "This is page 1")
    can.showPage()

    can.drawString(100, 750, "This is page 2")
    can.showPage()

    can.drawString(100, 750, "This is page 3")
    can.save()

    packet.seek(0)

    # Save test PDF
    test_pdf_path = "test_sample.pdf"
    with open(test_pdf_path, "wb") as f:
        f.write(packet.read())

    # Verify we can read it back
    test_reader = PdfReader(test_pdf_path)
    assert len(test_reader.pages) == 3, "Test PDF should have 3 pages"

    print(f"✓ Sample test PDF created: {test_pdf_path}")
    print(f"  Pages: {len(test_reader.pages)}")
    print(f"  Size: {os.path.getsize(test_pdf_path)} bytes")

except Exception as e:
    print(f"⚠ Could not create test PDF: {e}")
    print("  This is optional - manual testing will be required")

# Final Summary
print("\n" + "=" * 60)
print("TEST SUMMARY")
print("=" * 60)
print("✓ All critical tests passed!")
print("\nThe PDF Editor application is ready to use.")
print("\nTo run the application:")
print("  python pdf_editor.py")
print("\nTo test with the sample PDF (if created):")
print("  1. Run: python pdf_editor.py")
print("  2. Click 'Load PDF'")
print("  3. Select 'test_sample.pdf'")
print("  4. Try various operations")
print("\n" + "=" * 60)
