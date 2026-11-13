import json
import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from audit import audit, is_test


class AuditTests(unittest.TestCase):
    def test_classifies_tests(self):
        self.assertTrue(is_test("python -m pytest tests/test_api.py"))
        self.assertTrue(is_test("go test ./..."))
        self.assertFalse(is_test("git status --short"))

    def test_counts_completed_events_and_repeated_commands(self):
        events = [
            {"type": "turn.started"},
            {"type": "item.started", "item": {"type": "command_execution", "command": "pytest tests"}},
            {"type": "item.completed", "item": {"type": "command_execution", "command": "pytest tests"}},
            {"type": "item.completed", "item": {"type": "command_execution", "command": "pytest   tests"}},
            {"type": "item.completed", "item": {"type": "agent_message", "text": "done"}},
            {"type": "turn.completed", "usage": {"input_tokens": 100, "cached_input_tokens": 60, "output_tokens": 10}},
        ]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "events.jsonl"
            path.write_text("\n".join(json.dumps(e) for e in events) + "\nnot json\n", encoding="utf-8")
            result = audit(path)
        self.assertEqual(result["commands_completed"], 2)
        self.assertEqual(result["test_commands_completed"], 2)
        self.assertEqual(result["duplicate_command_candidates"], 1)
        self.assertEqual(result["duplicate_test_candidates"], 1)
        self.assertEqual(result["input_tokens"], 100)
        self.assertEqual(result["cached_input_tokens"], 60)
        self.assertEqual(result["malformed_lines"], 1)

    def test_empty_log(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "empty.jsonl"
            path.write_text("", encoding="utf-8")
            self.assertEqual(audit(path)["commands_completed"], 0)


if __name__ == "__main__":
    unittest.main()
