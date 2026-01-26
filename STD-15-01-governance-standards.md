---
id: STD-15-01
type: standard
area: 15-governance
title: Governance and Audit Standards
status: draft
created: 2026-01-25
updated: 2026-01-25
author: compass-research
summary: Specifies audit log schema, event type enumeration, and governance compliance requirements for Compass
tags: [governance, audit, standards, logging, compliance]
related:
  - DD-15-01
  - DD-13-01
companion: DD-15-01
enforcement: System configuration and periodic review
---

# Governance and Audit Standards

## Document Purpose

This document provides enforceable standards for governance implementation in Compass. It is the actionable companion to DD-15-01 (Governance, Roles, Permissions, and Audit).

**How to use this document:**
1. When implementing audit logging, use the schema and event types specified here
2. When configuring permissions, use the verification checklist to ensure compliance
3. When reviewing governance, use the periodic review checklist

---

## Part 1: Audit Log Schema

### 1.1 Core Schema

Every audit log entry MUST contain these fields:

```json
{
  "id": "uuid-v4",
  "timestamp": "2026-01-25T14:30:00.000Z",
  "event_type": "artifact.approved",
  "actor": {
    "type": "user",
    "id": "user_abc123",
    "email": "jane@efn.com"
  },
  "sponsor": null,
  "project": {
    "id": "proj_xyz789",
    "name": "Broadcast Tools"
  },
  "resource": {
    "type": "artifact",
    "id": "SPEC-broadcast-001",
    "name": "Data Visualization Spec"
  },
  "action": "approved",
  "outcome": "success",
  "context": {},
  "client": {
    "ip_address": "10.0.1.42",
    "user_agent": "Mozilla/5.0..."
  }
}
```

### 1.2 Field Specifications

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | UUID v4 | Yes | Unique identifier for this log entry |
| `timestamp` | ISO 8601 | Yes | When the event occurred (UTC, millisecond precision) |
| `event_type` | String (enum) | Yes | Event type from §1.3 |
| `actor.type` | Enum | Yes | `user` or `agent` |
| `actor.id` | String | Yes | Unique identifier for the actor |
| `actor.email` | String | Yes (for users) | Email address (for human-readable attribution) |
| `sponsor` | Object | Conditional | Required when `actor.type` is `agent`; contains sponsoring user |
| `sponsor.id` | String | Yes (if sponsor) | User ID of sponsoring human |
| `sponsor.email` | String | Yes (if sponsor) | Email of sponsoring human |
| `project.id` | String | Conditional | Project ID if event is project-scoped |
| `project.name` | String | Conditional | Project name for readability |
| `resource.type` | String | Conditional | Type of resource affected |
| `resource.id` | String | Conditional | ID of resource affected |
| `resource.name` | String | Conditional | Human-readable resource name |
| `action` | String | Yes | What happened |
| `outcome` | Enum | Yes | `success`, `failure`, or `denied` |
| `context` | Object | Yes | Event-specific additional data (can be empty `{}`) |
| `client.ip_address` | String | Conditional | Required for authentication events |
| `client.user_agent` | String | No | Browser/client identifier |

### 1.3 Event Type Enumeration

Event types follow the pattern: `{domain}.{action}`.

#### Authentication Events

| Event Type | Description | Required Context |
|------------|-------------|------------------|
| `auth.login` | User logged in | `method` (sso, password, etc.) |
| `auth.logout` | User logged out | — |
| `auth.login_failed` | Authentication failed | `reason` |
| `auth.session_expired` | Session timed out | — |
| `auth.mfa_challenge` | MFA challenge issued | — |
| `auth.mfa_success` | MFA challenge passed | — |
| `auth.mfa_failed` | MFA challenge failed | — |

#### User Management Events

| Event Type | Description | Required Context |
|------------|-------------|------------------|
| `user.created` | New user account created | `role` |
| `user.role_changed` | User role modified | `from_role`, `to_role` |
| `user.disabled` | User account disabled | `reason` |
| `user.enabled` | User account re-enabled | — |
| `user.deleted` | User account deleted | — |
| `user.project_access_granted` | User given project access | `project_id` |
| `user.project_access_revoked` | User project access removed | `project_id` |

#### Artifact Events

