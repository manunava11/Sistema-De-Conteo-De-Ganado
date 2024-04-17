import cv2
from ultralytics import YOLO
import numpy as np
#import torch
import random
import os

# Generate a random integer between a specified range (inclusive)

#print(torch.backends.mps.is_available())
output_folder = "/Users/ramirososa/Desktop/video_1"
cap = cv2.VideoCapture("/Users/ramirososa/Desktop/prueba_corta.mov")
model = YOLO("yolov8m.pt")

def num_check(c,count):
    if count == 1:
        random_number = random.randint(417, 439)
        return f"Peso: {random_number}" 
    elif count ==2:
        random_number = random.randint(507, 525)
        return f"Peso: {random_number}"

def frame_interaction():
    i=0
    while True:
        ret, frame = cap.read()
        height, width, _ = frame.shape
        if not ret:
            break
        i+=1
        results = model(frame,device="mps")
        result = results[0]
        bboxes = np.array(result.boxes.xyxy.cpu(), dtype="int")
        classes = np.array(result.boxes.cls.cpu(), dtype="int")
        cow_count=0
        for cls, bbox in zip(classes,bboxes):
            if cls == 19: # assuming 19 is the class ID for cows
                cow_count += 1
                (x,y,x2,y2) = bbox
                cv2.rectangle(frame,(x,y),(x2,y2),(0,0,225),3)
                cv2.putText(frame,num_check(cls,cow_count),(x,y - 5),0,2,(0,0,225),3)
        cv2.putText(frame,str(f"Vacas detectadas: {cow_count}"),(width - 650,height - 20),0,2,(0,0,225),3)
        print()
        cv2.imshow("Img", frame)
        frame_filename = os.path.join(output_folder, f"frame_{i+1}.png")
        cv2.imwrite(frame_filename, frame)
        key = cv2.waitKey(1)
        if key == 27:
            break


def main():
    frame_interaction()
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()