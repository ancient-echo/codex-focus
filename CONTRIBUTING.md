# Contributing to Codex Focus

Thanks for helping evaluate this early prototype. Both positive and negative results are useful.

## Report an issue

Please provide (only if you can share it safely):
- Codex CLI version, OS, model, and relevant installation method.
- A **minimal, non-sensitive** task that reproduces the behavior.
- Expected outcome versus observed outcome.
- Whether the issue concerns answer clarity, unnecessary tests, duplicate commands, or analyzer correctness.
- If comparing baseline and Focus, the aggregated analyzer output and whether the task passed its checks.

**Do not upload raw Codex logs, secrets, private source code, user data, or access tokens.**

## Make a change

1. Fork the repository and create a focused branch.
2. Keep scope narrow. Don't weaken safety, authorization, privacy, or project-mandated verification.
3. Run `python -m unittest discover -s tests -v`.
4. Open a PR describing the behavior change, evidence, and limitations.

## How to evaluate

Use two identical clean test worktrees, with matching model, task, agent configuration, and permissions. The baseline must not contain Codex Focus instructions. Confirm correctness **before** interpreting token savings. Prefer several small and medium tasks instead of a single cherry-picked run.

The analyzer's duplicate-command counters are potential repeats, **not proof of unnecessary work**. Qualitative comments about decisive responses should be accompanied by concrete examples when possible.

## Current roadmap

- [ ] Collect reproducible baseline vs Focus feedback.
- [ ] Add task-correctness and verification-status reporting.
- [ ] Better identify potentially redundant checks by correlating commands with file changes.
- [ ] Validate compatibility with future Codex CLI output changes.
- [ ] Build a representative, public benchmark with no proprietary inputs.

This project is independent and is not affiliated with or endorsed by OpenAI.
