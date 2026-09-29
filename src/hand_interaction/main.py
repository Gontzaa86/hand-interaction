import cv2

from hand_interaction import config

from hand_interaction.camera.camera import Camera

from hand_interaction.hand_tracker.hand_tracker import HandTracker

from hand_interaction.gesture.finger_states import FingerStateDetector
from hand_interaction.gesture.gesture_classifier import GestureClassifier

from hand_interaction.interaction.cursor_controller import CursorController
from hand_interaction.interaction.click_controller import ClickController

MODEL_PATH = "models/gesture_recognizer.task"

def main():
    camera = Camera()
    hand_tracker = HandTracker(MODEL_PATH)

    finger_detector = FingerStateDetector()
    gesture_classifier = GestureClassifier()

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

            # Verificación de carga de gestos con nueva lógica de Gesture Recognizer de MediaPipe
            # Mostrar unicamente; Score y category_name
            if result.gestures:
                gesture = result.gestures[0][0]

                print(f"Gesto: {gesture.category_name} | Confianza: {gesture.score:.3f}")

            # Dibujar landmarks
            frame = hand_tracker.draw_landmarks(frame, result)

            # Establecer gesto por defecto
            gesture = "No Hand"

            # Estados de los dedos por defecto
            finger_states = {
                "thumb": False,
                "index": False,
                "middle": False,
                "ring": False,
                "pinky": False
            }

            # Si se detecta una mano
            if result.hand_landmarks:
                hand_landmarks = result.hand_landmarks[0]

                # Obtener estado de los dedos
                finger_states = finger_detector.get_finger_states(hand_landmarks)

                # Reconocer el gesto
                gesture = gesture_classifier.classify(finger_states)

                # Mover el cursor si se está apuntando.
                if gesture == "Raised Index":
                    index_tip = hand_landmarks[8]

                    # Mover únicamente si se encuentra dentro del recuadro.
                    if cursor_controller.is_inside_active_area(index_tip.x, index_tip.y):
                        cursor_controller.move(index_tip.x, index_tip.y)
                    else:
                        # Reiniciar suaziado cuando el dedo sale de la zona.
                        cursor_controller.reset_smoothing()

                # Cambiar gesto de "L Sign" a "Pinch" si los dedos se encuentran juntos.
                if gesture == "L Sign":
                    if finger_detector.is_pinch(hand_landmarks):
                        gesture = "Pinch"

            click_controller.update(gesture) # Clicka si se cumplen las condiciones establecidas.

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

            # Mostrar estado de los dedos
            frame = draw_finger_status(frame, finger_states)
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

def draw_finger_status(frame, finger_states):
    """
    Muestra el estado de los cinco dedos en la esquina superior derecha
    """

    height, width, _ = frame.shape

    x = width - 180
    y = 40

    for finger, extended in finger_states.items():
        if extended:
            color = (0, 255, 0)
            state = "EXTENDED"
        else:
            color = (0, 0, 255)
            state = "FOLDED"

        cv2.putText(
            frame,
            f"{finger}: {state}",
            (x, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            color,
            2,
            cv2.LINE_AA
        )

        y += 30

    return frame

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