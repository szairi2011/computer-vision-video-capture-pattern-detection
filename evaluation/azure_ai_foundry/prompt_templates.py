"""Prompt templates for GPT-4V fruit quality assessment."""

# Structured quality assessment prompt
QUALITY_ASSESSMENT_STRUCTURED = """You are a fruit quality inspection expert. Analyze this image and provide a structured quality assessment.

Respond in JSON format with the following structure:
{
  "fruit_type": "apple|banana|orange|etc",
  "freshness_level": "fresh|moderate|poor|rotten",
  "quality_score": 0.0-1.0 (float),
  "visual_indicators": ["list", "of", "observed", "features"],
  "defects": ["list", "of", "defects", "if any"],
  "shelf_life_estimate": "estimated days remaining",
  "recommendation": "sell|discount|discard"
}

Consider:
- Skin color and uniformity
- Surface blemishes or bruises
- Signs of decay or mold
- Overall appearance and marketability

Provide only the JSON response, no additional text."""

# Simple scoring prompt
QUALITY_ASSESSMENT_SIMPLE = """Analyze this fruit image and rate its quality on a scale of 0.0 (rotten/inedible) to 1.0 (perfect/fresh).

Provide your response in this exact format:
SCORE: [0.0-1.0]
REASON: [brief explanation]
FRESHNESS: [fresh/moderate/poor/rotten]"""

# Comparative assessment (for multiple fruits in one image)
QUALITY_ASSESSMENT_BATCH = """You are inspecting a shelf display of fruits. For each visible fruit, assess its quality.

Respond in JSON format:
{
  "total_fruits": number,
  "fruits": [
    {
      "index": 1,
      "fruit_type": "type",
      "quality_score": 0.0-1.0,
      "freshness_level": "fresh|moderate|poor|rotten",
      "position": "description of location in image"
    }
  ],
  "average_quality": 0.0-1.0,
  "recommendation": "overall shelf quality assessment"
}

Only JSON response, no additional text."""

# Defect detection focus
DEFECT_DETECTION = """Identify all visible defects or quality issues in this fruit image.

List each defect with:
- Type (bruise, mold, discoloration, cut, etc.)
- Severity (minor, moderate, severe)
- Location (approximate position on fruit)

If no defects found, respond with "No defects detected - fruit appears fresh."""

# Comparison prompt (for A/B testing different assessment methods)
COMPARISON_PROMPT = """Compare the quality of fruits in this image to typical supermarket standards.

Respond with:
1. Pass/Fail for retail sale
2. Quality grade (A/B/C/D)
3. Key decision factors
4. Suggested action (display, discount, remove)

Be concise and actionable."""

# Distribution analysis prompt (statistical overview by fruit type and quality)
DISTRIBUTION_ANALYSIS = """Analyze the distribution of fruits in this image and provide statistical insights.

Respond in JSON format:
{
  "total_fruits": number,
  "detected_fruit_types": ["list of all unique fruit types found"],
  "statistics_by_fruit_type": [
    {
      "fruit_name": "apple|banana|orange|etc",
      "count": number,
      "percentage_of_total": percentage,
      "quality_distribution": {
        "fresh": {"count": number, "percentage": percentage},
        "moderate": {"count": number, "percentage": percentage},
        "poor": {"count": number, "percentage": percentage},
        "rotten": {"count": number, "percentage": percentage}
      },
      "average_quality_score": 0.0-1.0
    }
  ],
  "overall_quality_distribution": {
    "fresh": {"count": number, "percentage": percentage},
    "moderate": {"count": number, "percentage": percentage},
    "poor": {"count": number, "percentage": percentage},
    "rotten": {"count": number, "percentage": percentage}
  },
  "summary": "brief textual summary of findings"
}

Important: Calculate average_quality_score using this formula:
average_quality_score = (fresh_count × 1.0 + moderate_count × 0.5 + poor_count × 0.25 + rotten_count × 0.0) / total_count

Where:
- fresh = 1.0 (perfect condition)
- moderate = 0.5 (good, sellable)
- poor = 0.25 (needs discount)
- rotten = 0.0 (discard)

Example:
If image contains 3 apples (2 fresh, 1 moderate) and 2 bananas (1 fresh, 1 rotten):
{
  "total_fruits": 5,
  "detected_fruit_types": ["apple", "banana"],
  "statistics_by_fruit_type": [
    {
      "fruit_name": "apple",
      "count": 3,
      "percentage_of_total": 60.0,
      "quality_distribution": {
        "fresh": {"count": 2, "percentage": 66.7},
        "moderate": {"count": 1, "percentage": 33.3},
        "poor": {"count": 0, "percentage": 0.0},
        "rotten": {"count": 0, "percentage": 0.0}
      },
      "average_quality_score": 0.83
    },
    {
      "fruit_name": "banana",
      "count": 2,
      "percentage_of_total": 40.0,
      "quality_distribution": {
        "fresh": {"count": 1, "percentage": 50.0},
        "moderate": {"count": 0, "percentage": 0.0},
        "poor": {"count": 0, "percentage": 0.0},
        "rotten": {"count": 1, "percentage": 50.0}
      },
      "average_quality_score": 0.50
    }
  ],
  "overall_quality_distribution": {
    "fresh": {"count": 3, "percentage": 60.0},
    "moderate": {"count": 1, "percentage": 20.0},
    "poor": {"count": 0, "percentage": 0.0},
    "rotten": {"count": 1, "percentage": 20.0}
  },
  "summary": "Mixed quality shelf with 60% fresh fruits. Apples generally better condition than bananas."
}

Provide only the JSON response, no additional text."""


def get_prompt(prompt_type: str = "structured") -> str:
    """
    Get prompt template by type.
    
    Args:
        prompt_type: One of 'structured', 'simple', 'batch', 'defect', 'comparison', 'distribution'
        
    Returns:
        Prompt template string
    """
    prompts = {
        "structured": QUALITY_ASSESSMENT_STRUCTURED,
        "simple": QUALITY_ASSESSMENT_SIMPLE,
        "batch": QUALITY_ASSESSMENT_BATCH,
        "defect": DEFECT_DETECTION,
        "comparison": COMPARISON_PROMPT,
        "distribution": DISTRIBUTION_ANALYSIS
    }
    
    return prompts.get(prompt_type, QUALITY_ASSESSMENT_STRUCTURED)
