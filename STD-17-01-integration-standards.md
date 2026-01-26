---
id: STD-17-01
type: standard
area: 17-integration-patterns
title: Integration Standards
status: draft
created: 2026-01-25
updated: 2026-01-25
author: compass-research
summary: Specifies integration compliance requirements for secret management, error logging, and pre-deployment verification
tags: [integration, standards, secrets, errors, compliance]
related:
  - DD-17-01
  - DD-14-01
  - STD-14-01
companion: DD-17-01
enforcement: Code review and integration testing
---

# Integration Standards

## Document Purpose

This document provides enforceable standards and compliance checklists for Compass integrations. It is the actionable companion to DD-17-01 (Integration Architecture Patterns).

**How to use this document**:
1. When building a new integration, review DD-17-01 for patterns and rationale
2. Use the checklists in this document before deploying any integration
3. Reference specific rules during code review
4. Use the quick reference card for common decisions

---

## Part 1: Secret Management Rules

These rules are non-negotiable. Violations create security vulnerabilities that are difficult to detect and expensive to remediate.

### 1.1 Storage Rules

**MUST**: Store all secrets in environment variables or a dedicated secrets manager (Convex env vars, Doppler, or Infisical).

**MUST**: Include `.env` in `.gitignore` before adding any environment file to the project.

**MUST**: Create `.env.example` documenting all required environment variables with placeholder values, not real secrets.

**MUST NOT**: Commit secrets to Git under any circumstances, including private repositories.

**MUST NOT**: Store secrets in code, comments, configuration files, or documentation.

**MUST NOT**: Use the same secrets for development and production environments.

### 1.2 Transmission Rules

**MUST NOT**: Share secrets via Slack, email, Discord, or other chat platforms.

**MUST**: Use a secrets manager's secure sharing features or transmit secrets in person when onboarding team members.

**MUST NOT**: Include secrets in URLs, query parameters, or request bodies that might be logged.

### 1.3 Logging Rules

**MUST NOT**: Log secrets, even partially masked (e.g., "API key: sk-abc***" is not acceptable).

**MUST NOT**: Log request bodies that may contain credentials or tokens.

**MUST**: Sanitize error messages before logging to remove any embedded credentials.

### 1.4 Access Control Rules

**MUST**: Enable MFA on all accounts with access to production secrets (Convex dashboard, secrets manager, cloud accounts).

**MUST**: Rotate secrets when team members with access leave the organization.

**MUST**: Maintain a record of which team members have access to which secrets.

### 1.5 Rotation Rules

**MUST**: Rotate secrets immediately upon suspected compromise.

**MUST**: Rotate secrets when team members with access depart.

**SHOULD**: Rotate high-value credentials (primary API keys) annually.

---

## Part 2: Required Error Logging Fields

Every integration error logged to the system must include these fields. This ensures consistent debugging capability across all integrations.

### 2.1 Mandatory Fields

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | ISO 8601 string | When the error occurred, in UTC |
| `level` | enum | `ERROR` for failures, `WARN` for transient issues |
| `service` | string | The external service name (e.g., `linear`, `openai`) |
| `operation` | string | What was being attempted (e.g., `create_task`) |
| `request_id` | string | Unique identifier for this request |

### 2.2 Required for Retryable Operations

| Field | Type | Description |
|-------|------|-------------|
| `idempotency_key` | string | The idempotency key if applicable |
| `retry_attempt` | number | Which retry attempt (0 for first try) |
| `max_retries` | number | Maximum retries configured |

### 2.3 Required for HTTP Errors

| Field | Type | Description |
|-------|------|-------------|
| `status_code` | number | HTTP status code received |
| `error_code` | string | API-specific error code if available |
| `duration_ms` | number | Request duration in milliseconds |

### 2.4 Optional but Recommended

| Field | Type | Description |
|-------|------|-------------|
| `correlation_id` | string | ID linking related operations |
| `user_id` | string | User who initiated the operation |
| `rate_limit_remaining` | number | Remaining API quota if available |

### 2.5 Prohibited Fields

