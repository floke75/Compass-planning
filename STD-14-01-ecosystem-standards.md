---
id: STD-14-01
type: standard
area: 14-efn-ecosystem
title: EFN Shared Standards and Compliance Checklist
status: draft
created: 2026-01-25
updated: 2026-01-25
author: compass-research
summary: Provides enforceable standards and compliance checklists for EFN tools based on archetype requirements
tags: [standards, compliance, checklist, ecosystem, verification]
related:
  - DD-14-01
  - DD-12-01
  - DD-13-01
companion: DD-14-01
enforcement: Pre-launch review and periodic audits
---

# EFN Shared Standards and Compliance Checklist

## Document Purpose

This document provides enforceable standards and compliance checklists for EFN tools. It is the actionable companion to DD-14-01 (EFN Tooling Ecosystem Requirements).

**How to use this document**:
1. When planning a new tool, determine its archetype using DD-14-01
2. Use the archetype-specific checklist in this document to identify requirements
3. Use the shared standards checklist to ensure baseline compliance
4. Reference this document during spec reviews and pre-launch verification

---

## Part 1: Archetype Compliance Checklists

Each archetype has specific requirements. Complete the relevant checklist before considering a tool ready for its intended use.

### 1.1 Broadcast-Critical Checklist

Tools used during live broadcasts where failure is visible to the audience.

#### Pre-Development
- [ ] Tool owner identified and documented
- [ ] Reliability tier (Tier 1) requirements reviewed and accepted
- [ ] Backup/fallback procedure designed before primary implementation
- [ ] Integration points with broadcast infrastructure identified

#### Architecture & Design
- [ ] No single points of failure in critical path
- [ ] Graceful degradation defined (what happens if data is stale? if service is down?)
- [ ] State can be recovered without losing broadcast capability
- [ ] Manual override capability exists for automated functions

#### Development & Testing
- [ ] All code paths tested, including error paths
- [ ] Load testing completed at 2x expected broadcast load
- [ ] Failover tested (primary fails, backup takes over)
- [ ] Integration tested with actual broadcast infrastructure (not mocks)

#### Operations
- [ ] Health check endpoint implemented (`/health`)
- [ ] Monitoring and alerting configured
- [ ] On-call responsibility assigned for broadcast windows
- [ ] Runbook documented: startup, shutdown, common issues, escalation

#### Pre-Broadcast
- [ ] Pre-broadcast verification procedure documented
- [ ] Verification checklist available to operators
- [ ] Rollback procedure tested and documented
- [ ] Contact information for support current

#### Security & Compliance
- [ ] SSO authentication implemented
- [ ] Audit logging captures all significant actions
- [ ] Data encrypted in transit
- [ ] Access limited to necessary personnel

---

### 1.2 Production Pipeline Checklist

Tools that create or modify content before publication with human review.

