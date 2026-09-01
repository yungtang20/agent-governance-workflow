# Codex Agent Governance

## Execution mode

Record `execution_mode`: `REVIEWED_PIPELINE` or `SINGLE_EXECUTOR`.

Begin with minimum local evidence. Use `REVIEWED_PIPELINE` for trust-boundary architecture, security or permission changes, sensitive data, migrations, irreversible operations, unresolved evidence conflicts, or shared public interfaces.

The reviewer receives the bounded template in `task-packet.md` and remains read-only. The executor records `ACCEPT`, `ACCEPT_WITH_MODIFICATIONS`, or `REJECT` for every recommendation and performs all edits and verification.

Use `DUAL_MODEL_PASS` only when all four evidence artifacts exist. Otherwise use `SINGLE_AGENT_MODE`, `PARTIAL`, or `UNVERIFIED`.

## Universal boundaries

- Preserve user-owned changes.
- Make the smallest necessary Diff.
- Do not expose secrets or production data.
- Never claim unexecuted checks passed.
- Project-local `AGENTS.md` remains authoritative for project data and verification.

## Lifecycle

Apply the risk-based lifecycle in `docs/ai-native-sdlc.md` and record it with `templates/lifecycle-record.md`. Use the smallest justified phase set, record every skipped phase as `SKIPPED_WITH_REASON`, and never treat `DEPLOY` as authorization to change external state.
