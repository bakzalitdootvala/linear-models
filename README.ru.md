# linear-models

[English](README.md) · **Русский**

[![CI](https://github.com/bakzalitdootvala/linear-models/actions/workflows/ci.yml/badge.svg)](https://github.com/bakzalitdootvala/linear-models/actions/workflows/ci.yml) [![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](pyproject.toml) [![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-261230.svg)](https://docs.astral.sh/ruff/) [![Types: mypy strict](https://img.shields.io/badge/types-mypy%20strict-2a6db2.svg)](https://mypy-lang.org/)

Линейная регрессия с нуля на NumPy, сверка со scikit-learn и оценка на реальных данных.

Эталонные значения в тестах посчитаны независимо от кода, каждый тест [проверен мутацией](AGENTS.md#mutation-checks-mandatory) (он обязан упасть на нарочно сломанной копии кода), типизация строгая, а всё случайное запускается с фиксированным seed.

## Статус

В репозитории каркас проекта: инструменты, проверки, CI и документация на двух языках.

## Быстрый старт

```bash
git clone https://github.com/bakzalitdootvala/linear-models.git
cd linear-models
uv sync
uv run pytest
uv run pre-commit install
```

Требования и список проверок описаны в [docs/ru/setup.md](docs/ru/setup.md).

## Стек

- Python 3.12, виртуальное окружение и зависимости ведёт [uv](https://docs.astral.sh/uv/)
- NumPy, pandas, scikit-learn
- pytest, ruff, mypy в строгом режиме
- pre-commit-хуки и GitHub Actions запускают одни и те же проверки

## Структура

```text
.
├── src/linear_models/     код пакета
├── tests/                 тесты pytest
├── docs/
│   ├── en/                документация на английском
│   └── ru/                та же документация на русском
├── scripts/               служебные скрипты, только стандартная библиотека
└── .github/workflows/     CI
```

Ноутбуки лежат в `notebooks/`, датасеты в `data/`, которую git игнорирует.

## Языки

Идентификаторы в коде английские. Docstring'и и комментарии русские, и в коде, и в конфигурационных файлах. Документация есть на английском в `docs/en/` и на русском в `docs/ru/`, по одним и тем же путям, и любая правка на одном языке вносится в другой в том же изменении. Основной язык репозитория английский.

## Документация

Оглавление документации: [docs/ru/README.md](docs/ru/README.md). Термины из кода и документации объяснены в [глоссарии](docs/ru/GLOSSARY.md).

## Лицензия

[MIT](LICENSE).