| Event Type | Description | Required Context |
|------------|-------------|------------------|
| `artifact.created` | New artifact created | `artifact_type`, `status` |
| `artifact.edited` | Artifact content modified | `fields_changed` (array of field names) |
| `artifact.submitted` | Artifact submitted for review | — |
| `artifact.approved` | Artifact approved (draft → active) | — |
| `artifact.deprecated` | Artifact deprecated | `superseded_by` (if applicable) |
| `artifact.deleted` | Artifact deleted | — |

#### Branch Events

| Event Type | Description | Required Context |
|------------|-------------|------------------|
| `branch.created` | New branch created | `branch_type` (research, exploration, etc.) |
| `branch.merged` | Branch merged to canonical | `changes_summary` |
| `branch.merge_rejected` | Branch merge rejected | `reason` |
| `branch.archived` | Branch archived | — |

#### Project Events

| Event Type | Description | Required Context |
|------------|-------------|------------------|
| `project.created` | New project created | — |
| `project.archived` | Project archived | — |
| `project.deleted` | Project deleted | — |
| `project.settings_changed` | Project settings modified | `settings_changed` (array) |

#### Integration Events

| Event Type | Description | Required Context |
|------------|-------------|------------------|
| `integration.configured` | Integration added/modified | `integration_type`, `destination` |
| `integration.removed` | Integration removed | `integration_type` |
| `integration.invoked` | Integration executed | `integration_type`, `trigger` |
| `integration.failed` | Integration execution failed | `integration_type`, `error` |

#### Export Events

| Event Type | Description | Required Context |
|------------|-------------|------------------|
| `export.initiated` | Data export started | `format`, `scope` |
| `export.completed` | Data export finished | `format`, `record_count` |
| `export.failed` | Data export failed | `error` |

#### Agent Events

| Event Type | Description | Required Context |
|------------|-------------|------------------|
| `agent.action` | Agent performed an action | `agent_id`, `action_type`, `target` |
| `agent.rate_limited` | Agent hit rate limit | `agent_id`, `limit_type` |
| `agent.scope_violation` | Agent attempted out-of-scope action | `agent_id`, `attempted_action` |

---

## Part 2: Minimum Logging Requirements

### 2.1 Events That MUST Be Logged

The following events MUST always be logged, regardless of configuration:

#### Security-Critical (Non-Negotiable)

- `auth.login` — All successful logins
- `auth.login_failed` — All failed login attempts
- `user.role_changed` — All permission changes
- `user.project_access_granted` — All access grants
- `user.project_access_revoked` — All access revocations
- `integration.configured` — All integration changes
- `export.initiated` — All data exports

#### Audit-Critical (Required for Accountability)

- `artifact.created` — All artifact creation
- `artifact.approved` — All artifact approvals
- `artifact.deprecated` — All deprecations
- `artifact.deleted` — All deletions
- `branch.merged` — All branch merges
- `branch.merge_rejected` — All merge rejections
- `project.deleted` — All project deletions

### 2.2 Events That SHOULD Be Logged

These events should be logged in production but may be disabled in development:

- `artifact.edited` — Content changes (without diff)
- `branch.created` — Branch creation
- `branch.archived` — Branch archival
- `project.created` — Project creation
- `agent.action` — Agent actions

### 2.3 Events That MAY Be Logged

Optional logging for debugging or enhanced audit trails:

- `auth.logout` — Logout events
- `auth.session_expired` — Session timeouts
- `project.settings_changed` — Settings modifications
- `integration.invoked` — Integration executions

### 2.4 Events That MUST NOT Be Logged

Never log these for privacy and noise reasons:

- View/read operations (except exports)
- Search queries (content privacy)
- Chat messages that don't result in artifacts
- Draft content before save
- Partial input (keystrokes, partial forms)

---

## Part 3: Permission Verification Checklist

Use this checklist when configuring or auditing permission settings.

### 3.1 Role Configuration Checklist

For each role, verify:

#### Owner Role

- [ ] Exactly 1–2 accounts have Owner role (not more)
- [ ] Owner accounts have strong authentication (MFA enabled if available)
- [ ] Owner accounts are assigned to real, accountable humans (not shared accounts)
- [ ] Owner permissions include all administrative functions

#### Planner Role

- [ ] Only intended primary users have Planner role
- [ ] Planners are assigned to appropriate projects (not all projects by default)
- [ ] Planners cannot access user management functions
- [ ] Planners cannot access integration configuration
- [ ] Planners can access audit logs for their projects

