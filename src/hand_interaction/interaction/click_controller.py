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
        Realiza un click izquierdo cuando se inicia el gesto de Pinch.
        Solamente se produce un click al pasar de:
            - "L Sign" estable durante PINCH_ARM_DELAY --> Pinch --> Click -
        Un pinch procedente de cualquier otro gesto no produce click.
        """

        # ==========================================
        # L Sign
        # ==========================================

        if gesture == "L Sign":
            # Si acabamos de entrar en L Sign, iniciamos el temporizador.
            if self.l_sign_start_time is None:
                self.l_sign_start_time = time.monotonic()

            # Comprobamos cuánto timepo llevamos en L Sign.
            elapsed = time.monotonic() - self.l_sign_start_time

            if elapsed >= config.PINCH_ARM_DELAY:
                self.click_armed = True

            # L Sign significa que ya no estamos haciendo pinch.
            self.pinch_active = False

            return

        # ==========================================
        # Pinch
        # ==========================================

        if gesture == "Pinch":
            # Solo hacemos click si previamente hemos mantenido L Sign durante el tiempo necesario.
            if self.click_armed and not self.pinch_active:
                pyautogui.click()

                # Después del click dejamos de estar armados.
                self.click_armed = False

            self.pinch_active = True

            return

        # ==========================================
        # Cualquier otro gesto
        # ==========================================

        self.l_sign_start_time = None
        self.click_armed = False
        self.pinch_active = False