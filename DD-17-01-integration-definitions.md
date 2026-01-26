---
id: DD-17-01
type: definition
area: 17-integration-patterns
title: Integration Architecture Patterns
status: draft
created: 2026-01-25
updated: 2026-01-25
author: compass-research
summary: Defines standard patterns for external system integration including webhooks, retries, error handling, and secret management
tags: [integration, patterns, api, webhooks, reliability, secrets]
related:
  - RF-01-01
  - DD-14-01
  - STD-14-01
companion: STD-17-01
---

# Integration Architecture Patterns

## Document Purpose

This document defines standard patterns for how Compass connects to external systems. It covers webhooks, polling, retry strategies, error handling, rate limits, and secret management—everything needed to build reliable integrations that a small, non-traditional development team can maintain.

**Why this matters**: Compass must integrate with PM tools (Linear, Notion), research sources (web APIs, documentation), LLM providers, and implementation platforms. Without consistent patterns, each integration becomes a unique snowflake that's hard to debug and maintain. These patterns ensure reliability without requiring deep infrastructure expertise.

**Audience**: Builders implementing integrations, and LLM coding agents that will generate integration code.

**Key principle**: Simple patterns that will actually be followed beat theoretically optimal patterns that get bypassed after week two.

---

## Part 1: Integration Types and Patterns

Compass connects to external systems in four distinct ways, each with different reliability requirements and appropriate patterns.

### 1.1 Integration Type Overview

Based on the Compass System Definition (§3.6), external integrations fall into four categories:

| Integration Type | Direction | Examples | Pattern |
|-----------------|-----------|----------|---------|
| **Implementation Platforms** | Output-only | GitHub, coding agents | Push artifacts via API |
| **Project Management** | Bidirectional | Linear, Notion | Webhooks + API calls |
| **Research Sources** | Input-only | Web APIs, documentation | Polling + caching |
| **Authentication** | Identity only | SSO providers | Standard OAuth/SAML |

### 1.2 The Standard Integration Pattern

For most Compass integrations, use the **mutation → scheduled action** pattern. This separates the user's intent (captured immediately) from the external call (executed asynchronously with retries).

**Why this pattern exists**: External API calls can fail, be slow, or hit rate limits. If you call an external API directly from user-facing code, the user experiences every failure. By scheduling the external call, the user gets immediate feedback while the system handles failures in the background.

**How it works in Convex**:

```
User Action → Mutation (saves intent) → Scheduler → Action (calls external API)
                    ↓                                         ↓
              Returns immediately              Retries on failure, writes result
```

The mutation captures what the user wants to do (e.g., "sync this task to Linear") and stores it in the database with a "pending" status. The mutation then schedules an action to perform the actual external call. The action runs asynchronously, handles retries and errors, and updates the status when complete.

**When to use this pattern**: Any integration that calls an external API where failure should not block the user. This includes syncing with PM tools, sending handoff bundles to implementation platforms, and calling LLM APIs for non-interactive tasks.

**When NOT to use this pattern**: Interactive LLM responses where the user is waiting for a reply. For those, call the LLM directly from an action (not a mutation) and stream the response.

### 1.3 Webhooks vs Polling: When to Use Each

**Choose webhooks when**:
- The external service supports reliable webhooks with documented retry policies
- Real-time updates are genuinely needed (payment confirmations, task assignments)
- The service provides webhook signature verification

**Choose polling when**:
- Webhook support is inconsistent or undocumented
- You can tolerate 15-30 minute sync delays
- You're prototyping or validating an integration
- The service lacks webhook signature verification

**The practical reality**: Start with polling for new integrations. It's simpler to debug, requires no public endpoint security, and works with every API. Graduate to webhooks when polling frequency becomes a problem or real-time matters.

**Hybrid pattern**: For established integrations, use webhooks for time-critical events while running polling every 15-30 minutes as a catch-up mechanism. This provides real-time responsiveness with eventual consistency guarantees.

