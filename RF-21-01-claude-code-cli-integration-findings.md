---
id: RF-21-01
type: rf
area: 21-execution-integration
title: Claude Code CLI Integration Research Findings
status: draft
created: 2026-02-05
updated: 2026-02-05
author: compass-research
summary: Evaluates integration patterns for Compass Planning with Claude Code CLI for local desktop execution, analyzing tools like GSD, Auto-Claude, and Claude Agent SDK to recommend a hybrid architecture
tags: [claude-code, cli, desktop, integration, gsd, auto-claude, agent-sdk, mcp, local-execution]
related:
  - SYS-00
  - DD-11-01
  - DD-17-01
  - ADR-02-01
  - RF-02-01
confidence: high
methodology: "Web research with official Anthropic documentation, GitHub repositories, community tools (GSD, Auto-Claude, Claude-Flow), and SDK specifications"
limitations:
  - "No hands-on performance benchmarking conducted"
  - "Claude Code CLI features evolve rapidly; some capabilities may have changed"
  - "Cost analysis based on API pricing; actual usage varies significantly by workflow"
  - "Community tools (GSD, Auto-Claude) are third-party and may have stability issues"
responds_to: "How would Compass Planning integrate with Claude Code CLI for local desktop execution?"
implications_for: [SYS-00, DD-11-01, DD-17-01, ADR-02-01]
---

# Claude Code CLI Integration Research Findings

## Executive Summary

**Recommendation**: Implement a **hybrid architecture** where Compass Planning serves as the **specification and orchestration layer** while Claude Code CLI handles **local execution**. The integration uses three complementary approaches:

1. **Handoff Bundle Export** — Compass generates implementation-ready specifications that Claude Code consumes
2. **Claude Agent SDK** — Programmatic control of Claude Code from Compass backend for automated workflows
3. **MCP Server Bridge** — Bidirectional communication allowing Claude Code to query Compass state and report progress

**Confidence**: High — Patterns are well-documented in official Anthropic SDK and demonstrated by successful community tools (GSD, Auto-Claude, Claude-Flow).

**Key insight**: Compass's value proposition—converting vague intent into rigorous specifications—is orthogonal to Claude Code's strength—autonomous local execution. Rather than competing, they form a natural pipeline: Compass plans, Claude Code executes.

**Cost advantage**: By using Claude Code CLI with the user's existing Claude subscription (OAuth authentication), organizations avoid API costs for execution while Compass handles the planning layer via API. This mirrors the model used by GSD and Auto-Claude.

---

## Part 1: Context and Problem Space

### 1.1 Research Question

How would the Compass Planning system integrate with Claude Code CLI for local desktop use cases, similar to tools like GSD (Get Shit Done) and Auto-Claude?

### 1.2 The Cost Problem

LLM API usage for software development is expensive. A typical coding session might consume:

| Activity | Tokens (approx) | Cost at Claude Opus |
|----------|-----------------|---------------------|
| Planning session (1 hour) | 100k-300k | $1.50-$4.50 |
| Implementation (8 hours) | 500k-2M | $7.50-$30.00 |
| Testing/debugging cycles | 200k-500k | $3.00-$7.50 |
| **Total per feature** | **800k-2.8M** | **$12-$42** |

For teams building multiple features, this quickly reaches hundreds of dollars per week.

**The emerging solution**: Separate planning (API-based, Compass) from execution (subscription-based, Claude Code CLI). Users pay $100-200/month for Claude Max subscription with generous limits, while planning happens on the more cost-efficient web layer.

### 1.3 Market Validation

Several tools have validated this pattern:

| Tool | Approach | Key Innovation |
|------|----------|----------------|
| **GSD (Get Shit Done)** | Planning layer atop Claude Code | Phase-based workflows prevent context rot |
| **Auto-Claude** | Multi-agent orchestration | Parallel execution across 12+ agent terminals |
| **Claude-Flow** | Swarm orchestration | 87 MCP tools for distributed coordination |
| **claude-code-webui** | Web frontend for CLI | Session management and visualization |
| **Opcode** | Tauri desktop app | GUI wrapper with usage tracking |

