"""Single image evaluation script for GPT-4V quality assessment."""

import sys
import json
import argparse
from pathlib import Path
from time import time

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from evaluation.azure_ai_foundry.gpt4v_client import GPT4VisionClient
from evaluation.azure_ai_foundry.prompt_templates import get_prompt
from evaluation.azure_ai_foundry.cost_tracker import CostTracker


def test_connection():
    """Test Azure OpenAI connection."""
    print("Testing Azure OpenAI connection...")
    try:
        client = GPT4VisionClient()
        print(f"✓ Connection successful")
        print(f"Endpoint: {client.endpoint}")
        print(f"Deployment: {client.deployment}")
        return True
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        return False


def evaluate_image(
    image_path: str,
    prompt_type: str = "structured",
    output_file: str = None,
    track_costs: bool = True
):
    """
    Evaluate single fruit image with GPT-4V.
    
    Args:
        image_path: Path to image file
        prompt_type: Prompt template to use
        output_file: Optional file to save results
        track_costs: Whether to track API costs
    """
    print(f"\n{'='*60}")
    print(f"Evaluating: {image_path}")
    print(f"Prompt type: {prompt_type}")
    print(f"{'='*60}\n")
    
    # Initialize client
    client = GPT4VisionClient()
    prompt = get_prompt(prompt_type)
    
    # Track costs if enabled
    tracker = None
    if track_costs:
        tracker = CostTracker()
        tracker.start_session(
            session_name=f"single_image_{Path(image_path).stem}",
            description=f"Evaluation of {image_path} with {prompt_type} prompt"
        )
    
    # Run assessment
    print("Sending request to GPT-4V...")
    start_time = time()
    
    try:
        result = client.assess_quality(image_path, prompt)
        
        response_time_ms = (time() - start_time) * 1000
        
        # Log to cost tracker
        if tracker:
            tracker.log_request(
                image_path=image_path,
                prompt_tokens=result["usage"]["prompt_tokens"],
                completion_tokens=result["usage"]["completion_tokens"],
                total_tokens=result["usage"]["total_tokens"],
                response_time_ms=response_time_ms,
                model=result["model"]
            )
            tracker.end_session()
        
        # Display results
        print(f"\n{'='*60}")
        print("GPT-4V RESPONSE:")
        print(f"{'='*60}")
        print(result["content"])
        print(f"\n{'='*60}")
        print("USAGE STATISTICS:")
        print(f"{'='*60}")
        print(f"Response time: {response_time_ms:.2f} ms")
        print(f"Prompt tokens: {result['usage']['prompt_tokens']}")
        print(f"Completion tokens: {result['usage']['completion_tokens']}")
        print(f"Total tokens: {result['usage']['total_tokens']}")
        
        # Cost estimate
        cost = client.get_cost_estimate()
        print(f"\nEstimated cost: ${cost['estimated_cost_usd']:.4f} USD")
        print(f"  - Prompt: ${cost['prompt_cost_usd']:.4f}")
        print(f"  - Completion: ${cost['completion_cost_usd']:.4f}")
        
        # Save to file if requested
        if output_file:
            # Strip markdown code block delimiters if present
            content = result["content"].strip()
            if content.startswith("```json"):
                content = content[7:]  # Remove ```json
            elif content.startswith("```"):
                content = content[3:]  # Remove ```
            if content.endswith("```"):
                content = content[:-3]  # Remove trailing ```
            content = content.strip()
            
            # At minimum, use the cleaned content (without markdown delimiters)
            parsed_response = content
            
            # Try to parse the cleaned content as JSON
            try:
                parsed_response = json.loads(content)
                print(f"  ✓ Response parsed as JSON")
            except (json.JSONDecodeError, TypeError) as e:
                # Keep as cleaned string if not valid JSON
                print(f"  ⚠ Response is not valid JSON (may be truncated). Saving cleaned text.")
                print(f"    Error: {str(e)[:100]}")
            
            output_data = {
                "image": image_path,
                "prompt_type": prompt_type,
                "response": parsed_response,
                "usage": result["usage"],
                "cost_usd": cost["estimated_cost_usd"],
                "response_time_ms": response_time_ms
            }
            
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            
            print(f"\nResults saved to: {output_file}")
        
        return result
        
        return result
        
    except Exception as e:
        print(f"\n✗ Error during evaluation: {e}")
        if tracker:
            tracker.end_session()
        return None


def show_costs():
    """Display cost summary from previous evaluations."""
    tracker = CostTracker()
    summary = tracker.get_summary()
    
    print(f"\n{'='*60}")
    print("COST SUMMARY (All Evaluations)")
    print(f"{'='*60}")
    
    if "message" in summary:
        print(summary["message"])
    else:
        print(f"Total sessions: {summary['total_sessions']}")
        print(f"Total requests: {summary['total_requests']}")
        print(f"Total tokens: {summary['total_tokens']}")
        print(f"Total cost: ${summary['total_cost_usd']:.4f} USD")
        print(f"Avg per request: ${summary['avg_cost_per_request']:.6f} USD")
        
        print(f"\nSession Breakdown:")
        for session in summary['sessions']:
            print(f"  - {session['name']}: {session['requests']} requests, ${session['cost_usd']:.4f}")


def main():
    parser = argparse.ArgumentParser(
        description="Evaluate fruit quality using GPT-4V",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Test connection
  python eval_single_image.py --test-connection
  
  # Evaluate single image with default (structured) prompt
  python eval_single_image.py data/samples/apple.jpg
  
  # Use simple scoring prompt
  python eval_single_image.py data/samples/banana.jpg --prompt simple
  
  # Analyze fruit distribution and quality statistics
  python eval_single_image.py data/samples/shelf.jpg --prompt distribution
  
  # Save results to file
  python eval_single_image.py data/samples/orange.jpg --output results/orange_eval.json
  
  # View cost summary
  python eval_single_image.py --show-costs
        """
    )
    
    parser.add_argument(
        'image',
        nargs='?',
        help='Path to fruit image'
    )
    parser.add_argument(
        '--prompt',
        choices=['structured', 'simple', 'batch', 'defect', 'comparison', 'distribution'],
        default='structured',
        help='Prompt template to use (default: structured)'
    )
    parser.add_argument(
        '--output',
        help='Save results to JSON file'
    )
    parser.add_argument(
        '--no-track-costs',
        action='store_true',
        help='Disable cost tracking'
    )
    parser.add_argument(
        '--test-connection',
        action='store_true',
        help='Test Azure OpenAI connection and exit'
    )
    parser.add_argument(
        '--show-costs',
        action='store_true',
        help='Show cost summary from all evaluations'
    )
    
    args = parser.parse_args()
    
    # Handle special commands
    if args.test_connection:
        test_connection()
        return
    
    if args.show_costs:
        show_costs()
        return
    
    # Require image path for evaluation
    if not args.image:
        parser.error("Image path required (or use --test-connection or --show-costs)")
    
    # Verify image exists
    if not Path(args.image).exists():
        print(f"✗ Error: Image not found: {args.image}")
        sys.exit(1)
    
    # Run evaluation
    evaluate_image(
        image_path=args.image,
        prompt_type=args.prompt,
        output_file=args.output,
        track_costs=not args.no_track_costs
    )


if __name__ == "__main__":
    main()
