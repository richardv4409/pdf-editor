"""
Demonstration script for PDF Editor functionality
Shows how to use pypdf for various operations without GUI
"""

import sys
import os

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

print("=" * 70)
print("PDF EDITOR - FUNCTIONAL DEMONSTRATION")
print("=" * 70)

# Create test PDFs
print("\n[1] Creating Test PDF Files")
print("-" * 70)

def create_test_pdf(filename, num_pages, content_prefix):
    """Create a test PDF with specified number of pages"""
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)

    for page_num in range(1, num_pages + 1):
        can.drawString(100, 750, f"{content_prefix} - Page {page_num}")
        can.drawString(100, 730, f"This is page {page_num} of {num_pages}")
        can.drawString(100, 700, "Lorem ipsum dolor sit amet, consectetur adipiscing elit.")
        can.showPage()

    can.save()
    packet.seek(0)

    with open(filename, "wb") as f:
        f.write(packet.read())

    return filename

# Create test files
doc1 = create_test_pdf("test_doc1.pdf", 3, "Document 1")
doc2 = create_test_pdf("test_doc2.pdf", 2, "Document 2")
print(f"✓ Created: {doc1} (3 pages)")
print(f"✓ Created: {doc2} (2 pages)")

# Test 1: Read PDF Info
print("\n[2] Reading PDF Information")
print("-" * 70)
reader = PdfReader(doc1)
print(f"File: {doc1}")
print(f"  Number of pages: {len(reader.pages)}")
for i, page in enumerate(reader.pages, 1):
    box = page.mediabox
    print(f"  Page {i}: {float(box.width):.1f} x {float(box.height):.1f} points")

# Test 2: Extract Text
print("\n[3] Extracting Text")
print("-" * 70)
print(f"Extracting text from page 1 of {doc1}:")
page1_text = reader.pages[0].extract_text()
print(f"  Text preview: {page1_text[:80]}...")

# Test 3: Merge PDFs
print("\n[4] Merging PDFs")
print("-" * 70)
merger = PdfWriter()

reader1 = PdfReader(doc1)
reader2 = PdfReader(doc2)

for page in reader1.pages:
    merger.add_page(page)

for page in reader2.pages:
    merger.add_page(page)

merged_file = "test_merged.pdf"
with open(merged_file, "wb") as output_file:
    merger.write(output_file)

merged_reader = PdfReader(merged_file)
print(f"✓ Merged {doc1} and {doc2} into {merged_file}")
print(f"  Result: {len(merged_reader.pages)} pages (3 + 2 = 5)")

# Test 4: Split PDF
print("\n[5] Splitting PDF")
print("-" * 70)
reader = PdfReader(merged_file)

# Split into individual pages
for i, page in enumerate(reader.pages, 1):
    writer = PdfWriter()
    writer.add_page(page)

    output_file = f"test_split_page_{i}.pdf"
    with open(output_file, "wb") as f:
        writer.write(f)

    print(f"✓ Created: {output_file}")

# Test 5: Rotate Pages
print("\n[6] Rotating Pages")
print("-" * 70)
reader = PdfReader(doc1)
writer = PdfWriter()

for i, page in enumerate(reader.pages):
    if i == 1:  # Rotate only page 2
        page.rotate(90)
        print(f"  Rotating page {i+1} by 90 degrees")
    writer.add_page(page)

rotated_file = "test_rotated.pdf"
with open(rotated_file, "wb") as output_file:
    writer.write(output_file)

print(f"✓ Created: {rotated_file} (page 2 rotated)")

# Test 6: Crop Pages
print("\n[7] Cropping Pages")
print("-" * 70)
reader = PdfReader(doc1)
writer = PdfWriter()

page = reader.pages[0]
media_box = page.mediabox

# Crop 50 points from each side
crop_margin = 50
new_left = float(media_box.left) + crop_margin
new_bottom = float(media_box.bottom) + crop_margin
new_right = float(media_box.right) - crop_margin
new_top = float(media_box.top) - crop_margin

print(f"  Original size: {float(media_box.width):.1f} x {float(media_box.height):.1f}")
print(f"  Cropping {crop_margin} points from each side")

page.mediabox.lower_left = (new_left, new_bottom)
page.mediabox.upper_right = (new_right, new_top)

