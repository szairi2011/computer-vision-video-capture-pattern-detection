"""
Video stream simulator for offline testing.

This module provides TWO separate utilities:
1. VideoStreamSimulator - Loops existing video files as live streams (REQUIRES VIDEO)
2. generate_test_video() - Creates synthetic test videos from scratch (NO INPUT NEEDED)

Usage:
    # Generate synthetic video (no input needed):
    python -m src.utils.video_simulator generate --duration 30
    
    # Loop existing video as stream (requires video file):
    python -m src.utils.video_simulator stream my_video.mp4 --loop
"""

import cv2
import time
from pathlib import Path
from typing import Optional
import argparse


class VideoStreamSimulator:
    """
    Simulates live camera stream by looping an EXISTING video file.
    
    ⚠️ NOTE: This class REQUIRES an existing video file as input.
    To create a synthetic video from scratch, use generate_test_video() instead.
    
    Use Case: Make recorded video behave like live camera feed (loop infinitely).
    """
    
    def __init__(self, video_path: str, loop: bool = True, fps_override: Optional[float] = None):
        """
        Initialize video stream simulator.
        
        Args:
            video_path: Path to video file
            loop: Whether to loop video infinitely
            fps_override: Override video FPS (None = use original)
        """
        self.video_path = Path(video_path)
        self.loop = loop
        self.fps_override = fps_override
        
        if not self.video_path.exists():
            raise FileNotFoundError(f"Video not found: {video_path}")
        
        self.cap = cv2.VideoCapture(str(self.video_path))
        self.original_fps = self.cap.get(cv2.CAP_PROP_FPS) or 25.0
        self.fps = fps_override or self.original_fps
        self.frame_delay = 1.0 / self.fps  # Delay between frames in seconds
    
    def stream(self):
        """
        Stream video frames with realistic timing.
        
        Yields:
            Frames from video file
        """
        frame_count = 0
        
        while True:
            ret, frame = self.cap.read()
            
            if not ret:
                if not self.loop:
                    break
                
                # Reset to beginning for loop
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                frame_count = 0
                continue
            
            # Simulate real-time streaming with delay
            time.sleep(self.frame_delay)
            
            frame_count += 1
            yield frame
    
    def close(self):
        """Release video capture."""
        self.cap.release()


def generate_test_video(
    output_path: str = "data/samples/test_shelf.avi",
    duration: int = 10,
    width: int = 640,
    height: int = 480,
    fps: float = 25.0
):
    """
    Generate synthetic test video with moving shapes FROM SCRATCH.
    
    ✅ NO INPUT VIDEO REQUIRED - Creates video programmatically using OpenCV.
    
    ⚠️ LIMITATION: Creates simple geometric shapes (circles), NOT realistic fruit imagery.
    
    Use Cases:
    - Testing pipeline mechanics (video I/O, frame processing, encoding)
    - Verifying detection code runs without errors
    - Quick smoke tests without downloads
    
    NOT suitable for:
    - Testing actual fruit detection accuracy
    - Quality assessment algorithm validation
    - Realistic demos for customers
    
    For realistic fruit testing, use:
    - Download real fruit videos (YouTube, Kaggle datasets)
    - Record your own shelf videos with webcam
    - Use public IP camera streams
    
    See: docs/execution_guide.md#offline-development-mode
    
    Args:
        output_path: Output video file path
        duration: Video duration in seconds
        width: Frame width
        height: Frame height
        fps: Frames per second
    """
    import numpy as np
    
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    total_frames = int(fps * duration)
    
    for i in range(total_frames):
        # Create frame with gradient background
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        frame[:, :] = [50 + i % 50, 100, 150]
        
        # Add moving circle (simulates fruit)
        x = int((width / 2) + 100 * np.sin(i / 10))
        y = int((height / 2) + 100 * np.cos(i / 10))
        cv2.circle(frame, (x, y), 30, (0, 255, 0), -1)
        
        # Add timestamp text
        cv2.putText(
            frame, f"Frame {i}/{total_frames}", (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2
        )
        
        writer.write(frame)
    
    writer.release()
    print(f"Generated test video: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Video stream simulator utilities")
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Simulate stream command
    stream_parser = subparsers.add_parser('stream', help='Simulate video stream')
    stream_parser.add_argument('video', help='Path to video file')
    stream_parser.add_argument('--loop', action='store_true', help='Loop video infinitely')
    stream_parser.add_argument('--fps', type=float, help='Override FPS')
    
    # Generate test video command
    gen_parser = subparsers.add_parser('generate', help='Generate synthetic test video')
    gen_parser.add_argument('--output', default='data/samples/test_shelf.avi', help='Output path')
    gen_parser.add_argument('--duration', type=int, default=10, help='Duration in seconds')
    
    args = parser.parse_args()
    
    if args.command == 'stream':
        simulator = VideoStreamSimulator(args.video, loop=args.loop, fps_override=args.fps)
        
        print(f"Streaming video: {args.video}")
        print("Press 'q' to quit")
        
        try:
            for frame in simulator.stream():
                cv2.imshow('Simulated Stream', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        finally:
            simulator.close()
            cv2.destroyAllWindows()
    
    elif args.command == 'generate':
        generate_test_video(
            output_path=args.output,
            duration=args.duration
        )
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
