"""
Test signature sharpening feature
Creates a sample signature and shows before/after sharpening
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import io

def create_test_signature():
    """Create a sample signature image"""
    # Create image with white background
    img = Image.new('RGB', (300, 100), 'white')
    draw = ImageDraw.Draw(img)

    # Try to use a handwriting-style font, fallback to default
    try:
        font = ImageFont.truetype("segoeui.ttf", 40)
    except:
        font = ImageFont.load_default()

    # Draw signature-like text
    draw.text((20, 30), "John Doe", fill='black', font=font)

    # Add some curves to make it look more like a signature
    draw.line([(20, 75), (50, 65), (80, 75), (110, 70)], fill='black', width=2)

    # Convert to RGBA
    img = img.convert('RGBA')

    return img

def remove_white_background(img):
    """Remove white background"""
    if img.mode != 'RGBA':
        img = img.convert('RGBA')

    pixels = img.load()
    width, height = img.size
    white_threshold = 240

    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            if r >= white_threshold and g >= white_threshold and b >= white_threshold:
                pixels[x, y] = (r, g, b, 0)

    return img

def sharpen_signature(img):
    """Sharpen signature image"""
    if img.mode != 'RGBA':
        img = img.convert('RGBA')

    # Split channels
    r, g, b, a = img.split()
    rgb = Image.merge('RGB', (r, g, b))

    # Apply unsharp mask
    rgb = rgb.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))

    # Enhance contrast
    enhancer = ImageEnhance.Contrast(rgb)
    rgb = enhancer.enhance(1.2)

    # Merge back
    r, g, b = rgb.split()
    sharpened = Image.merge('RGBA', (r, g, b, a))

    return sharpened

def add_blur(img, radius=1):
    """Add slight blur to simulate low-quality scan"""
    if img.mode != 'RGBA':
        img = img.convert('RGBA')

    r, g, b, a = img.split()
    rgb = Image.merge('RGB', (r, g, b))
    rgb = rgb.filter(ImageFilter.GaussianBlur(radius))
    r, g, b = rgb.split()
    return Image.merge('RGBA', (r, g, b, a))

if __name__ == "__main__":
    print("Creating test signature...")

    # Create base signature
    signature = create_test_signature()

    # Remove white background
    signature = remove_white_background(signature)

    # Add slight blur to simulate real-world scanned signature
    blurred_sig = add_blur(signature, radius=1.5)

    # Save original (blurred) version
    blurred_sig.save("signature_before.png")
    print("[OK] Saved: signature_before.png (original - slightly blurred)")

    # Apply sharpening
    sharpened_sig = sharpen_signature(blurred_sig)

    # Save sharpened version
    sharpened_sig.save("signature_after.png")
    print("[OK] Saved: signature_after.png (sharpened)")

    # Create side-by-side comparison
    comparison = Image.new('RGBA', (600, 120), (255, 255, 255, 255))

    # Add text labels
    draw = ImageDraw.Draw(comparison)
    try:
        font = ImageFont.truetype("arial.ttf", 12)
    except:
        font = ImageFont.load_default()

    draw.text((80, 5), "BEFORE (Blurred)", fill='red', font=font)
    draw.text((380, 5), "AFTER (Sharpened)", fill='green', font=font)

    # Paste signatures
    comparison.paste(blurred_sig, (0, 20), blurred_sig)
    comparison.paste(sharpened_sig, (300, 20), sharpened_sig)

    comparison.save("signature_comparison.png")
    print("[OK] Saved: signature_comparison.png (side-by-side)")

    print("\n" + "="*60)
    print("SHARPENING TEST COMPLETE!")
    print("="*60)
    print("\nFiles created:")
    print("  1. signature_before.png    - Original (slightly blurred)")
    print("  2. signature_after.png     - After sharpening")
    print("  3. signature_comparison.png - Side-by-side comparison")
    print("\nOpen 'signature_comparison.png' to see the difference!")
    print("="*60)

    # Calculate and show enhancement metrics
    print("\nSharpening Settings:")
    print("  - UnsharpMask: radius=2, percent=150, threshold=3")
    print("  - Contrast boost: 1.2x (20% increase)")
    print("  - Effect: Sharper edges, better clarity")
