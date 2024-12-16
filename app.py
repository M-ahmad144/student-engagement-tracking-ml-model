from flask import Flask, request, jsonify
import os
import shutil  # To delete directories
from capture import extract_frames, analyze_extracted_frames
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173", "https://engageify.vercel.app"])

# Global variable to store engagement results temporarily
engagement_results = {}


@app.route("/upload", methods=["POST"])
def upload_video():
    """
    Handle video upload, processing, and cleanup of temporary files.
    """
    if "video" not in request.files:
        return jsonify({"error": "No file part"}), 400

    video_file = request.files["video"]
    if video_file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # Ensure the file is a valid video format (e.g., mp4)
    if not video_file.filename.lower().endswith((".mp4", ".avi", ".mov")):
        return (
            jsonify({"error": "Invalid file type. Only .mp4, .avi, .mov are allowed."}),
            400,
        )

    try:
        # Save the uploaded video file
        upload_folder = "uploads"
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        video_path = os.path.join(upload_folder, video_file.filename)
        video_file.save(video_path)

        # Create a folder for the extracted frames
        extracted_frames_folder = "extracted_frames"
        if not os.path.exists(extracted_frames_folder):
            os.makedirs(extracted_frames_folder)

        # Extract frames from the video
        extract_frames(video_path, extracted_frames_folder)

        # Analyze the extracted frames and store the results
        global engagement_results
        engagement_results = analyze_extracted_frames(extracted_frames_folder)

        # Clean up: Remove the video file and extracted frames folder
        if os.path.exists(video_path):
            os.remove(video_path)  # Delete the uploaded video
        if os.path.exists(extracted_frames_folder):
            shutil.rmtree(extracted_frames_folder)  # Delete extracted frames folder

        print("Engagement results after processing:", engagement_results)
        return jsonify(
            {
                "message": "Video uploaded, processed successfully, and cleaned up.",
                "video_name": video_file.filename,
            }
        )

    except Exception as e:
        return jsonify({"error": f"An error occurred during processing: {str(e)}"}), 500


@app.route("/analysis-result", methods=["GET"])
def get_analysis_result():
    """
    Fetch the analysis results for a specific video.
    """
    video_name = request.args.get("video_name")

    if not video_name:
        return jsonify({"error": "Video name is required."}), 400

    if not engagement_results:
        return jsonify({"error": "No analysis results available."}), 404

    return jsonify({"video_name": video_name, "engagement_results": engagement_results})


if __name__ == "__main__":
    # Ensure necessary directories exist
    if not os.path.exists("uploads"):
        os.makedirs("uploads")

    app.run(debug=True)
