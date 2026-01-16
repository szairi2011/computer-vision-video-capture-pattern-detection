"""Batch evaluation script for testing multiple images with GPT-4V."""

import sys
import json
from pathlib import Path
from time import time
from typing import List

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from evaluation.azure_ai_foundry.gpt4v_client import GPT4VisionClient
from evaluation.azure_ai_foundry.prompt_templates import get_prompt
from evaluation.azure_ai_foundry.cost_tracker import CostTracker


def evaluate_batch(
    image_dir: str,
    prompt_type: str = "structured",
    max_images: int = None,
    output_file: str = "evaluation/results/batch_results.json"
):
    """
    Evaluate multiple images in batch.
    
    Args:
        image_dir: Directory containing fruit images
        prompt_type: Prompt template to use
        max_images: Maximum number of images to process (None = all)
        output_file: Path to save results
    """
    print(f"\n{'='*60}")
    print(f"BATCH EVALUATION")
    print(f"{'='*60}")
    print(f"Directory: {image_dir}")
    print(f"Prompt type: {prompt_type}")
    print(f"Max images: {max_images or 'unlimited'}")
    print(f"{'='*60}\n")
    
    # Find all image files
    image_path = Path(image_dir)
    if not image_path.exists():
        print(f"✗ Error: Directory not found: {image_dir}")
        return
    
    # Supported image formats
    extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp']
    image_files: List[Path] = []
    for ext in extensions:
        image_files.extend(image_path.glob(ext))
    
    if not image_files:
        print(f"✗ No images found in {image_dir}")
        return
    
    # Limit if specified
    if max_images:
        image_files = image_files[:max_images]
    
    print(f"Found {len(image_files)} images to process\n")
    
    # Initialize
    client = GPT4VisionClient()
    prompt = get_prompt(prompt_type)
    tracker = CostTracker()
    
    tracker.start_session(
        session_name=f"batch_{Path(image_dir).name}",
        description=f"Batch evaluation of {len(image_files)} images"
    )
    
    results = []
    
    # Process each image
    for idx, image_file in enumerate(image_files, 1):
        print(f"[{idx}/{len(image_files)}] Processing: {image_file.name}")
        
        start_time = time()
        
        try:
            result = client.assess_quality(str(image_file), prompt)
            response_time_ms = (time() - start_time) * 1000
            
            # Log to tracker
            tracker.log_request(
                image_path=str(image_file),
                prompt_tokens=result["usage"]["prompt_tokens"],
                completion_tokens=result["usage"]["completion_tokens"],
                total_tokens=result["usage"]["total_tokens"],
                response_time_ms=response_time_ms,
                model=result["model"]
            )
            
            # Store result
            results.append({
                "image": str(image_file),
                "image_name": image_file.name,
                "response": result["content"],
                "usage": result["usage"],
                "response_time_ms": response_time_ms,
                "success": True
            })
            
            print(f"  ✓ Completed in {response_time_ms:.2f} ms")
            print(f"  Tokens: {result['usage']['total_tokens']}")
            
        except Exception as e:
            print(f"  ✗ Error: {e}")
            results.append({
                "image": str(image_file),
                "image_name": image_file.name,
                "error": str(e),
                "success": False
            })
        
        print()  # Blank line between images
    
    # End session
    tracker.end_session()
    
    # Summary statistics
    print(f"\n{'='*60}")
    print("BATCH EVALUATION SUMMARY")
    print(f"{'='*60}")
    
    successful = sum(1 for r in results if r["success"])
    failed = len(results) - successful
    
    print(f"Total images: {len(results)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    
    if successful > 0:
        total_tokens = sum(r["usage"]["total_tokens"] for r in results if r["success"])
        avg_tokens = total_tokens / successful
        
        response_times = [r["response_time_ms"] for r in results if r["success"]]
        avg_time = sum(response_times) / len(response_times)
        
        print(f"\nAverage tokens per image: {avg_tokens:.2f}")
        print(f"Average response time: {avg_time:.2f} ms")
        print(f"Total tokens used: {total_tokens}")
        
        # Cost estimate
        cost = client.get_cost_estimate()
        print(f"\nTotal estimated cost: ${cost['estimated_cost_usd']:.4f} USD")
        print(f"Average cost per image: ${cost['estimated_cost_usd']/successful:.4f} USD")
    
    # Save results
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    output_data = {
        "batch_info": {
            "directory": image_dir,
            "prompt_type": prompt_type,
            "total_images": len(results),
            "successful": successful,
            "failed": failed
        },
        "results": results,
        "cost_summary": client.get_cost_estimate() if successful > 0 else None
    }
    
    with open(output_path, 'w') as f:
        json.dump(output_data, f, indent=2)
    
    print(f"\nResults saved to: {output_file}")
    print(f"Cost tracking saved to: evaluation/results/cost_analysis.json")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Batch evaluate multiple fruit images")
    parser.add_argument(
        'image_dir',
        help='Directory containing fruit images'
    )
    parser.add_argument(
        '--prompt',
        choices=['structured', 'simple', 'batch', 'defect', 'comparison', 'distribution'],
        default='structured',
        help='Prompt template to use'
    )
    parser.add_argument(
        '--max-images',
        type=int,
        help='Maximum number of images to process'
    )
    parser.add_argument(
        '--output',
        default='evaluation/results/batch_results.json',
        help='Output file for results'
    )
    
    args = parser.parse_args()
    
    evaluate_batch(
        image_dir=args.image_dir,
        prompt_type=args.prompt,
        max_images=args.max_images,
        output_file=args.output
    )


if __name__ == "__main__":
    main()
