"""Tests for quality module."""

import pytest
import numpy as np
from src.quality.score import assess_freshness, FreshnessLevel, QualityScore


def test_assess_freshness_returns_score():
    """Test that freshness assessment returns QualityScore."""
    frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    bbox = (100, 100, 200, 200)
    
    score = assess_freshness(frame, bbox, "apple")
    
    assert isinstance(score, QualityScore)
    assert isinstance(score.freshness_level, FreshnessLevel)
    assert 0 <= score.score <= 100
    assert 0 <= score.confidence <= 1


def test_assess_freshness_empty_bbox():
    """Test handling of invalid bounding box."""
    frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    bbox = (100, 100, 100, 100)  # Zero-size box
    
    score = assess_freshness(frame, bbox)
    
    assert score.score == 50.0  # Default score
    assert score.confidence == 0.0
