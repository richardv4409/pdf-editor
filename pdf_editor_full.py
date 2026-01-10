"""
Enhanced Interactive PDF Editor with Full Signature Management
Includes: Electronic signatures with save/load, initials, shapes, highlighting, stamps, undo/redo
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser, simpledialog
from tkinter.scrolledtext import ScrolledText
import fitz  # PyMuPDF
from PIL import Image, ImageTk, ImageDraw, ImageFont
import io
from typing import Optional, List, Tuple, Dict
import os
from datetime import datetime
import base64
import json


class SignatureStorage:
    """Manages signature storage and retrieval"""

    def __init__(self, storage_file="signatures.json"):
        self.storage_file = storage_file
        self.signatures: Dict[str, dict] = {}
        self.load_signatures()

    def load_signatures(self):
        """Load signatures from file"""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r') as f:
                    data = json.load(f)
                    self.signatures = data
            except:
                self.signatures = {}

    def save_signatures(self):
        """Save signatures to file"""
        try:
            with open(self.storage_file, 'w') as f:
                json.dump(self.signatures, f, indent=2)
        except Exception as e:
            print(f"Error saving signatures: {e}")

    def add_signature(self, name: str, signature_data: bytes, sig_type: str = "signature"):
        """Add a signature to storage"""
        # Convert bytes to base64 for JSON storage
        b64_data = base64.b64encode(signature_data).decode('utf-8')

        self.signatures[name] = {
            'data': b64_data,
            'type': sig_type,
            'created': datetime.now().isoformat()
        }
        self.save_signatures()

    def get_signature(self, name: str) -> Optional[bytes]:
        """Get signature data by name"""
        if name in self.signatures:
            b64_data = self.signatures[name]['data']
            return base64.b64decode(b64_data)
        return None

    def delete_signature(self, name: str):
        """Delete a signature"""
        if name in self.signatures:
            del self.signatures[name]
            self.save_signatures()

    def get_all_names(self) -> List[str]:
        """Get all signature names"""
        return list(self.signatures.keys())

    def get_signature_info(self, name: str) -> Optional[dict]:
        """Get signature info"""
        return self.signatures.get(name)


class Annotation:
    """Base class for all annotations"""
    def __init__(self, page_num: int):
        self.page_num = page_num
        self.selected = False

    def draw(self, draw, zoom_level):
        """Draw the annotation on PIL ImageDraw"""
        pass

    def contains_point(self, x: float, y: float, zoom: float) -> bool:
        """Check if point is within annotation"""
        return False


class TextAnnotation(Annotation):
    """Text annotation"""
    def __init__(self, page_num: int, x: float, y: float, text: str,
                 fontsize: int = 12, color: Tuple[float, float, float] = (0, 0, 0),
                 fontname: str = "helv"):
        super().__init__(page_num)
        self.x = x
        self.y = y
        self.text = text
        self.fontsize = fontsize
        self.color = color
        self.fontname = fontname

    def draw(self, draw, zoom_level):
        x = self.x * zoom_level
        y = self.y * zoom_level
        size = int(self.fontsize * zoom_level)

        try:
            font = ImageFont.truetype("arial.ttf", size)
        except:
            font = ImageFont.load_default()

        color = tuple(int(c * 255) for c in self.color)
        draw.text((x, y - size), self.text, fill=color, font=font)

        if self.selected:
            bbox = draw.textbbox((x, y - size), self.text, font=font)
            draw.rectangle(bbox, outline="blue", width=2)

    def contains_point(self, x: float, y: float, zoom: float) -> bool:
        annot_x = self.x * zoom
        annot_y = self.y * zoom
        text_width = len(self.text) * self.fontsize * zoom * 0.6
        text_height = self.fontsize * zoom * 1.2

        return (annot_x <= x <= annot_x + text_width and
                annot_y - text_height <= y <= annot_y)


class SignatureAnnotation(Annotation):
    """Electronic signature annotation"""
    def __init__(self, page_num: int, x: float, y: float,
                 signature_data: bytes, width: float = 150, height: float = 50):
        super().__init__(page_num)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.signature_data = signature_data
        self.image = None
        self._load_image()

    def _load_image(self):
        """Load signature image from bytes"""
        self.image = Image.open(io.BytesIO(self.signature_data))

    def draw(self, draw, zoom_level):
        x = int(self.x * zoom_level)
        y = int(self.y * zoom_level)
        w = int(self.width * zoom_level)
        h = int(self.height * zoom_level)

        sig_resized = self.image.resize((w, h), Image.Resampling.LANCZOS)
        img = draw._image
        img.paste(sig_resized, (x, y), sig_resized if sig_resized.mode == 'RGBA' else None)

        if self.selected:
            draw.rectangle([x, y, x + w, y + h], outline="blue", width=2)

    def contains_point(self, x: float, y: float, zoom: float) -> bool:
        sx = self.x * zoom
        sy = self.y * zoom
        sw = self.width * zoom
        sh = self.height * zoom
        return sx <= x <= sx + sw and sy <= y <= sy + sh


class ShapeAnnotation(Annotation):
    """Shape annotation (rectangle, circle, line, arrow)"""
    def __init__(self, page_num: int, x1: float, y1: float, x2: float, y2: float,
                 shape_type: str = "rectangle", color: Tuple[int, int, int] = (255, 0, 0),
                 thickness: int = 2, fill: bool = False):
        super().__init__(page_num)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.shape_type = shape_type
        self.color = color
        self.thickness = thickness
        self.fill = fill

    def draw(self, draw, zoom_level):
        x1 = int(self.x1 * zoom_level)
        y1 = int(self.y1 * zoom_level)
        x2 = int(self.x2 * zoom_level)
        y2 = int(self.y2 * zoom_level)
        thickness = max(1, int(self.thickness * zoom_level))

        if self.shape_type == "rectangle":
            if self.fill:
                draw.rectangle([x1, y1, x2, y2], fill=self.color, outline=self.color, width=thickness)
            else:
                draw.rectangle([x1, y1, x2, y2], outline=self.color, width=thickness)

        elif self.shape_type == "circle":
            if self.fill:
                draw.ellipse([x1, y1, x2, y2], fill=self.color, outline=self.color, width=thickness)
            else:
                draw.ellipse([x1, y1, x2, y2], outline=self.color, width=thickness)

        elif self.shape_type == "line":
            draw.line([x1, y1, x2, y2], fill=self.color, width=thickness)

        elif self.shape_type == "arrow":
            draw.line([x1, y1, x2, y2], fill=self.color, width=thickness)
            import math
            angle = math.atan2(y2 - y1, x2 - x1)
            arrow_size = 10 * zoom_level
            left_angle = angle + 2.7
            right_angle = angle - 2.7
            left_x = x2 - arrow_size * math.cos(left_angle)
            left_y = y2 - arrow_size * math.sin(left_angle)
            right_x = x2 - arrow_size * math.cos(right_angle)
            right_y = y2 - arrow_size * math.sin(right_angle)
            draw.polygon([x2, y2, left_x, left_y, right_x, right_y], fill=self.color)

        if self.selected:
            draw.rectangle([min(x1, x2) - 2, min(y1, y2) - 2,
                          max(x1, x2) + 2, max(y1, y2) + 2],
                          outline="blue", width=2)

    def contains_point(self, x: float, y: float, zoom: float) -> bool:
        sx1, sy1 = self.x1 * zoom, self.y1 * zoom
        sx2, sy2 = self.x2 * zoom, self.y2 * zoom
        margin = 5
        return (min(sx1, sx2) - margin <= x <= max(sx1, sx2) + margin and
                min(sy1, sy2) - margin <= y <= max(sy1, sy2) + margin)


class HighlightAnnotation(Annotation):
    """Highlight annotation"""
    def __init__(self, page_num: int, x1: float, y1: float, x2: float, y2: float,
                 color: Tuple[int, int, int] = (255, 255, 0)):
        super().__init__(page_num)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color = color

    def draw(self, draw, zoom_level):
        x1 = int(self.x1 * zoom_level)
        y1 = int(self.y1 * zoom_level)
        x2 = int(self.x2 * zoom_level)
        y2 = int(self.y2 * zoom_level)

        overlay = Image.new('RGBA', draw._image.size, (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        color_with_alpha = (*self.color, 100)
        overlay_draw.rectangle([x1, y1, x2, y2], fill=color_with_alpha)

        draw._image.paste(Image.alpha_composite(draw._image.convert('RGBA'), overlay).convert('RGB'))

        if self.selected:
            draw.rectangle([x1, y1, x2, y2], outline="blue", width=2)

    def contains_point(self, x: float, y: float, zoom: float) -> bool:
        sx1, sy1 = self.x1 * zoom, self.y1 * zoom
        sx2, sy2 = self.x2 * zoom, self.y2 * zoom
        return (min(sx1, sx2) <= x <= max(sx1, sx2) and
                min(sy1, sy2) <= y <= max(sy1, sy2))


class StampAnnotation(Annotation):
    """Stamp annotation (Approved, Confidential, etc.)"""
    def __init__(self, page_num: int, x: float, y: float, stamp_type: str = "approved"):
        super().__init__(page_num)
        self.x = x
        self.y = y
        self.stamp_type = stamp_type
        self.width = 100
        self.height = 40

    def draw(self, draw, zoom_level):
        x = int(self.x * zoom_level)
        y = int(self.y * zoom_level)
        w = int(self.width * zoom_level)
        h = int(self.height * zoom_level)

        stamps = {
            "approved": ("APPROVED", (0, 150, 0)),
            "rejected": ("REJECTED", (200, 0, 0)),
            "confidential": ("CONFIDENTIAL", (200, 0, 0)),
            "draft": ("DRAFT", (128, 128, 128)),
            "final": ("FINAL", (0, 0, 200)),
            "reviewed": ("REVIEWED", (150, 0, 150)),
        }

        text, color = stamps.get(self.stamp_type, ("APPROVED", (0, 150, 0)))

        draw.rounded_rectangle([x, y, x + w, y + h], radius=5,
                              outline=color, width=3)

        try:
            font_size = int(16 * zoom_level)
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()

        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        text_x = x + (w - text_w) // 2
        text_y = y + (h - text_h) // 2

        draw.text((text_x, text_y), text, fill=color, font=font)

        date_text = datetime.now().strftime("%Y-%m-%d")
        try:
            date_font = ImageFont.truetype("arial.ttf", int(10 * zoom_level))
        except:
            date_font = ImageFont.load_default()

        bbox = draw.textbbox((0, 0), date_text, font=date_font)
        date_w = bbox[2] - bbox[0]
        date_x = x + (w - date_w) // 2
        date_y = y + h + 2
        draw.text((date_x, date_y), date_text, fill=color, font=date_font)

        if self.selected:
            draw.rectangle([x - 2, y - 2, x + w + 2, y + h + 15],
                          outline="blue", width=2)

    def contains_point(self, x: float, y: float, zoom: float) -> bool:
        sx = self.x * zoom
        sy = self.y * zoom
        sw = self.width * zoom
        sh = self.height * zoom + 15
        return sx <= x <= sx + sw and sy <= y <= sy + sh


class SignaturePad(tk.Toplevel):
    """Drawing pad for creating signatures"""

    def __init__(self, parent, callback, title="Draw Signature", allow_save=True, storage=None):
        super().__init__(parent)
        self.callback = callback
        self.title(title)
        self.geometry("550x350")
        self.resizable(False, False)
        self.allow_save = allow_save
        self.storage = storage

        # Drawing data
        self.image = Image.new('RGBA', (480, 200), (255, 255, 255, 0))
        self.draw = ImageDraw.Draw(self.image)
        self.last_x = None
        self.last_y = None

        # Canvas
        canvas_frame = ttk.Frame(self, padding="10")
        canvas_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(canvas_frame, text="Draw your signature below:",
                 font=('Arial', 10)).pack()

        self.canvas = tk.Canvas(canvas_frame, width=480, height=200,
                               bg='white', relief=tk.SUNKEN, bd=2)
        self.canvas.pack(pady=5)

        # Bindings
        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)

        # Buttons
        button_frame = ttk.Frame(self, padding="10")
        button_frame.pack(fill=tk.X)

        ttk.Button(button_frame, text="Clear", command=self.clear).pack(side=tk.LEFT, padx=5)

        if allow_save and storage:
            ttk.Button(button_frame, text="Save for Later",
                      command=self.save_signature).pack(side=tk.LEFT, padx=5)

        ttk.Button(button_frame, text="Cancel", command=self.cancel).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Use This Signature",
                  command=self.done).pack(side=tk.RIGHT, padx=5)

    def paint(self, event):
        x, y = event.x, event.y
        if self.last_x and self.last_y:
            self.canvas.create_line(self.last_x, self.last_y, x, y,
                                   width=2, fill='black', capstyle=tk.ROUND, smooth=True)
            self.draw.line([self.last_x, self.last_y, x, y],
                          fill=(0, 0, 0, 255), width=3)
        self.last_x = x
        self.last_y = y

    def reset(self, event):
        self.last_x = None
        self.last_y = None

    def clear(self):
        self.canvas.delete("all")
        self.image = Image.new('RGBA', (480, 200), (255, 255, 255, 0))
        self.draw = ImageDraw.Draw(self.image)

    def save_signature(self):
        """Save signature to storage"""
        name = simpledialog.askstring("Save Signature",
                                     "Enter a name for this signature:",
                                     parent=self)
        if name:
            buffer = io.BytesIO()
            self.image.save(buffer, format='PNG')
            sig_data = buffer.getvalue()

            self.storage.add_signature(name, sig_data, "signature")
            messagebox.showinfo("Saved", f"Signature '{name}' saved successfully!")

    def done(self):
        buffer = io.BytesIO()
        self.image.save(buffer, format='PNG')
        sig_data = buffer.getvalue()

        if self.callback:
            self.callback(sig_data)
        self.destroy()

    def cancel(self):
        self.destroy()


class SignatureManagerDialog(tk.Toplevel):
    """Dialog to manage saved signatures"""

    def __init__(self, parent, storage: SignatureStorage, callback=None):
        super().__init__(parent)
        self.storage = storage
        self.callback = callback
        self.title("Signature Manager")
        self.geometry("600x400")

        # Top label
        ttk.Label(self, text="Saved Signatures",
                 font=('Arial', 12, 'bold')).pack(pady=10)

        # Main container
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Left: List of signatures
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        ttk.Label(list_frame, text="Select a signature:").pack(anchor=tk.W)

        # Listbox with scrollbar
        list_scroll_frame = ttk.Frame(list_frame)
        list_scroll_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        scrollbar = ttk.Scrollbar(list_scroll_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.sig_listbox = tk.Listbox(list_scroll_frame, yscrollcommand=scrollbar.set)
        self.sig_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.sig_listbox.yview)

        self.sig_listbox.bind('<<ListboxSelect>>', self.on_select)

        # Right: Preview
        preview_frame = ttk.LabelFrame(main_frame, text="Preview", padding="10")
        preview_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))

        self.preview_canvas = tk.Canvas(preview_frame, width=250, height=150,
                                       bg='white', relief=tk.SUNKEN, bd=1)
        self.preview_canvas.pack()

        self.info_label = ttk.Label(preview_frame, text="", justify=tk.LEFT)
        self.info_label.pack(pady=10)

        # Buttons
        button_frame = ttk.Frame(self, padding="10")
        button_frame.pack(fill=tk.X)

        ttk.Button(button_frame, text="Use Selected",
                  command=self.use_signature).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete Selected",
                  command=self.delete_signature).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Close",
                  command=self.destroy).pack(side=tk.RIGHT, padx=5)

        # Load signatures
        self.refresh_list()

    def refresh_list(self):
        """Refresh the signature list"""
        self.sig_listbox.delete(0, tk.END)
        for name in self.storage.get_all_names():
            self.sig_listbox.insert(tk.END, name)

    def on_select(self, event):
        """Handle signature selection"""
        selection = self.sig_listbox.curselection()
        if not selection:
            return

        name = self.sig_listbox.get(selection[0])
        sig_data = self.storage.get_signature(name)
        info = self.storage.get_signature_info(name)

        if sig_data:
            # Show preview
            self.preview_canvas.delete("all")
            img = Image.open(io.BytesIO(sig_data))
            # Resize to fit
            img.thumbnail((240, 140), Image.Resampling.LANCZOS)
            self.preview_image = ImageTk.PhotoImage(img)
            self.preview_canvas.create_image(125, 75, image=self.preview_image)

            # Show info
            if info:
                created = info.get('created', 'Unknown')
                if 'T' in created:
                    created = created.split('T')[0]
                self.info_label.config(text=f"Created: {created}\nType: {info.get('type', 'signature')}")

    def use_signature(self):
        """Use the selected signature"""
        selection = self.sig_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a signature first")
            return

        name = self.sig_listbox.get(selection[0])
        sig_data = self.storage.get_signature(name)

        if sig_data and self.callback:
            self.callback(sig_data)
            self.destroy()

    def delete_signature(self):
        """Delete the selected signature"""
        selection = self.sig_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a signature first")
            return

        name = self.sig_listbox.get(selection[0])

        if messagebox.askyesno("Confirm Delete",
                              f"Are you sure you want to delete '{name}'?"):
            self.storage.delete_signature(name)
            self.refresh_list()
            self.preview_canvas.delete("all")
            self.info_label.config(text="")
            messagebox.showinfo("Deleted", f"Signature '{name}' deleted")


class EnhancedPDFEditor:
    """Enhanced PDF Editor with full signature management"""

    def __init__(self, root):
        self.root = root
        self.root.title("PDF Editor Pro - With Signature Management")
        self.root.geometry("1400x900")

        # Initialize signature storage
        self.signature_storage = SignatureStorage()

        # PDF state
        self.pdf_document: Optional[fitz.Document] = None
        self.current_page_num: int = 0
        self.total_pages: int = 0
        self.pdf_path: Optional[str] = None

        # Display state
        self.zoom_level: float = 1.0
        self.current_pixmap = None
        self.current_photo = None

        # Annotations
        self.annotations: List[Annotation] = []
        self.selected_annotation: Optional[Annotation] = None

        # Undo/Redo stacks
        self.undo_stack: List = []
        self.redo_stack: List = []

        # Drawing state
        self.is_drawing: bool = False
        self.is_dragging: bool = False
        self.drag_start_x: int = 0
        self.drag_start_y: int = 0
        self.draw_start_x: int = 0
        self.draw_start_y: int = 0

        # Tool settings
        self.current_tool: str = "select"
        self.text_font: str = "Helvetica"
        self.text_size: int = 12
        self.text_color: Tuple[int, int, int] = (0, 0, 0)
        self.text_color_normalized: Tuple[float, float, float] = (0, 0, 0)
        self.shape_color: Tuple[int, int, int] = (255, 0, 0)
        self.shape_thickness: int = 2
        self.shape_fill: bool = False
        self.highlight_color: Tuple[int, int, int] = (255, 255, 0)
        self.stamp_type: str = "approved"

        # Setup UI
        self.setup_ui()

    def setup_ui(self):
        """Setup the user interface"""

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
        edit_menu.add_command(label="Undo", command=self.undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label="Redo", command=self.redo, accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="Delete Selected", command=self.delete_selected, accelerator="Del")

        # Signature menu
        sig_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Signatures", menu=sig_menu)
        sig_menu.add_command(label="Manage Signatures", command=self.manage_signatures)
        sig_menu.add_command(label="Use Saved Signature", command=self.use_saved_signature)

        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Zoom In", command=self.zoom_in, accelerator="Ctrl++")
        view_menu.add_command(label="Zoom Out", command=self.zoom_out, accelerator="Ctrl+-")
        view_menu.add_command(label="Reset Zoom", command=self.reset_zoom, accelerator="Ctrl+0")

        # Keyboard bindings
        self.root.bind('<Control-o>', lambda e: self.open_pdf())
        self.root.bind('<Control-s>', lambda e: self.save_pdf())
        self.root.bind('<Control-z>', lambda e: self.undo())
        self.root.bind('<Control-y>', lambda e: self.redo())
        self.root.bind('<Delete>', lambda e: self.delete_selected())
        self.root.bind('<Control-plus>', lambda e: self.zoom_in())
        self.root.bind('<Control-minus>', lambda e: self.zoom_out())
        self.root.bind('<Control-0>', lambda e: self.reset_zoom())

        # Main container
        main_container = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_container.pack(fill=tk.BOTH, expand=True)

        # Left panel - Tools
        left_panel = ttk.Frame(main_container, width=280)
        main_container.add(left_panel, weight=0)

        # Create scrollable left panel
        canvas_left = tk.Canvas(left_panel, width=280)
        scrollbar_left = ttk.Scrollbar(left_panel, orient="vertical", command=canvas_left.yview)
        scrollable_frame = ttk.Frame(canvas_left)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas_left.configure(scrollregion=canvas_left.bbox("all"))
        )

        canvas_left.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas_left.configure(yscrollcommand=scrollbar_left.set)

        canvas_left.pack(side="left", fill="both", expand=True)
        scrollbar_left.pack(side="right", fill="y")

        # Tools section
        tools_frame = ttk.LabelFrame(scrollable_frame, text="Tools", padding="10")
        tools_frame.pack(fill=tk.X, padx=5, pady=5)

        self.tool_var = tk.StringVar(value="select")

        tools = [
            ("Select/Move", "select"),
            ("Add Text", "add_text"),
            ("Draw Signature", "signature"),
            ("Add Initials", "initials"),
            ("Rectangle", "rectangle"),
            ("Circle", "circle"),
            ("Line", "line"),
            ("Arrow", "arrow"),
            ("Highlight", "highlight"),
            ("Stamp", "stamp"),
        ]

        for text, value in tools:
            ttk.Radiobutton(tools_frame, text=text, variable=self.tool_var,
                          value=value, command=self.change_tool).pack(anchor=tk.W, pady=2)

        # Text properties
        text_props_frame = ttk.LabelFrame(scrollable_frame, text="Text Properties", padding="10")
        text_props_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(text_props_frame, text="Font:").pack(anchor=tk.W)
        self.font_combo = ttk.Combobox(text_props_frame, values=["Helvetica", "Arial", "Times"],
                                      width=18, state='readonly')
        self.font_combo.set("Helvetica")
        self.font_combo.pack(fill=tk.X, pady=2)
        self.font_combo.bind('<<ComboboxSelected>>', lambda e: setattr(self, 'text_font', self.font_combo.get()))

        ttk.Label(text_props_frame, text="Size:").pack(anchor=tk.W, pady=(10, 0))
        self.size_var = tk.IntVar(value=12)
        size_spinbox = ttk.Spinbox(text_props_frame, from_=6, to=72,
                                  textvariable=self.size_var, width=18)
        size_spinbox.pack(fill=tk.X, pady=2)
        self.size_var.trace('w', lambda *args: setattr(self, 'text_size', self.size_var.get()))

        ttk.Label(text_props_frame, text="Color:").pack(anchor=tk.W, pady=(10, 0))
        color_frame = ttk.Frame(text_props_frame)
        color_frame.pack(fill=tk.X, pady=2)
        self.color_display = tk.Canvas(color_frame, width=30, height=20,
                                      bg="black", relief=tk.SUNKEN, bd=1)
        self.color_display.pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(color_frame, text="Choose", command=self.choose_text_color).pack(side=tk.LEFT)

        # Shape properties
        shape_props_frame = ttk.LabelFrame(scrollable_frame, text="Shape Properties", padding="10")
        shape_props_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(shape_props_frame, text="Color:").pack(anchor=tk.W)
        shape_color_frame = ttk.Frame(shape_props_frame)
        shape_color_frame.pack(fill=tk.X, pady=2)
        self.shape_color_display = tk.Canvas(shape_color_frame, width=30, height=20,
                                            bg="red", relief=tk.SUNKEN, bd=1)
        self.shape_color_display.pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(shape_color_frame, text="Choose", command=self.choose_shape_color).pack(side=tk.LEFT)

        ttk.Label(shape_props_frame, text="Thickness:").pack(anchor=tk.W, pady=(10, 0))
        self.thickness_var = tk.IntVar(value=2)
        ttk.Spinbox(shape_props_frame, from_=1, to=10,
                   textvariable=self.thickness_var, width=18).pack(fill=tk.X, pady=2)
        self.thickness_var.trace('w', lambda *args: setattr(self, 'shape_thickness', self.thickness_var.get()))

        self.fill_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(shape_props_frame, text="Fill shape",
                       variable=self.fill_var).pack(anchor=tk.W, pady=5)
        self.fill_var.trace('w', lambda *args: setattr(self, 'shape_fill', self.fill_var.get()))

        # Highlight properties
        highlight_frame = ttk.LabelFrame(scrollable_frame, text="Highlight Color", padding="10")
        highlight_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(highlight_frame, text="Used by Highlight tool",
                 font=('Arial', 8, 'italic')).pack(anchor=tk.W, pady=(0, 5))

        hl_color_frame = ttk.Frame(highlight_frame)
        hl_color_frame.pack(fill=tk.X)
        self.highlight_color_display = tk.Canvas(hl_color_frame, width=30, height=20,
                                                bg="yellow", relief=tk.SUNKEN, bd=1)
        self.highlight_color_display.pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(hl_color_frame, text="Choose", command=self.choose_highlight_color).pack(side=tk.LEFT)

        # Stamp properties
        stamp_frame = ttk.LabelFrame(scrollable_frame, text="Stamp Type", padding="10")
        stamp_frame.pack(fill=tk.X, padx=5, pady=5)

        self.stamp_var = tk.StringVar(value="approved")
        for stamp in ["approved", "rejected", "confidential", "draft", "final", "reviewed"]:
            ttk.Radiobutton(stamp_frame, text=stamp.title(), variable=self.stamp_var,
                          value=stamp).pack(anchor=tk.W, pady=1)
        self.stamp_var.trace('w', lambda *args: setattr(self, 'stamp_type', self.stamp_var.get()))

        # Signature management - ENHANCED
        sig_frame = ttk.LabelFrame(scrollable_frame, text="Signature Quick Access", padding="10")
        sig_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(sig_frame, text="📝 Manage Signatures",
                  command=self.manage_signatures).pack(fill=tk.X, pady=2)
        ttk.Button(sig_frame, text="✍️ Use Saved Signature",
                  command=self.use_saved_signature).pack(fill=tk.X, pady=2)

        # Show count
        sig_count = len(self.signature_storage.get_all_names())
        self.sig_count_label = ttk.Label(sig_frame,
                                         text=f"{sig_count} saved signature(s)",
                                         font=('Arial', 8, 'italic'))
        self.sig_count_label.pack(pady=5)

        # Navigation
        nav_frame = ttk.LabelFrame(scrollable_frame, text="Navigation", padding="10")
        nav_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(nav_frame, text="Previous Page", command=self.previous_page).pack(fill=tk.X, pady=2)
        self.page_label = ttk.Label(nav_frame, text="0 / 0")
        self.page_label.pack(pady=5)
        ttk.Button(nav_frame, text="Next Page", command=self.next_page).pack(fill=tk.X, pady=2)

        # Zoom
        zoom_frame = ttk.LabelFrame(scrollable_frame, text="Zoom", padding="10")
        zoom_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(zoom_frame, text="Zoom In (+)", command=self.zoom_in).pack(fill=tk.X, pady=2)
        ttk.Button(zoom_frame, text="Zoom Out (-)", command=self.zoom_out).pack(fill=tk.X, pady=2)
        ttk.Button(zoom_frame, text="Reset (100%)", command=self.reset_zoom).pack(fill=tk.X, pady=2)
        self.zoom_label = ttk.Label(zoom_frame, text="100%")
        self.zoom_label.pack(pady=5)

        # Center panel - PDF viewer
        center_panel = ttk.Frame(main_container)
        main_container.add(center_panel, weight=1)

        # Canvas
        canvas_frame = ttk.Frame(center_panel)
        canvas_frame.pack(fill=tk.BOTH, expand=True)

        h_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        v_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

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

        # Status bar
        self.status_label = ttk.Label(self.root, text="Ready | Tip: Use 'Manage Signatures' to save your signatures for quick reuse",
                                     relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

    def update_status(self, message: str):
        """Update status bar"""
        self.status_label.config(text=message)
        self.root.update_idletasks()

    def update_signature_count(self):
        """Update signature count display"""
        count = len(self.signature_storage.get_all_names())
        self.sig_count_label.config(text=f"{count} saved signature(s)")

    def change_tool(self):
        """Handle tool change"""
        self.current_tool = self.tool_var.get()
        cursors = {
            "select": "arrow",
            "add_text": "crosshair",
            "signature": "crosshair",
            "initials": "crosshair",
            "rectangle": "crosshair",
            "circle": "crosshair",
            "line": "crosshair",
            "arrow": "crosshair",
            "highlight": "crosshair",
            "stamp": "crosshair",
        }
        self.canvas.config(cursor=cursors.get(self.current_tool, "arrow"))
        self.update_status(f"Tool: {self.current_tool.replace('_', ' ').title()}")

    def choose_text_color(self):
        """Choose text color"""
        color = colorchooser.askcolor(
            color=f"#{self.text_color[0]:02x}{self.text_color[1]:02x}{self.text_color[2]:02x}"
        )
        if color[0]:
            self.text_color = tuple(int(c) for c in color[0])
            self.text_color_normalized = tuple(c / 255.0 for c in self.text_color)
            self.color_display.config(bg=color[1])

    def choose_shape_color(self):
        """Choose shape color"""
        color = colorchooser.askcolor(
            color=f"#{self.shape_color[0]:02x}{self.shape_color[1]:02x}{self.shape_color[2]:02x}"
        )
        if color[0]:
            self.shape_color = tuple(int(c) for c in color[0])
            self.shape_color_display.config(bg=color[1])

    def choose_highlight_color(self):
        """Choose highlight color"""
        color = colorchooser.askcolor(
            color=f"#{self.highlight_color[0]:02x}{self.highlight_color[1]:02x}{self.highlight_color[2]:02x}"
        )
        if color[0]:
            self.highlight_color = tuple(int(c) for c in color[0])
            self.highlight_color_display.config(bg=color[1])

    def manage_signatures(self):
        """Open signature management dialog"""
        def on_signature_selected(sig_data):
            """Called when signature is selected from manager"""
            if hasattr(self, 'pending_signature_callback'):
                self.pending_signature_callback(sig_data)
                del self.pending_signature_callback

        SignatureManagerDialog(self.root, self.signature_storage, on_signature_selected)
        self.update_signature_count()

    def use_saved_signature(self):
        """Quick-apply a saved signature"""
        if not self.pdf_document:
            messagebox.showwarning("No PDF", "Please open a PDF first")
            return

        saved_names = self.signature_storage.get_all_names()
        if not saved_names:
            messagebox.showinfo("No Signatures",
                              "No saved signatures found.\n\n"
                              "Draw a signature and click 'Save for Later' to save it.")
            return

        # Show selection dialog
        def on_selected(sig_data):
            if sig_data:
                # Get click position from user
                self.update_status("Click on PDF where you want to place the signature")
                self.pending_signature_data = sig_data
                self.temp_tool = self.current_tool
                self.tool_var.set("signature")
                self.change_tool()

        SignatureManagerDialog(self.root, self.signature_storage, on_selected)

    def open_pdf(self):
        """Open PDF file"""
        file_path = filedialog.askopenfilename(
            title="Select PDF File",
            filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")]
        )

        if not file_path:
            return

        try:
            if self.pdf_document:
                self.pdf_document.close()

            self.pdf_document = fitz.open(file_path)
            self.pdf_path = file_path
            self.total_pages = len(self.pdf_document)
            self.current_page_num = 0
            self.annotations = []
            self.undo_stack = []
            self.redo_stack = []
            self.zoom_level = 1.0

            self.display_current_page()
            self.update_status(f"Opened: {os.path.basename(file_path)} ({self.total_pages} pages)")
            messagebox.showinfo("Success", f"PDF loaded!\n{self.total_pages} pages")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to open PDF:\n{str(e)}")

    def display_current_page(self):
        """Display current PDF page"""
        if not self.pdf_document:
            return

        try:
            page = self.pdf_document[self.current_page_num]
            mat = fitz.Matrix(self.zoom_level, self.zoom_level)
            pix = page.get_pixmap(matrix=mat, alpha=False)

            img_data = pix.tobytes("ppm")
            img = Image.open(io.BytesIO(img_data))

            # Draw annotations
            img = self.draw_annotations(img)

            self.current_photo = ImageTk.PhotoImage(img)

            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.current_photo)
            self.canvas.config(scrollregion=(0, 0, pix.width, pix.height))

            self.page_label.config(text=f"{self.current_page_num + 1} / {self.total_pages}")
            self.zoom_label.config(text=f"{int(self.zoom_level * 100)}%")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to display page:\n{str(e)}")

    def draw_annotations(self, img):
        """Draw all annotations on image"""
        draw = ImageDraw.Draw(img)

        for annot in self.annotations:
            if annot.page_num == self.current_page_num:
                annot.draw(draw, self.zoom_level)

        return img

    def canvas_to_pdf_coords(self, canvas_x: int, canvas_y: int) -> Tuple[float, float]:
        """Convert canvas to PDF coordinates"""
        scroll_x = self.canvas.canvasx(canvas_x)
        scroll_y = self.canvas.canvasy(canvas_y)
        pdf_x = scroll_x / self.zoom_level
        pdf_y = scroll_y / self.zoom_level
        return pdf_x, pdf_y

    def on_canvas_click(self, event):
        """Handle canvas click"""
        if not self.pdf_document:
            return

        pdf_x, pdf_y = self.canvas_to_pdf_coords(event.x, event.y)
        scroll_x = self.canvas.canvasx(event.x)
        scroll_y = self.canvas.canvasy(event.y)

        # Check if using saved signature
        if hasattr(self, 'pending_signature_data'):
            sig_data = self.pending_signature_data
            sig = SignatureAnnotation(self.current_page_num, pdf_x, pdf_y, sig_data)
            self.add_annotation(sig)
            del self.pending_signature_data
            if hasattr(self, 'temp_tool'):
                self.tool_var.set(self.temp_tool)
                self.change_tool()
                del self.temp_tool
            return

        if self.current_tool == "add_text":
            self.add_text_annotation(event.x_root, event.y_root, pdf_x, pdf_y)

        elif self.current_tool == "signature":
            self.add_signature(pdf_x, pdf_y)

        elif self.current_tool == "initials":
            self.add_initials(pdf_x, pdf_y)

        elif self.current_tool == "stamp":
            self.add_stamp_annotation(pdf_x, pdf_y)

        elif self.current_tool in ["rectangle", "circle", "line", "arrow"]:
            self.is_drawing = True
            self.draw_start_x = pdf_x
            self.draw_start_y = pdf_y

        elif self.current_tool == "highlight":
            self.is_drawing = True
            self.draw_start_x = pdf_x
            self.draw_start_y = pdf_y

        elif self.current_tool == "select":
            clicked = None
            for annot in reversed(self.annotations):
                if annot.page_num == self.current_page_num:
                    if annot.contains_point(scroll_x, scroll_y, self.zoom_level):
                        clicked = annot
                        break

            if clicked:
                self.selected_annotation = clicked
                self.is_dragging = True
                self.drag_start_x = pdf_x
                self.drag_start_y = pdf_y
                for a in self.annotations:
                    a.selected = False
                clicked.selected = True
            else:
                for a in self.annotations:
                    a.selected = False
                self.selected_annotation = None

            self.display_current_page()

    def on_canvas_drag(self, event):
        """Handle canvas drag"""
        if not self.pdf_document:
            return

        pdf_x, pdf_y = self.canvas_to_pdf_coords(event.x, event.y)

        if self.is_dragging and self.selected_annotation:
            dx = pdf_x - self.drag_start_x
            dy = pdf_y - self.drag_start_y

            if isinstance(self.selected_annotation, (TextAnnotation, SignatureAnnotation, StampAnnotation)):
                self.selected_annotation.x += dx
                self.selected_annotation.y += dy
            elif isinstance(self.selected_annotation, (ShapeAnnotation, HighlightAnnotation)):
                self.selected_annotation.x1 += dx
                self.selected_annotation.y1 += dy
                self.selected_annotation.x2 += dx
                self.selected_annotation.y2 += dy

            self.drag_start_x = pdf_x
            self.drag_start_y = pdf_y
            self.display_current_page()

    def on_canvas_release(self, event):
        """Handle mouse release"""
        if not self.pdf_document:
            return

        pdf_x, pdf_y = self.canvas_to_pdf_coords(event.x, event.y)

        if self.is_drawing and self.current_tool in ["rectangle", "circle", "line", "arrow"]:
            shape = ShapeAnnotation(
                self.current_page_num,
                self.draw_start_x, self.draw_start_y,
                pdf_x, pdf_y,
                self.current_tool,
                self.shape_color,
                self.shape_thickness,
                self.shape_fill
            )
            self.add_annotation(shape)

        elif self.is_drawing and self.current_tool == "highlight":
            highlight = HighlightAnnotation(
                self.current_page_num,
                self.draw_start_x, self.draw_start_y,
                pdf_x, pdf_y,
                self.highlight_color
            )
            self.add_annotation(highlight)

        self.is_drawing = False
        self.is_dragging = False

    def on_mouse_wheel(self, event):
        """Handle mouse wheel"""
        if event.state & 0x0004:
            if event.delta > 0:
                self.zoom_in()
            else:
                self.zoom_out()

    def add_text_annotation(self, screen_x, screen_y, pdf_x, pdf_y):
        """Add text annotation with floating entry"""
        from pdf_editor_interactive import FloatingTextEntry

        def callback(text):
            if text and text.strip():
                annot = TextAnnotation(
                    self.current_page_num, pdf_x, pdf_y, text,
                    self.text_size, self.text_color_normalized, self.text_font
                )
                self.add_annotation(annot)

        FloatingTextEntry(self.root, screen_x, screen_y, callback)

    def add_signature(self, pdf_x, pdf_y):
        """Add signature annotation"""
        def callback(sig_data):
            if sig_data:
                sig = SignatureAnnotation(self.current_page_num, pdf_x, pdf_y, sig_data)
                self.add_annotation(sig)

        SignaturePad(self.root, callback, "Draw Your Signature",
                    allow_save=True, storage=self.signature_storage)

    def add_initials(self, pdf_x, pdf_y):
        """Add initials"""
        def callback(sig_data):
            if sig_data:
                sig = SignatureAnnotation(self.current_page_num, pdf_x, pdf_y, sig_data, 60, 30)
                self.add_annotation(sig)

        SignaturePad(self.root, callback, "Draw Your Initials",
                    allow_save=True, storage=self.signature_storage)

    def add_stamp_annotation(self, pdf_x, pdf_y):
        """Add stamp"""
        stamp = StampAnnotation(self.current_page_num, pdf_x, pdf_y, self.stamp_type)
        self.add_annotation(stamp)

    def add_annotation(self, annotation):
        """Add annotation to list and update display"""
        self.annotations.append(annotation)
        self.undo_stack.append(('add', annotation))
        self.redo_stack.clear()
        self.display_current_page()
        self.update_status(f"Added {type(annotation).__name__}")

    def delete_selected(self):
        """Delete selected annotation"""
        if self.selected_annotation and self.selected_annotation in self.annotations:
            self.annotations.remove(self.selected_annotation)
            self.undo_stack.append(('delete', self.selected_annotation))
            self.redo_stack.clear()
            self.selected_annotation = None
            self.display_current_page()
            self.update_status("Deleted annotation")

    def undo(self):
        """Undo last action"""
        if not self.undo_stack:
            return

        action, annotation = self.undo_stack.pop()
        self.redo_stack.append((action, annotation))

        if action == 'add':
            self.annotations.remove(annotation)
        elif action == 'delete':
            self.annotations.append(annotation)

        self.display_current_page()
        self.update_status("Undo")

    def redo(self):
        """Redo last undone action"""
        if not self.redo_stack:
            return

        action, annotation = self.redo_stack.pop()
        self.undo_stack.append((action, annotation))

        if action == 'add':
            self.annotations.append(annotation)
        elif action == 'delete':
            self.annotations.remove(annotation)

        self.display_current_page()
        self.update_status("Redo")

    def zoom_in(self):
        """Zoom in"""
        self.zoom_level = min(5.0, self.zoom_level + 0.25)
        self.display_current_page()

    def zoom_out(self):
        """Zoom out"""
        self.zoom_level = max(0.25, self.zoom_level - 0.25)
        self.display_current_page()

    def reset_zoom(self):
        """Reset zoom"""
        self.zoom_level = 1.0
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

    def save_pdf(self):
        """Save PDF"""
        if not self.pdf_document:
            return

        try:
            self.apply_annotations()
            self.pdf_document.save(self.pdf_path, incremental=True, encryption=fitz.PDF_ENCRYPT_KEEP)
            self.update_status("Saved")
            messagebox.showinfo("Success", "PDF saved!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save:\n{str(e)}")

    def save_pdf_as(self):
        """Save PDF as"""
        if not self.pdf_document:
            return

        output_path = filedialog.asksaveasfilename(
            title="Save PDF As",
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")]
        )

        if output_path:
            try:
                self.apply_annotations()
                self.pdf_document.save(output_path)
                self.pdf_path = output_path
                self.update_status(f"Saved as: {os.path.basename(output_path)}")
                messagebox.showinfo("Success", "PDF saved!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save:\n{str(e)}")

    def apply_annotations(self):
        """Apply annotations to PDF"""
        for annot in self.annotations:
            page = self.pdf_document[annot.page_num]

            if isinstance(annot, TextAnnotation):
                page.insert_text((annot.x, annot.y), annot.text,
                               fontsize=annot.fontsize, color=annot.color)

            elif isinstance(annot, SignatureAnnotation):
                rect = fitz.Rect(annot.x, annot.y,
                               annot.x + annot.width, annot.y + annot.height)
                page.insert_image(rect, stream=annot.signature_data)

            elif isinstance(annot, ShapeAnnotation):
                rect = fitz.Rect(annot.x1, annot.y1, annot.x2, annot.y2)
                color = tuple(c / 255.0 for c in annot.color)

                if annot.shape_type == "rectangle":
                    page.draw_rect(rect, color=color, width=annot.thickness)
                elif annot.shape_type == "circle":
                    page.draw_circle((annot.x1 + annot.x2) / 2, (annot.y1 + annot.y2) / 2,
                                   abs(annot.x2 - annot.x1) / 2, color=color, width=annot.thickness)
                elif annot.shape_type == "line":
                    page.draw_line((annot.x1, annot.y1), (annot.x2, annot.y2),
                                 color=color, width=annot.thickness)

            elif isinstance(annot, HighlightAnnotation):
                rect = fitz.Rect(annot.x1, annot.y1, annot.x2, annot.y2)
                page.add_highlight_annot(rect)

            elif isinstance(annot, StampAnnotation):
                page.insert_text((annot.x, annot.y + 20), annot.stamp_type.upper(),
                               fontsize=16, color=(0, 0.5, 0))


def main():
    """Main entry point"""
    root = tk.Tk()
    app = EnhancedPDFEditor(root)
    root.mainloop()


if __name__ == "__main__":
    main()
