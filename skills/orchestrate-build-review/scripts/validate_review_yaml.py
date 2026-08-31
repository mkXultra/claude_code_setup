#!/usr/bin/env python3
"""Validate orchestrate-build-review reviewer YAML artifacts."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ModuleNotFoundError:
    print(
        "ERROR: PyYAML is required to validate review artifacts",
        file=sys.stderr,
    )
    raise SystemExit(2)


REQUIRED_FINDING_KEYS = (
    "key",
    "position",
    "severity",
    "target",
    "reason",
    "fix",
)
POSITIONS = {"needs_fix", "no_fix"}


class UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate mapping keys."""


def _construct_unique_mapping(
    loader: UniqueKeyLoader,
    node: yaml.nodes.MappingNode,
    deep: bool = False,
) -> dict[Any, Any]:
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in mapping
        except TypeError as exc:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                "found an unhashable mapping key",
                key_node.start_mark,
            ) from exc
        if duplicate:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                f"found duplicate key {key!r}",
                key_node.start_mark,
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_unique_mapping,
)


def _is_non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_document(document: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(document, dict):
        return ["top-level document must be a mapping"]

    summary = document.get("verification_summary")
    if not _is_non_empty_string(summary):
        errors.append("verification_summary must be a non-empty string")

    findings = document.get("findings")
    if not isinstance(findings, list):
        errors.append("findings must be a list")
        return errors

    seen_keys: set[str] = set()
    for index, finding in enumerate(findings):
        prefix = f"findings[{index}]"
        if not isinstance(finding, dict):
            errors.append(f"{prefix} must be a mapping")
            continue

        missing = [key for key in REQUIRED_FINDING_KEYS if key not in finding]
        if missing:
            errors.append(f"{prefix} is missing keys: {', '.join(missing)}")

        for key in REQUIRED_FINDING_KEYS:
            if key in finding and not _is_non_empty_string(finding[key]):
                errors.append(f"{prefix}.{key} must be a non-empty string")

        position = finding.get("position")
        if isinstance(position, str) and position not in POSITIONS:
            errors.append(
                f"{prefix}.position must be one of: {', '.join(sorted(POSITIONS))}"
            )

        finding_key = finding.get("key")
        if _is_non_empty_string(finding_key):
            if finding_key in seen_keys:
                errors.append(f"{prefix}.key duplicates {finding_key!r}")
            seen_keys.add(finding_key)

    return errors


def validate_path(path: Path) -> list[str]:
    try:
        source = path.read_text(encoding="utf-8")
    except OSError as exc:
        return [f"cannot read file: {exc}"]

    try:
        document = yaml.load(source, Loader=UniqueKeyLoader)
    except yaml.YAMLError as exc:
        return [f"invalid YAML: {exc}"]

    return validate_document(document)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate orchestrate-build-review reviewer YAML files."
    )
    parser.add_argument("files", nargs="+", type=Path)
    args = parser.parse_args(argv)

    invalid = False
    for path in args.files:
        errors = validate_path(path)
        if errors:
            invalid = True
            for error in errors:
                print(f"INVALID {path}: {error}", file=sys.stderr)
        else:
            print(f"VALID {path}")

    return 1 if invalid else 0


if __name__ == "__main__":
    raise SystemExit(main())
