---
id: RF-21-01-LLM
type: research-findings
area: 21-execution-integration
title: Claude Code CLI Integration Research Findings (LLM View)
created: 2026-02-05
updated: 2026-02-05
summary: LLM-optimized view of integration patterns for Compass Planning with Claude Code CLI, recommending a hybrid architecture using handoff bundles, Agent SDK, and MCP bridge
tags: [claude-code, cli, desktop, integration, agent-sdk, mcp, local-execution, llm, view]
links:
  - rel: related
    target_id: "SYS-00"
  - rel: related
    target_id: "DD-11-01"
  - rel: related
    target_id: "DD-17-01"
  - rel: related
    target_id: "ADR-02-01"
  - rel: related
    target_id: "RF-02-01"
view: llm
source_id: RF-21-01
source_updated: 2026-02-05
staleness: fresh
---

# Claude Code CLI Integration Research Findings (LLM View)

## LLM Summary
RF-21 evaluates how Compass Planning integrates with Claude Code CLI for local desktop execution. The research recommends a hybrid architecture where Compass serves as the specification and orchestration layer while Claude Code handles local execution. Three complementary integration mechanisms are identified: handoff bundle export (primary), Claude Agent SDK for programmatic control, and MCP server bridge for bidirectional communication. The key insight is that Compass's strength (converting vague intent to rigorous specs) is orthogonal to Claude Code's strength (autonomous local execution), forming a natural pipeline. The hybrid cost model separates planning (API-based, Compass) from execution (subscription-based, Claude Code CLI), reducing costs significantly for medium-to-heavy usage.

## Canonical Statements
- Compass SHOULD serve as the specification and orchestration layer; Claude Code CLI SHOULD handle local execution.
- Handoff bundle export (Pattern A) SHOULD be the primary integration mechanism due to simplicity and robustness.
- Handoff bundles MUST follow the `DD-11-01` schema.
- The Claude Agent SDK (Python `claude-code-sdk` or TypeScript `@anthropic-ai/claude-code`) SHOULD be used for programmatic Claude Code control in automated workflows.
- MCP server bridge SHOULD enable bidirectional communication between Claude Code sessions and Compass state.
- Claude Code tool restrictions SHOULD use `--allowedTools` for automated execution to prevent destructive commands.
- `SYS-00` SHOULD be updated to add a Layer 7b for local execution platforms.
- `DD-11-01` SHOULD be extended with Claude Code-specific sections (system prompt additions, allowed tools, MCP config, session strategy, verification commands).
- `DD-17-01` SHOULD define a new `claude_code_cli` integration type (bidirectional, MCP over HTTP).

## Scope and Non-Goals
- In scope: CLI integration mechanisms (print mode, Agent SDK, MCP), architecture patterns, lessons from community tools, cost model, security considerations.
- Out of scope: Hands-on performance benchmarks; implementation of the integration; desktop app development.

## Dependencies
- System architecture: `SYS-00` (architecture layers, handoff model).
- Handoff bundle schema: `DD-11-01`.
- Integration patterns: `DD-17-01`.
- Orchestration framework: `ADR-02-01` (Mastra + AI SDK).
- Orchestration evaluation: `RF-02-01`.

## Core Invariants
- The specification is permanent; the implementation is ephemeral (per `SYS-00` §1.4).
- Compass plans, Claude Code executes—the pipeline is unidirectional for specification, bidirectional for progress/reconciliation.
- No runtime dependency between Compass and Claude Code is required for the primary pattern (handoff bundles).
- Implementation discoveries MUST be folded back into Compass specifications via reconciliation.

## Findings
- **Natural pipeline**: Compass's value proposition (converting vague intent to rigorous specs) is orthogonal to Claude Code's strength (autonomous local execution). They complement rather than compete.
- **Cost advantage**: Hybrid model (planning via API + execution via subscription) reduces costs from ~$112.50/month to ~$7.50/month API cost at medium usage (covered by $100–200/month flat subscription).
- **Community validation**: GSD, Auto-Claude, claude-code-webui, and Opcode all validate the pattern of rich planning/orchestration + CLI execution.
- **Three integration patterns** identified, each suitable for different automation levels:
  - Pattern A (Handoff Bundle Export): simplest, no runtime dependency, works offline.
  - Pattern B (SDK-Driven Orchestration): full automation with real-time progress streaming.
  - Pattern C (Hybrid Desktop App): Tauri 2 desktop app with multi-agent management, offline support, cost tracking.
