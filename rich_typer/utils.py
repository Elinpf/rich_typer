from typing import Tuple, Optional

from rich.text import Text


def blend_text(
    message: str,
    blend: Optional[Tuple[Tuple[int, int, int],
                          Tuple[int, int, int]]] = None
) -> Text:
    """Blend text from one color to another."""
    text = Text(message)
    color1, color2 = blend
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    dr = r2 - r1
    dg = g2 - g1
    db = b2 - b1
    size = len(text)
    for index in range(size):
        blend = index / size
        color = f"#{int(r1 + dr * blend):2X}{int(g1 + dg * blend):2X}{int(b1 + db * blend):2X}"
        text.stylize(color, index, index + 1)
    return text
