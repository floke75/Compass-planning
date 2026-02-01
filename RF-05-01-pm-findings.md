---
id: RF-05-01
type: rf
area: 05-pm-integration
title: Project Management Integration Research Findings
status: draft
created: 2026-02-01
updated: 2026-02-01
author: compass-research
summary: Evaluates PM tools (Linear, GitHub Issues/Projects, Plane.so, Notion) for Compass integration based on API quality, webhook support, pricing, and DD-17-01 compliance
tags: [pm, integration, project-management, api, webhooks]
related:
  - DD-17-01
  - STD-17-01
  - SYS-00
confidence: high
methodology: "Web research with API documentation analysis and pricing verification"
limitations:
  - Pricing may change; verified as of February 2026
  - Plane.so API is actively evolving with deprecations planned
  - Notion webhook feature is recent; long-term reliability unconfirmed
responds_to: null
implications_for:
  - ADR-05-01
  - Phase 4 implementation timeline
---

# Project Management Integration Research Findings

## Document Purpose

This document evaluates project management tools for integration with Compass, focusing on how well each candidate supports the bidirectional sync requirements defined in the Compass System Definition (§3.6) and the integration patterns established in DD-17-01.

**Why this matters**: Secondary users (broader EFN stakeholders) need visibility into planning work through familiar PM tools. They submit bugs and requests that become planning inputs, track progress, and consume documentation—all without learning Compass's full planning interface.

**Scope**: API quality, webhook support, pricing for ~120 users, and compliance with DD-17-01/STD-17-01 integration standards.

---

## Executive Summary

**Recommendation**: Linear (primary) with GitHub Issues/Projects as budget alternative.

**Confidence**: High—based on direct API documentation review and current pricing verification.

**Key trade-offs**:

| Factor | Linear (3 seats) | GitHub (3 seats) |
|--------|------------------|------------------|
| Annual cost | $576 | $144 |
| API coherence | Excellent (single GraphQL) | Good (REST + GraphQL split) |
| Webhook reliability | Automatic retries | Manual redelivery only |
| Secondary user intake | Linear Asks (Slack/email) | Requires custom bot/forms |
| SDK maturity | Strong (601k weekly downloads) | Exceptional (10.6M weekly downloads) |

Secondary users (EFN stakeholders) don't need PM tool accounts. Linear Asks enables Slack-based submission and status updates without accounts. Only 2–3 primary Compass users need Linear seats.

**Budget fit**: Linear Business at 3 users ($576/year) fits within the initial Compass budget ($600–$2,000/year). The 4x cost premium over GitHub ($144/year) buys superior intake workflow and reduced integration complexity.

---

## Part 1: Capability Matrix

### 1.1 API and SDK Comparison

| Capability | Linear | GitHub Issues/Projects | Plane.so | Notion |
|------------|--------|------------------------|----------|--------|
| **API Type** | GraphQL only | REST + GraphQL | REST only | REST only |
| **Official TypeScript SDK** | ✅ @linear/sdk | ✅ @octokit/rest | ✅ @makeplane/plane-node-sdk | ✅ @notionhq/client |
| **Weekly npm downloads** | ~601,000 | ~10,600,000 | ~2,000 | ~525,000 |
| **API Documentation Quality** | Excellent | Excellent | Good | Good |
| **OpenAPI/Schema Available** | GraphQL schema | OpenAPI spec | OpenAPI spec | OpenAPI spec |

**Analysis**: Linear and GitHub have the most mature SDKs. Linear's GraphQL-only approach provides consistent patterns that work well with LLM code generation—the strong typing reduces hallucination risk. GitHub's dual API (REST for Issues, GraphQL required for Projects v2) adds complexity but Octokit handles both seamlessly.

Plane.so's SDK is functional but immature (~2,000 weekly downloads suggests limited production adoption). Notion's SDK is solid but the API is designed for general-purpose databases, not PM-specific workflows.

### 1.2 Rate Limits

| Tool | Limit | Window | Burst Handling |
|------|-------|--------|----------------|
| **Linear** | 5,000 requests | Per hour | X-RateLimit headers |
| **GitHub** | 5,000–15,000 requests | Per hour | Retry-After header |
| **Plane.so** | 60 requests | Per minute | Unknown |
| **Notion** | 3 requests | Per second (~10,800/hr) | Retry-After header |

**Analysis**: Linear and GitHub provide adequate headroom for LLM-orchestrated automation with 120 users. Plane.so's 60/minute limit would constrain batch operations. Notion's per-second limit is manageable but requires careful request pacing.

