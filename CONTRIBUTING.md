# Contributing to TrendPulse

## Development Setup

```bash
git clone https://github.com/homgorn/trendpulse.git
cd trendpulse
pip install -e ".[dev]"
```

## Coding Standards

- **Lint**: `ruff check src/`
- **Format**: `ruff format src/`
- **Tests**: `pytest tests/`

Run all checks:
```bash
make lint && make test
```

## API Patterns

### Adding a New LLM Provider

1. Create `src/trendpulse/adapters/{provider}_backend.py`
2. Implement `LLMBackend` interface from `core/llm/backends.py`
3. Add provider to `config.py` settings
4. Add tests in `tests/test_gateway.py`

### Adding New API Endpoint

1. Define request/response schemas in `schemas.py`
2. Add endpoint to `api.py`
3. Add business logic to `service.py`
4. Add tests in `tests/test_api.py`

## Submitting PRs

1. Fork the repo
2. Create feature branch: `git checkout -b feature/my-feature`
3. Run tests: `pytest tests/`
4. Run lint: `ruff check src/`
5. Commit with conventional commits
6. Push and open PR

## Commit Messages

Use conventional commits:
- `feat:` new feature
- `fix:` bug fix
- `docs:` documentation
- `test:` tests
- `refactor:` code refactoring
- `chore:` maintenance

## Questions

Open an issue: https://github.com/homgorn/trendpulse/issues