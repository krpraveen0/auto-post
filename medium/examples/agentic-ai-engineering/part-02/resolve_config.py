"""Resolve and validate the six-surface configuration taught in Part 02."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

import jsonschema
import yaml


ALLOWED_OVERRIDE_PATHS = {
    "model.id",
    "model.max_output_tokens",
    "retrieval.max_results",
}
MUTATING_TOOLS = {"promote_release", "delete_release", "write_repository"}
REGISTRIES = {
    "prompts": {"release-analyst-v2": "release-analyst-v2@sha256:8b7f0d1"},
    "models": {"stable-model": "provider-model-2026-08-15"},
    "tools": {
        "read_release_notes": "read_release_notes@1.3.0",
        "read_test_summary": "read_test_summary@1.1.0",
        "request_clarification": "request_clarification@1.0.0",
        "promote_release": "promote_release@2.0.0",
    },
}


class UnsafeOverlay(ValueError):
    pass


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain one mapping")
    return value


def flatten_leaves(value: Any, prefix: str = "") -> dict[str, Any]:
    if not isinstance(value, dict):
        return {prefix: value}
    leaves: dict[str, Any] = {}
    for key, child in value.items():
        path = f"{prefix}.{key}" if prefix else key
        leaves.update(flatten_leaves(child, path))
    return leaves


def set_path(target: dict[str, Any], path: str, value: Any) -> None:
    keys = path.split(".")
    cursor = target
    for key in keys[:-1]:
        if key not in cursor or not isinstance(cursor[key], dict):
            raise UnsafeOverlay(f"overlay cannot create unknown object {key!r}")
        cursor = cursor[key]
    if keys[-1] not in cursor:
        raise UnsafeOverlay(f"overlay cannot create unknown field {path!r}")
    cursor[keys[-1]] = copy.deepcopy(value)


def merge_strict(base: dict[str, Any], overlay: dict[str, Any]) -> dict[str, Any]:
    merged = copy.deepcopy(base)
    for path, value in flatten_leaves(overlay).items():
        if path not in ALLOWED_OVERRIDE_PATHS:
            raise UnsafeOverlay(f"production overlay cannot change {path!r}")
        set_path(merged, path, value)
    return merged


def bind_references(config: dict[str, Any]) -> dict[str, Any]:
    resolved = copy.deepcopy(config)
    prompt_alias = resolved["prompt"]["id"]
    model_alias = resolved["model"]["id"]
    resolved["prompt"]["requested_id"] = prompt_alias
    resolved["prompt"]["id"] = REGISTRIES["prompts"][prompt_alias]
    resolved["model"]["requested_id"] = model_alias
    resolved["model"]["id"] = REGISTRIES["models"][model_alias]
    resolved["tools"]["resolved_versions"] = {
        name: REGISTRIES["tools"][name]
        for name in resolved["tools"]["allow"]
    }
    return resolved


def validate_declared(config: dict[str, Any], schema_path: Path) -> None:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator(schema).validate(config)


def validate_policy_consistency(config: dict[str, Any]) -> None:
    allowed_mutations = set(config["tools"]["allow"]) & MUTATING_TOOLS
    if config["guardrails"]["mutation_policy"] == "deny" and allowed_mutations:
        names = ", ".join(sorted(allowed_mutations))
        raise ValueError(f"mutation policy denies allowed mutating tools: {names}")


def canonical_sha256(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def resolve(base_path: Path, overlay_path: Path) -> dict[str, Any]:
    declared = load_yaml(base_path)
    overlay = load_yaml(overlay_path)
    schema_path = Path(__file__).with_name("agent-config.schema.json")
    merged = merge_strict(declared, overlay)
    validate_declared(merged, schema_path)
    validate_policy_consistency(merged)
    resolved = bind_references(merged)
    return {
        "agent_id": resolved["agent_id"],
        "config_version": resolved["config_version"],
        "resolved_config_sha256": canonical_sha256(resolved),
        "components": {
            "prompt": resolved["prompt"]["id"],
            "model": resolved["model"]["id"],
            "tools": resolved["tools"]["resolved_versions"],
        },
        "resolved": resolved,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("base", type=Path)
    parser.add_argument("overlay", type=Path)
    args = parser.parse_args()
    print(json.dumps(resolve(args.base, args.overlay), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
