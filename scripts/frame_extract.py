import cv2
import os

def extract_frames(video_path, output_folder, cow_id):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Get frames per second (fps) and frame count
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    print(f"Vaca Nro {cow_id}:")
    print(f"Frames per second: {fps}")
    print(f"Frame count: {frame_count}")
    #counter_frames=0
    # Loop through each frame and save it as an image
    for i in range(frame_count):
        ret, frame = cap.read()
        if not ret:
            break
        if i % 3 == 0:
        #    counter_frames+=1
            frame_filename = os.path.join(output_folder, f"manchega_lat_{cow_id}_{i//3}.png")
            cv2.imwrite(frame_filename, frame)

    # Release the video capture object
    cap.release()

if __name__ == "__main__":
    for elem in range(1, 132):
        video_path = f"/Users/ramirososa/Desktop/Videos procesados (lateral)/Vaca {elem}.mp4"
        output_folder = f"/Users/ramirososa/Desktop/Frames Lateral/manchega_lat_{elem}"
        extract_frames(video_path, output_folder, elem)
