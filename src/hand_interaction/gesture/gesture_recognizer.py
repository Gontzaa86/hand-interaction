# Código de reconocimiento de gestos.

import math

class GestureRecognizer:
    def recognize(self, hand_landmarks):
        """
        Recibe los 21 landmarks de una mano y devuelve el gesto detectado.
        """

        if not hand_landmarks:
            return "Unknown"

        # Determinar qué dedos están extendidos
        """
        Nota nomenclatura del código:
            - tip --> Punta del dedo
            - pip --> "Proximal Interphalangeal" | Es el nudillo medio del dedo.
            - mcp --> "Metacarpophalangeal" | Es el nudillo de la base del dedo, donde el dedo se une a la palma de la mano.
        No se usa, pero existe (para el punto restante):
            - dip --> "Distal Interphalangeal" | El nudillo más cercano a la uña
        """
        thumb_extended = self._is_thumb_extended(hand_landmarks)
        index_extended = self._is_finger_extended(
            hand_landmarks,
            tip_index=8, pip_index=6, mcp_index=5
        )
        middle_extended = self._is_finger_extended(
            hand_landmarks,
            tip_index=12, pip_index=10, mcp_index=9
        )
        ring_extended = self._is_finger_extended(
            hand_landmarks,
            tip_index=16, pip_index=14, mcp_index=13
        )
        pinky_extended = self._is_finger_extended(
            hand_landmarks,
            tip_index=20, pip_index=18, mcp_index=17
        )

        # Distintos Gestos
        # Fist
        if not any([
            thumb_extended,
            index_extended,
            middle_extended,
            ring_extended,
            pinky_extended
        ]):
            return "Fist"

        # Open Hand
        if all([
            thumb_extended,
            index_extended,
            middle_extended,
            ring_extended,
            pinky_extended
        ]):
            return "Open Hand"

        # V Sign
        if (
            index_extended
            and middle_extended
            and not ring_extended
            and not pinky_extended
        ):
            return "V Sign"

        # Raised Index
        if (
            index_extended
            and not middle_extended
            and not ring_extended
            and not pinky_extended
        ):
            return "Raised Index"

        return "Unknown"

    # Función que determina si un dedo está extendido.
    def _is_finger_extended(self, landmarks, tip_index, pip_index, mcp_index):
        """
        Determina si un dedo está extendido utilizando las distancias respecto a la muñeca.
        """

        wrist = landmarks[0]
        tip = landmarks[tip_index]
        pip = landmarks[pip_index]
        mcp = landmarks[mcp_index]

        wrist_to_tip = self._distance(wrist, tip)
        wrist_to_pip = self._distance(wrist, pip)
        wrist_to_mcp = self._distance(wrist, mcp)

        return (
            wrist_to_tip > wrist_to_pip
            and wrist_to_pip > wrist_to_mcp
        )

    def _is_thumb_extended(self, landmarks):
        """
        Determina si el pulgar está extendido.
        El pulgar necesita un tratamiento diferente debido a su orientación
        """

        wrist = landmarks[0]
        thumb_tip = landmarks[4]
        thumb_ip = landmarks[3]

        wrist_to_tip = self._distance(wrist, thumb_tip)
        wrist_to_ip = self._distance(wrist, thumb_ip)

        return wrist_to_tip > wrist_to_ip

    @staticmethod
    def _distance(point_a, point_b):
        """
        Distancia euclídea entre dos landmarks.
        La distancia euclidiana es la longitud del segmento de recta que une dos puntos, calculada mediante el teorema de Pitágoras.
        """

        dx = point_a.x - point_b.x
        dy = point_a.y - point_b.y

        return math.sqrt(dx * dx + dy * dy)