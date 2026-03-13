#!/usr/bin/env python3
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent / "static"
ICON = ROOT / "favicon.ico"
APPLE = ROOT / "apple-touch-icon.png"
APPLE_PRE = ROOT / "apple-touch-icon-precomposed.png"

BG = "#0a0a10"
ACCENT = "#e8a83e"
EDGE = "#232637"
FONT = Path("/System/Library/Fonts/Supplemental/Georgia Bold Italic.ttf")


def make_base(size: int = 512) -> Image.Image:
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    pad = size // 16
    radius = size // 5
    draw.rounded_rectangle(
        (pad, pad, size - pad, size - pad),
        radius=radius,
        fill=BG,
        outline=EDGE,
        width=max(2, size // 64),
    )

    font = ImageFont.truetype(str(FONT), size=int(size * 0.63))
    bbox = draw.textbbox((0, 0), "s", font=font)
    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]
    x = (size - width) / 2 - bbox[0]
    y = (size - height) / 2 - bbox[1] - size * 0.035

    draw.text((x, y), "s", font=font, fill=ACCENT)
    return image


def main() -> None:
    base = make_base(512)

    apple = base.resize((180, 180), Image.Resampling.LANCZOS)
    apple.save(APPLE)
    apple.save(APPLE_PRE)

    base.save(
        ICON,
        format="ICO",
        sizes=[(16, 16), (32, 32), (48, 48), (64, 64)],
    )

    print(f"wrote {ICON}")
    print(f"wrote {APPLE}")
    print(f"wrote {APPLE_PRE}")


if __name__ == "__main__":
    main()