For Compass's expected usage pattern (sporadic planning sessions, not continuous automation), all four tools have sufficient capacity. Linear and GitHub's hourly windows are more forgiving for burst activity during intensive planning sessions.

### 1.3 Authentication Methods

| Tool | API Key | OAuth 2.0 | Personal Access Token |
|------|---------|-----------|----------------------|
| **Linear** | ✅ | ✅ (recommended) | ✅ |
| **GitHub** | ❌ | ✅ (GitHub Apps) | ✅ |
| **Plane.so** | ✅ | ❌ | ❌ |
| **Notion** | ❌ | ✅ (integrations) | ❌ |

**Analysis**: For production deployment, OAuth 2.0 provides proper workspace-level permissions and token refresh. Linear and GitHub both support this well. Plane.so's API key–only approach limits permission granularity. Notion requires creating an "integration" which functions similarly to OAuth.

---

## Part 2: Webhook Support Analysis

### 2.1 Webhook Capabilities

| Capability | Linear | GitHub | Plane.so | Notion |
|------------|--------|--------|----------|--------|
| **Signature Verification** | ✅ HMAC-SHA256 | ✅ HMAC-SHA256 | ✅ HMAC-SHA256 | ✅ HMAC-SHA256 |
| **Signature Header** | `Linear-Signature` | `X-Hub-Signature-256` | `X-Plane-Signature` | `X-Notion-Signature` |
| **Delivery ID Header** | `Linear-Delivery` | `X-GitHub-Delivery` | `X-Plane-Delivery` | Client-side only |
| **Event Types** | ~50 | ~70 | ~5 entity types | ~4 event types |
| **Automatic Retries** | ✅ 3 retries with backoff | ❌ Manual only | ✅ Exponential backoff | ❌ Unknown |
| **Retry Schedule** | 1 min → 1 hr → 6 hr | N/A | Exponential | N/A |

**Analysis**: Linear provides the most robust webhook delivery with automatic retries using exponential backoff. This aligns well with DD-17-01's reliability requirements—Linear handles transient failures automatically, reducing the need for Compass to implement complex retry logic.

GitHub's lack of automatic retries is a significant gap. If a webhook delivery fails (endpoint down, timeout), GitHub marks it as failed and requires manual redelivery via the UI or API. For reliable sync, Compass would need to implement a polling fallback or a manual reconciliation workflow.

All four tools support HMAC-SHA256 signature verification, meeting STD-17-01's webhook security requirements.

### 2.2 Webhook Event Coverage

**Linear webhook events** (relevant subset):
- `Issue`: create, update, remove (state changes, assignments, labels)
- `Comment`: create, update, remove
- `Project`: create, update, remove
- `Cycle`: create, update, remove
- `Label`: create, update, remove

**GitHub webhook events** (relevant subset):
- `issues`: opened, edited, deleted, closed, reopened, assigned, labeled
- `issue_comment`: created, edited, deleted
- `project_v2_item`: created, edited, deleted, converted
- `milestone`: created, edited, deleted

**Plane.so webhook events**:
- `issue`: create, update, delete
- `cycle`: create, update, delete
- `module`: create, update, delete
- `project`: create, update, delete
- `work_item`: create, update, delete (new model)

**Notion webhook events**:
- `page.content_updated`: batched, 1–2 minute delay
- `page.created`, `page.deleted`
- `comment.created`, `comment.deleted`
- `database.schema_updated`

**Analysis**: Linear and GitHub provide granular events covering all PM operations Compass needs. Notion's event set is limited and batched with delays—content updates are aggregated and delivered with 1–2 minute latency, making near-real-time sync impractical.

### 2.3 DD-17-01 Compliance Assessment

| Requirement (per DD-17-01) | Linear | GitHub | Plane.so | Notion |
|---------------------------|--------|--------|----------|--------|
| HMAC signature verification | ✅ | ✅ | ✅ | ✅ |
| Timestamp validation possible | ✅ (in payload) | ✅ (in payload) | ✅ (in payload) | ✅ |
| Delivery ID for deduplication | ✅ | ✅ | ✅ | ⚠️ Partial |
| Idempotency keys (native) | ❌ | ❌ | ❌ | ❌ |
| Retry-After header | ⚠️ Custom format | ✅ Standard | ❌ Unknown | ✅ Standard |
| Structured error responses | ✅ GraphQL errors | ✅ JSON errors | ✅ JSON errors | ✅ JSON errors |

**Critical finding**: None of the candidates provide native idempotency keys. Compass must implement client-side deduplication using delivery IDs before processing webhook payloads. This is standard practice but adds implementation overhead.

