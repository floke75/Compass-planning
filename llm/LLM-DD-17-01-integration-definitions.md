---
id: DD-17-01-LLM
type: definition
area: 17-integration-patterns
title: Integration Architecture Patterns (LLM View)
created: 2026-02-03
updated: 2026-02-03
summary: LLM-optimized view of integration patterns and reliability rules
tags: [integration, patterns, webhooks, retries, secrets, llm, view]
links:
  - rel: related
    target_id: "RF-01-01"
  - rel: related
    target_id: "DD-14-01"
  - rel: related
    target_id: "STD-14-01"
  - rel: companion
    target_id: "STD-17-01"
view: llm
source_id: DD-17-01
source_updated: 2026-02-03
staleness: fresh
---

# Integration Architecture Patterns (LLM View)

## LLM Summary
DD-17 defines standard integration patterns for how Compass connects to external systems. It categorizes integrations (implementation platforms, PM tools, research sources, authentication) and prescribes a mutation-then-scheduled-action pattern for most external API calls to isolate user experience from external failures. It provides guidance on when to use webhooks versus polling, recommends starting with polling for simplicity, and suggests hybrid webhook plus polling for reliability. The document establishes idempotency expectations, retry strategies, error handling, rate-limit behavior, and secret management principles tailored to a small team. These patterns are designed to reduce snowflake integrations and improve reliability without heavy infrastructure. It also clarifies when to bypass the pattern for interactive LLM responses. DD-17 is enforced by STD-17, which provides concrete compliance checklists and required logging fields.

## Canonical Statements
- External API calls SHOULD use mutation -> scheduled action pattern.
- Integrations MUST be idempotent and retry-safe.
- Webhooks are preferred when reliable; polling is acceptable by default.
- Secrets MUST be managed outside code and never logged.

## Scope and Non-Goals
- In scope: Integration patterns, reliability rules, and routing guidance.
- Out of scope: Tool-specific configuration and enforcement checklists.

## Dependencies and Interfaces
- Ecosystem context: `DD-14-01`.
- Enforcement standard: `STD-17-01`.

## Core Invariants
- Reliability over immediacy for external calls.
- Idempotency is mandatory for retries.
- Start simple, add complexity only when needed.

## Glossary Snapshot
- **Mutation -> action pattern**: Store intent then execute externally.
- **Idempotency key**: Stable identifier to prevent duplicate effects.
- **Polling**: Periodic fetch for updates when webhooks are unreliable.
