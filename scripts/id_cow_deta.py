from transformers import AutoImageProcessor, DetaForObjectDetection
from PIL import Image
import torch
import cv2

cap = cv2.VideoCapture("/Users/ramirososa/Desktop/GitHub/Sistema-De-Conteo-De-Ganado/scripts/prueba2.mp4")

ret, frame = cap.read()
image = Image.fromarray(frame)
image_processor = AutoImageProcessor.from_pretrained("jozhang97/deta-swin-large")
model = DetaForObjectDetection.from_pretrained("jozhang97/deta-swin-large")

inputs = image_processor(images=image, return_tensors="pt")
outputs = model(**inputs)

# convert outputs (bounding boxes and class logits) to Pascal VOC format (xmin, ymin, xmax, ymax)
target_sizes = torch.tensor([image.size[::-1]])
results = image_processor.post_process_object_detection(outputs, threshold=0.5, target_sizes=target_sizes)[0]
for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
    box = [round(i, 2) for i in box.tolist()]
    print(
        f"Detected {model.config.id2label[label.item()]} with confidence "
        f"{round(score.item(), 3)} at location {box}"
    )