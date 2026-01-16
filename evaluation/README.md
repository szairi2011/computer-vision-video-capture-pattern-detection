# Azure AI Foundry Evaluation - 2-Day Sprint Plan

**Branch:** `azure-ai-foundry` (temporary evaluation branch)

**Goal:** Rapid hands-on evaluation of Azure AI Foundry GPT-4V for intelligent fruit quality assessment to inform backlog creation and effort estimation.

---

## What is Azure AI Foundry?

Azure AI Foundry (formerly Azure AI Studio) provides:
- **GPT-4V (Vision)** - Image understanding and quality assessment via natural language prompts
- **Semantic capabilities** - Context-aware analysis vs. heuristic rules
- **Prompt engineering** - Customizable assessment criteria
- **Azure integration** - Native Azure ecosystem compatibility

**Key Difference from Current Approach:**
- Current: Color/texture heuristics (fast, deterministic, offline)
- GPT-4V: AI-powered analysis (slower, contextual, requires API, more detailed reasoning)

---

## 2-Day Evaluation Timeline

### Day 1: Setup + Basic Integration (6-8 hours)

#### Morning (3-4 hours): Azure Setup

**9:00-9:30** - Create Azure OpenAI resource
- Portal: https://portal.azure.com → "Azure OpenAI"
- Resource group: `rg-fruits-quality-eval`
- Region: East US (GPT-4V available)
- Name: `fruits-quality-openai-001`

**9:30-10:00** - Deploy GPT-4V model
- Go to: https://ai.azure.com
- Deploy `gpt-4o` model
- Deployment name: `fruit-quality-gpt4v`
- Token limit: 10K TPM

**10:00-11:00** - Configure project
```powershell
# Install dependencies
pip install openai>=1.0.0 pillow

# Update .env with credentials
# AZURE_OPENAI_ENDPOINT=...
# AZURE_OPENAI_API_KEY=...

# Test connection
python evaluation/scripts/eval_single_image.py --test-connection
```

**11:00-13:00** - First evaluations
```powershell
# Test single image
python evaluation/scripts/eval_single_image.py data/samples/apple.jpg

# Try different prompts
python evaluation/scripts/eval_single_image.py data/samples/banana.jpg --prompt simple
python evaluation/scripts/eval_single_image.py data/samples/orange.jpg --prompt defect
```

**Deliverable:** Working GPT-4V quality assessment for single images

---

#### Afternoon (3-4 hours): Batch Testing

**14:00-16:00** - Batch evaluation
```powershell
# Process 10 images
python evaluation/scripts/eval_batch.py data/samples/ --max-images 10

# Check costs
python evaluation/scripts/eval_single_image.py --show-costs
```

**16:00-18:00** - Method comparison
```powershell
# Compare current vs. GPT-4V
python evaluation/scripts/compare_methods.py data/samples/apple.jpg
python evaluation/scripts/compare_methods.py data/samples/banana.jpg
```

**Analysis:**
- Score agreement level
- Response time differences
- Cost per image
- Quality of reasoning

**Deliverable:** Comparison data showing differences between methods

---

### Day 2: Analysis + Backlog Creation (6-8 hours)

#### Morning (3-4 hours): Advanced Testing

**9:00-10:30** - Prompt engineering experiments
```powershell
# Test all prompt templates
for prompt in structured simple batch defect comparison; do
  python evaluation/scripts/eval_single_image.py data/samples/test.jpg --prompt $prompt
done
```

**10:30-12:00** - Edge case testing
- Batch images (multiple fruits in one frame)
- Poor quality images
- Different fruit types
- Various lighting conditions

**12:00-13:00** - Performance benchmarking
- Response times (avg, min, max)
- Token usage patterns
- Cost per 100 images extrapolation

**Deliverable:** Performance metrics and cost projections

---

#### Afternoon (3-4 hours): Documentation + Backlog

**14:00-15:30** - Create comparison report

Document:
1. **Capabilities discovered**
   - Quality scoring accuracy
   - Defect detection precision
   - Reasoning quality
   - Multi-fruit handling

2. **Limitations found**
   - Response time (1-2 seconds vs instant)
   - API dependency (internet required)
   - Cost considerations (~$0.02 per image)
   - Rate limits (10K TPM)

3. **Integration opportunities**
   - Replace heuristic scoring entirely
   - Hybrid approach (fast pre-filter + GPT-4V for edge cases)
   - Validation layer (double-check heuristic results)
   - Training data generation (use GPT-4V to label images)

**15:30-17:00** - Backlog creation

**Epic: GPT-4V Quality Assessment Integration**

**Feature 1: Basic GPT-4V Integration**
- Story 1.1: Create GPT-4V service adapter (ISemanticQuery interface)
- Story 1.2: Implement prompt templates with configuration
- Story 1.3: Add cost tracking to service layer
- Story 1.4: Wire into orchestration pipeline
- **Estimate:** 8-13 story points (1-2 weeks)

