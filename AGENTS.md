# Agent Guidelines for RAG Project

This document provides guidelines for AI agents working on this Python RAG (Retrieval-Augmented Generation) project. The project builds a local knowledge base over PDF papers using LangChain, ChromaDB, and Deepseek API.

## Project Overview

- **Language**: Python 3.10+
- **Dependencies**: See `requirements.txt`
- **Source Code**: `src/` directory
- **Configuration**: `configs/settings.yaml`
- **Data**: PDFs in `data/papers/`
- **Vector Database**: `db/chroma/`

## Build and Run Commands

### Environment Setup

```bash
python -m venv .venv
.venv\Scripts\activate           # Windows
source .venv/bin/activate        # Linux/macOS
pip install -r requirements.txt
```

### Running the Application

```bash
python src/ingest.py
python src/query.py "Your question here"
```

### Development Dependencies (Optional)

```bash
pip install black isort flake8 mypy pytest pytest-cov pre-commit
```

## Linting and Formatting

### Auto‑formatting

```bash
black src/ configs/
isort src/ configs/
```

### Linting

```bash
flake8 src/ configs/
mypy src/ --ignore-missing-imports
```

### Pre‑commit Hooks

```bash
pre-commit install
pre-commit run --all-files
```

## Testing

Currently no test suite is defined. When tests are added (likely under `tests/`):

```bash
pytest
pytest tests/test_utils.py
pytest tests/test_utils.py::test_parse_filename_metadata -v
pytest --cov=src --cov-report=html
```

## Code Style Guidelines

### General Principles

- Follow **PEP 8** and **PEP 257**.
- Use type hints for all function arguments and return values.
- Keep functions small and focused.
- Prefer immutable data structures where possible.

### Imports

- Group imports: standard library → third‑party → local.
- Use absolute imports for local modules.
- Separate groups with a blank line.

**Example**:
```python
import os
import re
from typing import Dict, List

import fitz
import yaml
from langchain.schema import Document

from utils import load_settings
```

### Formatting

- Indentation: 4 spaces (no tabs).
- Line length: 88 characters (Black’s default).
- Quotes: double quotes (`"`) for string literals, single quotes (`'`) if the string contains double quotes. Use triple double quotes for docstrings.
- Trailing commas in multi‑line collections and argument lists.
- Run `black` before committing.

### Type Annotations

- Annotate all function parameters and return types.
- Use `typing` module (`List`, `Dict`, `Tuple`, `Optional`, etc.).
- For data‑carrying classes, prefer `@dataclass`.

### Naming Conventions

- Variables & functions: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Private functions/methods: prefix with `_`

### Error Handling

- Use explicit checks for expected edge cases.
- Raise built‑in exceptions (`ValueError`, `TypeError`, `FileNotFoundError`) with descriptive messages.
- Avoid bare `except:`; catch specific exceptions.
- Consider migrating from `print` to `logging` for errors.

### Docstrings and Comments

- Write docstrings for all public functions, classes, and modules using triple‑double quotes.
- Follow Google style: summary line, blank line, detailed description, `Args:`, `Returns:`, `Raises:`.
- Use inline comments only to explain **why** something non‑obvious is done.

### Configuration and Environment

- Keep configuration in `configs/settings.yaml`; do not hardcode settings.
- Use environment variables for secrets (`DEEPSEEK_API_KEY`).
- Load settings via `load_settings` function in `utils.py`.

### Adding New Features

- Place new functionality in existing modules (`utils.py`, `ingest.py`, `query.py`) or create a new module in `src/` if it represents a distinct subsystem.
- Avoid breaking changes to the public API (functions called from `ingest.py` or `query.py`).
- If adding a third‑party dependency, append it to `requirements.txt` with a pinned version.

## Git Practices

- Commit messages should follow **Conventional Commits**:
  ```
  feat: add support for EPUB ingestion
  fix: handle empty PDF pages gracefully
  docs: update README with installation notes
  refactor: simplify repeated‑line detection
  test: add unit tests for filename parsing
  ```
- Keep commits focused on a single logical change.
- Run formatting and linting before committing (or rely on pre‑commit hooks).

## Cursor / Copilot Rules

No repository‑specific Cursor rules (`.cursorrules` or `.cursor/rules/`) or GitHub Copilot instructions (`.github/copilot‑instructions.md`) are currently present. When added, agents should review and follow those rules.

## Agent Checklist

Before submitting a change, ensure:

- [ ] Code follows the style guidelines above
- [ ] Type annotations are present and correct
- [ ] No new linting errors introduced (run `flake8` and `mypy`)
- [ ] Code is formatted with `black` and `isort`
- [ ] Docstrings are provided for new public functions/classes
- [ ] Existing tests pass (if any)
- [ ] Changes are backward compatible (or the breaking change is documented)
- [ ] Configuration and environment variables are documented in README if added

---

*This document is intended for AI agents assisting with development. Update it as the project evolves.*