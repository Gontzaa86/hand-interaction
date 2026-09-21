# FICHERO TEMPORAL PARA PRUEBAS DE DETECCIón DE MANO EN EL PORTÁTIL-

import cv2
import mediapipe as mp

from mediapipe import ImageFormat
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

MODEL_PATH = "models/hand_landmarker.task"

# Configuración del modelo
base_options = python.BaseOptions(model_asset_path=MODEL_PATH)

options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=1,
    min_hand_detection_confidence=0.5,
    min_hand_presence_confidence=0.5,
    min_tracking_confidence=0.5
)

# Crear el detector
detector = vision.HandLandmarker.create_from_options(options)

# Abrir Webcam
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("No se pudo abrir la cámara.")
    exit()

print("Cámara abierta correctamente. Pulsa 'Q' para salir.")

while True:
    success, frame = camera.read()

    if not success:
        print("No se pudo leer un frame.")
        break

    # OpenCV utiliza BGR y MediaPipe espera RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Convertir el frame al formato de MediaPie
    mp_image = mp.Image(
        image_format=ImageFormat.SRGB,
        data=rgb_frame
    )

    # Detectar manos
    result = detector.detect(mp_image)

    # Dibujar landmarks si se ha encontrado una mano
    if result.hand_landmarks:
        for hand_landmarks in result.hand_landmarks:
            height, width, _ = frame.shape

            # Dibujar los 21 puntos
            for landmark in hand_landmarks:
                x = int(landmark.x * width)
                y = int(landmark.y * height)

                cv2.circle(
                    frame,
                    (x, y),
                    5,
                    (0, 255, 0),
                    -1
                )

    # cv2.flip(frame, 1, frame) # Voltea horizontalmente, para evitar el efecto espejo del a imágen.
    
    # Mostrar resultados
    cv2.imshow("Hand Interaction", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
detector.close()