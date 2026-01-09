# GitHub Copilot Instructions - Fruits Quality Detection Project

## Project Context

This is a **production-grade PoC** for supermarket fruit quality detection using YOLOv8, Azure Event Hub (CEP), and Azure AI Search. The codebase emphasizes **pythonic design patterns, minimal cognitive load, and modular architecture** suitable for enterprise customers.

---

## Core Principles

### 1. Reduce Cognitive Load
- **Inline Comments**: Explain *why* and *what* syntax means, not just *what* code does
- **Examples**: For complex patterns (decorators, generators, Union types), add brief examples
- **Assume Context Switching**: Developer may be coming from Java/C#/TypeScript, explain Python-specific syntax
- **Key Areas to Comment**:
  - `@dataclass` - Why used (auto-generates `__init__`, `__repr__`, etc.)
  - `Union[A, B]` - Type can be A OR B
  - `Optional[T]` - Shorthand for `Union[T, None]`
  - `Generator` - Why/when to use over lists (memory efficiency)
  - `@contextmanager` - How it enables `with` statements
  - `Enum` - Why better than plain strings (type safety, autocomplete)
  - `@lru_cache` - Singleton pattern implementation
  - `functools.wraps` - Preserves function metadata in decorators
  - `*args, **kwargs` - Variable positional/keyword arguments

### 2. Single-Purpose Modules
- **One responsibility per file**: `capture.py` = video I/O, `detect.py` = detection only
- **Max ~100 lines per file**: If larger, split into logical submodules
- **Clear module hierarchy**: 
  ```
  src/vision/     # All computer vision code
  src/events/     # All Azure Event Hub code
  src/pipeline/   # Orchestration only
  ```

### 3. Naming Conventions

#### Functions
- **Verbs for actions**: `detect_objects()`, `assess_freshness()`, `publish_event()`
- **Nouns for getters**: `get_settings()`, `get_video_props()`
- **Boolean prefixes**: `is_valid()`, `has_detections()`, `can_process()`

#### Classes
- **Nouns**: `FruitDetector`, `QualityScore`, `EventPublisher`
- **Descriptive suffixes**: 
  - `*Detector` for detection models
  - `*Repository` for data access
  - `*Publisher` for event streaming
  - `*Score` for result objects

#### Variables
- **Descriptive, avoid abbreviations**: `confidence_threshold` not `conf_thresh`
- **Units in name when relevant**: `max_frames`, `elapsed_seconds`
- **Collections plural**: `detections`, `events`, `frames`

#### Constants
- **UPPER_SNAKE_CASE**: `DEFAULT_CONFIDENCE = 0.3`

---

## Design Patterns to Use

### Creational Patterns
1. **Factory Functions**: `create_quality_event()`, `create_fruit_document()`
   - Use when: Creating complex objects with validation
   - Comment: "Factory function - encapsulates object creation logic"

2. **Singleton**: `@lru_cache()` on `get_settings()`
   - Use when: Need single shared instance (config, connections)
   - Comment: "Singleton pattern via LRU cache - ensures one instance"

### Structural Patterns
1. **Repository**: `SearchRepository` for Azure AI Search
   - Use when: Abstracting data access/external services
   - Comment: "Repository pattern - abstracts Azure SDK details"

2. **Decorator**: `@timer`, `@retry`, `@log_execution`
   - Use when: Adding cross-cutting concerns (logging, monitoring)
   - Comment: "Decorator pattern - adds [behavior] without modifying function"

### Behavioral Patterns
1. **Strategy**: Different quality scoring algorithms
   - Use when: Multiple interchangeable algorithms
   - Comment: "Strategy pattern - swappable quality assessment algorithms"

2. **Chain of Responsibility**: Pipeline processing stages
   - Use when: Sequential processing with multiple handlers
   - Comment: "Chain pattern - sequential processing stages"

### Functional Patterns
1. **Generator**: `stream_frames()` for video
   - Use when: Processing large/infinite sequences
   - Comment: "Generator pattern - memory-efficient streaming (no full load)"

2. **Pure Functions**: `assess_freshness()`, `draw_detections()`
   - Use when: No side effects, testable logic
   - Comment: "Pure function - no side effects, same input → same output"

3. **Context Manager**: `video_writer()`
   - Use when: Resource management (files, connections, locks)
   - Comment: "Context manager - ensures resource cleanup (even on errors)"

