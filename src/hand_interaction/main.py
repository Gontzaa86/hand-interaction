import cv2

from hand_interaction import config

from hand_interaction.camera.camera import Camera

from hand_interaction.hand_tracker.hand_tracker import HandTracker

from hand_interaction.gesture.gesture_recognizer import GestureRecognizer

from hand_interaction.interaction.cursor_controller import CursorController
from hand_interaction.interaction.click_controller import ClickController

MODEL_PATH = "models/gesture_recognizer.task"

def main():
    camera = Camera()
    hand_tracker = HandTracker(MODEL_PATH)
    gesture_recognizer = GestureRecognizer()

    cursor_controller = CursorController()
    click_controller = ClickController()

    print("Cámara abierta correctamente. Pulsa 'Q' para cerrar.")

    try:
        while True:
            # Obtener frame de la cámara. Rotar horizontalmente para evitar efecto espejo.
            frame = camera.read()
            frame = cv2.flip(frame, 1)

            # Detectar manos
            result = hand_tracker.detect(frame)

            # Interpretar el resultado de MediaPipe y detectar Pinch.
            gesture = gesture_recognizer.get_gesture(result)
            print(f"Gesto: {gesture}")

            # Si no hay ninguna mano, mostramos "No Hand"
            if not result.hand_landmarks:
                gesture = "No Hand"

            # Dibujar landmarks
            frame = hand_tracker.draw_landmarks(frame, result)

            # Si se detecta una mano
            if result.hand_landmarks:
                hand_landmarks = result.hand_landmarks[0]

                # Mover el cursor si se está apuntando.
                if gesture == "Pointing_Up":
                    index_tip = hand_landmarks[8]

                    # Mover únicamente si se encuentra dentro del recuadro.
                    if cursor_controller.is_inside_active_area(index_tip.x, index_tip.y):
                        cursor_controller.move(index_tip.x, index_tip.y)
                    else:
                        # Reiniciar suaziado cuando el dedo sale de la zona.
                        cursor_controller.reset_smoothing()

            # Actualizar el controlador del click.
            click_controller.update(gesture)

            # Mostrar el gesto en pantalla
            cv2.putText(
                frame,
                f"Gesture: {gesture}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2,
                cv2.LINE_AA
            )

            # Mostrar área de interacción
            frame = draw_active_area(frame)

            # Mostrar imágen
            cv2.imshow("Hand Interaction", frame)

            # Salir con la Q
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        camera.release()
        hand_tracker.close()
        cv2.destroyAllWindows()

def draw_active_area(frame):
    """
    Muestra el rectángulo de acción donde se podrá mover el índice para controlar el ratón.
    """
    height, width, _ = frame.shape

    left = int(width * config.ACTIVE_AREA_LEFT)
    right = int(width * config.ACTIVE_AREA_RIGHT)
    top = int(height * config.ACTIVE_AREA_TOP)
    bottom = int(height * config.ACTIVE_AREA_BOTTOM)

    cv2.rectangle(
        frame,
        (left, top),
        (right, bottom),
        (255, 255, 0),
        2
    )

    return frame

if __name__ == "__main__":
    main()