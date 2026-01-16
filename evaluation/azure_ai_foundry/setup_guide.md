# Azure AI Foundry Setup Guide (Evaluation)

Quick setup guide for evaluating Azure AI Foundry GPT-4V for fruit quality assessment.

## Prerequisites

- Azure account with active subscription (trial subscription works)
- Python 3.11+ with venv activated
- Git branch: `azure-ai-foundry`

## Step 1: Create Azure OpenAI Resource

### Option A: Using Azure Portal (Recommended for First Time)

#### Step 1: Navigate to Azure Portal and Create Resource

1. **Open Azure Portal**
   - Go to https://portal.azure.com
   - Sign in with your Azure account (trial or paid subscription)

2. **Start Creating Azure OpenAI Service**
   - Click the **☰ (hamburger menu)** in top-left corner
   - Click **"Create a resource"** (or use the big **"+ Create a resource"** button in the center)
   - In the search box at top, type: **`Azure OpenAI`**
   - From the results, select **"Azure OpenAI"** (publisher: Microsoft)
   - Click the blue **"Create"** button

#### Step 2: Configure Basic Settings

On the **"Create Azure OpenAI"** page, configure the following tabs:

**Basics Tab:**
- **Subscription:** Select your subscription (e.g., "Free Trial" or "Pay-As-You-Go")
- **Resource Group:** 
  - Click **"Create new"** 
  - Enter name: `rg-fruits-quality-eval`
  - Click **"OK"**
  - (Or select existing resource group if you have one)
- **Region:** Select a region with GPT-4V/GPT-4o availability:
  - **East US** (recommended - most models available)
  - **Sweden Central** (alternative)
  - **Australia East** (alternative)
  - **France Central** (alternative)
  - Note: GPT-4V availability varies by region. If deployment fails later, try East US.
- **Name:** Enter unique name: `fruits-quality-openai-001`
  - Must be globally unique (Azure will validate)
  - If taken, try: `fruits-quality-openai-002`, `fruits-eval-openai-001`, etc.
- **Pricing tier:** Select **"Standard S0"**

**Network Tab:**
- Leave default: **"All networks, including the internet, can access this resource"**
- (For evaluation, public access is fine. Lock down for production.)

**Tags Tab (Optional):**
- Skip or add tags like:
  - Name: `Environment`, Value: `Evaluation`
  - Name: `Project`, Value: `FruitsQuality`

#### Step 3: Review and Create

- Click **"Review + create"** button at bottom
- Azure validates your configuration (takes 10-15 seconds)
- Review the summary:
  - Subscription cost: Standard S0 (pay-per-token, no upfront cost)
  - Estimated cost: ~$0 initially, usage-based billing
- Click blue **"Create"** button
- Deployment starts (progress bar appears)
- Wait 2-4 minutes for deployment to complete
- When done, you'll see: **"Your deployment is complete"**
- Click **"Go to resource"** button

#### Step 4: Get API Credentials

Now you're on your Azure OpenAI resource page.

1. **Copy Endpoint URL:**
   - In the left sidebar menu, click **"Keys and Endpoint"** (under "Resource Management" section)
   - You'll see:
     - **KEY 1** (hidden by default - shows as `•••••••••`)
     - **KEY 2** (backup key)
     - **Endpoint** (URL format: `https://fruits-quality-openai-001.openai.azure.com/`)
   - Click the **📋 copy icon** next to **Endpoint** 
   - Save this URL - you'll need it for `.env` file

2. **Copy API Key:**
   - Click **"Show Key"** next to **KEY 1**
   - Key will appear (long string like: `a1b2c3d4e5f6...`)
   - Click the **📋 copy icon** to copy
   - Save this securely - you'll need it for `.env` file
   - **Important:** Keep this key private! Don't commit to Git.

3. **Note Resource Details:**
   - Resource name: `fruits-quality-openai-001`
   - Resource group: `rg-fruits-quality-eval`
   - Region: (whichever you selected)

