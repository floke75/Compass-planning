---
id: ADR-05-01
type: adr
area: 05-pm-integration
title: Project Management Integration Selection
status: proposed
created: 2026-02-01
updated: 2026-02-01
author: compass-research
summary: Selects Linear as primary PM tool for Compass integration, with GitHub Issues/Projects as budget alternative
tags: [pm, integration, decision, linear, github]
related:
  - RF-05-01
  - DD-17-01
  - STD-17-01
  - SYS-00
decision_date: null
deciders: []
supersedes: null
---

# Project Management Integration Selection

## Decision Status

**Status**: Proposed

**Decision Date**: Pending

**Deciders**: Pending

---

## Context

Compass requires integration with a project management tool to serve secondary users (broader EFN stakeholders) who need to:

- Submit bugs and feature requests that become planning inputs
- Track progress on planning work without learning Compass's full interface
- Consume documentation through familiar tools

Per the Compass System Definition (§3.6), PM integration is bidirectional: Compass pushes visibility (milestones, tasks, decision references) to the PM tool, and the PM tool feeds bugs/requests back into Compass as planning inputs.

This integration is scheduled for **Phase 4** of the Compass implementation timeline, meaning it will leverage the "proven value" budget tier ($3,000–$5,000/year) rather than the initial budget.

### Decision Drivers

1. **API quality for LLM-orchestrated automation**: Compass is built and maintained by LLM coding agents—the PM tool's API must be well-documented with predictable patterns
2. **Webhook reliability**: Bidirectional sync requires reliable event delivery
3. **DD-17-01 compliance**: Integration must follow established patterns for idempotency, retries, and error handling
4. **Secondary user experience**: Non-technical stakeholders must find the tool accessible
5. **Cost alignment**: Should fit within proven-value budget, or have clear justification for dedicated allocation

---

## Decision

**Primary Selection**: Linear (Business plan)

**Budget Alternative**: GitHub Issues/Projects (Team plan)

### Rationale

Linear is selected as the primary choice based on:

| Factor | Linear Advantage |
|--------|------------------|
| API coherence | Single GraphQL API with strong typing |
| SDK maturity | Official TypeScript SDK (601k weekly downloads) with 300+ operations |
| Webhook reliability | Automatic retries with exponential backoff (1 min → 1 hr → 6 hr) |
| User experience | Purpose-built PM UI accessible to non-technical stakeholders |
| Intake pattern | Linear Asks enables Slack/email submission without Linear accounts |

GitHub Issues/Projects is designated as the budget alternative when Linear's cost cannot be justified:

| Factor | GitHub Advantage |
|--------|------------------|
| Cost | $144/year (3 users) vs. Linear's $576/year |
| SDK ecosystem | Octokit has 10.6M weekly downloads—exceptional maturity |
| Team familiarity | Most developers already know GitHub |
| Code integration | Natural fit for implementation handoff |

### Cost Impact

Secondary users (EFN stakeholders) don't need PM tool accounts. They submit bugs/requests via Slack (Linear Asks) or forms, and receive status updates via Slack threads. Only the 2–3 primary Compass users need direct PM tool access.

| Configuration | Annual Cost | Budget Fit |
|---------------|-------------|------------|
| Linear Business (3 users) | $576 | ✅ Initial budget |
| Linear Business (5 users) | $960 | ✅ Initial budget |
| GitHub Team (3 users) | $144 | ✅ Initial budget |
| GitHub Team (5 users) | $240 | ✅ Initial budget |

**Both options fit within the initial budget** ($600–$2,000/year) when properly scoped.

### Trade-offs with Small Linear Team (3–5 seats)

| Capability | With 3 Business Seats | Mitigation |
|------------|----------------------|------------|
| Direct issue management | ✅ Primary users only | Sufficient for Compass workflow |
| Secondary user submission | ✅ Via Slack (Linear Asks) | No accounts needed |
| Secondary user visibility | ⚠️ Slack threads only | Build optional read-only dashboard if needed |
| API/webhook integration | ✅ Full access | Works regardless of seat count |
| Additional triagers | ❌ Need more seats ($16/user/month) | Add seats as needed, scales linearly |

**Critical requirement**: Linear Asks (Slack intake) requires **Business plan** ($16/user/month). The Basic plan ($10/user/month) lacks this feature, making the small-team intake workflow impractical.

---

## Alternatives Considered

### Plane.so

**Status**: Rejected

**Reasoning**: The 60 requests/minute rate limit would constrain LLM-orchestrated automation. The API is actively deprecating `/issues/` endpoints in favor of `/work-items/` with end-of-support in March 2026, creating migration risk. The official TypeScript SDK has only ~2,000 weekly downloads, indicating limited production adoption.

