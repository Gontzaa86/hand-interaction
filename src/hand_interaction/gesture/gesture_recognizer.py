# Código de reconocimiento de gestos.

import math

THUMB_EXTENDED_ANGLE = 155 # 155º es el valor aproximado obtenido como delimitador tras las pruebas.

class GestureRecognizer:
    def get_finger_states(self, hand_landmarks):
        """
        Devuelve el estado de los cinco dedos.
        True --> Dedo extendido
        Flase --> Dedo recogido

        Sumado a una interfaz, permitirá ver que esta viendo o entendiendo realmente el ordenador
        permitiendo depurar la detección de dedos y gestos más fácilmente.
        """

        if not hand_landmarks:
            return {
                "Thumb": False,
                "Index": False,
                "Middle": False,
                "Ring": False,
                "Pinky": False
            }

        """
        Nota nomenclatura del código:
            - tip --> Punta del dedo
            - pip --> "Proximal Interphalangeal" | Es el nudillo medio del dedo.
            - mcp --> "Metacarpophalangeal" | Es el nudillo de la base del dedo, donde el dedo se une a la palma de la mano.
        No se usa, pero existe (para el punto restante):
            - dip --> "Distal Interphalangeal" | El nudillo más cercano a la uña
        """
        return {
            "Thumb": self._is_thumb_extended(hand_landmarks),
            "Index": self._is_finger_extended(
                hand_landmarks,
                tip_index=8, pip_index=6, mcp_index=5
            ),
            "Middle": self._is_finger_extended(
                hand_landmarks,
                tip_index=12, pip_index=10, mcp_index=9
            ),
            "Ring": self._is_finger_extended(
                hand_landmarks,
                tip_index=16, pip_index=14, mcp_index=13
            ),
            "Pinky": self._is_finger_extended(
                hand_landmarks,
                tip_index=20, pip_index=18, mcp_index=17
            )
        }

    def recognize(self, hand_landmarks):
        """
        Recibe los 21 landmarks de una mano y devuelve el gesto detectado.
        """

        if not hand_landmarks:
            return "Unknown"

        fingers = self.get_finger_states(hand_landmarks)

        thumb = fingers["Thumb"]
        index = fingers["Index"]
        middle = fingers["Middle"]
        ring = fingers["Ring"]
        pinky = fingers["Pinky"]

        # ==== Definimos distintos Gestos ====
        # Fist
        if not any(fingers.values()):
            return "Fist"

        # Open Hand
        if all(fingers.values()):
            return "Open Hand"

        # V Sign
        if (
            index
            and middle
            and not ring
            and not pinky
        ):
            return "V Sign"

        # Raised Index
        if (
            index
            and not middle
            and not ring
            and not pinky
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

        # Calcular mediante la distancia entre la punta del pulgar (4), y el nudillo del meñique (17).
        thumb_tip = landmarks[4]
        thumb_ip = landmarks[3]
        pinky_mcp = landmarks[17]

        tip_distance = self._distance(thumb_tip, pinky_mcp)
        ip_distance = self._distance(thumb_ip, pinky_mcp)

        return tip_distance > ip_distance

    @staticmethod
    def _distance(point_a, point_b):
        """
        Distancia euclídea entre dos landmarks.
        La distancia euclidiana es la longitud del segmento de recta que une dos puntos, calculada mediante el teorema de Pitágoras.
        """

        dx = point_a.x - point_b.x
        dy = point_a.y - point_b.y

        return math.sqrt(dx * dx + dy * dy)