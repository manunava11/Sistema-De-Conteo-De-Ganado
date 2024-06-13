from ultralytics import YOLO
# Load a model
model = YOLO("yolov8s.yaml")  # build a new model from scratch
# model = YOLO("yolov10s.yaml")  # build a new model from scratch
# model = YOLO("yolov8s.pt")  # entrenar modelo pre-entrenado
model = YOLO("EntrenarYolov8\SantaIsabel.pt")  # load a pretrained model (recommended for training)

# Use the model
# pretrained = false CAMBIAR SI RE ENTRENO EL V8
# device = 0 GPU
# cache = True da acceso a la RAM
# patience indica cuando parar si no esta mejorando
model.train(data="EntrenarYolov8\config.yaml", epochs=400, device=0, cache =True, patience = 50)  # train the model
# model.train(data="C:\\Users\\Manuel\\Desktop\\Carpeta Visual\\EntrenarYolov8\\config.yaml", epochs=300)  # train the model