#### Contributor Role

- [ ] Contributors cannot approve artifacts
- [ ] Contributors cannot merge branches
- [ ] Contributors can only edit artifacts they created while in draft status
- [ ] Contributors are assigned to specific projects (limited scope)

#### Viewer Role

- [ ] Viewers have read-only access (no create, edit, delete)
- [ ] Viewers are assigned to specific projects (limited scope)
- [ ] Viewers cannot access audit logs
- [ ] Viewers can view artifact history (for context)

### 3.2 Project Access Checklist

For each project, verify:

- [ ] At least one Planner is assigned
- [ ] Users have minimum necessary access (not broader than needed)
- [ ] No orphaned access (users who left team still have access)
- [ ] Sensitive projects have restricted access (not all users)

### 3.3 Agent Configuration Checklist

For each agent:

- [ ] Agent has a designated sponsor (human user)
- [ ] Agent permissions do not exceed sponsor's permissions
- [ ] Agent cannot approve artifacts
- [ ] Agent cannot delete resources
- [ ] Agent rate limits are configured
- [ ] Agent scope is defined and enforced
- [ ] Agent actions are logged with sponsor attribution

---

## Part 4: Compliance Verification

### 4.1 New User Setup Verification

When adding a new user, verify:

- [ ] User assigned appropriate role (default to Viewer if uncertain)
- [ ] User assigned to specific projects (not automatic access to everything)
- [ ] User addition logged in audit trail
- [ ] User acknowledges any required policies (if applicable)

### 4.2 Role Change Verification

When changing a user's role, verify:

- [ ] Role change is authorized by Owner
- [ ] Role change is logged with reason
- [ ] New permissions are appropriate for user's responsibilities
- [ ] Any elevated access is justified

### 4.3 Project Creation Verification

When creating a new project, verify:

- [ ] At least one Planner assigned
- [ ] Default access is restricted (not open to all users)
- [ ] Project creation logged

### 4.4 Integration Configuration Verification

When configuring an integration, verify:

- [ ] Integration is authorized by Owner
- [ ] Credentials are stored securely (not in audit logs or source code)
- [ ] Integration scope is limited to necessary data
- [ ] Integration configuration logged

### 4.5 Periodic Review Checklist

Quarterly (or monthly, adjust based on team preferences):

#### Access Review

- [ ] All users still need their current access level
- [ ] No orphaned accounts (departed users, unused accounts)
- [ ] No excessive permissions (users with more access than needed)
- [ ] Roles are correctly assigned

#### Audit Log Review

- [ ] Audit logs are being collected (no gaps)
- [ ] No suspicious patterns (failed logins, unusual exports)
- [ ] Storage is within retention policy limits
- [ ] Export procedures work correctly

#### Agent Review

- [ ] All agents have active sponsors
- [ ] Agent permissions are appropriate
- [ ] Agent rate limits are effective
- [ ] Agent actions align with intended use

---

## Part 5: Audit Log Queries

Common queries for investigating audit logs. Syntax is pseudocode; adapt to actual query language.

### 5.1 Security Investigation Queries

**Who accessed this project in the last 30 days?**
```
events where
  project.id = "proj_xyz" AND
  timestamp > now() - 30d
group by actor.id
```

**Failed login attempts in the last 24 hours:**
```
events where
  event_type = "auth.login_failed" AND
  timestamp > now() - 24h
order by timestamp desc
```

**All role changes in the last 90 days:**
```
events where
  event_type = "user.role_changed" AND
  timestamp > now() - 90d
order by timestamp desc
```

### 5.2 Accountability Queries

**Who approved this artifact?**
```
events where
  event_type = "artifact.approved" AND
  resource.id = "SPEC-broadcast-001"
order by timestamp desc
limit 1
```

**What did this user do in this project?**
```
events where
  actor.id = "user_abc123" AND
  project.id = "proj_xyz"
order by timestamp desc
```

**What changes happened to this artifact?**
```
events where
  resource.id = "SPEC-broadcast-001"
order by timestamp asc
```

### 5.3 Agent Accountability Queries

**All actions by a specific agent:**
```
events where
  actor.type = "agent" AND
  actor.id = "agent_research_001"
order by timestamp desc
```

**All agent actions sponsored by a user:**
```
events where
  actor.type = "agent" AND
  sponsor.id = "user_abc123"
order by timestamp desc
```

