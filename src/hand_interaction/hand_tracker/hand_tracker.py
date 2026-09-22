# Código de control de MediaPipe para el trazado de los 21 puntos de la mano.

import cv2
import mediapipe as mp

from mediapipe import ImageFormat
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# Colores para diferenciación de dedos en el "Esqueleto" de la mano. BGR (OpenCV)
THUMB_COLOR = (0, 0, 255)       # Rojo
INDEX_COLOR = (0, 255, 255)     # Amarillo
MIDDLE_COLOR = (0, 255, 0)      # Verde
RING_COLOR = (255, 0, 0)        # Azul
PINKY_COLOR = (255, 0, 255)     # Morado
PALM_COLOR = (255, 255, 255)    # Blanco

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

        # Conexiones con cáda dedo.
        # El landmark 0 corresponde a la palma de la mano, el resto 4 por dedo de forma ordenada.
        fingers = {
            "thumb": {
                "landmarks": [1, 2, 3, 4],
                "color": THUMB_COLOR
            },
            "index": {
                "landmarks": [5, 6, 7, 8],
                "color": INDEX_COLOR
            },
            "middle": {
                "landmarks": [9, 10, 11, 12],
                "color": MIDDLE_COLOR
            },
            "ring": {
                "landmarks": [13, 14, 15, 16],
                "color": RING_COLOR
            },
            "pinky": {
                "landmarks": [17, 18, 19, 20],
                "color": PINKY_COLOR
            }
        }

        # Dibujar los 21 puntos
        for hand_landmarks in result.hand_landmarks:
            # Convertir landmarks normalizados a píxeles.
            points = []

            for landmark in hand_landmarks:
                x = int(landmark.x * width)
                y = int(landmark.y * height)

                points.append((x, y))

            # Dibujar palma y conexiones principales
            palm_connections = [
                (0, 1),     # Palma --> Pulgar
                (0, 5),     # Palma --> Índice
                (0, 9),     # Palma --> Corazón
                (0, 13),    # Palma --> Anular
                (0, 17),    # Palma --> Meñique
                (5, 9),     # Índice
                (9, 13),    # Corazón
                (13, 17)    # Anular
            ]

            for start, end in palm_connections:
                cv2.line(
                    frame,
                    points[start],
                    points[end],
                    PALM_COLOR,
                    1
                )

            # Dibujar cada dedo con su color.
            for finger in fingers.values():
                landmark_indices = finger["landmarks"]
                color = finger["color"]

                for i in range(len(landmark_indices) - 1):
                    start = landmark_indices[i]
                    end = landmark_indices[i + 1]

                    cv2.line(
                        frame,
                        points[start],
                        points[end],
                        color,
                        2
                    )

                # Dibujar los puntos.
                for index in landmark_indices:
                    cv2.circle(
                        frame,
                        points[index],
                        5,
                        color,
                        -1
                    )

            # Dibujar la muñeca.
            cv2.circle(
                frame,
                points[0],
                6,
                PALM_COLOR,
                -1
            )

        return frame

    def close(self):
        self.detector.close()
        