---
project_name: 'OLIPD'
user_name: 'Admin'
date: '2026-04-19'
sections_completed: ['technology_stack', 'language_rules', 'framework_rules', 'testing_rules', 'code_quality_rules', 'workflow_rules', 'anti_patterns']
status: 'complete'
rule_count: 42
optimized_for_llm: true
---

# Project Context for AI Agents: LLM Inference Optimization Toolkit (OLIPD)

_This file contains critical rules and patterns that AI agents must follow when implementing code in this project. Focus on unobvious details that agents might otherwise miss._

---

## Technology Stack & Versions

- **Core Models:** LLaMA (v3), Mistral (v0.x), Phi-3
- **Optimization Engines:** 
    - High-Performance: `vLLM` (PagedAttention, Continuous Batching)
    - High-Compatibility: `AutoAWQ`, `AutoGPTQ` (fallback for older GPUs)
- **Quantization:** AWQ (Primary for 4-bit accuracy), GPTQ (Alternative)
- **Backend:** FastAPI (Async-first) + Uvicorn
- **Pinned Versions (Mandatory):**
    - `transformers==4.40.0`
    - `torch>=2.2.0`
    - `vllm>=0.4.0` (for Llama-3 support)
- **Hardware Profile:** Target NVIDIA T4 (compatibility) & A10/A100 (performance)

## Critical Implementation Rules

### Language-Specific Rules (Python)
- **Typed Code:** Strict use of Python type hints for all function signatures and complex ML objects.
- **Boundary Validation:** Use `Pydantic` (v2) models for all API request/response data. Internal compute logic must use native `numpy`/`torch` types to avoid overhead.
- **Streaming by Default:** All text-generation endpoints must implement `Async Generators` and FastAPI `StreamingResponse` to optimize Time-To-First-Token (TTFT).
- **Resource Lifecycle:** Mandatory VRAM cleanup patterns using `try...finally` blocks to ensure `torch.cuda.empty_cache()` is called.
- **Memory Watchdog:** ML Worker processes must implement a memory heartbeat check; proactively restart or flush `torch.cuda` cache if VRAM fragmentation exceeds 15% of total.
- **Structured Logging:** Use the standard `logging` library; `print()` statements are forbidden in production code.
- **Configuration:** Use `pydantic-settings` for environment variable management (e.g., `MODEL_ID`, `CUDA_VISIBLE_DEVICES`).

### Framework-Specific Rules (FastAPI)
- **Singleton Model Loading:** Use FastAPI `Depends()` with a singleton pattern for model loading to prevent redundant VRAM usage.
- **Early Disconnect Handling:** Async generator routes must proactively check `request.is_disconnected()` to terminate inference and free GPU resources if the client drops.
- **Concurrency Limiting:** Implement a global `asyncio.Semaphore` dependency to limit concurrent inference tasks based on hardware capacity (preventing OOM).
- **Admin & Observability:** 
    - Separate `AdminRouter` for `/health`, `/metrics`, and `/cache/clear`.
    - Every response must include `X-Inference-Time-MS`, `X-Model-ID`, and `X-Request-ID` in headers.
- **Async Safety:** Mandatory use of `httpx` for outgoing requests; blocking synchronous calls (like `requests.get`) are forbidden inside `async def` routes.
- **Standardized Errors:** Implement global exception handlers for `torch.cuda.OutOfMemoryError` and other ML-specific failures.
- **Streaming Reliability:** Use `EventSourceResponse` for stable Server-Sent Events (SSE) when streaming long LLM responses.

### Testing Rules
- **GPU-Free Unit Tests:** Mandatory mocking of all `torch`, `cuda`, and `transformers` model loading in unit tests to ensure they run in non-GPU environments.
- **Quantization Parity:** Benchmark scripts must include a validation pass checking that quantized outputs remain within a defined delta from the FP16 baseline.
- **Async Testing:** Use `pytest-asyncio` for all API tests, specifically validating that StreamingResponse yields chunks as expected.
- **Integration Slashing:** Integration tests that require local GPUs must be clearly marked with `@pytest.mark.gpu` and kept separate from fast unit tests.

### Code Quality & Style Rules
- **Modern Tooling:** Use `Ruff` for linting and `Black` for formatting.
- **Naming Conventions:** Strict `snake_case` for variables/functions, `PascalCase` for classes, and `UPPER_SNAKE_CASE` for constants.
- **Documentation:** Mandatory Google-style docstrings for all public functions, especially those involving Tensor manipulations (must specify expected shapes).
- **Directory Layout:** Follow a modular structure: `core/` (optimization), `api/` (routes), `services/` (inference logic), and `utils/` (helpers).

### Development Workflow Rules
- **Branching Strategy:** Use `feature/` or `fix/` branches; direct commits to `main` are restricted.
- **Commit Standards:** Follow `Conventional Commits` format for all changes.
- **CI/CD Gates:** PRs must pass linting (Ruff), formatting (Black), and all non-GPU unit tests before merging.
- **Atomic Commits:** Prefer small, atomic commits that address a single logic change or feature.

### Critical Don't-Miss Rules
- **No Overlapping Loads:** Never attempt to load two large models into the same GPU simultaneously without an explicit VRAM management lock.
- **Mandatory Warm-up:** Every model loading service must include a "warm-up" phase with dummy inference to stabilize hardware latency before going live.
- **Safe Weights Only:** Strictly use `safetensors` for model weight loading; the use of `pickle` is forbidden due to security risks.
- **Benchmark Integrity:** A performance optimization is considered "failed" if it degrades model accuracy by more than a predefined threshold (default: 2% relative accuracy).

---

## Usage Guidelines

**For AI Agents:**
- Read this file before implementing any code.
- Follow ALL rules exactly as documented.
- When in doubt, prefer the more restrictive option.
- Update this file if new patterns emerge.

**For Humans:**
- Keep this file lean and focused on agent needs.
- Update when technology stack changes.
- Review quarterly for outdated rules.
- Remove rules that become obvious over time.

Last Updated: 2026-04-19
