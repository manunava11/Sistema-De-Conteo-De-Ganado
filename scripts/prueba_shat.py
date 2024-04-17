import cv2
import numpy as np

def load_yolov8():
    # Make sure you have yolov8.weights, yolov8.cfg, and yolov8.names in the 'yolov8' folder
    weights_path = "yolov8/yolov8.weights"
    config_path = "yolov8/yolov8.cfg"
    names_path = "yolov8/yolov8.names"

    net = cv2.dnn.readNet(weights_path, config_path)
    classes = []
    with open(names_path, "r") as f:
        classes = [line.strip() for line in f.readlines()]
    output_layers = net.getUnconnectedOutLayersNames()

    return net, classes, output_layers

def detect_objects(frame, net, output_layers):
    height, width, channels = frame.shape
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    class_ids = []
    confidences = []
    boxes = []

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])

    return class_ids, confidences, boxes

def draw_boxes(frame, class_ids, confidences, boxes, classes):
    font = cv2.FONT_HERSHEY_PLAIN
    colors = np.random.uniform(0, 255, size=(len(classes), 3))

    for i in range(len(boxes)):
        x, y, w, h = boxes[i]
        label = str(classes[class_ids[i]])
        color = colors[i]
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        cv2.putText(frame, label, (x, y - 5), font, 1, color, 1)

def main():
    net, classes, output_layers = load_yolov8()

    # Load the input image
    input_file = '/Users/ramirososa/Desktop/pruebashat.png'  # Change this to your input image
    frame = cv2.imread(input_file)

    class_ids, confidences, boxes = detect_objects(frame, net, output_layers)
    draw_boxes(frame, class_ids, confidences, boxes, classes)

    # Display the image with bounding boxes
    cv2.imshow("Object Detection", frame)
    
    # Save the image with bounding boxes
    output_file = '/Users/ramirososa/Desktop/resultadoshat.png'  # Change this to your desired output image
    cv2.imwrite(output_file, frame)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
