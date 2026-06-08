"""Apply the namespace workflow-sync manifest.

This tool is intentionally independent of drift-gate's manifest schema. It
copies the manifest-declared files from an upstream checkout into a local target
checkout, then applies exact string rewrite rules to declared rewrite targets.
"""

from __future__ import annotations

import argparse
import filecmp
import json
import shutil
import sys
import tempfile
from pathlib import Path, PurePosixPath
from typing import Any


def fail(message: str) -> None:
    raise SystemExit(f"workflow sync manifest failed: {message}")


def clean_rel(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value:
        fail(f"{field} must be a non-empty string")
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts:
        fail(f"{field} must be repo-rooted and must not contain '..': {value!r}")
    return path.as_posix()


def rooted(root: Path, rel: str) -> Path:
    return root.joinpath(*PurePosixPath(rel).parts)


def load_manifest(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"{path} is not valid JSON: {exc}")
    required = {"version", "source_repo", "source_ref", "rewrite_rules", "files", "rewrite_targets"}
    if not isinstance(data, dict) or not required.issubset(data):
        fail(f"{path.name} must contain {sorted(required)}")
    if data["version"] != "1":
        fail(f"unsupported manifest version: {data['version']!r}")
    if not isinstance(data["rewrite_rules"], list):
        fail("rewrite_rules must be a list")
    if not isinstance(data["files"], list) or not data["files"]:
        fail("files must be a non-empty list")
    if not isinstance(data["rewrite_targets"], list):
        fail("rewrite_targets must be a list")
    return data


def normalized_entries(manifest: dict[str, Any]) -> list[tuple[str, str]]:
    entries: list[tuple[str, str]] = []
    targets: set[str] = set()
    for idx, item in enumerate(manifest["files"]):
        if not isinstance(item, dict):
            fail(f"files[{idx}] must be an object")
        source = clean_rel(item.get("source"), f"files[{idx}].source")
        target = clean_rel(item.get("target"), f"files[{idx}].target")
        if target in targets:
            fail(f"duplicate target path: {target}")
        targets.add(target)
        entries.append((source, target))
    return entries


def normalized_rules(manifest: dict[str, Any]) -> list[tuple[str, str]]:
    rules: list[tuple[str, str]] = []
    for idx, item in enumerate(manifest["rewrite_rules"]):
        if not isinstance(item, dict):
            fail(f"rewrite_rules[{idx}] must be an object")
        match = item.get("match")
        replace = item.get("replace")
        if not isinstance(match, str) or not match:
            fail(f"rewrite_rules[{idx}].match must be a non-empty string")
        if not isinstance(replace, str):
            fail(f"rewrite_rules[{idx}].replace must be a string")
        rules.append((match, replace))
    return rules


def copy_entries(upstream: Path, output: Path, entries: list[tuple[str, str]]) -> None:
    for source, target in entries:
        src = rooted(upstream, source)
        dst = rooted(output, target)
        if not src.is_file():
            fail(f"manifest source is missing: {source}")
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)


def apply_rewrites(output: Path, manifest: dict[str, Any], rules: list[tuple[str, str]]) -> None:
    for idx, raw_target in enumerate(manifest["rewrite_targets"]):
        target = clean_rel(raw_target, f"rewrite_targets[{idx}]")
        path = rooted(output, target)
        if not path.is_file():
            fail(f"rewrite target is missing after copy: {target}")
        text = path.read_text(encoding="utf-8")
        for match, replace in rules:
            text = text.replace(match, replace)
        path.write_text(text, encoding="utf-8", newline="")


def compare_outputs(expected_root: Path, local_target: Path, entries: list[tuple[str, str]]) -> list[str]:
    drift: list[str] = []
    for _, target in entries:
        expected = rooted(expected_root, target)
        actual = rooted(local_target, target)
        if not actual.is_file() or not filecmp.cmp(expected, actual, shallow=False):
            drift.append(target)
    return drift


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply workflow-sync-manifest.json")
    parser.add_argument("upstream_checkout_dir", type=Path)
    parser.add_argument("local_target_dir", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    manifest_path = Path.cwd() / "workflow-sync-manifest.json"
    manifest = load_manifest(manifest_path)
    entries = normalized_entries(manifest)
    rules = normalized_rules(manifest)
    upstream = args.upstream_checkout_dir.resolve()
    local_target = args.local_target_dir.resolve()

    if args.dry_run:
        with tempfile.TemporaryDirectory(prefix="workflow-sync-") as tmp:
            expected = Path(tmp) / "target"
            copy_entries(upstream, expected, entries)
            apply_rewrites(expected, manifest, rules)
            drift = compare_outputs(expected, local_target, entries)
            if drift:
                for path in drift:
                    print(f"DRIFT {path}")
                return 1
            print(f"workflow-sync-manifest dry-run: OK ({len(entries)} files)")
            return 0

    copy_entries(upstream, local_target, entries)
    apply_rewrites(local_target, manifest, rules)
    print(f"workflow-sync-manifest applied: {len(entries)} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())