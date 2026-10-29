#!/usr/bin/env python3
"""Проверка, что английская и русская документация зеркальны.

Документация лежит в ``docs/en/`` и ``docs/ru/``, верхние страницы в ``README.md`` и
``README.ru.md``. Скрипт проверяет, что:

- у каждого файла в ``docs/en/`` есть пара в ``docs/ru/`` по тому же пути, и наоборот; скрытые
  файлы вроде ``.DS_Store`` игнорируются;
- каждый Markdown-файл ссылается на свою пару на другом языке;
- каждая страница, кроме ``README.md``, перечислена в оглавлении ``README.md`` своего языка;
- ``README.md`` и ``README.ru.md`` ссылаются друг на друга и на оглавление документации своего
  языка.

Скрипт печатает каждую найденную проблему и завершается с кодом 1, если проблемы есть. Пустое
дерево ``docs/en/`` тоже ошибка: проверка, которая сравнивает ничто с ничем, проходила бы, ничего
не проверив.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = {"en": "README.md", "ru": "README.ru.md"}
OTHER = {"en": "ru", "ru": "en"}
INDEX = Path("README.md")


def docs_dir(language: str) -> Path:
    """Каталог документации языка: ``docs/<язык>/``."""
    return ROOT / "docs" / language


def tree_files(language: str) -> set[Path]:
    """Все нескрытые файлы дерева языка, пути отсчитываются от ``docs/<язык>/``."""
    base = docs_dir(language)
    if not base.is_dir():
        return set()
    files = (path.relative_to(base) for path in base.rglob("*") if path.is_file())
    return {path for path in files if not any(part.startswith(".") for part in path.parts)}


def read(path: Path) -> str:
    """Текст файла или пустая строка, если файла нет."""
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def main() -> int:
    trees = {language: tree_files(language) for language in README}
    problems: list[str] = []

    for language, files in trees.items():
        other = OTHER[language]
        problems += [
            f"docs/{language}/{path.as_posix()} has no twin under docs/{other}/"
            for path in sorted(files - trees[other])
        ]
    problems += [f"{name} is missing" for name in README.values() if not (ROOT / name).is_file()]
    if not trees["en"]:
        problems.append("docs/en/ has no files: there is nothing to compare")

    for language, files in trees.items():
        index = read(docs_dir(language) / INDEX)
        for path in sorted(item for item in files if item.suffix == ".md"):
            where = f"docs/{language}/{path.as_posix()}"
            twin = "../" * len(path.parts) + f"{OTHER[language]}/{path.as_posix()}"
            if f"]({twin})" not in read(docs_dir(language) / path):
                problems.append(f"{where} does not link to its twin {twin}")
            if path != INDEX and f"]({path.as_posix()})" not in index:
                problems.append(f"{where} is not listed in docs/{language}/{INDEX.as_posix()}")

    for language, name in README.items():
        top = read(ROOT / name)
        other_name = README[OTHER[language]]
        if f"]({other_name})" not in top:
            problems.append(f"{name} does not link to {other_name}")
        docs_index = f"docs/{language}/{INDEX.as_posix()}"
        if f"]({docs_index})" not in top:
            problems.append(f"{name} does not link to {docs_index}")

    for line in problems:
        print(line)
    if problems:
        return 1
    pages = sum(1 for item in trees["en"] if item.suffix == ".md")
    print(f"ru/en parity: {pages} pages per language, cross-linked and indexed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
