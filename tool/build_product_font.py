"""Build the original NV Green Dark product icon font with FontTools."""

from pathlib import Path
from math import cos, sin, pi, hypot

from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen


NAMES = [
    "add", "close", "search", "gear", "refresh", "right", "down", "files",
    "extensions", "terminal", "branch", "run", "check", "warning", "info",
    "filter", "ellipsis", "folder", "account", "bell", "debug", "calendar",
    "clock", "eye",
]


class Shape:
    def __init__(self):
        self.pen = TTGlyphPen(None)

    def polygon(self, points):
        self.pen.moveTo(tuple(map(round, points[0])))
        for point in points[1:]:
            self.pen.lineTo(tuple(map(round, point)))
        self.pen.closePath()

    def rect(self, x1, y1, x2, y2):
        self.polygon([(x1, y1), (x2, y1), (x2, y2), (x1, y2)])

    def line(self, x1, y1, x2, y2, width=78):
        length = hypot(x2 - x1, y2 - y1)
        nx, ny = -(y2 - y1) * width / (2 * length), (x2 - x1) * width / (2 * length)
        self.polygon([(x1 + nx, y1 + ny), (x2 + nx, y2 + ny),
                      (x2 - nx, y2 - ny), (x1 - nx, y1 - ny)])

    def circle(self, cx, cy, radius, sides=20):
        self.polygon([(cx + radius * cos(2 * pi * i / sides),
                       cy + radius * sin(2 * pi * i / sides)) for i in range(sides)])

    def ring(self, cx, cy, radius, width=75, start=0, end=20, sides=20):
        for i in range(start, end):
            a, b = 2 * pi * i / sides, 2 * pi * (i + 1) / sides
            self.line(cx + radius * cos(a), cy + radius * sin(a),
                      cx + radius * cos(b), cy + radius * sin(b), width)


def draw(name):
    s = Shape()
    if name == "add":
        s.rect(460, 170, 540, 830); s.rect(170, 460, 830, 540)
    elif name == "close":
        s.line(240, 240, 760, 760, 90); s.line(240, 760, 760, 240, 90)
    elif name == "search":
        s.ring(440, 570, 240); s.line(615, 395, 800, 210, 90)
    elif name == "gear":
        s.ring(500, 500, 190, 115)
        for i in range(8):
            a = 2 * pi * i / 8
            s.line(500 + 245 * cos(a), 500 + 245 * sin(a),
                   500 + 330 * cos(a), 500 + 330 * sin(a), 105)
    elif name == "refresh":
        s.ring(500, 500, 265, 80, 2, 19)
        s.polygon([(720, 650), (840, 680), (755, 815)])
    elif name == "right":
        s.line(360, 220, 640, 500, 90); s.line(640, 500, 360, 780, 90)
    elif name == "down":
        s.line(220, 640, 500, 360, 90); s.line(500, 360, 780, 640, 90)
    elif name == "files":
        for x, y in [(240, 160), (380, 300)]:
            s.line(x, y, x + 370, y, 65); s.line(x, y, x, y + 490, 65)
            s.line(x + 370, y, x + 370, y + 490, 65); s.line(x, y + 490, x + 370, y + 490, 65)
    elif name == "extensions":
        for x, y in [(185, 185), (540, 185), (185, 540), (540, 540)]:
            s.rect(x, y, x + 270, y + 270)
    elif name == "terminal":
        s.line(170, 200, 830, 200); s.line(170, 200, 170, 800)
        s.line(830, 200, 830, 800); s.line(170, 800, 830, 800)
        s.line(270, 625, 430, 500); s.line(430, 500, 270, 375); s.line(505, 375, 720, 375)
    elif name == "branch":
        s.line(300, 230, 300, 690); s.line(300, 500, 700, 500); s.line(700, 500, 700, 680)
        for x, y in [(300, 230), (300, 700), (700, 700)]: s.circle(x, y, 78)
    elif name == "run":
        s.polygon([(310, 170), (820, 500), (310, 830)])
    elif name == "check":
        s.line(190, 500, 420, 280, 92); s.line(420, 280, 820, 740, 92)
    elif name == "warning":
        for a, b in [((500, 840), (120, 175)), ((120, 175), (880, 175)), ((880, 175), (500, 840))]:
            s.line(*a, *b, 70)
        s.rect(465, 380, 535, 645); s.circle(500, 270, 46)
    elif name == "info":
        s.ring(500, 500, 320, 70); s.rect(465, 300, 535, 585); s.circle(500, 700, 48)
    elif name == "filter":
        s.polygon([(150, 800), (850, 800), (580, 500), (580, 260), (420, 180), (420, 500)])
    elif name == "ellipsis":
        for x in [250, 500, 750]: s.circle(x, 500, 72)
    elif name == "folder":
        s.polygon([(130, 230), (870, 230), (870, 690), (520, 690), (430, 780), (130, 780)])
    elif name == "account":
        s.circle(500, 650, 145); s.ring(500, 180, 320, 80, 1, 9)
    elif name == "bell":
        s.ring(500, 470, 230, 78, 0, 10); s.line(230, 260, 770, 260); s.circle(500, 170, 55)
    elif name == "debug":
        s.circle(500, 500, 195)
        for y in [340, 500, 660]:
            s.line(260, y - 60, 135, y - 130, 75); s.line(740, y - 60, 865, y - 130, 75)
    elif name == "calendar":
        for a, b in [((170, 200), (830, 200)), ((170, 200), (170, 760)),
                     ((830, 200), (830, 760)), ((170, 760), (830, 760)), ((170, 590), (830, 590))]:
            s.line(*a, *b, 70)
        s.line(350, 820, 350, 670, 75); s.line(650, 820, 650, 670, 75)
    elif name == "clock":
        s.ring(500, 500, 320, 70); s.line(500, 500, 500, 695, 70); s.line(500, 500, 650, 420, 70)
    elif name == "eye":
        s.polygon([(105, 500), (340, 740), (660, 740), (895, 500), (660, 260), (340, 260)])
        s.circle(500, 500, 155)
    return s.pen.glyph()


def main():
    glyph_order = [".notdef"] + NAMES
    builder = FontBuilder(1000, isTTF=True)
    builder.setupGlyphOrder(glyph_order)
    builder.setupCharacterMap({0xE001 + index: name for index, name in enumerate(NAMES)})
    builder.setupGlyf({".notdef": TTGlyphPen(None).glyph(), **{name: draw(name) for name in NAMES}})
    builder.setupHorizontalMetrics({name: (1000, 0) for name in glyph_order})
    builder.setupHorizontalHeader(ascent=900, descent=-100)
    builder.setupNameTable({"familyName": "NV Green Symbols", "styleName": "Regular",
                            "uniqueFontIdentifier": "NV Green Symbols 0.1.0",
                            "fullName": "NV Green Symbols", "psName": "NVGreenSymbols"})
    builder.setupOS2(sTypoAscender=900, sTypoDescender=-100, usWinAscent=900, usWinDescent=100)
    builder.setupPost()
    builder.setupMaxp()
    builder.font.flavor = "woff"
    output = Path(__file__).resolve().parents[1] / "themes" / "fonts" / "nv-green-symbols.woff"
    output.parent.mkdir(parents=True, exist_ok=True)
    builder.save(output)
    print(output)


if __name__ == "__main__":
    main()