---

## Part 6: Example Audit Log Entries

### 6.1 User Login

```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "timestamp": "2026-01-25T09:15:00.000Z",
  "event_type": "auth.login",
  "actor": {
    "type": "user",
    "id": "user_jane",
    "email": "jane@efn.com"
  },
  "sponsor": null,
  "project": null,
  "resource": null,
  "action": "login",
  "outcome": "success",
  "context": {
    "method": "sso"
  },
  "client": {
    "ip_address": "10.0.1.42",
    "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)..."
  }
}
```

### 6.2 Artifact Approval

```json
{
  "id": "b2c3d4e5-f6a7-8901-bcde-f23456789012",
  "timestamp": "2026-01-25T14:30:00.000Z",
  "event_type": "artifact.approved",
  "actor": {
    "type": "user",
    "id": "user_jane",
    "email": "jane@efn.com"
  },
  "sponsor": null,
  "project": {
    "id": "proj_broadcast",
    "name": "Broadcast Tools"
  },
  "resource": {
    "type": "artifact",
    "id": "SPEC-broadcast-001",
    "name": "Data Visualization Spec"
  },
  "action": "approved",
  "outcome": "success",
  "context": {
    "previous_status": "review",
    "new_status": "active"
  },
  "client": {
    "ip_address": "10.0.1.42",
    "user_agent": null
  }
}
```

### 6.3 Agent Action with Sponsor

```json
{
  "id": "c3d4e5f6-a7b8-9012-cdef-345678901234",
  "timestamp": "2026-01-25T14:45:00.000Z",
  "event_type": "agent.action",
  "actor": {
    "type": "agent",
    "id": "agent_research_001",
    "email": null
  },
  "sponsor": {
    "id": "user_jane",
    "email": "jane@efn.com"
  },
  "project": {
    "id": "proj_broadcast",
    "name": "Broadcast Tools"
  },
  "resource": {
    "type": "artifact",
    "id": "RF-01-05",
    "name": "Widget Library Research"
  },
  "action": "created_draft",
  "outcome": "success",
  "context": {
    "agent_id": "agent_research_001",
    "action_type": "artifact_creation",
    "artifact_type": "rf"
  },
  "client": null
}
```

### 6.4 Branch Merge

```json
{
  "id": "d4e5f6a7-b8c9-0123-def4-567890123456",
  "timestamp": "2026-01-25T16:00:00.000Z",
  "event_type": "branch.merged",
  "actor": {
    "type": "user",
    "id": "user_alex",
    "email": "alex@efn.com"
  },
  "sponsor": null,
  "project": {
    "id": "proj_broadcast",
    "name": "Broadcast Tools"
  },
  "resource": {
    "type": "branch",
    "id": "branch_api_research",
    "name": "API Provider Research"
  },
  "action": "merged",
  "outcome": "success",
  "context": {
    "changes_summary": {
      "artifacts_added": ["RF-01-06"],
      "artifacts_modified": ["SPEC-broadcast-001"],
      "decisions_recorded": ["ADR-01-03"]
    },
    "merge_target": "canonical"
  },
  "client": {
    "ip_address": "10.0.1.55",
    "user_agent": null
  }
}
```

### 6.5 Permission Denied

```json
{
  "id": "e5f6a7b8-c9d0-1234-efa5-678901234567",
  "timestamp": "2026-01-25T10:30:00.000Z",
  "event_type": "artifact.deleted",
  "actor": {
    "type": "user",
    "id": "user_viewer",
    "email": "viewer@efn.com"
  },
  "sponsor": null,
  "project": {
    "id": "proj_broadcast",
    "name": "Broadcast Tools"
  },
  "resource": {
    "type": "artifact",
    "id": "SPEC-broadcast-001",
    "name": "Data Visualization Spec"
  },
  "action": "delete_attempted",
  "outcome": "denied",
  "context": {
    "reason": "insufficient_permissions",
    "required_role": "owner",
    "actual_role": "viewer"
  },
  "client": {
    "ip_address": "10.0.1.100",
    "user_agent": null
  }
}
```

---

## Part 7: Retention and Storage

### 7.1 Retention Periods

| Event Category | Retention Period | Rationale |
|----------------|------------------|-----------|
| Security events (auth, permissions) | 2 years | Compliance baseline |
| Artifact lifecycle events | 2 years | Audit trail for decisions |
| Agent events | 1 year | Debugging and accountability |
| Integration events | 1 year | Debugging |
| Denied/failed events | 90 days | Security investigation |

