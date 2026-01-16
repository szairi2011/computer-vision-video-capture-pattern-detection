# GitHub Copilot Instructions - Fruits Quality Detection

## Project Overview
Production-grade PoC for supermarket fruit quality detection using **YOLOv8, Azure Event Hub (CEP), and Azure AI Search**. Emphasizes pythonic patterns, enterprise-grade modularity, and low cognitive load through extensive inline comments.

## Architecture Quick Reference

```
src/
├── vision/          # Video capture (generators) + YOLO detection
├── quality/         # Freshness scoring algorithms
├── events/          # Azure Event Hub async publishing
├── search/          # Azure AI Search indexing (Repository pattern)
├── pipeline/        # Orchestrator + decorators (@timer, @retry, @log_execution)
└── config/          # Pydantic settings with @lru_cache singleton
```

**Key Data Flow:** `Video → Detect → Quality Score → Event Hub → AI Search`

## Critical Development Patterns

### 1. Generators for Streaming (Memory Efficiency)
Video frames use `yield` not lists. See [capture.py](src/vision/capture.py):
```python
def stream_frames(source: Union[int, str], max_frames: int = 0) -> Generator:
    # Streams one frame at a time, avoids loading entire video into RAM
    yield ret, frame
```

### 2. Singleton Config via @lru_cache
[settings.py](src/config/settings.py) uses `@lru_cache()` on `get_settings()` to ensure single instance across modules.

### 3. Azure Integration with Graceful Degradation
All Azure components ([publisher.py](src/events/publisher.py), [indexer.py](src/search/indexer.py)) **must support offline mode**:
```python
if not self.connection_string:
    print(f"[EVENT] {event}")  # Fallback for local dev
    return True
```

### 4. Decorator-Based Pipeline
Use existing decorators for all new pipeline steps:
- `@timer` - Performance tracking
- `@retry(max_attempts=3)` - Fault tolerance
- `@log_execution` - Traceability

### 5. Inline Comments for Python Syntax
**Always explain non-obvious syntax** for developers from Java/C#/TypeScript:
```python
items: list[str]  # list[T] - generic type, Python 3.9+ syntax
source: Union[int, str]  # Union = can be int OR str
@dataclass  # Auto-generates __init__, __repr__, __eq__ methods
```

## Developer Workflows

### Local Development (No Azure)
```bash
python -m src.main demo  # 10-second webcam demo
python -m src.main detect --source 0  # Full pipeline without Azure
```

### Testing
```bash
pytest tests/  # Run all tests
pytest tests/test_vision.py -v  # Specific module with verbose output
```

### Configuration
- **Config source:** [settings.py](src/config/settings.py) (Pydantic + `.env`)
- **Azure optional:** System works offline if credentials missing
- **View config:** `python -m src.main config`

## Naming Conventions (Strict)
- **Functions:** Verbs (`detect_objects()`, `assess_freshness()`)
- **Classes:** Nouns with suffixes (`FruitDetector`, `EventPublisher`, `SearchRepository`)
- **Variables:** Full words, plural for collections (`detections`, `confidence_threshold`)
- **Constants:** `UPPER_SNAKE_CASE`

## Type Hints (Required)
All functions **must** have type hints:
```python
def process(data: dict[str, int]) -> list[str]:  # Modern syntax (Python 3.9+)
    pass
```
Common patterns: `Optional[T]`, `Union[A, B]`, `Generator[YieldType, None, None]`, `Callable[[Args], ReturnType]`

## Module Structure Rules
1. **Single responsibility:** `capture.py` = video I/O only, `detect.py` = detection only
2. **~100 lines max per file** - split if larger
3. **Import order:** stdlib → third-party → local (alphabetical within groups)

## Documentation Requirements
**Only update these 4 files** when adding features:
1. [README.md](README.md) - Quick start, CLI changes
2. [docs/architecture.md](docs/architecture.md) - New components/patterns
3. [docs/setup_guide.md](docs/setup_guide.md) - Dependencies, Azure config
4. [docs/execution_guide.md](docs/execution_guide.md) - CLI usage, troubleshooting

## Adding New Features

### New Detection Model
1. Create `src/vision/new_detector.py` with `detect() -> list[Detection]`
2. Export in `src/vision/__init__.py`
3. Update [architecture.md](docs/architecture.md)
4. Add CLI option in [main.py](src/main.py)

### New Azure Service
1. Create module in `src/<service>/`
2. Add settings to [settings.py](src/config/settings.py)
3. Add to `.env.example`
4. Implement offline fallback
5. Update [setup_guide.md](docs/setup_guide.md) + [architecture.md](docs/architecture.md)

### New Pipeline Step
1. Add function/class in `src/pipeline/`
2. Apply decorators (`@timer`, `@retry`)
3. Wire into [orchestrator.py](src/pipeline/orchestrator.py) chain
4. Update [execution_guide.md](docs/execution_guide.md)

## Quality Checklist (Verify Before Committing)
- [ ] Type hints on all params/returns
- [ ] Inline comments for Python-specific syntax (`@dataclass`, `Union`, `*args`)
- [ ] Design pattern identified in comments (`# Repository pattern - ...`)
- [ ] Error messages specific with context (`f"Cannot open {source}. Check camera index or URL."`)
- [ ] No hardcoded values (use [settings.py](src/config/settings.py))
- [ ] Follows single-responsibility principle
- [ ] Doc updates identified (which of 4 files?)

## Reference Files for Patterns
- **Generators:** [capture.py](src/vision/capture.py)
- **Dataclasses:** [detect.py](src/vision/detect.py) (`Detection` class)
- **Decorators:** [decorators.py](src/pipeline/decorators.py)
- **Async Azure:** [publisher.py](src/events/publisher.py)
- **CLI:** [main.py](src/main.py)
- **Config:** [settings.py](src/config/settings.py)

---

**Philosophy:** Code is read 10x more than written. Prioritize **clarity and low cognitive load** over cleverness.
