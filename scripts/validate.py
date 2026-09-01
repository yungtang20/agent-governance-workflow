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
    "docs/ai-native-sdlc.md",
    "templates/AGENTS.codex.md",
    "templates/AGENTS.pi.md",
    "templates/executor.opencode.md",
    "templates/task-packet.md",
    "templates/audit-ledger.md",
    "templates/lifecycle-record.md",
)

STAGES = ("PLAN", "DESIGN", "BUILD", "TEST", "DEPLOY", "MAINTAIN")

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


def validate_lifecycle(text: str) -> list[str]:
    failures: list[str] = []
    positions = [text.find(f"## {stage}") for stage in STAGES]
    if any(position < 0 for position in positions):
        failures.append("lifecycle missing one or more stage headings")
    elif positions != sorted(positions):
        failures.append("lifecycle stages are out of order")
    for stage in STAGES:
        block_start = text.find(f"## {stage}")
        block_end = text.find("\n## ", block_start + 4)
        block = text[block_start:] if block_end < 0 else text[block_start:block_end]
        for marker in ("Input", "Output", "Gate", "Skip criteria"):
            if marker not in block:
                failures.append(f"lifecycle {stage} missing {marker}")
    if "does not auto-deploy" not in text:
        failures.append("lifecycle missing no-auto-deploy boundary")
    return failures


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
    lifecycle_path = root / "docs/ai-native-sdlc.md"
    lifecycle = lifecycle_path.read_text(encoding="utf-8") if lifecycle_path.is_file() else ""
    failures.extend(validate_lifecycle(lifecycle))
    record_path = root / "templates/lifecycle-record.md"
    record = record_path.read_text(encoding="utf-8") if record_path.is_file() else ""
    for marker in ("included_phases", "skipped_phases", "SKIPPED_WITH_REASON", "authorization_status", "automatic_fix_attempts"):
        if marker not in record:
            failures.append(f"lifecycle record missing marker: {marker}")
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
