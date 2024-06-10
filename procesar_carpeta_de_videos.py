import os
import cv2
from pathlib import Path
from ultralytics import YOLO

# Cargar el modelo YOLOv8 entrenado (best.pt)
model_path = r'C:\Users\Manuel\Desktop\Carpeta Visual\PruebasModelo\SantaIsabel.pt'
model = YOLO(model_path)

# Carpeta de entrada y salida
input_folder = r'C:\Users\Manuel\Desktop\Carpeta Visual\PruebasModelo\LABORATORIOS_CELU'
output_folder = r'C:\Users\Manuel\Desktop\Carpeta Visual\PruebasModelo\SALIDA_LABORATORIOS'

# Crear la carpeta de salida si no existe
Path(output_folder).mkdir(parents=True, exist_ok=True)

# Obtener lista de todas las imágenes y videos en la carpeta de entrada
image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
video_extensions = ['.mp4', '.avi', '.mov', '.mkv']
files = [f for f in os.listdir(input_folder) if any(f.lower().endswith(ext) for ext in image_extensions + video_extensions)]

for file_name in files:
    file_path = os.path.join(input_folder, file_name)

    if any(file_name.lower().endswith(ext) for ext in image_extensions):
        # Procesar imágenes
        image = cv2.imread(file_path)
        # Redimensionar la imagen a 4K (3840x2160)
        resized_image = cv2.resize(image, (2720, 1530))
        results = model(resized_image)
        for result in results:
            # Filtrar las detecciones con una confianza mayor a 0.7
            filtered_boxes = [box for box in result.boxes if box.conf > 0.7]
            if filtered_boxes:
                result_image = result.plot()  # Renderizar resultados
                output_image_path = os.path.join(output_folder, file_name)
                cv2.imwrite(output_image_path, result_image)
        print(f"Procesada {file_name}, guardada en {output_image_path}")

    elif any(file_name.lower().endswith(ext) for ext in video_extensions):
        # Procesar videos
        video_capture = cv2.VideoCapture(file_path)
        fps = video_capture.get(cv2.CAP_PROP_FPS)
        output_video_path = os.path.join(output_folder, file_name)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_video_path, fourcc, fps, (3840, 2160))

        while video_capture.isOpened():
            ret, frame = video_capture.read()
            if not ret:
                break
            # Redimensionar el frame a 2K (3840x2160)
            resized_frame = cv2.resize(frame, (3840, 2160))
            results = model(resized_frame)
            for result in results:
                # Filtrar las detecciones con una confianza mayor a 0.8
                filtered_boxes = [box for box in result.boxes if box.conf > 0.8]
                if filtered_boxes:
                    result_frame = result.plot()  # Renderizar resultados
                    out.write(result_frame)
        video_capture.release()
        out.release()
        print(f"Procesado {file_name}, guardado en {output_video_path}")

print("Proceso completado.")
