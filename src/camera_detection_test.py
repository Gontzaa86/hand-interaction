# FICHERO TEMPORAL PARA PRUEBAS DE DETECCIón DE MANO EN EL PORTÁTIL-

import cv2
import mediapipe as mp

# Inicializar mediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode = False,
    max_num_hands = 1,
    min_detection_confidence = 0.5,
    min_tracking_confidence = 0.5
)

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

    # Detectar manos
    results = hands.process(rgb_frame)

    # Dibujar landmarks si se ha encontrado una mano
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

    # cv2.flip(frame, 1, frame) # Voltea horizontalmente, para evitar el efecto espejo del a imágen.
    
    # Mostrar resultados
    cv2.imshow("Hand Interaction", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
hands.close()