---

## Code Structure Standards

### Module Organization
```python
"""Module docstring - what this module does."""

# Standard library imports
import os
from typing import Optional

# Third-party imports
import cv2
import numpy as np

# Local imports
from ..config import get_settings

# Constants
DEFAULT_TIMEOUT = 30

# Classes/Functions (alphabetical or logical order)
```

### Function/Method Structure
```python
def function_name(
    param1: str,
    param2: Optional[int] = None  # Optional = can be int or None
) -> ReturnType:  # Always include return type hint
    """
    Brief one-line summary.
    
    Longer explanation if needed. Explain *why* not just *what*.
    
    Args:
        param1: Description with units/format if relevant
        param2: Description, note default behavior
    
    Returns:
        Description of return value
        
    Raises:
        ValueError: When/why this is raised
    """
    # Implementation with inline comments for complex logic
    pass
```

### Class Structure
```python
# @dataclass: Auto-generates __init__, __repr__, __eq__ methods
# Why: Reduces boilerplate for data-holding classes
@dataclass
class MyClass:
    """Brief class description."""
    field1: str  # Description
    field2: int = 10  # Default value
    
    def method(self) -> None:
        """Method docstring."""
        pass
```

---

## Documentation Standards

### Only Update These 4 Docs
1. **README.md** - Quick start, overview, links to other docs
2. **docs/architecture.md** - Component design, patterns, data flow
3. **docs/setup_guide.md** - Installation, Azure config, verification
4. **docs/execution_guide.md** - CLI usage, demos, troubleshooting

### When to Update Docs
- **README.md**: New features, changed CLI commands, project structure changes
- **architecture.md**: New modules, design pattern changes, Azure service additions
- **setup_guide.md**: New dependencies, Azure service config, environment variables
- **execution_guide.md**: New CLI commands, demo scenarios, common issues

### Documentation Style
- **Cross-link between docs**: Use relative links `[See Setup Guide](setup_guide.md#section)`
- **Table of Contents**: Every doc has TOC with anchor links
- **Code examples**: Show actual commands, not placeholders
- **Troubleshooting**: Common errors with solutions

---

## Type Hints Standards

### Always Use Type Hints
```python
# Good - clear types
def process(data: dict[str, int]) -> list[str]:
    pass

# Avoid - no type hints
def process(data):
    pass
```

### Common Type Patterns
```python
from typing import Optional, Union, List, Dict, Callable, Generator

# Optional: Value or None
name: Optional[str] = None  # Same as Union[str, None]

# Union: Multiple possible types
source: Union[int, str]  # Can be int OR str

# Collections (modern syntax, Python 3.9+)
items: list[str]  # List of strings
config: dict[str, int]  # Dict with string keys, int values

# Callable: Function type
callback: Callable[[int, str], bool]  # Function taking (int, str), returning bool

# Generator: Streaming data
def stream() -> Generator[str, None, None]:  # Yields str, sends None, returns None
    yield "data"
```

---

## Comment Guidelines

### When to Comment

✅ **Always comment**:
- Python-specific syntax (`@dataclass`, `Union`, `*args`)
- Design pattern usage (`# Repository pattern - ...`)
- Non-obvious business logic
- Performance optimizations
- Workarounds/hacks

✅ **Sometimes comment**:
- Complex algorithms (why chosen, trade-offs)
- External API usage (link to docs)

❌ **Don't comment**:
- Self-explanatory code (`x = x + 1  # increment x`)
- Obvious variable assignments

### Comment Style

```python
# Single-line: Explain why/what syntax means
items: list[str]  # list[T] - generic type, list containing strings

# Multi-line: Explain complex logic or patterns
# Generator pattern: Memory-efficient streaming
# Why: Processes frames one-by-one without loading entire video
# Alternative: list[Frame] would load all frames (OOM for long videos)
def stream_frames() -> Generator[Frame, None, None]:
    pass

# Inline: Brief clarification
confidence_threshold = 0.3  # Lower = more detections (but more false positives)
```

---

## Error Handling

### Explicit Error Messages
```python
# Good - clear error with context
if not cap.isOpened():
    raise ValueError(f"Cannot open video source: {source}. Check camera index or URL.")

# Avoid - vague error
if not cap.isOpened():
    raise ValueError("Error")
```