#### Pre-Development
- [ ] Tool owner identified and documented
- [ ] Reliability tier (Tier 2) requirements reviewed
- [ ] Upstream dependencies identified (what feeds this tool?)
- [ ] Downstream consumers identified (what uses this tool's output?)

#### Architecture & Design
- [ ] Input validation implemented
- [ ] Output quality signals included (confidence scores, verification flags)
- [ ] Processing can be retried safely (idempotent)
- [ ] Queue/batch processing handles failures gracefully

#### Development & Testing
- [ ] Unit tests for core logic
- [ ] Integration tests with real data samples
- [ ] Edge cases tested (empty input, malformed input, very large input)
- [ ] Output quality validated against human-reviewed samples

#### Operations
- [ ] Health check endpoint implemented
- [ ] Monitoring for error rates and queue depth
- [ ] Alert thresholds configured
- [ ] Runbook documents common failure modes and recovery

#### Security & Compliance
- [ ] SSO authentication implemented
- [ ] Role-based access configured
- [ ] Standard audit logging in place
- [ ] Data encrypted in transit

---

### 1.3 Publishing Pipeline Checklist

Tools that prepare content for distribution to external channels.

#### Pre-Development
- [ ] Tool owner identified and documented
- [ ] Target platforms/channels documented
- [ ] API constraints of target platforms understood (rate limits, formats)
- [ ] Manual fallback procedure identified

#### Architecture & Design
- [ ] Output format matches platform requirements
- [ ] Rate limiting respected for external APIs
- [ ] Retry logic handles transient failures
- [ ] Status/progress visible to users

#### Development & Testing
- [ ] End-to-end tests with actual platforms (staging if available)
- [ ] Error handling tested for common platform failures
- [ ] Format validation against platform requirements
- [ ] Manual fallback procedure tested

#### Operations
- [ ] Basic monitoring configured
- [ ] Alerts on repeated failures
- [ ] Documentation of platform-specific quirks
- [ ] Runbook for common issues

#### Security & Compliance
- [ ] SSO authentication implemented
- [ ] Platform credentials stored securely
- [ ] Standard audit logging in place
- [ ] Data encrypted in transit

---

### 1.4 Internal Utility Checklist

Tools that support internal operations without directly affecting content.

#### Pre-Development
- [ ] Tool owner identified (even if informal)
- [ ] Purpose documented (what problem does this solve?)
- [ ] Expected lifespan estimated (is this temporary or persistent?)

#### Development
- [ ] Basic input validation
- [ ] Errors produce understandable messages
- [ ] README documents usage

#### Operations
- [ ] Users know how to report issues
- [ ] Basic recovery procedure documented (even if "restart it")

#### Graduation Criteria
If an internal utility becomes essential, it should upgrade:
- [ ] Is this tool blocking if unavailable? → Consider upgrading archetype
- [ ] Are multiple people depending on this? → Document properly
- [ ] Has this survived 6+ months? → Review for proper standards compliance

---

### 1.5 Analytics & Intelligence Checklist

Tools that aggregate and analyze data to inform decisions.

#### Pre-Development
- [ ] Tool owner identified and documented
- [ ] Data sources identified and access approved
- [ ] Privacy review completed for all data sources
- [ ] Data retention requirements defined

#### Architecture & Design
- [ ] Data aggregation preserves privacy (no individual-level data exposed unnecessarily)
- [ ] Access controls enforce need-to-know
- [ ] No external data sharing without explicit approval
- [ ] Export capabilities respect privacy constraints

#### Development & Testing
- [ ] Calculations validated against known datasets
- [ ] Access controls tested
- [ ] Data refresh/staleness handling verified

#### Operations
- [ ] Data source availability monitored
- [ ] Stale data clearly indicated to users
- [ ] Runbook for data refresh issues

#### Security & Compliance (**Elevated for this archetype**)
- [ ] SSO authentication required
- [ ] Strict role-based access enforced
- [ ] Full audit logging of all data access
- [ ] Data encrypted at rest AND in transit
- [ ] No third-party services that retain or train on EFN data
- [ ] Data ownership terms verified with all vendors

---

### 1.6 Exploratory/Experimental Checklist

Tools built to test ideas where failure is acceptable.

#### Before Starting
- [ ] Experiment scope defined (what are we trying to learn?)
- [ ] Time box established (when do we evaluate?)
- [ ] Success criteria defined (how do we know if this worked?)

#### During Experiment
- [ ] Clearly marked as experimental (users know this is not production)
- [ ] Not connected to production data/systems without explicit approval
- [ ] Findings documented as learned

#### Experiment End
- [ ] Decision made: graduate, iterate, or retire
- [ ] If graduating: new archetype assigned, proper standards applied
- [ ] If retiring: code archived, learnings documented

---

## Part 2: Shared Standards Compliance Checklist

These standards apply to **all tools** at Tier 1-4 (not Exploratory). Check all that apply.

### 2.1 API Standards

*Applies to any tool that exposes an API (internal or external)*

- [ ] RESTful conventions followed (standard HTTP methods, meaningful status codes)
- [ ] Consistent response format with `data`, `meta`, `errors` structure
- [ ] API versioned in URL path (`/api/v1/...`)
- [ ] OpenAPI/Swagger documentation exists
- [ ] Documentation includes example requests and responses

### 2.2 Authentication Standards

- [ ] SSO integration implemented (Tier 1-4)
- [ ] Service-to-service auth uses API keys or JWT (not hardcoded credentials)
- [ ] Credentials stored in secure vault (not in code or config files)
- [ ] Role-based access control implemented

### 2.3 Logging Standards

- [ ] Structured logging (JSON format)
- [ ] Standard fields included: `timestamp`, `level`, `service`, `message`, `correlation_id`
- [ ] Log levels used appropriately (DEBUG, INFO, WARN, ERROR)
- [ ] Errors logged with context
- [ ] No credentials or sensitive data in logs

### 2.4 Observability Standards (Tier 1-3)

- [ ] Health check endpoint exists (`/health`)
- [ ] Key metrics tracked (request count, error rate, latency)
- [ ] Alerting configured for error rate spikes
- [ ] Alerting configured for availability drops

### 2.5 Error Handling Standards

- [ ] Errors don't crash the application
- [ ] Error responses include code, message, and suggestion
- [ ] Transient failures retry with exponential backoff
- [ ] Circuit breaker implemented for external dependencies (Tier 1-2)

### 2.6 Documentation Standards

- [ ] README exists with purpose, usage, and ownership
- [ ] Architecture overview documents component relationships
- [ ] API documentation exists for exposed interfaces
- [ ] Runbook exists for deployment and recovery (Tier 1-3)
- [ ] Documentation lives in the repository (not in separate wiki)
- [ ] Specification written before implementation

### 2.7 Data Format Standards

- [ ] JSON used for machine interchange
- [ ] Timestamps in ISO 8601 format, UTC for storage
- [ ] Schema documented for any produced data formats
- [ ] Media IDs consistent with ecosystem conventions

### 2.8 Dependency Management Standards

- [ ] All dependencies explicitly declared
- [ ] Dependency versions pinned
- [ ] Security scanning configured for dependencies
- [ ] No dependencies that require sharing EFN data

---

## Part 3: Compliance Verification Points

Use these verification points to ensure standards are maintained over time.

### 3.1 New Tool Review (Before Development)

Before significant development begins:

1. **Archetype Assigned**: Is this tool classified correctly?
2. **Requirements Understood**: Has the team reviewed the archetype checklist?
3. **Spec Complete**: Is there a specification that covers requirements?
4. **Integration Points Identified**: Are dependencies and consumers documented?

### 3.2 Pre-Launch Review

Before a tool goes into production use:

1. **Archetype Checklist Complete**: All required items checked
2. **Shared Standards Compliance**: Applicable shared standards implemented
3. **Documentation Complete**: README, architecture, API docs, runbook (if required)
4. **Security Review**: Authentication, authorization, logging, encryption verified

### 3.3 Periodic Review (Quarterly)

For tools in active use:

1. **Still Correctly Classified**: Has the tool's criticality changed?
2. **Documentation Current**: Does documentation match implementation?
3. **Dependencies Healthy**: Any deprecated or vulnerable dependencies?
4. **Standards Drift**: Any erosion of compliance since launch?

### 3.4 Post-Incident Review

After any significant incident:

1. **Root Cause Documented**: What actually went wrong?
2. **Standards Gap Identified**: Did any missing standard contribute?
3. **Runbook Updated**: Does the runbook cover this scenario now?
4. **Checklist Updated**: Should the checklist include new items?

---

## Part 4: Compliance Levels

Not all standards are equally critical. Use these levels to prioritize when resources are limited.

### Level 1: Non-Negotiable (Must have before any use)

- Security: Authentication, no credentials in code
- Safety: No single points of failure for Broadcast-Critical
- Privacy: No unauthorized external data sharing for Analytics

### Level 2: Required (Must have before production use)

- All archetype-specific checklist items
- Logging and error handling standards
- Documentation: README and API docs

### Level 3: Expected (Should have within 30 days of launch)

- Full observability (Tier 1-3)
- Complete runbook
- All shared standards compliance

### Level 4: Desired (Should have within 90 days of launch)

- Architecture documentation polished
- Dependency security scanning automated
- Integration tests comprehensive

---

## Appendix A: Quick Reference Card

### Archetype Selection
```
Live broadcast? → Broadcast-Critical
Creates content + human review? → Production Pipeline  
Publishes content? → Publishing Pipeline
Analyzes data? → Analytics & Intelligence
Experiment? → Exploratory
Otherwise → Internal Utility
```

### Reliability Tiers
```
Tier 1: 99.9%, zero downtime during broadcast, <30s recovery
Tier 2: 99%, hours acceptable, <1h recovery
Tier 3: 95%, days acceptable with fallback, <4h recovery
Tier 4: 90%, days acceptable, <24h recovery
Tier 5: Best effort
```

### Privacy Profiles
```
Public: Outputs are published
Internal: EFN only, standard handling
Sensitive: Competitive/business intelligence, strict controls
```

### Minimum Documentation
```
All tools: README (purpose, usage, owner)
Tier 1-3: + Architecture, API docs, Runbook
Analytics: + Privacy review, Data flow diagram
```

---

## Appendix B: Related Documents

- **DD-14-01**: The companion definition document this standard enforces
- **DD-12-01**: Repository structure and organization standards
- **DD-13-01**: Artifact taxonomy and documentation standards
- **Compass System Definition**: The authoritative system specification

---

*End of EFN Shared Standards and Compliance Checklist (STD-14-01)*
