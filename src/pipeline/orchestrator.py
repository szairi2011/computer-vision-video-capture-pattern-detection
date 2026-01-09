"""End-to-end pipeline orchestration for fruit quality detection."""

import cv2
import asyncio
from typing import Optional
from dataclasses import dataclass

from ..vision.capture import stream_frames
from ..vision.detect import FruitDetector, draw_detections
from ..quality.score import assess_freshness
from ..events.publisher import EventPublisher, create_quality_event
from ..search.indexer import SearchRepository, create_fruit_document
from .decorators import timer, log_execution


@dataclass
class PipelineConfig:
    """Configuration for processing pipeline."""
    source: str
    output_path: Optional[str] = None
    max_frames: int = 0
    detector_conf: float = 0.3
    enable_events: bool = False
    enable_search: bool = False
    display: bool = True


@timer
@log_execution
def process_shelf_video(config: PipelineConfig) -> dict:
    """
    End-to-end processing pipeline.
    
    Pipeline steps:
    1. Stream video frames
    2. Detect fruits with YOLO
    3. Assess quality for each detection
    4. Publish events to Event Hub
    5. Index results in AI Search
    6. Display/save annotated video
    
    Args:
        config: Pipeline configuration
        
    Returns:
        Processing statistics
    """
    # Initialize components
    detector = FruitDetector(conf_threshold=config.detector_conf)
    event_publisher = EventPublisher() if config.enable_events else None
    search_repo = SearchRepository() if config.enable_search else None
    
    stats = {
        'frames_processed': 0,
        'detections': 0,
        'events_published': 0,
        'documents_indexed': 0
    }
    
    try:
        for success, frame in stream_frames(config.source, config.max_frames):
            if not success:
                break
            
            # Detect fruits in frame
            detections = detector.detect(frame)
            stats['detections'] += len(detections)
            
            # Process each detection
            for det in detections:
                # Assess quality
                quality = assess_freshness(frame, det.bbox, det.label)
                
                # Publish event asynchronously
                if event_publisher:
                    event = create_quality_event(
                        fruit_type=det.label,
                        freshness_level=quality.freshness_level.value,
                        quality_score=quality.score,
                        confidence=det.confidence
                    )
                    asyncio.run(event_publisher.publish(event))
                    stats['events_published'] += 1
                
                # Index in AI Search
                if search_repo:
                    document = create_fruit_document(
                        fruit_type=det.label,
                        freshness_level=quality.freshness_level.value,
                        quality_score=quality.score,
                        confidence=det.confidence
                    )
                    search_repo.index_document(document)
                    stats['documents_indexed'] += 1
            
            # Annotate frame
            annotated = draw_detections(frame, detections)
            
            # Display or save
            if config.display:
                cv2.imshow('Fruit Quality Detection', annotated)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            # TODO: Add video writer if output_path specified
            
            stats['frames_processed'] += 1
    
    finally:
        cv2.destroyAllWindows()
        if event_publisher:
            asyncio.run(event_publisher.close())
    
    return stats
