
# Import OpenCV for video capture and writing
import cv2

# Import argparse for command-line argument parsing
import argparse
# Import os for file and directory operations
import os


def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Capture video from local or IP camera.")
    # --source: camera index or URL (e.g. --source http://webcam.anklam.de/axis-cgi/mjpg/video.cgi), --output: output file path, --duration: capture duration
    parser.add_argument('--source', type=str, required=True, help='Camera source: 0 for local webcam, or RTSP/HTTP URL for IP camera')
    parser.add_argument('--output', type=str, default='output/output.avi', help='Output video file path')
    parser.add_argument('--duration', type=int, default=10, help='Duration to capture in seconds (default: 10)')

    args = parser.parse_args()

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(args.output), exist_ok=True)


    # If the source is a digit, treat it as a webcam index (e.g., 0 for default webcam)
    source = int(args.source) if args.source.isdigit() else args.source
    # Open the video capture (webcam or IP camera)
    cap = cv2.VideoCapture(source)


    # Check if the camera opened successfully
    if not cap.isOpened():
        print(f"Error: Cannot open camera source {args.source}")
        return

    # Get video properties (frames per second, width, height)
    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0  # Default to 25 FPS if not available
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # Define the codec and create VideoWriter object to save the video
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(args.output, fourcc, fps, (width, height))

    print(f"Capturing from {args.source} to {args.output} for {args.duration} seconds...")
    frame_count = 0
    max_frames = int(fps * args.duration)  # Calculate the maximum number of frames to capture


    # Main loop to read frames from the camera
    while cap.isOpened() and frame_count < max_frames:
        ret, frame = cap.read()  # Read a frame
        if not ret:
            print("Failed to grab frame.")
            break
        out.write(frame)  # Write the frame to the output file
        cv2.imshow('Camera', frame)  # Display the frame in a window
        # Exit if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        frame_count += 1

    # Release resources
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print("Capture finished.")

# Run the main function if this script is executed directly
if __name__ == "__main__":
    main()