All these tools share a common pattern: **rich planning/orchestration interface + Claude Code CLI execution**.

### 1.4 Compass's Position in This Ecosystem

Per SYS-00 §1.4, Compass's core principle is: *"The specification is permanent; the implementation is ephemeral."*

This aligns perfectly with the CLI integration model:

```
┌─────────────────────────────────────────────────────────────────┐
│                    COMPASS PLANNING (Web/API)                    │
│  • Converts vague intent to rigorous specs                       │
│  • Questioning arc (OPEN→FOLLOW→SHARPEN→BOUNDARY→GROUND)        │
│  • Widget-driven structured input                                │
│  • Research integration (Context7, Firecrawl, Tavily)           │
│  • Decision tracking with rationale                              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼ Handoff Bundle (HANDOFF-*)
┌─────────────────────────────────────────────────────────────────┐
│                 CLAUDE CODE CLI (Local Desktop)                  │
│  • Autonomous code generation                                    │
│  • File system access                                            │
│  • Test execution                                                │
│  • Git operations                                                │
│  • Uses existing Claude subscription (no API costs)              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼ Implementation Deltas
┌─────────────────────────────────────────────────────────────────┐
│                   COMPASS RECONCILIATION                         │
│  • Fold implementation discoveries back into specs               │
│  • Update decision records                                       │
│  • Maintain specification as source of truth                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## Part 2: Claude Code CLI Integration Mechanisms

### 2.1 Print Mode (`-p` / `--print`)

Claude Code's print mode enables non-interactive, programmatic execution:

```bash
# Basic execution
claude -p "Implement the authentication module per the spec"

# With tool permissions
claude -p "Run tests and fix failures" --allowedTools "Bash,Read,Edit"

# With structured output
claude -p "Analyze this codebase" --output-format json

# With session continuation
session_id=$(claude -p "Start implementation" --output-format json | jq -r '.session_id')
claude -p "Continue with the API layer" --resume "$session_id"
```

**Key flags for integration**:

| Flag | Purpose | Compass Use Case |
|------|---------|------------------|
| `-p` / `--print` | Non-interactive mode | Automated task execution |
| `--output-format json` | Structured response | Parse results programmatically |
| `--output-format stream-json` | Real-time streaming | Progress monitoring |
| `--allowedTools` | Auto-approve tools | Unattended execution |
| `--append-system-prompt` | Add context | Inject Compass specifications |
| `--resume <session_id>` | Continue session | Multi-phase implementations |
| `--json-schema` | Enforce output schema | Structured progress reports |

### 2.2 Claude Agent SDK

Anthropic provides official SDKs for programmatic Claude Code control:

**Python SDK** (`claude-code-sdk` on PyPI):

```python
from claude_agent_sdk import query, ClaudeAgentOptions

options = ClaudeAgentOptions(
    system_prompt="You are implementing a Compass handoff bundle.",
    allowed_tools=["Read", "Write", "Edit", "Bash"],
    cwd="/path/to/project",
    mcp_servers={
        "compass": compass_mcp_server  # Bidirectional bridge
    }
)

async for message in query(
    prompt="Implement the authentication module per HANDOFF-AUTH-001",
    options=options
):
    # Stream progress to Compass UI
    await compass_client.report_progress(message)
```

**TypeScript SDK** (`@anthropic-ai/claude-code` on NPM):

```typescript
import { query, ClaudeAgentOptions } from '@anthropic-ai/claude-code';

const options: ClaudeAgentOptions = {
  systemPrompt: compassHandoffBundle.toSystemPrompt(),
  allowedTools: ['Read', 'Write', 'Edit', 'Bash'],
  cwd: projectPath,
  mcpServers: { compass: compassMcpServer }
};

