import cv2
import os
from ultralytics import YOLO, solutions

# Rutas de los archivos
video_input_path = r'C:\Users\Manuel\Desktop\Carpeta Visual\Sistema-De-Conteo-De-Ganado\RecorteConteo2.MP4'
output_folder = r'C:\Users\Manuel\Desktop\Carpeta Visual\Sistema-De-Conteo-De-Ganado'

# Cargar el modelo YOLO
model = YOLO(os.path.join(output_folder, r'C:\Users\Manuel\Desktop\Carpeta Visual\Sistema-De-Conteo-De-Ganado\EntrenarYolov8\SantaIsabel.pt'))

# Abrir el video
cap = cv2.VideoCapture(video_input_path)
assert cap.isOpened(), "Error reading video file"

# Obtener propiedades del video
w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

# Definir puntos de la línea
line_points = [(0, 1100), (2720, 1100)]

# Nombre del video resultante
video_name = os.path.basename(video_input_path)
output_video_name = "Conteo_Resultante_" + video_name

# Inicializar el escritor de video con la ruta de salida deseada
output_video_path = os.path.join(output_folder, output_video_name)
video_writer = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

# Inicializar el contador de objetos
counter = solutions.ObjectCounter(
    view_img=False,  # No mostrar la imagen
    reg_pts=line_points,
    classes_names=model.names,
    draw_tracks=False,
    line_thickness=2,
    track_thickness=0,
    view_out_counts=False,
    view_in_counts=False,
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
    tracks = model.track(im0, persist=True, show=False, conf=0.7, tracker="bytetrack.yaml")

    # Contar los objetos en el frame
    current_count = counter.start_counting(im0, tracks)
    total_count = counter.in_counts + counter.out_counts
    text = f'Conteo total: {total_count}'
    cv2.putText(im0, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # Escribir el frame procesado en el video de salida
    video_writer.write(im0)

# Liberar recursos
cap.release()
video_writer.release()
cv2.destroyAllWindows()

total_count = counter.in_counts + counter.out_counts
print(f"Proceso completado. Total de vacas: {total_count}. Video de salida generado como '{output_video_name}' en la carpeta deseada.")
