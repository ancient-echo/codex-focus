#!/usr/bin/env python3
"""Offline summary of Codex `codex exec --json` event logs.

Processes local logs only. Outputs aggregate statistics; command bodies are not
printed because they may contain sensitive paths or literals.
"""
from __future__ import annotations

import argparse
import collections
import json
import re
from pathlib import Path

TEST_RE = re.compile(
    r"\b(?:pytest|unittest|jest|vitest|cargo\s+test|go\s+test|node\s+--test|"
    r"npm\s+(?:run\s+)?test|pnpm\s+(?:run\s+)?test|yarn\s+test|"
    r"mvn\s+test|gradle\s+test|dotnet\s+test|make\s+test)\b",
    re.IGNORECASE,
)


def is_test(command: str) -> bool:
    return bool(TEST_RE.search(command))


def audit(path: Path) -> dict:
    usages = collections.Counter()
    commands: list[str] = []
    test_commands: list[str] = []
    turns = messages = malformed = 0

    with path.open("r", encoding="utf-8") as stream:
        for line in stream:
            if not line.strip():
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                malformed += 1
                continue
            if not isinstance(event, dict):
                malformed += 1
                continue
            event_type = event.get("type")
            if event_type == "turn.completed":
                turns += 1
                usage = event.get("usage") or {}
                if isinstance(usage, dict):
                    for key in ("input_tokens", "cached_input_tokens", "output_tokens", "reasoning_output_tokens"):
                        value = usage.get(key, 0)
                        if isinstance(value, (int, float)) and not isinstance(value, bool) and value >= 0:
                            usages[key] += value
            elif event_type == "item.completed":
                item = event.get("item") or {}
                if not isinstance(item, dict):
                    continue
                if item.get("type") == "agent_message":
                    messages += 1
                if item.get("type") == "command_execution":
                    command = item.get("command") or ""
                    if not isinstance(command, str):
                        command = ""
                    normalized = " ".join(command.strip().split())
                    if normalized:
                        commands.append(normalized)
                        if is_test(normalized):
                            test_commands.append(normalized)

    counts = collections.Counter(commands)
    test_counts = collections.Counter(test_commands)
    return {
        "file": path.name,
        "turns_completed": turns,
        "agent_messages": messages,
        "input_tokens": usages["input_tokens"],
        "cached_input_tokens": usages["cached_input_tokens"],
        "output_tokens": usages["output_tokens"],
        "reasoning_output_tokens": usages["reasoning_output_tokens"],
        "commands_completed": len(commands),
        "test_commands_completed": len(test_commands),
        "duplicate_command_candidates": sum(n - 1 for n in counts.values() if n > 1),
        "duplicate_test_candidates": sum(n - 1 for n in test_counts.values() if n > 1),
        "malformed_lines": malformed,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("logs", type=Path, nargs="+", help="Codex JSONL log(s)")
    parser.add_argument("--json", action="store_true", help="Print JSON for CI or analysis")
    args = parser.parse_args()
    results = [audit(path) for path in args.logs]
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for result in results:
            print(f"{result['file']} | turns={result['turns_completed']} | "
                  f"input={result['input_tokens']} (cached={result['cached_input_tokens']}) "
                  f"output={result['output_tokens']} | commands={result['commands_completed']} "
                  f"tests={result['test_commands_completed']} | "
                  f"repeat_candidates={result['duplicate_command_candidates']} "
                  f"(tests={result['duplicate_test_candidates']})")
        print("Note: identical commands can be legitimate after edits or failures. "
              "Token totals are logged usage, not cash cost or subscription quota.")


if __name__ == "__main__":
    main()