**You now have:**
✅ Azure OpenAI resource created  
✅ Endpoint URL copied  
✅ API Key copied  

**Next:** Deploy the GPT-4V model (see Step 5 below)

---

#### Step 5: Deploy GPT-4V Model (Using Azure AI Foundry Studio)

Azure OpenAI models must be deployed before use. We'll use Azure AI Foundry (formerly Azure AI Studio).

1. **Navigate to Azure AI Foundry:**
   - Open new browser tab: https://ai.azure.com
   - Sign in with same Azure account
   - If prompted to create a project:
     - Click **"Create project"**
     - Project name: `FruitsQualityEval`
     - Select your Azure OpenAI resource: `fruits-quality-openai-001`
     - Click **"Create"**

2. **Create Model Deployment:**
   - In left sidebar, click **"Deployments"** (under "Shared resources")
   - Click **"+ Create deployment"** button (or **"+ Deploy model"** → **"Deploy base model"**)
   - A panel opens on the right

3. **Select Model:**
   - **Model family:** Scroll and select **"gpt-4"**
   - **Model:** Look for one of these (listed by preference):
     1. **`gpt-4o`** (newer, better, recommended) - version `2024-05-13` or later
     2. **`gpt-4-vision-preview`** (if gpt-4o not available)
     3. **`gpt-4-turbo`** with vision (alternative)
   - If you don't see GPT-4V models:
     - Region issue: Your Azure OpenAI resource region doesn't support GPT-4V
     - Solution: Recreate resource in **East US** region
     - Check availability: https://learn.microsoft.com/azure/ai-services/openai/concepts/models#model-summary-table-and-region-availability

4. **Configure Deployment:**
   - **Deployment name:** Enter: `fruit-quality-gpt4v`
     - Important: Use this exact name or update `.env` later
   - **Deployment type:** Select **"Standard"**
   - **Model version:** Select latest available (e.g., `2024-05-13` for gpt-4o)
   - **Tokens per Minute Rate Limit (thousands):**
     - Set to: **10** (10,000 tokens per minute)
     - This is sufficient for evaluation (handles ~5-10 images/minute)
     - Can increase later if needed

5. **Create Deployment:**
   - Click **"Deploy"** button
   - Deployment starts (takes 30-60 seconds)
   - Status shows: **"Creating"** → **"Succeeded"**
   - You'll see the deployment in the list with:
     - Name: `fruit-quality-gpt4v`
     - Model: `gpt-4o` (or whichever you selected)
     - Status: **Running** (green checkmark)

**You now have:**
✅ GPT-4V model deployed  
✅ Deployment name: `fruit-quality-gpt4v`  
✅ Ready to use via API  

---

#### Step 6: Final Verification

Before proceeding, verify you have all three pieces:

1. **Endpoint:** `https://fruits-quality-openai-001.openai.azure.com/`
2. **API Key:** `a1b2c3d4...` (long string)
3. **Deployment Name:** `fruit-quality-gpt4v`

**Screenshot of where to find each:**

**Endpoint & Key:** Azure Portal → Your OpenAI resource → "Keys and Endpoint"
```
┌─────────────────────────────────────────┐
│ Keys and Endpoint                       │
├─────────────────────────────────────────┤
│ KEY 1         [Show Key]  📋            │
│ KEY 2         [Show Key]  📋            │
│                                         │
│ Endpoint      📋                        │
│ https://fruits-quality-openai-001...   │
└─────────────────────────────────────────┘
```

**Deployment:** Azure AI Foundry (ai.azure.com) → Deployments
```
┌────────────────────────────────────────────────────┐
│ Deployments                                        │
├────────────────┬─────────────┬──────────┬─────────┤
│ Name           │ Model       │ Status   │ Actions │
├────────────────┼─────────────┼──────────┼─────────┤
│ fruit-quality- │ gpt-4o      │ ✓Running │ ...     │
│ gpt4v          │             │          │         │
└────────────────┴─────────────┴──────────┴─────────┘
```

