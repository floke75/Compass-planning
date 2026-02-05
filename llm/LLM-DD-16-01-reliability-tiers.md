---
id: DD-16-01-LLM
type: definition
area: 16-reliability-tiers
title: Reliability Tiers and Operational Standards (LLM View)
created: 2026-02-05
updated: 2026-02-05
summary: LLM-optimized view of reliability tier definitions, per-tier operational requirements, tier assignment criteria, and archetype-to-tier mapping
tags: [reliability, operations, monitoring, tiers, recovery, observability, llm, view]
links:
  - rel: companion
    target_id: "STD-16-01"
  - rel: related
    target_id: "DD-14-01"
  - rel: related
    target_id: "STD-14-01"
  - rel: related
    target_id: "DD-17-01"
  - rel: related
    target_id: "ADR-01-01"
view: llm
source_id: DD-16-01
source_updated: 2026-02-01
staleness: fresh
---

# Reliability Tiers and Operational Standards (LLM View)

## LLM Summary
DD-16 defines five reliability tiers for EFN (a financial news organization) tools, matching operational investment to business criticality. Each tier specifies requirements across four domains: safeguards, observability, backup/recovery, and incident response. The document provides a decision framework for tier assignment, maps project archetypes from `DD-14-01` to default tiers, and defines Compass itself as Tier 2 (Business-Critical) with specific enhancements for continuous state persistence and graceful degradation. Availability targets are goals guiding design, not contractual SLAs. The framework ensures broadcast-critical tools get redundancy and failover while internal utilities get minimal overhead proportionate to a small team's capacity.

## Canonical Statements
- Reliability tier MUST be assigned before detailed planning begins.
- Tier assignment MUST be derived from archetype classification per `DD-14-01`.
- Redundant components are REQUIRED for Tier 1; recommended for Tier 2.
- Graceful degradation design is REQUIRED for Tier 1 (documented) and Tier 2.
- Circuit breakers are REQUIRED for Tier 1 and Tier 2 external dependencies.
- Pre-broadcast verification is REQUIRED before every broadcast window for Tier 1 tools.
- On-call responsibility MUST be assigned for every Tier 1 broadcast window.
- Monitoring MUST detect Tier 2 failures within minutes.
- Tier 2 work MUST queue safely during outages using idempotent operations per `DD-17-01` §2.
- Tier 3 tools MUST have basic monitoring and documented manual fallback procedures.
- Tier 4 tools MUST provide understandable error messages and a clear issue-reporting path.
- Tier 5 tools MUST be clearly labeled as experimental and MUST NOT connect to production data without explicit approval.
- Every Tier 5 experiment SHOULD have a planned graduation or retirement date.
- Any tool involved in a security incident is treated as Tier 2 minimum until remediation is complete.
- Tier assignments SHOULD be reviewed when usage increases 10×, new downstream dependencies appear, incidents reveal higher-than-expected impact, scope expands, or annually per `STD-14-01` §3.3.

## Scope and Non-Goals
- In scope: Tier definitions, per-tier operational requirements, tier assignment decision framework, archetype-to-tier mapping, Compass reliability target.
- Out of scope: Enforceable checklists and schemas (see `STD-16-01`); detailed integration patterns (see `DD-17-01`).

## Dependencies
- Archetype definitions: `DD-14-01`.
- Compliance checklists per archetype: `STD-14-01`.
- Integration patterns (idempotency, circuit breakers, retries): `DD-17-01`.
- Backend selection (Convex reliability characteristics): `ADR-01-01`.
- Enforceable standard companion: `STD-16-01`.

## Core Invariants
- Operational investment is proportionate to business criticality—never uniform.
- Availability percentages are targets guiding design, not SLAs with penalties.
- Tier 1 requires zero single points of failure in the critical path during broadcast.
- Compass targets Tier 2 with enhanced state persistence (continuous save, conflict detection, graceful degradation for external services).
- Tier assignment can be overridden upward by security incidents, regulatory requirements, or executive commitments.
- Managed services are preferred over self-hosting to match small team capacity.

## Glossary Snapshot
- **Availability target**: Percentage of time a system is operational; 99.9% = 43 min downtime/month, 99% = 7.2 hours, 95% = 36 hours, 90% = 72 hours.
- **Recovery Time Objective (RTO)**: Maximum acceptable downtime before full service restoration.
- **Recovery Point Objective (RPO)**: Maximum acceptable data loss measured in time.
- **Graceful degradation**: Continued partial service when dependencies fail, rather than complete failure.

## Tier Catalog

| Tier | Name | Impact of Failure | Availability Target | RTO |
|------|------|-------------------|---------------------|-----|
| 1 | Broadcast-Critical | Visible to audience in real-time | 99.9% during broadcast windows | < 30 seconds |
| 2 | Business-Critical | Significantly blocks content creation | 99% during business hours | < 1 hour |
| 3 | Business-Important | Delays publication; work can queue | 95% | < 4 hours |
| 4 | Internal Standard | Causes inconvenience; workarounds exist | 90% | < 24 hours |
| 5 | Best Effort | Minimal impact; failure acceptable | No target | No target |