Linear uses custom rate limit headers (`X-RateLimit-*`) rather than standard `Retry-After`, requiring adapter code to translate to STD-17-01 patterns.

---

## Part 3: Pricing Analysis

### 3.1 Understanding the Actual User Requirement

Per the Compass System Definition (§1.5):

- **Primary users (2–3 people)**: Run the full planning workflow in Compass and need direct PM tool access
- **Secondary users (~117 people)**: Submit bugs/requests and track progress via familiar tools—they do NOT need PM tool accounts

This shapes the pricing model. Linear's **Linear Asks** feature (Business plan) allows anyone in Slack to submit requests and receive updates without a Linear account.

### 3.2 Small-Team Pricing (Realistic Scenario)

| Scenario | Linear Business | GitHub Team | Plane.so Pro | Notion Plus |
|----------|----------------|-------------|--------------|-------------|
| **3 users** | $576/year | $144/year | $216/year | $360/year |
| **5 users** | $960/year | $240/year | $360/year | $600/year |
| **10 users** | $1,920/year | $480/year | $720/year | $1,200/year |

**Linear Business @ 3 users = $576/year** fits comfortably within the initial budget ($600–$2,000/year).

### 3.3 How Secondary Users Interact (Without PM Tool Accounts)

| Tool | Secondary User Intake Method | Secondary User Status Visibility |
|------|------------------------------|----------------------------------|
| **Linear** | Linear Asks via Slack/email (Business plan) | Slack thread updates, email notifications |
| **GitHub** | Create issues via Slack bot or forms | GitHub notifications, Slack integration |
| **Plane.so** | API-based forms | Custom dashboard or Slack |
| **Notion** | Comment as guest (free) or forms | Page access as guest (free) |

**Linear Asks** is the cleanest solution: secondary users submit via Slack emoji reaction (🎫) or `/ask` command, and receive automatic status updates in the same Slack thread. No Linear account needed.

### 3.4 Trade-offs with Small Linear Team

Running Linear with only 3 Business seats means:

| Capability | Available? | Workaround |
|------------|-----------|------------|
| Primary users manage issues directly | ✅ Yes | — |
| Secondary users submit via Slack | ✅ Yes | Linear Asks (Business) |
| Secondary users view full Linear UI | ❌ No | Slack updates + optional dashboard |
| Compass↔Linear API sync | ✅ Yes | API works regardless of seat count |
| Webhook-based intake | ✅ Yes | Works regardless of seat count |

**Key constraint**: If more than 3 people need to directly triage, assign, or manage issues in Linear's UI, additional seats are needed at $16/user/month each.

### 3.5 Budget Alignment

| Configuration | Annual Cost | Budget Fit |
|---------------|-------------|------------|
| Linear Business (3 users) | $576 | ✅ Fits initial budget |
| Linear Business (5 users) | $960 | ✅ Fits initial budget |
| Linear Business (10 users) | $1,920 | ✅ Fits initial budget |
| GitHub Team (3 users) | $144 | ✅ Fits initial budget |
| GitHub Team (10 users) | $480 | ✅ Fits initial budget |

**Conclusion**: Both Linear and GitHub fit within Compass's initial budget when properly scoped to the actual user requirement. Linear's premium is ~4x GitHub's cost but provides superior intake workflow via Linear Asks.

### 3.6 What Linear Asks Provides (Business Plan)

Linear Asks enables the bug/request intake pattern without requiring secondary users to have accounts:

- **Slack intake**: Submit via emoji (🎫) or `/ask` command in any channel
- **Email intake**: Forward/CC to designated Linear email addresses
- **Templates**: Structured forms for different request types (bug, feature, IT ticket)
- **Bidirectional sync**: Slack thread updates when issue status changes
- **No account required**: Anyone in Slack workspace can submit

This matches exactly what Compass needs for secondary user intake per SYS-00 §3.6.

---

## Part 4: Integration Pattern Fit

### 4.1 Artifact-to-PM-Object Mapping

Based on Compass artifact types (per DD-13-01) and PM tool native constructs:

| Compass Artifact | Linear | GitHub | Plane.so | Notion |
|------------------|--------|--------|----------|--------|
| **Planning Milestone** | Project (with target date) | Milestone | Cycle | Database item (Date property) |
| **Task (from work breakdown)** | Issue | Issue | Work Item | Database item (Status) |
| **Decision Record (ADR)** | Linked Document | Issue with `decision` label | Module description | Linked page |
| **Research Finding (RF)** | Issue attachment (URL) | Issue body link | Issue link | Embedded page |
| **Epic/Theme** | Initiative → Projects | Labels + Milestones | Module | Parent relation |

