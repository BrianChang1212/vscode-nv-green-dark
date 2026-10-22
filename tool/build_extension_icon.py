"""Draw the NV Green Dark extension icon as a deterministic PNG."""

from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "extension-icon.png"
SCALE = 4
SIZE = 256


def points(values):
    return [(x * SCALE, y * SCALE) for x, y in values]


def main():
    image = Image.new("RGB", (SIZE * SCALE, SIZE * SCALE), "#08110d")
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((12 * SCALE, 12 * SCALE, 244 * SCALE, 244 * SCALE),
                           radius=42 * SCALE, fill="#101f17", outline="#36593d", width=3 * SCALE)
    draw.rounded_rectangle((26 * SCALE, 26 * SCALE, 230 * SCALE, 230 * SCALE),
                           radius=30 * SCALE, outline="#244a2c", width=2 * SCALE)
    draw.line(points([(60, 182), (60, 76), (109, 182), (109, 76)]),
              fill="#89e829", width=17 * SCALE, joint="curve")
    draw.line(points([(137, 76), (166, 182), (195, 76)]),
              fill="#b6f270", width=17 * SCALE, joint="curve")
    draw.rounded_rectangle((60 * SCALE, 204 * SCALE, 196 * SCALE, 211 * SCALE),
                           radius=3 * SCALE, fill="#4c9b3e")
    draw.ellipse((204 * SCALE, 45 * SCALE, 218 * SCALE, 59 * SCALE), fill="#89e829")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    image.resize((SIZE, SIZE), Image.Resampling.LANCZOS).save(OUTPUT, optimize=True)


if __name__ == "__main__":
    main()
