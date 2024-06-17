from ultralytics import YOLO
import torch

def main():
    # Verificación de disponibilidad de CUDA
    print("Is CUDA available: ", torch.cuda.is_available())
    print("Number of GPUs: ", torch.cuda.device_count())
    print("CUDA version: ", torch.version.cuda)
    if torch.cuda.is_available():
        print("GPU Name: ", torch.cuda.get_device_name(0))
    else:
        print("No CUDA GPUs are available")

    # Entrenamiento del modelo
    try:
        model = YOLO("yolov8s.yaml").load("EntrenarYolov8\SantaIsabel.pt")  # build from YAML and transfer weights
        model.train(data=r"EntrenarYolov8\config.yaml", device='cuda', cache=True, epochs=600, patience=50)
    except Exception as e:
        print(f"Error during training: {e}")

if __name__ == '__main__':
    main()
