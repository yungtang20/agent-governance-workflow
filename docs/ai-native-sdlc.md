# AI-native SDLC

This is the single authority for the six-stage delivery lifecycle. It is orthogonal to execution mode: `REVIEWED_PIPELINE` and `SINGLE_EXECUTOR` describe who reviews and executes; they do not add or remove phases.

```text
PLAN -> DESIGN -> BUILD -> TEST -> DEPLOY -> MAINTAIN
                         ^                  |
                         +------------------+
```

Use risk-based tailoring. A small low-risk change may use `PLAN -> BUILD -> TEST`; a high-risk change should use all six phases. Every included phase needs input, output, gate, and evidence. Every skipped phase must be recorded as `SKIPPED_WITH_REASON`. After `BUILD`, do not skip the corresponding `TEST` without a documented exception.

## PLAN
- **Purpose**: establish intent, scope, success criteria, and risk.
- **Input**: user request, project rules, baseline evidence.
- **Output**: bounded task packet, scope, success criteria, risk classification.
- **Gate**: scope and authority are clear; material ambiguity is escalated.
- **Skip criteria**: never skip for a change that modifies behavior.

## DESIGN
- **Purpose**: choose the smallest safe approach.
- **Input**: approved plan, constraints, dependency and impact evidence.
- **Output**: design decision, affected modules, recovery thought process.
- **Gate**: architecture, security, data, and API risks are addressed.
- **Skip criteria**: localized change with no design choice, with a recorded reason.

## BUILD
- **Purpose**: implement the approved change.
- **Input**: plan, design (or documented skip), and clean baseline.
- **Output**: minimal diff and build artifacts, if applicable.
- **Gate**: diff is scoped and user changes are preserved.
- **Skip criteria**: analysis or verification-only task.

## TEST
- **Purpose**: verify behavior and quality against success criteria.
- **Input**: change, test strategy, and acceptance criteria.
- **Output**: test, lint, type-check, or other verification evidence.
- **Gate**: relevant checks pass; the same root cause is auto-fixed no more than twice.
- **Skip criteria**: no-change task or explicitly documented exception.

## DEPLOY
- **Purpose**: prepare or perform delivery to a target environment.
- **Input**: verified artifact, target, deployment plan, and authorization status.
- **Output**: deployment result, or `NOT_DEPLOYED` with reason.
- **Gate**: explicit human authorization is required for external or irreversible state changes. This package provides plans and evidence; it does not auto-deploy or install global configuration.
- **Skip criteria**: no deployable artifact, or deployment outside scope.

## MAINTAIN
- **Purpose**: observe the delivered result and capture incidents or follow-up work.
- **Input**: delivered state, agreed observation window, monitoring or feedback.
- **Output**: maintenance record, incident record, or follow-up plan.
- **Gate**: close with evidence, or escalate to a new `PLAN` cycle.
- **Skip criteria**: no delivery occurred; record `NOT_SCHEDULED` rather than implying continuous monitoring.

| Risk | Suggested phases | Non-negotiable conditions |
|---|---|---|
| Low | `PLAN -> BUILD -> TEST` | Test after behavior changes; inspect Diff |
| Medium | `PLAN -> DESIGN -> BUILD -> TEST` | Design and verification evidence |
| High | All six | Human gates for architecture, data, security, and deployment |

The record format is [`templates/lifecycle-record.md`](../templates/lifecycle-record.md). `MAINTAIN` is a bounded observation agreement, not an implicit autonomous monitor.
