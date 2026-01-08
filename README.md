
# Capture CCTV Camera Videos POC

This project demonstrates how to capture video streams from both local webcams and IP cameras using OpenCV in Python. It also includes a simple face detection example using Haar cascades. The project uses `uv` as the build and dependency manager.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Setup](#setup)
3. [Usage](#usage)
    - [Video Capture](#video-capture)
    - [Face Detection (Haar)](#face-detection-haar)
    - [Eye Detection (Haar)](#eye-detection-haar)
4. [Files](#files)
5. [Notes](#notes)

## Prerequisites
- Python 3.8–3.12 installed
- [uv](https://github.com/astral-sh/uv) installed (`pip install uv`)

## Setup
1. Clone this repository or download the source code.
2. Open a terminal in the project directory.
3. Install dependencies:

    uv pip install -r requirements.txt

## Usage

### Video Capture
Capture video from a local webcam:

    uv pip run python capture.py --source 0

Capture video from an IP camera (replace the URL with your camera's RTSP/HTTP stream):

    uv pip run python capture.py --source rtsp://username:password@ip_address:port/stream

Captured frames or video will be saved in the `output/` directory.


### Face Detection (Haar)
Detect faces in real-time from a webcam or video file and mark them with rectangles:

    uv pip run python face_detect_haar.py --source 0

Replace `0` with a video file path to run detection on a video file.

### Eye Detection (Haar)
Detect eyes within faces in real-time from a webcam or video file and mark them with rectangles:

    uv pip run python eye_detect_haar.py --source 0

Replace `0` with a video file path to run detection on a video file.

## Files
- `capture.py`: Main script to capture video from a camera source.
- `face_detect_haar.py`: Simple face detection using Haar cascades.
- `eye_detect_haar.py`: Simple eye detection using Haar cascades.
- `requirements.txt`: Python dependencies.

## Notes
- For IP cameras, ensure your network allows access to the camera stream.
- You can modify the scripts to save images instead of video, or to process frames as needed.
