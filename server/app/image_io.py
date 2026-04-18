import base64
from io import BytesIO

import cv2
import numpy as np
from PIL import Image


def decode_image(data: str) -> np.ndarray:
    if "," in data:
        data = data.split(",", 1)[1]
    payload = base64.b64decode(data)
    array = np.frombuffer(payload, dtype=np.uint8)
    image = cv2.imdecode(array, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("Could not decode image payload.")
    return image


def encode_image_data_url(image: np.ndarray) -> str:
    ok, buffer = cv2.imencode(".png", image)
    if not ok:
        raise ValueError("Could not encode augmented image.")
    encoded = base64.b64encode(buffer).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def pil_to_cv_rgba(image: Image.Image) -> np.ndarray:
    rgba = image.convert("RGBA")
    return cv2.cvtColor(np.array(rgba), cv2.COLOR_RGBA2BGRA)


def cv_to_pil(image: np.ndarray) -> Image.Image:
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return Image.fromarray(rgb)

