from flask import Blueprint, request, send_from_directory

from .assets import get_sticker, serialize_stickers
from .config import ASSETS_DIR
from .face_detector import FaceDetector
from .image_io import decode_image, encode_image_data_url
from .sticker_overlay import augment_faces


api = Blueprint("api", __name__)
assets = Blueprint("assets", __name__)
detector = FaceDetector()


@api.get("/health")
def health() -> tuple[dict, int]:
    return {"ok": True, "service": "opencv-ar-stickers"}, 200


@api.get("/stickers")
def stickers() -> tuple[dict, int]:
    return {"stickers": serialize_stickers()}, 200


@api.post("/augment")
def augment() -> tuple[dict, int]:
    payload = request.get_json(silent=True) or {}
    image_payload = payload.get("image")
    if not image_payload:
        return {"error": "Missing image payload."}, 400

    try:
        frame = decode_image(image_payload)
        sticker = get_sticker(payload.get("stickerId"))
        faces = detector.detect(frame)
        augmented = augment_faces(frame, faces, sticker)
        return {
            "image": encode_image_data_url(augmented),
            "faces": [face.as_dict() for face in faces],
            "stickerId": sticker.id,
        }, 200
    except Exception as exc:
        return {"error": str(exc)}, 500


@assets.get("/<path:path>")
def serve_asset(path: str):
    return send_from_directory(ASSETS_DIR, path)

