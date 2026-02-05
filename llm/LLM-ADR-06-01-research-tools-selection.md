---
id: ADR-06-01-LLM
type: adr
area: 06-research-tools
title: Research Tools Selection (LLM View)
created: 2026-02-03
updated: 2026-02-03
summary: LLM-optimized view of the research tool stack decision
tags: [research-tools, context7, firecrawl, tavily, decision, llm, view]
links:
  - rel: related
    target_id: "RF-06-01"
  - rel: related
    target_id: "DD-20-01"
  - rel: related
    target_id: "STD-20-01"
  - rel: related
    target_id: "ADR-04-01"
view: llm
source_id: ADR-06-01
source_updated: 2026-02-03
staleness: fresh
---

# Research Tools Selection (LLM View)

## LLM Summary
This ADR proposes a three-tool research stack for Compass evidence collection: Context7 for version-specific library docs, Firecrawl for general web and PDF extraction with JavaScript rendering, and Tavily for discovery-oriented search with citations. The stack aligns with DD-20/STD-20 evidence requirements and keeps initial budget constraints low while preserving coverage breadth. The decision favors tool specialization over a single do-it-all platform, accepting the need for a transformation layer to produce full citation metadata. Alternatives such as Firecrawl plus Exa, Perplexity plus Firecrawl, Browserbase-only, or Jina Reader-only were rejected due to missing version-specific coverage, higher cost, or lack of discovery. The trade-offs are additional configuration and ongoing MCP server maintenance versus higher quality, version-aware evidence. Consequences include a clear routing strategy for different research tasks and a required evidence transformation pipeline.

## Canonical Statements
- Compass SHOULD use Context7, Firecrawl, and Tavily as the primary research stack.
- Evidence outputs MUST be transformed to meet DD-20/STD-20 citation fields.
- Tool selection MUST fit budget constraints across growth stages.

## Scope and Non-Goals
- In scope: Research tool selection for evidence collection.
- Out of scope: Implementation details of the evidence transformation pipeline.

## Dependencies and Interfaces
- Research evidence: `RF-06-01`.
- Evidence standards: `DD-20-01`, `STD-20-01`.
- Documentation platform context: `ADR-04-01`.

## Core Invariants
- Evidence outputs must transform to DD-20/STD-20 citation format.
- Tool selection must fit budget constraints.
- Version-specific documentation coverage is required.

## Decision
- Use Context7 + Firecrawl + Tavily as the research tool stack.

## Drivers
- Version-specific documentation coverage.
- High-quality extraction for web and PDF content.
- MCP availability and budget alignment.

## Alternatives and Disposition
- Firecrawl + Exa: Rejected due to cost and missing version-aware docs.
- Perplexity + Firecrawl: Rejected due to pricing and limited control.
- Browserbase-only: Rejected as overkill.
- Jina Reader-only: Rejected due to lack of discovery.

## Consequences
- Positive: Broad coverage with strong MCP support and low initial cost.
- Negative: Multi-tool configuration and transformation layer required.
