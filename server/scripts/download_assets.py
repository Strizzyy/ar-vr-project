import json
from io import BytesIO
from pathlib import Path

import requests
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
ASSETS_DIR = ROOT / "assets"
STICKERS_DIR = ASSETS_DIR / "stickers"
SHEET_PATH = ASSETS_DIR / "sticker_sheet.png"
MANIFEST_PATH = ASSETS_DIR / "stickers.json"

TWEMOJI_BASE = "https://cdnjs.cloudflare.com/ajax/libs/twemoji/14.0.2/72x72"

STICKERS = [
    {
        "id": "sunglasses",
        "name": "Cool Shades",
        "file": "sunglasses.png",
        "url": f"{TWEMOJI_BASE}/1f60e.png",
        "anchor": "eyes",
        "scale": 0.82,
        "yOffset": 0.38,
    },
    {
        "id": "crown",
        "name": "Crown",
        "file": "crown.png",
        "url": f"{TWEMOJI_BASE}/1f451.png",
        "anchor": "forehead",
        "scale": 0.88,
        "yOffset": -0.18,
    },
    {
        "id": "cat",
        "name": "Cat Face",
        "file": "cat.png",
        "url": f"{TWEMOJI_BASE}/1f431.png",
        "anchor": "face",
        "scale": 1.06,
        "yOffset": 0.08,
    },
    {
        "id": "panda",
        "name": "Panda Mask",
        "file": "panda.png",
        "url": f"{TWEMOJI_BASE}/1f43c.png",
        "anchor": "face",
        "scale": 1.08,
        "yOffset": 0.08,
    },
]


def fallback_sticker(sticker_id: str) -> Image.Image:
    image = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    if sticker_id == "sunglasses":
        draw.rounded_rectangle((35, 90, 115, 145), 16, fill=(10, 20, 25, 235))
        draw.rounded_rectangle((140, 90, 220, 145), 16, fill=(10, 20, 25, 235))
        draw.rectangle((110, 112, 145, 123), fill=(10, 20, 25, 235))
    elif sticker_id == "crown":
        draw.polygon([(38, 190), (62, 70), (112, 145), (128, 52), (146, 145), (198, 70), (220, 190)], fill=(255, 204, 56, 245))
        draw.rounded_rectangle((42, 178, 216, 220), 8, fill=(255, 183, 31, 255))
    elif sticker_id == "cat":
        draw.polygon([(55, 88), (88, 28), (116, 95)], fill=(255, 184, 77, 245))
        draw.polygon([(141, 95), (170, 28), (203, 88)], fill=(255, 184, 77, 245))
        draw.ellipse((48, 62, 208, 222), fill=(255, 184, 77, 235))
        draw.ellipse((84, 125, 105, 146), fill=(20, 20, 20, 255))
        draw.ellipse((151, 125, 172, 146), fill=(20, 20, 20, 255))
    else:
        draw.ellipse((38, 44, 218, 224), fill=(245, 245, 245, 240))
        draw.ellipse((40, 42, 92, 100), fill=(20, 20, 20, 245))
        draw.ellipse((164, 42, 216, 100), fill=(20, 20, 20, 245))
        draw.ellipse((83, 112, 119, 148), fill=(20, 20, 20, 245))
        draw.ellipse((137, 112, 173, 148), fill=(20, 20, 20, 245))
    return image


def download_sticker(item: dict) -> Image.Image:
    try:
        response = requests.get(item["url"], timeout=20)
        response.raise_for_status()
        return Image.open(BytesIO(response.content)).convert("RGBA").resize((256, 256))
    except Exception as exc:
        print(f"Using generated fallback for {item['id']}: {exc}")
        return fallback_sticker(item["id"])


def build_sprite_sheet(images: list[Image.Image]) -> list[dict]:
    tile = 256
    sheet = Image.new("RGBA", (tile * len(images), tile), (0, 0, 0, 0))
    frames = []
    for index, image in enumerate(images):
        x = index * tile
        sheet.alpha_composite(image, (x, 0))
        frames.append({"x": x, "y": 0, "width": tile, "height": tile})
    sheet.save(SHEET_PATH)
    return frames


def main() -> None:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    STICKERS_DIR.mkdir(parents=True, exist_ok=True)

    images = []
    manifest = []
    for item in STICKERS:
        image = download_sticker(item)
        image.save(STICKERS_DIR / item["file"])
        images.append(image)
        manifest.append({key: value for key, value in item.items() if key != "url"})

    frames = build_sprite_sheet(images)
    for item, frame in zip(manifest, frames):
        item["sprite"] = frame

    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2))
    print(f"Wrote {len(manifest)} stickers to {STICKERS_DIR}")
    print(f"Wrote sprite sheet to {SHEET_PATH}")


if __name__ == "__main__":
    main()

