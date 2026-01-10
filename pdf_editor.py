"""
PDF Editor GUI Application
A comprehensive desktop application for editing PDF files using Tkinter and pypdf.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from tkinter.scrolledtext import ScrolledText
import os
from typing import List, Optional
try:
    from pypdf import PdfReader, PdfWriter, Transformation
    from pypdf.generic import RectangleObject
except ImportError:
    messagebox.showerror("Import Error",
                        "pypdf library not found. Please install it using:\npip install pypdf")
    exit(1)


class PDFEditorApp:
    """Main PDF Editor Application Class"""

    def __init__(self, root):
        self.root = root
        self.root.title("PDF Editor Pro")
        self.root.geometry("900x700")

        # Application state
        self.current_pdf_path: Optional[str] = None
        self.pdf_reader: Optional[PdfReader] = None
        self.pdf_writer: PdfWriter = PdfWriter()
        self.loaded_pages: List = []

        # Setup UI
        self.setup_ui()

    def setup_ui(self):
        """Setup the main user interface"""

        # Title
        title_frame = ttk.Frame(self.root, padding="10")
        title_frame.pack(fill=tk.X)
        ttk.Label(title_frame, text="PDF Editor Pro",
                 font=('Arial', 16, 'bold')).pack()

        # Main container
        main_container = ttk.Frame(self.root, padding="10")
        main_container.pack(fill=tk.BOTH, expand=True)

        # Left panel - Controls
        left_panel = ttk.Frame(main_container, padding="5")
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

        # File Operations Section
        file_frame = ttk.LabelFrame(left_panel, text="File Operations", padding="10")
        file_frame.pack(fill=tk.X, pady=5)

        ttk.Button(file_frame, text="Load PDF",
                  command=self.load_pdf, width=20).pack(pady=2)
        ttk.Button(file_frame, text="Save PDF",
                  command=self.save_pdf, width=20).pack(pady=2)

        # Edit Operations Section
        edit_frame = ttk.LabelFrame(left_panel, text="Edit Operations", padding="10")
        edit_frame.pack(fill=tk.X, pady=5)

        ttk.Button(edit_frame, text="Merge PDFs",
                  command=self.merge_pdfs, width=20).pack(pady=2)
        ttk.Button(edit_frame, text="Split PDF",
                  command=self.split_pdf, width=20).pack(pady=2)
        ttk.Button(edit_frame, text="Rotate Pages",
                  command=self.rotate_pages, width=20).pack(pady=2)
        ttk.Button(edit_frame, text="Crop Pages",
                  command=self.crop_pages, width=20).pack(pady=2)
        ttk.Button(edit_frame, text="Encrypt PDF",
                  command=self.encrypt_pdf, width=20).pack(pady=2)

        # Text Operations Section
        text_frame = ttk.LabelFrame(left_panel, text="Text Operations", padding="10")
        text_frame.pack(fill=tk.X, pady=5)

        ttk.Button(text_frame, text="Extract Text",
                  command=self.extract_text, width=20).pack(pady=2)
        ttk.Button(text_frame, text="Add Text Overlay",
                  command=self.add_text_overlay, width=20).pack(pady=2)

        # Right panel - Info Display
        right_panel = ttk.Frame(main_container, padding="5")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # PDF Info Section
        info_frame = ttk.LabelFrame(right_panel, text="PDF Information", padding="10")
        info_frame.pack(fill=tk.BOTH, expand=True)

        self.info_text = ScrolledText(info_frame, wrap=tk.WORD,
                                      width=50, height=30)
        self.info_text.pack(fill=tk.BOTH, expand=True)

        # Status bar
        self.status_bar = ttk.Label(self.root, text="Ready",
                                    relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def update_status(self, message: str):
        """Update status bar message"""
        self.status_bar.config(text=message)
        self.root.update_idletasks()

    def update_info_display(self, text: str):
        """Update the information display area"""
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(1.0, text)

    def load_pdf(self):
        """Load a PDF file and display information"""
        try:
            file_path = filedialog.askopenfilename(
                title="Select PDF File",
                filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")]
            )

            if not file_path:
                return

            self.current_pdf_path = file_path
            self.pdf_reader = PdfReader(file_path)
            self.loaded_pages = list(range(len(self.pdf_reader.pages)))

            # Display PDF information
            info = self.get_pdf_info()
            self.update_info_display(info)
            self.update_status(f"Loaded: {os.path.basename(file_path)}")

            messagebox.showinfo("Success",
                              f"PDF loaded successfully!\n{len(self.pdf_reader.pages)} pages found.")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load PDF:\n{str(e)}")
            self.update_status("Error loading PDF")

    def get_pdf_info(self) -> str:
        """Get detailed information about the loaded PDF"""
        if not self.pdf_reader:
            return "No PDF loaded"

        info_lines = []
        info_lines.append("=" * 50)
        info_lines.append("PDF DOCUMENT INFORMATION")
        info_lines.append("=" * 50)
        info_lines.append(f"\nFile: {os.path.basename(self.current_pdf_path)}")
        info_lines.append(f"Total Pages: {len(self.pdf_reader.pages)}")

        # Metadata
        if self.pdf_reader.metadata:
            info_lines.append("\nMetadata:")
            for key, value in self.pdf_reader.metadata.items():
                info_lines.append(f"  {key}: {value}")

        # Page details
        info_lines.append("\n" + "=" * 50)
        info_lines.append("PAGE DETAILS")
        info_lines.append("=" * 50)

        for i, page in enumerate(self.pdf_reader.pages, 1):
            box = page.mediabox
            width = float(box.width)
            height = float(box.height)
            info_lines.append(f"\nPage {i}:")
            info_lines.append(f"  Size: {width:.2f} x {height:.2f} points")
            info_lines.append(f"  Rotation: {page.get('/Rotate', 0)} degrees")

            # Try to get text preview
            try:
                text = page.extract_text()
                preview = text[:100].replace('\n', ' ') if text else "No text"
                info_lines.append(f"  Preview: {preview}...")
            except:
                info_lines.append("  Preview: Unable to extract")

        return "\n".join(info_lines)

    def merge_pdfs(self):
        """Merge multiple PDF files into one"""
        try:
            file_paths = filedialog.askopenfilenames(
                title="Select PDF Files to Merge",
                filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")]
            )

            if not file_paths or len(file_paths) < 2:
                messagebox.showwarning("Warning",
                                     "Please select at least 2 PDF files to merge")
                return

            self.update_status("Merging PDFs...")

            # Create new writer
            merger = PdfWriter()

            # Add all pages from all PDFs
            for file_path in file_paths:
                reader = PdfReader(file_path)
                for page in reader.pages:
                    merger.add_page(page)

            # Save merged PDF
            output_path = filedialog.asksaveasfilename(
                title="Save Merged PDF",
                defaultextension=".pdf",
                filetypes=[("PDF Files", "*.pdf")]
            )

            if output_path:
                with open(output_path, "wb") as output_file:
                    merger.write(output_file)

                self.update_status("Merge completed")
                messagebox.showinfo("Success",
                                  f"PDFs merged successfully!\nSaved to: {output_path}")
            else:
                self.update_status("Merge cancelled")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to merge PDFs:\n{str(e)}")
            self.update_status("Error merging PDFs")

    def split_pdf(self):
        """Split PDF into individual pages or ranges"""
        if not self.pdf_reader:
            messagebox.showwarning("Warning", "Please load a PDF file first")
            return

        try:
            # Ask user for split mode
            split_dialog = SplitDialog(self.root, len(self.pdf_reader.pages))
            self.root.wait_window(split_dialog.dialog)

            if not split_dialog.result:
                return

            mode = split_dialog.result['mode']

            # Select output directory
            output_dir = filedialog.askdirectory(title="Select Output Directory")
            if not output_dir:
                return

            self.update_status("Splitting PDF...")
            base_name = os.path.splitext(os.path.basename(self.current_pdf_path))[0]

            if mode == "individual":
                # Split into individual pages
                for i, page in enumerate(self.pdf_reader.pages, 1):
                    writer = PdfWriter()
                    writer.add_page(page)
                    output_path = os.path.join(output_dir, f"{base_name}_page_{i}.pdf")
                    with open(output_path, "wb") as output_file:
                        writer.write(output_file)

                messagebox.showinfo("Success",
                                  f"Split into {len(self.pdf_reader.pages)} individual pages")

            elif mode == "range":
                # Split by range
                ranges = split_dialog.result['ranges']
                for idx, (start, end) in enumerate(ranges, 1):
                    writer = PdfWriter()
                    for i in range(start - 1, end):
                        if i < len(self.pdf_reader.pages):
                            writer.add_page(self.pdf_reader.pages[i])
                    output_path = os.path.join(output_dir,
                                              f"{base_name}_part_{idx}_pages_{start}-{end}.pdf")
                    with open(output_path, "wb") as output_file:
                        writer.write(output_file)

                messagebox.showinfo("Success", f"Split into {len(ranges)} parts")

            self.update_status("Split completed")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to split PDF:\n{str(e)}")
            self.update_status("Error splitting PDF")

    def rotate_pages(self):
        """Rotate pages by specified degrees"""
        if not self.pdf_reader:
            messagebox.showwarning("Warning", "Please load a PDF file first")
            return

        try:
            # Get rotation parameters
            rotate_dialog = RotateDialog(self.root, len(self.pdf_reader.pages))
            self.root.wait_window(rotate_dialog.dialog)

            if not rotate_dialog.result:
                return

            angle = rotate_dialog.result['angle']
            pages = rotate_dialog.result['pages']

            self.update_status("Rotating pages...")

            # Create new PDF with rotated pages
            writer = PdfWriter()

            for i, page in enumerate(self.pdf_reader.pages):
                if i + 1 in pages:
                    page.rotate(angle)
                writer.add_page(page)

            # Save rotated PDF
            output_path = filedialog.asksaveasfilename(
                title="Save Rotated PDF",
                defaultextension=".pdf",
                filetypes=[("PDF Files", "*.pdf")]
            )

            if output_path:
                with open(output_path, "wb") as output_file:
                    writer.write(output_file)

                self.update_status("Rotation completed")
                messagebox.showinfo("Success",
                                  f"Pages rotated by {angle} degrees\nSaved to: {output_path}")
            else:
                self.update_status("Rotation cancelled")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to rotate pages:\n{str(e)}")
            self.update_status("Error rotating pages")

    def crop_pages(self):
        """Crop pages to custom dimensions"""
        if not self.pdf_reader:
            messagebox.showwarning("Warning", "Please load a PDF file first")
            return

        try:
            # Get crop parameters
            crop_dialog = CropDialog(self.root, len(self.pdf_reader.pages))
            self.root.wait_window(crop_dialog.dialog)

            if not crop_dialog.result:
                return

            pages = crop_dialog.result['pages']
            left = crop_dialog.result['left']
            bottom = crop_dialog.result['bottom']
            right = crop_dialog.result['right']
            top = crop_dialog.result['top']

            self.update_status("Cropping pages...")

            # Create new PDF with cropped pages
            writer = PdfWriter()

            for i, page in enumerate(self.pdf_reader.pages):
                if i + 1 in pages:
                    # Get current mediabox
                    media_box = page.mediabox

                    # Calculate new coordinates
                    new_left = float(media_box.left) + left
                    new_bottom = float(media_box.bottom) + bottom
                    new_right = float(media_box.right) - right
                    new_top = float(media_box.top) - top

                    # Apply crop
                    page.mediabox.lower_left = (new_left, new_bottom)
                    page.mediabox.upper_right = (new_right, new_top)

                writer.add_page(page)

            # Save cropped PDF
            output_path = filedialog.asksaveasfilename(
                title="Save Cropped PDF",
                defaultextension=".pdf",
                filetypes=[("PDF Files", "*.pdf")]
            )

            if output_path:
                with open(output_path, "wb") as output_file:
                    writer.write(output_file)

                self.update_status("Cropping completed")
                messagebox.showinfo("Success",
                                  f"Pages cropped successfully\nSaved to: {output_path}")
            else:
                self.update_status("Cropping cancelled")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to crop pages:\n{str(e)}")
            self.update_status("Error cropping pages")

    def encrypt_pdf(self):
        """Encrypt PDF with password"""
        if not self.pdf_reader:
            messagebox.showwarning("Warning", "Please load a PDF file first")
            return

        try:
            # Get password
            encrypt_dialog = EncryptDialog(self.root)
            self.root.wait_window(encrypt_dialog.dialog)

            if not encrypt_dialog.result:
                return

            user_password = encrypt_dialog.result['user_password']
            owner_password = encrypt_dialog.result.get('owner_password', user_password)

            self.update_status("Encrypting PDF...")

            # Create encrypted PDF
            writer = PdfWriter()

            # Add all pages
            for page in self.pdf_reader.pages:
                writer.add_page(page)

            # Add encryption (try AES-256, fall back to RC4-128 if cryptography not available)
            try:
                writer.encrypt(user_password=user_password,
                              owner_password=owner_password,
                              algorithm="AES-256")
            except Exception as e:
                if "cryptography" in str(e):
                    messagebox.showinfo("Encryption Notice",
                        "AES-256 requires 'cryptography' library.\n"
                        "Using RC4-128 encryption instead.\n\n"
                        "For AES-256: pip install cryptography")
                    writer.encrypt(user_password=user_password,
                                  owner_password=owner_password,
                                  algorithm="RC4-128")
                else:
                    raise

            # Save encrypted PDF
            output_path = filedialog.asksaveasfilename(
                title="Save Encrypted PDF",
                defaultextension=".pdf",
                filetypes=[("PDF Files", "*.pdf")]
            )

            if output_path:
                with open(output_path, "wb") as output_file:
                    writer.write(output_file)

                self.update_status("Encryption completed")
                messagebox.showinfo("Success",
                                  f"PDF encrypted successfully\nSaved to: {output_path}")
            else:
                self.update_status("Encryption cancelled")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to encrypt PDF:\n{str(e)}")
            self.update_status("Error encrypting PDF")

    def extract_text(self):
        """Extract text from PDF pages"""
        if not self.pdf_reader:
            messagebox.showwarning("Warning", "Please load a PDF file first")
            return

        try:
            # Ask which pages to extract
            page_range = simpledialog.askstring(
                "Extract Text",
                f"Enter page range (e.g., '1-5' or '1,3,5' or 'all'):\nTotal pages: {len(self.pdf_reader.pages)}"
            )

            if not page_range:
                return

            # Parse page range
            if page_range.lower() == 'all':
                pages_to_extract = list(range(len(self.pdf_reader.pages)))
            else:
                pages_to_extract = self.parse_page_range(page_range,
                                                         len(self.pdf_reader.pages))

            self.update_status("Extracting text...")

            # Extract text
            extracted_text = []
            extracted_text.append("=" * 50)
            extracted_text.append("EXTRACTED TEXT")
            extracted_text.append("=" * 50)

            for page_num in pages_to_extract:
                page = self.pdf_reader.pages[page_num]
                text = page.extract_text()
                extracted_text.append(f"\n--- Page {page_num + 1} ---\n")
                extracted_text.append(text)

            # Display extracted text
            text_content = "\n".join(extracted_text)
            self.update_info_display(text_content)

            # Ask to save to file
            save = messagebox.askyesno("Save Text",
                                      "Would you like to save the extracted text to a file?")
            if save:
                output_path = filedialog.asksaveasfilename(
                    title="Save Extracted Text",
                    defaultextension=".txt",
                    filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
                )
                if output_path:
                    with open(output_path, "w", encoding="utf-8") as f:
                        f.write(text_content)
                    messagebox.showinfo("Success", f"Text saved to: {output_path}")

            self.update_status("Text extraction completed")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to extract text:\n{str(e)}")
            self.update_status("Error extracting text")

    def add_text_overlay(self):
        """Add text overlay to PDF pages"""
        if not self.pdf_reader:
            messagebox.showwarning("Warning", "Please load a PDF file first")
            return

        try:
            # Get overlay parameters
            overlay_dialog = TextOverlayDialog(self.root, len(self.pdf_reader.pages))
            self.root.wait_window(overlay_dialog.dialog)

            if not overlay_dialog.result:
                return

            text = overlay_dialog.result['text']
            pages = overlay_dialog.result['pages']
            x = overlay_dialog.result['x']
            y = overlay_dialog.result['y']
            font_size = overlay_dialog.result['font_size']

            self.update_status("Adding text overlay...")

            # Create new PDF with text overlay using reportlab
            try:
                from reportlab.pdfgen import canvas
                from reportlab.lib.pagesizes import letter
                import io

                writer = PdfWriter()

                for i, page in enumerate(self.pdf_reader.pages):
                    if i + 1 in pages:
                        # Create overlay
                        packet = io.BytesIO()
                        can = canvas.Canvas(packet)

                        # Get page size
                        page_width = float(page.mediabox.width)
                        page_height = float(page.mediabox.height)
                        can.setPageSize((page_width, page_height))

                        # Add text
                        can.setFont("Helvetica", font_size)
                        can.drawString(x, y, text)
                        can.save()

                        # Move to beginning of buffer
                        packet.seek(0)

                        # Read overlay PDF
                        overlay_pdf = PdfReader(packet)
                        overlay_page = overlay_pdf.pages[0]

                        # Merge overlay with original page
                        page.merge_page(overlay_page)

                    writer.add_page(page)

            except ImportError:
                # Fallback: Add as annotation (simpler approach)
                messagebox.showinfo("Info",
                    "reportlab not installed. Text overlay feature requires reportlab.\n"
                    "Install with: pip install reportlab\n\n"
                    "As a workaround, the PDF will be saved without text overlay.")

                writer = PdfWriter()
                for page in self.pdf_reader.pages:
                    writer.add_page(page)

            # Save PDF with overlay
            output_path = filedialog.asksaveasfilename(
                title="Save PDF with Text Overlay",
                defaultextension=".pdf",
                filetypes=[("PDF Files", "*.pdf")]
            )

            if output_path:
                with open(output_path, "wb") as output_file:
                    writer.write(output_file)

                self.update_status("Text overlay completed")
                messagebox.showinfo("Success",
                                  f"Text overlay added\nSaved to: {output_path}")
            else:
                self.update_status("Text overlay cancelled")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to add text overlay:\n{str(e)}")
            self.update_status("Error adding text overlay")

    def save_pdf(self):
        """Save the current PDF"""
        if not self.pdf_reader:
            messagebox.showwarning("Warning", "Please load a PDF file first")
            return

        try:
            output_path = filedialog.asksaveasfilename(
                title="Save PDF",
                defaultextension=".pdf",
                filetypes=[("PDF Files", "*.pdf")]
            )

            if not output_path:
                return

            self.update_status("Saving PDF...")

            # Create writer and copy all pages
            writer = PdfWriter()
            for page in self.pdf_reader.pages:
                writer.add_page(page)

            with open(output_path, "wb") as output_file:
                writer.write(output_file)

            self.update_status("Save completed")
            messagebox.showinfo("Success", f"PDF saved to: {output_path}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save PDF:\n{str(e)}")
            self.update_status("Error saving PDF")

    @staticmethod
    def parse_page_range(range_str: str, total_pages: int) -> List[int]:
        """Parse page range string into list of page indices"""
        pages = []

        for part in range_str.split(','):
            part = part.strip()
            if '-' in part:
                start, end = part.split('-')
                start = int(start.strip())
                end = int(end.strip())
                pages.extend(range(start - 1, end))
            else:
                pages.append(int(part) - 1)

        # Validate and filter pages
        pages = [p for p in pages if 0 <= p < total_pages]
        return sorted(list(set(pages)))


class SplitDialog:
    """Dialog for split PDF options"""

    def __init__(self, parent, total_pages):
        self.result = None
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Split PDF")
        self.dialog.geometry("400x300")

        ttk.Label(self.dialog, text=f"Total Pages: {total_pages}",
                 font=('Arial', 10, 'bold')).pack(pady=10)

        # Split mode
        self.mode_var = tk.StringVar(value="individual")

        ttk.Radiobutton(self.dialog, text="Split into individual pages",
                       variable=self.mode_var, value="individual").pack(anchor=tk.W, padx=20)
        ttk.Radiobutton(self.dialog, text="Split by page ranges",
                       variable=self.mode_var, value="range").pack(anchor=tk.W, padx=20)

        # Range input
        range_frame = ttk.Frame(self.dialog, padding="10")
        range_frame.pack(fill=tk.X, padx=20, pady=10)

        ttk.Label(range_frame, text="Page ranges (e.g., 1-5,6-10):").pack(anchor=tk.W)
        self.range_entry = ttk.Entry(range_frame, width=30)
        self.range_entry.pack(fill=tk.X, pady=5)

        # Buttons
        button_frame = ttk.Frame(self.dialog, padding="10")
        button_frame.pack(side=tk.BOTTOM, fill=tk.X)

        ttk.Button(button_frame, text="OK", command=self.ok).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.cancel).pack(side=tk.RIGHT)

    def ok(self):
        mode = self.mode_var.get()
        self.result = {'mode': mode}

        if mode == "range":
            range_str = self.range_entry.get()
            if not range_str:
                messagebox.showwarning("Warning", "Please enter page ranges")
                return
            try:
                # Parse ranges
                ranges = []
                for part in range_str.split(','):
                    start, end = part.split('-')
                    ranges.append((int(start.strip()), int(end.strip())))
                self.result['ranges'] = ranges
            except:
                messagebox.showerror("Error", "Invalid range format")
                return

        self.dialog.destroy()

    def cancel(self):
        self.result = None
        self.dialog.destroy()


class RotateDialog:
    """Dialog for rotate pages options"""

    def __init__(self, parent, total_pages):
        self.result = None
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Rotate Pages")
        self.dialog.geometry("400x250")

        ttk.Label(self.dialog, text=f"Total Pages: {total_pages}",
                 font=('Arial', 10, 'bold')).pack(pady=10)

        # Angle selection
        angle_frame = ttk.Frame(self.dialog, padding="10")
        angle_frame.pack(fill=tk.X, padx=20)

        ttk.Label(angle_frame, text="Rotation Angle:").pack(anchor=tk.W)
        self.angle_var = tk.IntVar(value=90)

        for angle in [90, 180, 270, -90]:
            ttk.Radiobutton(angle_frame, text=f"{angle} degrees",
                           variable=self.angle_var, value=angle).pack(anchor=tk.W)

        # Page selection
        page_frame = ttk.Frame(self.dialog, padding="10")
        page_frame.pack(fill=tk.X, padx=20, pady=10)

        ttk.Label(page_frame, text="Pages (e.g., 1-5 or 1,3,5 or 'all'):").pack(anchor=tk.W)
        self.page_entry = ttk.Entry(page_frame, width=30)
        self.page_entry.insert(0, "all")
        self.page_entry.pack(fill=tk.X, pady=5)

        # Buttons
        button_frame = ttk.Frame(self.dialog, padding="10")
        button_frame.pack(side=tk.BOTTOM, fill=tk.X)

        ttk.Button(button_frame, text="OK", command=self.ok).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.cancel).pack(side=tk.RIGHT)

        self.total_pages = total_pages

    def ok(self):
        angle = self.angle_var.get()
        page_str = self.page_entry.get().strip()

        try:
            if page_str.lower() == 'all':
                pages = list(range(1, self.total_pages + 1))
            else:
                pages = []
                for part in page_str.split(','):
                    part = part.strip()
                    if '-' in part:
                        start, end = part.split('-')
                        pages.extend(range(int(start), int(end) + 1))
                    else:
                        pages.append(int(part))

            self.result = {'angle': angle, 'pages': pages}
            self.dialog.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Invalid page format:\n{str(e)}")

    def cancel(self):
        self.result = None
        self.dialog.destroy()


class CropDialog:
    """Dialog for crop pages options"""

    def __init__(self, parent, total_pages):
        self.result = None
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Crop Pages")
        self.dialog.geometry("400x350")

        ttk.Label(self.dialog, text=f"Total Pages: {total_pages}",
                 font=('Arial', 10, 'bold')).pack(pady=10)

        # Crop margins
        margin_frame = ttk.Frame(self.dialog, padding="10")
        margin_frame.pack(fill=tk.X, padx=20)

        ttk.Label(margin_frame, text="Crop Margins (in points):").pack(anchor=tk.W, pady=5)

        # Create margin inputs
        self.margins = {}
        for label in ['Left', 'Bottom', 'Right', 'Top']:
            frame = ttk.Frame(margin_frame)
            frame.pack(fill=tk.X, pady=2)
            ttk.Label(frame, text=f"{label}:", width=10).pack(side=tk.LEFT)
            entry = ttk.Entry(frame, width=15)
            entry.insert(0, "0")
            entry.pack(side=tk.LEFT)
            self.margins[label.lower()] = entry

        # Page selection
        page_frame = ttk.Frame(self.dialog, padding="10")
        page_frame.pack(fill=tk.X, padx=20, pady=10)

        ttk.Label(page_frame, text="Pages (e.g., 1-5 or 1,3,5 or 'all'):").pack(anchor=tk.W)
        self.page_entry = ttk.Entry(page_frame, width=30)
        self.page_entry.insert(0, "all")
        self.page_entry.pack(fill=tk.X, pady=5)

        # Buttons
        button_frame = ttk.Frame(self.dialog, padding="10")
        button_frame.pack(side=tk.BOTTOM, fill=tk.X)

        ttk.Button(button_frame, text="OK", command=self.ok).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.cancel).pack(side=tk.RIGHT)

        self.total_pages = total_pages

    def ok(self):
        try:
            # Get margins
            left = float(self.margins['left'].get())
            bottom = float(self.margins['bottom'].get())
            right = float(self.margins['right'].get())
            top = float(self.margins['top'].get())

            # Get pages
            page_str = self.page_entry.get().strip()
            if page_str.lower() == 'all':
                pages = list(range(1, self.total_pages + 1))
            else:
                pages = []
                for part in page_str.split(','):
                    part = part.strip()
                    if '-' in part:
                        start, end = part.split('-')
                        pages.extend(range(int(start), int(end) + 1))
                    else:
                        pages.append(int(part))

            self.result = {
                'left': left,
                'bottom': bottom,
                'right': right,
                'top': top,
                'pages': pages
            }
            self.dialog.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Invalid input:\n{str(e)}")

    def cancel(self):
        self.result = None
        self.dialog.destroy()


class EncryptDialog:
    """Dialog for PDF encryption options"""

    def __init__(self, parent):
        self.result = None
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Encrypt PDF")
        self.dialog.geometry("400x200")

        ttk.Label(self.dialog, text="PDF Encryption",
                 font=('Arial', 12, 'bold')).pack(pady=10)

        # Password inputs
        pwd_frame = ttk.Frame(self.dialog, padding="10")
        pwd_frame.pack(fill=tk.X, padx=20)

        # User password
        ttk.Label(pwd_frame, text="User Password:").pack(anchor=tk.W)
        self.user_pwd = ttk.Entry(pwd_frame, show="*", width=30)
        self.user_pwd.pack(fill=tk.X, pady=5)

        # Owner password
        ttk.Label(pwd_frame, text="Owner Password (optional):").pack(anchor=tk.W, pady=(10, 0))
        self.owner_pwd = ttk.Entry(pwd_frame, show="*", width=30)
        self.owner_pwd.pack(fill=tk.X, pady=5)

        # Buttons
        button_frame = ttk.Frame(self.dialog, padding="10")
        button_frame.pack(side=tk.BOTTOM, fill=tk.X)

        ttk.Button(button_frame, text="Encrypt", command=self.ok).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.cancel).pack(side=tk.RIGHT)

    def ok(self):
        user_password = self.user_pwd.get()

        if not user_password:
            messagebox.showwarning("Warning", "Please enter a user password")
            return

        owner_password = self.owner_pwd.get() or user_password

        self.result = {
            'user_password': user_password,
            'owner_password': owner_password
        }
        self.dialog.destroy()

    def cancel(self):
        self.result = None
        self.dialog.destroy()


class TextOverlayDialog:
    """Dialog for text overlay options"""

    def __init__(self, parent, total_pages):
        self.result = None
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add Text Overlay")
        self.dialog.geometry("450x350")

        ttk.Label(self.dialog, text=f"Total Pages: {total_pages}",
                 font=('Arial', 10, 'bold')).pack(pady=10)

        # Text input
        text_frame = ttk.Frame(self.dialog, padding="10")
        text_frame.pack(fill=tk.X, padx=20)

        ttk.Label(text_frame, text="Text to overlay:").pack(anchor=tk.W)
        self.text_entry = ttk.Entry(text_frame, width=40)
        self.text_entry.pack(fill=tk.X, pady=5)

        # Position inputs
        pos_frame = ttk.Frame(self.dialog, padding="10")
        pos_frame.pack(fill=tk.X, padx=20)

        ttk.Label(pos_frame, text="Position (in points from bottom-left):").pack(anchor=tk.W)

        xy_frame = ttk.Frame(pos_frame)
        xy_frame.pack(fill=tk.X, pady=5)

        ttk.Label(xy_frame, text="X:").pack(side=tk.LEFT)
        self.x_entry = ttk.Entry(xy_frame, width=10)
        self.x_entry.insert(0, "100")
        self.x_entry.pack(side=tk.LEFT, padx=5)

        ttk.Label(xy_frame, text="Y:").pack(side=tk.LEFT, padx=(20, 0))
        self.y_entry = ttk.Entry(xy_frame, width=10)
        self.y_entry.insert(0, "100")
        self.y_entry.pack(side=tk.LEFT, padx=5)

        # Font size
        font_frame = ttk.Frame(self.dialog, padding="10")
        font_frame.pack(fill=tk.X, padx=20)

        ttk.Label(font_frame, text="Font Size:").pack(side=tk.LEFT)
        self.font_size_entry = ttk.Entry(font_frame, width=10)
        self.font_size_entry.insert(0, "12")
        self.font_size_entry.pack(side=tk.LEFT, padx=5)

        # Page selection
        page_frame = ttk.Frame(self.dialog, padding="10")
        page_frame.pack(fill=tk.X, padx=20, pady=10)

        ttk.Label(page_frame, text="Pages (e.g., 1-5 or 1,3,5 or 'all'):").pack(anchor=tk.W)
        self.page_entry = ttk.Entry(page_frame, width=30)
        self.page_entry.insert(0, "all")
        self.page_entry.pack(fill=tk.X, pady=5)

        # Buttons
        button_frame = ttk.Frame(self.dialog, padding="10")
        button_frame.pack(side=tk.BOTTOM, fill=tk.X)

        ttk.Button(button_frame, text="OK", command=self.ok).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.cancel).pack(side=tk.RIGHT)

        self.total_pages = total_pages

    def ok(self):
        try:
            text = self.text_entry.get()
            if not text:
                messagebox.showwarning("Warning", "Please enter text to overlay")
                return

            x = float(self.x_entry.get())
            y = float(self.y_entry.get())
            font_size = int(self.font_size_entry.get())

            # Get pages
            page_str = self.page_entry.get().strip()
            if page_str.lower() == 'all':
                pages = list(range(1, self.total_pages + 1))
            else:
                pages = []
                for part in page_str.split(','):
                    part = part.strip()
                    if '-' in part:
                        start, end = part.split('-')
                        pages.extend(range(int(start), int(end) + 1))
                    else:
                        pages.append(int(part))

            self.result = {
                'text': text,
                'x': x,
                'y': y,
                'font_size': font_size,
                'pages': pages
            }
            self.dialog.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Invalid input:\n{str(e)}")

    def cancel(self):
        self.result = None
        self.dialog.destroy()


def main():
    """Main application entry point"""
    root = tk.Tk()
    app = PDFEditorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
