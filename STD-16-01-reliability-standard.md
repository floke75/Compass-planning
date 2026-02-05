---
id: STD-16-01
type: std
area: 16-reliability-tiers
title: Reliability and Observability Standard
status: draft
created: 2026-02-01
updated: 2026-02-01
author: compass-research
summary: Enforceable observability and reliability requirements per tier, including logging standards, alert definitions, and health check specifications
tags: [reliability, observability, logging, alerting, standard, monitoring, health-check]
related:
  - DD-16-01
  - STD-14-01
  - DD-17-01
companion: DD-16-01
enforcement: Pre-launch review and periodic audits
---

# Reliability and Observability Standard

## Document Purpose

This document specifies enforceable observability and reliability requirements for each reliability tier. It translates the tier definitions from DD-16-01 into concrete, verifiable standards that can be checked during development and audited in production.

**How to use this document**:
1. Determine your tool's reliability tier using DD-16-01
2. Use the tier-specific checklist in Part 1 to verify compliance
3. Implement logging following Part 2 specifications
4. Configure alerting following Part 3 definitions
5. Implement health checks following Part 4 specifications

**Enforcement**: Pre-launch review verifies these standards before production deployment. Periodic audits (quarterly for Tier 1-2, annually for Tier 3-4) verify continued compliance.

---

## Part 1: Tier-Specific Compliance Checklists

Each tier has specific requirements. Complete the relevant checklist before considering a tool ready for its intended reliability tier.

### 1.1 Tier 1: Broadcast-Critical Checklist

Tools used during live broadcasts where failure is visible to the audience.

#### Architecture & Redundancy
- [ ] No single point of failure in critical path identified and documented
- [ ] Redundant network paths available (or documented exception)
- [ ] Backup data source configured and tested
- [ ] Graceful degradation behavior documented (what shows when data is stale/unavailable)
- [ ] Manual override capability exists for automated functions
- [ ] Circuit breaker implemented for all external dependencies

#### Observability
- [ ] Structured logging implemented (JSON format, all required fields)
- [ ] Comprehensive health check endpoint at `/health` (verifies all dependencies)
- [ ] Error rate metrics collected and exposed
- [ ] Latency metrics (P50, P95, P99) collected
- [ ] Custom monitoring dashboard created
- [ ] Request correlation IDs passed through all components
- [ ] Log retention configured for 90+ days

#### Alerting
- [ ] Critical alerts configured for: health check failure, error rate spike, latency degradation
- [ ] Alert routing verified to reach on-call person within 1 minute
- [ ] Alert thresholds tuned based on baseline (not default values)
- [ ] Alerting tested with simulated failures

#### Backup & Recovery
- [ ] Backup frequency < 1 hour (or continuous)
- [ ] Backup retention configured for 30+ days
- [ ] Point-in-time recovery capability verified
- [ ] Recovery runbook documented and tested
- [ ] Recovery drill completed within last quarter

#### Incident Response
- [ ] On-call schedule defined for all broadcast windows
- [ ] On-call contact information current and accessible
- [ ] Escalation path documented with contact information
- [ ] Post-incident review process defined

#### Pre-Broadcast
- [ ] Pre-broadcast verification checklist documented
- [ ] Verification procedure covers: data freshness, connectivity, system state
- [ ] Rollback procedure documented and tested

---

### 1.2 Tier 2: Business-Critical Checklist

Tools essential for content creation where failure blocks work.

#### Architecture
- [ ] Graceful degradation behavior defined (even if "retry later")
- [ ] Idempotent operations for all retryable processes
- [ ] Circuit breaker implemented for external dependencies
- [ ] Work queuing handles temporary unavailability

#### Observability
- [ ] Structured logging implemented (JSON format, required fields)
- [ ] Health check endpoint at `/health`
- [ ] Error rate metrics collected with alerting
- [ ] Latency metrics (P50, P95) collected
- [ ] Request correlation IDs implemented
- [ ] Log retention configured for 30+ days

#### Alerting
- [ ] Alerts configured for: health check failure, error rate above threshold
- [ ] Alert routing reaches responsible person within 30 minutes
- [ ] Alert thresholds documented

