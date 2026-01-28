# Research Phase: Reliability Tiers and Operational Standards

**Area**: 16 | **Tier**: 4 (Integration & Handoff) | **Track**: B (Internal Design)

---

## Instructions

Copy everything below this line and paste it into a new Claude chat. Ensure the Compass System Definition is available as project context.

---

## Pre-Research Setup

### Mandatory Context (Must Be Available)
- **Compass System Definition** (`Compass___System_Definition.md`) — Read Part 3.8 (Reliability and Recovery), Part 4.2 (Team Capacity), and Part 1.1 (The Core Problem)
- **COMPASS-00-REFERENCE-INDEX.md** — Check for completed prior research

### Required Prior Research (Include If Available)
- `DD-14-01-ecosystem-definitions.md` — EFN tool archetypes (maps to reliability tiers)
- `STD-14-01-ecosystem-standards.md` — Per-archetype requirements informing tier definitions

### Optional Context (Use If Available)
- `DD-17-01-integration-patterns.md` — Error handling and degradation patterns
- `ADR-01-01-backend-selection.md` — Backend SLA and reliability characteristics

---

## Important Instructions

1. **Read the Compass System Definition first**, particularly:
   - Part 3.8: Reliability and Recovery (failure handling, degradation)
   - Part 4.2: Team Capacity (operational simplicity, debuggability)
   - Part 1.1: The Core Problem (broadcast-critical vs internal tools)
   - Part 1.7: Guiding principles (reliable under partial failure)

2. **Do not ask the user technical questions** — derive reliability requirements from System Definition and EFN ecosystem context.

3. **If DD-14-01 exists**, ensure archetype-to-tier mapping is consistent with defined archetypes.

4. **Focus on practical operational requirements** suitable for a non-traditional development team.

---

## Available Context (If Present)

### From DD-14-01 (EFN Ecosystem) — Extract If Available:
- Project archetype definitions (Broadcast-Critical, Production Pipeline, etc.)
- Per-archetype reliability requirements
- Privacy and data handling profiles

### From STD-14-01 (Compliance Checklists) — Extract If Available:
- Per-archetype compliance requirements
- Observability standards
- Documentation requirements

### If DD-14-01 Not Available:
Use the archetype hints from System Definition:
- EFN tools span: broadcast-critical (live), business-critical (production), internal utilities
- Different reliability requirements implied by use case
- Planning work is high-value (losing work is unacceptable)

---

# RESEARCH TASK: Define Reliability Tiers and Operational Standards

## Context

You are helping define reliability tiers for **Compass** and the EFN tool ecosystem. EFN is a financial news broadcaster with ~120 people that builds internal tools ranging from broadcast-critical systems to simple admin utilities.

This is a **Track B (Internal Design)** task. You are defining internal standards based on requirements, not evaluating external tools.

**Key Insight from System Definition**: "Broadcast-critical tools have different requirements than internal admin tools. Clear tiers prevent over-engineering simple tools and under-engineering critical ones."

## Scope

### What This Definition Must Cover

1. **Reliability Tier Definitions**: What tiers exist? What characterizes each?
2. **Per-Tier Requirements**: Safeguards, observability, backup, incident response
3. **Tier Assignment Criteria**: How to decide which tier a tool belongs to
4. **Compass's Own Tier**: What reliability tier should Compass target?
5. **Archetype-to-Tier Mapping**: How project archetypes map to reliability tiers

### Out of Scope
- EFN ecosystem archetype details (Area 14 — reference existing)
- Integration patterns (Area 17 — reference existing)
- Specific monitoring tool selection
- Incident management tool selection

## Reliability Context from System Definition

### From Part 3.8 (Reliability and Recovery):
- Planning work is high-value; losing work is unacceptable
- Conversation state saves continuously
- Documents auto-save with conflict detection
- Failed operations retry automatically where safe
- Manual recovery procedures exist for edge cases
- System degrades gracefully when external services unavailable

### From Part 4.2 (Team Capacity):
- Non-traditional dev team
- Operational simplicity essential
- Debuggability matters

## Required Outputs

### 1. Definition Document (DD-16-01)

**Output File**: `DD-16-01-reliability-tiers.md`

**Frontmatter Schema**:
```yaml
---
id: DD-16-01
type: dd
area: 16-reliability-tiers
title: Reliability Tiers and Operational Standards
status: draft
created: 2026-01-XX
updated: 2026-01-XX
author: compass-research
summary: Defines reliability tiers and per-tier operational requirements
tags: [reliability, operations, monitoring, tiers]
related:
  - DD-14-01
  - STD-14-01
  - DD-17-01
---
```

**Required Sections**:

1. **Reliability Tier Catalog**
   Define 4 tiers (suggested):
   
   | Tier | Name | Impact of Failure | Availability Target | Recovery Time |
   |------|------|-------------------|---------------------|---------------|
   | 1 | Broadcast-Critical | Visible to audience | 99.9% during broadcast | < 30 seconds |
   | 2 | Business-Critical | Significantly impacts operations | 99% | < 1 hour |
   | 3 | Business-Important | Causes inconvenience | 95% | < 4 hours |
   | 4 | Internal Utility | Minimal impact | 90% | < 24 hours |

2. **Per-Tier Requirements Matrix**
   For each tier, specify:
   - **Safeguards**: Redundancy, failover, testing, deployment practices
   - **Observability**: Logging, metrics, tracing, alerting
   - **Backup and Restore**: Frequency, retention, testing
   - **Incident Response**: Response time, escalation, communication

3. **Tier Assignment Criteria**
   - Decision framework with questions
   - Factors to consider
   - Override conditions
   - Re-evaluation triggers

4. **Compass Reliability Target**
   - Recommended tier for Compass itself
   - Rationale (planning work is high-value)
   - Specific requirements

5. **Archetype-to-Tier Mapping**
   If DD-14-01 archetypes available:
   - Broadcast-Critical archetype → Tier 1
   - Production Pipeline → Tier 2
   - Publishing Pipeline → Tier 2/3
   - Analytics & Intelligence → Tier 3
   - Internal Utility → Tier 4
   - Exploratory → No tier (best effort)

### 2. Standard Document (STD-16-01)

**Output File**: `STD-16-01-reliability-standard.md`

**Frontmatter Schema**:
```yaml
---
id: STD-16-01
type: std
area: 16-reliability-tiers
title: Reliability and Observability Standard
status: draft
created: 2026-01-XX
updated: 2026-01-XX
author: compass-research
summary: Enforceable observability and reliability requirements per tier
tags: [reliability, observability, logging, alerting, standard]
related:
  - DD-16-01
  - STD-14-01
companion: DD-16-01
enforcement: Pre-launch review and periodic audits
---
```

**Required Content**:
- Observability requirements in specification form
- Minimum logging fields per tier
- Alert severity definitions
- Health check endpoint requirements

## Evidence Citation Format

Follow this format for all sources (per STD-20-01 if available):
```
N. **[T#/S#]** Author. "Title". Published DATE. Retrieved DATE. URL
```

## Stop Conditions

Definition is complete when:
- Tiers are defined with clear assignment criteria
- Requirements per tier are documented
- Sample tools are classified into tiers
- Compass's own tier is specified
- Archetype-to-tier mapping is complete (if DD-14-01 available)

---

**Begin the research and produce the Definition Document and Standard.**
