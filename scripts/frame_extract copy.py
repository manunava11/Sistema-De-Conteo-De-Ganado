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
        #if i % 20 == 0:
        #    counter_frames+=1
        frame_filename = os.path.join(output_folder, f"el_talar_fron_{cow_id}_{i}.png")
        cv2.imwrite(frame_filename, frame)

    # Release the video capture object
    cap.release()

if __name__ == "__main__":
    #for elem in [3,4,5,8,27,39,46,52,61,62,66,70,71,72,73,74,75,76]:
    elem=74
    video_path = f"/Users/ramirososa/Desktop/video_{elem}.mov"
    output_folder = f"/Users/ramirososa/Desktop/frames_nuevo/el_talar_front_{elem}"
    extract_frames(video_path, output_folder, elem)
