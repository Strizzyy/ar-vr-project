from functools import lru_cache

import cv2
import numpy as np

from .assets import Sticker
from .face_detector import FaceBox


@lru_cache(maxsize=32)
def _load_sticker(path: str) -> np.ndarray:
    sticker = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if sticker is None:
        raise FileNotFoundError(f"Sticker asset not found: {path}")
    if sticker.shape[2] == 3:
        alpha = np.full(sticker.shape[:2] + (1,), 255, dtype=np.uint8)
        sticker = np.concatenate([sticker, alpha], axis=2)
    return sticker


def _placement(face: FaceBox, sticker: Sticker) -> tuple[int, int, int, int]:
    width = max(1, int(face.width * sticker.scale))
    original = _load_sticker(str(sticker.path))
    aspect = original.shape[0] / original.shape[1]
    height = max(1, int(width * aspect))
    center_x = face.x + face.width // 2
    center_y = face.y + int(face.height * sticker.y_offset)

    if sticker.anchor == "forehead":
        top = face.y + int(face.height * sticker.y_offset) - height // 2
    elif sticker.anchor == "eyes":
        top = face.y + int(face.height * sticker.y_offset) - height // 2
    else:
        top = center_y + face.height // 2 - height // 2

    left = center_x - width // 2
    return left, top, width, height


def overlay_sticker(frame: np.ndarray, face: FaceBox, sticker: Sticker) -> np.ndarray:
    sticker_image = _load_sticker(str(sticker.path))
    left, top, width, height = _placement(face, sticker)
    resized = cv2.resize(sticker_image, (width, height), interpolation=cv2.INTER_AREA)

    frame_h, frame_w = frame.shape[:2]
    x1 = max(0, left)
    y1 = max(0, top)
    x2 = min(frame_w, left + width)
    y2 = min(frame_h, top + height)

    if x1 >= x2 or y1 >= y2:
        return frame

    sx1 = x1 - left
    sy1 = y1 - top
    sx2 = sx1 + (x2 - x1)
    sy2 = sy1 + (y2 - y1)

    sticker_roi = resized[sy1:sy2, sx1:sx2]
    rgb = sticker_roi[:, :, :3].astype(float)
    alpha = (sticker_roi[:, :, 3:4].astype(float) / 255.0)
    roi = frame[y1:y2, x1:x2].astype(float)
    blended = (alpha * rgb) + ((1.0 - alpha) * roi)
    frame[y1:y2, x1:x2] = blended.astype(np.uint8)
    return frame


def augment_faces(frame: np.ndarray, faces: list[FaceBox], sticker: Sticker) -> np.ndarray:
    output = frame.copy()
    for face in faces:
        output = overlay_sticker(output, face, sticker)
    return output

