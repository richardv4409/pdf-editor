"""
Interactive PDF Editor with PyMuPDF (fitz)
Enhanced visual PDF editor with click-to-edit, zoom, pan, and text manipulation
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser, font as tkfont
from tkinter.scrolledtext import ScrolledText
import fitz  # PyMuPDF
from PIL import Image, ImageTk
import io
from typing import Optional, List, Tuple, Dict
import os


class TextAnnotation:
    """Represents a text annotation on the PDF"""

    def __init__(self, page_num: int, x: float, y: float, text: str,
                 fontsize: int = 12, color: Tuple[float, float, float] = (0, 0, 0),
                 fontname: str = "helv"):
        self.page_num = page_num
        self.x = x
        self.y = y
        self.text = text
        self.fontsize = fontsize
        self.color = color  # RGB tuple (0-1 range)
        self.fontname = fontname
        self.rect = None  # Bounding rectangle (calculated)

    def calculate_rect(self, page):
        """Calculate bounding rectangle for this text"""
        # Estimate text width/height
        text_width = len(self.text) * self.fontsize * 0.6
        text_height = self.fontsize * 1.2
        self.rect = fitz.Rect(self.x, self.y - text_height,
                             self.x + text_width, self.y)
        return self.rect

    def contains_point(self, x: float, y: float) -> bool:
        """Check if point is within this annotation"""
        if self.rect:
            return self.rect.contains((x, y))
        return False


class FloatingTextEntry(tk.Toplevel):
    """Floating text entry window for adding/editing text"""

    def __init__(self, parent, x, y, callback, initial_text="", title="Add Text"):
        super().__init__(parent)
        self.callback = callback
        self.result = None

        # Window setup
        self.title(title)
        self.geometry(f"300x100+{x}+{y}")
        self.attributes('-topmost', True)
        self.resizable(False, False)

        # Entry field
        entry_frame = ttk.Frame(self, padding="10")
        entry_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(entry_frame, text="Text:").pack(anchor=tk.W)
        self.text_entry = ttk.Entry(entry_frame, width=40)
        self.text_entry.pack(fill=tk.X, pady=5)
        self.text_entry.insert(0, initial_text)
        self.text_entry.focus()

        # Buttons
        button_frame = ttk.Frame(entry_frame)
        button_frame.pack(fill=tk.X)

        ttk.Button(button_frame, text="OK", command=self.ok).pack(side=tk.RIGHT, padx=2)
        ttk.Button(button_frame, text="Cancel", command=self.cancel).pack(side=tk.RIGHT)

        # Bind Enter key
        self.text_entry.bind('<Return>', lambda e: self.ok())
        self.text_entry.bind('<Escape>', lambda e: self.cancel())

        # Handle window close
        self.protocol("WM_DELETE_WINDOW", self.cancel)

    def ok(self):
        self.result = self.text_entry.get()
        if self.callback:
            self.callback(self.result)
        self.destroy()

    def cancel(self):
        self.result = None
        self.destroy()


class InteractivePDFEditor:
    """Main Interactive PDF Editor Application"""

    def __init__(self, root):
        self.root = root
        self.root.title("Interactive PDF Editor Pro")
        self.root.geometry("1200x800")

        # PDF state
        self.pdf_document: Optional[fitz.Document] = None
        self.current_page_num: int = 0
        self.total_pages: int = 0
        self.pdf_path: Optional[str] = None

        # Display state
        self.zoom_level: float = 1.0
        self.pan_offset_x: int = 0
        self.pan_offset_y: int = 0
        self.current_pixmap = None
        self.current_photo = None

        # Interaction state
        self.is_panning: bool = False
        self.pan_start_x: int = 0
        self.pan_start_y: int = 0
        self.text_annotations: List[TextAnnotation] = []
        self.selected_annotation: Optional[TextAnnotation] = None
        self.is_dragging: bool = False
        self.drag_start_x: int = 0
        self.drag_start_y: int = 0

        # Text tool settings
        self.text_font: str = "Helvetica"
        self.text_size: int = 12
        self.text_color: Tuple[int, int, int] = (0, 0, 0)  # RGB 0-255
        self.text_color_normalized: Tuple[float, float, float] = (0, 0, 0)  # RGB 0-1

        # Tool mode
        self.current_tool: str = "select"  # "select", "add_text", "pan"

        # Setup UI
        self.setup_ui()

    def setup_ui(self):
        """Setup the main user interface"""

        # Menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open PDF", command=self.open_pdf, accelerator="Ctrl+O")
        file_menu.add_command(label="Save PDF", command=self.save_pdf, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As...", command=self.save_pdf_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Search Text", command=self.search_text, accelerator="Ctrl+F")
        edit_menu.add_command(label="Replace Text", command=self.replace_text, accelerator="Ctrl+H")

        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Zoom In", command=self.zoom_in, accelerator="Ctrl++")
        view_menu.add_command(label="Zoom Out", command=self.zoom_out, accelerator="Ctrl+-")
        view_menu.add_command(label="Reset Zoom", command=self.reset_zoom, accelerator="Ctrl+0")
        view_menu.add_separator()
        view_menu.add_command(label="Fit Width", command=self.fit_width)
        view_menu.add_command(label="Fit Page", command=self.fit_page)

        # Keyboard bindings
        self.root.bind('<Control-o>', lambda e: self.open_pdf())
        self.root.bind('<Control-s>', lambda e: self.save_pdf())
        self.root.bind('<Control-f>', lambda e: self.search_text())
        self.root.bind('<Control-h>', lambda e: self.replace_text())
        self.root.bind('<Control-plus>', lambda e: self.zoom_in())
        self.root.bind('<Control-minus>', lambda e: self.zoom_out())
        self.root.bind('<Control-0>', lambda e: self.reset_zoom())

        # Main container
        main_container = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_container.pack(fill=tk.BOTH, expand=True)

        # Left panel - Tools
        left_panel = ttk.Frame(main_container, width=250)
        main_container.add(left_panel, weight=0)

        # Tools section
        tools_frame = ttk.LabelFrame(left_panel, text="Tools", padding="10")
        tools_frame.pack(fill=tk.X, padx=5, pady=5)

        self.tool_var = tk.StringVar(value="select")

        ttk.Radiobutton(tools_frame, text="Select/Move Text", variable=self.tool_var,
                       value="select", command=self.change_tool).pack(anchor=tk.W, pady=2)
        ttk.Radiobutton(tools_frame, text="Add Text", variable=self.tool_var,
                       value="add_text", command=self.change_tool).pack(anchor=tk.W, pady=2)
        ttk.Radiobutton(tools_frame, text="Pan View", variable=self.tool_var,
                       value="pan", command=self.change_tool).pack(anchor=tk.W, pady=2)

        # Text properties
        text_props_frame = ttk.LabelFrame(left_panel, text="Text Properties", padding="10")
        text_props_frame.pack(fill=tk.X, padx=5, pady=5)

        # Font selection
        ttk.Label(text_props_frame, text="Font:").pack(anchor=tk.W)
        available_fonts = sorted(list(tkfont.families()))
        self.font_combo = ttk.Combobox(text_props_frame, values=available_fonts,
                                       width=20, state='readonly')
        self.font_combo.set("Helvetica")
        self.font_combo.pack(fill=tk.X, pady=2)
        self.font_combo.bind('<<ComboboxSelected>>', self.on_font_changed)

        # Font size
        ttk.Label(text_props_frame, text="Size:").pack(anchor=tk.W, pady=(10, 0))
        self.size_var = tk.IntVar(value=12)
        size_frame = ttk.Frame(text_props_frame)
        size_frame.pack(fill=tk.X, pady=2)

        ttk.Button(size_frame, text="-", width=3,
                  command=self.decrease_font_size).pack(side=tk.LEFT)
        size_spinbox = ttk.Spinbox(size_frame, from_=6, to=72,
                                   textvariable=self.size_var, width=5,
                                   command=self.on_size_changed)
        size_spinbox.pack(side=tk.LEFT, padx=5)
        ttk.Button(size_frame, text="+", width=3,
                  command=self.increase_font_size).pack(side=tk.LEFT)

        # Color selection
        ttk.Label(text_props_frame, text="Color:").pack(anchor=tk.W, pady=(10, 0))
        color_frame = ttk.Frame(text_props_frame)
        color_frame.pack(fill=tk.X, pady=2)

        self.color_display = tk.Canvas(color_frame, width=40, height=25,
                                       bg="black", relief=tk.SUNKEN, bd=1)
        self.color_display.pack(side=tk.LEFT, padx=(0, 5))

        ttk.Button(color_frame, text="Choose Color",
                  command=self.choose_color).pack(side=tk.LEFT)

        # Navigation
        nav_frame = ttk.LabelFrame(left_panel, text="Navigation", padding="10")
        nav_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(nav_frame, text="First Page",
                  command=self.first_page).pack(fill=tk.X, pady=2)
        ttk.Button(nav_frame, text="Previous Page",
                  command=self.previous_page).pack(fill=tk.X, pady=2)

        page_frame = ttk.Frame(nav_frame)
        page_frame.pack(fill=tk.X, pady=5)
        ttk.Label(page_frame, text="Page:").pack(side=tk.LEFT)
        self.page_label = ttk.Label(page_frame, text="0 / 0")
        self.page_label.pack(side=tk.LEFT, padx=5)

        ttk.Button(nav_frame, text="Next Page",
                  command=self.next_page).pack(fill=tk.X, pady=2)
        ttk.Button(nav_frame, text="Last Page",
                  command=self.last_page).pack(fill=tk.X, pady=2)

        # Zoom controls
        zoom_frame = ttk.LabelFrame(left_panel, text="Zoom", padding="10")
        zoom_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(zoom_frame, text="Zoom In (+)",
                  command=self.zoom_in).pack(fill=tk.X, pady=2)
        ttk.Button(zoom_frame, text="Zoom Out (-)",
                  command=self.zoom_out).pack(fill=tk.X, pady=2)
        ttk.Button(zoom_frame, text="Reset (100%)",
                  command=self.reset_zoom).pack(fill=tk.X, pady=2)

        self.zoom_label = ttk.Label(zoom_frame, text="100%")
        self.zoom_label.pack(pady=5)

        # Center panel - PDF viewer
        center_panel = ttk.Frame(main_container)
        main_container.add(center_panel, weight=1)

        # Canvas for PDF display
        canvas_frame = ttk.Frame(center_panel)
        canvas_frame.pack(fill=tk.BOTH, expand=True)

        # Scrollbars
        h_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        v_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Canvas
        self.canvas = tk.Canvas(canvas_frame, bg='gray75',
                               xscrollcommand=h_scrollbar.set,
                               yscrollcommand=v_scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        h_scrollbar.config(command=self.canvas.xview)
        v_scrollbar.config(command=self.canvas.yview)

        # Canvas bindings
        self.canvas.bind('<Button-1>', self.on_canvas_click)
        self.canvas.bind('<B1-Motion>', self.on_canvas_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_canvas_release)
        self.canvas.bind('<MouseWheel>', self.on_mouse_wheel)
        self.canvas.bind('<Motion>', self.on_canvas_motion)

        # Status bar
        status_frame = ttk.Frame(self.root)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.status_label = ttk.Label(status_frame, text="Ready",
                                      relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.cursor_label = ttk.Label(status_frame, text="",
                                      relief=tk.SUNKEN, width=20)
        self.cursor_label.pack(side=tk.RIGHT)

    def update_status(self, message: str):
        """Update status bar message"""
        self.status_label.config(text=message)
        self.root.update_idletasks()

    def change_tool(self):
        """Handle tool change"""
        self.current_tool = self.tool_var.get()
        tool_names = {
            "select": "Select/Move Text",
            "add_text": "Add Text",
            "pan": "Pan View"
        }
        self.update_status(f"Tool: {tool_names.get(self.current_tool, 'Unknown')}")

        # Update cursor
        if self.current_tool == "add_text":
            self.canvas.config(cursor="crosshair")
        elif self.current_tool == "pan":
            self.canvas.config(cursor="fleur")
        else:
            self.canvas.config(cursor="arrow")

    def on_font_changed(self, event=None):
        """Handle font selection change"""
        self.text_font = self.font_combo.get()

    def on_size_changed(self, event=None):
        """Handle font size change"""
        self.text_size = self.size_var.get()

    def increase_font_size(self):
        """Increase font size"""
        current = self.size_var.get()
        self.size_var.set(min(72, current + 2))
        self.text_size = self.size_var.get()

    def decrease_font_size(self):
        """Decrease font size"""
        current = self.size_var.get()
        self.size_var.set(max(6, current - 2))
        self.text_size = self.size_var.get()

    def choose_color(self):
        """Open color chooser dialog"""
        color = colorchooser.askcolor(
            color=f"#{self.text_color[0]:02x}{self.text_color[1]:02x}{self.text_color[2]:02x}",
            title="Choose Text Color"
        )

        if color[0]:  # color[0] is RGB tuple, color[1] is hex string
            self.text_color = tuple(int(c) for c in color[0])
            self.text_color_normalized = tuple(c / 255.0 for c in self.text_color)

            # Update color display
            hex_color = color[1]
            self.color_display.config(bg=hex_color)

    def open_pdf(self):
        """Open a PDF file"""
        file_path = filedialog.askopenfilename(
            title="Select PDF File",
            filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")]
        )

        if not file_path:
            return

        try:
            self.update_status("Opening PDF...")

            # Close previous document if any
            if self.pdf_document:
                self.pdf_document.close()

            # Open new document
            self.pdf_document = fitz.open(file_path)
            self.pdf_path = file_path
            self.total_pages = len(self.pdf_document)
            self.current_page_num = 0

            # Reset state
            self.text_annotations = []
            self.selected_annotation = None
            self.zoom_level = 1.0
            self.pan_offset_x = 0
            self.pan_offset_y = 0

            # Display first page
            self.display_current_page()

            self.update_status(f"Opened: {os.path.basename(file_path)} ({self.total_pages} pages)")
            messagebox.showinfo("Success", f"PDF loaded successfully!\n{self.total_pages} pages")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to open PDF:\n{str(e)}")
            self.update_status("Error opening PDF")

    def display_current_page(self):
        """Render and display the current PDF page"""
        if not self.pdf_document:
            return

        try:
            # Get current page
            page = self.pdf_document[self.current_page_num]

            # Create transformation matrix for zoom
            mat = fitz.Matrix(self.zoom_level, self.zoom_level)

            # Render page to pixmap
            pix = page.get_pixmap(matrix=mat, alpha=False)
            self.current_pixmap = pix

            # Convert to PIL Image
            img_data = pix.tobytes("ppm")
            img = Image.open(io.BytesIO(img_data))

            # Draw annotations
            img = self.draw_annotations(img, page, mat)

            # Convert to PhotoImage
            self.current_photo = ImageTk.PhotoImage(img)

            # Update canvas
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.current_photo)

            # Update scroll region
            self.canvas.config(scrollregion=(0, 0, pix.width, pix.height))

            # Update page label
            self.page_label.config(text=f"{self.current_page_num + 1} / {self.total_pages}")

            # Update zoom label
            self.zoom_label.config(text=f"{int(self.zoom_level * 100)}%")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to display page:\n{str(e)}")

    def draw_annotations(self, img, page, mat):
        """Draw text annotations on the image"""
        from PIL import ImageDraw, ImageFont

        draw = ImageDraw.Draw(img)

        # Draw each annotation for current page
        for annot in self.text_annotations:
            if annot.page_num == self.current_page_num:
                # Transform coordinates
                x = annot.x * mat.a
                y = annot.y * mat.d
                size = int(annot.fontsize * self.zoom_level)

                # Try to load font
                try:
                    font = ImageFont.truetype("arial.ttf", size)
                except:
                    font = ImageFont.load_default()

                # Convert color from 0-1 to 0-255
                color = tuple(int(c * 255) for c in annot.color)

                # Draw text
                draw.text((x, y - size), annot.text, fill=color, font=font)

                # Draw selection rectangle if selected
                if annot == self.selected_annotation:
                    bbox = draw.textbbox((x, y - size), annot.text, font=font)
                    draw.rectangle(bbox, outline="blue", width=2)

        return img

    def canvas_to_pdf_coords(self, canvas_x: int, canvas_y: int) -> Tuple[float, float]:
        """Convert canvas coordinates to PDF coordinates"""
        # Account for scroll position
        scroll_x = self.canvas.canvasx(canvas_x)
        scroll_y = self.canvas.canvasy(canvas_y)

        # Account for zoom
        pdf_x = scroll_x / self.zoom_level
        pdf_y = scroll_y / self.zoom_level

        return pdf_x, pdf_y

    def on_canvas_click(self, event):
        """Handle canvas click events"""
        if not self.pdf_document:
            return

        pdf_x, pdf_y = self.canvas_to_pdf_coords(event.x, event.y)

        if self.current_tool == "add_text":
            # Add text mode - show floating entry
            self.show_text_entry(event.x_root, event.y_root, pdf_x, pdf_y)

        elif self.current_tool == "select":
            # Select mode - check if clicking on annotation
            clicked_annot = None
            for annot in self.text_annotations:
                if annot.page_num == self.current_page_num:
                    # Calculate rect in canvas coordinates
                    annot_x = annot.x * self.zoom_level
                    annot_y = annot.y * self.zoom_level
                    annot_size = annot.fontsize * self.zoom_level

                    # Simple bounding box check
                    text_width = len(annot.text) * annot_size * 0.6
                    text_height = annot_size * 1.2

                    scroll_x = self.canvas.canvasx(event.x)
                    scroll_y = self.canvas.canvasy(event.y)

                    if (annot_x <= scroll_x <= annot_x + text_width and
                        annot_y - text_height <= scroll_y <= annot_y):
                        clicked_annot = annot
                        break

            if clicked_annot:
                self.selected_annotation = clicked_annot
                self.is_dragging = True
                self.drag_start_x = pdf_x
                self.drag_start_y = pdf_y
                self.display_current_page()
            else:
                self.selected_annotation = None
                self.display_current_page()

        elif self.current_tool == "pan":
            # Pan mode
            self.is_panning = True
            self.pan_start_x = event.x
            self.pan_start_y = event.y

    def on_canvas_drag(self, event):
        """Handle canvas drag events"""
        if self.is_dragging and self.selected_annotation:
            # Drag annotation
            pdf_x, pdf_y = self.canvas_to_pdf_coords(event.x, event.y)
            dx = pdf_x - self.drag_start_x
            dy = pdf_y - self.drag_start_y

            self.selected_annotation.x += dx
            self.selected_annotation.y += dy

            self.drag_start_x = pdf_x
            self.drag_start_y = pdf_y

            self.display_current_page()

        elif self.is_panning:
            # Pan view
            dx = event.x - self.pan_start_x
            dy = event.y - self.pan_start_y

            self.canvas.xview_scroll(-dx, "units")
            self.canvas.yview_scroll(-dy, "units")

            self.pan_start_x = event.x
            self.pan_start_y = event.y

    def on_canvas_release(self, event):
        """Handle canvas button release"""
        self.is_dragging = False
        self.is_panning = False

    def on_canvas_motion(self, event):
        """Handle mouse motion over canvas"""
        if not self.pdf_document:
            return

        pdf_x, pdf_y = self.canvas_to_pdf_coords(event.x, event.y)
        self.cursor_label.config(text=f"X: {int(pdf_x)}, Y: {int(pdf_y)}")

    def on_mouse_wheel(self, event):
        """Handle mouse wheel for zooming"""
        if event.state & 0x0004:  # Ctrl key
            # Zoom
            if event.delta > 0:
                self.zoom_in()
            else:
                self.zoom_out()
        else:
            # Scroll
            if event.delta > 0:
                self.canvas.yview_scroll(-1, "units")
            else:
                self.canvas.yview_scroll(1, "units")

    def show_text_entry(self, screen_x: int, screen_y: int, pdf_x: float, pdf_y: float):
        """Show floating text entry dialog"""

        def on_text_entered(text):
            if text and text.strip():
                # Create new annotation
                annot = TextAnnotation(
                    page_num=self.current_page_num,
                    x=pdf_x,
                    y=pdf_y,
                    text=text,
                    fontsize=self.text_size,
                    color=self.text_color_normalized,
                    fontname=self.text_font
                )
                self.text_annotations.append(annot)
                self.display_current_page()
                self.update_status(f"Added text: '{text}'")

        FloatingTextEntry(self.root, screen_x, screen_y, on_text_entered)

    def zoom_in(self):
        """Zoom in"""
        self.zoom_level = min(5.0, self.zoom_level + 0.25)
        self.display_current_page()

    def zoom_out(self):
        """Zoom out"""
        self.zoom_level = max(0.25, self.zoom_level - 0.25)
        self.display_current_page()

    def reset_zoom(self):
        """Reset zoom to 100%"""
        self.zoom_level = 1.0
        self.display_current_page()

    def fit_width(self):
        """Fit page width to window"""
        if not self.pdf_document:
            return

        page = self.pdf_document[self.current_page_num]
        page_width = page.rect.width
        canvas_width = self.canvas.winfo_width()

        self.zoom_level = canvas_width / page_width
        self.display_current_page()

    def fit_page(self):
        """Fit entire page to window"""
        if not self.pdf_document:
            return

        page = self.pdf_document[self.current_page_num]
        page_width = page.rect.width
        page_height = page.rect.height
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        zoom_x = canvas_width / page_width
        zoom_y = canvas_height / page_height

        self.zoom_level = min(zoom_x, zoom_y)
        self.display_current_page()

    def first_page(self):
        """Go to first page"""
        if self.pdf_document and self.current_page_num > 0:
            self.current_page_num = 0
            self.display_current_page()

    def previous_page(self):
        """Go to previous page"""
        if self.pdf_document and self.current_page_num > 0:
            self.current_page_num -= 1
            self.display_current_page()

    def next_page(self):
        """Go to next page"""
        if self.pdf_document and self.current_page_num < self.total_pages - 1:
            self.current_page_num += 1
            self.display_current_page()

    def last_page(self):
        """Go to last page"""
        if self.pdf_document and self.current_page_num < self.total_pages - 1:
            self.current_page_num = self.total_pages - 1
            self.display_current_page()

    def search_text(self):
        """Search for text in PDF"""
        if not self.pdf_document:
            messagebox.showwarning("Warning", "Please open a PDF first")
            return

        search_window = tk.Toplevel(self.root)
        search_window.title("Search Text")
        search_window.geometry("400x150")

        ttk.Label(search_window, text="Search for:").pack(pady=10)
        search_entry = ttk.Entry(search_window, width=40)
        search_entry.pack(pady=5)
        search_entry.focus()

        result_label = ttk.Label(search_window, text="")
        result_label.pack(pady=10)

        def do_search():
            search_term = search_entry.get()
            if not search_term:
                return

            found_pages = []
            for page_num in range(len(self.pdf_document)):
                page = self.pdf_document[page_num]
                text_instances = page.search_for(search_term)
                if text_instances:
                    found_pages.append(page_num + 1)

            if found_pages:
                result_label.config(
                    text=f"Found on pages: {', '.join(map(str, found_pages))}"
                )
                # Go to first found page
                self.current_page_num = found_pages[0] - 1
                self.display_current_page()
            else:
                result_label.config(text="Text not found")

        ttk.Button(search_window, text="Search", command=do_search).pack(pady=5)

    def replace_text(self):
        """Replace text in PDF"""
        if not self.pdf_document:
            messagebox.showwarning("Warning", "Please open a PDF first")
            return

        replace_window = tk.Toplevel(self.root)
        replace_window.title("Replace Text")
        replace_window.geometry("400x200")

        ttk.Label(replace_window, text="Find:").pack(pady=5)
        find_entry = ttk.Entry(replace_window, width=40)
        find_entry.pack(pady=5)

        ttk.Label(replace_window, text="Replace with:").pack(pady=5)
        replace_entry = ttk.Entry(replace_window, width=40)
        replace_entry.pack(pady=5)

        result_label = ttk.Label(replace_window, text="")
        result_label.pack(pady=10)

        def do_replace():
            find_text = find_entry.get()
            replace_text = replace_entry.get()

            if not find_text:
                return

            count = 0
            for page_num in range(len(self.pdf_document)):
                page = self.pdf_document[page_num]
                text_instances = page.search_for(find_text)

                for inst in text_instances:
                    # Add redaction to cover old text
                    page.add_redact_annot(inst, fill=(1, 1, 1))

                    # Add new text as annotation
                    annot = TextAnnotation(
                        page_num=page_num,
                        x=inst.x0,
                        y=inst.y1,
                        text=replace_text,
                        fontsize=self.text_size,
                        color=self.text_color_normalized
                    )
                    self.text_annotations.append(annot)
                    count += 1

                # Apply redactions
                page.apply_redactions()

            if count > 0:
                result_label.config(text=f"Replaced {count} instances")
                self.display_current_page()
            else:
                result_label.config(text="Text not found")

        ttk.Button(replace_window, text="Replace All", command=do_replace).pack(pady=5)

    def save_pdf(self):
        """Save PDF with annotations"""
        if not self.pdf_document:
            messagebox.showwarning("Warning", "No PDF loaded")
            return

        if not self.pdf_path:
            self.save_pdf_as()
            return

        try:
            self.apply_annotations_to_pdf()
            self.pdf_document.save(self.pdf_path, incremental=True, encryption=fitz.PDF_ENCRYPT_KEEP)
            self.update_status("PDF saved")
            messagebox.showinfo("Success", "PDF saved successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save PDF:\n{str(e)}")

    def save_pdf_as(self):
        """Save PDF with annotations to new file"""
        if not self.pdf_document:
            messagebox.showwarning("Warning", "No PDF loaded")
            return

        output_path = filedialog.asksaveasfilename(
            title="Save PDF As",
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")]
        )

        if not output_path:
            return

        try:
            self.apply_annotations_to_pdf()
            self.pdf_document.save(output_path)
            self.pdf_path = output_path
            self.update_status(f"Saved as: {os.path.basename(output_path)}")
            messagebox.showinfo("Success", f"PDF saved to:\n{output_path}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save PDF:\n{str(e)}")

    def apply_annotations_to_pdf(self):
        """Apply text annotations to the actual PDF"""
        for annot in self.text_annotations:
            page = self.pdf_document[annot.page_num]

            # Insert text at position
            page.insert_text(
                (annot.x, annot.y),
                annot.text,
                fontsize=annot.fontsize,
                color=annot.color,
                fontname=annot.fontname
            )


def main():
    """Main application entry point"""
    root = tk.Tk()
    app = InteractivePDFEditor(root)
    root.mainloop()


if __name__ == "__main__":
    main()
