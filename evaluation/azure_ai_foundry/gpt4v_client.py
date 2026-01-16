"""GPT-4V client wrapper for fruit quality assessment evaluation."""

import base64
import os
from pathlib import Path
from typing import Optional
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()


class GPT4VisionClient:
    """
    Azure OpenAI GPT-4V client for image analysis.
    
    Wrapper around Azure OpenAI SDK for fruit quality assessment.
    Tracks token usage for cost analysis.
    """
    
    def __init__(
        self,
        endpoint: Optional[str] = None,
        api_key: Optional[str] = None,
        deployment: Optional[str] = None,
        api_version: str = "2024-02-15-preview"
    ):
        """
        Initialize GPT-4V client.
        
        Args:
            endpoint: Azure OpenAI endpoint URL (from env if not provided)
            api_key: Azure OpenAI API key (from env if not provided)
            deployment: Deployment name (from env if not provided)
            api_version: API version (default: latest stable)
        """
        self.endpoint = endpoint or os.getenv("AZURE_OPENAI_ENDPOINT")
        self.api_key = api_key or os.getenv("AZURE_OPENAI_API_KEY")
        self.deployment = deployment or os.getenv("AZURE_OPENAI_DEPLOYMENT", "fruit-quality-gpt4v")
        self.api_version = api_version
        
        if not all([self.endpoint, self.api_key]):
            raise ValueError(
                "Azure OpenAI credentials not found. Set AZURE_OPENAI_ENDPOINT "
                "and AZURE_OPENAI_API_KEY in .env file."
            )
        
        # Initialize Azure OpenAI client
        self.client = AzureOpenAI(
            azure_endpoint=self.endpoint,
            api_key=self.api_key,
            api_version=self.api_version
        )
        
        # Token usage tracking for cost analysis
        self.total_tokens = 0
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
    
    def encode_image(self, image_path: str) -> str:
        """
        Encode image to base64 for API submission.
        
        Args:
            image_path: Path to image file
            
        Returns:
            Base64-encoded image string
        """
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def assess_quality(
        self,
        image_path: str,
        prompt: str,
        max_tokens: int = 1500,  # Increased for complex responses (distribution analysis)
        temperature: float = 0.0  # Low temperature for consistent scoring
    ) -> dict:
        """
        Assess fruit quality using GPT-4V.
        
        Args:
            image_path: Path to fruit image
            prompt: System prompt for quality assessment
            max_tokens: Maximum response tokens
            temperature: Sampling temperature (0.0 = deterministic)
            
        Returns:
            Dict with 'content' (response text) and 'usage' (token counts)
        """
        # Encode image
        base64_image = self.encode_image(image_path)
        
        # Create message with image
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ]
        
        # Call GPT-4V
        response = self.client.chat.completions.create(
            model=self.deployment,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature
        )
        
        # Track token usage
        usage = response.usage
        self.total_tokens += usage.total_tokens
        self.total_prompt_tokens += usage.prompt_tokens
        self.total_completion_tokens += usage.completion_tokens
        
        return {
            "content": response.choices[0].message.content,
            "usage": {
                "prompt_tokens": usage.prompt_tokens,
                "completion_tokens": usage.completion_tokens,
                "total_tokens": usage.total_tokens
            },
            "model": response.model
        }
    
    def get_cost_estimate(self) -> dict:
        """
        Calculate estimated cost based on token usage.
        
        GPT-4V pricing (as of Jan 2026):
        - Prompt: ~$0.01 per 1K tokens
        - Completion: ~$0.03 per 1K tokens
        
        Returns:
            Dict with token counts and estimated cost in USD
        """
        # Pricing per 1K tokens (approximate, check Azure pricing for exact rates)
        prompt_cost_per_1k = 0.01
        completion_cost_per_1k = 0.03
        
        prompt_cost = (self.total_prompt_tokens / 1000) * prompt_cost_per_1k
        completion_cost = (self.total_completion_tokens / 1000) * completion_cost_per_1k
        total_cost = prompt_cost + completion_cost
        
        return {
            "total_tokens": self.total_tokens,
            "prompt_tokens": self.total_prompt_tokens,
            "completion_tokens": self.total_completion_tokens,
            "estimated_cost_usd": round(total_cost, 4),
            "prompt_cost_usd": round(prompt_cost, 4),
            "completion_cost_usd": round(completion_cost, 4)
        }
    
    def reset_usage(self):
        """Reset token usage counters."""
        self.total_tokens = 0
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
