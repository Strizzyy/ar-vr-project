from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
ASSETS_DIR = BASE_DIR / "assets"
STICKERS_DIR = ASSETS_DIR / "stickers"
MANIFEST_PATH = ASSETS_DIR / "stickers.json"
SPRITE_SHEET_PATH = ASSETS_DIR / "sticker_sheet.png"
STATIC_DIR = BASE_DIR.parent / "client" / "dist"

