# Lifecycle Record

```yaml
execution_mode: SINGLE_EXECUTOR
risk_level: LOW
included_phases: [PLAN, BUILD, TEST]
skipped_phases:
  - phase: DESIGN
    status: SKIPPED_WITH_REASON
    reason: localized change with no design choice
  - phase: DEPLOY
    status: SKIPPED_WITH_REASON
    reason: no deployable artifact requested
authorization_status: NOT_REQUESTED
root_cause_id: none
automatic_fix_attempts: 0
final_status: IN_PROGRESS
```

For every included phase, complete the following record. For every skipped phase, retain `SKIPPED_WITH_REASON` and a concrete reason.

## PLAN
- Input:
- Output:
- Gate:
- Evidence:

## DESIGN
- Input:
- Output:
- Gate:
- Evidence:

## BUILD
- Input:
- Output:
- Gate:
- Evidence:

## TEST
- Input:
- Output:
- Gate:
- Evidence:

## DEPLOY
- Input:
- Output (`NOT_DEPLOYED` when applicable):
- Gate (human authorization):
- Evidence:

## MAINTAIN
- Input (observation window / owner):
- Output:
- Gate (closure or escalation):
- Evidence:

## Decision and recovery
- Sol decision (if reviewed): `ACCEPT` / `ACCEPT_WITH_MODIFICATIONS` / `REJECT` / `NOT_APPLICABLE`
- Root cause and attempt number:
- If automatic attempts exceed 2: `STOPPED_AWAITING_HUMAN`
- Final status: `COMPLETE` / `PARTIAL` / `UNKNOWN` / `STOPPED_AWAITING_HUMAN`
