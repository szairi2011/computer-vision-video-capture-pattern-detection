"""Object detection using YOLOv8 with functional patterns."""

import cv2
from dataclasses import dataclass  # Auto-generates __init__, __repr__, __eq__ methods
from typing import Optional  # Optional[T] = Union[T, None] - value can be T or None
from ultralytics import YOLO
import numpy as np


# @dataclass: Decorator that auto-generates boilerplate code for data-holding classes
# Why: Eliminates manual __init__, __repr__, __eq__ methods, reducing code by ~10 lines
# Result: Cleaner, more maintainable code focused on data structure
@dataclass
class Detection:
    """Detection result with bounding box and metadata."""
    bbox: tuple[int, int, int, int]  # Bounding box: (x1, y1, x2, y2) top-left and bottom-right
    label: str  # Object class name (e.g., "apple", "banana")
    confidence: float  # Detection confidence score (0.0 to 1.0)


class FruitDetector:
    """YOLOv8-based fruit detector with configurable classes."""
    
    def __init__(
        self,
        model_name: str = 'yolov8n.pt',
        classes: Optional[list[str]] = None,  # Optional means: can be list[str] OR None
        conf_threshold: float = 0.3
    ):
        self.model = YOLO(model_name)
        self.classes = classes  # None = detect all classes, list = filter specific classes
        self.conf_threshold = conf_threshold
    
    # __call__: Makes class instance callable like a function
    # Why: Allows detector(frame) instead of detector.detect(frame)
    # Pattern: Common in ML/AI for model inference (e.g., PyTorch, sklearn)
    def __call__(self, frame: np.ndarray) -> list[Detection]:
        """Detect objects in frame (callable pattern)."""
        return self.detect(frame)
    
    def detect(self, frame: np.ndarray) -> list[Detection]:
        """Run detection on a single frame."""
        results = self.model(frame, conf=self.conf_threshold, verbose=False)
        detections = []
        
        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls[0])
                label = self.model.names[cls_id]
                
                # Filter by class if specified
                if self.classes and label not in self.classes:
                    continue
                
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                confidence = float(box.conf[0])
                
                detections.append(Detection(
                    bbox=(x1, y1, x2, y2),
                    label=label,
                    confidence=confidence
                ))
        
        return detections


def detect_objects(
    frame: np.ndarray,
    detector: FruitDetector
) -> list[Detection]:
    """Functional wrapper for detection."""
    return detector.detect(frame)


def draw_detections(frame: np.ndarray, detections: list[Detection]) -> np.ndarray:
    """Draw bounding boxes on frame (pure function)."""
    annotated = frame.copy()
    
    for det in detections:
        x1, y1, x2, y2 = det.bbox
        label_text = f"{det.label} {det.confidence:.2f}"
        
        # Draw box and label
        cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(
            annotated, label_text, (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2
        )
    
    return annotated