for await (const message of query(prompt, options)) {
  await compassClient.reportProgress(message);
}
```

**Key SDK capabilities**:

| Feature | Description | Compass Integration |
|---------|-------------|---------------------|
| `query()` | One-off async execution | Simple task dispatch |
| `ClaudeSDKClient` | Multi-turn interactive | Complex implementations |
| `hooks` | Pre/post tool execution | Validation and approval |
| `mcp_servers` | In-process MCP tools | Bidirectional state sync |
| `ClaudeAgentOptions.cwd` | Working directory | Project isolation |

### 2.3 MCP Server Integration

The Model Context Protocol enables bidirectional communication between Compass and Claude Code:

**Compass MCP Server** (exposed to Claude Code):

```typescript
// In-process MCP server running within Compass
const compassMcpServer = createMcpServer({
  name: "compass-planning",
  tools: {
    // Query planning state
    "get_spec": async ({ specId }) => {
      return await compassDb.getSpec(specId);
    },

    // Report implementation progress
    "report_progress": async ({ taskId, status, notes }) => {
      await compassDb.updateTaskProgress(taskId, status, notes);
      return { success: true };
    },

    // Request clarification (triggers async notification)
    "request_clarification": async ({ question, context }) => {
      await compassDb.createClarificationRequest(question, context);
      return { requestId, message: "Question queued for human review" };
    },

    // Record implementation decision
    "record_decision": async ({ decisionType, choice, rationale }) => {
      await compassDb.recordImplementationDecision(decisionType, choice, rationale);
      return { success: true };
    }
  }
});
```

**Claude Code configuration** (`.mcp.json` in project):

```json
{
  "mcpServers": {
    "compass": {
      "type": "http",
      "url": "https://compass.example.com/mcp",
      "headers": {
        "Authorization": "Bearer ${COMPASS_API_KEY}"
      }
    }
  }
}
```

---

## Part 3: Integration Architecture Patterns

### 3.1 Pattern A: Handoff Bundle Export (Recommended Primary)

The simplest and most robust integration. Compass exports implementation-ready bundles that Claude Code consumes as context.

**Workflow**:

```
1. User completes planning in Compass (5-stage questioning arc)
2. Compass generates HANDOFF-* bundle (per DD-11-01 schema)
3. User downloads bundle or Compass pushes to Git repo
4. User opens project in Claude Code CLI
5. Claude Code reads HANDOFF-* as context and implements
6. On completion, user triggers reconciliation in Compass
```

**Handoff bundle structure** (per DD-11-01):

```markdown
# HANDOFF-AUTH-001: User Authentication Module

## Overview
- **Vision**: Secure, passwordless authentication for EFN tools
- **Success Metrics**: <100ms auth latency, 99.9% availability
- **Stakeholders**: Security team, all EFN users

## Requirements
### In Scope
- Magic link email authentication
- Session management with refresh tokens
- Rate limiting (100 attempts/hour/IP)

### Out of Scope
- Social OAuth providers (deferred to Phase 2)
- Biometric authentication

### Constraints
- Must use existing Convex backend
- No third-party auth services (cost constraint)

## Decision Ledger
| ID | Decision | Status | Rationale |
|----|----------|--------|-----------|
| D-001 | Use JWT for sessions | Accepted | Stateless, Convex-compatible |
| D-002 | Magic link over password | Accepted | Better UX, no password storage |
| D-003 | Social OAuth | Rejected | Cost exceeds budget |

## Architecture
[Component diagram, data flows, API contracts]

## Work Breakdown
1. [ ] Implement magic link generation endpoint
2. [ ] Create email template and sending logic
3. [ ] Build session validation middleware
4. [ ] Add rate limiting with Convex
5. [ ] Write integration tests

