import cv2
import numpy as np
import os
from tensorflow.keras.models import load_model
from datetime import datetime

# Load the engagement detection model
cnn_model = load_model("./model/engagement-model.h5")  # Load your CNN model here


def preprocess_frame(frame):
    """
    Preprocess the video frame for engagement detection (resize, grayscale, etc.)

    Args:
        frame (numpy.ndarray): The input video frame in BGR format.

    Returns:
        numpy.ndarray: The preprocessed frame, converted to grayscale, resized to 48x48,
                       and normalized to have pixel values in the range [0, 1].
    """
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    resized_frame = cv2.resize(gray_frame, (48, 48))
    return resized_frame / 255.0  # Normalize


def analyze_engagement(frame):
    """
    Analyze the given video frame to predict the engagement status of the person in it.

    Args:
        frame (numpy.ndarray): The input video frame in BGR format.

    Returns:
        str: The predicted engagement status, either "Engaged" or "Distracted".
    """
    processed_frame = preprocess_frame(frame)
    prediction = cnn_model.predict(np.expand_dims(processed_frame, axis=0))

    # Access the prediction value correctly
    # Assuming the output is a single scalar value representing the probability
    engagement_status = "Engaged" if prediction[0][0] > 0.5 else "Distracted"

    return engagement_status


def analyze_extracted_frames(extracted_frames_folder):
    """
    Analyze all the extracted frames from the provided folder and predict their engagement status.

    Args:
        extracted_frames_folder (str): Path to the folder containing extracted frames (images).

    Returns:
        None
    """
    # Get the list of images in the extracted frames folder
    frame_files = [f for f in os.listdir(extracted_frames_folder) if f.endswith(".jpg")]

    if not frame_files:
        print("No images found in the provided folder.")
        return

    # Sort the images to ensure they're in the correct order
    frame_files.sort()

    # Counters for engagement analysis
    total_frames = 0
    engaged_frames = 0

    # Iterate through each image, analyze it, and print the engagement status
    for frame_file in frame_files:
        frame_path = os.path.join(extracted_frames_folder, frame_file)

        # Load the image
        frame = cv2.imread(frame_path)
        if frame is None:
            continue

        # Analyze the engagement status of the frame
        engagement_status = analyze_engagement(frame)

        # Increment counters
        total_frames += 1
        if engagement_status == "Engaged":
            engaged_frames += 1

        # Print engagement status for each frame
        print(f"Frame: {frame_file} - Engagement Status: {engagement_status}")

    # Calculate and print engagement percentage
    if total_frames > 0:
        engagement_percentage = (engaged_frames / total_frames) * 100
        print(f"\nTotal Frames Analyzed: {total_frames}")
        print(f"Engaged Frames: {engaged_frames}")
        print(f"Engagement Percentage: {engagement_percentage:.2f}%")
    else:
        print("No valid frames were analyzed.")


if __name__ == "__main__":
    # Path to the extracted frames folder
    extracted_frames_folder = "extracted_frames"  # Replace with your folder path

    # Start analyzing the frames
    analyze_extracted_frames(extracted_frames_folder)
