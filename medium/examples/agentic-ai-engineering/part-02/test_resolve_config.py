import copy
import importlib.util
import json
import sys
import unittest
from pathlib import Path

import jsonschema


ROOT = Path(__file__).parent
SPEC = importlib.util.spec_from_file_location("resolve_config", ROOT / "resolve_config.py")
resolve_config = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = resolve_config
SPEC.loader.exec_module(resolve_config)


class ResolveConfigTests(unittest.TestCase):
    def setUp(self):
        self.base_path = ROOT / "base-config.yaml"
        self.overlay_path = ROOT / "production-overlay.yaml"
        self.schema_path = ROOT / "agent-config.schema.json"

    def test_resolves_exact_components_and_stable_hash(self):
        first = resolve_config.resolve(self.base_path, self.overlay_path)
        second = resolve_config.resolve(self.base_path, self.overlay_path)
        expected = json.loads((ROOT / "expected-release-record.json").read_text())
        self.assertEqual(first["resolved_config_sha256"], second["resolved_config_sha256"])
        self.assertEqual(first["components"]["model"], "provider-model-2026-08-15")
        self.assertIn("@", first["components"]["prompt"])
        self.assertEqual(
            {key: first[key] for key in expected},
            expected,
        )

    def test_unsafe_overlay_is_rejected(self):
        with self.assertRaisesRegex(resolve_config.UnsafeOverlay, "tools.allow"):
            resolve_config.resolve(self.base_path, ROOT / "unsafe-overlay.yaml")

    def test_schema_rejects_non_string_collection(self):
        config = resolve_config.load_yaml(self.base_path)
        config["retrieval"]["collections"] = [42]
        with self.assertRaises(jsonschema.ValidationError):
            resolve_config.validate_declared(config, self.schema_path)

    def test_schema_rejects_non_string_memory_field(self):
        config = resolve_config.load_yaml(self.base_path)
        config["memory"]["step"] = [{"secret": "not-a-field-name"}]
        with self.assertRaises(jsonschema.ValidationError):
            resolve_config.validate_declared(config, self.schema_path)

    def test_schema_rejects_unknown_field(self):
        config = resolve_config.load_yaml(self.base_path)
        config["guardrails"]["max_stepz"] = 8
        with self.assertRaises(jsonschema.ValidationError):
            resolve_config.validate_declared(config, self.schema_path)

    def test_cross_field_policy_rejects_mutating_tool(self):
        config = resolve_config.load_yaml(self.base_path)
        config["tools"]["allow"].append("promote_release")
        with self.assertRaisesRegex(ValueError, "mutation policy denies"):
            resolve_config.validate_policy_consistency(config)


if __name__ == "__main__":
    unittest.main()
