---
id: STD-16-01-LLM
type: standard
area: 16-reliability-tiers
title: Reliability and Observability Standard (LLM View)
created: 2026-02-05
updated: 2026-02-05
summary: LLM-optimized view of enforceable observability and reliability requirements per tier, including logging schemas, alert definitions, health check specifications, and incident response procedures
tags: [reliability, observability, logging, alerting, standard, monitoring, health-check, llm, view]
links:
  - rel: companion
    target_id: "DD-16-01"
  - rel: related
    target_id: "STD-14-01"
  - rel: related
    target_id: "DD-17-01"
view: llm
source_id: STD-16-01
source_updated: 2026-02-01
staleness: fresh
---

# Reliability and Observability Standard (LLM View)

## LLM Summary
STD-16 specifies enforceable observability and reliability requirements for each reliability tier defined in `DD-16-01`. It provides tier-specific compliance checklists, a structured logging schema (JSON format with required fields), alert severity definitions with routing rules, health check endpoint specifications, incident severity classification (SEV-1 through SEV-4), and post-incident review requirements. Compliance is verified through pre-launch review and periodic audits (quarterly for Tier 1–2, annually for Tier 3–4). Exceptions to requirements MUST be documented with rationale, approved by tool owner plus one reviewer, and reviewed at each audit cycle.

## Canonical Statements
- All production tools (Tier 1–4) MUST implement structured logging with required fields.
- Every log entry MUST be valid JSON with: `timestamp` (ISO 8601 UTC), `level`, `service`, `message`.
- Tier 1–2 tools MUST additionally include `correlation_id` and `context` (entity IDs) in log entries.
- Tools MUST NOT log credentials, API keys, tokens, passwords, or sensitive personal data.
- All Tier 1–3 tools MUST expose a health check endpoint at `/health`.
- Health check MUST return HTTP 200 when healthy, HTTP 503 when unhealthy, and respond within 5 seconds.
- Health check MUST NOT require authentication.
- Tier 1 alerts MUST route to on-call person within 1 minute.
- Pre-launch verification MUST confirm documentation exists, health endpoints work, logging format is correct, and alerts are configured.
- Tier 1–2 pre-launch MUST include recovery procedure execution in test environment.
- Compliance exceptions MUST be documented with rationale, approved by tool owner + one reviewer, reviewed each audit cycle, and MUST NOT be used for core safety requirements.

## Scope and Non-Goals
- In scope: Tier-specific checklists, logging schema, alert definitions, health check spec, incident response procedures, compliance verification.
- Out of scope: Tier rationale and assignment criteria (see `DD-16-01`); broader compliance checklists per archetype (see `STD-14-01`).

## Dependencies
- Tier definitions and assignment: `DD-16-01`.
- Broader compliance checklists: `STD-14-01`.
- Integration patterns (error handling, retries): `DD-17-01`.

## Core Invariants
- Logging schema is uniform across all tiers; only required fields increase for Tier 1–2.
- Health check is stateless, unauthenticated, and lightweight.
- Alert thresholds MUST be tuned from baselines, not defaults.
- Untested alerts and untested backups are considered theoretical (not compliant).
- Post-incident reviews are blameless learning exercises, not blame assignments.

## Compliance Checklist

### Tier 1: Broadcast-Critical
- [ ] No single point of failure documented
- [ ] Redundant network paths or documented exception
- [ ] Backup data source configured and tested
- [ ] Graceful degradation documented
- [ ] Manual override exists
- [ ] Circuit breaker on all external dependencies
- [ ] Structured JSON logging with all required fields
- [ ] Comprehensive health check at `/health` (verifies all dependencies)
- [ ] Error rate + latency (P50/P95/P99) metrics
- [ ] Custom monitoring dashboard
- [ ] Correlation IDs through all components
- [ ] 90+ day log retention
- [ ] Critical alerts for health failure, error spike, latency degradation
- [ ] Alert routing verified to reach on-call within 1 minute
- [ ] Alert thresholds tuned from baseline
- [ ] Backup frequency < 1 hour; 30+ day retention
- [ ] Point-in-time recovery verified
- [ ] Recovery runbook documented and tested
- [ ] Recovery drill within last quarter
- [ ] On-call schedule for all broadcast windows
- [ ] Escalation path with contacts
- [ ] Pre-broadcast verification checklist

### Tier 2: Business-Critical
- [ ] Graceful degradation defined
- [ ] Idempotent operations for retryable processes
- [ ] Circuit breaker on external dependencies
- [ ] Work queuing handles temporary unavailability
- [ ] Structured JSON logging with correlation IDs
- [ ] Health check at `/health`
- [ ] Error rate metrics with alerting
- [ ] P50/P95 latency metrics
- [ ] 30+ day log retention
- [ ] Alerts for health failure and error rate threshold
- [ ] Alert routing within 30 minutes
- [ ] Daily backup; 14+ day retention
- [ ] Recovery procedure documented and tested within last year
- [ ] Business hours escalation path

### Tier 3: Business-Important
- [ ] Input validation; user-actionable error messages
- [ ] Rate limiting if API exposed
- [ ] Logging implemented (structured preferred)
- [ ] Health check at `/health`
- [ ] Error rate tracked; 14+ day log retention
- [ ] Alerts for repeated failures (routing within 2 hours)
- [ ] Daily backup; recovery procedure documented
- [ ] Manual fallback documented and known to users