**Linear-specific mapping**: 
- Compass milestones → Linear **Projects** with milestone checkpoints
- Individual tasks → Linear **Issues** within Projects
- Strategic themes → Linear **Initiatives** grouping related Projects
- Use Labels for categorization: `compass:planning`, `compass:research`, `compass:decision`

**GitHub-specific mapping**:
- Compass milestones → GitHub **Milestones** (time-bounded)
- Tasks → GitHub **Issues** with Projects v2 custom fields
- Decision records → Issues with `decision-record` label, linked bidirectionally
- Use **iteration fields** in Projects v2 for cycles

### 4.2 Bug/Request Intake Flow

**Recommended pattern**: PM-side submission with Compass-side triage.

```
┌─────────────────────────────────────────────────────────────┐
│ Secondary User submits bug/request in PM Tool               │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ PM Tool fires webhook (issue.created)                       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ Compass Intake Service receives webhook                     │
│ • Validates signature (per STD-17-01)                       │
│ • Deduplicates using delivery ID                            │
│ • Creates lightweight intake reference (NOT full sync)      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ Compass planners review in intake queue                     │
│ • Accept → Creates Compass planning item                    │
│ • Decline → Updates PM tool with explanation                │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ Status sync: Compass → PM Tool                              │
│ • Planning status reflected in PM tool                      │
│ • Stakeholders see progress without Compass access          │
└─────────────────────────────────────────────────────────────┘
```

**Key design decisions**:

1. **One-way import, two-way status**: Bugs/requests are imported as planning inputs, not fully mirrored. Compass pushes status updates back so stakeholders see progress.

2. **Triage happens in Compass**: Secondary users submit freely in PM tool. Planning decisions happen in Compass's intake queue, keeping planning logic centralized.

3. **Tagging convention**: PM tool issues tagged `compass:intake` trigger import. After triage, tag becomes `compass:planned` or `compass:declined` with rationale comment.

**Linear-specific**: Linear's **Customer Requests** feature (Business plan) is designed exactly for this pattern—external requests flow in, get triaged, and link to implementing Issues.

### 4.3 Phased Integration Scope

**Phase 1 (Minimal Visibility)**:
- Compass pushes milestones and tasks to PM tool (one-way)
- Manual task creation in PM tool for bugs/requests
- No automated sync—planners manually check PM tool
- **Validates**: API connectivity, authentication, basic CRUD

**Phase 4 (Full Bidirectional)**:
- Webhook-driven intake from PM tool to Compass
- Automatic status sync in both directions
- Comment and activity sync
- Assignment changes propagate
- Decision records auto-link in PM tool

See ADR-05-01 for detailed phased implementation roadmap.

---

## Part 5: Candidate Assessments

### 5.1 Linear

**Strengths**:
- GraphQL API is internally consistent—Linear uses the same API they expose
- Official TypeScript SDK provides 300+ type-safe operations
- Webhook retries with exponential backoff reduce reliability burden
- Purpose-built PM UI is intuitive for non-technical users
- **Linear Asks** enables Slack/email intake without accounts for secondary users

