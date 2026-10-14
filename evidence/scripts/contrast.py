"""Appendix A §A.6: the contrast of the diagram text colour on each palette fill.

    python scripts/contrast.py

WCAG 2 contrast ratio, (L1 + 0.05) / (L2 + 0.05), using relative luminance.
"""
FILLS = {"human": "#FFE6DA", "ci": "#D9F4FA", "data": "#ECF7D5", "ops": "#D9F5EC",
         "govern": "#FFF0D6", "gap": "#F1F3F5"}
TEXT = "#14243A"


def lum(hex_colour: str) -> float:
    def ch(c: float) -> float:
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (int(hex_colour[i:i + 2], 16) for i in (1, 3, 5))
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


lowest = None
for name, fill in FILLS.items():
    ratio = (lum(fill) + 0.05) / (lum(TEXT) + 0.05)
    lowest = ratio if lowest is None else min(lowest, ratio)
    print(f"{name:7} {fill} with {TEXT}: {ratio:5.2f}:1")
print(f"lowest {lowest:.2f}:1")