## Context Pack
[Relevant code snippets, API documentation, prior research]
```

**Advantages**:
- No runtime dependency between systems
- Works offline
- Maximum Claude Code autonomy
- Clear audit trail

**Disadvantages**:
- Manual reconciliation step
- No real-time progress visibility

### 3.2 Pattern B: SDK-Driven Orchestration

Compass backend spawns Claude Code sessions programmatically for automated workflows.

**Workflow**:

```
1. User completes planning in Compass
2. User clicks "Start Implementation" in Compass UI
3. Compass backend spawns Claude Code via Agent SDK
4. Claude Code executes with Compass specs injected as system prompt
5. Progress streams back to Compass UI in real-time
6. Compass automatically reconciles on completion
```

**Implementation sketch**:

```typescript
// Compass backend - implementation orchestrator
async function startImplementation(handoffId: string, projectPath: string) {
  const handoff = await db.getHandoff(handoffId);
  const tasks = handoff.workBreakdown;

  const options: ClaudeAgentOptions = {
    systemPrompt: generateSystemPrompt(handoff),
    allowedTools: ["Read", "Write", "Edit", "Bash(npm *)", "Bash(git *)"],
    cwd: projectPath,
    mcpServers: {
      compass: createCompassMcpServer(handoffId)
    }
  };

  for (const task of tasks) {
    const sessionId = await startSession(task, options);

    for await (const message of query(task.prompt, { ...options, resume: sessionId })) {
      // Stream to Compass UI
      await broadcastProgress(handoffId, task.id, message);

      // Record tool usage for audit
      if (message.type === 'tool_use') {
        await recordToolUsage(handoffId, task.id, message);
      }
    }

    // Mark task complete, trigger next
    await db.markTaskComplete(task.id);
  }

  // Trigger reconciliation
  await triggerReconciliation(handoffId);
}
```

**Advantages**:
- Full automation from planning to implementation
- Real-time progress visibility
- Automatic reconciliation

**Disadvantages**:
- Requires Claude Code installed on Compass server (or user's machine via desktop app)
- More complex deployment
- Potential for runaway costs if not monitored

### 3.3 Pattern C: Hybrid Desktop App

A desktop application that runs Claude Code locally while syncing with Compass cloud.

**Architecture**:

```
┌──────────────────────────────────────────────────────────────┐
│                    COMPASS WEB (Cloud)                        │
│  • Planning UI                                                │
│  • Specification storage (Convex)                             │
│  • Research integration                                       │
│  • Decision tracking                                          │
└──────────────────────────────────────────────────────────────┘
                    │                          ▲
                    │ Sync via WebSocket       │ Progress reports
                    ▼                          │
┌──────────────────────────────────────────────────────────────┐
│               COMPASS DESKTOP (Electron/Tauri)                │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Local State Sync                                       │  │
│  │ • Pull handoff bundles                                 │  │
│  │ • Push implementation deltas                           │  │
│  │ • Offline queue for intermittent connectivity          │  │
│  └────────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Claude Code Orchestrator                               │  │
│  │ • Spawn Claude Code sessions                           │  │
│  │ • Manage multiple parallel agents (like Auto-Claude)   │  │
│  │ • Progress visualization                               │  │
│  │ • Cost tracking                                        │  │
│  └────────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Claude Code CLI (subprocess)                           │  │
│  │ • Uses local Claude subscription (OAuth)               │  │
│  │ • Full filesystem access                               │  │
│  │ • Git operations                                       │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

**Key features**:

| Feature | Implementation | Reference Tool |
|---------|----------------|----------------|
| Multi-agent terminals | Git worktrees per agent | Auto-Claude |
| Phase-based execution | Task state machine | GSD |
| Progress visualization | Stream-JSON parsing | claude-code-webui |
| Cost tracking | Token counting | Opcode |
| Offline support | Local SQLite queue | — |

**Technology choices**:

| Component | Recommended | Rationale |
|-----------|-------------|-----------|
| Desktop framework | **Tauri 2** | Rust backend, small binary, secure IPC |
| State sync | **Convex client** | Matches Compass backend |
| Claude Code interface | **Agent SDK (TS)** | Official, well-maintained |
| Local storage | **SQLite** | Offline queue, session cache |

