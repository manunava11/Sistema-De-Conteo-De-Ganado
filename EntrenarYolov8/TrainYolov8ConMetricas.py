from ultralytics import YOLO
import torch
import os

def main():
    # Verificación de disponibilidad de CUDA
    print("Is CUDA available: ", torch.cuda.is_available())
    print("Number of GPUs: ", torch.cuda.device_count())
    print("CUDA version: ", torch.version.cuda)
    if torch.cuda.is_available():
        print("GPU Name: ", torch.cuda.get_device_name(0))
        torch.backends.cudnn.enabled = False  # Si no me tira NAN
    else:
        print("No CUDA GPUs are available")

    # Cargar el modelo YOLOv8
    model = YOLO('yolov8n.pt')  # Puedes cambiar el modelo por el que estás usando
    #model = YOLO(r"yolov8x.pt").load(r"Sistema-De-Conteo-De-Ganado\EntrenarYolov8\best70.pt")  # build from YAML and transfer weights
    # Definir la ruta donde se guardarán los pesos
    save_dir = 'runs/detect/TrainPrueba/weights'

    # Entrenar el modelo y registrar métricas
    results = model.train(
        data=r"C:\Users\Manuel\Desktop\Carpeta Visual\Sistema-De-Conteo-De-Ganado\EntrenarYolov8\config2.yaml",  # Ruta a tu archivo de configuración de datos
        epochs=500,  # Número de épocas,
        patience=50,
        device='cuda',
        #batch=0.7,  # Tamaño del batch (90% de la GPU si tengo)
        imgsz=640,  # Tamaño de las imágenes
        #save_period=5,  # Guardar cada cuántas épocas
        name='NuestrasV8n500',  # Nombre carpeta donde se guarda todo
        val=True  # Validar en cada época
    )

    # Validate the model using Traing
    metrics = model.val(split='val')  # no arguments needed, dataset and settings remembered
    boxMap5095Val=metrics.box.map
    boxMap50Val=metrics.box.map50
    boxMap75Val=metrics.box.map75

    # Validate the model using Train
    metrics = model.val(split='train')  # no arguments needed, dataset and settings remembered
    boxMap5095T=metrics.box.map
    boxMap50T=metrics.box.map50
    boxMap75T=metrics.box.map75
    print("mAP50-95 Train: " + str(boxMap5095T)+ " mAP50-95 Val: " + str(boxMap5095Val))
    print("mAP50 Train: " + str(boxMap50T)+ " mAP50 Val: " + str(boxMap50Val))
    print("mAP75 Train: " + str(boxMap75T)+ " mAP75 Val: " + str(boxMap75Val))

if __name__ == '__main__':
    main()
