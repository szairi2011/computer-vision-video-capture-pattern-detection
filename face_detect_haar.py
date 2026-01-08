import cv2
import argparse

# Load the pre-trained Haar cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def main():
    parser = argparse.ArgumentParser(description="Simple face detection using Haar cascades.")
    parser.add_argument('--source', type=str, required=True, help='Camera source: 0 for local webcam, or video file path')
    args = parser.parse_args()

    # Handle integer source for local webcam
    source = int(args.source) if args.source.isdigit() else args.source
    cap = cv2.VideoCapture(source, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print(f"Error: Cannot open camera source {args.source}")
        return

    print(f"Press 'q' to quit.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break
        # Convert to grayscale for Haar cascade
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Detect faces
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))
        # Draw rectangles around detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imshow('Face Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
