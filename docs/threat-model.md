# Threat Model

## Protected assets

- Credentials and personal information.
- User-owned uncommitted changes.
- Production data and configuration.
- Accurate claims about model participation and verification.

## Main threats

- Publishing local paths or secrets.
- Treating a configured subagent as proof it actually ran.
- Sending excessive repository context to a reviewer.
- Letting a read-only reviewer invoke side effects.
- Committing unrelated user files.
- Claiming local tests prove CI, deployment, or production state.

## Controls

- Minimum sufficient Task Packets and redaction.
- Explicit execution mode and decision records.
- Scoped staging and staged-Diff review.
- Validator negative tests.
- Fresh-clone smoke tests before release.
