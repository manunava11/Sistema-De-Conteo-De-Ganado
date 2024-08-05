from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import UploadedVideo, CowCount
from django.utils import timezone
import cv2
import os
from ultralytics import YOLO, solutions
import torch
#from celery_progress.backend import ProgressRecorder

@shared_task
def process_video(video_id, cow_count_id):
    #progress_recorder = ProgressRecorder(self)
    
    # Fetch the video and cow count from the database
    video = UploadedVideo.objects.get(id=video_id)
    cow_count = CowCount.objects.get(id=cow_count_id)
    video_input_path = video.uploaded_video.path
    output_folder = os.path.dirname(video_input_path)

    # Check if CUDA is available
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Using device: {device}")

    # Load the model
    model = YOLO('/app/model/cattle_v8x.pt').to(device)

    # Open the video
    cap = cv2.VideoCapture(video_input_path)
    assert cap.isOpened(), "Error reading video file"

    # Get video properties
    w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

    # Define region points
    region_points = [(0, 0), (0, h), (w, h), (w, 0)]

    # Name of the resulting video
    video_name = os.path.basename(video_input_path)
    output_video_name = "Conteo_Resultante_" + video_name
    track_buffer = 300  # 10 seconds

    # Initialize video writer
    output_video_path = os.path.join(output_folder, output_video_name)
    video_writer = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

    # Initialize object counter
    counter = solutions.ObjectCounter(
        view_img=False,
        reg_pts=region_points,
        names=model.names,
        draw_tracks=False,
        line_thickness=2,
        track_thickness=2,
        view_out_counts=False,
        view_in_counts=False,
        count_reg_color=(0, 255, 0),
        region_thickness=0,
    )

    # Total object count
    total_count = 0

    # Process the video
    while cap.isOpened():
        success, im0 = cap.read()
        if not success:
            print("Video frame is empty or video processing has been successfully completed.")
            break

        # Perform tracking with the model
        tracks = model.track(im0, persist=True, show=False, conf=0.7, iou=0.4, tracker="bytetrack.yaml")

        # Count objects in the frame
        current_count = counter.start_counting(im0, tracks)
        total_count = counter.in_counts + counter.out_counts
        text = f'Conteo total: {total_count}'
        cv2.putText(im0, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        # Write the processed frame to the output video
        video_writer.write(im0)

        #progress_recorder.set_progress()

    # Release resources
    cap.release()
    video_writer.release()
    cv2.destroyAllWindows()

    total_count = counter.in_counts + counter.out_counts
    print(f"Proceso completado. Total de vacas: {total_count}. Video de salida generado como '{output_video_name}' en la carpeta deseada.")

    # Save the processed video and count to the database
    video.processed_video.name = output_video_path
    video.cow_count.cow_count = total_count
    video.processed_at = timezone.now()
    video.save()
    video.cow_count.save()