import cv2
import os

def extract_frames(video_path, output_folder, interval=1):
    # Crea la carpeta de salida si no existe
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Abre el video
    video_capture = cv2.VideoCapture(video_path)
    
    # Obtén la cantidad de frames por segundo (fps) del video
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    
    # Calcula el intervalo de frames a capturar basado en los fps
    frame_interval = int(fps * interval)
    
    frame_count = 0
    success = True
    
    while success:
        # Lee el siguiente frame
        success, frame = video_capture.read()
        
        if not success:
            break
        
        # Guarda el frame si es múltiplo del intervalo
        if frame_count % frame_interval == 0:
            frame_filename = os.path.join(output_folder, f"DJI0164_{frame_count}.jpg") #Poner nombre
            cv2.imwrite(frame_filename, frame)
            print(f"Guardado {frame_filename}")
        
        frame_count += 1
    
    # Libera el video
    video_capture.release()
    print("Extracción de frames completada.")

# Ejemplo de uso
video_path = 'C:\\Users\\Manuel\\Desktop\\Carpeta Visual\\PruebasModelo\\DJI_0164.mp4'
output_folder = 'C:\\Users\\Manuel\\Desktop\\Carpeta Visual\\PruebasModelo\\framesAEtiquetar'

extract_frames(video_path, output_folder)