### Use Specific Exceptions
```python
# Good
raise ValueError("...")  # Invalid value
raise FileNotFoundError("...")  # Missing file
raise ConnectionError("...")  # Network issue

# Avoid
raise Exception("...")  # Too generic
```

---

## Testing Standards

### Test Organization
```python
# tests/test_module.py
"""Tests for module_name module."""

import pytest
from src.module import function_to_test

def test_function_success_case():
    """Test description - what scenario is tested."""
    result = function_to_test(input)
    assert result == expected

def test_function_error_case():
    """Test error handling."""
    with pytest.raises(ValueError):
        function_to_test(invalid_input)
```

### Naming
- **Test files**: `test_*.py`
- **Test functions**: `test_<function_name>_<scenario>()`
- **Fixtures**: Descriptive names (`sample_frame`, `mock_detector`)

---

## Performance Patterns

### Prefer Generators for Streaming
```python
# Good - memory efficient
def stream_frames() -> Generator[Frame, None, None]:
    while True:
        yield frame  # Yields one frame at a time

# Avoid - loads everything into memory
def get_all_frames() -> list[Frame]:
    return [frame1, frame2, ...]  # OOM risk for long videos
```

### Use @lru_cache for Expensive Operations
```python
from functools import lru_cache

@lru_cache(maxsize=128)  # Caches last 128 results
def expensive_computation(x: int) -> int:
    # Complex calculation
    return result
```

---

## Azure Integration Patterns

### Async for I/O Operations
```python
# Event Hub, AI Search operations should be async
async def publish_event(event: Event) -> bool:
    async with EventHubProducerClient(...) as client:
        await client.send_batch(...)
```

### Fallback for Missing Credentials
```python
# Allow local dev without Azure
if not self.connection_string:
    # Fallback: log to console
    print(f"[EVENT] {event}")
    return True

# Otherwise: use Azure
await self._client.send(event)
```

---

## CLI Design (Click)

### Command Structure
```python
@click.command()
@click.option('--source', '-s', required=True, help='Clear description')
@click.option('--conf', '-c', default=0.3, help='Include defaults in help')
def detect(source, conf):
    """Command description shown in --help."""
    click.echo(f"Processing {source}...")  # User-friendly output
```

### Output Style
- **Progress**: Use `click.echo()` for status updates
- **Errors**: Use `click.secho('Error: ...', fg='red')`
- **Success**: Use `click.secho('✓ Complete', fg='green')`

---

## Examples for Common Scenarios

### Adding New Detection Model
1. Create `src/vision/new_detector.py`
2. Implement detector class with `detect()` method returning `list[Detection]`
3. Add to `src/vision/__init__.py` exports
4. Update `docs/architecture.md` with new component
5. Add CLI option in `src/main.py`

### Adding Azure Service
1. Create module in `src/<service>/`
2. Add config to `src/config/settings.py`
3. Add to `.env.example`
4. Update `docs/setup_guide.md` with setup steps
5. Update `docs/architecture.md` with integration details

### Adding Pipeline Step
1. Create function/class in `src/pipeline/`
2. Add to orchestrator chain in `orchestrator.py`
3. Add relevant decorator (`@timer`, `@retry`)
4. Update `docs/execution_guide.md` with usage

---

## Quality Checklist (for Copilot to verify)

Before suggesting code:

- [ ] Type hints on all function parameters and returns
- [ ] Docstrings for public functions/classes
- [ ] Inline comments for Python-specific syntax
- [ ] Design pattern identified and commented
- [ ] Error messages are specific and actionable
- [ ] No hardcoded values (use config or constants)
- [ ] Follows single-responsibility principle
- [ ] Module/function name is intuitive (verb for function, noun for class)
- [ ] If adding feature: identified which of 4 docs to update

---

## Additional Guidelines

### Imports
- Group by: standard library, third-party, local
- Alphabetical within groups
- No wildcard imports (`from x import *`)

### String Formatting
- Use f-strings: `f"Value: {x}"`
- Avoid: `"Value: " + str(x)` or `"Value: {}".format(x)`

### File Paths
- Use `pathlib.Path` for path operations
- Cross-platform: avoid hardcoded `/` or `\`

### Logging
- Use `logging` module, not `print()` (except CLI output)
- Levels: DEBUG (detailed), INFO (progress), WARNING (issues), ERROR (failures)

---

**Remember**: Code is read 10x more than written. Optimize for **clarity** and **low cognitive load** over cleverness.
