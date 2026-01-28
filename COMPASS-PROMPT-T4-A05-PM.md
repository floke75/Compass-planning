# Research Phase: Project Management Integration

**Area**: 05 | **Tier**: 4 (Integration & Handoff) | **Track**: A (External Research)

---

## Instructions

Copy everything below this line and paste it into a new Claude chat. Ensure the Compass System Definition is available as project context.

**Recommended**: Use Claude's deep research capability for this phase.

---

## Pre-Research Setup

### Mandatory Context (Must Be Available)
- **Compass System Definition** (`Compass___System_Definition.md`) — Read Part 1.5 (Who Uses Compass) and Part 3.6 (External Integrations)
- **COMPASS-00-REFERENCE-INDEX.md** — Check for any completed prior research

### Optional Context (Use If Available)
- `DD-17-01-integration-definitions.md` — Integration patterns (idempotency, retry, error handling)
- `STD-17-01-integration-standards.md` — Secret management, error logging

---

## Important Instructions

1. **Read the Compass System Definition first**, particularly:
   - Part 1.5: Who Uses Compass (secondary users need PM visibility)
   - Part 3.6: External Integrations (PM is bidirectional sync)
   - Part 3.3: Interface Requirements (secondary interface)

2. **Do not ask the user technical questions** — research and surface insights about PM tools and their APIs.

3. **Use deep research** to investigate PM tool APIs, webhooks, and integration patterns.

4. **If A17 research exists**, apply integration patterns. If not, assume standard webhook/API patterns.

---

## Available Context (If Present)

### From DD-17-01 (Integration Patterns) — Extract If Available:
- Standard integration architecture
- Idempotency approach
- Retry/backoff strategy
- Error handling standards
- Secret management requirements

### If DD-17-01 Is Not Available:
Assume:
- Webhook-based integration where possible
- Exponential backoff for retries
- Structured error logging
- Secure API key storage

---

# RESEARCH TASK: Evaluate and Select Project Management Integration

## Context

You are researching PM integration options for **Compass**, an LLM-orchestrated planning, research, and documentation system for EFN (a financial news broadcaster with ~120 people).

This is a **Track A (External Research)** task. You are evaluating PM tools against integration criteria.

**Why This Matters**: Secondary users need visibility into planning through familiar tools. Bugs and requests need a path into the planning process.

## Scope

### Questions to Answer

1. **Minimal vs Full Integration**:
   - Phase 1: Basic visibility, manual task creation
   - Phase 4: Automated sync, bidirectional updates

2. **Bug/Request Intake**: How do bugs become planning inputs without turning Compass into a bug tracker?

3. **Artifact Sync**: What Compass artifacts should sync to PM tools?
   - Milestones and timeline
   - Tasks and work breakdown
   - Decision references

4. **Automation Level**: What's the right balance of automation vs manual control?

### Out of Scope
- Backend platform selection (Area 01)
- Handoff bundle format (Area 11)
- Detailed task schema design

## Evaluation Criteria

### Required Capabilities

| Capability | Requirement |
|------------|-------------|
| API quality | Programmatic access, webhooks, reasonable rate limits |
| Visual UI | Suitable for daily use by secondary users |
| Issue tracking | Supports bugs and planning items |
| Document linking | Can reference external documentation |
| Pricing | Fits EFN team size budget |

### Integration Quality (per A17 patterns)
- Webhook support
- API completeness
- Rate limits
- Authentication methods
- Idempotency support

## Candidates to Investigate

1. **Linear** — Excellent API, clean UI, strong workflow
2. **GitHub Issues/Projects** — Tight code integration, free
3. **Plane.so** — Open source, self-hostable
4. **Notion Databases** — Flexible, familiar UI

## Required Outputs

### 1. Research Findings Document (RF-05-01)

**Output File**: `RF-05-01-pm-findings.md`

**Frontmatter Schema**:
```yaml
---
id: RF-05-01
type: rf
area: 05-pm-integration
title: Project Management Integration Research Findings
status: draft
created: 2026-01-XX
updated: 2026-01-XX
author: compass-research
summary: Evaluates PM tools for Compass integration
tags: [pm, integration, project-management]
related:
  - DD-17-01
  - STD-17-01
confidence: high
methodology: "Web research with API analysis"
limitations: []
responds_to: null
implications_for: []
---
```

**Required Sections**:
1. **Executive Summary** — Recommendation, confidence, key trade-offs
2. **Capability Matrix** — API quality, webhooks, UI, pricing per candidate
3. **Integration Pattern Fit** — How well each fits A17 patterns
4. **Phased Integration Plan** — Phase 1 (visibility) vs Phase 4 (bidirectional)
5. **Artifact Mapping** — Compass artifacts → PM objects
6. **Recommendation** — Primary choice with rationale

### 2. Architecture Decision Record (ADR-05-01)

**Output File**: `ADR-05-01-pm-selection.md`

**Frontmatter Schema**:
```yaml
---
id: ADR-05-01
type: adr
area: 05-pm-integration
title: Project Management Integration Selection
status: proposed
created: 2026-01-XX
updated: 2026-01-XX
author: compass-research
summary: Selects PM tool for Compass integration
tags: [pm, integration, decision]
related:
  - RF-05-01
  - DD-17-01
decision_date: null
deciders: []
supersedes: null
---
```

## Evidence Citation Format

Follow this format for all sources:
```
N. **[T#/S#]** Author. "Title". Published DATE. Retrieved DATE. URL
```

## Stop Conditions

Research is complete when:
- Integration patterns (A17) applied to evaluation
- At least two candidates evaluated for API completeness
- Artifact-to-PM-object mapping is drafted
- Phase 1 vs Phase 4 scope is clear

---

**Begin the research. Produce the Research Findings document and the ADR.**
