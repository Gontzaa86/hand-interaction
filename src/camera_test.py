# FICHERO TEMPORAL PARA PRUEBAS DE CÁMARA EN EL PORTÁTIL

import cv2

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

    cv2.imshow("Camera test", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()