### Option B: Using Azure CLI (Faster for Developers)

```powershell
# Install Azure CLI (if not installed)
# Download from: https://aka.ms/installazurecliwindows

# Login
az login

# Set subscription (if you have multiple)
az account set --subscription "YOUR_SUBSCRIPTION_NAME"

# Create resource group
az group create --name rg-fruits-quality-eval --location eastus

# Create Azure OpenAI resource
az cognitiveservices account create `
  --name fruits-quality-openai-001 `
  --resource-group rg-fruits-quality-eval `
  --kind OpenAI `
  --sku S0 `
  --location eastus

# Get endpoint
az cognitiveservices account show `
  --name fruits-quality-openai-001 `
  --resource-group rg-fruits-quality-eval `
  --query properties.endpoint `
  --output tsv

# Get API key
az cognitiveservices account keys list `
  --name fruits-quality-openai-001 `
  --resource-group rg-fruits-quality-eval `
  --query key1 `
  --output tsv
```

## Step 2: Deploy GPT-4V Model

### Using Azure AI Foundry Studio (Portal)

1. **Navigate to AI Foundry**
   - Go to https://ai.azure.com
   - Sign in with same Azure account
   - Create new project or select existing

2. **Deploy Model**
   - Left menu → "Deployments"
   - Click "Create new deployment"
   - **Model:** Select `gpt-4` with vision capability (look for `gpt-4o` or `gpt-4-vision-preview`)
   - **Deployment name:** `fruit-quality-gpt4v` (use this exact name or update .env)
   - **Deployment type:** Standard
   - **Tokens per minute rate limit:** 10K (sufficient for evaluation)
   - Click "Deploy"

3. **Verify Deployment**
   - Deployment should show "Succeeded" status
   - Note the deployment name (needed for .env)

### Using Azure CLI

```powershell
# List available models (find GPT-4V model)
az cognitiveservices account deployment list `
  --name fruits-quality-openai-001 `
  --resource-group rg-fruits-quality-eval

# Create deployment
az cognitiveservices account deployment create `
  --name fruits-quality-openai-001 `
  --resource-group rg-fruits-quality-eval `
  --deployment-name fruit-quality-gpt4v `
  --model-name gpt-4o `
  --model-version "2024-05-13" `
  --model-format OpenAI `
  --sku-capacity 10 `
  --sku-name "Standard"
```

## Step 3: Configure Environment Variables

1. **Update `.env` file in project root:**

```bash
# Azure AI Foundry / OpenAI
AZURE_OPENAI_ENDPOINT=https://fruits-quality-openai-001.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_DEPLOYMENT=fruit-quality-gpt4v
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

2. **Verify credentials are loaded:**

```powershell
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('Endpoint:', os.getenv('AZURE_OPENAI_ENDPOINT'))"
```

## Step 4: Install Dependencies

```powershell
# Activate venv (if not already active)
.venv\Scripts\Activate.ps1

# Install Azure OpenAI SDK
pip install openai>=1.0.0 pillow python-dotenv

# Save dependencies
pip freeze > requirements-eval.txt
```

## Step 5: Test Connection

Run quick connection test:

```powershell
python evaluation/scripts/eval_single_image.py --test-connection
```

Expected output:
```
✓ Azure OpenAI connection successful
Endpoint: https://fruits-quality-openai-001.openai.azure.com/
Deployment: fruit-quality-gpt4v
```

## Troubleshooting

### Issue: "Resource not found" or 404 errors
- **Solution:** Verify deployment name matches exactly in `.env`
- Run: `az cognitiveservices account deployment list --name fruits-quality-openai-001 --resource-group rg-fruits-quality-eval`

### Issue: "Insufficient quota"
- **Solution:** Check token limits in Azure Portal → Deployments → Edit deployment
- Increase tokens per minute (TPM) limit

### Issue: "Model not available in region"
- **Solution:** GPT-4V availability varies by region
- Try regions: East US, Sweden Central, Australia East
- Check availability: https://learn.microsoft.com/azure/ai-services/openai/concepts/models

