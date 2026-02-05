---
id: RF-04-01-LLM
type: rf
area: 04-documentation
title: Documentation Platform Research Findings (LLM View)
created: 2026-02-03
updated: 2026-02-03
summary: LLM-optimized view of documentation platform research findings
tags: [documentation, obsidian, gitbook, mcp, research, llm, view]
view: llm
source_id: RF-04-01
source_updated: 2026-01-26
staleness: fresh
---

# Documentation Platform Research Findings (LLM View)

## LLM Summary
This research evaluates documentation platforms against Compass requirements for YAML frontmatter, Git workflows, backlinks, and LLM retrieval. The primary recommendation is Obsidian with Git due to perfect frontmatter preservation, native wiki-links and backlinks, built-in graph visualization, and a mature MCP server ecosystem, all at zero cost. GitBook is identified as a strong alternative when collaboration UI and auto llms.txt generation are prioritized, but it carries frontmatter risk in its web editor. VS Code with Foam also meets requirements but is more developer-oriented. Mintlify is rejected due to cost, and Notion or Outline are rejected due to weak frontmatter and Git compatibility. The landscape is influenced by MCP adoption, which makes native access a core criterion rather than a bonus. These findings inform ADR-04-01.

## Canonical Statements
- Obsidian with Git best satisfies Compass documentation requirements.
- YAML frontmatter preservation is a hard requirement.
- MCP support is a key selection criterion.
- Real-time collaboration is secondary to structure fidelity.

## Scope and Non-Goals
- In scope: Documentation platform evaluation.
- Out of scope: Tooling for code execution or deployment.

## Dependencies and Interfaces
- Repository structure: `DD-12-01`.
- Artifact schema: `DD-13-01`.
- Decision output: `ADR-04-01`.

## Findings
- Obsidian provides the best balance of frontmatter fidelity, backlinks, and MCP access.
- GitBook excels at collaboration but risks frontmatter loss when edited in-app.
- Mintlify fails cost constraints; Notion and Outline fail frontmatter and Git needs.

## Evidence Quality
- Platform documentation: T1/S1 (official sources)
- Feature comparisons: T2/S2 (based on documentation review)
- Collaboration assessments: T3/S3 (not independently verified)

## Limitations
- Real-time collaboration claims not independently verified.
- Mobile sync performance claims not tested.

## Recommendation
- Recommend Obsidian with Git; GitBook is the secondary alternative.
- Evidence rating: S/I not explicitly rated in source; Confidence = high.