### 7.2 Storage Estimates

Rough storage estimates for planning:

| Event Volume | Daily Events | Monthly Storage |
|--------------|--------------|-----------------|
| Low (2–3 users, light use) | ~50–100 | ~15 MB |
| Medium (5–10 users, active) | ~500–1000 | ~150 MB |
| High (20+ users, heavy use) | ~2000–5000 | ~500 MB |

Estimates assume ~500 bytes per event average. Actual usage varies.

### 7.3 Purge Procedures

When retention period expires:

1. Events older than retention threshold are identified
2. Events are exported to cold storage (optional, for extended archive)
3. Events are deleted from primary storage
4. Purge action itself is logged (as system event)

**Important:** Purge should be automated, not manual. Manual purges create compliance risks.

---

## Appendix A: JSON Schema

For validation, the complete JSON Schema for audit log entries:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Compass Audit Log Entry",
  "type": "object",
  "required": ["id", "timestamp", "event_type", "actor", "action", "outcome"],
  "properties": {
    "id": {
      "type": "string",
      "format": "uuid"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time"
    },
    "event_type": {
      "type": "string",
      "pattern": "^[a-z]+\\.[a-z_]+$"
    },
    "actor": {
      "type": "object",
      "required": ["type", "id"],
      "properties": {
        "type": { "enum": ["user", "agent"] },
        "id": { "type": "string" },
        "email": { "type": ["string", "null"] }
      }
    },
    "sponsor": {
      "type": ["object", "null"],
      "properties": {
        "id": { "type": "string" },
        "email": { "type": "string" }
      }
    },
    "project": {
      "type": ["object", "null"],
      "properties": {
        "id": { "type": "string" },
        "name": { "type": "string" }
      }
    },
    "resource": {
      "type": ["object", "null"],
      "properties": {
        "type": { "type": "string" },
        "id": { "type": "string" },
        "name": { "type": "string" }
      }
    },
    "action": { "type": "string" },
    "outcome": { "enum": ["success", "failure", "denied"] },
    "context": { "type": "object" },
    "client": {
      "type": ["object", "null"],
      "properties": {
        "ip_address": { "type": ["string", "null"] },
        "user_agent": { "type": ["string", "null"] }
      }
    }
  }
}
```

---

## Appendix B: Quick Reference

### Roles at a Glance

| Role | Can Create | Can Edit | Can Approve | Can Delete | Can Admin |
|------|------------|----------|-------------|------------|-----------|
| Owner | ✓ | ✓ | ✓ | ✓ | ✓ |
| Planner | ✓ | ✓ | ✓ | ✗ | ✗ |
| Contributor | Draft only | Own drafts | ✗ | ✗ | ✗ |
| Viewer | ✗ | ✗ | ✗ | ✗ | ✗ |
| Agent* | ✓ | ✓ | ✗ | ✗ | ✗ |

*Agent inherits from sponsor, minus approval/delete.

### Event Types Quick List

```
auth.login, auth.logout, auth.login_failed, auth.session_expired

user.created, user.role_changed, user.disabled, user.enabled, user.deleted,
user.project_access_granted, user.project_access_revoked

artifact.created, artifact.edited, artifact.submitted, artifact.approved,
artifact.deprecated, artifact.deleted

branch.created, branch.merged, branch.merge_rejected, branch.archived

project.created, project.archived, project.deleted, project.settings_changed

integration.configured, integration.removed, integration.invoked, integration.failed

export.initiated, export.completed, export.failed

agent.action, agent.rate_limited, agent.scope_violation
```

### Minimum Logging Quick Check

Always log: `auth.login`, `auth.login_failed`, `user.role_changed`, `artifact.approved`, `artifact.deleted`, `branch.merged`, `integration.configured`, `export.initiated`

Never log: Views, searches, chat messages, draft content, keystrokes

---

## Appendix C: Related Documents

- **DD-15-01**: Governance definitions (companion document with rationale and policies)
- **DD-13-01**: Artifact taxonomy (defines artifact lifecycle states)
- **DD-14-01**: EFN ecosystem (defines tool archetypes)
- **Compass System Definition**: Authoritative source for security requirements

---

*End of Governance and Audit Standards (STD-15-01)*
