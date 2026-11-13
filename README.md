# Codex Focus

**Make AI coding agents more decisive, proportionate in testing, and measurable.**

Codex Focus is an **experimental, independent, open-source toolkit** for users of OpenAI Codex CLI. It combines a project instruction file, an optional Agent Skill, and a local telemetry analyzer.

> **Early public prototype (v0.1.0).** We have not yet established that it reduces tokens, latency, or failures on real tasks. Help us test that claim! Codex Focus is not an official OpenAI product.

## What it does

- **Clearer conclusions:** lead with an evidence-supported decision; label unknowns rather than hedge indefinitely.
- **Proportionate checks:** pick tests based on the change and its risks, not a blanket "run everything" habit.
- **Less repetition:** reuse unchanged evidence, avoid rereading files, and question repeated commands.
- **Measurable behavior:** analyze `codex exec --json` logs for token usage, command counts, and potential repeats.

It does **not** modify the model, intercept commands, automatically prevent tests, override system policies, or guarantee better behavior.

## Install — try in a disposable repository first

**Project-level install (recommended):**

1. Copy [`AGENTS.md`](AGENTS.md) into the root of a small test repository. If it already has an `AGENTS.md`, **merge the rules** rather than overwrite them.
2. Optionally copy [`.agents/skills/codex-focus/`](.agents/skills/codex-focus/SKILL.md) into the test repository for explicit invocation with `$codex-focus`.
3. Start a new Codex session inside the repository and give it a bounded coding task.

**Personal default (advanced):** after backing up existing instructions, merge these rules into `~/.codex/AGENTS.md`. You can place the Skill in `~/.agents/skills/codex-focus/`. Prefer project-level installation for initial experiments.

## Measure baseline vs Focus

Run the **same task on two separate clean copies** of the same repo, with the same model, prompt, approval settings, and tool access. Only one copy should have Focus instructions.

```bash
# From the baseline worktree (illustrative; requires Codex CLI and login):
codex exec --json "Fix the failing parser test with minimal changes" > baseline.jsonl

# From a separate, equally clean worktree with Focus instructions:
codex exec --json "Fix the failing parser test with minimal changes" > focus.jsonl

# From the codex-focus directory:
python tools/audit.py /path/to/baseline.jsonl /path/to/focus.jsonl
python tools/audit.py --json /path/to/baseline.jsonl /path/to/focus.jsonl
```

Make sure both variants **actually solve the task correctly**. Repeat across several tasks/trials: one lower-token run is not proof. Do not use sensitive production repos for experiments.

The analyzer currently reports completed turns and commands, test-like command counts, exact-command repeat candidates, and reported input/output/cached token counts. **Identical commands are not necessarily waste** (for example, rerunning tests after edits is often correct). Token usage is **not** a cash price or a subscription quota estimate.

## Privacy

JSONL logs can contain prompts, source code, file paths, and tool outputs. The analyzer is **local-only** and prints aggregate counts by default. **Never commit or share raw logs** unless you have reviewed and redacted them. The included `.gitignore` excludes common log names.

## Limitations

- An instruction file does not guarantee the agent will comply.
- This prototype does not objectively score decisiveness or task correctness.
- Command repetition is a weak proxy for inefficiency.
- Mandatory CI, safety, privacy, and authorization requirements still apply.
- The analyzer supports the documented Codex CLI JSONL event shapes; behavior may change across CLI versions.

## Development and feedback

Run tests (Python 3.10+, standard library only):

```bash
python -m unittest discover -s tests -v
```

Feedback is welcome, including **cases where Focus made things worse**. Open an [Issue](../../issues/new/choose) with the Codex version, a minimal reproducible task, before/after results, and any constraints. **Do not post private logs, credentials, or proprietary source code.**

See [CONTRIBUTING.md](CONTRIBUTING.md) for experiment and contribution guidance.

MIT license. Maintained by community contributors.
