# Código de control de movimiento del cursor mediante gestos.

import pyautogui

from hand_interaction import config

class CursorController:
    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()

        self.previous_x = None
        self.previous_y = None

    @staticmethod
    def _map_coordinate(value, minimum, maximum):
        """
        Función que delimita el rango de acción de la cámara para evitar problemas de detección 
        y problemas con los bordes. Normlaiza la coordenada a un ranto entre 0.0 - 1.0.
        """
        value = max(minimum, min(value, maximum))

        return (value - minimum) / (maximum - minimum)

    # Función de movimiento, mediante el gesto "Raised Index"
    def move(self, x, y):
        x = self._map_coordinate(x, config.ACTIVE_AREA_LEFT, config.ACTIVE_AREA_RIGHT)
        y = self._map_coordinate(y, config.ACTIVE_AREA_TOP, config.ACTIVE_AREA_BOTTOM)

        # Inicializar la posición la primera vez.
        if self.previous_x is None:
            self.previous_x = x
            self.previous_y = y

        # Aplicar suavizado
        self.previous_x += (x - self.previous_x) * config.CURSOR_SMOOTHING
        self.previous_y += (y - self.previous_y) * config.CURSOR_SMOOTHING

        screen_x = int(self.previous_x * (self.screen_width - 1))
        screen_y = int(self.previous_y * (self.screen_height - 1))
        
        pyautogui.moveTo(screen_x, screen_y)

    # Verifica si el dedo se encuentra dentro del área definida.
    def is_inside_active_area(self, x, y):
        return(
            config.ACTIVE_AREA_LEFT <= x <= config.ACTIVE_AREA_RIGHT
            and
            config.ACTIVE_AREA_TOP <= y <= config.ACTIVE_AREA_BOTTOM
        )

    # Reiniciar el estado del suavizado. Para cuando el dedo sale del rectángulo.
    def reset_smoothing(self):
        self.previous_x = None
        self.previous_y = None