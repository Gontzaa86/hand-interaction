import cv2

from hand_interaction.camera.camera import Camera
from hand_interaction.hand_tracker.hand_tracker import HandTracker
from hand_interaction.gesture.gesture_recognizer import GestureRecognizer

MODEL_PATH = "models/hand_landmarker.task"

def main():
    camera = Camera()
    hand_tracker = HandTracker(MODEL_PATH)
    gesture_recognizer = GestureRecognizer()

    print("Cámara abierta correctamente. Pulsa 'Q' para cerrar.")

    try:
        while True:
            # Obtener frame de la cámara.
            frame = camera.read()

            # Detectar manos
            result = hand_tracker.detect(frame)

            # Dibujar landmarks
            frame = hand_tracker.draw_landmarks(frame, result)

            # Establecer gesto por defecto
            gesture = "No Hand"

            # Estados de los dedos por defecto
            finger_states = {
                "Thumb": False,
                "Index": False,
                "Middle": False,
                "Ring": False,
                "Pinky": False
            }

            # Si se detecta una mano
            if result.hand_landmarks:
                hand_landmarks = result.hand_landmarks[0]

                # Obtener estado de los dedos
                finger_states = gesture_recognizer.get_finger_states(hand_landmarks)

                # Reconocer el gesto
                gesture = gesture_recognizer.recognize(hand_landmarks)

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

if __name__ == "__main__":
    main()