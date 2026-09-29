# Interpretación de los resultados del GestureRecognizer de MediaPipe

import math

class GestureRecognizer:
    PINCH_RATIO_THRESHOLD = 0.2

    def get_gesture(self, result):
        """
        Obtiene el gesto detectado por MediaPipe.
        Args:
            result: Resultado de MediaPipe GestureRecognizer.
        Returns:
            str: Nombre del gesto detectado.
        """

        if not result.gestures or not  result.hand_landmarks:
            return "Unknown"

        # Gesto estándar reconocido por MediaPipe.
        gesture = result.gestures[0][0]

        return gesture.category_name