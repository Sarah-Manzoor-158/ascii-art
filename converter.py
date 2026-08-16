"""Convert images to ASCII art."""

from PIL import Image

# Dark to light — denser chars read as darker on screen
ASCII_CHARS = "@%#*+=-:. "


def image_to_ascii(image_path: str, width: int = 100) -> str:
    """Load an image and return ASCII art as a string."""
    img = Image.open(image_path).convert("L")

    aspect_ratio = img.height / img.width
    # Terminal chars are ~2x taller than wide
    new_width = max(10, min(width, 200))
    new_height = max(1, int(new_width * aspect_ratio * 0.55))

    img = img.resize((new_width, new_height))

    pixels = img.getdata()
    lines = []

    for i, pixel in enumerate(pixels):
        char = ASCII_CHARS[pixel * len(ASCII_CHARS) // 256]
        lines.append(char)
        if (i + 1) % new_width == 0:
            lines.append("\n")

    return "".join(lines).rstrip()
