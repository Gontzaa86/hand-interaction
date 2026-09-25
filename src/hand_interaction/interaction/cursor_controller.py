# Código de control de movimiento del cursor mediante gestos.

import pyautogui

class CursorController:
    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()

    # Función de movimiento, mediante el gesto "Raised Index"
    def move(self, x, y):
        screen_x = int(x * self.screen_height)
        screen_y = int(y * self.screen_height)

        pyautogui.moveTo(screen_x, screen_y)