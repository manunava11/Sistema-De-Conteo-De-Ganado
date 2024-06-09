from ultralytics import YOLO

# Load a model
model = YOLO("yolov8s.yaml")  # build a new model from scratch
# model = YOLO("yolov8s.pt")  # entrenar modelo pre-entrenado
model = YOLO("EntrenarYolov8\SoloDron.pt")  # load a pretrained model (recommended for training)

# Use the model
model.train(data="EntrenarYolov8\config.yaml", epochs=400)  # train the model
# model.train(data="C:\\Users\\Manuel\\Desktop\\Carpeta Visual\\EntrenarYolov8\\config.yaml", epochs=300)  # train the model
