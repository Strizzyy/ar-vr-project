from dataclasses import dataclass

import cv2
import numpy as np


@dataclass(frozen=True)
class FaceBox:
    x: int
    y: int
    width: int
    height: int

    def as_dict(self) -> dict:
        return {
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
        }


class FaceDetector:
    def __init__(self) -> None:
        cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        self.classifier = cv2.CascadeClassifier(cascade_path)
        if self.classifier.empty():
            raise RuntimeError(f"Could not load OpenCV cascade: {cascade_path}")

    def detect(self, image: np.ndarray) -> list[FaceBox]:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        boxes = self.classifier.detectMultiScale(
            gray,
            scaleFactor=1.08,
            minNeighbors=5,
            minSize=(80, 80),
            flags=cv2.CASCADE_SCALE_IMAGE,
        )
        return [FaceBox(int(x), int(y), int(w), int(h)) for (x, y, w, h) in boxes]

