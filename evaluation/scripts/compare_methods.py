"""Compare current heuristic quality scoring vs GPT-4V assessment."""

import sys
import json
from pathlib import Path
from time import time
from typing import Dict

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from evaluation.azure_ai_foundry.gpt4v_client import GPT4VisionClient
from evaluation.azure_ai_foundry.prompt_templates import get_prompt

# Import existing quality assessment (if available)
try:
    from src.quality.score import assess_freshness
    from src.vision.detect import FruitDetector, Detection
    CURRENT_METHOD_AVAILABLE = True
except ImportError:
    CURRENT_METHOD_AVAILABLE = False
    print("Warning: Current quality assessment not available. Will only show GPT-4V results.")


def compare_single_image(image_path: str, detection_bbox: tuple = None):
    """
    Compare current method vs GPT-4V for single image.
    
    Args:
        image_path: Path to fruit image
        detection_bbox: Optional bounding box (x1, y1, x2, y2) for current method
    """
    print(f"\n{'='*60}")
    print(f"COMPARISON: Current Method vs GPT-4V")
    print(f"{'='*60}")
    print(f"Image: {image_path}")
    print(f"{'='*60}\n")
    
    results = {
        "image": image_path,
        "current_method": None,
        "gpt4v": None,
        "comparison": None
    }
    
    # Method 1: Current heuristic approach
    if CURRENT_METHOD_AVAILABLE:
        print("Running current quality assessment method...")
        try:
            import cv2
            frame = cv2.imread(image_path)
            
            # If bbox provided, use it; otherwise use full image
            if detection_bbox:
                x1, y1, x2, y2 = detection_bbox
                roi = frame[y1:y2, x1:x2]
            else:
                roi = frame
            
            # Create mock detection for assessment
            detection = Detection(
                bbox=detection_bbox or (0, 0, frame.shape[1], frame.shape[0]),
                label="fruit",
                confidence=1.0
            )
            
            current_result = assess_freshness(detection, frame)
            
            results["current_method"] = {
                "freshness_level": current_result.freshness_level,
                "score": current_result.score,
                "method": "color/texture heuristics"
            }
            
            print(f"  Score: {current_result.score:.2f}")
            print(f"  Freshness: {current_result.freshness_level}")
            
        except Exception as e:
            print(f"  ✗ Error: {e}")
            results["current_method"] = {"error": str(e)}
    else:
        print("Current method not available (skipped)")
    
    # Method 2: GPT-4V
    print("\nRunning GPT-4V assessment...")
    client = GPT4VisionClient()
    prompt = get_prompt("simple")  # Use simple prompt for easier comparison
    
    try:
        start_time = time()
        gpt4v_result = client.assess_quality(image_path, prompt)
        response_time = (time() - start_time) * 1000
        
        # Parse GPT-4V response (looking for SCORE and FRESHNESS)
        response_text = gpt4v_result["content"]
        score = None
        freshness = None
        
        for line in response_text.split('\n'):
            if 'SCORE:' in line.upper():
                try:
                    score = float(line.split(':')[1].strip())
                except:
                    pass
            if 'FRESHNESS:' in line.upper():
                freshness = line.split(':')[1].strip().lower()
        
        results["gpt4v"] = {
            "score": score,
            "freshness_level": freshness,
            "full_response": response_text,
            "response_time_ms": response_time,
            "tokens": gpt4v_result["usage"]["total_tokens"],
            "cost_usd": client.get_cost_estimate()["estimated_cost_usd"]
        }
        
        print(f"  Score: {score}")
        print(f"  Freshness: {freshness}")
        print(f"  Response time: {response_time:.2f} ms")
        print(f"  Cost: ${results['gpt4v']['cost_usd']:.4f}")
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
        results["gpt4v"] = {"error": str(e)}
    
    # Comparison analysis
    if results["current_method"] and results["gpt4v"]:
        print(f"\n{'='*60}")
        print("COMPARISON ANALYSIS")
        print(f"{'='*60}")
        
        current_score = results["current_method"].get("score")
        gpt4v_score = results["gpt4v"].get("score")
        
        if current_score is not None and gpt4v_score is not None:
            diff = abs(current_score - gpt4v_score)
            
            results["comparison"] = {
                "score_difference": diff,
                "agreement_level": "high" if diff < 0.2 else "medium" if diff < 0.4 else "low",
                "current_faster": True,  # Heuristics always faster
                "gpt4v_more_detailed": True  # GPT-4V provides reasoning
            }
            
            print(f"Score difference: {diff:.2f}")
            print(f"Agreement: {results['comparison']['agreement_level']}")
            print(f"\nCurrent method: Fast, deterministic, no API cost")
            print(f"GPT-4V: Slower, contextual, API cost: ${results['gpt4v']['cost_usd']:.4f}")
    
    return results


def generate_comparison_report(results_list: list, output_file: str):
    """Generate comparison report from multiple evaluations."""
    report = {
        "summary": {
            "total_comparisons": len(results_list),
            "avg_score_difference": 0,
            "agreement_distribution": {"high": 0, "medium": 0, "low": 0}
        },
        "details": results_list
    }
    
    # Calculate statistics
    valid_comparisons = [r for r in results_list if r.get("comparison")]
    if valid_comparisons:
        diffs = [r["comparison"]["score_difference"] for r in valid_comparisons]
        report["summary"]["avg_score_difference"] = sum(diffs) / len(diffs)
        
        for comp in valid_comparisons:
            level = comp["comparison"]["agreement_level"]
            report["summary"]["agreement_distribution"][level] += 1
    
    # Save report
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\nComparison report saved to: {output_file}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Compare quality assessment methods")
    parser.add_argument(
        'image',
        help='Path to fruit image'
    )
    parser.add_argument(
        '--bbox',
        nargs=4,
        type=int,
        metavar=('x1', 'y1', 'x2', 'y2'),
        help='Bounding box coordinates for current method'
    )
    parser.add_argument(
        '--output',
        default='evaluation/results/comparison.json',
        help='Output file for comparison results'
    )
    
    args = parser.parse_args()
    
    # Verify image exists
    if not Path(args.image).exists():
        print(f"✗ Error: Image not found: {args.image}")
        sys.exit(1)
    
    # Run comparison
    bbox = tuple(args.bbox) if args.bbox else None
    results = compare_single_image(args.image, bbox)
    
    # Save results
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to: {args.output}")


if __name__ == "__main__":
    main()
