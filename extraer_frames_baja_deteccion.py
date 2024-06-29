import cv2
import torch
from ultralytics import YOLO
import os

# Ruta del video
video_path = r'C:\Users\Manuel\Desktop\Carpeta Visual\Videoide\DJI_0262 (40m).MP4'
# Ruta donde se guardarán los frames
output_folder = r'C:\Users\Manuel\Desktop\Carpeta Visual\FramesNewTrain'

# Crear la carpeta de salida si no existe
os.makedirs(output_folder, exist_ok=True)

device = 'cuda' if torch.cuda.is_available() else 'cpu'  # tener cuda instalado (11.8) y drivers actualizados
print(f"Using device: {device}")
# Cargar el modelo YOLOv8
model = YOLO(r'C:\Users\Manuel\Desktop\Carpeta Visual\Sistema-De-Conteo-De-Ganado\EntrenarYolov8\SantaIsabel.pt').to(device)
video_name = os.path.splitext(os.path.basename(video_path))[0]
# Abrir el video
cap = cv2.VideoCapture(video_path)
frame_count = 0
saved_frame_count = 0

# Procesar el video frame por frame
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Realizar las detecciones
    results = model(frame)

    # Comprobar las detecciones y guardar el frame si hay alguna detección con la confianza requerida
    save_frame = False
    for result in results:
        boxes = result.boxes
        for box in boxes:
            conf = box.conf.item()
            if 0.5 <= conf <= 0.85:
                save_frame = True
                break
        if save_frame:
            break

    if save_frame:
        # Guardar el frame sin cuadros de detección
        frame_filename = os.path.join(output_folder, f'{video_name}_frame_{saved_frame_count:04d}.jpg')
        cv2.imwrite(frame_filename, frame)
        saved_frame_count += 1

    frame_count += 1

cap.release()
print(f'Proceso completado. Se guardaron {saved_frame_count} frames.')
