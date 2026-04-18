# OpenCV AR Face Stickers

Client/server demo for Snapchat-like AR sticker placement on detected faces.

## Project layout

```text
.
├── client/                     # React + Vite camera UI
│   ├── src/
│   │   ├── components/         # Presentational UI pieces
│   │   │   ├── CameraStage.tsx
│   │   │   └── ControlPanel.tsx
│   │   ├── hooks/              # Camera, sticker loading, and AR stream logic
│   │   │   ├── useAugmentedStream.ts
│   │   │   ├── useCamera.ts
│   │   │   └── useStickers.ts
│   │   ├── utils/              # Browser frame capture helpers
│   │   │   └── captureFrame.ts
│   │   ├── api.ts              # API client for the Flask server
│   │   ├── App.tsx             # App composition and top-level state
│   │   ├── main.tsx            # React entrypoint
│   │   ├── styles.css          # UI styles
│   │   └── types.ts            # Shared client-side types
│   ├── package.json
│   └── vite.config.ts
├── server/                     # Flask + OpenCV backend
│   ├── app/
│   │   ├── assets.py           # Sticker manifest loading and lookup
│   │   ├── config.py           # Server paths
│   │   ├── face_detector.py    # OpenCV Haar cascade face detector
│   │   ├── image_io.py         # Base64/data URL image encoding and decoding
│   │   ├── main.py             # Flask app factory and dev entrypoint
│   │   ├── routes.py           # API and asset routes
│   │   └── sticker_overlay.py  # Alpha compositing for face stickers
│   ├── assets/
│   │   └── stickers.json       # Sticker metadata committed to source
│   ├── scripts/
│   │   └── download_assets.py  # Downloads sticker PNGs and builds sprite sheet
│   └── requirements.txt
└── README.md
```

Generated local files are intentionally ignored by git:

- `client/node_modules/`
- `client/dist/`
- `server/.venv/`
- `server/assets/stickers/*.png`
- `server/assets/sticker_sheet.png`
- Python `__pycache__/` folders

## Setup

Start the backend:

```bash
cd server
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/download_assets.py
python -m app.main
```

Start the frontend in another terminal:

```bash
cd client
npm install
npm run dev
```

Open the React URL printed by Vite. The client expects the API at `http://127.0.0.1:5001` by default. You can override it with `VITE_API_BASE_URL`.

## Asset workflow

`server/scripts/download_assets.py` downloads open sticker PNGs, writes them to `server/assets/stickers/`, and creates `server/assets/sticker_sheet.png`.

Those PNG files are generated and ignored. If they are missing after cloning, run:

```bash
cd server
source .venv/bin/activate
python scripts/download_assets.py
```

## API

- `GET /api/health` - server status.
- `GET /api/stickers` - sticker metadata.
- `POST /api/augment` - accepts `{ image, stickerId }`, where `image` is a data URL or base64 encoded image.

## Verification

Backend sanity check:

```bash
cd server
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -c "from app.main import create_app; c=create_app().test_client(); print(c.get('/api/health').json); print(len(c.get('/api/stickers').json['stickers']))"
```

Frontend type check and production build:

```bash
cd client
./node_modules/.bin/tsc --noEmit
npm run build
```
