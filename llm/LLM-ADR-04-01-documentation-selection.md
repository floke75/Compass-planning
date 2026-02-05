---
id: ADR-04-01-LLM
type: adr
area: 04-documentation
title: Documentation Platform Selection (LLM View)
created: 2026-02-03
updated: 2026-02-03
summary: LLM-optimized view of the documentation platform selection decision
tags: [documentation, obsidian, git, decision, llm, view]
links:
  - rel: related
    target_id: "RF-04-01"
  - rel: related
    target_id: "DD-12-01"
  - rel: related
    target_id: "DD-13-01"
view: llm
source_id: ADR-04-01
source_updated: 2026-02-03
staleness: fresh
---

# Documentation Platform Selection (LLM View)

## LLM Summary
This ADR proposes Obsidian with Git as the documentation platform for Compass. The decision prioritizes perfect YAML frontmatter preservation, wiki-links and backlinks, graph visualization, and mature MCP server support, all while keeping zero vendor lock-in and zero core cost. The platform must support DD-12 repository structure, DD-13 frontmatter requirements, GitHub Flow, and LLM retrieval through MCP. Alternatives considered include GitBook (strong collaboration and auto llms.txt but weaker frontmatter handling), VS Code + Foam (good Git integration but more developer-oriented), Mintlify (AI-native but too expensive), and plain GitHub editing (insufficient navigation). The trade-offs accepted are lack of real-time co-editing and reliance on Git for collaboration. Consequences include strong local-first durability, straightforward LLM access, and the need for manual llms.txt generation and sync discipline.

## Canonical Statements
- Compass SHOULD use Obsidian with Git for documentation workflows.
- Documentation MUST preserve full YAML frontmatter without loss.
- Wiki-links and backlinks MUST be supported for artifact navigation.
- MCP access MUST be available for LLM retrieval.

## Scope and Non-Goals
- In scope: Documentation authoring and navigation platform selection.
- Out of scope: Orchestration, backend, or hosting decisions.

## Dependencies and Interfaces
- Research evidence: `RF-04-01`.
- Repository structure: `DD-12-01`.
- Artifact taxonomy and frontmatter: `DD-13-01`.

## Core Invariants
- YAML frontmatter must be preserved without loss.
- Wiki-links and backlinks are required for navigation.
- MCP access is mandatory for LLM retrieval.

## Open Questions
- Final stakeholder approval and decision date remain pending.

## Decision
- Use Obsidian with Git as the documentation platform.

## Drivers
- Perfect frontmatter preservation and local-first markdown.
- Native backlinks and graph visualization.
- Mature MCP server ecosystem.

## Alternatives and Disposition
- GitBook: Rejected due to frontmatter risk and vendor layer.
- VS Code + Foam: Rejected due to developer-focused UX.
- Mintlify: Rejected due to cost.
- Plain GitHub: Rejected due to weak navigation.

## Consequences
- Positive: Strong structure fidelity, LLM access, zero lock-in.
- Negative: No real-time co-editing, manual llms.txt, sync discipline required.
