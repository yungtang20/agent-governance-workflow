# Single Executor

`SINGLE_EXECUTOR` is the portable default for Pi, OpenCode, and CLIs without a verifiable independent reviewer.

The same agent performs:

```text
understand -> evidence -> self-review checkpoint -> minimal change -> tests -> Diff -> report
```

It may use a Task Packet as an internal checkpoint, but must not claim that a second model or independent reviewer participated. Reports use `SINGLE_AGENT_MODE`.
