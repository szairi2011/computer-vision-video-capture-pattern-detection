"""Tests for vision module."""

import pytest
import cv2
import numpy as np
from src.vision.capture import stream_frames, get_video_props
from src.vision.detect import FruitDetector, Detection, draw_detections


def test_stream_frames_with_limit():
    """Test frame streaming with max_frames limit."""
    frames = list(stream_frames(0, max_frames=5))
    assert len(frames) <= 5


def test_fruit_detector_initialization():
    """Test detector initialization."""
    detector = FruitDetector(conf_threshold=0.5)
    assert detector.conf_threshold == 0.5


def test_draw_detections():
    """Test drawing bounding boxes."""
    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    detections = [
        Detection(bbox=(10, 10, 100, 100), label="apple", confidence=0.9)
    ]
    
    annotated = draw_detections(frame, detections)
    assert annotated.shape == frame.shape
    assert not np.array_equal(annotated, frame)  # Should be different
