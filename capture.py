import os
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from datetime import datetime

# Load the engagement detection model
cnn_model = load_model("./engagement-model01.h5")  # Path to your trained model


def preprocess_frame(frame):
    """
    Preprocess the video frame for engagement detection (resize, grayscale, etc.)
    """
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    resized_frame = cv2.resize(gray_frame, (48, 48))
    return resized_frame / 255.0  # Normalize


def analyze_engagement(frame):
    """
    Analyze the given video frame to predict the engagement status of the person in it.
    """
    processed_frame = preprocess_frame(frame)
    prediction = cnn_model.predict(np.expand_dims(processed_frame, axis=0))

    # Assuming the model's output is a binary classification: "Engaged" or "Distracted"
    engagement_status = "Engaged" if prediction[0][0] > 0.5 else "Distracted"

    return engagement_status


def extract_frames(video_path, output_folder, interval=5, resize_factor=0.5):
    """
    Extract frames from the video at a given interval and save them in the specified folder.
    """
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps * interval)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    saved_frame_count = 0

    for frame_num in range(0, total_frames, frame_interval):
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        ret, frame = cap.read()
        if not ret:
            break

        if resize_factor != 1:
            frame = cv2.resize(frame, (0, 0), fx=resize_factor, fy=resize_factor)

        frame_filename = os.path.join(
            output_folder, f"frame_{saved_frame_count + 1}.jpg"
        )
        cv2.imwrite(frame_filename, frame)
        saved_frame_count += 1

    cap.release()


def analyze_extracted_frames(extracted_frames_folder):
    """
    Analyze all the extracted frames and predict their engagement status.
    """
    frame_files = [f for f in os.listdir(extracted_frames_folder) if f.endswith(".jpg")]
    if not frame_files:
        return []

    frame_files.sort()
    engagement_results = []

    for frame_file in frame_files:
        frame_path = os.path.join(extracted_frames_folder, frame_file)
        frame = cv2.imread(frame_path)
        if frame is None:
            continue

        engagement_status = analyze_engagement(frame)
        engagement_results.append(
            {"frame": frame_file, "engagement_status": engagement_status}
        )

    return engagement_results
