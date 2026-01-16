# Setup Guide

Complete setup instructions for local development and Azure integration.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Local Setup](#local-setup)
- [Azure Event Hub Setup](#azure-event-hub-setup)
- [Azure AI Search Setup](#azure-ai-search-setup)
- [Environment Configuration](#environment-configuration)
- [Verification](#verification)

## Prerequisites

### Required Software
- Python 3.11+ ([Download](https://www.python.org/downloads/))
- uv package manager ([Install](https://github.com/astral-sh/uv))
- Git (for cloning repository)
- Webcam or IP camera (for testing)

### Optional (for Azure integration)
- Azure subscription ([Free account](https://azure.microsoft.com/free/))
- Azure CLI ([Install](https://learn.microsoft.com/cli/azure/install-azure-cli))

### Hardware Recommendations
- **CPU**: 4+ cores for real-time processing
- **RAM**: 8GB minimum, 16GB recommended
- **GPU**: Optional, NVIDIA GPU with CUDA for faster detection
- **Storage**: 5GB for models and dependencies

## Local Setup

### 1. Clone Repository

```bash
cd /path/to/projects
git clone <repository-url>
cd capture-cctv-videos
```

### 2. Install Dependencies

```bash
# Install core dependencies
uv pip install -e .

# Install development dependencies (optional)
uv pip install -e ".[dev]"
```

### 3. Download YOLO Model

The YOLOv8n model will be downloaded automatically on first run. To pre-download:

```bash
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
```

**Model sizes:**
- `yolov8n.pt` - Nano (6MB, fastest)
- `yolov8s.pt` - Small (11MB)
- `yolov8m.pt` - Medium (25MB)
- `yolov8l.pt` - Large (45MB)

Edit `src/config/settings.py` to change the default model.

### 4. Test Local Installation

```bash
# Run demo without Azure (webcam required)
python -m src.main demo

# Should display video with detections
# Press 'q' to quit
```

## Azure Event Hub Setup

### 1. Create Event Hub Namespace

Using Azure Portal:
1. Navigate to **Create a resource** → **Event Hubs**
2. Fill in details:
   - **Namespace name**: `fruits-quality-events`
   - **Pricing tier**: Standard (supports partitions)
   - **Region**: Choose nearest region
3. Click **Review + Create**

Using Azure CLI:

```bash
# Login to Azure
az login

# Create resource group
az group create --name fruits-quality-rg --location eastus

# Create Event Hub namespace
az eventhubs namespace create \
  --name fruits-quality-events \
  --resource-group fruits-quality-rg \
  --location eastus \
  --sku Standard
```

### 2. Create Event Hub

Using Azure Portal:
1. Navigate to your Event Hub namespace
2. Click **+ Event Hub**
3. Name: `quality-detections`
4. Partition count: 2 (adjust based on throughput needs)
5. Click **Create**

Using Azure CLI:

```bash
az eventhubs eventhub create \
  --name quality-detections \
  --namespace-name fruits-quality-events \
  --resource-group fruits-quality-rg \
  --partition-count 2
```

### 3. Get Connection String

Using Azure Portal:
1. Navigate to **Shared access policies**
2. Click **RootManageSharedAccessKey**
3. Copy **Connection string–primary key**

Using Azure CLI:

```bash
az eventhubs namespace authorization-rule keys list \
  --resource-group fruits-quality-rg \
  --namespace-name fruits-quality-events \
  --name RootManageSharedAccessKey \
  --query primaryConnectionString -o tsv
```

**[See Architecture](architecture.md#azure-integration)** for Event Hub usage patterns

## Azure AI Search Setup

### 1. Create AI Search Service

Using Azure Portal:
1. Navigate to **Create a resource** → **Azure AI Search**
2. Fill in details:
   - **Service name**: `fruits-quality-search`
   - **Pricing tier**: Free or Basic
   - **Region**: Same as Event Hub
3. Click **Review + Create**

Using Azure CLI:

```bash
az search service create \
  --name fruits-quality-search \
  --resource-group fruits-quality-rg \
  --location eastus \
  --sku free
```

### 2. Get Admin Key

Using Azure Portal:
1. Navigate to your AI Search service
2. Click **Keys** in left menu
3. Copy **Primary admin key**

Using Azure CLI:

```bash
az search admin-key show \
  --resource-group fruits-quality-rg \
  --service-name fruits-quality-search \
  --query primaryKey -o tsv
```

### 3. Create Index (Automatic)

The application will create the index automatically on first run. To create manually:

```python
from src.search.indexer import SearchRepository

repo = SearchRepository(
    endpoint="https://fruits-quality-search.search.windows.net",
    api_key="<your-admin-key>"
)
repo.create_index()
```

**[See Architecture](architecture.md#azure-integration)** for AI Search usage patterns

## Environment Configuration

### 1. Create .env File

```bash
# Copy template
cp .env.example .env

# Edit with your credentials
nano .env  # or use your preferred editor
```

### 2. Configure Environment Variables

Edit `.env` file:

```bash
# Azure Event Hub Configuration
EVENT_HUB_CONNECTION_STRING=Endpoint=sb://fruits-quality-events.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=...
EVENT_HUB_NAME=quality-detections

# Azure AI Search Configuration
SEARCH_ENDPOINT=https://fruits-quality-search.search.windows.net
SEARCH_API_KEY=<your-admin-key>
SEARCH_INDEX_NAME=fruits-quality

# Detection Configuration
YOLO_MODEL=yolov8n.pt
DETECTION_CONFIDENCE=0.3

# Video Configuration
DEFAULT_CAMERA_SOURCE=0
OUTPUT_DIRECTORY=output
```

**⚠️ Security Note**: Never commit `.env` to version control. It's already in `.gitignore`.

## Verification

### 1. Check Configuration

```bash
python -m src.main config
```

Should show:
```
=== Current Configuration ===
YOLO Model: yolov8n.pt
Detection Confidence: 0.3
Output Directory: output

Azure Event Hub: Configured
Azure AI Search: Configured
```

### 2. Test Local Pipeline (No Azure)

```bash
python -m src.main demo
```

### 3. Test Full Pipeline (With Azure)

```bash
python -m src.main detect --source 0 --events --search --max-frames 100
```

Check Azure Portal:
- **Event Hub**: Metrics → Incoming Messages should show activity
- **AI Search**: Indexes → fruits-quality should have documents

### 4. Troubleshooting

**Issue:** "Cannot open video source"
- **Solution**: Check camera permissions, try different source index (0, 1, 2)

**Issue:** "Event Hub connection failed"
- **Solution**: Verify connection string format, check firewall settings

**Issue:** "AI Search authentication failed"
- **Solution**: Verify admin key, check service endpoint URL

**Issue:** "YOLO model not found"
- **Solution**: Run `python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"`

**[See Execution Guide](execution_guide.md#troubleshooting)** for more troubleshooting tips

---

## Azure AI Foundry Evaluation Setup

**Purpose:** Quick evaluation of GPT-4V for intelligent fruit quality assessment (temporary - evaluation branch only)

**Branch:** `azure-ai-foundry`

### Quick Setup (1-2 Day Evaluation)

#### 1. Install Evaluation Dependencies

```powershell
# Activate venv
.venv\Scripts\Activate.ps1

# Install Azure OpenAI SDK
pip install openai>=1.0.0 pillow

# Save dependencies
pip freeze > requirements-eval.txt
```

#### 2. Azure Portal Setup

**Option A: Azure Portal (Recommended for first time)**

**Step-by-step navigation:**

1. **Create Azure OpenAI resource:**
   - Navigate to https://portal.azure.com
   - Click **☰ hamburger menu** (top-left) → **"Create a resource"**
   - In search box, type: **`Azure OpenAI`**
   - Select **"Azure OpenAI"** (Microsoft) → Click **"Create"**
   - **Basics tab:**
     - Subscription: (select your trial/paid)
     - Resource Group: Click **"Create new"** → Name: `rg-fruits-quality-eval` → **OK**
     - Region: Select **East US** (best GPT-4V model availability)
     - Name: `fruits-quality-openai-001` (globally unique - adjust if taken)
     - Pricing tier: **Standard S0**
   - **Network tab:** Leave default (all networks)
   - Click **"Review + create"** → **"Create"**
   - Wait 2-4 minutes for deployment
   - Click **"Go to resource"** when complete

2. **Deploy GPT-4V model:**
   - Open new tab: https://ai.azure.com
   - Sign in with same Azure account
   - If prompted: **"Create project"**
     - Name: `FruitsQualityEval`
     - Resource: Select `fruits-quality-openai-001`
     - Click **"Create"**
   - Left sidebar → **"Deployments"** (under Shared resources)
   - Click **"+ Create deployment"** or **"+ Deploy model"** → **"Deploy base model"**
   - **Select model:**
     - Model family: **gpt-4**
     - Model: **`gpt-4o`** (recommended, version 2024-05-13+) or **`gpt-4-vision-preview`**
   - **Configure:**
     - Deployment name: `fruit-quality-gpt4v` (exact name)
     - Deployment type: **Standard**
     - Tokens per minute rate limit: **10** (10,000 TPM - sufficient for eval)
   - Click **"Deploy"** → Wait 30-60 seconds
   - Verify: Status shows **✓ Running** (green checkmark)

3. **Get credentials:**
   - Return to Azure Portal (portal.azure.com)
   - Navigate to your resource: `fruits-quality-openai-001`
   - Left sidebar → **"Keys and Endpoint"** (under Resource Management)
   - Copy **Endpoint** (click 📋 icon): `https://fruits-quality-openai-001.openai.azure.com/`
   - Click **"Show Key"** next to KEY 1 → Copy key (click 📋)
   - Save both securely for `.env` file

**Option B: Azure CLI (Faster)**

```powershell
# Login
az login

# Create resource
az cognitiveservices account create `
  --name fruits-quality-openai-001 `
  --resource-group rg-fruits-quality-eval `
  --kind OpenAI `
  --sku S0 `
  --location eastus

# Get credentials
az cognitiveservices account show `
  --name fruits-quality-openai-001 `
  --resource-group rg-fruits-quality-eval `
  --query properties.endpoint --output tsv

az cognitiveservices account keys list `
  --name fruits-quality-openai-001 `
  --resource-group rg-fruits-quality-eval `
  --query key1 --output tsv
```

#### 3. Configure Environment

Add to `.env` file:

```bash
# Azure AI Foundry Evaluation
AZURE_OPENAI_ENDPOINT=https://fruits-quality-openai-001.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_DEPLOYMENT=fruit-quality-gpt4v
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

#### 4. Verify Connection

```powershell
python evaluation/scripts/eval_single_image.py --test-connection
```

**Expected output:**
```
✓ Connection successful
Endpoint: https://fruits-quality-openai-001.openai.azure.com/
Deployment: fruit-quality-gpt4v
```

### Cost Management

**GPT-4V Pricing (approximate):**
- Input: $0.01 per 1K tokens
- Output: $0.03 per 1K tokens  
- Image: ~1000-1500 tokens each

**Estimated evaluation costs:**
- Single image: $0.02-$0.04
- 100 images: $2-$4
- Trial credit: $200 (sufficient)

**Track costs:**
```powershell
python evaluation/scripts/eval_single_image.py --show-costs
```

### Detailed Setup

See comprehensive guide: [evaluation/azure_ai_foundry/setup_guide.md](../evaluation/azure_ai_foundry/setup_guide.md)

---

**Related Documentation:**
- [Architecture](architecture.md) - System design and components
- [Execution Guide](execution_guide.md) - Running demos and scenarios
- [Azure AI Foundry Evaluation](execution_guide.md#azure-ai-foundry-evaluation) - Evaluation commands
- [README](../README.md) - Project overview

**Next Steps:**
- [Run Demo Scenarios](execution_guide.md#demo-scenarios)
- [Run Azure AI Foundry Evaluation](execution_guide.md#azure-ai-foundry-evaluation)
- [Deploy to Production](execution_guide.md#deployment-scenarios)
