# Fruits Quality Detection - Data Samples

Place sample fruit shelf videos and images here for testing.

## Quick Start

### Generate Synthetic Test Video

```bash
# Generate 30-second test video
python -m src.utils.video_simulator generate --duration 30

# Generates: data/samples/test_shelf.avi
```

### Simulate Live Camera Stream

```bash
# Loop existing video as if it were a live stream
python -m src.utils.video_simulator stream data/samples/videos/shelf_video.mp4 --loop
```

## Recommended Datasets

1. **Fruit-360**: [https://www.kaggle.com/moltean/fruits](https://www.kaggle.com/moltean/fruits)
   - 90,000+ images of 131 fruit types
   - Perfect for training/validation

2. **Fruit Quality Dataset** (Roboflow): Search on [Roboflow Universe](https://universe.roboflow.com/)
   - Fresh vs. rotten fruit images
   - Good for quality model testing

3. **Custom Videos**: Record your own shelf videos for realistic testing
   ```bash
   python legacy/capture.py --source 0 --output data/samples/videos/my_shelf.avi --duration 30
   ```

4. **Public Webcam Streams** (for testing)
   - German town: `http://webcam.anklam.de/axis-cgi/mjpg/video.cgi`
   - Search "public IP camera" for more sources

5. **YouTube Supermarket Videos**
   ```bash
   # Download with yt-dlp
   yt-dlp -o "data/samples/videos/supermarket.mp4" "https://youtube.com/watch?v=..."
   
   # Search terms: "supermarket shelf", "fruit display", "grocery store produce"
   ```

## File Structure

```
samples/
├── videos/
│   ├── shelf_apples.mp4          # Sample shelf videos
│   ├── shelf_bananas.mp4
│   ├── shelf_mixed.mp4
│   └── test_shelf.avi            # Generated synthetic video
├── images/
│   ├── fresh/
│   │   ├── fresh_apple_01.jpg    # Fresh fruit images
│   │   └── fresh_banana_01.jpg
│   └── rotten/
│       ├── rotten_apple_01.jpg   # Rotten fruit images
│       └── rotten_banana_01.jpg
└── README.md
```

## Usage Examples

### Test with Sample Video

```bash
# Run detection on sample video
python -m src.main detect --source data/samples/videos/shelf_apples.mp4
```

### Process All Videos

```bash
# PowerShell: Process all videos in folder
Get-ChildItem data/samples/videos/*.mp4 | ForEach-Object {
    python -m src.main detect --source $_.FullName --output "output/processed_$($_.Name)"
}

# Bash: Process all videos
for video in data/samples/videos/*.mp4; do
    python -m src.main detect --source "$video" --output "output/processed_$(basename $video)"
done
```

### Offline Demo Preparation

```bash
# 1. Generate test video (if no real videos available)
python -m src.utils.video_simulator generate --duration 120

# 2. Test pipeline
python -m src.main detect --source data/samples/test_shelf.avi --events --search

# 3. For demo: Loop video as live stream
python -m src.utils.video_simulator stream data/samples/test_shelf.avi --loop
```

## Recording Custom Test Data

### Capture from Webcam

```bash
# Record 60-second test video
python legacy/capture.py --source 0 --output data/samples/videos/my_test.avi --duration 60
```

### Tips for Good Test Videos

1. **Lighting**: Ensure good, consistent lighting
2. **Angle**: Position camera to clearly see fruits
3. **Variety**: Record fresh, medium, and rotten fruits
4. **Duration**: 30-60 seconds per scenario
5. **Label**: Name files descriptively (e.g., `fresh_apples_well_lit.mp4`)

## Downloading Datasets

### Kaggle Datasets

```bash
# Install Kaggle CLI
pip install kaggle

# Configure API key (from https://www.kaggle.com/settings)
# Place kaggle.json in ~/.kaggle/

# Download Fruit-360 dataset
kaggle datasets download -d moltean/fruits
unzip fruits.zip -d data/samples/images/
```

### Roboflow Datasets

1. Browse [Roboflow Universe](https://universe.roboflow.com/)
2. Search for "fruit quality" or "fruit detection"
3. Download in COCO or YOLO format
4. Extract to `data/samples/images/`

---

**See [Execution Guide - Offline Development Mode](../../docs/execution_guide.md#offline-development-mode)** for detailed testing scenarios.
