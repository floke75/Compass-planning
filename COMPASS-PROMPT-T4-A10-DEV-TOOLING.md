# Research Phase: Development Tooling

**Area**: 10 | **Tier**: 4 (Integration & Handoff) | **Track**: A (External Research)

---

## Instructions

Copy everything below this line and paste it into a new Claude chat. Ensure the Compass System Definition is available as project context.

**Recommended**: Use Claude's deep research capability for this phase.

---

## Pre-Research Setup

### Mandatory Context (Must Be Available)
- **Compass System Definition** (`Compass___System_Definition.md`) — Read Part 4.2 (Team Capacity), Part 1.7 (Guiding Principles)
- **COMPASS-00-REFERENCE-INDEX.md** — Check for completed prior research

### Required Prior Research (Must Be Available)
- `RF-01-01-backend-findings.md` — Backend platform capabilities
- `ADR-01-01-backend-selection.md` — Selected backend platform

### Optional Context (Use If Available)
- `RF-08-01-hosting-findings.md` — Hosting approach
- `ADR-08-01-hosting-selection.md` — Deployment pipeline context
- `DD-17-01-integration-patterns.md` — Secret management requirements

---

## Important Instructions

1. **Read the Compass System Definition first**, particularly:
   - Part 4.2: Team Capacity (non-traditional dev team, LLM maintainability)
   - Part 1.7: Guiding Principles (debuggability, explicit error handling)
   - Part 3.8: Reliability and Recovery (testing requirements)

2. **Backend selection is required context** — Extract from ADR-01-01:
   - Selected backend platform (Supabase, Convex, etc.)
   - TypeScript support details
   - Testing considerations

3. **Do not ask the user technical questions** — research and recommend tooling optimized for LLM-assisted development.

4. **Prioritize LLM maintainability** — Common patterns, excellent docs, simple debugging over clever solutions.

---

## Available Context (If Present)

### From RF-01-01/ADR-01-01 (Backend) — Required:
- Selected backend platform
- TypeScript support quality
- Available client libraries
- Testing approaches mentioned

### From ADR-08-01 (Hosting) — If Available:
- Hosting platform
- Deployment pipeline approach
- Preview deployment support

### If ADR-08-01 Is Not Available:
Assume:
- GitHub-based workflow
- CI/CD via GitHub Actions
- Preview deployments desirable

### From DD-17-01 (Integration Patterns) — If Available:
- Secret management requirements
- Environment configuration approach

---

# RESEARCH TASK: Evaluate and Select Development Tooling

## Context

You are researching development tooling for **Compass**, an LLM-orchestrated planning, research, and documentation system for EFN (a financial news broadcaster with ~120 people).

This is a **Track A (External Research)** task. You are evaluating development tools against LLM maintainability and team capacity requirements.

**Why This Matters**: Development tooling affects how effectively LLM coding agents (like Claude Code) can work with the codebase. Simple, well-documented patterns enable better AI-assisted development.

## Scope

### Questions to Answer

1. **Testing Framework**: What testing approach works best?
   - Unit testing (core logic)
   - Integration testing (backend interaction)
   - E2E testing (if needed)

2. **CI/CD**: What minimizes operational burden?
   - Build pipeline configuration
   - Test automation
   - Deployment triggers

3. **Linting/Formatting**: What enforces consistency?
   - Code style
   - Type checking
   - Error prevention

4. **Environment Configuration**: How are environments managed?
   - Local development
   - Preview environments
   - Production

### Out of Scope
- Backend selection (Area 01 — use ADR-01-01)
- Hosting selection (Area 08 — use ADR-08-01)
- Integration patterns (Area 17 — reference DD-17-01)

## Evaluation Criteria

### Required Capabilities

| Capability | Requirement |
|------------|-------------|
| LLM maintainability | Common patterns, excellent documentation |
| Backend integration | Works with selected backend |
| TypeScript | First-class TypeScript support |
| Test coverage | Unit and integration at minimum |
| CI/CD simplicity | Low maintenance, clear configuration |

### LLM Maintainability Focus (Per System Definition 4.2)

Prioritize:
- Common stacks over exotic choices
- Strong documentation
- Simple patterns over clever solutions
- Explicit error handling
- Clear logs and observable workflows

## Candidates to Investigate

### Testing
1. **Vitest**
   - Modern, fast, excellent TypeScript
   - Jest-compatible API
   - Investigate: backend integration, mocking

2. **Playwright** (for E2E if needed)
   - Browser automation
   - Investigate: complexity vs value

### CI/CD
1. **GitHub Actions**
   - Ubiquitous, well-documented
   - Investigate: workflow patterns for stack

2. **Platform CI** (Vercel/Netlify if using)
   - Built-in deployment triggers
   - Investigate: testing integration

### Linting/Formatting
1. **Biome**
   - Fast, all-in-one
   - Investigate: TypeScript support, rule coverage

2. **ESLint + Prettier**
   - Industry standard
   - Investigate: configuration complexity

## Required Outputs

### 1. Research Findings Document (RF-10-01)

**Output File**: `RF-10-01-dev-tooling-findings.md`

**Frontmatter Schema**:
```yaml
---
id: RF-10-01
type: rf
area: 10-dev-tooling
title: Development Tooling Research Findings
status: draft
created: 2026-01-XX
updated: 2026-01-XX
author: compass-research
summary: Evaluates development tooling for Compass
tags: [dev-tooling, testing, ci-cd, linting, typescript]
related:
  - ADR-01-01
  - ADR-08-01
  - DD-17-01
confidence: high
methodology: "Tool evaluation with LLM maintainability focus"
limitations:
  - "Tooling preferences are somewhat subjective"
  - "Ecosystem evolves rapidly"
responds_to: null
implications_for: [development-workflow]
---
```

**Required Sections**:
1. **Executive Summary** — Recommended toolchain, confidence, trade-offs
2. **Testing Strategy** — Framework, test categories, coverage expectations
3. **CI/CD Design** — Pipeline stages, environment strategy
4. **Linting/Formatting** — Tools, configuration approach, enforcement
5. **Environment Configuration** — Variables, secrets, local vs production
6. **LLM Maintainability Assessment** — How tooling supports AI development
7. **Recommendation** — Complete toolchain with rationale

### 2. Architecture Decision Record (ADR-10-01)

**Output File**: `ADR-10-01-dev-tooling-selection.md`

**Frontmatter Schema**:
```yaml
---
id: ADR-10-01
type: adr
area: 10-dev-tooling
title: Development Tooling Selection
status: proposed
created: 2026-01-XX
updated: 2026-01-XX
author: compass-research
summary: Selects development tooling for Compass
tags: [dev-tooling, decision]
related:
  - RF-10-01
  - ADR-01-01
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
- Testing strategy documented with framework selection
- CI/CD pipeline designed
- Linting/formatting tools selected
- Backend/hosting compatibility confirmed
- LLM maintainability assessed

---

**Begin the research. Reference backend and hosting selections. Produce the Research Findings document and the ADR.**
