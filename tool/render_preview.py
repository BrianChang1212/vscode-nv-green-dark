"""Render the bundled product glyphs for local visual inspection."""

from pathlib import Path
from tempfile import TemporaryDirectory

from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont

from build_product_font import NAMES


root = Path(__file__).resolve().parents[1]
source = root / "themes" / "fonts" / "nv-green-symbols.woff"
output = root / "test" / "product-icon-preview.png"
with TemporaryDirectory() as temp:
    font = TTFont(source)
    font.flavor = None
    ttf = Path(temp) / "nv-green-symbols.ttf"
    font.save(ttf)
    glyph_font = ImageFont.truetype(str(ttf), 48)
    label_font = ImageFont.truetype("arial.ttf", 12)
    preview = Image.new("RGB", (640, 540), "#080D0A")
    draw = ImageDraw.Draw(preview)
    for index, name in enumerate(NAMES):
        x, y = (index % 6) * 106, (index // 6) * 132
        draw.rounded_rectangle((x + 6, y + 6, x + 100, y + 124), radius=8, fill="#111B14", outline="#31513A")
        draw.text((x + 30, y + 24), chr(0xE001 + index), font=glyph_font, fill="#89E829")
        draw.text((x + 12, y + 101), name, font=label_font, fill="#A4C3AA")
    preview.save(output)
    print(output)
