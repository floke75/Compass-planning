---
id: RF-06-01-LLM
type: rf
area: 06-research-tools
title: Research Tools Research Findings (LLM View)
status: draft
created: 2026-02-03
updated: 2026-02-03
author: compass-research
summary: LLM-optimized view of research tool evaluation findings
tags: [research-tools, evidence, context, firecrawl, tavily, context7, llm, view]
related:
  - RF-06-01
  - ADR-06-01
  - DD-20-01
  - STD-20-01
view: llm
source_id: RF-06-01
source_updated: 2026-01-28
staleness: fresh
---

# Research Tools Research Findings (LLM View)

## LLM Summary
This research evaluates tools for evidence collection in Compass and recommends a three-tool stack: Context7 for version-specific library docs, Firecrawl for robust web and PDF extraction with JavaScript rendering, and Tavily for discovery-oriented search with citations. The selection balances coverage breadth, MCP availability, and budget constraints, while acknowledging that no single tool provides all DD-20 citation fields. Exa is positioned as a precision add-on, Jina Reader as a low-cost extractor, and Browserbase as a last-resort for authenticated content. The trade-off is increased configuration and the need for a transformation layer to normalize outputs into Compass evidence artifacts. Costs are within Phase 1 and Phase 3 budgets, and the MCP ecosystem maturity makes these tools viable for LLM-driven workflows. These findings inform ADR-06-01 and the Pristine Context Layer design.

## Canonical Statements
- Context7, Firecrawl, and Tavily are the primary recommended tools.
- A transformation layer is required to meet DD-20/STD-20 citation fields.
- Tool routing should be based on content type and coverage gaps.

## Scope and Non-Goals
- In scope: Research tool evaluation for evidence gathering.
- Out of scope: Implementation details of the transformation pipeline.

## Dependencies and Interfaces
- Evidence standards: `DD-20-01`, `STD-20-01`.
- Decision output: `ADR-06-01`.

## Evidence and Freshness
- Source updated 2026-01-28; staleness marked fresh.
- Pricing and rate limits may change; MCP ecosystem is evolving.

## Open Questions
- None.

## Change Log
- 2026-02-03: LLM view created from `RF-06-01` with no semantic changes.

## Findings
- Context7 provides best-in-class version-specific documentation coverage.
- Firecrawl excels at JS rendering and PDF extraction.
- Tavily provides discovery with citations but limited depth.

## Limitations
- Vendor pricing and rate limits are subject to change.
- Coverage varies by library popularity.

## Recommendation
- Recommend Context7 + Firecrawl + Tavily as the primary research stack.
- Evidence rating: S/I not explicitly rated in source; Confidence = high.
