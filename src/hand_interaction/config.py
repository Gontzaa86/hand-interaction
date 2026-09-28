# Delimitación del rectángulo de "Zona Segura" que se usará como "pantalla".
ACTIVE_AREA_LEFT = 0.15
ACTIVE_AREA_RIGHT = 0.85
ACTIVE_AREA_TOP = 0.15
ACTIVE_AREA_BOTTOM = 0.85

# Factor de suavizado para el movimiento del cursor.
# Valores altos --> Movimiento más rápido y menos suave.
# Valores bajos --> Movimientos más suaves y con más retraso.
CURSOR_SMOOTHING = 0.25

# Tiempo, en segundo, que debe permancer el gesto "L Sign" para que el próximo pinch sea considerado un click.
# Sirve como medida para evitar clickar múltiples veces con un único gesto debido a fallos en la detección de los dedos.
PINCH_ARM_DELAY = 1.0