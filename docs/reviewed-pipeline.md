# Reviewed Pipeline

Use `REVIEWED_PIPELINE` when a task crosses trust boundaries, changes security or permissions, performs irreversible operations, affects a shared public interface, or otherwise requires independent reasoning.

```text
Executor evidence collection
  -> 1-3K token Task Packet
    -> independent read-only reviewer
      -> executor ACCEPT / ACCEPT_WITH_MODIFICATIONS / REJECT
        -> implementation and verification
```

The reviewer receives only the minimum sufficient evidence. It cannot modify files, invoke side-effect tools, expand authorization, or request secrets.

`DUAL_MODEL_PASS` requires all four artifacts:

1. Task Packet.
2. Independent reviewer response.
3. Executor decision record.
4. Final test, Diff, and required graph evidence.

If independent review cannot be proven, downgrade to `SINGLE_EXECUTOR` and record the reason.
