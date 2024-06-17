from ultralytics import YOLO
# Load a model
model = YOLO("yolov8s.yaml")  # build a new model from scratch
# model = YOLO("yolov8s.pt")  # entrenar modelo pre-entrenado
model = YOLO("EntrenarYolov8\SantaIsabel.pt")  # load a pretrained model (recommended for training)
model = YOLO("yolov8n.yaml").load("EntrenarYolov8\SantaIsabel.pt")  # build from YAML and transfer weights
# Use the model
# pretrained = false CAMBIAR SI RE ENTRENO EL V8
# device = 0 GPU
# cache = True da acceso a la RAM
# patience indica cuando parar si no esta mejorando
model.train(data="EntrenarYolov8\config.yaml",device='cuda',cache= True, epochs=600, patience = 50)  # train the model
# model.train(data="C:\\Users\\Manuel\\Desktop\\Carpeta Visual\\EntrenarYolov8\\config.yaml", epochs=300)  # train the model
