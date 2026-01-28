# Research Phase: Research Tools and Context Collection

**Area**: 06 | **Tier**: 4 (Integration & Handoff) | **Track**: A (External Research)

---

## Instructions

Copy everything below this line and paste it into a new Claude chat. Ensure the Compass System Definition is available as project context.

**Recommended**: Use Claude's deep research capability for this phase.

---

## Pre-Research Setup

### Mandatory Context (Must Be Available)
- **Compass System Definition** (`SYS-00-system-definition.md`) — Read Part 2.3 (Research Integration), Part 5.1 (The Layers — Pristine Context Layer)
- **IDX-00-MASTER.md** — Check for completed prior research

### Required Prior Research (Must Be Available)
- `DD-20-01-evidence-definitions.md` — Evidence grading and source qualification
- `STD-20-01-evidence-standards.md` — Citation format specification

### Optional Context (Use If Available)
- `ADR-04-01-documentation-selection.md` — Output format requirements
- `RF-04-01-documentation-findings.md` — Platform integration constraints

---

## Important Instructions

1. **Read the Compass System Definition first**, particularly:
   - Part 2.3: Research Integration (research types, branching, merge gates)
   - Part 5.1: Layer 5 — Pristine Context and Evidence Layer
   - Part 3.2: Memory layers (evidence storage)

2. **DD-20-01 and STD-20-01 are required** — These define evidence standards that tools must support. Extract:
   - Five-tier source taxonomy (T1-T5) from Part 2.1
   - Source reliability ratings (S1-S4) from Part 1.2
   - Required citation fields from Part 3.1
   - Freshness/staleness rules from Part 4

3. **Do not ask the user technical questions** — research and evaluate tools against evidence standards.

4. **Use deep research** to investigate current research tools, their source coverage, and output formats.

---

## Available Context (If Present)

### From DD-20-01/STD-20-01 (Evidence Standards) — Required:
- Five-tier source taxonomy (Part 2.1: T1 Authoritative → T5 Unverified)
- Source reliability ratings (Part 1.2: S1-S4)
- Information quality ratings (Part 1.3: I1-I4)
- Required citation fields (Part 3.1: id, source_url, title, source_type, retrieved_at)
- Freshness thresholds by content type (Part 4.2)
- Evidence artifact schema (Part 5.1)

### From ADR-04-01 (Documentation) — If Available:
- Selected documentation platform
- Document format requirements
- LLM retrieval approach

### If ADR-04-01 Is Not Available:
Assume:
- Markdown with YAML frontmatter is the target format
- Output must be LLM-retrievable
- Citation metadata must be structured

---

# RESEARCH TASK: Evaluate and Select Research Tools

## Context

You are researching tools for collecting and verifying external evidence for **Compass**, an LLM-orchestrated planning, research, and documentation system for EFN (a financial news broadcaster with ~120 people).

This is a **Track A (External Research)** task. You are evaluating research and context collection tools against evidence standards.

**Why This Matters**: Research quality depends on accessing current, authoritative sources. Implementation agents need verified context rather than hallucinated training data.

## Scope

### Questions to Answer

1. **Source Coverage**: What sources can each tool access?
   - Official documentation
   - Version-specific docs
   - Web pages (static and JS-rendered)
   - PDFs and documents
   - Internal repos

2. **Evidence Standards Support**: How well does each tool support DD-20-01?
   - Can it capture source URL, timestamp, and metadata?
   - Does it support quality grading?
   - Can outputs match citation format?

3. **Output Format**: What formats does each tool produce?
   - Markdown quality
   - Structured metadata
   - Compatibility with documentation platform

4. **Rate Limits and Pricing**: What are the constraints?
   - Rate limits per tool
   - Cost at Phase 1 and Phase 3 volume

### Out of Scope
- Evidence standards definition (Area 20 — use DD-20-01/STD-20-01)
- Documentation platform selection (Area 04)
- Memory system design (Area 03)

## Evaluation Criteria

### Required Capabilities

| Capability | Requirement |
|------------|-------------|
| Source coverage | Web pages, PDFs, JS-rendered, version-specific docs |
| Timestamp capture | Retrieved-at timestamp for staleness tracking |
| Metadata output | Structured citation metadata |
| Output format | Clean Markdown with frontmatter support |
| Rate limits | Workable for research volume |

### Evidence Standards Compatibility (Per DD-20-01)

Tools must support capturing:
- Source URL and identifier
- Access timestamp
- Source type (for tier assignment)
- Extracted content
- Reliability indicators

## Candidates to Investigate

1. **Context7**
   - Version-specific library documentation
   - Investigate: coverage, API access, pricing

2. **Firecrawl**
   - Web scraping with JS rendering
   - Investigate: rate limits, Markdown quality

3. **Tavily**
   - RAG-optimized search
   - Investigate: source quality, citation support

4. **Jina Reader**
   - URL to Markdown conversion
   - Investigate: JS rendering, PDF support

5. **Perplexity API**
   - Search with citations
   - Investigate: pricing, citation format

6. **Direct Vendor APIs** (supplementary)
   - GitHub API, npm/PyPI
   - Investigate: coverage, rate limits

## Required Outputs

### 1. Research Findings Document (RF-06-01)

**Output File**: `RF-06-01-research-tools-findings.md`

**Frontmatter Schema**:
```yaml
---
id: RF-06-01
type: rf
area: 06-research-tools
title: Research Tools Research Findings
status: draft
created: 2026-01-XX
updated: 2026-01-XX
author: compass-research
summary: Evaluates research and context collection tools for Compass
tags: [research-tools, evidence, context, web-scraping, documentation]
related:
  - DD-20-01
  - STD-20-01
  - ADR-04-01
confidence: high
methodology: "Documentation analysis with evidence standards mapping"
limitations:
  - "Rate limits may change"
  - "Pricing subject to updates"
responds_to: null
implications_for: [integration-pipeline]
---
```

**Required Sections**:
1. **Executive Summary** — Recommendation, confidence, key trade-offs
2. **Source Coverage Matrix** — Web, PDFs, JS, version-specific per tool
3. **Evidence Standards Fit** — How each tool supports DD-20-01
4. **Output Format Assessment** — Markdown quality, metadata structure
5. **Rate Limits and Pricing** — Phase 1 and Phase 3 cost estimates
6. **Ingestion Pipeline Sketch** — How tools combine for coverage
7. **Recommendation** — Primary tool(s) with rationale

### 2. Architecture Decision Record (ADR-06-01)

**Output File**: `ADR-06-01-research-tools-selection.md`

**Frontmatter Schema**:
```yaml
---
id: ADR-06-01
type: adr
area: 06-research-tools
title: Research Tools Selection
status: proposed
created: 2026-01-XX
updated: 2026-01-XX
author: compass-research
summary: Selects research tools for Compass context collection
tags: [research-tools, decision]
related:
  - RF-06-01
  - DD-20-01
decision_date: null
deciders: []
supersedes: null
---
```

## Evidence Citation Format

Follow DD-20-01/STD-20-01 format:
```
N. **[T#/S#]** Author. "Title". Published DATE. Retrieved DATE. URL
```

## Stop Conditions

Research is complete when:
- Evidence standards (DD-20-01) are mapped to tool capabilities
- At least 3 tools evaluated for source coverage
- Output format compatibility verified
- Rate limits and pricing documented
- Ingestion pipeline sketched

---

**Begin the research. Apply evidence standards from DD-20-01/STD-20-01. Produce the Research Findings document and the ADR.**
