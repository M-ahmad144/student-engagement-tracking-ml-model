import cv2
import os


def extract_frames(video_path, output_folder, frame_step=2):
    # Open the video using OpenCV
    cap = cv2.VideoCapture(video_path)

    # Check if the video file is opened successfully
    if not cap.isOpened():
        print(f"Error: Could not open video {video_path}")
        return

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    frame_count = 0
    saved_count = 0
    while True:
        # Read the next frame
        ret, frame = cap.read()

        if not ret:
            break  # Exit loop when no more frames

        # Save every 'frame_step' frames (i.e., skip frames)
        if frame_count % frame_step == 0:
            # Construct the filename for the extracted frame
            frame_filename = os.path.join(output_folder, f"frame_{saved_count:04d}.jpg")

            # Save the frame as a JPG image
            cv2.imwrite(frame_filename, frame)

            saved_count += 1

        frame_count += 1
        print(f"Processed frame {frame_count}", end="\r")

    # Release the video capture object
    cap.release()

    print(f"\nFrame extraction complete. {saved_count} frames saved to {output_folder}")


# Example usage
if __name__ == "__main__":
    video_path = r"F:\U n i v e r s i t y\5TH - S E M E S T E R\AI\Artificial - Intellligennce\student-engagemnet-tracking-application\student-engagement-tracking\backend\data\Video\WIN_20241214_13_26_15_Pro.mp4"
    output_folder = r"F:\U n i v e r s i t y\5TH - S E M E S T E R\AI\Artificial - Intellligennce\student-engagemnet-tracking-application\student-engagement-tracking\backend\data\engangement dataset\test\lookingAwayFromCamera"

    extract_frames(video_path, output_folder)
