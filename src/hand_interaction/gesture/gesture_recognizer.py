# Interpretación de los resultados del GestureRecognizer de MediaPipe

import math

class GestureRecognizer:
    PINCH_THRESHOLD = 0.05

    def get_gesture(self, result):
        """
        Obtiene el gesto detectado por MediaPipe o Pinch.
        Args:
            result: Resultado de MediaPipe GestureRecognizer.
        Returns:
            str: Nombre del gesto detectado.
        """

        if not result.gestures or not  result.hand_landmarks:
            return "Unknown"

        hand_landmarks = result.hand_landmarks[0]

        # Pinch es nuestro gesto adicional.
        if self.is_pinch(hand_landmarks):
            return "Pinch"

        # Gesto estándar reconocido por MediaPipe.
        gesture = result.gestures[0][0]

        return gesture.category_name

    def is_pinch(self, hand_landmarks):
        """
        Determina si el pulgar y el índice están realizando un Pinch.
        """

        thumb_tip = hand_landmarks[4]
        index_tip = hand_landmarks[8]

        distance = math.sqrt(
            (thumb_tip.x - index_tip.x) ** 2 +
            (thumb_tip.y - index_tip.y) ** 2
        )

        return distance < self.PINCH_THRESHOLD