**Weaknesses**:
- Business plan required for Linear Asks ($16/user/month vs. Basic's $10)
- No native idempotency keys
- GraphQL-only requires learning curve if team unfamiliar

**Cost**: 
- 3 Business seats: $576/year ✅ Fits initial budget
- 5 Business seats: $960/year ✅ Fits initial budget

**Integration complexity**: Low. Single API paradigm, strong SDK, reliable webhooks, built-in Slack intake.

### 5.2 GitHub Issues/Projects

**Strengths**:
- Most mature ecosystem—Octokit SDK has 10.6M weekly downloads
- REST API documentation is exceptional
- Lowest cost option at $144–$240/year (3–5 users)
- Team likely already familiar with GitHub
- Tight integration with code repositories

**Weaknesses**:
- Projects v2 requires GraphQL—dual API paradigm adds complexity
- No automatic webhook retries—must implement polling fallback
- No built-in Slack intake—requires custom bot or forms
- Code-centric UI may confuse non-technical stakeholders
- Custom fields require GraphQL mutations

**Cost**:
- 3 Team seats: $144/year ✅ Fits initial budget
- 5 Team seats: $240/year ✅ Fits initial budget

**Integration complexity**: Medium. Dual API, manual retry handling, custom intake workflow needed.

### 5.3 Plane.so

**Strengths**:
- Self-hosted option is genuinely free (AGPL-3.0)
- Official TypeScript SDK now available
- Active development and feature parity focus
- Clean UI similar to Linear

**Weaknesses**:
- 60 requests/minute rate limit constrains automation
- API is deprecating `/issues/` in favor of `/work-items/` (March 2026)
- SDK maturity is low (~2,000 weekly downloads)
- Self-hosting adds operational overhead

**Integration complexity**: Medium-High. Rate limits, API churn, less mature SDK.

### 5.4 Notion

**Strengths**:
- Native webhooks now available (recent addition)
- Flexible database model adapts to any schema
- Free guests allow viewer-only access at no cost
- Many teams already use Notion

**Weaknesses**:
- 3 req/sec rate limit requires careful batching
- Webhook events batched with 1–2 minute delays
- No PM-specific constructs (sprints, velocity, dependencies)
- General-purpose tool, not PM-optimized

**Integration complexity**: High. Rate limits, event delays, requires building PM abstractions.

---

## Part 6: Recommendation

### Primary: Linear Business (3–5 seats)

Linear provides the cleanest integration path for an LLM-orchestrated system. The single GraphQL API, strong TypeScript SDK, and automatic webhook retries reduce implementation complexity and ongoing maintenance burden.

**Cost**: $576–$960/year (3–5 Business seats) fits within the initial budget.

**Key advantage**: Linear Asks enables secondary users to submit bugs/requests via Slack without needing Linear accounts. This solves the intake problem elegantly—the ~117 secondary EFN stakeholders interact through Slack, not Linear.

**When to add seats**: If more than 3–5 people need to directly triage, assign, or manage issues in Linear's UI, add seats at $16/user/month. This scales linearly and predictably.

### Budget Alternative: GitHub Issues/Projects (3–5 seats)

At $144–$240/year (3–5 Team seats), GitHub is the most cost-effective option. The Octokit SDK is exceptionally mature, and most developers are already familiar with GitHub.

**Trade-offs**:
- No equivalent to Linear Asks—requires building a custom Slack bot or intake form
- Lacks automatic webhook retries—must implement polling fallback
- Projects v2 requires GraphQL for custom fields
- Non-technical stakeholders may find the code-centric interface less intuitive

**When GitHub makes sense**: If EFN already has strong GitHub adoption, the familiarity advantage may outweigh Linear's superior intake workflow.

### Not Recommended

**Plane.so**: The 60 req/min rate limit and API deprecation timeline create unnecessary friction. Revisit in 12–18 months.

**Notion**: The 3 req/sec rate limit and 1–2 minute event delays make responsive bidirectional sync impractical. Notion lacks PM-specific constructs.

---

## Appendix A: Sources

1. **[T1/S1]** Linear. "Pricing – Linear." Retrieved 2026-02-01. https://linear.app/pricing

2. **[T1/S1]** Linear. "Rate limiting – Linear Developers." Retrieved 2026-02-01. https://linear.app/developers/rate-limiting

3. **[T1/S1]** Linear. "Webhooks – Linear Developers." Retrieved 2026-02-01. https://linear.app/developers/webhooks

4. **[T1/S1]** Linear. "Getting started – Linear Developers." Retrieved 2026-02-01. https://linear.app/developers/sdk

5. **[T1/S1]** Linear. "Linear Asks – Manage workplace requests." Retrieved 2026-02-01. https://linear.app/asks

6. **[T1/S1]** Linear. "Asks – Linear Docs." Retrieved 2026-02-01. https://linear.app/docs/linear-asks

7. **[T1/S1]** Linear. "Members and roles – Linear Docs." Retrieved 2026-02-01. https://linear.app/docs/members-roles

8. **[T1/S1]** Linear. "Customer Requests – Linear Docs." Retrieved 2026-02-01. https://linear.app/docs/customer-requests

9. **[T1/S1]** GitHub. "Handling failed webhook deliveries - GitHub Docs." Retrieved 2026-02-01. https://docs.github.com/en/webhooks/using-webhooks/handling-failed-webhook-deliveries

10. **[T1/S1]** Plane. "Plane API Documentation." Retrieved 2026-02-01. https://developers.plane.so/api-reference/introduction

11. **[T2/S2]** npm. "@octokit/rest." Retrieved 2026-02-01. https://www.npmjs.com/package/@octokit/rest

---

## Appendix B: Related Documents

- **SYS-00**: Compass System Definition (§1.5 Who Uses Compass, §3.3 Interface Requirements, §3.6 External Integrations)
- **DD-17-01**: Integration Architecture Patterns (webhooks, retries, idempotency)
- **STD-17-01**: Integration Standards (compliance checklists)
- **ADR-05-01**: PM Integration Selection (decision record, implementation roadmap)

---

*End of Project Management Integration Research Findings (RF-05-01)*
