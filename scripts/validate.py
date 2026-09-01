from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = (
    "README.md",
    "SECURITY.md",
    "CONTRIBUTING.md",
    "docs/reviewed-pipeline.md",
    "docs/single-executor.md",
    "templates/AGENTS.codex.md",
    "templates/AGENTS.pi.md",
    "templates/executor.opencode.md",
    "templates/task-packet.md",
    "templates/audit-ledger.md",
)

FORBIDDEN_PATTERNS = {
    "Windows user path": re.compile(r"[A-Za-z]:\\Users\\", re.IGNORECASE),
    "Windows drive path": re.compile(r"\b[A-Za-z]:\\(?!path\\to\\project)"),
    "POSIX user path": re.compile(r"/(?:Users|home)/[^/\s]+/"),
    "private key": re.compile(r"BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY"),
    "GitHub token": re.compile(r"\b(?:gh[opusr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,})\b"),
    "bearer token": re.compile(r"Bearer\s+[A-Za-z0-9._~+/-]{20,}", re.IGNORECASE),
    "secret assignment": re.compile(r"(?:api[_-]?key|password|secret|token)\s*[:=]\s*['\"][^<\s][^'\"]+['\"]", re.IGNORECASE),
}


def route(*, excluded: bool = False, hard: int = 0, simple: bool = False, soft: int = 0) -> str:
    if excluded:
        return "SINGLE_EXECUTOR"
    if hard:
        return "REVIEWED_PIPELINE"
    if simple:
        return "SINGLE_EXECUTOR"
    if soft >= 2:
        return "REVIEWED_PIPELINE"
    return "SINGLE_EXECUTOR"


def scan_text(path: Path, text: str) -> list[str]:
    return [f"{path}: forbidden {name}" for name, pattern in FORBIDDEN_PATTERNS.items() if pattern.search(text)]


def validate(root: Path = ROOT) -> list[str]:
    failures: list[str] = []
    for relative in REQUIRED_FILES:
        if not (root / relative).is_file():
            failures.append(f"missing required file: {relative}")

    for path in root.rglob("*"):
        if not path.is_file() or ".git" in path.parts or "__pycache__" in path.parts:
            continue
        if path.suffix.lower() not in {".md", ".py", ".txt", ".yaml", ".yml"}:
            continue
        failures.extend(scan_text(path.relative_to(root), path.read_text(encoding="utf-8")))

    reviewed = (root / "docs/reviewed-pipeline.md").read_text(encoding="utf-8") if (root / "docs/reviewed-pipeline.md").is_file() else ""
    for marker in ("REVIEWED_PIPELINE", "DUAL_MODEL_PASS", "Task Packet", "ACCEPT_WITH_MODIFICATIONS"):
        if marker not in reviewed:
            failures.append(f"reviewed pipeline missing marker: {marker}")

    scenarios = (
        (route(simple=True), "SINGLE_EXECUTOR"),
        (route(hard=1, simple=True), "REVIEWED_PIPELINE"),
        (route(soft=2), "REVIEWED_PIPELINE"),
        (route(excluded=True, hard=1), "SINGLE_EXECUTOR"),
    )
    for actual, expected in scenarios:
        if actual != expected:
            failures.append(f"route mismatch: expected {expected}, got {actual}")
    return failures


def main() -> int:
    failures = validate()
    if failures:
        print("FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("PASS: package structure, governance markers, routing, and public-content checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
