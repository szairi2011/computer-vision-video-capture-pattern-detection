# System Architecture

Modular architecture for fruits quality detection with Azure cloud integration.

## Table of Contents
- [Overview](#overview)
- [Component Architecture](#component-architecture)
- [Data Flow](#data-flow)
- [Design Patterns](#design-patterns)
- [Scalability Considerations](#scalability-considerations)
- [Azure Integration](#azure-integration)

## Overview

The system follows a modular, event-driven architecture designed for scalability and maintainability. Each component has a single responsibility and can be scaled independently.

## Component Architecture

### 1. Vision Module (`src/vision/`)

**Purpose:** Video capture and object detection

**Components:**
- `capture.py` - Frame streaming with generator pattern
- `detect.py` - YOLOv8-based fruit detection

**Key Features:**
- Generator-based streaming (memory efficient)
- Context managers for resource cleanup
- Dataclass-based detection results
- Functional and OOP patterns mixed appropriately

**External Dependencies:**
- OpenCV for video I/O
- Ultralytics YOLOv8 for detection

### 2. Quality Module (`src/quality/`)

**Purpose:** Assess fruit freshness and quality

**Components:**
- `score.py` - Quality scoring algorithms

**Key Features:**
- Color analysis (HSV-based)
- Texture analysis (variance-based)
- Enum-based freshness levels
- Pure functions for testability

**Future Enhancement:**
Replace heuristic scoring with trained ML model (e.g., fine-tuned ResNet or EfficientNet on fruit quality dataset)

### 3. Events Module (`src/events/`)

**Purpose:** Stream detection events to Azure Event Hub

**Components:**
- `publisher.py` - Async event publishing

**Key Features:**
- Async/await patterns for I/O operations
- Dataclass event schemas
- Factory functions for event creation
- Graceful fallback when Azure not configured

**Azure Integration:**
- Azure Event Hub Producer Client (async)
- JSON event serialization
- Connection pooling

**[See Setup Guide](setup_guide.md#azure-event-hub-setup)** for Event Hub configuration

### 4. Search Module (`src/search/`)

**Purpose:** Index and search fruit quality data

**Components:**
- `indexer.py` - Repository pattern for AI Search

**Key Features:**
- Repository pattern (abstraction over Azure SDK)
- Document-based indexing
- Flexible query interface
- OData filtering support

**Azure Integration:**
- Azure AI Search client
- Custom index schema for fruit quality
- Full-text and semantic search capabilities

**[See Setup Guide](setup_guide.md#azure-ai-search-setup)** for AI Search configuration

### 5. Pipeline Module (`src/pipeline/`)

**Purpose:** Orchestrate end-to-end processing

**Components:**
- `orchestrator.py` - Main processing pipeline
- `decorators.py` - Reusable decorators

**Key Features:**
- Decorator patterns (@timer, @retry, @log_execution)
- Chain of responsibility for processing steps
- Centralized configuration via dataclass
- Statistics collection

**Processing Flow:**
1. Stream video frames
2. Detect fruits per frame
3. Assess quality for each detection
4. Publish events (async)
5. Index documents (sync)
6. Display/save results

### 6. Config Module (`src/config/`)

**Purpose:** Centralized settings management

**Components:**
- `settings.py` - Pydantic-based configuration

**Key Features:**
- Environment variable loading (.env)
- Type validation via Pydantic
- Singleton pattern (LRU cache)
- Sensible defaults

## Data Flow

```
┌──────────────┐
│ Video Source │
└──────┬───────┘
       │
       ▼
┌──────────────────┐
│ Vision.Capture   │ (Generator)
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Vision.Detect    │ (YOLO)
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Quality.Score    │ (Freshness)
└──────┬───────────┘
       │
       ├─────────────────────┐
       │                     │
       ▼                     ▼
┌──────────────┐      ┌─────────────┐
│ Events.Pub   │      │ Search.Index│
│ (Event Hub)  │      │ (AI Search) │
└──────────────┘      └─────────────┘
```

## Design Patterns

### Creational Patterns
- **Factory Functions**: `create_quality_event()`, `create_fruit_document()`
- **Singleton**: Settings via `@lru_cache()`

### Structural Patterns
- **Repository**: `SearchRepository` abstracts Azure AI Search
- **Decorator**: `@timer`, `@retry`, `@log_execution` for cross-cutting concerns

### Behavioral Patterns
- **Strategy**: Quality scoring algorithms (extensible for different fruit types)
- **Chain of Responsibility**: Pipeline processing stages
- **Observer**: Event publishing (decoupled from detection)

### Functional Patterns
- **Generator**: `stream_frames()` for memory-efficient streaming
- **Pure Functions**: `assess_freshness()`, `draw_detections()`
- **Context Manager**: `video_writer()` for resource management

## Scalability Considerations

### Horizontal Scaling
- **Vision Module**: Multiple camera streams → multiple detector instances
- **Event Hub**: Partitioned event ingestion (high throughput)
- **AI Search**: Distributed indexing and querying

### Vertical Scaling
- **GPU Acceleration**: YOLO detection can leverage CUDA
- **Batch Processing**: Process multiple frames in parallel

### Cloud-Native Patterns
- **Stateless Components**: All modules are stateless (scalable via containers)
- **Event-Driven**: Decoupled via Event Hub (resilient to failures)
- **Async I/O**: Non-blocking Azure operations

### Deployment Options
1. **Edge**: Deploy detector on edge devices (NVIDIA Jetson)
2. **Hybrid**: Local detection + cloud analytics
3. **Full Cloud**: Azure Container Instances + Azure Functions

**[See Execution Guide](execution_guide.md#deployment-scenarios)** for deployment details

## Azure Integration

### Event Hub (CEP)
- **Purpose**: Real-time event streaming for alerts
- **Use Cases**:
  - Alert when rottenness detected
  - Aggregate quality trends
  - Trigger restocking workflows

### AI Search
- **Purpose**: Searchable quality insights
- **Use Cases**:
  - "Show all rotten apples in aisle 3"
  - "Quality decline trends for bananas"
  - Historical analysis and reporting

### Future Azure Services
- **Azure Functions**: Serverless event processing
- **Azure Stream Analytics**: Real-time CEP queries
- **Azure Blob Storage**: Store shelf images
- **Azure ML**: Retrain quality models

**[See Setup Guide](setup_guide.md)** for Azure service configuration

---

**Related Documentation:**
- [Setup Guide](setup_guide.md) - Azure setup and configuration
- [Execution Guide](execution_guide.md) - Running the system
- [README](../README.md) - Project overview
