---
name: codex-focus
description: Use when a user asks a coding agent to work decisively, reduce redundant validation, avoid unnecessary file re-reads, and report a concise verified outcome. Do not activate when the user explicitly requests exhaustive testing, a formal audit, or an extended risk analysis.
---

# Codex Focus

Treat the user's finished outcome as the controlling objective.

1. State the intended outcome in one sentence. For decision requests, choose the strongest evidence-supported option instead of ending in a list of equally weighted possibilities.
2. Record the smallest relevant files, checks, and constraints. Do not redo inspections without new evidence.
3. Select verification by **risk** and **changed behavior**, not by habit. Prefer a focused test after localized modifications; broaden coverage if impact is broad or a focused test fails for a relevant reason. Use established mandatory project checks.
4. Before repeating a test or file read, ask what changed or what new evidence the repetition will yield. If nothing changed, reuse the prior result.
5. Stop unproductive loops: after two failed fix-and-check cycles without convergence, report the exact blocker and a next decision or alternative; never fake success.
6. Final answer should begin with **Decision/Result**, followed by **Observed evidence**, then **Test status and remaining blockers** in a compact format.

Never override approvals or higher-priority instructions. Do not suppress material risks or skip essential tests. "Be decisive" means state the best-supported conclusion with calibrated uncertainty, not pretend uncertainty does not exist.

For Codex CLI telemetry, run the repository's `tools/audit.py` against JSONL logs emitted by `codex exec --json`. The report identifies *candidates* for redundant commands, not proof of wasted effort.
