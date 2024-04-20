from ultralytics import YOLO

# Load a model
model = YOLO("yolov8n.yaml")  # build a new model from scratch
model = YOLO("yolov8n.pt")  # load a pretrained model (recommended for training)

# Use the model
model.train(data="EntrenarYolov8\config.yaml", epochs=300)  # train the model
# C:\Users\Manuel\Desktop\Carpeta Visual\Python\config.yaml
# coco128.yaml