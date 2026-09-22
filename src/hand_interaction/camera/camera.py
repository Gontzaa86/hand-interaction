# Código de control de la cámara mediante OpenCV.

import cv2

class Camera:
    def __init__(self, camera_index: int = 0):
        self.camera = cv2.VideoCapture(camera_index)

        if not self.camera.isOpened():
            raise RuntimeError("No se pudo abrir la cámara.")

    def read(self):
        success, frame = self.camera.read()

        if not success:
            raise RuntimeError("No se pudo leer un frame de la cámara.")

        return frame

    def release(self):
        self.camera.release()