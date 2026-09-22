import cv2

from hand_interaction.camera.camera import Camera
from hand_interaction.hand_tracker.hand_tracker import HandTracker

MODEL_PATH = "models/hand_landmarker.task"

def main():
    camera = Camera()
    hand_tracker = HandTracker(MODEL_PATH)

    print("Cámara abierta correctamente. Pulsa 'Q' para cerrar.")

    try:
        while True:
            # Obtener frame de la cámara.
            frame = camera.read()

            # Detectar manos
            result = hand_tracker.detect(frame)

            # Dibujar landmarks
            frame = hand_tracker.draw_landmarks(frame, result)

            # Mostrar imágen
            cv2.imshow("Hand Interaction", frame)

            # Salir con la Q
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        camera.release()
        hand_tracker.close()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()