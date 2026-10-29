#!/usr/bin/env python3
"""Проверка, что относительные ссылки в Markdown-файлах ведут на существующие файлы и заголовки.

Внешние ссылки (``http://``, ``https://``, ``mailto:``) пропускаются. Проверяются встроенные
ссылки, включая цели в ``<...>`` и заголовки в кавычках, и определения ссылок в стиле
reference. Относительная ссылка должна указывать на существующий файл или каталог, где
ведущий ``/`` означает корень репозитория. Если у ссылки есть якорь, он должен совпасть с
заголовком целевого файла по правилам GitHub. Блоки кода и inline-код игнорируются, поэтому
примеры внутри них никогда не считаются ссылками. Каталог ``info/`` в корне (личные заметки,
которые git игнорирует) не проверяется.
"""

import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", ".venv", ".mypy_cache", ".ruff_cache", ".pytest_cache", "node_modules"}
# Каталоги в корне репозитория, которые git игнорирует: личные заметки не проверяются.
SKIP_ROOT_DIRS = {"info"}
EXTERNAL = ("http://", "https://", "mailto:")

LINK = re.compile(
    r"!?\[[^\]]*\]\(\s*(?:<([^>]+)>|([^)\s]+))"
    r"(?:\s+(?:\"[^\"]*\"|'[^']*'|\([^)]*\)))?\s*\)"
)
REF_DEF = re.compile(r"^ {0,3}\[(?!\^)[^\]]+\]:\s*<?([^\s>]+)>?", re.MULTILINE)
FENCE = re.compile(r"^(```|~~~).*?^\1", re.MULTILINE | re.DOTALL)
INLINE_CODE = re.compile(r"`[^`\n]*`")
HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$", re.MULTILINE)


def markdown_files() -> list[Path]:
    """Все Markdown-файлы репозитория, кроме служебных каталогов и личных заметок."""
    return sorted(
        path
        for path in ROOT.rglob("*.md")
        if not SKIP_DIRS.intersection(path.relative_to(ROOT).parts)
        and path.relative_to(ROOT).parts[0] not in SKIP_ROOT_DIRS
    )


def strip_code(text: str) -> str:
    """Убирает блоки кода, затем inline-код."""
    return INLINE_CODE.sub("", FENCE.sub("", text))


def github_anchor(heading: str) -> str:
    """Превращает заголовок в якорь, который GitHub строит для него."""
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", heading)
    text = re.sub(r"[^\w\- ]", "", text.strip().lower())
    return text.replace(" ", "-")


def anchors(path: Path) -> set[str]:
    """Все якоря файла; повторяющиеся заголовки получают суффиксы ``-1``, ``-2``, как на GitHub.

    Здесь убираются только блоки кода: inline-код внутри заголовка входит в его якорь.
    """
    seen: dict[str, int] = {}
    result: set[str] = set()
    for heading in HEADING.findall(FENCE.sub("", path.read_text(encoding="utf-8"))):
        base = github_anchor(heading)
        count = seen.get(base, 0)
        seen[base] = count + 1
        result.add(base if count == 0 else f"{base}-{count}")
    return result


def link_targets(text: str) -> list[str]:
    """Цели встроенных ссылок и определений ссылок в стиле reference."""
    inline = [angle or bare for angle, bare in LINK.findall(text)]
    return inline + REF_DEF.findall(text)


def main() -> int:
    files = markdown_files()
    problems: list[str] = []
    checked = 0
    for source in files:
        where = source.relative_to(ROOT).as_posix()
        for target in link_targets(strip_code(source.read_text(encoding="utf-8"))):
            if target.startswith(EXTERNAL):
                continue
            checked += 1
            raw_path, _, raw_anchor = target.partition("#")
            path_part = unquote(raw_path.split("?", 1)[0])
            anchor = unquote(raw_anchor)
            base = ROOT if path_part.startswith("/") else source.parent
            resolved = (base / path_part.lstrip("/")).resolve() if path_part else source
            if not resolved.exists():
                problems.append(f"{where}: {target} — no such file or directory")
            elif (
                anchor
                and resolved.is_file()
                and resolved.suffix == ".md"
                and anchor.lower() not in anchors(resolved)
            ):
                problems.append(f"{where}: {target} — no such heading")

    for line in problems:
        print(line)
    if problems:
        return 1
    print(f"relative links: {checked} checked in {len(files)} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
