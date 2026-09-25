# Código de detección de gestos de la mano, basado en finger_states.

class GestureClassifier:
    def classify(self, fingers):
        """
        Clasifica un conjunto de estados de dedos y devuelve el gesto correspondiente.
        """

        if not fingers: 
            return "Unknown"

        thumb = fingers["thumb"]
        index = fingers["index"]
        middle = fingers["middle"]
        ring = fingers["ring"]
        pinky = fingers["pinky"]
        
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