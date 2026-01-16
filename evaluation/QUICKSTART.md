# Azure AI Foundry Evaluation - Quick Start Checklist

**Branch:** `azure-ai-foundry`  
**Time:** 1-2 days  
**Goal:** Evaluate GPT-4V for fruit quality assessment

---

## ✅ Pre-Flight Checklist

### Day 1 Morning (Setup - 3 hours)

- [ ] **1. Verify you're on evaluation branch**
  ```powershell
  git branch  # Should show: * azure-ai-foundry
  ```

- [ ] **2. Install dependencies**
  ```powershell
  .venv\Scripts\Activate.ps1
  pip install openai>=1.0.0 pillow
  pip freeze > requirements-eval.txt
  ```

- [ ] **3. Create Azure OpenAI resource**
  
  **Detailed navigation:**
  1. Go to https://portal.azure.com
  2. Click **☰ menu** (top-left) → **"Create a resource"**
  3. Search: **`Azure OpenAI`** → Select it → Click **"Create"**
  4. Configure:
     - Subscription: (your trial/paid subscription)
     - Resource Group: Click **"Create new"** → Name: `rg-fruits-quality-eval`
     - Region: **East US** (best GPT-4V availability)
     - Name: `fruits-quality-openai-001` (must be globally unique)
     - Pricing: **Standard S0**
  5. Click **"Review + create"** → **"Create"**
  6. Wait 2-4 minutes → Click **"Go to resource"**
  7. Left menu → **"Keys and Endpoint"**
     - Copy **Endpoint** URL (click 📋)
     - Click **"Show Key"** for KEY 1 → Copy (click 📋)

- [ ] **4. Deploy GPT-4V model**
  
  **Detailed navigation:**
  1. Go to https://ai.azure.com (sign in with same account)
  2. Create project if prompted:
     - Name: `FruitsQualityEval`
     - Select your OpenAI resource: `fruits-quality-openai-001`
  3. Left sidebar → **"Deployments"** → Click **"+ Create deployment"**
  4. Configure:
     - Model family: **gpt-4**
     - Model: **`gpt-4o`** (preferred) or **`gpt-4-vision-preview`**
     - Deployment name: `fruit-quality-gpt4v` (exact name)
     - Deployment type: **Standard**
     - Tokens per minute: **10** (= 10K TPM)
  5. Click **"Deploy"** → Wait 30-60 seconds
  6. Verify status shows: **✓ Running** (green checkmark)

- [ ] **5. Configure .env file**
  ```bash
  AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
  AZURE_OPENAI_API_KEY=your-key-here
  AZURE_OPENAI_DEPLOYMENT=fruit-quality-gpt4v
  AZURE_OPENAI_API_VERSION=2024-02-15-preview
  ```

- [ ] **6. Test connection**
  ```powershell
  python evaluation/scripts/eval_single_image.py --test-connection
  ```
  Expected: `✓ Connection successful`

---

### Day 1 Afternoon (First Tests - 3 hours)

- [ ] **7. Test single image**
  ```powershell
  python evaluation/scripts/eval_single_image.py data/samples/apple.jpg
  ```
  Expected: JSON response with quality score

- [ ] **8. Try different prompts**
  ```powershell
  python evaluation/scripts/eval_single_image.py data/samples/apple.jpg --prompt simple
  python evaluation/scripts/eval_single_image.py data/samples/apple.jpg --prompt defect
  ```

- [ ] **9. Run batch evaluation (10 images)**
  ```powershell
  python evaluation/scripts/eval_batch.py data/samples/ --max-images 10
  ```

- [ ] **10. Check costs**
  ```powershell
  python evaluation/scripts/eval_single_image.py --show-costs
  ```
  Expected: ~$0.30 for 10 images

- [ ] **11. Compare methods**
  ```powershell
  python evaluation/scripts/compare_methods.py data/samples/apple.jpg
  ```

---

### Day 2 Morning (Analysis - 3 hours)

- [ ] **12. Test all prompt types**
  - structured (JSON output)
  - simple (score + reason)
  - batch (multiple fruits)
  - defect (defect focus)
  - comparison (A/B grading)

- [ ] **13. Edge case testing**
  - Poor quality images
  - Multiple fruits in frame
  - Different lighting
  - Various fruit types

- [ ] **14. Collect performance metrics**
  - Average response time
  - Token usage per image
  - Cost per 100 images (extrapolate)
  - Review: `evaluation/results/cost_analysis.json`

---

### Day 2 Afternoon (Backlog - 3 hours)

- [ ] **15. Document findings**
  Create document with:
  - Quality scoring accuracy
  - Response times
  - Cost projections
  - Limitations discovered

- [ ] **16. Create backlog items**
  Features to consider:
  - Basic GPT-4V integration (8-13 SP)
  - Hybrid strategy (13-21 SP)
  - Cost optimization (5-8 SP)
  - Prompt engineering (5-8 SP)

- [ ] **17. Prepare demo**
  - Screenshots of comparisons
  - Cost analysis
  - Recommendation (integrate/hybrid/skip)

---

## 🎯 Success Metrics

By end of Day 2, you should have:

✅ **Working integration:** GPT-4V quality assessment functional  
✅ **Data:** 30-50 images evaluated  
✅ **Costs:** Total spent + per-image cost calculated  
✅ **Performance:** Response time metrics collected  
✅ **Comparison:** Current vs GPT-4V analysis complete  
✅ **Backlog:** Features identified with effort estimates  
✅ **Recommendation:** Clear decision on integration approach  

---

## 📊 Expected Outcomes

**Cost Data:**
- Per image: $0.02-$0.04
- 100 images: ~$2-$4
- 1000 images: ~$20-$40

**Performance:**
- Response time: 1-2 seconds per image
- Current method: <50ms per image

**Quality:**
- GPT-4V provides reasoning
- Detects subtle defects
- Context-aware assessment

---

## 🆘 Quick Troubleshooting

**Connection failed?**
```powershell
# Check credentials
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('AZURE_OPENAI_ENDPOINT'))"
```

**404 errors?**
```powershell
# Verify deployment name
az cognitiveservices account deployment list `
  --name fruits-quality-openai-001 `
  --resource-group rg-fruits-quality-eval
```

**Quota exceeded?**
- Azure Portal → Your OpenAI → Deployments → Edit → Increase TPM

---

## 📚 Documentation

**Detailed setup:** `evaluation/azure_ai_foundry/setup_guide.md`  
**Execution guide:** `docs/execution_guide.md#azure-ai-foundry-evaluation`  
**Full plan:** `evaluation/README.md`  

---

## 🚀 Start Now

```powershell
# Step 1: Test connection
python evaluation/scripts/eval_single_image.py --test-connection

# Step 2: First evaluation
python evaluation/scripts/eval_single_image.py data/samples/apple.jpg

# Step 3: View results and costs
python evaluation/scripts/eval_single_image.py --show-costs
```

**Good luck with the evaluation! 🎉**
