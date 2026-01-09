"""Video capture with generator pattern for frame streaming."""

import cv2
# Union[A, B]: Type can be either A or B (e.g., Union[int, str] = int OR str)
# Why: Allows function to accept multiple types without overloading
from typing import Generator, Union
from contextlib import contextmanager  # Decorator for creating context managers (with statements)


# Generator: Function that yields values instead of returning (memory efficient)
# Why: Streams frames one-by-one without loading entire video into memory
# Pattern: Ideal for processing large/infinite streams (e.g., camera feeds)
def stream_frames(
    source: Union[int, str],  # Union = can be int (camera index) OR str (file/URL)
    max_frames: int = 0  # 0 means unlimited (stream until user stops)
) -> Generator[tuple[bool, any], None, None]:  # Generator[YieldType, SendType, ReturnType]
    """
    Stream video frames from camera or file.
    
    Args:
        source: Camera index (int) or video file/stream URL (str)
        max_frames: Maximum frames to capture (0 = unlimited)
    
    Yields:
        (success, frame) tuples
    """
    cap = cv2.VideoCapture(source)
    
    if not cap.isOpened():
        raise ValueError(f"Cannot open video source: {source}")
    
    try:
        frame_count = 0
        while cap.isOpened():
            if max_frames > 0 and frame_count >= max_frames:
                break
                
            ret, frame = cap.read()
            if not ret:
                break
                
            yield ret, frame
            frame_count += 1
    finally:
        cap.release()


# @contextmanager: Decorator that turns generator into context manager
# Why: Enables 'with' statement usage for automatic resource cleanup
# Pattern: Ensures resources (files, connections) are always released, even on errors
@contextmanager
def video_writer(output_path: str, fps: float, width: int, height: int):
    """Context manager for video writing."""
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Video codec (XVID = compressed AVI)
    writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    try:
        yield writer  # Yield = return value to 'with' block, then resume here after block
    finally:
        writer.release()  # Always executes, even if error occurs in 'with' block


def get_video_props(source: Union[int, str]) -> dict:
    """Extract video properties (fps, width, height)."""
    cap = cv2.VideoCapture(source)
    
    if not cap.isOpened():
        raise ValueError(f"Cannot open video source: {source}")
    
    props = {
        'fps': cap.get(cv2.CAP_PROP_FPS) or 25.0,
        'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    }
    
    cap.release()
    return props
