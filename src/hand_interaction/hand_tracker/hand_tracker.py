# Código de control de MediaPipe para el trazado de los 21 puntos de la mano.

import cv2
import mediapipe as mp

from mediapipe import ImageFormat
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

class HandTracker:
    def __init__(self, model_path: str, num_hands: int = 1):
        base_options = python.BaseOptions(model_asset_path=model_path)

        options = vision.HandLandmarkerOptions(
        base_options=base_options,
        num_hands=1,
        min_hand_detection_confidence=0.5,
        min_hand_presence_confidence=0.5,
        min_tracking_confidence=0.5
        )

        self.detector = vision.HandLandmarker.create_from_options(options)

    def detect(self, frame):
        # OpenCV utiliza BGR y MediaPipe espera RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Covertir el frame al formato de MediaPipe
        mp_image = mp.Image(
            image_format=ImageFormat.SRGB,
            data=rgb_frame
        )

        # Detectar las manos
        result = self.detector.detect(mp_image)

        return result

    def draw_landmarks(self, frame, result):
        if not result.hand_landmarks:
            return frame

        height, width, _ = frame.shape

        # Dibujar los 21 puntos
        for hand_landmarks in result.hand_landmarks:
            for landmark in hand_landmarks:
                x = int(landmark.x * width)
                y = int(landmark.y * height)

                cv2.circle(
                    frame,
                    (x, y),
                    5,
                    (0, 255, 0),
                    -1
                )

        return frame

    def close(self):
        self.detector.close()
        