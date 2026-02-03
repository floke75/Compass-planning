---
id: STD-17-01-LLM
type: standard
area: 17-integration-patterns
title: Integration Standards (LLM View)
status: draft
created: 2026-02-03
updated: 2026-02-03
author: compass-research
summary: LLM-optimized view of integration compliance rules for secrets and error handling
tags: [integration, standards, secrets, errors, llm, view]
related:
  - STD-17-01
  - DD-17-01
  - DD-14-01
  - STD-14-01
links:
  - rel: related
    target_id: "DD-17-01"
  - rel: related
    target_id: "DD-14-01"
  - rel: related
    target_id: "STD-14-01"
  - rel: companion
    target_id: "DD-17-01"
view: llm
source_id: STD-17-01
source_updated: 2026-02-03
staleness: fresh
---

# Integration Standards (LLM View)

## LLM Summary
STD-17 defines enforceable standards for Compass integrations, focusing on secret management, error logging, and pre-deployment verification. It mandates secure storage and handling of secrets, forbids logging or committing credentials, and requires MFA and rotation practices. It also specifies required fields for integration error logs to ensure consistent debugging across services, including idempotency keys and retry metadata where applicable. The standard includes rules for safe transmission of secrets and explicit redaction requirements in logs. It provides pre-deploy checks to catch risky integrations early. It also standardizes the minimum diagnostic data required for reliable retries. Finally, it provides compliance checklists used in code review and integration testing. These standards operationalize the integration patterns in DD-17 and are intended to be simple enough for a small team to follow consistently.

## Canonical Statements
- Secrets MUST never be committed, logged, or shared insecurely.
- Integration errors MUST be logged with required fields and context.
- Pre-deployment verification MUST include the defined checklist.
- Standards apply to all external integrations.

## Scope and Non-Goals
- In scope: Secret handling rules and integration error logging requirements.
- Out of scope: Integration architecture patterns (see `DD-17-01`).

## Dependencies and Interfaces
- Integration patterns: `DD-17-01`.
- Ecosystem standards: `DD-14-01`, `STD-14-01`.

## Evidence and Freshness
- Source updated 2026-01-25; staleness marked fresh.
- No external citations required; standards are internal.

## Open Questions
- None.

## Change Log
- 2026-02-03: LLM view created from `STD-17-01` with no semantic changes.

## Enforcement
- Enforced via code review and integration testing.

## Compliance Checklist
- [ ] Secrets stored in approved manager or env vars only.
- [ ] No secrets in code, logs, or documentation.
- [ ] Error logs include required fields and retry metadata.
- [ ] Integration verification checklist completed before deploy.
