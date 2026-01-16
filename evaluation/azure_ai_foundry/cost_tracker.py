"""Cost tracking and analysis for Azure AI Foundry evaluation."""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional


class CostTracker:
    """Track API costs during evaluation for budget analysis."""
    
    def __init__(self, output_file: str = "evaluation/results/cost_analysis.json"):
        """
        Initialize cost tracker.
        
        Args:
            output_file: Path to save cost tracking data
        """
        self.output_file = Path(output_file)
        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        
        self.sessions = []
        self.current_session = None
    
    def start_session(self, session_name: str, description: str = ""):
        """
        Start a new evaluation session.
        
        Args:
            session_name: Name for this evaluation session
            description: Optional description
        """
        self.current_session = {
            "session_name": session_name,
            "description": description,
            "start_time": datetime.now().isoformat(),
            "requests": [],
            "total_tokens": 0,
            "total_cost_usd": 0.0
        }
    
    def log_request(
        self,
        image_path: str,
        prompt_tokens: int,
        completion_tokens: int,
        total_tokens: int,
        response_time_ms: float,
        model: str = "gpt-4v"
    ):
        """
        Log a single API request.
        
        Args:
            image_path: Path to image analyzed
            prompt_tokens: Tokens in prompt
            completion_tokens: Tokens in completion
            total_tokens: Total tokens used
            response_time_ms: Response time in milliseconds
            model: Model used
        """
        if not self.current_session:
            raise ValueError("No active session. Call start_session() first.")
        
        # Calculate cost (approximate pricing)
        prompt_cost_per_1k = 0.01
        completion_cost_per_1k = 0.03
        
        request_cost = (
            (prompt_tokens / 1000) * prompt_cost_per_1k +
            (completion_tokens / 1000) * completion_cost_per_1k
        )
        
        request_data = {
            "timestamp": datetime.now().isoformat(),
            "image": str(image_path),
            "model": model,
            "tokens": {
                "prompt": prompt_tokens,
                "completion": completion_tokens,
                "total": total_tokens
            },
            "cost_usd": round(request_cost, 6),
            "response_time_ms": round(response_time_ms, 2)
        }
        
        self.current_session["requests"].append(request_data)
        self.current_session["total_tokens"] += total_tokens
        self.current_session["total_cost_usd"] += request_cost
    
    def end_session(self):
        """End current session and save data."""
        if not self.current_session:
            return
        
        self.current_session["end_time"] = datetime.now().isoformat()
        self.current_session["total_cost_usd"] = round(
            self.current_session["total_cost_usd"], 4
        )
        
        # Calculate statistics
        requests = self.current_session["requests"]
        if requests:
            response_times = [r["response_time_ms"] for r in requests]
            self.current_session["statistics"] = {
                "total_requests": len(requests),
                "avg_response_time_ms": round(sum(response_times) / len(response_times), 2),
                "min_response_time_ms": round(min(response_times), 2),
                "max_response_time_ms": round(max(response_times), 2),
                "avg_tokens_per_request": round(
                    self.current_session["total_tokens"] / len(requests), 2
                )
            }
        
        self.sessions.append(self.current_session)
        self.current_session = None
        self._save()
    
    def _save(self):
        """Save cost tracking data to file."""
        data = {
            "generated_at": datetime.now().isoformat(),
            "sessions": self.sessions,
            "total_cost_all_sessions": round(
                sum(s["total_cost_usd"] for s in self.sessions), 4
            )
        }
        
        with open(self.output_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_summary(self) -> dict:
        """
        Get cost summary across all sessions.
        
        Returns:
            Summary statistics
        """
        if not self.sessions:
            return {"message": "No sessions tracked yet"}
        
        total_cost = sum(s["total_cost_usd"] for s in self.sessions)
        total_requests = sum(s["statistics"]["total_requests"] for s in self.sessions)
        total_tokens = sum(s["total_tokens"] for s in self.sessions)
        
        return {
            "total_sessions": len(self.sessions),
            "total_requests": total_requests,
            "total_tokens": total_tokens,
            "total_cost_usd": round(total_cost, 4),
            "avg_cost_per_request": round(total_cost / total_requests, 6) if total_requests > 0 else 0,
            "sessions": [
                {
                    "name": s["session_name"],
                    "requests": s["statistics"]["total_requests"],
                    "cost_usd": s["total_cost_usd"]
                }
                for s in self.sessions
            ]
        }
