# Agent Governance Workflow

A portable, evidence-first governance kit for coding agents.

It supports two execution modes:

- `REVIEWED_PIPELINE`: an executor prepares a bounded Task Packet, an independent read-only reviewer analyzes it, and the executor records decisions and performs verification.
- `SINGLE_EXECUTOR`: one agent plans, executes, and verifies without claiming independent model review.

Codex can use `REVIEWED_PIPELINE` when the runtime proves an independent reviewer was actually invoked. Pi, OpenCode, and other CLIs default to `SINGLE_EXECUTOR`.

## Quick start

1. Copy the relevant files from `templates/` into your agent configuration.
2. Replace placeholders such as `${PROJECT_ROOT}` and `${AGENT_GOVERNANCE_HOME}`.
3. Keep project-specific authority in the project's own `AGENTS.md`.
4. Run:

```text
python scripts/validate.py
python -m unittest discover -s tests -v
```

Configuration does not prove that an independent review occurred. `DUAL_MODEL_PASS` requires a Task Packet, independent reviewer response, executor decision record, and final verification evidence.

## Safety

- Do not copy secrets, personal paths, production data, or real audit records into a public repository.
- The first release intentionally contains no installer that writes global configuration.
- See `SECURITY.md` and `docs/threat-model.md` before publishing changes.

## License

Licensed under the MIT License. See `LICENSE`.