### Issue: API key not working
- **Solution:** Regenerate key in Azure Portal → Keys and Endpoint → Regenerate Key 1
- Update `.env` file immediately

## Cost Management

**GPT-4V Pricing (approximate):**
- Input (prompt): $0.01 per 1K tokens
- Output (completion): $0.03 per 1K tokens
- Image processing: ~1,200-1,500 tokens per image (depends on resolution)

**Token breakdown per request:**
```
Prompt tokens (input):
  - Image encoding: ~1,200 tokens
  - Text prompt: ~50-100 tokens
  - Total input: ~1,250-1,300 tokens → ~$0.013

Completion tokens (output):
  - Controlled by max_tokens parameter (default: 1,500)
  - Simple prompts: 50-100 tokens → ~$0.002-$0.003
  - Structured JSON: 300-500 tokens → ~$0.009-$0.015
  - Distribution analysis: 800-1,200 tokens → ~$0.024-$0.036
  - Model stops when: (1) reaches max_tokens, (2) completes naturally, (3) hits 4K limit
  - You pay only for tokens actually generated, not the max_tokens ceiling

Total per image:
  - Simple assessment: $0.015-$0.025
  - Structured assessment: $0.025-$0.035
  - Distribution analysis: $0.040-$0.050
```

**Estimated costs for evaluation:**
- Single image: $0.015-$0.050 (depends on prompt complexity)
- 100 images (simple): ~$2.00-$3.00
- 100 images (distribution): ~$4.00-$5.00
- Trial credit: Usually $200 (sufficient for ~4,000-10,000 images)

**Important:** The `max_tokens` parameter in `gpt4v_client.py` (default: 1,500) prevents cost overruns. Increase only if responses are truncated. Lower values may truncate complex JSON responses (watch for incomplete output).

**Monitor usage:**
```powershell
# Check current usage
python evaluation/scripts/eval_single_image.py --show-costs
```

---

## Running Evaluations

### Single Image Evaluation

**Basic evaluation (structured JSON output):**
```powershell
python evaluation/scripts/eval_single_image.py data/samples/apple.jpg
```

**Expected output:**
```
==========================================================
Evaluating: data/samples/apple.jpg
Prompt type: structured
==========================================================

Sending request to GPT-4V...

==========================================================
GPT-4V RESPONSE:
==========================================================
{
  "fruit_type": "apple",
  "freshness_level": "fresh",
  "quality_score": 0.85,
  "visual_indicators": ["bright red color", "smooth skin", "no blemishes"],
  "defects": [],
  "shelf_life_estimate": "7-10 days",
  "recommendation": "sell"
}

==========================================================
USAGE STATISTICS:
==========================================================
Response time: 1234.56 ms
Prompt tokens: 1205
Completion tokens: 87
Total tokens: 1292

Estimated cost: $0.0147 USD
  - Prompt: $0.0121
  - Completion: $0.0026
```

**Use different prompts:**
```powershell
# Simple scoring (just score + reason)
python evaluation/scripts/eval_single_image.py data/samples/apple.jpg --prompt simple

# Defect detection focus
python evaluation/scripts/eval_single_image.py data/samples/apple.jpg --prompt defect

# Comparison to standards
python evaluation/scripts/eval_single_image.py data/samples/apple.jpg --prompt comparison
```

**Save results to file:**
```powershell
python evaluation/scripts/eval_single_image.py data/samples/apple.jpg --output evaluation/results/apple_eval.json
```

---

### Batch Evaluation

**Process all images in a directory:**
```powershell
python evaluation/scripts/eval_batch.py data/samples/
```

**Limit number of images:**
```powershell
# Process only first 10 images
python evaluation/scripts/eval_batch.py data/samples/ --max-images 10
```

**Use specific prompt template:**
```powershell
python evaluation/scripts/eval_batch.py data/samples/ --prompt simple --max-images 5
```

