"""Fruit quality scoring using color and texture analysis."""

import cv2
import numpy as np
from dataclasses import dataclass
# Enum: Creates a set of symbolic names bound to unique constant values
# Why: Type-safe constants, better than strings (no typos, autocomplete works)
from enum import Enum
from typing import Optional


# Enum Pattern: Defines allowed values as named constants
# Why: Prevents invalid values like "freesh" (typo), enables IDE autocomplete
# Alternative to: Using plain strings like "fresh", "medium", "rotten"
class FreshnessLevel(Enum):
    """Freshness levels for fruits."""
    FRESH = "fresh"  # Access via FreshnessLevel.FRESH
    MEDIUM = "medium"
    ROTTEN = "rotten"


# @dataclass: Auto-generates __init__, __repr__, __eq__ for data-holding classes
# Why: Reduces boilerplate, makes data structures explicit and type-safe
@dataclass
class QualityScore:
    """Quality assessment result."""
    freshness_level: FreshnessLevel  # Type hint enforces Enum usage
    score: float  # Overall quality score (0-100, higher = better)
    color_score: float  # Color-based freshness (0-100)
    texture_score: float  # Texture-based freshness (0-100)
    confidence: float  # Model confidence (0.0-1.0)


def assess_freshness(
    frame: np.ndarray,
    bbox: tuple[int, int, int, int],
    fruit_type: Optional[str] = None
) -> QualityScore:
    """
    Assess fruit freshness from image region.
    
    Uses color and texture analysis as proxy for quality.
    In production, replace with trained ML model.
    
    Args:
        frame: Input image
        bbox: Bounding box (x1, y1, x2, y2)
        fruit_type: Type of fruit for specialized scoring
    
    Returns:
        QualityScore with freshness assessment
    """
    x1, y1, x2, y2 = bbox
    roi = frame[y1:y2, x1:x2]
    
    if roi.size == 0:
        return _default_score()
    
    # Color analysis - detect browning/darkening
    color_score = _analyze_color(roi, fruit_type)
    
    # Texture analysis - detect spots/blemishes
    texture_score = _analyze_texture(roi)
    
    # Combined score
    overall_score = (color_score * 0.6) + (texture_score * 0.4)
    
    # Determine freshness level
    if overall_score >= 70:
        level = FreshnessLevel.FRESH
    elif overall_score >= 40:
        level = FreshnessLevel.MEDIUM
    else:
        level = FreshnessLevel.ROTTEN
    
    return QualityScore(
        freshness_level=level,
        score=overall_score,
        color_score=color_score,
        texture_score=texture_score,
        confidence=0.75  # Placeholder - use model confidence in production
    )


def _analyze_color(roi: np.ndarray, fruit_type: Optional[str] = None) -> float:
    """Analyze color distribution (simplified heuristic)."""
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    
    # Calculate mean brightness and saturation
    mean_value = np.mean(hsv[:, :, 2])
    mean_saturation = np.mean(hsv[:, :, 1])
    
    # Simple heuristic: darker/less saturated = worse quality
    brightness_score = (mean_value / 255) * 100
    saturation_score = (mean_saturation / 255) * 100
    
    return (brightness_score + saturation_score) / 2


def _analyze_texture(roi: np.ndarray) -> float:
    """Analyze texture for spots/blemishes."""
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    
    # Calculate variance (high variance = more texture/spots)
    variance = np.var(gray)
    
    # Lower variance often means better quality (smoother surface)
    # Normalize to 0-100 scale (inverse relationship)
    texture_score = max(0, 100 - (variance / 10))
    
    return min(100, texture_score)


def _default_score() -> QualityScore:
    """Return default score for invalid input."""
    return QualityScore(
        freshness_level=FreshnessLevel.MEDIUM,
        score=50.0,
        color_score=50.0,
        texture_score=50.0,
        confidence=0.0
    )
