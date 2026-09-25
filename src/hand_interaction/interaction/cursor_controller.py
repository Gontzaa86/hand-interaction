# Código de control de movimiento del cursor mediante gestos.

import pyautogui
from hand_interaction import config

class CursorController:
    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()

    @staticmethod
    def _map_coordinate(value, minimum, maximum):
        """
        Función que delimita el rango de acción de la cámara para evitar problemas de detección 
        y problemas con los bordes.
        """
        value = max(minimum, min(value, maximum))

        return (value - minimum) / (maximum - minimum)

    # Función de movimiento, mediante el gesto "Raised Index"
    def move(self, x, y):
        x = self._map_coordinate(x, config.ACTIVE_AREA_LEFT, config.ACTIVE_AREA_RIGHT)
        y = self._map_coordinate(y, config.ACTIVE_AREA_TOP, config.ACTIVE_AREA_BOTTOM)

        screen_x = int(x * (self.screen_width - 1))
        screen_y = int(y * (self.screen_height - 1))
        
        pyautogui.moveTo(screen_x, screen_y)

    # Verifica si el dedo se encuentra dentro del área definida.
    def is_inside_active_area(self, x, y):
        return(
            config.ACTIVE_AREA_LEFT <= x <= config.ACTIVE_AREA_RIGHT
            and
            config.ACTIVE_AREA_TOP <= y <= config.ACTIVE_AREA_BOTTOM
        )