### 1.4 Pattern by Integration Type

| Type | Recommended Pattern | Rationale |
|------|---------------------|-----------|
| PM tools (Linear, Notion) | Start with polling, add webhooks for task changes | Webhook support varies; polling works everywhere |
| LLM APIs | Direct action calls with retry | Synchronous request-response; cache identical prompts |
| Research APIs | Polling + aggressive caching | Usually request-response only; cache heavily |
| Implementation handoff | Push via scheduled action | One-way; receiver controls timing |
| File storage | Webhooks for change notifications | Most providers support them well |

---

## Part 2: Idempotency Standard

Idempotency ensures that processing the same operation multiple times produces the same result as processing it once. This is critical when retries occur—you don't want to create duplicate Linear tasks or send duplicate LLM requests.

### 2.1 What Idempotency Means in Practice

An operation is idempotent if calling it once or calling it five times produces the same final state. For example, "set user status to 'active'" is idempotent (running it twice leaves user active), while "increment counter by 1" is not (running it twice adds 2).

**Why this matters for Compass**: Network requests fail. When they fail, you retry. If your operations aren't idempotent, retries create duplicates, corrupt state, or charge you twice for LLM calls.

### 2.2 Idempotency Key Generation

Every external API call that creates or modifies data should include an idempotency key. The key is a unique identifier for the operation that remains stable across retries.

**Simple approach (recommended for most cases)**: Generate a UUID when the operation is first initiated and pass it through the entire flow.

```
const idempotencyKey = crypto.randomUUID();
// Result: "4fa282fe-6f26-4f33-8a32-447c6d8a1953"
```

**Deterministic approach (for duplicate detection)**: Hash the operation parameters so identical requests produce identical keys.

```
const idempotencyKey = hash(userId + operation + JSON.stringify(params));
// Same parameters always produce the same key
```

Use the deterministic approach when you need to detect and prevent duplicate submissions (e.g., user submits the same form twice).

### 2.3 Idempotency Key Storage

Store idempotency keys in the database with:
- The key itself (indexed for fast lookup)
- The operation status: `pending`, `complete`, or `failed`
- The timestamp (for expiration)
- The result (so retries can return the cached response)

**Expiration**: Delete idempotency records after 24 hours. This matches industry standards (Stripe uses 24 hours) and prevents the table from growing indefinitely while still catching retries from transient failures.

### 2.4 Idempotency Flow

When processing an operation with an idempotency key:

1. **Check for existing**: Look up the key in the database
2. **If found and complete**: Return the cached result immediately
3. **If found and pending**: Either wait or return "in progress"
4. **If not found**: Create a new record with status "pending"
5. **Process the operation**: Call the external API
6. **Update status**: Mark as "complete" with result, or "failed" with error

**Critical rule**: Only cache successful responses (HTTP 2xx) and permanent errors (4xx). Never cache transient errors (5xx, timeouts)—the next retry might succeed.

---

## Part 3: Retry and Backoff Strategy

Retries handle transient failures—the kind that succeed if you just try again. But naive retries can overwhelm systems, so you need exponential backoff with jitter.

### 3.1 Exponential Backoff Explained

Exponential backoff increases the delay between retries exponentially: 1 second, then 2 seconds, then 4, then 8, and so on. This gives failing systems time to recover instead of hammering them with requests.

**The formula**:
```
delay = min(cap, base × 2^attempt)
```

Where:
- `base` is the initial delay (typically 1 second)
- `attempt` is the retry number (0, 1, 2, 3...)
- `cap` is the maximum delay (typically 30-60 seconds)

### 3.2 Why Jitter Matters

If multiple requests fail at the same time and all retry with the same exponential schedule, they'll retry at the same time—creating a "thundering herd" that overwhelms the system again.

Jitter randomizes the retry timing so requests spread out naturally. AWS research shows that **full jitter** (randomizing across the entire delay window) produces the best results.

