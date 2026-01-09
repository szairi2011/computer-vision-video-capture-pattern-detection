"""Tests for pipeline decorators."""

import pytest
import time
from src.pipeline.decorators import timer, retry, log_execution


def test_timer_decorator():
    """Test that timer decorator measures execution time."""
    @timer
    def slow_function():
        time.sleep(0.1)
        return "done"
    
    result = slow_function()
    assert result == "done"


def test_retry_decorator_success():
    """Test retry with successful function."""
    @retry(max_attempts=3)
    def succeeds():
        return "success"
    
    assert succeeds() == "success"


def test_retry_decorator_eventual_success():
    """Test retry with function that fails then succeeds."""
    call_count = {"count": 0}
    
    @retry(max_attempts=3, delay=0.1)
    def fails_twice():
        call_count["count"] += 1
        if call_count["count"] < 3:
            raise ValueError("Not yet")
        return "success"
    
    result = fails_twice()
    assert result == "success"
    assert call_count["count"] == 3


def test_log_execution_decorator():
    """Test log execution decorator."""
    @log_execution
    def example_func():
        return 42
    
    result = example_func()
    assert result == 42
