# linear-models

**English** · [Русский](README.ru.md)

[![CI](https://github.com/bakzalitdootvala/linear-models/actions/workflows/ci.yml/badge.svg)](https://github.com/bakzalitdootvala/linear-models/actions/workflows/ci.yml) [![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](pyproject.toml) [![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-261230.svg)](https://docs.astral.sh/ruff/) [![Types: mypy strict](https://img.shields.io/badge/types-mypy%20strict-2a6db2.svg)](https://mypy-lang.org/)

Linear regression implemented from scratch in NumPy, checked against scikit-learn and evaluated on real data.

Expected values in the tests come from an independent calculation, every test is [mutation-checked](AGENTS.md#mutation-checks-mandatory) (it has to fail on a deliberately broken copy of the code), the code is strictly typed, and everything random runs with a fixed seed.

## Status

The repository contains the project skeleton: tooling, checks, CI and documentation in two languages.

## Quick start

```bash
git clone https://github.com/bakzalitdootvala/linear-models.git
cd linear-models
uv sync
uv run pytest
uv run pre-commit install
```

Requirements and the list of checks are in [docs/en/setup.md](docs/en/setup.md).

## Stack

- Python 3.12, with the virtual environment and dependencies managed by [uv](https://docs.astral.sh/uv/)
- NumPy, pandas, scikit-learn
- pytest, ruff, mypy in strict mode
- pre-commit hooks and GitHub Actions run the same checks

## Layout

```text
.
├── src/linear_models/     package code
├── tests/                 pytest tests
├── docs/
│   ├── en/                documentation in English
│   └── ru/                the same documentation in Russian
├── scripts/               maintenance scripts, standard library only
└── .github/workflows/     CI
```

Notebooks go to `notebooks/`, datasets to `data/`, which git ignores.

## Languages

Identifiers in code are English. Docstrings and comments are Russian, both in code and in configuration files. The documentation exists in English under `docs/en/` and in Russian under `docs/ru/`, at the same paths, and every change in one language goes into the other in the same change. English is the primary language of the repository.

## Documentation

The documentation index is [docs/en/README.md](docs/en/README.md). Terms used in the code and the documentation are explained in the [glossary](docs/en/GLOSSARY.md).

## License

[MIT](LICENSE).