Never include in error logs:
- API keys, tokens, or credentials
- Full request bodies containing user content
- PII (personally identifiable information)
- OAuth tokens or refresh tokens

---

## Part 3: Integration Compliance Checklist

Complete this checklist before deploying any new integration or significant changes to an existing integration.

### 3.1 Pre-Development Checklist

Before writing integration code:

- [ ] Integration type identified (output-only, bidirectional, input-only)
- [ ] External API documentation reviewed and understood
- [ ] Rate limits documented and understood
- [ ] Authentication method confirmed (API key, OAuth, webhook secret)
- [ ] Required secrets identified and documented in `.env.example`

### 3.2 Secret Management Checklist

Before using any credentials:

- [ ] Secrets stored in environment variables, not in code
- [ ] `.env` is in `.gitignore`
- [ ] `.env.example` created with all required variables (placeholder values only)
- [ ] Development and production use different credentials
- [ ] MFA enabled on accounts with secret access

### 3.3 Error Handling Checklist

Before considering error handling complete:

- [ ] All HTTP errors are caught and classified (transient/permanent/user-actionable)
- [ ] Error logs include all mandatory fields from Part 2
- [ ] User-facing error messages are specific, actionable, and non-technical
- [ ] No secrets or sensitive data appear in logs
- [ ] Escalation path defined for failed operations

### 3.4 Retry Logic Checklist

Before enabling retries:

- [ ] Idempotency keys generated for all state-changing operations
- [ ] Exponential backoff implemented with jitter
- [ ] Max retry count appropriate for operation type (see DD-17-01 §3.3)
- [ ] Permanent errors (4xx) do not trigger retries
- [ ] Dead letter queue captures operations that exhaust retries

### 3.5 Rate Limit Handling Checklist

Before calling rate-limited APIs:

- [ ] 429 responses detected and handled appropriately
- [ ] Retry-After header honored when present
- [ ] X-RateLimit-Remaining tracked for proactive limiting (if available)
- [ ] Batch operations paced to stay within limits
- [ ] User notification implemented for rate-limited operations

### 3.6 Webhook Security Checklist (if receiving webhooks)

Before exposing webhook endpoints:

- [ ] Signature verification implemented using raw request body
- [ ] Webhook secret stored in environment variable
- [ ] Timestamp validation rejects webhooks older than 5 minutes
- [ ] Idempotent processing handles duplicate deliveries
- [ ] Endpoint returns 200 within 20 seconds (heavy work is async)

### 3.7 Testing Checklist

Before deployment:

- [ ] Unit tests cover success and failure cases
- [ ] Tests verify retry logic triggers on 5xx and 429
- [ ] Tests verify idempotent processing of duplicates
- [ ] Webhook tests verify signature validation (valid and invalid)
- [ ] Manual verification completed against real API (staging if available)

### 3.8 Documentation Checklist

Before considering integration complete:

- [ ] README documents the integration purpose and configuration
- [ ] Required environment variables documented in `.env.example`
- [ ] API rate limits and quotas documented
- [ ] Error codes and their meanings documented
- [ ] Runbook documents common issues and resolution steps

---

## Part 4: Quick Reference Card

### 4.1 When to Retry

| Response | Action |
|----------|--------|
| 2xx | Success, don't retry |
| 400, 401, 403, 404, 422 | Permanent error, don't retry |
| 429 | Rate limited, retry after Retry-After delay |
| 500, 502, 503, 504 | Server error, retry with backoff |
| Timeout | Retry with backoff (use idempotency key) |

### 4.2 Backoff Calculation

```
delay = random(0, min(max_delay, base_delay × 2^attempt))
```

Recommended values:
- `base_delay`: 1000ms
- `max_delay`: 30000ms (LLM), 60000ms (other)

### 4.3 Idempotency Key Decision

| Scenario | Key Generation |
|----------|----------------|
| New operation | `crypto.randomUUID()` |
| Detecting duplicates | `hash(user + operation + params)` |
| Expiration | 24 hours |

### 4.4 Webhook Verification Steps

