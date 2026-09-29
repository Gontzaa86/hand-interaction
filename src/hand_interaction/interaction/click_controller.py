# Código de control de click mediante gesto de Pinch.

import time
import pyautogui

from hand_interaction import config

class ClickController:
    def __init__(self):
        # Inicialización de variables de control de clicks.
        self.l_sign_start_time = None
        self.click_armed = False
        self.pinch_active = False

    def update(self, gesture):
        """
        Realiza un click izquierdo cuando se inicia el gesto de Closed_Fist.
        """

        fist_detected = gesture == "Closed_Fist"

        # Detectar la transición: No puño → Puño
        if fist_detected and not self.fist_active:
            pyautogui.click()

        self.fist_active = fist_detected