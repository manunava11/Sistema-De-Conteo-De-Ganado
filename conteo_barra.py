import cv2 # opencv-python
import os
from ultralytics import YOLO, solutions #ultralytics
import torch #torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Rutas de los archivos
video_input_path = r'C:\Users\Manuel\Desktop\Carpeta Visual\Videoide\DJI_0262 (40m).MP4'
output_folder = r'C:\Users\Manuel\Desktop\Carpeta Visual\Sistema-De-Conteo-De-Ganado'

# Verificar si CUDA está disponible
device = 'cuda' if torch.cuda.is_available() else 'cpu' # tener cuda instalado (11.8) y drivers actualizados
print(f"Using device: {device}")
#PyTorch version: 2.2.2+cu118
#CUDA version: 11.8
#torchvision version: 0.17.2+cu118
#torchaudio version: 2.2.2+cu118
model = YOLO(os.path.join(output_folder, r'C:\Users\Manuel\Desktop\Carpeta Visual\Sistema-De-Conteo-De-Ganado\EntrenarYolov8\BestNuestrasX.pt')).to(device)

# Abrir el video
cap = cv2.VideoCapture(video_input_path)
assert cap.isOpened(), "Error reading video file"

# Obtener propiedades del video
w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

# Definir puntos de la línea
# line_points = [(0, 1400), (2720, 1400)]
# Define region points
region_points = [(0, 0), (0, h), (w, h), (w, 0)]
# Nombre del video resultante
video_name = os.path.basename(video_input_path)
output_video_name = "Conteo_Resultante_" + video_name
track_buffer=300 # 10 segundos
# Inicializar el escritor de video con la ruta de salida deseada
output_video_path = os.path.join(output_folder, output_video_name)
video_writer = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

# Inicializar el contador de objetos
counter = solutions.ObjectCounter(
    view_img=False,  # No mostrar la imagen
    # reg_pts=line_points,
    reg_pts=region_points,
    classes_names=model.names,
    draw_tracks=False,
    line_thickness=2,
    track_thickness=2,
    view_out_counts=False,
    view_in_counts=False,
    count_reg_color=(0,255,0),
    region_thickness=0,
)

# Contador total de objetos que cruzan la línea
total_count = 0

# Procesar el video
while cap.isOpened():
    success, im0 = cap.read()
    if not success:
        print("Video frame is empty or video processing has been successfully completed.")
        break

    # Realizar el tracking con el modelo
    tracks = model.track(im0, persist=True, show=False, conf=0.7,iou=0.5, tracker="bytetrack.yaml")

    # Contar los objetos en el frame
    current_count = counter.start_counting(im0, tracks)
    total_count = counter.in_counts + counter.out_counts
    text = f'Conteo total: {total_count}'
    text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
    text_x, text_y = 50, 50
    # Rectangulo blanco atras del texto
    cv2.rectangle(im0, (text_x - 5, text_y + 5), (text_x + text_size[0] + 5, text_y - text_size[1] - 5), (255, 255, 255), cv2.FILLED)
    cv2.putText(im0, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (44, 110, 47), 2, cv2.LINE_AA)
    # Escribir el frame procesado en el video de salida
    video_writer.write(im0)

# Liberar recursos
cap.release()
video_writer.release()
cv2.destroyAllWindows()

total_count = counter.in_counts + counter.out_counts
print(f"Proceso completado. Total de vacas: {total_count}. Video de salida generado como '{output_video_name}' en la carpeta deseada.")