## Per-Tier Requirements Matrix

### Safeguards

| Requirement | T1 | T2 | T3 | T4 | T5 |
|---|---|---|---|---|---|
| Redundant components | Required | Recommended | — | — | — |
| Graceful degradation | Required, documented | Required | Recommended | Optional | — |
| Pre-deployment testing | Load+integration+failover | Integration+unit | Unit+smoke | Basic | — |
| Manual override | Required | Recommended | Optional | — | — |
| Circuit breaker | Required | Required | Recommended | Optional | — |
| Input validation | Strict | Standard | Basic | Basic | Optional |
| Rate limiting (API) | Required | Required | Recommended | Optional | — |

### Observability

| Requirement | T1 | T2 | T3 | T4 | T5 |
|---|---|---|---|---|---|
| Structured logging (JSON) | Required | Required | Required | Recommended | Optional |
| Log retention | 90 days | 30 days | 14 days | 7 days | — |
| Health check endpoint | Required (comprehensive) | Required (basic) | Required (basic) | Recommended | — |
| Error rate metrics | Real-time + alerting | With alerting | Collected | Optional | — |
| Latency metrics | P50/P95/P99 | P50/P95 | Optional | — | — |
| Request tracing (correlation IDs) | Required | Required | Recommended | Optional | — |
| Custom dashboards | Required | Recommended | Optional | — | — |

### Backup & Recovery

| Requirement | T1 | T2 | T3 | T4 | T5 |
|---|---|---|---|---|---|
| Data backup frequency | Continuous or < 1 hr | Daily | Daily | Weekly | — |
| Backup retention | 30 days | 14 days | 7 days | 7 days | — |
| Backup verification | Weekly restore tests | Monthly restore tests | Quarterly | Annual | — |
| Recovery runbook | Detailed, tested quarterly | Documented, tested annually | Documented | Informal OK | — |
| Recovery drills | Quarterly | Annually | — | — | — |
| Point-in-time recovery | Required | Recommended | Optional | — | — |

### Incident Response

| Requirement | T1 | T2 | T3 | T4 | T5 |
|---|---|---|---|---|---|
| Detection target | < 1 min | < 5 min | < 30 min | < 4 hrs | User-reported |
| Initial response target | < 5 min | < 30 min | < 2 hrs | < 8 hrs | Best effort |
| On-call requirement | During broadcast | Business hours | — | — | — |
| Escalation path | Defined with contacts | Defined | Informal OK | Informal OK | — |
| Post-incident review | All incidents | Extended outages (>1 hr) | Optional | — | — |

## Tier Assignment Decision Framework

1. **Used during live broadcasts?** → Tier 1
2. **Failure blocks content creation?** → Tier 2 (or Tier 3 if work can queue with tolerance)
3. **Failure delays publication?** → Tier 3 (or Tier 4 if manageable)
4. **Experiment or prototype?** → Tier 5; otherwise → Tier 4

**Factors increasing tier**: downstream dependencies, data sensitivity, user count scaling, revenue proximity.
**Factors decreasing tier**: robust manual fallback, low usage frequency, easy rollback.
**Override conditions**: security incidents (→ Tier 2 minimum), regulatory requirements, executive commitments.

## Archetype-to-Tier Mapping

| Archetype (DD-14-01) | Default Tier |
|---|---|
| Broadcast-Critical | Tier 1 |
| Production Pipeline | Tier 2 |
| Publishing Pipeline | Tier 3 |
| Analytics & Intelligence | Tier 4* |
| Internal Utility | Tier 4 |
| Exploratory | Tier 5 |

*Analytics & Intelligence defaults to Tier 4 availability but has elevated security and privacy requirements regardless of tier.

## Compass Reliability Target

- **Tier**: 2 (Business-Critical)
- **Availability**: 99% during business hours (Mon–Fri, 8 AM–8 PM)
- **RTO**: < 1 hour full; < 5 minutes degraded mode (browsing existing content)
- **RPO**: < 1 minute conversation state; < 5 minutes artifact edits
- **Enhancements beyond standard Tier 2**: continuous state persistence (every user input persisted within seconds), auto-save with conflict detection, graceful degradation for LLM/memory failures, safe retry for idempotent operations per `DD-17-01` §2.
- **Rationale for Tier 2 (not Tier 1)**: Not used during live broadcasts; planning sessions can pause/resume; 2–3 person team cannot sustain Tier 1 operational costs.

## Tier Transition Procedures

**Upgrading** (e.g., T4 → T3): complete new-tier compliance checklist (`STD-14-01`), implement required observability, document monitoring/alerting/recovery, run at new tier 30 days with enhanced monitoring.

**Downgrading** (e.g., T2 → T3): document rationale, notify dependent users, update monitoring thresholds, archive (don't delete) higher-tier documentation.