1. Get raw body (before JSON parse)
2. Get signature from header
3. Compute HMAC-SHA256(body, secret)
4. Compare signatures (timing-safe)
5. Check timestamp ≤ 5 minutes old

### 4.5 Log Level Selection

| Situation | Level |
|-----------|-------|
| Operation succeeded | INFO |
| Transient failure, will retry | WARN |
| Permanent failure | ERROR |
| Dead letter queue entry | ERROR + alert |

---

## Part 5: Compliance Verification Points

Use these verification points to ensure standards are maintained over time.

### 5.1 New Integration Review

Before a new integration is deployed:

1. **Secrets Audit**: Verify no secrets in codebase (search for common patterns)
2. **Logging Audit**: Verify logs don't contain sensitive data
3. **Checklist Complete**: All items in Part 3 checked
4. **Test Coverage**: All required test cases passing

### 5.2 Periodic Review (Quarterly)

For integrations in production:

1. **Secret Hygiene**: Are any secrets older than 1 year?
2. **Error Patterns**: Are there recurring errors that indicate integration issues?
3. **Dead Letter Queue**: Are items being reviewed and resolved?
4. **Documentation Currency**: Does documentation match current behavior?

### 5.3 Post-Incident Review

After any integration failure:

1. **Root Cause**: What actually failed and why?
2. **Detection Time**: How long until we knew about it?
3. **Recovery Time**: How long until it was resolved?
4. **Checklist Gap**: Was there a standard we should have followed?
5. **Improvement**: What changes prevent recurrence?

---

## Appendix A: Environment Variable Template

Use this template for `.env.example`:

```bash
# Integration: Linear
# Required for: PM tool sync
# Get from: https://linear.app/settings/api
LINEAR_API_KEY=your_linear_api_key_here
LINEAR_WEBHOOK_SECRET=your_webhook_secret_here

# Integration: OpenAI
# Required for: LLM API calls
# Get from: https://platform.openai.com/api-keys
OPENAI_API_KEY=your_openai_api_key_here

# Integration: Anthropic
# Required for: LLM API calls
# Get from: https://console.anthropic.com/settings/keys
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Add additional integrations following this format:
# # Integration: [Name]
# # Required for: [Purpose]
# # Get from: [URL or instructions]
# VARIABLE_NAME=placeholder_value
```

---

## Appendix B: Standard Error Response Format

For user-facing integration errors, use this format:

```typescript
interface IntegrationError {
  code: string;          // Machine-readable: "LINEAR_PROJECT_NOT_FOUND"
  message: string;       // Human-readable: "The Linear project could not be found"
  suggestion: string;    // Actionable: "Check that the project ID is correct"
  retryable: boolean;    // Can this be retried?
  retryAfter?: number;   // Seconds until retry (if retryable)
}
```

---

## Appendix C: Common Integration Errors

| Error Code | Meaning | User Message |
|------------|---------|--------------|
| `AUTH_FAILED` | Invalid credentials | "Unable to authenticate. Please reconnect your account." |
| `RATE_LIMITED` | Hit API rate limit | "Processing paused temporarily. Will resume automatically." |
| `SERVICE_UNAVAILABLE` | External API down | "[Service] is temporarily unavailable. We'll retry automatically." |
| `NOT_FOUND` | Resource doesn't exist | "The requested [item] was not found. Please verify it exists." |
| `PERMISSION_DENIED` | Insufficient access | "You don't have permission to access this [resource]." |
| `INVALID_REQUEST` | Bad request data | "[Specific field] is invalid. [What's wrong and how to fix]." |

---

## Appendix D: Related Documents

- **DD-17-01**: The companion definition document with patterns and rationale
- **DD-14-01**: EFN Ecosystem Requirements (tool archetypes, reliability tiers)
- **STD-14-01**: EFN Shared Standards (logging, error handling, documentation)
- **RF-01-01**: Backend Platform Research (Convex capabilities)
- **Compass System Definition**: Authoritative specification (§3.6, §3.8, §4.2)

---

*End of Integration Standards (STD-17-01)*
