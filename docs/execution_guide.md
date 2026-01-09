# Execution Guide

Comprehensive guide for running demos, testing scenarios, and deploying the system.

## Table of Contents
- [Quick Start](#quick-start)
- [Demo Scenarios](#demo-scenarios)
- [Offline Development Mode](#offline-development-mode)
- [CLI Reference](#cli-reference)
- [Testing](#testing)
- [Deployment Scenarios](#deployment-scenarios)
- [Troubleshooting](#troubleshooting)

## Quick Start

### Run Quick Demo

```bash
# 10-second demo with webcam (no Azure required)
python -m src.main demo
```

**Expected Output:**
- Video window with detection boxes
- Console output with statistics
- Press 'q' to quit early

### Run Full Pipeline

```bash
# Full pipeline with Azure integration
python -m src.main detect \
  --source 0 \
  --events \
  --search \
  --max-frames 300
```

**[See Setup Guide](setup_guide.md)** for Azure configuration

## Demo Scenarios

### Scenario 1: Local Webcam Demo (No Azure)

**Use Case:** Quick testing without cloud dependencies

```bash
python -m src.main detect --source 0
```

**What Happens:**
- Streams from webcam (index 0)
- Detects objects with YOLO
- Displays annotated video
- No events/indexing

**Expected Results:**
- Real-time detection boxes
- Quality scores printed to console
- Frame statistics on exit

---

### Scenario 2: IP Camera Stream (No Azure)

**Use Case:** Test with actual shelf camera feed

```bash
python -m src.main detect \
  --source http://webcam.anklam.de/axis-cgi/mjpg/video.cgi \
  --output output/shelf_video.avi
```

**What Happens:**
- Streams from IP camera URL
- Saves annotated video to file
- No Azure integration

**Expected Results:**
- Processed video saved to `output/shelf_video.avi`
- Statistics in console

---

### Scenario 3: Full Pipeline with Azure

**Use Case:** End-to-end demo for stakeholders

```bash
python -m src.main detect \
  --source 0 \
  --events \
  --search \
  --max-frames 600 \
  --conf 0.4
```

**What Happens:**
1. Streams 600 frames (~20 seconds)
2. Detects fruits (0.4 confidence threshold)
3. Publishes events to Event Hub
4. Indexes documents in AI Search
5. Displays live video

**Expected Results:**
```
Processing video from: 0
Executing process_shelf_video
process_shelf_video executed in 23.45s
process_shelf_video completed successfully

=== Processing Complete ===
Frames processed: 600
Detections: 142
Events published: 142
Documents indexed: 142
```

**Verification:**
- Check Event Hub metrics in Azure Portal
- Query AI Search index for documents

---

### Scenario 4: Batch Processing (No Display)

**Use Case:** Process pre-recorded videos in background

```bash
python -m src.main detect \
  --source data/samples/shelf_video.mp4 \
  --output output/processed.avi \
  --no-display \
  --events \
  --search
```

**What Happens:**
- Processes entire video file
- Saves output without displaying
- Publishes to Azure services

**Use Cases:**
- Overnight batch processing
- Historical video analysis
- Server-side processing

---

### Scenario 5: High-Confidence Detection Only

**Use Case:** Focus on high-quality detections

```bash
python -m src.main detect \
  --source 0 \
  --conf 0.7 \
  --events \
  --search
```

**What Happens:**
- Only detects objects with 70%+ confidence
- Reduces false positives
- Higher quality results

---

## Offline Development Mode

Testing and development scenarios without real cameras or Azure services.

### Sample Datasets & Videos

**Recommended Sources:**

1. **Fruit-360 Dataset** (Kaggle)
   - 90,000+ images of fruits
   - [Download](https://www.kaggle.com/moltean/fruits)

2. **Fruit Quality Dataset** (Roboflow)
   - Fresh vs. rotten fruit images
   - [Search Roboflow Universe](https://universe.roboflow.com/)

3. **Public Webcam Streams** (for testing)
   ```bash
   # German town square camera
   python -m src.main detect --source http://webcam.anklam.de/axis-cgi/mjpg/video.cgi
   ```

4. **YouTube Supermarket Videos**
   - Download with `yt-dlp`: `yt-dlp "https://youtube.com/watch?v=..."` 
   - Search: "supermarket shelf", "fruit display"

---

### Generate Synthetic Test Video

**Use Case:** No sample videos available, need quick test data

```bash
# Generate 30-second test video with moving objects
python -m src.utils.video_simulator generate \
  --output data/samples/test_shelf.avi \
  --duration 30
```

**What It Creates:**
- Simple synthetic video with moving shapes
- Useful for pipeline testing (not for quality model training)
- Saved to `data/samples/` directory

---

### Simulate Live Camera Stream

**Use Case:** Test with video file as if it were a live camera feed

```bash
# Loop video file infinitely (simulates continuous camera)
python -m src.utils.video_simulator stream data/samples/shelf_video.mp4 --loop

# Control playback speed
python -m src.utils.video_simulator stream video.mp4 --fps 15
```

**Then process with pipeline:**
```bash
# In another terminal, process the "live" stream
python -m src.main detect --source data/samples/shelf_video.mp4
```

**Pro Tip:** Use looping video files to simulate 24/7 camera feeds during development.

---

### Mock Azure Services Locally

**Event Hub Mock:**
The system automatically falls back to console logging when Event Hub is not configured:

```bash
# Run without Azure credentials - events printed to console
python -m src.main detect --source 0 --events

# Output shows:
# [EVENT] {
#   "timestamp": "2026-01-09T...",
#   "fruit_type": "apple",
#   "freshness_level": "fresh",
#   ...
# }
```

**AI Search Mock:**
Similarly, search indexing logs to console when not configured:

```bash
# Run without Azure - documents printed to console  
python -m src.main detect --source 0 --search

# Output shows:
# [INDEX] {
#   "id": "apple_1736438...",
#   "fruit_type": "apple",
#   "quality_score": 85.3,
#   ...
# }
```

**Full Offline Pipeline:**
```bash
# Test complete pipeline without any Azure services
python -m src.main detect \
  --source data/samples/test_shelf.avi \
  --events \
  --search \
  --output output/offline_test.avi
```

---

### Offline Testing Scenarios

#### Scenario 1: Pipeline Development

**Goal:** Develop new features without Azure dependencies

```bash
# 1. Generate test video
python -m src.utils.video_simulator generate --duration 60

# 2. Run pipeline with mocked services
python -m src.main detect \
  --source data/samples/test_shelf.avi \
  --events \
  --search \
  --no-display \
  --output output/dev_test.avi

# 3. Review console logs for event/index output
```

---

#### Scenario 2: Quality Model Testing

**Goal:** Test freshness detection algorithm with known data

```bash
# Download fruit quality dataset from Roboflow
# Place images in data/samples/images/

# Test quality scoring on individual images
python -c "
from src.quality.score import assess_freshness
import cv2

frame = cv2.imread('data/samples/images/fresh_apple.jpg')
bbox = (0, 0, frame.shape[1], frame.shape[0])  # Full image
score = assess_freshness(frame, bbox, 'apple')

print(f'Freshness: {score.freshness_level.value}')
print(f'Score: {score.score:.1f}/100')
"
```

---

#### Scenario 3: Batch Video Processing

**Goal:** Process multiple videos overnight for analysis

```bash
# PowerShell script for batch processing
Get-ChildItem data/samples/videos/*.mp4 | ForEach-Object {
    python -m src.main detect `
      --source $_.FullName `
      --output "output/processed_$($_.Name)" `
      --no-display `
      --events `
      --search
}
```

---

#### Scenario 4: Performance Benchmarking

**Goal:** Measure FPS and throughput without Azure overhead

```bash
# Process 1000 frames and measure performance
python -m src.main detect \
  --source data/samples/test_shelf.avi \
  --max-frames 1000 \
  --no-display

# Check console for timing:
# "process_shelf_video executed in X.XXs"
# Calculate FPS: 1000 / X.XX
```

---

### Creating Custom Test Datasets

**Directory Structure:**
```
data/samples/
├── videos/
│   ├── fresh_apples_shelf.mp4    # Good quality fruit
│   ├── rotten_bananas_shelf.mp4  # Poor quality fruit  
│   └── mixed_quality_shelf.mp4   # Mixed scenarios
├── images/
│   ├── fresh/
│   │   ├── apple_01.jpg
│   │   └── banana_01.jpg
│   └── rotten/
│       ├── apple_rotten_01.jpg
│       └── banana_rotten_01.jpg
└── README.md
```

**Recording Your Own Test Videos:**

```bash
# Capture from webcam to create test dataset
python legacy/capture.py \
  --source 0 \
  --output data/samples/videos/my_test_shelf.avi \
  --duration 30

# Then use for testing
python -m src.main detect --source data/samples/videos/my_test_shelf.avi
```

**Pro Tip:** Record videos of actual fruits at different quality levels (fresh, medium, rotten) for realistic model validation.

---

### Offline Demo Setup (Customer Presentation)

**Preparation:**

1. **Download sample videos** (1 week before demo)
   ```bash
   # Use yt-dlp or download from datasets
   yt-dlp -o "data/samples/supermarket_shelf.mp4" "https://youtube.com/watch?v=..."
   ```

2. **Generate synthetic video** (backup option)
   ```bash
   python -m src.utils.video_simulator generate --duration 120
   ```

3. **Test pipeline** (1 day before)
   ```bash
   python -m src.main detect \
     --source data/samples/supermarket_shelf.mp4 \
     --events \
     --search \
     --max-frames 300
   ```

**Demo Day:**

```bash
# Option 1: Loop video as if live stream
python -m src.utils.video_simulator stream \
  data/samples/supermarket_shelf.mp4 \
  --loop &

# Option 2: Direct file playback
python -m src.main detect \
  --source data/samples/supermarket_shelf.mp4 \
  --events \
  --search
```

**Expected Output:**
- Real-time detection boxes on fruits
- Console logs showing events and search documents
- Statistics at end (frames, detections, events)

---

## CLI Reference

### Main Commands

```bash
# Run detection pipeline
python -m src.main detect [OPTIONS]

# Run quick demo
python -m src.main demo

# Show configuration
python -m src.main config
```

### Detect Command Options

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--source` | `-s` | str | Required | Video source (index, file, URL) |
| `--output` | `-o` | str | None | Output video file path |
| `--max-frames` | `-m` | int | 0 | Max frames (0 = unlimited) |
| `--conf` | `-c` | float | 0.3 | Detection confidence (0.0-1.0) |
| `--events` | - | flag | False | Enable Event Hub publishing |
| `--search` | - | flag | False | Enable AI Search indexing |
| `--display` | - | flag | True | Show video window |

### Examples

```bash
# Webcam with high confidence
python -m src.main detect -s 0 -c 0.6

# IP camera with Azure
python -m src.main detect \
  -s http://camera/stream \
  --events --search

# Process 500 frames only
python -m src.main detect -s 0 -m 500

# Save output without display
python -m src.main detect \
  -s 0 \
  -o output/result.avi \
  --no-display
```

## Testing

### Unit Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific module
pytest tests/test_quality.py
```

### Integration Tests

```bash
# Test vision module
pytest tests/test_vision.py -v

# Test Azure integration (requires credentials)
pytest tests/test_events.py -v
pytest tests/test_search.py -v
```

### Manual Testing

```bash
# Test video capture only
python -c "
from src.vision.capture import stream_frames
for i, (success, frame) in enumerate(stream_frames(0, 10)):
    print(f'Frame {i}: {success}')
"

# Test YOLO detection
python -c "
from src.vision.detect import FruitDetector
import cv2
detector = FruitDetector()
frame = cv2.imread('data/samples/test_image.jpg')
detections = detector.detect(frame)
print(f'Found {len(detections)} objects')
"
```

## Deployment Scenarios

### Local Development

```bash
# Use .env file for configuration
python -m src.main detect --source 0 --events --search
```

### Docker Deployment

```dockerfile
# Dockerfile (create in project root)
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install uv && uv pip install -e .

CMD ["python", "-m", "src.main", "detect", "--source", "0"]
```

```bash
# Build and run
docker build -t fruits-detection .
docker run -it --rm \
  -e EVENT_HUB_CONNECTION_STRING="..." \
  -e SEARCH_ENDPOINT="..." \
  fruits-detection
```

### Edge Deployment (NVIDIA Jetson)

```bash
# Install on Jetson device
uv pip install -e .

# Use GPU for YOLO
export YOLO_DEVICE=cuda

# Run with camera
python -m src.main detect \
  --source /dev/video0 \
  --events --search
```

### Azure Container Instances

```bash
# Build and push to ACR
az acr build --registry <your-acr> --image fruits-detection .

# Deploy to ACI
az container create \
  --resource-group fruits-quality-rg \
  --name fruits-detector \
  --image <your-acr>.azurecr.io/fruits-detection \
  --environment-variables \
    EVENT_HUB_CONNECTION_STRING="..." \
    SEARCH_ENDPOINT="..."
```

**[See Architecture](architecture.md#scalability-considerations)** for scaling strategies

## Troubleshooting

### Common Issues

#### Video Source Errors

**Problem:** "Cannot open video source: 0"

**Solutions:**
1. Check camera permissions (Windows/macOS)
2. Try different index: `--source 1` or `--source 2`
3. List cameras: `python -c "import cv2; print([i for i in range(5) if cv2.VideoCapture(i).isOpened()])"`
4. Test with video file instead: `--source data/samples/test.mp4`

---

#### YOLO Model Issues

**Problem:** "Model not found" or slow detection

**Solutions:**
1. Pre-download: `python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"`
2. Check internet connection (first run downloads model)
3. Use smaller model: Edit `src/config/settings.py` → `YOLO_MODEL = "yolov8n.pt"`
4. For GPU: Install `torch` with CUDA support

---

#### Azure Connection Errors

**Problem:** "Event Hub authentication failed"

**Solutions:**
1. Verify connection string format in `.env`
2. Check firewall/network settings
3. Test connection: 
   ```bash
   python -c "from azure.eventhub import EventHubProducerClient; \
   client = EventHubProducerClient.from_connection_string('YOUR_CONNECTION_STRING', eventhub_name='YOUR_HUB')"
   ```
4. Verify namespace and hub names match

**Problem:** "AI Search unauthorized"

**Solutions:**
1. Verify admin key (not query key)
2. Check endpoint URL format: `https://<service>.search.windows.net`
3. Ensure service is running (check Azure Portal)

---

#### Performance Issues

**Problem:** Slow frame processing

**Solutions:**
1. Lower confidence threshold: `--conf 0.2` (faster but more false positives)
2. Use smaller YOLO model: `yolov8n.pt` instead of `yolov8l.pt`
3. Reduce frame rate: Process every Nth frame
4. Enable GPU: Install CUDA-enabled PyTorch
5. Close other applications

---

#### Memory Errors

**Problem:** "Out of memory"

**Solutions:**
1. Use generator pattern (already implemented)
2. Limit max frames: `--max-frames 500`
3. Don't save output: Remove `--output` flag
4. Use smaller model: `yolov8n.pt`
5. Process in batches

---

### Debug Mode

Enable verbose logging:

```python
# Add to src/pipeline/decorators.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

Run with debugging:

```bash
python -m pdb -m src.main detect --source 0
```

### Logs and Monitoring

```bash
# View Event Hub metrics
az monitor metrics list \
  --resource-id "/subscriptions/.../fruits-quality-events" \
  --metric IncomingMessages

# Query AI Search
curl -X GET "https://fruits-quality-search.search.windows.net/indexes/fruits-quality/docs?search=*&$count=true" \
  -H "api-key: YOUR_ADMIN_KEY"
```

---

**Related Documentation:**
- [Setup Guide](setup_guide.md) - Installation and configuration
- [Architecture](architecture.md) - System design
- [README](../README.md) - Project overview

**Need Help?**
- Check [Architecture](architecture.md#design-patterns) for design details
- Review [Setup Guide](setup_guide.md#verification) for configuration
- Contact: sofiane@example.com
