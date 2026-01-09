# Fruits Quality Detection System

AI-powered fruit quality detection system for supermarket shelf monitoring using YOLOv8, Azure Event Hub, and Azure AI Search.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Documentation](#documentation)
- [Project Structure](#project-structure)
- [Git Workflow](#git-workflow)

## Overview

This PoC demonstrates an end-to-end scalable solution for monitoring fruit quality on supermarket shelves using computer vision and Azure cloud services.

**Key Capabilities:**
- Real-time fruit detection with YOLOv8
- Quality assessment (freshness/rottenness scoring)
- Event streaming to Azure Event Hub for Complex Event Processing (CEP)
- Searchable insights via Azure AI Search
- Modular, pythonic architecture with modern design patterns

## Features

✅ **Vision Module**: Video capture with generator patterns, YOLO-based object detection  
✅ **Quality Analysis**: Color and texture-based freshness scoring  
✅ **Event Pipeline**: Async publishing to Azure Event Hub  
✅ **AI Search**: Document indexing for flexible querying  
✅ **Pipeline Orchestration**: Decorator-based processing chains  
✅ **CLI Interface**: Click-based command-line tool  

## Quick Start

### Installation

```bash
# Install dependencies
uv pip install -e .

# Copy environment template
cp .env.example .env

# Edit .env with your Azure credentials (optional for local demo)
```

### Run Demo

```bash
# Quick demo with webcam (no Azure required)
python -m src.main demo

# Process video with full pipeline
python -m src.main detect --source 0 --events --search

# Process IP camera stream
python -m src.main detect --source http://camera-url/stream --output output/results.avi
```

### View Configuration

```bash
python -m src.main config
```

## Architecture

High-level system architecture:

```
Video Source → Vision (Capture + Detect) → Quality Analysis
                                              ↓
                                         Event Publisher → Azure Event Hub
                                              ↓
                                         Search Indexer → Azure AI Search
```

**Design Patterns Used:**
- Repository Pattern (search)
- Strategy Pattern (quality models)
- Decorator Pattern (pipeline steps)
- Generator Pattern (video streaming)

📖 **[Full Architecture Documentation](docs/architecture.md)**

## Documentation

- **[Setup Guide](docs/setup_guide.md)** - Azure configuration and dependencies
- **[Architecture](docs/architecture.md)** - System design and component details
- **[Execution Guide](docs/execution_guide.md)** - Demo scenarios and troubleshooting
  - [Offline Development Mode](docs/execution_guide.md#offline-development-mode) - Testing without cameras/Azure

## Project Structure

```
src/
├── vision/          # Video capture and object detection
├── quality/         # Freshness scoring models
├── events/          # Azure Event Hub integration
├── search/          # Azure AI Search integration
├── pipeline/        # Orchestration and decorators
├── config/          # Settings management (Pydantic)
└── main.py          # CLI entry point

legacy/              # Original scripts (archived)
tests/               # Unit and integration tests
docs/                # Comprehensive documentation
data/samples/        # Sample videos and datasets
```

## Legacy Scripts

Original proof-of-concept scripts have been moved to the `legacy/` folder for reference.

---

## Git Workflow

### Initial Setup and Push to GitHub

**Prerequisites:** Install [GitHub CLI](https://cli.github.com/)

```bash
# 1. Initialize git repository (if not already done)
git init

# 2. Add all files
git add .

# 3. Create initial commit
git commit -m "feat: Production-ready fruit quality detection PoC with Azure integration

Modular Python architecture for supermarket shelf monitoring using YOLOv8, 
Azure Event Hub (CEP), and Azure AI Search. Includes comprehensive documentation, 
offline testing tools, and pythonic design patterns for enterprise scalability."

# 4. Create GitHub repository (choose visibility)
gh repo create fruits-quality-detection --private --source=. --remote=origin

# 5. Rename branch to master and push
git branch -M master
git push -u origin master
```

### Feature Branch Workflow

```bash
# 1. Create and switch to feature branch
git checkout -b feature/your-feature-name

# 2. Make your changes...
# (edit files)

# 3. Stage changes
git add .

# 4. Commit with descriptive message
git commit -m "feat: Add new feature description"

# 5. Push feature branch to remote
git push -u origin feature/your-feature-name

# 6. Create pull request via GitHub CLI
gh pr create --title "Add your feature" --body "Description of changes" --base master

# 7. After PR approval, merge to master
gh pr merge --merge

# 8. Switch back to master and pull latest
git checkout master
git pull

# 9. Delete local feature branch (optional)
git branch -d feature/your-feature-name
```

### Quick Commands Reference

```bash
# Check status
git status

# View commit history
git log --oneline --graph --decorate --all

# Create new feature branch
git checkout -b feature/feature-name

# Switch branches
git checkout master
git checkout feature/feature-name

# Pull latest changes
git pull origin master

# Push current branch
git push

# View remote repositories
git remote -v
```

---

**Version:** 0.1.0  
**License:** MIT  
**Author:** Sofiane