writer.add_page(page)

cropped_file = "test_cropped.pdf"
with open(cropped_file, "wb") as output_file:
    writer.write(output_file)

print(f"✓ Created: {cropped_file}")
print(f"  New size: {float(page.mediabox.width):.1f} x {float(page.mediabox.height):.1f}")

# Test 7: Encrypt PDF
print("\n[8] Encrypting PDF")
print("-" * 70)

# Check if cryptography is available
try:
    import cryptography
    has_crypto = True
except ImportError:
    has_crypto = False

if has_crypto:
    reader = PdfReader(doc1)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    password = "test123"

    try:
        writer.encrypt(user_password=password, owner_password=password, algorithm="AES-256")
        encryption_type = "AES-256"
    except:
        writer.encrypt(user_password=password, owner_password=password, algorithm="RC4-128")
        encryption_type = "RC4-128"

    encrypted_file = "test_encrypted.pdf"
    with open(encrypted_file, "wb") as output_file:
        writer.write(output_file)

    print(f"✓ Created: {encrypted_file}")
    print(f"  Password: {password}")
    print(f"  Encryption: {encryption_type}")

    # Verify encryption by trying to read
    try:
        encrypted_reader = PdfReader(encrypted_file)
        if encrypted_reader.is_encrypted:
            print(f"  ✓ PDF is encrypted")
            encrypted_reader.decrypt(password)
            print(f"  ✓ Successfully decrypted with password")
    except:
        print(f"  ✓ PDF is encrypted and cannot be read without password")
else:
    print("⚠ Skipping encryption test (cryptography library not installed)")
    print("  Install with: pip install cryptography")
    encrypted_file = None

# Test 8: Add Text Overlay
print("\n[9] Adding Text Overlay")
print("-" * 70)
reader = PdfReader(doc1)
writer = PdfWriter()

# Create overlay
packet = io.BytesIO()
can = canvas.Canvas(packet, pagesize=letter)
can.setFont("Helvetica-Bold", 24)
can.setFillColorRGB(1, 0, 0)  # Red color
can.drawString(150, 500, "WATERMARK - DEMO")
can.save()

packet.seek(0)
overlay_pdf = PdfReader(packet)
overlay_page = overlay_pdf.pages[0]

# Merge overlay with each page
for page in reader.pages:
    page.merge_page(overlay_page)
    writer.add_page(page)

overlay_file = "test_overlay.pdf"
with open(overlay_file, "wb") as output_file:
    writer.write(output_file)

print(f"✓ Created: {overlay_file}")
print(f"  Added red 'WATERMARK - DEMO' text overlay")

# Summary
print("\n" + "=" * 70)
print("DEMONSTRATION COMPLETE")
print("=" * 70)
print("\nCreated test files:")
test_files = [
    "test_doc1.pdf", "test_doc2.pdf", "test_merged.pdf",
    "test_split_page_1.pdf", "test_split_page_2.pdf", "test_split_page_3.pdf",
    "test_split_page_4.pdf", "test_split_page_5.pdf",
    "test_rotated.pdf", "test_cropped.pdf", "test_overlay.pdf"
]

if encrypted_file:
    test_files.append("test_encrypted.pdf")

print("\nInput files:")
print("  - test_doc1.pdf (3 pages)")
print("  - test_doc2.pdf (2 pages)")

print("\nOutput files:")
print("  - test_merged.pdf (merged: 5 pages)")
print("  - test_split_page_*.pdf (5 files, 1 page each)")
print("  - test_rotated.pdf (page 2 rotated 90°)")
print("  - test_cropped.pdf (cropped margins)")
if encrypted_file:
    print("  - test_encrypted.pdf (password: test123)")
print("  - test_overlay.pdf (with watermark)")

total_size = sum(os.path.getsize(f) for f in test_files if os.path.exists(f))
print(f"\nTotal size of test files: {total_size:,} bytes")

print("\n✓ All operations completed successfully!")
print("\nYou can now:")
print("  1. Open these PDFs in any PDF viewer to verify")
print("  2. Run 'python pdf_editor.py' to test with the GUI")
print("  3. Load any of these test files in the PDF Editor")

print("\n" + "=" * 70)
