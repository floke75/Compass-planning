# Agent Instructions for Compass Documentation

## Purpose
This repository contains the canonical planning, research, and decision artifacts for Compass. Canonical documents are the source of truth. LLM views are derived for retrieval and must not introduce new decisions or requirements.

## Document Hierarchy
1. System Definition (`SYS-*`) is authoritative for system intent and requirements.
2. Definitions (`DD-*`) define concepts, schemas, and taxonomy.
3. Standards (`STD-*`) are mandatory enforcement rules.
4. ADRs (`ADR-*`) record decisions and rationale.
5. Research Findings (`RF-*`) are evidence, not decisions.
6. Indexes (`IDX-*`) provide navigation.

## LLM Views
- LLM views live in `llm/` and are derived from canonical docs.
- LLM view frontmatter must include `view: llm`, `source_id`, `source_updated`, and `staleness`.
- Required sections (in order):
  - LLM Summary
  - Canonical Statements
  - Scope and Non-Goals
  - Dependencies and Interfaces
  - Evidence and Freshness
  - Open Questions
  - Change Log
- LLM Summary must be 120-180 words.
- Never add decisions or requirements to LLM views.
- See `llm/LLM-INDEX.md` for the full list of available LLM views.

### Key LLM Views by Domain
- **Reliability & Observability**: `llm/LLM-DD-16-01-reliability-tiers.md` (tier definitions, requirements matrix, Compass target), `llm/LLM-STD-16-01-reliability-standard.md` (checklists, logging schema, alerts, health checks, incident response)
- **Execution Integration**: `llm/LLM-RF-21-01-claude-code-cli-integration-findings.md` (Claude Code CLI integration patterns, Agent SDK, MCP bridge, cost model)
- **System Definition**: `llm/LLM-SYS-00-system-definition.md`
- **Ecosystem & Archetypes**: `llm/LLM-DD-14-01-ecosystem-definitions.md`
- **Planning Arc**: `llm/LLM-DD-18-01-questioning-arc.md`
- **Widget Schema**: `llm/LLM-DD-19-01-widget-schema.md`

## Structured Cross-Links
- Use frontmatter `links` for typed relationships.
- `links` is an array of objects with `rel` and `target_id`.
- Allowed `rel` values:
  - related
  - companion
  - responds_to
  - implications_for
  - informed_by
  - supersedes
  - superseded_by
  - implements
  - depends_on
  - blocks
  - references
  - contradicts
  - duplicates
- Keep legacy `related` and other link fields for compatibility.

## Update Workflow
When a canonical doc changes:
1. Update canonical doc and bump `updated` date.
2. Run `python3 scripts/validate_docs.py`.
3. Update the LLM view:
   - Refresh LLM Summary and affected sections.
   - Set `source_updated` to the canonical `updated` date.
   - Set LLM view `updated` to today.
   - Set `staleness` based on mismatch window.
   - Copy `links` from the canonical doc.
4. Update `llm/LLM-INDEX.md` if a new artifact appears or status changes.

## Staleness Rules
- `fresh`: `source_updated == canonical.updated`
- `review`: mismatch is 1-30 days
- `stale`: mismatch is more than 30 days

## Validation
- Run `python3 scripts/validate_docs.py` before finalizing changes.
- Errors indicate schema issues; warnings indicate stale LLM views.
- CI runs the same script and does not fail builds on staleness warnings.

## Running Scripts
- Use `python3` for all scripts in `scripts/`.
- Primary command: `python3 scripts/validate_docs.py`
- Strict mode (fail on errors): `python3 scripts/validate_docs.py --strict`
- CI uses the non-strict command by default.

## Guardrails
- Do not delete or overwrite ADRs. Create a superseding ADR instead.
- Do not change standards without explicit approval.
- If ambiguity exists, check related ADRs and standards before guessing.