#### Backup & Recovery
- [ ] Daily backup configured
- [ ] Backup retention configured for 14+ days
- [ ] Recovery procedure documented
- [ ] Recovery tested within last year

#### Incident Response
- [ ] Business hours escalation path defined
- [ ] Contact information for responsible person documented

---

### 1.3 Tier 3: Business-Important Checklist

Tools that delay publication but have manual workarounds.

#### Architecture
- [ ] Input validation implemented
- [ ] Error messages are user-actionable (not raw stack traces)
- [ ] Rate limiting implemented if API is exposed

#### Observability
- [ ] Logging implemented (structured preferred)
- [ ] Health check endpoint at `/health`
- [ ] Error rate tracked (alerting optional)
- [ ] Log retention configured for 14+ days

#### Alerting
- [ ] Alerts configured for repeated failures
- [ ] Alert routing reaches someone within 2 hours

#### Backup & Recovery
- [ ] Daily backup configured
- [ ] Recovery procedure documented (informal acceptable)
- [ ] Manual fallback procedure documented and known to users

---

### 1.4 Tier 4: Internal Standard Checklist

Tools supporting internal operations with minimal availability requirements.

#### Basic Operation
- [ ] Error messages understandable to users
- [ ] Recovery procedure exists (informal acceptable)
- [ ] Issue reporting path clear to users

#### Minimal Observability
- [ ] Logging captures errors with context
- [ ] Health check recommended but not required
- [ ] Log retention 7+ days

#### Graduation Monitoring
- [ ] Is this tool blocking if unavailable? (If yes → review tier)
- [ ] Are 5+ people depending on this? (If yes → document properly)
- [ ] Has this existed 6+ months? (If yes → review for compliance)

---

### 1.5 Tier 5: Best Effort Checklist

Experimental tools where failure is acceptable.

#### Experiment Governance
- [ ] Clearly labeled as experimental/prototype
- [ ] Not connected to production data without explicit approval
- [ ] Time box established (graduation or retirement date)
- [ ] Success/failure criteria defined

No observability, backup, or alerting requirements for Tier 5.

---

## Part 2: Logging Standards

All production tools (Tier 1-4) must implement structured logging. This section specifies the format and required fields.

### 2.1 Log Entry Schema

Every log entry must be a valid JSON object with the following structure:

```json
{
  "timestamp": "2026-02-01T14:32:00.123Z",
  "level": "INFO",
  "service": "compass-api",
  "message": "Planning session created",
  "correlation_id": "req_abc123xyz",
  "context": {
    "user_id": "user_456",
    "project_id": "proj_789",
    "session_id": "sess_012"
  },
  "metadata": {
    "duration_ms": 145,
    "operation": "create_session"
  }
}
```

### 2.2 Required Fields (All Tiers)

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `timestamp` | ISO 8601 string | When the event occurred, UTC | `"2026-02-01T14:32:00.123Z"` |
| `level` | string | Severity level | `"DEBUG"`, `"INFO"`, `"WARN"`, `"ERROR"` |
| `service` | string | Which service/component | `"compass-api"`, `"artifact-sync"` |
| `message` | string | Human-readable description | `"Planning session created"` |

### 2.3 Required Fields (Tier 1-2)

In addition to base fields:

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `correlation_id` | string | Request trace identifier | `"req_abc123xyz"` |
| `context` | object | Relevant entity IDs | `{"user_id": "...", "project_id": "..."}` |

### 2.4 Recommended Fields (All Tiers)

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `metadata.duration_ms` | number | Operation duration | `145` |
| `metadata.operation` | string | What was being done | `"create_session"` |
| `error.code` | string | Machine-readable error code | `"RESOURCE_NOT_FOUND"` |
| `error.stack` | string | Stack trace (DEBUG level only) | `"Error: ..."` |

### 2.5 Log Level Definitions

Use these definitions consistently across all tools:

| Level | When to Use | Alerting |
|-------|-------------|----------|
| **DEBUG** | Detailed diagnostic information useful during development. Not enabled in production by default. | Never |
| **INFO** | Normal operations: requests received, processes completed, state changes. The baseline for understanding system behavior. | Never |
| **WARN** | Something unexpected that didn't cause failure: retry succeeded, fallback used, deprecated feature accessed. Investigate if frequent. | Threshold-based |
| **ERROR** | Something failed that needs attention: request could not be completed, dependency unavailable, data validation failed. | Always (Tier 1-2) |

### 2.6 What to Log

**Always log**:
- Entry and exit of significant operations (with duration)
- All errors with sufficient context to understand what happened
- External service calls (what was called, success/failure, duration)
- Authentication events (login, logout, failed attempts)
- Authorization failures (user tried to access something they shouldn't)

**Never log**:
- Credentials, API keys, or tokens (even partially)
- Passwords or password hashes
- Sensitive personal data (SSN, credit card numbers)
- Full request bodies containing user content (log IDs instead)
- Health check requests (too noisy; log only failures)

### 2.7 Log Retention by Tier

| Tier | Minimum Retention | Rationale |
|------|-------------------|-----------|
| Tier 1 | 90 days | Supports quarterly incident reviews and pattern analysis |
| Tier 2 | 30 days | Covers typical investigation windows |
| Tier 3 | 14 days | Balances storage cost with debugging needs |
| Tier 4 | 7 days | Minimal retention for basic troubleshooting |
| Tier 5 | Not required | Experiments don't warrant log storage costs |

---

## Part 3: Alert Definitions

Alerts notify humans when automated systems detect problems. This section defines alert severity levels and standard alert configurations.

### 3.1 Alert Severity Levels

| Severity | Response Time | When to Use | Example |
|----------|---------------|-------------|---------|
| **CRITICAL** | Immediate (< 5 min) | Production is down or severely degraded; users cannot work | Health check failing, error rate > 50% |
| **HIGH** | Soon (< 30 min) | Significant degradation; some users affected or approaching critical | Error rate > 10%, latency > 5x normal |
| **MEDIUM** | Business hours | Needs attention but not urgent; investigate when convenient | Error rate elevated, warnings increasing |
| **LOW** | When available | Informational; trend to watch | Approaching resource limits, deprecation warnings |

### 3.2 Standard Alert Configurations by Tier

#### Tier 1 Alert Requirements

| Alert | Severity | Trigger | Notification |
|-------|----------|---------|--------------|
| Health check failure | CRITICAL | `/health` returns non-200 for 30 seconds | Immediate page/SMS |
| Error rate spike | CRITICAL | Error rate > 5% for 2 minutes | Immediate page/SMS |
| Latency degradation | HIGH | P95 latency > 3x baseline for 5 minutes | Slack/email |
| Dependency failure | HIGH | External dependency unreachable for 1 minute | Slack/email |
| Recovery notification | INFO | System recovered from CRITICAL state | Slack |

#### Tier 2 Alert Requirements

| Alert | Severity | Trigger | Notification |
|-------|----------|---------|--------------|
| Health check failure | HIGH | `/health` returns non-200 for 2 minutes | Slack/email |
| Error rate spike | HIGH | Error rate > 10% for 5 minutes | Slack/email |
| Extended outage | CRITICAL | Unavailable for 15+ minutes | Page (if business hours) |
| Queue backup | MEDIUM | Work queue depth > normal for 30 minutes | Slack |

#### Tier 3 Alert Requirements

| Alert | Severity | Trigger | Notification |
|-------|----------|---------|--------------|
| Repeated failures | MEDIUM | Same error 10+ times in 1 hour | Email |
| Health check failure | MEDIUM | `/health` returns non-200 for 30 minutes | Email |

#### Tier 4 Recommendations

Alerting optional but recommended:
- Consider email notification for errors affecting multiple users
- Dashboard visibility into error rates is sufficient for most Tier 4 tools

### 3.3 Alert Best Practices

**Avoid alert fatigue**: An alert that fires constantly and gets ignored is worse than no alert. Tune thresholds based on actual baseline behavior, not theoretical ideals.

**Include actionable information**: Alert messages should help the responder understand what to do, not just what happened. Good: "Error rate 15% on compass-api. Runbook: [link]. Recent deploy: [yes/no]." Bad: "Error rate threshold exceeded."

**Test alerts**: Deliberately trigger alert conditions during setup to verify routing works. An untested alert is a theoretical alert.

**Review alert effectiveness**: Quarterly for Tier 1-2, annually for Tier 3-4, review which alerts fired and whether they led to useful action. Retire alerts that only generate noise.

### 3.4 Alert Routing Configuration

| Tier | Business Hours | After Hours |
|------|----------------|-------------|
| Tier 1 | Page/SMS to on-call | Page/SMS to on-call |
| Tier 2 | Slack + email to team | Slack (reviewed next day) |
| Tier 3 | Email to owner | Email (reviewed next day) |
| Tier 4 | Email optional | None |

---

## Part 4: Health Check Specifications

Health checks allow monitoring systems to verify service availability. This section specifies health check endpoint requirements.

### 4.1 Health Check Endpoint Requirements

All Tier 1-3 tools must expose a health check endpoint at `/health` that:

1. Returns HTTP 200 when the service is healthy
2. Returns HTTP 503 when the service is unhealthy
3. Responds within 5 seconds (timeout indicates unhealthy)
4. Does not require authentication
5. Is lightweight (does not perform expensive operations)

### 4.2 Health Check Response Schema

```json
{
  "status": "healthy",
  "timestamp": "2026-02-01T14:32:00Z",
  "version": "1.2.3",
  "checks": {
    "database": {
      "status": "healthy",
      "latency_ms": 12
    },
    "cache": {
      "status": "healthy",
      "latency_ms": 2
    },
    "llm_api": {
      "status": "degraded",
      "latency_ms": 2500,
      "message": "Response time elevated"
    }
  }
}
```

### 4.3 Status Values

| Status | HTTP Code | Meaning |
|--------|-----------|---------|
| `healthy` | 200 | All checks pass; service fully operational |
| `degraded` | 200 | Some non-critical checks failing; service operational with limitations |
| `unhealthy` | 503 | Critical checks failing; service not operational |

**When to return `degraded` vs `unhealthy`**: Return `unhealthy` only when the service cannot perform its core function. If a secondary feature (like analytics) is unavailable but core function works, return `degraded`.

### 4.4 Dependency Check Requirements by Tier

| Tier | Database | Cache | External APIs | LLM Provider |
|------|----------|-------|---------------|--------------|
| Tier 1 | Required | Required | Required | Required |
| Tier 2 | Required | Recommended | Recommended | Recommended |
| Tier 3 | Recommended | Optional | Optional | Optional |
| Tier 4 | Optional | Optional | Optional | Optional |

"Required" means the health check must verify this dependency is reachable. "Recommended" means include if the dependency is critical to the tool's function.

### 4.5 Health Check Implementation Guidelines

**Keep checks lightweight**: The health check itself should not cause load. Query a simple status, don't run full operations.

**Cache dependency checks**: For external dependencies, cache check results for 30-60 seconds. Don't hit external APIs on every health check request.

**Include version information**: The version field helps correlate health issues with deployments.

**Don't authenticate health checks**: Monitoring systems need to check health without credentials. If the health endpoint is only accessible internally, that's acceptable—but it should not require application-level authentication.

### 4.6 Startup and Shutdown Health

During startup:
- Return `unhealthy` until the service is ready to handle requests
- Don't accept traffic until health check returns `healthy`

During shutdown:
- Return `unhealthy` immediately when shutdown begins
- Allow in-flight requests to complete before stopping

This enables load balancers to route traffic correctly during deployments.

---

## Part 5: Incident Response Procedures

This section defines standard incident response procedures that tools should implement based on their tier.

### 5.1 Incident Severity Classification

| Severity | Definition | Example |
|----------|------------|---------|
| **SEV-1** | Complete outage of Tier 1 tool during broadcast, or data loss | Broadcast graphics unavailable during live show |
| **SEV-2** | Complete outage of Tier 2 tool, or significant degradation of Tier 1 | Compass unavailable for 30+ minutes |
| **SEV-3** | Complete outage of Tier 3 tool, or partial degradation of Tier 2 | Article companion generator down |
| **SEV-4** | Any Tier 4 issue, or minor issues in Tier 3 | File converter returns errors |

### 5.2 Response Time Targets

| Severity | Detection | Initial Response | Resolution |
|----------|-----------|------------------|------------|
| SEV-1 | < 1 minute | < 5 minutes | As fast as possible |
| SEV-2 | < 5 minutes | < 30 minutes | < 1 hour |
| SEV-3 | < 30 minutes | < 2 hours | < 4 hours |
| SEV-4 | < 4 hours | < 8 hours | < 24 hours |

### 5.3 Incident Communication Template

For SEV-1 and SEV-2 incidents, communicate status using this template:

**Initial notification** (within response time target):
```
[INCIDENT] [Service name] - [Brief description]
Status: Investigating
Impact: [Who/what is affected]
Next update: [Time]
```

**Update template** (every 30 minutes for SEV-1, every hour for SEV-2):
```
[UPDATE] [Service name] - [Brief description]
Status: [Investigating | Identified | Fixing | Monitoring]
Current state: [What's happening now]
Next steps: [What we're doing]
Next update: [Time]
```

**Resolution notification**:
```
[RESOLVED] [Service name] - [Brief description]
Duration: [How long the incident lasted]
Resolution: [What fixed it]
Follow-up: [Post-incident review scheduled for X]
```

### 5.4 Post-Incident Review Requirements

| Tier | Review Required | Timeline | Participants |
|------|-----------------|----------|--------------|
| Tier 1 | All incidents | Within 48 hours | All involved + stakeholders |
| Tier 2 | Incidents > 1 hour | Within 1 week | All involved |
| Tier 3 | Optional | Within 2 weeks | Owner |
| Tier 4 | Not required | N/A | N/A |

### 5.5 Post-Incident Review Template

```markdown
# Post-Incident Review: [Service] - [Date]

## Summary
[1-2 sentence description of what happened]

## Timeline
- [Time]: [Event]
- [Time]: [Event]
- [Time]: [Incident detected]
- [Time]: [Response began]
- [Time]: [Resolution]

## Impact
- Duration: [X hours/minutes]
- Users affected: [Description]
- Data loss: [Yes/No, details if yes]

## Root Cause
[What actually caused the incident]

## Contributing Factors
- [Factor 1]
- [Factor 2]

## What Went Well
- [Thing 1]
- [Thing 2]

## What Could Improve
- [Thing 1]
- [Thing 2]

## Action Items
- [ ] [Action] - [Owner] - [Due date]
- [ ] [Action] - [Owner] - [Due date]
```

---

## Part 6: Compliance Verification

This section defines how compliance with this standard is verified.

### 6.1 Pre-Launch Verification

Before any tool is deployed to production, verify compliance with its tier checklist (Part 1). Verification involves:

1. **Documentation review**: Confirm required documentation exists (runbooks, fallback procedures)
2. **Technical verification**: Confirm health endpoints work, logging format is correct, alerts are configured
3. **Test execution**: For Tier 1-2, execute recovery procedure in test environment

**Who verifies**: Tool owner + one reviewer (can be any other builder)

**Output**: Completed checklist stored with project documentation

### 6.2 Periodic Audit Schedule

| Tier | Audit Frequency | Scope |
|------|-----------------|-------|
| Tier 1 | Quarterly | Full checklist + recovery drill |
| Tier 2 | Quarterly | Full checklist |
| Tier 3 | Annually | Checklist review |
| Tier 4 | Annually | Graduation criteria check |
| Tier 5 | At time box expiry | Graduate or retire decision |

### 6.3 Audit Findings Classification

| Finding | Definition | Required Action |
|---------|------------|-----------------|
| **Critical** | Non-compliance with security or Tier 1 safety requirement | Immediate remediation; consider taking tool offline |
| **Major** | Non-compliance with tier-required item | Remediation within 2 weeks |
| **Minor** | Non-compliance with recommended item | Track for next audit cycle |
| **Observation** | Improvement opportunity | No required action |

### 6.4 Compliance Exceptions

If a tool cannot meet a specific requirement, document an exception:

```yaml
exception:
  tool: compass-api
  requirement: "Circuit breaker for all external dependencies"
  reason: "LLM provider circuit breaker causes user confusion; prefer visible errors"
  mitigation: "Enhanced timeout handling and user messaging instead"
  approved_by: [name]
  approved_date: 2026-02-01
  review_date: 2026-05-01
```

Exceptions must be:
- Documented with rationale
- Approved by tool owner and one other builder
- Reviewed at each audit cycle
- Not used for core safety requirements (Tier 1 redundancy, data encryption)

---

## Appendix A: Quick Reference Cards

### Logging Quick Reference

```
Required fields (all tiers):
  - timestamp (ISO 8601, UTC)
  - level (DEBUG/INFO/WARN/ERROR)
  - service (component name)
  - message (human-readable)

Required fields (Tier 1-2):
  - correlation_id (request trace)
  - context (entity IDs)

Never log:
  - Credentials, tokens, API keys
  - Passwords
  - Sensitive personal data
```

### Alert Quick Reference

```
CRITICAL: Page immediately, < 5 min response
HIGH: Slack/email, < 30 min response
MEDIUM: Email, business hours response
LOW: Dashboard, review when convenient

Tier 1: CRITICAL for health/errors
Tier 2: HIGH for health/errors
Tier 3: MEDIUM for repeated failures
```

### Health Check Quick Reference

```
Endpoint: /health
Methods: GET
Auth: None required

200 = healthy or degraded (operational)
503 = unhealthy (not operational)

Response time: < 5 seconds
Include: status, timestamp, version, dependency checks
```

---

## Appendix B: Implementation Examples

### Example: Structured Log Entry (TypeScript)

```typescript
function log(
  level: 'DEBUG' | 'INFO' | 'WARN' | 'ERROR',
  message: string,
  context?: {
    correlationId?: string;
    userId?: string;
    projectId?: string;
    operation?: string;
    durationMs?: number;
    error?: { code: string; message: string };
  }
) {
  console.log(JSON.stringify({
    timestamp: new Date().toISOString(),
    level,
    service: process.env.SERVICE_NAME || 'unknown',
    message,
    correlation_id: context?.correlationId,
    context: {
      user_id: context?.userId,
      project_id: context?.projectId,
    },
    metadata: {
      operation: context?.operation,
      duration_ms: context?.durationMs,
    },
    error: context?.error,
  }));
}
```

### Example: Health Check Endpoint (Convex HTTP Action)

```typescript
import { httpAction } from "./_generated/server";

export const health = httpAction(async (ctx) => {
  const start = Date.now();
  const checks: Record<string, { status: string; latency_ms?: number; message?: string }> = {};
  
  // Check database
  try {
    const dbStart = Date.now();
    await ctx.runQuery(api.health.ping);
    checks.database = { status: 'healthy', latency_ms: Date.now() - dbStart };
  } catch (e) {
    checks.database = { status: 'unhealthy', message: String(e) };
  }
  
  // Determine overall status
  const unhealthy = Object.values(checks).some(c => c.status === 'unhealthy');
  const status = unhealthy ? 'unhealthy' : 'healthy';
  
  return new Response(JSON.stringify({
    status,
    timestamp: new Date().toISOString(),
    version: process.env.VERSION || 'unknown',
    checks,
  }), {
    status: unhealthy ? 503 : 200,
    headers: { 'Content-Type': 'application/json' },
  });
});
```

---

## Appendix C: Related Documents

- **DD-16-01**: Companion definition document with tier rationale and assignment criteria
- **DD-14-01**: EFN Ecosystem Requirements (archetype definitions)
- **STD-14-01**: EFN Shared Standards (broader compliance requirements)
- **DD-17-01**: Integration Patterns (error handling, retry, logging details)
- **Compass System Definition**: Authoritative system specification

---

*End of Reliability and Observability Standard (STD-16-01)*