---

## Part 4: Lessons from Existing Tools

### 4.1 GSD (Get Shit Done)

**Key innovation**: Phase-based planning prevents "context rot" (accuracy degradation as context grows).

**Applicable to Compass**:
- GSD's phase model (Plan → Execute → Verify) maps to Compass's questioning arc
- Task registration with Claude's Task API provides native progress tracking
- Session isolation via `GSD_PROJECT` environment variable enables parallel work

**Pattern to adopt**:
```yaml
# GSD-style phase definition in Compass
phases:
  - id: phase-1
    name: "Core Authentication"
    objectives:
      - Implement magic link generation
      - Create session management
    deliverables:
      - auth/magic-link.ts
      - auth/session.ts
    success_criteria:
      - Unit tests pass
      - Manual flow verification
```

### 4.2 Auto-Claude

**Key innovation**: Parallel multi-agent execution with spec-driven workflow.

**Applicable to Compass**:
- Spec creation pipeline that assesses complexity before planning
- Planner → Coder → QA Reviewer → QA Fixer pipeline
- Git worktree isolation for parallel agents (up to 12 terminals)
- Flexible auth: OAuth (subscription) or API key

**Pattern to adopt**:
```typescript
// Auto-Claude-style agent pipeline
const pipeline = [
  { agent: 'planner', input: compassHandoff, output: 'subtasks' },
  { agent: 'coder', input: 'subtasks', output: 'implementation', parallel: true },
  { agent: 'qa-reviewer', input: 'implementation', output: 'issues' },
  { agent: 'qa-fixer', input: 'issues', output: 'fixes' }
];
```

### 4.3 Claude-Flow

**Key innovation**: MCP-based swarm orchestration with 87 specialized tools.

**Applicable to Compass**:
- Agent coordination through MCP namespaces (`mcp__claude-flow__*`)
- Distributed execution across local and remote machines
- RAG integration for context retrieval

**Pattern to adopt**:
```typescript
// Claude-Flow-style MCP tool namespacing
const compassTools = {
  'mcp__compass__get_spec': getSpecHandler,
  'mcp__compass__report_progress': reportProgressHandler,
  'mcp__compass__request_clarification': requestClarificationHandler,
  'mcp__compass__record_decision': recordDecisionHandler
};
```

---

## Part 5: Recommended Architecture

### 5.1 Phase 1: Handoff Bundle Integration

**Scope**: Enable Claude Code to consume Compass handoff bundles with minimal infrastructure.

**Deliverables**:
1. Enhanced HANDOFF-* template optimized for Claude Code consumption
2. Export formats: Markdown bundle, Git repo push, direct clipboard
3. CLAUDE.md file generator that summarizes project context
4. Reconciliation import wizard in Compass UI

**Cost**: No additional infrastructure. Uses existing Claude Code CLI.

**Timeline**: 2-3 weeks

### 5.2 Phase 2: MCP Bridge

**Scope**: Bidirectional communication between running Claude Code sessions and Compass.

**Deliverables**:
1. Compass MCP server with spec query and progress reporting tools
2. Authentication via Compass API keys
3. Real-time progress dashboard in Compass UI
4. Clarification request workflow (Claude Code → Compass → User → Claude Code)

**Architecture**:
```
Claude Code CLI
    │
    │ MCP Protocol (HTTP)
    ▼
Compass MCP Server (Vercel Edge Function)
    │
    │ Convex Client
    ▼
Compass Database
    │
    │ WebSocket
    ▼
Compass UI (real-time updates)
```

**Cost**: Minimal (edge function invocations). No additional LLM costs.

**Timeline**: 3-4 weeks

### 5.3 Phase 3: Desktop Orchestrator

**Scope**: Full desktop application for local Claude Code orchestration.