**The formula with jitter**:
```
delay = random(0, min(cap, base × 2^attempt))
```

### 3.3 Retry Limits by Operation Type

Different operations warrant different retry strategies:

| Operation Type | Max Retries | Base Delay | Max Delay | Rationale |
|---------------|-------------|------------|-----------|-----------|
| LLM API calls | 3 | 1s | 30s | Expensive; fail fast |
| PM tool sync | 5 | 2s | 60s | Important but not urgent |
| Webhook delivery | 5-8 | 1min | 1hr | Standard webhook practice |
| File operations | 5 | 2s | 60s | May need time for processing |

### 3.4 When to Stop Retrying

Stop retrying immediately (no backoff needed) for:
- **Authentication errors** (401, 403): Retrying won't help; credentials are wrong
- **Validation errors** (400, 422): The request is malformed; fix it first
- **Not found errors** (404): The resource doesn't exist
- **Payment failures** (402): Requires human intervention

Continue retrying (with backoff) for:
- **Server errors** (500, 502, 503, 504): The server is having problems
- **Rate limits** (429): You're calling too fast; slow down
- **Timeouts**: The request might have succeeded; retry with idempotency

### 3.5 Dead Letter Queue Pattern

When an operation fails all retries, don't lose it—move it to a dead letter queue for manual review.

For Compass on Convex, use a database table as the dead letter queue:

| Field | Purpose |
|-------|---------|
| `operationType` | What was being attempted |
| `payload` | The original request parameters |
| `errorMessage` | The final error |
| `retryCount` | How many times we tried |
| `status` | `pending_review`, `resolved`, `abandoned` |
| `createdAt` | When it failed |

**Alert threshold**: Notify humans (Slack, email) when items land in the dead letter queue. Don't let them accumulate silently.

---

## Part 4: Rate Limit Handling

External APIs limit how many requests you can make in a given time period. Exceeding these limits results in errors (usually HTTP 429) and potentially temporary bans.

### 4.1 Detecting Rate Limits

APIs signal rate limits through:

**HTTP 429 Too Many Requests**: The standard rate limit response code. Always check for this.

**Retry-After header**: Tells you how long to wait (in seconds) or when to retry (as an HTTP date). Honor this value—don't retry sooner.

**X-RateLimit headers**: Many APIs include:
- `X-RateLimit-Limit`: Total allowed requests per window
- `X-RateLimit-Remaining`: Requests left in current window
- `X-RateLimit-Reset`: When the window resets (Unix timestamp)

### 4.2 Responding to Rate Limits

When you hit a rate limit:

1. **Check for Retry-After**: If present, wait that long
2. **Check for X-RateLimit-Reset**: Calculate time until reset
3. **Default fallback**: Wait 60 seconds

**Proactive rate limiting**: Track `X-RateLimit-Remaining` and slow down when approaching zero. For batch operations, pace requests to stay within limits rather than sprinting and waiting.

### 4.3 Rate Limit Budgeting

Before starting a batch operation, calculate whether you have capacity:

| You Need | API Allows | Strategy |
|----------|------------|----------|
| 50 calls | 100/minute | Execute normally |
| 200 calls | 100/minute | Pace at 100/min for 2 minutes |
| 1000 calls | 100/minute | Queue for background processing |

For LLM APIs specifically, rate limits are often per-minute and per-day. Track both. The per-day limit matters more for Compass since planning sessions are sporadic, not continuous.

### 4.4 User Communication

When rate limits affect user-visible operations:
- Show a clear message: "Processing paused temporarily. Will resume automatically."
- Include an estimate: "Resuming in approximately 45 seconds."
- Never show raw API errors like "429 Too Many Requests"

---

## Part 5: Error Handling Standards

Good error handling means users understand what went wrong and know what to do about it. It also means operators can debug issues quickly.

