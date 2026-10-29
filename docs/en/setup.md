# Development setup

**English** · [Русский](../ru/setup.md)

> How to get the project running and what the checks do.

## Requirements

- git
- [uv](https://docs.astral.sh/uv/), which also installs Python 3.12 when it is missing

## Install

```bash
uv sync
```

This creates `.venv` and installs the runtime and development dependencies exactly as pinned in `uv.lock`.

## Run the checks by hand

```bash
uv run pytest
uv run mypy
uv run ruff check .
uv run ruff format --check .
```

## Pre-commit hooks

```bash
uv run pre-commit install
uv run pre-commit run --all-files
```

The hooks run before every commit:

- `ruff-check` and `ruff-format`: lint and formatting.
- `pre-commit-hooks`: trailing whitespace, end of file, line endings, YAML, TOML and JSON syntax, merge-conflict markers, case conflicts, symlinks, private keys, files larger than 512 KB.
- `nbstripout`: strips execution counters and metadata from notebooks and keeps their outputs.
- `gitleaks`: looks for secrets in the staged changes.
- `markdownlint`: Markdown style.
- `mypy`: strict type check in the project environment.
- `ru-en-parity` and `relative-links`: the English and Russian documentation mirror each other, and relative links point to existing files and headings.

The hooks are pinned to commit SHAs, with the tag kept in a `# frozen:` comment, so a tag that is moved to other code cannot swap the hook. To update them, run `uv run pre-commit autoupdate --freeze` and read the diff.

## Branches

The repository is personal and has one maintainer, so all work goes to `main` directly. There are no `develop`, `fix/*`, `feature/*` or other branches, and changes do not go through pull requests.

## Continuous integration

`.github/workflows/ci.yml` runs on every push to `main` and on every pull request. The `pre-commit hooks` job runs all hooks over all files and scans the whole git history with gitleaks. The `pytest` job runs the tests. Actions are pinned to commit SHAs.

## Dependencies

Add a runtime dependency with `uv add <package>` and a development one with `uv add --group dev <package>`. Commit `pyproject.toml` and `uv.lock` together. The ruff version in `.pre-commit-config.yaml` must match the one in `uv.lock`.

## Documentation in two languages

Every file under `docs/en/` has a twin under `docs/ru/` at the same path, and each file links to its twin in the first lines. `scripts/check_parity.py` fails when a twin is missing, a link to it is absent, or a page is not listed in the index of its language.