**Feature 2: Hybrid Assessment Strategy**
- Story 2.1: Implement fast heuristic pre-filter
- Story 2.2: GPT-4V validation for uncertain cases (score 0.3-0.7)
- Story 2.3: Fallback logic when API unavailable
- Story 2.4: A/B testing framework
- **Estimate:** 13-21 story points (2-3 weeks)

**Feature 3: Cost Optimization**
- Story 3.1: Image compression before API submission
- Story 3.2: Response caching for similar images
- Story 3.3: Batch API calls (if available)
- Story 3.4: Budget alerts and rate limiting
- **Estimate:** 5-8 story points (1 week)

**Feature 4: Prompt Engineering**
- Story 4.1: A/B test prompt variations
- Story 4.2: Fine-tune for specific fruit types
- Story 4.3: Multi-language support
- Story 4.4: Standardized output schema validation
- **Estimate:** 5-8 story points (1 week)

**17:00-18:00** - Demo preparation
- Screenshots of comparisons
- Cost analysis charts
- Performance metrics summary
- Recommendation: Full/Hybrid/Skip integration

**Deliverable:** Backlog items with estimates + demo slides

---

## Quick Reference Commands

### Setup
```powershell
# Test connection
python evaluation/scripts/eval_single_image.py --test-connection

# View costs
python evaluation/scripts/eval_single_image.py --show-costs
```

### Single Image
```powershell
# Default (structured JSON)
python evaluation/scripts/eval_single_image.py data/samples/apple.jpg

# Simple scoring
python evaluation/scripts/eval_single_image.py data/samples/apple.jpg --prompt simple

# Defect detection
python evaluation/scripts/eval_single_image.py data/samples/apple.jpg --prompt defect

# Save results
python evaluation/scripts/eval_single_image.py data/samples/apple.jpg --output results/apple.json
```

### Batch
```powershell
# All images
python evaluation/scripts/eval_batch.py data/samples/

# Limited
python evaluation/scripts/eval_batch.py data/samples/ --max-images 10
```

### Comparison
```powershell
# Current vs GPT-4V
python evaluation/scripts/compare_methods.py data/samples/apple.jpg
```

---

## Success Criteria

**After 2 days, you should have:**

✅ GPT-4V working with your Azure subscription  
✅ Quality assessments for 20-50 sample images  
✅ Cost data: total spent, per-image cost, extrapolation to 1K/10K images  
✅ Performance data: avg response time, token usage  
✅ Comparison analysis: GPT-4V vs current heuristics  
✅ Understanding of prompt engineering impact  
✅ Backlog items with effort estimates  
✅ Recommendation: integrate, hybrid, or skip  
✅ Demo-ready results for stakeholders  

---

## Cost Estimates

**GPT-4V Pricing:**
- Input: $0.01 per 1K tokens (~1000-1500 tokens per image)
- Output: $0.03 per 1K tokens (~100-200 tokens per response)
- **Per image:** ~$0.02-$0.04

**Evaluation costs:**
- Day 1 (20 images): ~$0.50
- Day 2 (30 images): ~$0.75
- **Total for 2-day eval:** ~$1.25 USD

**Your trial credit:** $200 (plenty of budget)

---

## Isolation from Main Project

**Evaluation folder structure:**
```
evaluation/                     # Completely isolated
├── azure_ai_foundry/          # Module
│   ├── gpt4v_client.py        # GPT-4V wrapper
│   ├── prompt_templates.py    # Prompts
│   ├── cost_tracker.py        # Cost tracking
│   └── setup_guide.md         # Detailed setup
├── scripts/                    # Executables
│   ├── eval_single_image.py   # Single image test
│   ├── eval_batch.py          # Batch processing
│   └── compare_methods.py     # Method comparison
└── results/                    # Generated outputs
    ├── batch_results.json
    ├── cost_analysis.json
    └── comparison.json
```

**No interference with:**
- `src/` - Main application code (untouched)
- `tests/` - Existing tests (unchanged)
- Current pipeline (still works independently)

---

## Next Steps After Evaluation

1. **Review results** with team
2. **Present comparison** (current vs GPT-4V)
3. **Decide integration approach:**
   - **Full replacement:** Use GPT-4V for all quality assessment
   - **Hybrid:** Heuristics first, GPT-4V for uncertain cases
   - **Skip:** Current method sufficient, GPT-4V too expensive/slow
4. **Create features** in Azure DevOps
5. **Estimate effort** based on evaluation learnings
6. **Plan sprint** if integration approved

---

## Documentation

**Setup:** [evaluation/azure_ai_foundry/setup_guide.md](evaluation/azure_ai_foundry/setup_guide.md)  
**Execution:** [docs/execution_guide.md#azure-ai-foundry-evaluation](docs/execution_guide.md#azure-ai-foundry-evaluation)  
**Integration:** [docs/setup_guide.md#azure-ai-foundry-evaluation-setup](docs/setup_guide.md#azure-ai-foundry-evaluation-setup)  

**Ready to start? Begin with setup:**
```powershell
python evaluation/scripts/eval_single_image.py --test-connection
```