**Deliverables**:
1. Tauri 2 desktop app for Windows, macOS, Linux
2. Multi-agent management (parallel Claude Code sessions)
3. Git worktree automation
4. Cost tracking and usage analytics
5. Offline mode with sync queue

**Technology stack**:
- **Framework**: Tauri 2 (Rust backend, web frontend)
- **Frontend**: React (shared components with Compass web)
- **State sync**: Convex client
- **Claude interface**: Agent SDK (TypeScript)
- **Local storage**: SQLite (better-sqlite3)

**Cost**: Development investment. No runtime LLM costs (uses subscription).

**Timeline**: 8-12 weeks

### 5.4 Architecture Summary

```
┌─────────────────────────────────────────────────────────────────────┐
│                        COMPASS ECOSYSTEM                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────────────┐    ┌──────────────────────┐              │
│  │   COMPASS WEB        │    │  COMPASS DESKTOP     │              │
│  │   (Planning Layer)   │    │  (Orchestration)     │              │
│  │                      │    │                      │              │
│  │ • Questioning arc    │◄──►│ • Claude Code spawn  │              │
│  │ • Widget UI          │sync│ • Multi-agent mgmt   │              │
│  │ • Research tools     │    │ • Progress viz       │              │
│  │ • Decision tracking  │    │ • Cost tracking      │              │
│  └──────────┬───────────┘    └──────────┬───────────┘              │
│             │                           │                           │
│             │ Convex                    │ Agent SDK                 │
│             ▼                           ▼                           │
│  ┌──────────────────────┐    ┌──────────────────────┐              │
│  │   CONVEX BACKEND     │    │  CLAUDE CODE CLI     │              │
│  │                      │    │  (Local Execution)   │              │
│  │ • Specs & artifacts  │◄──►│ • Filesystem access  │              │
│  │ • Decisions          │ MCP│ • Code generation    │              │
│  │ • Progress tracking  │    │ • Git operations     │              │
│  │ • Session state      │    │ • Test execution     │              │
│  └──────────────────────┘    └──────────────────────┘              │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Part 6: Cost Model Analysis

### 6.1 Current (API-Only) Model

| Activity | Model | Monthly Volume | Monthly Cost |
|----------|-------|----------------|--------------|
| Planning | Claude Opus 4.5 | 500k tokens | $7.50 |
| Implementation | Claude Opus 4.5 | 5M tokens | $75.00 |
| Testing/Debug | Claude Opus 4.5 | 2M tokens | $30.00 |
| **Total** | | **7.5M tokens** | **$112.50** |

### 6.2 Hybrid (Compass + Claude Code CLI) Model

| Activity | Platform | Monthly Volume | Monthly Cost |
|----------|----------|----------------|--------------|
| Planning | Compass (API) | 500k tokens | $7.50 |
| Implementation | Claude Code (subscription) | 5M tokens | $0* |
| Testing/Debug | Claude Code (subscription) | 2M tokens | $0* |
| **Total** | | **7.5M tokens** | **$7.50** |

*Covered by Claude Max subscription ($100-200/month flat rate)

### 6.3 Break-Even Analysis

| Scenario | API-Only | Hybrid + Subscription |
|----------|----------|----------------------|
| Light use (2M tokens/mo) | $30/mo | $107.50/mo (subscription overhead) |
| Medium use (10M tokens/mo) | $150/mo | $107.50/mo |
| Heavy use (50M tokens/mo) | $750/mo | $107.50/mo |
| Team (3 devs, 100M tokens/mo) | $1,500/mo | $307.50/mo |

**Break-even**: ~7M tokens/month for single user; lower for teams.

---

## Part 7: Implications for Compass Architecture

### 7.1 SYS-00 (System Definition)

**Required updates**:
- Add Layer 7b: "Local Execution Platforms" for Claude Code CLI integration
- Expand handoff bundle schema to include Claude Code-specific instructions
- Define reconciliation workflow for implementation delta ingestion

### 7.2 DD-11-01 (Handoff Schema)

**Required additions**:
```yaml
# Claude Code specific sections
claude_code:
  system_prompt_additions: |
    # Additional context for Claude Code
  allowed_tools:
    - Read
    - Write
    - Edit
    - Bash(npm *)
    - Bash(git *)
  mcp_config:
    compass:
      url: https://compass.example.com/mcp
  session_strategy: sequential | parallel
  verification_commands:
    - npm test
    - npm run lint
