# CLI Mapping

| Environment | Default mode | Entry template | Independent review |
|---|---|---|---|
| Codex | Capability-routed | `templates/AGENTS.codex.md` | Allowed only when runtime evidence exists |
| Pi | `SINGLE_EXECUTOR` | `templates/AGENTS.pi.md` | Not required |
| OpenCode | `SINGLE_EXECUTOR` | `templates/executor.opencode.md` | Not required |

Model names and providers are local configuration. The governance contract depends on observed capabilities and artifacts, not role labels.

All environments may use the same risk-based lifecycle record. Only the execution mode differs: Codex may route to an independently evidenced review; other CLIs use one executor.