**Expected output:**
```
==========================================================
BATCH EVALUATION
==========================================================
Directory: data/samples/
Prompt type: structured
Max images: 10
==========================================================

Found 10 images to process

[1/10] Processing: apple1.jpg
  ✓ Completed in 1234.56 ms
  Tokens: 1292

[2/10] Processing: banana1.jpg
  ✓ Completed in 1156.23 ms
  Tokens: 1278

... (continues for all images)

==========================================================
BATCH EVALUATION SUMMARY
==========================================================
Total images: 10
Successful: 10
Failed: 0

Average tokens per image: 1285.40
Average response time: 1245.32 ms
Total tokens used: 12854

Total estimated cost: $0.1542 USD
Average cost per image: $0.0154 USD

Results saved to: evaluation/results/batch_results.json
Cost tracking saved to: evaluation/results/cost_analysis.json
```

---

### Compare Methods (Current vs GPT-4V)

**Compare heuristic quality scoring vs GPT-4V:**
```powershell
python evaluation/scripts/compare_methods.py data/samples/apple.jpg
```

**Expected output:**
```
==========================================================
COMPARISON: Current Method vs GPT-4V
==========================================================
Image: data/samples/apple.jpg
==========================================================

Running current quality assessment method...
  Score: 0.72
  Freshness: moderate

Running GPT-4V assessment...
  Score: 0.68
  Freshness: moderate
  Response time: 1345.67 ms
  Cost: $0.0142

==========================================================
COMPARISON ANALYSIS
==========================================================
Score difference: 0.04
Agreement: high

Current method: Fast, deterministic, no API cost
GPT-4V: Slower, contextual, API cost: $0.0142

Results saved to: evaluation/results/comparison.json
```

**With specific bounding box (for detected fruits):**
```powershell
python evaluation/scripts/compare_methods.py data/samples/shelf.jpg --bbox 100 150 300 450
```

---

### View Cost Summary

**See total costs across all evaluation sessions:**
```powershell
python evaluation/scripts/eval_single_image.py --show-costs
```

**Expected output:**
```
==========================================================
COST SUMMARY (All Evaluations)
==========================================================
Total sessions: 3
Total requests: 35
Total tokens: 43750
Total cost: $0.5425 USD
Avg per request: $0.015500 USD

Session Breakdown:
  - single_image_apple: 1 requests, $0.0147
  - batch_samples: 25 requests, $0.3876
  - single_image_banana: 1 requests, $0.0142
```

---

### Available Prompt Templates

**structured** (default) - Detailed JSON response with quality score, defects, recommendations
```powershell
python evaluation/scripts/eval_single_image.py image.jpg --prompt structured
```

**simple** - Quick score (0.0-1.0) with brief explanation
```powershell
python evaluation/scripts/eval_single_image.py image.jpg --prompt simple
```

**batch** - Assess multiple fruits in one image
```powershell
python evaluation/scripts/eval_single_image.py shelf_image.jpg --prompt batch
```

**defect** - Focus on identifying defects and quality issues
```powershell
python evaluation/scripts/eval_single_image.py image.jpg --prompt defect
```

**comparison** - Compare to retail standards with pass/fail grade
```powershell
python evaluation/scripts/eval_single_image.py image.jpg --prompt comparison
```

**distribution** - Statistical analysis with fruit type distribution and quality percentages
```powershell
python evaluation/scripts/eval_single_image.py shelf_image.jpg --prompt distribution
```

---

## Next Steps

After completing setup and running initial evaluations:

1. **Analyze results** - Review generated JSON files in `evaluation/results/`
2. **Review costs** - Check `cost_analysis.json` for budget tracking
3. **Follow 2-day plan** - See [evaluation/README.md](../README.md) for full evaluation timeline
4. **Compare methods** - Run comparison script to understand GPT-4V vs current approach
5. **Create backlog** - Document findings and create Azure DevOps features

See [Execution Guide](../../docs/execution_guide.md#azure-ai-foundry-evaluation) for additional scenarios and troubleshooting.
