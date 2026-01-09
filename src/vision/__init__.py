"""Vision module - Video capture and object detection."""

from .capture import stream_frames
from .detect import detect_objects, FruitDetector

__all__ = ["stream_frames", "detect_objects", "FruitDetector"]
