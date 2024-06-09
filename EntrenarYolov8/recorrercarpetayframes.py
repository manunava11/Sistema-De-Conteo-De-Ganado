import os
import cv2

def extract_frames_from_video(video_path, output_folder):
    # Crear el objeto de captura de video
    video_capture = cv2.VideoCapture(video_path)
    
    # Verificar si el video se abrió correctamente
    if not video_capture.isOpened():
        print(f"No se puede abrir el video {video_path}")
        return
    
    frame_number = 0
    
    while True:
        # Leer el siguiente frame
        ret, frame = video_capture.read()
        
        # Si no se pudo leer el frame, salir del bucle
        if not ret:
            break
        
        # Construir el nombre del archivo para el frame
        frame_filename = os.path.join(output_folder, f"frame_{frame_number:04d}.png")
        
        # Guardar el frame como una imagen
        cv2.imwrite(frame_filename, frame)
        
        frame_number += 1
    
    # Liberar el objeto de captura de video
    video_capture.release()
    print(f"Frames extraídos y guardados en {output_folder}")

def process_videos_in_folder(input_folder):
    # Verificar si la carpeta de entrada existe
    if not os.path.isdir(input_folder):
        print(f"La carpeta {input_folder} no existe")
        return
    
    # Recorrer todos los archivos en la carpeta de entrada
    for filename in os.listdir(input_folder):
        # Construir la ruta completa al archivo
        file_path = os.path.join(input_folder, filename)
        
        # Verificar si el archivo es un video (puedes ajustar esta verificación según tus necesidades)
        if not filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
            continue
        
        # Crear la carpeta de salida para los frames
        video_name = os.path.splitext(filename)[0]
        output_folder = os.path.join(input_folder, video_name)
        
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        # Extraer los frames del video
        extract_frames_from_video(file_path, output_folder)

# Ruta de la carpeta que contiene los videos
input_folder = 'ruta/a/tu/carpeta/de/videos'

# Procesar los videos en la carpeta
process_videos_in_folder(input_folder)
