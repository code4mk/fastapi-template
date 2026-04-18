from __future__ import annotations

import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence


def normalize_path(path: str) -> str:
    """Normalize a URL path for comparison (root becomes empty string)."""
    stripped = path.rstrip("/")
    return "" if stripped == "" else stripped


def _matcher_for_pattern(pattern: str) -> Callable[[str], bool]:
    p = pattern.strip()
    if p == "/":
        return lambda norm: norm == ""

    if p.endswith("/*"):
        base = p[:-2].rstrip("/")
        if not base:
            msg = "Invalid exclusion pattern '/*': use '/' for the root path"
            raise ValueError(msg)

        def match_prefix(norm: str, b: str = base) -> bool:
            return norm == b or norm.startswith(b + "/")

        return match_prefix

    if "*" in p:
        parts = p.split("*")
        escaped = "".join(
            re.escape(part) + ("[^/]+" if i < len(parts) - 1 else "")
            for i, part in enumerate(parts)
        )
        rx = re.compile(f"^{escaped}$")

        def match_glob(norm: str) -> bool:
            return rx.match(norm) is not None

        return match_glob

    exact = p.rstrip("/")
    if not exact:
        return lambda norm: norm == ""

    return lambda norm, target=exact: norm == target


def compile_excluded_path_matchers(patterns: Sequence[str]) -> list[Callable[[str], bool]]:
    """Build matcher callables for each pattern string."""
    return [_matcher_for_pattern(p) for p in patterns]


def is_excluded_path(path: str, matchers: Sequence[Callable[[str], bool]]) -> bool:
    """Return True if path matches any compiled matcher."""
    normalized = normalize_path(path)
    return any(m(normalized) for m in matchers)


def excluded_path_checker(patterns: Sequence[str]) -> Callable[[str], bool]:
    """Return a function that tests paths against the given pattern list."""
    matchers = compile_excluded_path_matchers(patterns)

    def check(path: str) -> bool:
        return is_excluded_path(path, matchers)

    return check
