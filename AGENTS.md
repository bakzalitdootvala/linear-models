# AGENTS.md

Instructions for AI coding agents and human contributors working on this repository.

## What this repository is

Linear regression implemented from scratch in NumPy, checked against scikit-learn, then evaluated on real data. Python 3.12, managed with uv. The documentation is bilingual: English under `docs/en/` is the primary text, and Russian under `docs/ru/` mirrors it file for file.

## Layout

- `src/linear_models/`: the package. Library code only, nothing that runs on import.
- `tests/`: pytest tests.
- `docs/en/` and `docs/ru/`: documentation. Every file has a twin at the same path in the other language. `GLOSSARY.md` explains the terms used in the code and the documentation.
- `README.md` and `README.ru.md`: the top pages, linked to each other.
- `scripts/`: maintenance scripts that use only the standard library. `check_parity.py` checks that the two documentation trees mirror each other. `check_links.py` checks relative links and heading anchors.
- `notebooks/`: thin report notebooks over tested code from `src/`. Their outputs (tables and numbers) are committed; the `nbstripout` hook strips only execution counters and metadata. Run Restart and Run All before committing.
- `data/` and `models/` at the repository root: ignored by git. Datasets are downloaded or generated on demand.

## Languages and wording

- Identifiers, commit messages and pull request text are English. Job and step names in workflows and hook names count as identifiers.
- Docstrings and comments are Russian, in Python code and in configuration files (`pyproject.toml`, `.pre-commit-config.yaml`, `.github/workflows/`, `.gitignore`, `.markdownlint.yaml`). Names of tools and rules inside a comment stay as they are, and so do the comments that tools read: `# frozen: v1.2.3` after a hook `rev:` and `# v1.2.3` after an action SHA.
- Every documentation change in one language goes into the twin in the same change. Facts, structure and links must match.
- A new term gets an entry in `docs/en/GLOSSARY.md` and `docs/ru/GLOSSARY.md` in the change that introduces it, with an explanation in plain words and numbers.
- English uses American spelling.
- Terms keep their own names: write "endpoint", "token", "residual", never a metaphor in their place.
- Public text (README, docs, docstrings, comments, commit messages) describes what the code does and how it is checked. It does not refer to other repositories, to other projects or to local filesystem paths.

## Branches

The repository is personal and has one maintainer, so all work goes to `main`: commit to it directly. There are no `develop`, `fix/*`, `feature/*` or other branches, and changes do not go through pull requests. CI checks every push to `main`.

## Commands

```bash
uv sync                               # create .venv from uv.lock
uv run pytest                         # tests
uv run mypy                           # strict type check of src, tests and scripts
uv run ruff check .                   # lint
uv run ruff format .                  # format
uv run pre-commit install             # once per clone
uv run pre-commit run --all-files     # all hooks, the same set CI runs
```

## Mutation checks (mandatory)

Every test and every guard (hook, check script) gets a mutation check before the change counts as done:

1. Break exactly the thing it protects: delete the protecting line, flip a condition, remove the file it expects.
2. Run the test or the guard. It must fail, and the failure must be about the thing you broke: read the message, a red run for another reason proves nothing.
3. Restore the code and run it again. It must pass.

A test that has never failed proves nothing: it may be checking an empty list or a string that sits in a comment. Feeding a guard nothing is a mutation too: a guard that passes while checking zero items is broken. State in the change description which mutation was run and which test or guard caught it.

## Code rules

- Type hints on every function; mypy runs in strict mode. scikit-learn has no type information, so values that come from it are `Any`: annotate them where they enter your code.
- Use `numpy.random.default_rng(seed)`, never the legacy global `np.random.*` functions. Every random experiment takes a seed.
- Split the data before any fitting, and fit scalers and other learned transformations on the train part only.
- Expected numbers in tests come from an independent calculation (a formula worked out by hand, `numpy.polyfit`, scikit-learn), never from the code under test.

## Do not

- Commit secrets, tokens, datasets or trained model files; gitleaks and the large-file hook block most of them.
- Add personal agent instruction files such as `CLAUDE.md`; they are ignored on purpose, and this file is the shared one.
- Add dependencies to the scripts in `scripts/`; they stay on the standard library.
- Pin third-party hooks or actions by a tag. Pin them by commit SHA with the tag in a comment (`rev: <sha>  # frozen: v1.2.3`, `uses: owner/repo@<sha> # v1.2.3`) and update them deliberately: `uv run pre-commit autoupdate --freeze`, then read the diff.