```

### 7.3 DD-17-01 (Integration Definitions)

**New integration type**:
```yaml
claude_code_cli:
  type: bidirectional
  direction: output (handoff) + input (reconciliation)
  protocol: MCP over HTTP
  auth: API key (bearer token)
  sync_mode: real-time (streaming) | batch (reconciliation)
```

### 7.4 ADR-02-01 (Orchestration Selection)

**Consideration**: The Mastra + Vercel AI SDK architecture should include hooks for Claude Code dispatch as an execution target, alongside Compass's internal orchestration.

---

## Part 8: Security Considerations

### 8.1 Authentication

| Layer | Mechanism | Notes |
|-------|-----------|-------|
| Compass → User | Convex Auth (per ADR-01-01) | Existing |
| Claude Code → Anthropic | OAuth (subscription) or API key | User's choice |
| Claude Code → Compass MCP | API key (bearer token) | Per-user, rotatable |

### 8.2 Data Flow Security

**Handoff bundles**: May contain proprietary architecture details. Recommend:
- Encryption at rest (Convex handles)
- No third-party bundle hosting
- Optional local-only mode (never syncs to cloud)

**MCP communication**: HTTPS only. No sensitive data in tool responses (references only).

**Desktop app**:
- Secure IPC (Tauri provides this)
- No credential storage in plaintext
- Keychain/credential manager integration

### 8.3 Execution Safety

**Claude Code tool restrictions** (via `--allowedTools`):
```bash
# Restrictive (recommended for automated execution)
--allowedTools "Read,Write,Edit,Bash(npm test),Bash(npm run *),Bash(git *)"