The self-hosted option (AGPL-3.0, free) is attractive but adds operational overhead inappropriate for a 2–3 person team without dedicated infrastructure experience.

**Revisit**: Consider in 12–18 months as the platform matures.

### Notion

**Status**: Rejected

**Reasoning**: The 3 requests/second rate limit requires careful batching for 120 users. More critically, webhook events are batched with 1–2 minute delays, making responsive bidirectional sync impractical. Notion lacks PM-specific constructs (sprints, velocity tracking, dependencies) that Linear and GitHub provide natively.

Notion excels as a documentation platform but is not optimized for project management workflows.

---

## Implementation Approach

### Phased Rollout

Integration will proceed in four phases aligned with the broader Compass timeline:

| Phase | Scope | Effort Estimate | Dependencies |
|-------|-------|-----------------|--------------|
| **Phase 1** | Read-only visibility | 40–60 hours | None |
| **Phase 2** | Webhook intake | 60–80 hours | Phase 1 |
| **Phase 3** | Bidirectional status sync | 100–120 hours | Phase 2 |
| **Phase 4** | Full orchestration | 120–160 hours | Phase 3 |

**Total estimated effort**: 320–420 hours across all phases

### Phase 1: Read-Only Visibility (Weeks 1–4)

**Goal**: Stakeholders can see what Compass is working on via the PM tool.

**Scope**:
- Compass pushes milestones and tasks to PM tool via API (one-way)
- Manual task creation in PM tool for bugs/requests
- No automated sync—Compass team manually monitors PM tool

**Implementation details**:
- Create Linear Project for each Compass planning milestone
- Create Linear Issues for tasks from work breakdown
- Use Labels for categorization: `compass:planning`, `compass:research`, `compass:decision`
- Store bidirectional ID mapping: Compass artifact ID ↔ Linear object ID

**Validates**: API connectivity, authentication flow, basic CRUD operations

### Phase 2: Webhook Intake (Weeks 5–8)

**Goal**: Bugs/requests automatically surface in Compass.

**Scope**:
- PM tool webhooks notify Compass of new issues
- Compass creates lightweight intake references (not full sync)
- Status remains manual (humans update both systems)

**Implementation details**:
- Create Convex HTTP endpoint for webhook reception
- Implement HMAC-SHA256 signature verification per DD-17-01 §7.2
- Implement delivery ID deduplication per STD-17-01 §3.4
- Create intake queue table in Convex database
- Build intake review UI for planners

**Validates**: Webhook reliability, signature verification, event deduplication

### Phase 3: Bidirectional Status Sync (Weeks 9–14)

**Goal**: Status changes propagate automatically between systems.

**Scope**:
- Compass status updates push to PM tool
- PM tool status changes (close, reopen) sync to Compass
- Conflict resolution for simultaneous updates

**Implementation details**:
- Implement mutation → scheduled action pattern per DD-17-01 §1.2
- Build exponential backoff with jitter per DD-17-01 §3
- Implement dead letter queue for failed syncs per DD-17-01 §3.5
- Create conflict resolution rules (last-write-wins with audit log)

**Validates**: Sync reliability, conflict handling, retry mechanisms

### Phase 4: Full Orchestration (Weeks 15–20)

**Goal**: Compass can fully orchestrate PM tool as external interface.

**Scope**:
- Automated task breakdown from Compass to PM tool
- Comment and activity sync bidirectionally
- Assignment changes propagate
- Decision records auto-link in PM tool
- Reporting and analytics integration

**Implementation details**:
- Expand webhook subscription to all relevant event types
- Implement bi-directional comment sync
- Create Linear Document links for Decision Records
- Build dashboard views for cross-system reporting

**Validates**: Complete bidirectional integration, production readiness

### Artifact Mapping

| Compass Artifact | Linear Object | Sync Direction |
|------------------|---------------|----------------|
| Planning Milestone | Project (with target date) | Compass → Linear |
| Task (work breakdown) | Issue within Project | Compass ↔ Linear |
| Decision Record (ADR) | Linked Document | Compass → Linear |
| Research Finding (RF) | Issue attachment (URL) | Compass → Linear |
| Epic/Theme | Initiative → Projects | Compass → Linear |
| Bug/Request (intake) | Issue with `compass:intake` label | Linear → Compass |

### Tagging Convention

| Label | Meaning |
|-------|---------|
| `compass:planning` | Originated from Compass planning |
| `compass:research` | Research-related item |
| `compass:decision` | Links to decision record |
| `compass:intake` | Awaiting Compass triage |
| `compass:planned` | Accepted into Compass planning |
| `compass:declined` | Declined with rationale |