### 5.1 Error Classification

Classify every error into one of three categories that determine how to respond:

| Category | HTTP Codes | System Response | User Response |
|----------|------------|-----------------|---------------|
| **Transient** | 500, 502, 503, 504, 429 | Log warning, retry automatically | Show "trying again..." if visible |
| **Permanent** | 400, 401, 403, 404, 422 | Log error, stop retrying | Show specific error message |
| **User-actionable** | 400 (validation), 402, 409 | Log info, return to user | Explain what they need to fix |

### 5.2 Logging Requirements

Every integration error log must include these fields:

| Field | Purpose | Example |
|-------|---------|---------|
| `timestamp` | When it happened | `2026-01-25T14:32:00Z` |
| `request_id` | Trace across services | `req_abc123` |
| `idempotency_key` | Track retries | `4fa282fe-6f26...` |
| `service` | Which integration | `linear`, `openai` |
| `operation` | What was attempted | `create_task`, `chat_completion` |
| `status_code` | HTTP response code | `429` |
| `error_code` | API error code | `rate_limit_exceeded` |
| `retry_attempt` | Which retry (0-based) | `2` |
| `duration_ms` | How long it took | `1250` |

**What NOT to log**: Request bodies containing credentials, API keys, user content, or PII. Log enough to debug, not enough to leak.

### 5.3 User-Facing Error Messages

Error messages shown to users must be:
- **Specific**: "The Linear project 'PROJ-123' was not found" not "Not found"
- **Actionable**: "Check that the project ID is correct and try again"
- **Non-technical**: No stack traces, no HTTP codes, no raw API responses

**Pattern for user messages**:
```
[What went wrong] + [Why it might have happened] + [What to do next]

Example: "Unable to sync with Linear. The API is temporarily unavailable. 
This will retry automatically in a few minutes."
```

### 5.4 Escalation Path

Define clear escalation for when automated handling isn't enough:

| Condition | Automated Response | Human Escalation |
|-----------|-------------------|------------------|
| First 3 retries | Exponential backoff | None |
| Retries 4-5 | Continue backoff | Log warning |
| All retries exhausted | Move to dead letter queue | Slack notification |
| Dead letter queue > 5 items | N/A | Email alert |

---

## Part 6: Secret Management

Secrets are credentials that authenticate to external services: API keys, OAuth tokens, webhook signing keys. Mishandling secrets is the most common security mistake in small teams.

### 6.1 What Counts as a Secret

| Secret | Store Securely | Never Commit to Git |
|--------|---------------|---------------------|
| API keys | ✓ | ✓ |
| OAuth client secrets | ✓ | ✓ |
| Webhook signing keys | ✓ | ✓ |
| Database passwords | ✓ | ✓ |
| JWT signing keys | ✓ | ✓ |
| Encryption keys | ✓ | ✓ |
| Service account credentials | ✓ | ✓ |