# Permissive (for trusted, supervised execution)
--allowedTools "Read,Write,Edit,Bash"
```

**Hooks for validation** (via Agent SDK):
```typescript
const options: ClaudeAgentOptions = {
  hooks: {
    PreToolUse: [
      {
        matcher: "Bash",
        handler: async (input, toolUseId, context) => {
          // Block destructive commands
          if (input.command.match(/rm -rf|drop table/i)) {
            return {
              hookSpecificOutput: {
                permissionDecision: "deny",
                permissionDecisionReason: "Destructive command blocked"
              }
            };
          }
          return {};
        }
      }
    ]
  }
};
```

---

## Part 9: Open Questions

### 9.1 Unresolved Design Decisions

1. **Reconciliation granularity**: Should Compass track every file change, or just summary deltas?
2. **Branching during execution**: If Claude Code discovers a design issue, how does it signal back to Compass for re-planning?
3. **Multi-user coordination**: How do parallel implementations from different users merge?
4. **Offline conflict resolution**: What happens when offline changes conflict with cloud state?

### 9.2 Future Research Needed

1. **Performance benchmarking**: Latency of MCP round-trips under load
2. **Cost optimization**: Token-efficient handoff bundle formats
3. **UX research**: Ideal progress visualization for multi-agent execution
4. **Desktop app frameworks**: Tauri 2 vs Electron for this use case

---

## Sources

### Tier 1: Official Documentation

1. **[T1/S1]** Anthropic. "Run Claude Code programmatically". Retrieved 2026-02-05. https://code.claude.com/docs/en/headless
   Note: Official documentation for print mode and Agent SDK.

2. **[T1/S1]** Anthropic. "Claude Agent SDK for Python". Retrieved 2026-02-05. https://github.com/anthropics/claude-agent-sdk-python
   Note: Official SDK repository with technical specifications.

3. **[T1/S1]** Anthropic. "Connect Claude Code to tools via MCP". Retrieved 2026-02-05. https://code.claude.com/docs/en/mcp
   Note: Official MCP integration documentation.

4. **[T1/S1]** Anthropic. "Claude Code on desktop". Retrieved 2026-02-05. https://code.claude.com/docs/en/desktop
   Note: Official desktop integration documentation.

### Tier 2: Credible Developer Sources

5. **[T2/S2]** GitHub. "GSD (Get Shit Done) - Structured workflow system for Claude Code". Retrieved 2026-02-05. https://github.com/b-r-a-n/gsd-claude
   Note: Community tool demonstrating phase-based planning integration.

6. **[T2/S2]** GitHub. "Auto-Claude - Autonomous multi-session AI coding". Retrieved 2026-02-05. https://github.com/AndyMik90/Auto-Claude
   Note: Community tool demonstrating multi-agent orchestration.

7. **[T2/S2]** GitHub. "Claude-Flow - Agent orchestration platform". Retrieved 2026-02-05. https://github.com/ruvnet/claude-flow
   Note: Community framework demonstrating MCP-based swarm coordination.

8. **[T2/S2]** GitHub. "claude-code-webui - Web interface for Claude CLI". Retrieved 2026-02-05. https://github.com/sugyan/claude-code-webui
   Note: Community tool demonstrating web frontend integration.

9. **[T2/S2]** GitHub. "Opcode - GUI app for Claude Code". Retrieved 2026-02-05. https://github.com/winfunc/opcode
   Note: Community tool demonstrating Tauri-based desktop integration.

10. **[T2/S2]** PyPI. "claude-code-sdk". Retrieved 2026-02-05. https://pypi.org/project/claude-code-sdk/
    Note: Official Python SDK package.

### Tier 3: General Technology Sources

11. **[T3/S2]** Medium. "GSD Framework: Meta-Prompting System That Ships Faster". Retrieved 2026-02-05. https://medium.com/@joe.njenga/i-tested-gsd-claude-code-meta-prompting-that-ships-faster-no-agile-bs-ca62aff18c04
    Note: Practitioner experience with GSD framework.

12. **[T3/S2]** Pasquale Pillitteri. "GSD Framework: The System Revolutionizing Development with Claude Code". Retrieved 2026-02-05. https://pasqualepillitteri.it/en/news/169/gsd-framework-claude-code-ai-development
    Note: Analysis of GSD approach.

---

## Appendix A: Glossary

**Agent SDK**: Anthropic's official libraries (Python, TypeScript) for programmatic Claude Code control.

**Context rot**: Degradation in LLM accuracy as context window fills with tokens. GSD addresses this with phase isolation.

**Git worktree**: Git feature allowing multiple working directories from a single repository. Used by Auto-Claude for parallel agent isolation.

**Handoff bundle**: Compass artifact (HANDOFF-*) containing implementation-ready specifications per DD-11-01.

**MCP (Model Context Protocol)**: Open standard for AI-tool integrations. Enables bidirectional communication between Claude Code and external systems.

**Print mode**: Claude Code's `-p` flag for non-interactive, scriptable execution.

**Reconciliation**: Process of updating Compass specifications based on implementation discoveries.

**Stream-JSON**: Newline-delimited JSON output format for real-time Claude Code progress monitoring.

---

## Appendix B: Related Documents

- **SYS-00**: System Definition (architecture layers, handoff model)
- **DD-11-01**: Handoff Schema (bundle structure)
- **DD-17-01**: Integration Definitions (integration patterns)
- **STD-17-01**: Integration Standards (error handling, retries)
- **ADR-02-01**: Orchestration Selection (Mastra + AI SDK)
- **RF-02-01**: Orchestration Findings (framework comparison)

---

*End of Claude Code CLI Integration Research Findings (RF-21-01)*