---

## Consequences

### Positive

1. **Budget-friendly**: Linear Business at 3 seats ($576/year) fits within initial Compass budget
2. **Reduced integration complexity**: Single GraphQL API and automatic webhook retries reduce implementation burden
3. **Secondary user intake solved**: Linear Asks enables Slack-based submission without accounts for ~117 EFN stakeholders
4. **Accessible stakeholder interface**: Linear's purpose-built PM UI requires minimal training for primary users
5. **Strong SDK support**: Type-safe operations reduce bugs in LLM-generated integration code

### Negative

1. **Limited direct access**: Only 3–5 people can access Linear's full UI; others use Slack only
2. **Business plan required**: Linear Asks needs Business tier ($16/user) vs. Basic ($10/user)
3. **Slack dependency**: Secondary user workflow assumes EFN uses Slack (or will adopt it)
4. **GraphQL learning curve**: Team must learn GraphQL if unfamiliar (though LLM agents handle most code generation)
5. **Vendor dependency**: Linear is a startup; long-term viability risk compared to GitHub (Microsoft-backed)

### Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Need more triagers than 3 seats | Medium | Low | Add seats at $16/user/month as needed |
| Linear pricing increases | Low | Medium | Maintain GitHub fallback, export capability |
| EFN doesn't use Slack | Low | High | Evaluate email intake or custom forms instead |
| Linear API changes | Low | Medium | SDK abstracts most changes; monitor changelog |
| Webhook delivery failures | Low | Medium | Implement polling fallback for critical paths |

---

## Compliance

### DD-17-01 Compliance

| Requirement | Implementation |
|-------------|----------------|
| HMAC signature verification | Linear-Signature header with SHA-256 |
| Idempotency | Client-side via delivery ID (Linear-Delivery header) |
| Exponential backoff | Linear provides automatic; supplement with Convex scheduler |
| Dead letter queue | Convex table for failed operations |
| Secret management | Convex environment variables per STD-17-01 |

### STD-17-01 Checklist Applicability

The following checklists from STD-17-01 apply to this integration:

- §3.1 Pre-Development Checklist: Required before Phase 1
- §3.2 Secret Management Checklist: Required before Phase 1
- §3.3 Error Handling Checklist: Required before Phase 2
- §3.4 Retry Logic Checklist: Required before Phase 3
- §3.6 Webhook Security Checklist: Required before Phase 2

---

## Review Triggers

This decision should be revisited if:

1. Linear's pricing model changes significantly (>25% increase)
2. GitHub adds automatic webhook retries
3. Plane.so's API stabilizes and rate limits increase
4. Budget constraints require switching to GitHub
5. Linear is acquired or discontinues the product

---

## Appendix: GitHub Implementation Notes

If GitHub is selected as the budget alternative, the following adjustments are required:

### Cost Comparison

| Configuration | Linear Business | GitHub Team | Savings |
|---------------|-----------------|-------------|---------|
| 3 users | $576/year | $144/year | $432/year |
| 5 users | $960/year | $240/year | $720/year |

### API Differences

| Operation | Linear | GitHub |
|-----------|--------|--------|
| Create issue | GraphQL mutation | REST API |
| Update project item | GraphQL mutation | GraphQL mutation (Projects v2) |
| Custom fields | Limited (labels, estimates) | Full (GraphQL mutations) |
| Webhooks | Linear-Signature header | X-Hub-Signature-256 header |

### Additional Implementation Work

1. **Custom intake workflow**: Build Slack bot or web form for secondary user submission (Linear Asks equivalent doesn't exist)
2. **Dual API handling**: Use Octokit's unified interface but be aware of GraphQL requirements for Projects v2
3. **Webhook retry fallback**: Implement 15-minute polling as backup since GitHub doesn't retry failed deliveries
4. **User training**: Budget additional time for non-technical stakeholders unfamiliar with GitHub's code-centric interface

### Effort Adjustment

Add approximately 40–60 hours to total implementation estimate for:
- Custom Slack intake bot development
- Dual API abstraction layer
- Polling fallback implementation
- Additional stakeholder training materials

**Break-even analysis**: Linear's $432/year premium (vs. GitHub) pays for ~4–5 hours of development time at $100/hour. If custom intake development exceeds this, Linear's premium is justified.

---

## References

- RF-05-01: Project Management Integration Research Findings
- DD-17-01: Integration Architecture Patterns
- STD-17-01: Integration Standards
- SYS-00: Compass System Definition (§1.5, §3.3, §3.6, §4.1)

---

*End of Project Management Integration Selection (ADR-05-01)*
