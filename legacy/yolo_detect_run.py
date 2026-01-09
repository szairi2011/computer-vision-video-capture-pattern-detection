import cv2
import argparse
import os
from yolo_detect import YOLODetector

def main():
    parser = argparse.ArgumentParser(description="YOLOv8 Object Detection on video stream or file.")
    parser.add_argument('--source', type=str, required=True, help='Camera index, video file, or stream URL')
    parser.add_argument('--output', type=str, default=None, help='Optional output video file path')
    parser.add_argument('--duration', type=int, default=0, help='Duration to process in seconds (0 = unlimited)')
    parser.add_argument('--yolo-classes', type=str, default=None, help='Comma-separated list of YOLO classes to detect (default: all)')
    parser.add_argument('--conf', type=float, default=0.3, help='YOLO confidence threshold (default: 0.3)')
    args = parser.parse_args()

    source = int(args.source) if args.source.isdigit() else args.source
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        print(f"Error: Cannot open source {args.source}")
        return

    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = None
    if args.output:
        os.makedirs(os.path.dirname(args.output), exist_ok=True)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(args.output, fourcc, fps, (width, height))

    yolo_classes = [c.strip() for c in args.yolo_classes.split(',')] if args.yolo_classes else None
    detector = YOLODetector(classes=yolo_classes, conf=args.conf)

    frame_count = 0
    max_frames = int(fps * args.duration) if args.duration > 0 else float('inf')

    while cap.isOpened() and frame_count < max_frames:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break
        boxes = detector.detect(frame)
        frame = YOLODetector.draw_boxes(frame, boxes)
        if out:
            out.write(frame)
        cv2.imshow('YOLO Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        frame_count += 1

    cap.release()
    if out:
        out.release()
    cv2.destroyAllWindows()
    print("Detection finished.")

if __name__ == "__main__":
    main()