- **Claude-Flow excluded** from analysis due to credibility concerns (suspected artificial engagement, limited verified adoption).

## Evidence Quality

| Claim | Source Tier | Confidence |
|---|---|---|
| Agent SDK capabilities | T1 (official Anthropic docs) | High |
| MCP integration patterns | T1 (official Anthropic docs) | High |
| Print mode flags and behavior | T1 (official Anthropic docs) | High |
| GSD phase-based workflow | T2 (GitHub repository) | High |
| Auto-Claude multi-agent pattern | T2 (GitHub repository) | Medium-High |
| Cost projections | T1 (API pricing) + estimates | Medium |
| Desktop app technology choices | T3 (general analysis) | Medium |

## Limitations
- No hands-on performance benchmarking conducted.
- Claude Code CLI features evolve rapidly; some capabilities may have changed.
- Cost analysis based on API pricing; actual usage varies significantly by workflow.
- Community tools (GSD, Auto-Claude) are third-party and may have stability issues.

## Recommendation
Implement a three-phase approach:

1. **Handoff Bundle Integration**: Enhanced HANDOFF-* template for Claude Code consumption, export formats (markdown, Git push, clipboard), CLAUDE.md generator, reconciliation import wizard. No additional infrastructure required.
2. **MCP Bridge**: Compass MCP server with spec query and progress reporting, API key auth, real-time progress dashboard, clarification request workflow. Minimal infrastructure (edge function invocations).
3. **Desktop Orchestrator**: Tauri 2 desktop app with multi-agent management, Git worktree automation, cost tracking, offline mode. Recommended stack: Tauri 2 (Rust backend), React frontend, Convex client for sync, Agent SDK (TypeScript), SQLite for local storage.

## Integration Mechanisms

### Print Mode (`-p`)
Key flags: `-p` (non-interactive), `--output-format json|stream-json`, `--allowedTools` (auto-approve), `--append-system-prompt` (inject specs), `--resume <session_id>` (continue session), `--json-schema` (enforce output schema).

### Agent SDK
- Python: `claude-code-sdk` on PyPI; TypeScript: `@anthropic-ai/claude-code` on NPM.
- Key capabilities: `query()` for one-off execution, `ClaudeSDKClient` for multi-turn, `hooks` for pre/post tool validation, `mcp_servers` for in-process MCP tools, `cwd` for project isolation.

### MCP Server Bridge
Compass exposes MCP tools to Claude Code: `get_spec` (query planning state), `report_progress` (update task status), `request_clarification` (async human notification), `record_decision` (capture implementation decisions).

## Lessons from Community Tools

| Tool | Key Pattern for Compass |
|---|---|
| **GSD** | Phase-based planning prevents context rot; maps to Compass questioning arc |
| **Auto-Claude** | Spec-driven pipeline (planner → coder → QA reviewer → fixer); Git worktree isolation for parallel agents |
| **claude-code-webui** | Session management and stream-JSON progress visualization |
| **Opcode** | Tauri desktop wrapper with usage/cost tracking |

## Cost Model

| Scenario | API-Only | Hybrid (Compass + Subscription) |
|---|---|---|
| Light (2M tokens/mo) | $30/mo | $107.50/mo |
| Medium (10M tokens/mo) | $150/mo | $107.50/mo |
| Heavy (50M tokens/mo) | $750/mo | $107.50/mo |
| Team (3 devs, 100M tokens/mo) | $1,500/mo | $307.50/mo |

Break-even: ~7M tokens/month for single user.

## Security Considerations
- **Auth layers**: Compass→User (Convex Auth), Claude Code→Anthropic (OAuth/API key), Claude Code→Compass MCP (per-user rotatable API key).
- **Handoff bundles**: may contain proprietary details; encrypt at rest, no third-party hosting, optional local-only mode.
- **MCP communication**: HTTPS only, references only in responses (no sensitive data).
- **Execution safety**: use restrictive `--allowedTools` for automated execution; use SDK hooks to block destructive commands (`rm -rf`, `drop table`).

## Open Questions
- Reconciliation granularity: track every file change or summary deltas?
- Branching during execution: how does Claude Code signal back to Compass for re-planning?
- Multi-user coordination: how do parallel implementations from different users merge?
- Offline conflict resolution: what happens when offline changes conflict with cloud state?
- Performance benchmarking: MCP round-trip latency under load needs measurement.
- Token-efficient handoff bundle formats need investigation.
- Tauri 2 vs Electron comparison for desktop app needs deeper evaluation.