**Not secrets** (but still don't commit): Environment-specific URLs, feature flags, non-sensitive configuration.

### 6.2 Secret Storage Approach

Convex provides built-in environment variable storage that's appropriate for Compass's needs:

**For Convex functions**: Use environment variables set via dashboard or CLI (`npx convex env set API_KEY=secret`). Variables are per-deployment, so development and production naturally have different values.

**For secrets beyond Convex**: If you need to manage secrets for other services or share them across tools, use a dedicated secrets manager:
- **Doppler** (free for ≤3 users): Simple, team-friendly, integrates with Vercel/Convex
- **Infisical** (open source option): Self-hostable if needed

**Avoid for small teams**: HashiCorp Vault (requires significant operational overhead).

### 6.3 Secret Handling Rules

**Never**:
- Commit secrets to Git (even in private repos—they persist in history)
- Share secrets via Slack, email, or other chat (no audit trail, persists in logs)
- Log secrets (even partially—no "API key: sk-abc***")
- Store secrets in code comments, even as examples
- Use the same secrets for development and production

**Always**:
- Use environment variables or a secrets manager
- Include `.env` in `.gitignore` before adding any secrets
- Create `.env.example` with placeholder values documenting required variables
- Enable MFA on any account that has access to secrets
- Rotate secrets when team members with access leave

### 6.4 Secret Rotation

For Compass's scale, manual rotation is appropriate:
- **When someone leaves**: Rotate any secrets they had access to
- **After suspected compromise**: Rotate immediately
- **Annually**: Rotate high-value credentials (main API keys) once a year

Automated 90-day rotation is enterprise checkbox compliance—it adds operational burden without proportionate security benefit for small teams.

### 6.5 Audit Logging for Secrets

Track access to secrets for debugging and security:
- When secrets are read (at function startup, not every use)
- When secrets are changed (via dashboard or CLI)
- By whom (user or service)

Convex dashboard provides audit logs for environment variable changes. For secrets in external managers, enable their audit logging features.

---

## Part 7: Webhook Security

When receiving webhooks from external services, you must verify they're authentic. Without verification, attackers can send fake webhooks to manipulate your system.

### 7.1 Webhook Verification Requirements

Every webhook endpoint must implement:

1. **Signature verification**: Validate the cryptographic signature included in webhook headers
2. **Timestamp validation**: Reject webhooks older than 5 minutes (prevents replay attacks)
3. **Idempotent processing**: Handle duplicate deliveries gracefully

### 7.2 Signature Verification Pattern

Most webhook providers use HMAC-SHA256 signatures. The pattern:

1. Get the raw request body (before JSON parsing)
2. Get the signature from headers (location varies by provider)
3. Compute HMAC-SHA256 of the body using your webhook secret
4. Compare computed signature to provided signature (timing-safe comparison)

**Critical detail**: You must verify against the raw body, not parsed JSON. JSON parsing can change formatting, breaking signature verification.

**Common header locations**:
| Provider | Header |
|----------|--------|
| Stripe | `stripe-signature` |
| Linear | `linear-signature` |
| GitHub | `x-hub-signature-256` |
| Generic | `x-webhook-signature` |

### 7.3 Timestamp Validation

Webhook signatures often include a timestamp. Reject webhooks where the timestamp is more than 5 minutes old. This prevents replay attacks where an attacker captures a legitimate webhook and resends it later.

The timestamp is usually embedded in the signature header or payload. Check provider documentation for the exact format.

### 7.4 Webhook Processing Pattern

Process webhooks quickly and asynchronously:

1. **Verify signature** (immediately): Return 400 if invalid
2. **Check idempotency**: Return 200 if already processed
3. **Store event**: Write to database with "pending" status
4. **Return 200**: Signal success to the sender
5. **Process asynchronously**: Handle the event in a scheduled function

**Why return quickly**: Webhook providers expect responses within 10-20 seconds. If you take longer, they'll mark delivery as failed and retry, creating duplicates.

---

## Part 8: Integration Testing

Testing integrations without hitting production APIs requires mocks and stubs. But the tests should still validate real behavior.

### 8.1 Testing Strategy

| Test Type | What It Validates | Uses Real APIs? |
|-----------|-------------------|-----------------|
| Unit tests | Logic, parsing, error handling | No (mocked) |
| Integration tests | End-to-end flow with mocks | No (mocked) |
| Smoke tests | Connection to real service | Yes (staging) |
| Manual verification | Full flow works | Yes (production) |

### 8.2 Mocking External APIs

For Convex testing with `convex-test`, mock the `fetch` function to simulate external API responses:

**Testing success cases**: Return the expected response shape so your code can process it correctly.

**Testing failure cases**: Return error status codes (429, 500) to verify retry logic works.

**Testing timeouts**: Make the mock delay or never resolve to verify timeout handling.

### 8.3 Testing Webhooks

Convex HTTP endpoints are publicly accessible even in development (at your `.convex.site` URL), so you can test real webhooks:

1. Use the external service's test/sandbox mode
2. Configure it to send webhooks to your development endpoint
3. Verify the events are received and processed correctly

For automated tests without real webhook delivery, call the HTTP endpoint directly with test payloads and verify the response and database state.

### 8.4 What to Test

Every integration should have tests for:
- Successful operation (happy path)
- Invalid input (validation errors)
- Transient failure and retry (5xx, timeout)
- Rate limit handling (429)
- Idempotent processing (duplicate requests)
- Webhook signature verification (valid and invalid)

---

## Appendix A: Glossary

**Dead letter queue**: A holding area for operations that failed all retries, awaiting manual review.

**Exponential backoff**: A retry strategy where delays increase exponentially (1s, 2s, 4s, 8s...) to give failing systems time to recover.

**HMAC-SHA256**: A cryptographic algorithm used to verify webhook authenticity by computing a signature from the message and a shared secret.

**Idempotency**: The property where an operation produces the same result whether executed once or multiple times.

**Idempotency key**: A unique identifier for an operation that remains stable across retries, enabling duplicate detection.

**Jitter**: Random variation added to retry delays to prevent multiple clients from retrying simultaneously.

**Polling**: Periodically checking an API for updates, as opposed to receiving push notifications via webhooks.

**Rate limit**: A restriction on how many API requests you can make in a given time period.

**Retry-After**: An HTTP header indicating how long to wait before retrying a failed request.

**Webhook**: An HTTP callback where an external service sends data to your endpoint when events occur, as opposed to you polling for updates.

---

## Appendix B: Convex Integration Primitives

Compass uses Convex as its backend. Here's how Convex's primitives map to integration patterns:

| Convex Primitive | Integration Use |
|-----------------|-----------------|
| **Mutations** | Capture user intent, store operation state |
| **Actions** | Call external APIs (can't be in mutations) |
| **HTTP Actions** | Receive webhooks at `.convex.site` endpoints |
| **Scheduled Functions** | Async processing, retries, background sync |
| **Environment Variables** | Store API keys and secrets |

**Key constraint**: Mutations are transactional and can't make external calls. Actions can make external calls but aren't transactional. This is why the mutation → scheduled action pattern exists.

---

## Appendix C: Sources

1. **[T1/S1]** Convex. "HTTP Actions Documentation." Retrieved 2026-01-25. https://docs.convex.dev/functions/http-actions

2. **[T1/S1]** Convex. "Actions Documentation." Retrieved 2026-01-25. https://docs.convex.dev/functions/actions

3. **[T1/S1]** Convex. "Scheduled Functions Documentation." Retrieved 2026-01-25. https://docs.convex.dev/scheduling/scheduled-functions

4. **[T1/S1]** Convex. "Environment Variables Documentation." Retrieved 2026-01-25. https://docs.convex.dev/production/environment-variables

5. **[T1/S1]** AWS. "Exponential Backoff And Jitter." Retrieved 2026-01-25. https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/

6. **[T2/S2]** Merge. "Polling vs Webhooks: When to Use One Over the Other." Retrieved 2026-01-25. https://www.merge.dev/blog/webhooks-vs-polling

7. **[T1/S1]** Convex. "convex-test Documentation." Retrieved 2026-01-25. https://docs.convex.dev/testing/convex-test

---

## Appendix D: Related Documents

- **STD-17-01**: The companion standard with enforceable requirements and checklists
- **RF-01-01**: Backend Platform Research (Convex selection and capabilities)
- **DD-14-01**: EFN Ecosystem Requirements (integration principles)
- **STD-14-01**: EFN Shared Standards (error handling, logging standards)
- **Compass System Definition**: Authoritative system specification (§3.6 External Integrations, §3.8 Reliability)

---

*End of Integration Architecture Patterns (DD-17-01)*
