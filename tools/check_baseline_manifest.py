"""Validate the org baseline manifest consumed by drift-gate."""

from __future__ import annotations

import json
from pathlib import Path, PurePosixPath
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFESTS = (
    ROOT / "baseline-manifest.json",
    ROOT / "org-adr-manifest.json",
)
ADR_ROOT = ROOT / "docs" / "decision-records"


def fail(message: str) -> None:
    raise SystemExit(f"baseline-manifest check failed: {message}")


def manifest_path(field: str, value: Any) -> str:
    if not isinstance(value, str) or not value:
        fail(f"{field} must be a non-empty string")
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts:
        fail(f"{field} must be repo-rooted and must not contain '..': {value!r}")
    return value


def validate_manifest(manifest: Path) -> None:
    try:
        raw = json.loads(manifest.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"{manifest.name} is not valid JSON: {exc}")

    if not isinstance(raw, dict) or set(raw) != {"version", "files"}:
        fail(f"{manifest.name}: root must contain exactly 'version' and 'files'")
    if raw["version"] != "1":
        fail(f"{manifest.name}: unsupported manifest version: {raw['version']!r}")
    files = raw["files"]
    if not isinstance(files, list) or not files:
        fail(f"{manifest.name}: 'files' must be a non-empty list")

    sources: list[str] = []
    targets: set[str] = set()
    for idx, item in enumerate(files):
        if not isinstance(item, dict) or set(item) != {"source", "target"}:
            fail(f"{manifest.name}: files[{idx}] must contain exactly 'source' and 'target'")
        source = manifest_path(f"{manifest.name}: files[{idx}].source", item["source"])
        target = manifest_path(f"{manifest.name}: files[{idx}].target", item["target"])
        if target in targets:
            fail(f"{manifest.name}: duplicate target path: {target!r}")
        sources.append(source)
        targets.add(target)

    missing = [source for source in sources if not (ROOT / source).is_file()]
    if missing:
        fail(f"{manifest.name}: sources missing: {missing}")

    org_adrs = sorted(path.relative_to(ROOT).as_posix() for path in ADR_ROOT.glob("000*.md"))
    unlisted_adrs = [path for path in org_adrs if path not in sources]
    if unlisted_adrs:
        fail(f"{manifest.name}: org ADRs missing from manifest: {unlisted_adrs}")

    expected_targets = {
        f"docs/decision-records/org/{Path(source).name}"
        for source in org_adrs
    }
    missing_targets = sorted(expected_targets - targets)
    if missing_targets:
        fail(f"{manifest.name}: org ADR mirror targets missing from manifest: {missing_targets}")

    print(f"{manifest.name} check passed: {len(files)} files")


def main() -> None:
    for manifest in MANIFESTS:
        validate_manifest(manifest)


if __name__ == "__main__":
    main()
