# PDF Page Rotation Guide

## 🔄 New Feature: Page Rotation

You can now rotate individual PDF pages in 90-degree increments!

---

## How to Rotate Pages

### Method 1: Keyboard Shortcuts (Fastest)

**Rotate Clockwise (90° right):**
- Press `Ctrl + ]` (right bracket)

**Rotate Counter-Clockwise (90° left):**
- Press `Ctrl + [` (left bracket)

### Method 2: Menu Bar

1. Click **View** menu
2. Select:
   - "Rotate Clockwise (Ctrl+])" - Rotate 90° right
   - "Rotate Counter-Clockwise (Ctrl+[)" - Rotate 90° left
   - "Reset Rotation" - Return to 0°

### Method 3: Left Panel Buttons

In the left panel, find the **"Page Rotation"** section:

```
┌─────────────────────────────────┐
│  Page Rotation                  │
├─────────────────────────────────┤
│  [↻ Rotate Right (Ctrl+])]      │
│  [↺ Rotate Left (Ctrl+[)]       │
│  [Reset Rotation]               │
│                                 │
│  Current: 90°                   │
└─────────────────────────────────┘
```

---

## Rotation Options

### Available Rotations:
- **0°** - Original orientation (no rotation)
- **90°** - Rotated 90° clockwise (landscape → portrait)
- **180°** - Upside down
- **270°** - Rotated 90° counter-clockwise (portrait → landscape)

### Rotation is Per-Page:
- Each page can have its own rotation
- Page 1 can be 90°, Page 2 can be 0°, etc.
- Rotation is preserved when saving

---

## Common Use Cases

### 1. Fix Scanned Documents
```
Problem: Scanned pages are sideways
Solution: Rotate them to correct orientation
Steps:
  1. Navigate to sideways page
  2. Press Ctrl+] to rotate clockwise
  3. Repeat until correct
  4. Save PDF
```

### 2. Mix Portrait and Landscape
```
Use Case: Report with landscape tables
Steps:
  1. Keep text pages at 0°
  2. Rotate wide tables to 90°
  3. Save with mixed orientations
```

### 3. View Upside-Down Pages
```
Problem: Some pages printed upside down
Solution: Rotate 180°
Steps:
  1. Go to upside-down page
  2. Press Ctrl+] twice (90° + 90° = 180°)
  3. Page now right-side up
```

---

## Workflow Examples

### Example 1: Fix All Sideways Pages
```
1. Open PDF
2. Navigate to first sideways page
3. Press Ctrl+] to rotate 90°
4. Press "Next Page"
5. Repeat for each sideways page
6. Save (Ctrl+S)
```

### Example 2: Rotate Multiple Times
```
Starting at 0°:
  Press Ctrl+] → 90° (quarter turn right)
  Press Ctrl+] → 180° (half turn / upside down)
  Press Ctrl+] → 270° (three-quarter turn)
  Press Ctrl+] → 0° (back to start)
```

### Example 3: Counter-Clockwise Rotation
```
Starting at 0°:
  Press Ctrl+[ → 270° (quarter turn left)
  Press Ctrl+[ → 180° (half turn)
  Press Ctrl+[ → 90° (three-quarter turn left)
  Press Ctrl+[ → 0° (back to start)
```

---

## Features

### Real-Time Preview
- ✅ See rotation immediately in viewer
- ✅ No need to save first
- ✅ Rotate multiple times to find best angle

### Rotation Indicator
- **Display shows current rotation** (e.g., "90°")
- Located in Page Rotation panel
- Updates instantly when rotating

### Permanent Save
- Rotations applied to PDF when saved
- PDF opens with correct rotation in other viewers
- Rotation is not lost

### Undo Support
- Can undo rotations with "Reset Rotation" button
- Or manually rotate back to 0°

---

## Technical Details

### How It Works

**Display Rotation:**
```python
# Applies rotation to display only (temporary)
mat = fitz.Matrix(zoom, zoom).prerotate(rotation)
```

**Permanent Rotation:**
```python
# Applies to actual PDF when saving
page.set_rotation(new_rotation)
```

### Rotation Tracking
- Stored in `page_rotations` dictionary
- Key: page number (0-based)
- Value: rotation angle (0, 90, 180, 270)

### When Saved
- Each page's rotation is applied permanently
- PDF structure is updated
- Other PDF viewers will see the rotation

---

## Tips & Tricks

### Tip 1: Quick Navigation
```
Rotate page → Press "Next Page" → Rotate → Next → ...
Faster than menu each time!
```

### Tip 2: Preview Before Saving
```
Rotate all pages first
Review each page
Save only when all look correct
```

### Tip 3: Keyboard Shortcuts
```
Memorize:
  Ctrl+] = Clockwise (right)
  Ctrl+[ = Counter-clockwise (left)

Much faster than clicking!
```

### Tip 4: Reset If Wrong
```
Rotated too many times?
Click "Reset Rotation" to start over
Or keep rotating to cycle back to 0°
```

### Tip 5: Mix with Annotations
```
1. Rotate page to correct orientation
2. Add signatures/text/stamps
3. Save
Everything saved together!
```

---

## Keyboard Shortcuts Quick Reference

| Action | Shortcut | Alternative |
|--------|----------|-------------|
| Rotate Right | `Ctrl + ]` | View menu or button |
| Rotate Left | `Ctrl + [` | View menu or button |
| Reset Rotation | - | View menu or button |
| Next Page | - | Button only |
| Previous Page | - | Button only |

---

## Troubleshooting

### "Rotation doesn't save"
**Solution:** Make sure you save the PDF (Ctrl+S) after rotating

### "All pages rotated, only wanted one"
**Solution:** Rotation is per-page. Navigate to specific page before rotating.

### "Can't undo rotation"
**Solution:** Use "Reset Rotation" button or rotate 3 more times to complete circle

### "Rotation wrong in other PDF viewer"
**Solution:** Did you save? Rotation only applies to saved PDF.

---

## Comparison: Before vs After

**Before (No Rotation):**
```
- Sideways pages stayed sideways
- Had to rotate monitor
- Or edit in separate tool
- Export and re-import
```

**After (With Rotation):**
```
✓ Fix rotation in-app
✓ One-click rotation
✓ Preview instantly
✓ Save permanently
✓ No external tools
```

---

## Summary

### What You Can Do:
- ✅ Rotate pages 90°, 180°, 270°, or back to 0°
- ✅ Each page can have different rotation
- ✅ See rotation in real-time
- ✅ Save rotation permanently
- ✅ Use keyboard shortcuts for speed

### How to Use:
1. Navigate to page
2. Press `Ctrl+]` or `Ctrl+[`
3. Repeat until correct
4. Save PDF

### Result:
Perfect page orientation for all pages! 🔄

---

**Launch the editor:**
```bash
python pdf_editor_complete.py
```

Open a PDF and try rotating a page with `Ctrl+]`!