### Tier 4: Internal Standard
- [ ] Understandable error messages
- [ ] Recovery procedure exists (informal OK)
- [ ] Issue reporting path clear to users
- [ ] Logging captures errors with context; 7+ day retention
- [ ] Graduation monitoring: blocking if unavailable? 5+ dependents? 6+ months old?

### Tier 5: Best Effort
- [ ] Labeled as experimental/prototype
- [ ] No production data connection without explicit approval
- [ ] Time box established; success/failure criteria defined

## Logging Schema

**Required fields (all tiers)**:

| Field | Type | Description |
|---|---|---|
| `timestamp` | ISO 8601 string (UTC) | When event occurred |
| `level` | string: `DEBUG`, `INFO`, `WARN`, `ERROR` | Severity |
| `service` | string | Component name |
| `message` | string | Human-readable description |

**Additional required fields (Tier 1–2)**:

| Field | Type | Description |
|---|---|---|
| `correlation_id` | string | Request trace identifier |
| `context` | object | Relevant entity IDs (`user_id`, `project_id`, etc.) |

**Recommended fields**: `metadata.duration_ms`, `metadata.operation`, `error.code`, `error.stack` (DEBUG only).

**Log levels**:
- `DEBUG`: Diagnostic detail; not enabled in production by default. Never alert.
- `INFO`: Normal operations (requests, completions, state changes). Never alert.
- `WARN`: Unexpected non-failure (retry succeeded, fallback used). Threshold-based alerting.
- `ERROR`: Failure needing attention. Always alert for Tier 1–2.

**Always log**: operation entry/exit with duration, all errors with context, external service calls, auth events, authorization failures.
**Never log**: credentials, tokens, API keys, passwords, sensitive personal data, full request bodies (use IDs), health check successes.

**Retention**: T1=90 days, T2=30 days, T3=14 days, T4=7 days, T5=not required.

## Alert Definitions

**Severity levels**:

| Severity | Response Time | Trigger Pattern |
|---|---|---|
| CRITICAL | < 5 min | Production down or severely degraded |
| HIGH | < 30 min | Significant degradation; approaching critical |
| MEDIUM | Business hours | Needs attention but not urgent |
| LOW | When available | Trend to watch |

**Tier 1 alerts**: health check failure (CRITICAL, 30s), error rate >5% for 2 min (CRITICAL), P95 latency >3× baseline for 5 min (HIGH), dependency unreachable 1 min (HIGH).

**Tier 2 alerts**: health check failure 2 min (HIGH), error rate >10% for 5 min (HIGH), unavailable 15+ min (CRITICAL during business hours), queue backup 30 min (MEDIUM).

**Tier 3 alerts**: same error 10+ times in 1 hour (MEDIUM), health check failure 30 min (MEDIUM).

**Alert routing**: T1=page/SMS always; T2=Slack+email (business hours), Slack-only (after hours); T3=email; T4=email optional.

## Health Check Specification

- **Endpoint**: `/health` (GET, no auth)
- **Response time**: < 5 seconds
- **HTTP 200**: `status: "healthy"` or `"degraded"` (operational)
- **HTTP 503**: `status: "unhealthy"` (not operational)
- **Response fields**: `status`, `timestamp`, `version`, `checks` (per-dependency: `status`, `latency_ms`, optional `message`)
- Return `degraded` when non-critical checks fail; `unhealthy` only when core function is blocked.
- Cache dependency checks 30–60 seconds to avoid load.
- During startup: return `unhealthy` until ready. During shutdown: return `unhealthy` immediately, then drain in-flight requests.

**Dependency check requirements**: T1=database+cache+external APIs+LLM required; T2=database required, others recommended; T3=database recommended; T4=all optional.

## Incident Response

**Severity classification**:

| SEV | Definition |
|---|---|
| SEV-1 | Complete outage of Tier 1 during broadcast, or data loss |
| SEV-2 | Complete outage of Tier 2, or significant Tier 1 degradation |
| SEV-3 | Complete outage of Tier 3, or partial Tier 2 degradation |
| SEV-4 | Any Tier 4 issue, or minor Tier 3 issues |

**Response targets**: SEV-1: detect <1 min, respond <5 min; SEV-2: detect <5 min, respond <30 min, resolve <1 hr; SEV-3: detect <30 min, respond <2 hrs, resolve <4 hrs; SEV-4: detect <4 hrs, respond <8 hrs, resolve <24 hrs.

**Post-incident review**: T1=all incidents within 48 hrs; T2=incidents >1 hr within 1 week; T3=optional within 2 weeks; T4=not required.

## Enforcement

- **Pre-launch**: documentation review + technical verification + recovery test (T1–2). Verified by tool owner + one reviewer.
- **Periodic audits**: T1=quarterly (full checklist + recovery drill); T2=quarterly (full checklist); T3=annually (checklist review); T4=annually (graduation criteria); T5=at time box expiry.
- **Findings**: Critical (security/T1 safety) → immediate remediation; Major (tier-required) → 2 weeks; Minor (recommended) → next audit; Observation → no required action.
- **Exceptions**: documented with rationale, approved by owner + one reviewer, reviewed each audit, not allowed for core safety requirements (T1 redundancy, data encryption).
