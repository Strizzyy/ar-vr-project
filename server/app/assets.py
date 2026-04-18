import json
from dataclasses import dataclass
from pathlib import Path

from .config import ASSETS_DIR, MANIFEST_PATH, STICKERS_DIR


@dataclass(frozen=True)
class Sticker:
    id: str
    name: str
    file: str
    anchor: str
    scale: float
    y_offset: float

    @property
    def path(self) -> Path:
        return STICKERS_DIR / self.file


def _default_manifest() -> list[dict]:
    return [
        {
            "id": "sunglasses",
            "name": "Cool Shades",
            "file": "sunglasses.png",
            "anchor": "eyes",
            "scale": 0.82,
            "yOffset": 0.38,
        },
        {
            "id": "crown",
            "name": "Crown",
            "file": "crown.png",
            "anchor": "forehead",
            "scale": 0.88,
            "yOffset": -0.18,
        },
        {
            "id": "cat",
            "name": "Cat Face",
            "file": "cat.png",
            "anchor": "face",
            "scale": 1.06,
            "yOffset": 0.08,
        },
        {
            "id": "panda",
            "name": "Panda Mask",
            "file": "panda.png",
            "anchor": "face",
            "scale": 1.08,
            "yOffset": 0.08,
        },
    ]


def ensure_asset_dirs() -> None:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    STICKERS_DIR.mkdir(parents=True, exist_ok=True)


def load_stickers() -> list[Sticker]:
    ensure_asset_dirs()
    if MANIFEST_PATH.exists():
        raw = json.loads(MANIFEST_PATH.read_text())
    else:
        raw = _default_manifest()
    return [
        Sticker(
            id=item["id"],
            name=item["name"],
            file=item["file"],
            anchor=item.get("anchor", "face"),
            scale=float(item.get("scale", 1.0)),
            y_offset=float(item.get("yOffset", 0.0)),
        )
        for item in raw
    ]


def get_sticker(sticker_id: str | None) -> Sticker:
    stickers = load_stickers()
    if not stickers:
        raise FileNotFoundError("No stickers are available. Run server/scripts/download_assets.py.")
    for sticker in stickers:
        if sticker.id == sticker_id:
            return sticker
    return stickers[0]


def serialize_stickers(base_url: str = "") -> list[dict]:
    return [
        {
            "id": sticker.id,
            "name": sticker.name,
            "anchor": sticker.anchor,
            "url": f"{base_url}/api/assets/stickers/{sticker.file}",
        }
        for sticker in load_stickers()
    ]

