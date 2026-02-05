---
id: DD-16-01
type: dd
area: 16-reliability-tiers
title: Reliability Tiers and Operational Standards
status: draft
created: 2026-02-01
updated: 2026-02-01
author: compass-research
summary: Defines reliability tiers for EFN tools and per-tier operational requirements covering safeguards, observability, backup, and incident response
tags: [reliability, operations, monitoring, tiers, recovery, observability]
related:
  - DD-14-01
  - STD-14-01
  - DD-17-01
  - ADR-01-01
companion: STD-16-01
---

# Reliability Tiers and Operational Standards

## Document Purpose

This document defines reliability tiers for EFN tools, specifying what each tier requires in terms of safeguards, observability, backup procedures, and incident response. It provides a framework for matching operational investment to business criticality—so broadcast-critical tools get redundancy and testing while internal utilities get minimal overhead.

**Why tiers matter**: Not all tools deserve the same operational investment. Over-engineering an internal file converter wastes effort; under-engineering broadcast graphics risks on-air failures. Tiers create proportionate expectations that a small team can actually meet.

**Audience**: Builders, product owners, and anyone responsible for deploying or operating EFN tools.

**Key principle from System Definition (§1.7)**: "Reliable under partial failure—if a memory, search, or index service fails, Compass still functions in degraded but usable mode."

---

## Part 1: Reliability Tier Catalog

EFN uses five reliability tiers, aligned with the project archetypes defined in DD-14-01. Each tier specifies the acceptable failure impact and the operational investment required to achieve it.

### 1.1 Tier Overview

| Tier | Name | Impact of Failure | Availability Target | Recovery Time Objective |
|------|------|-------------------|---------------------|-------------------------|
| 1 | Broadcast-Critical | Visible to audience in real-time | 99.9% during broadcast windows | < 30 seconds |
| 2 | Business-Critical | Significantly blocks content creation | 99% during business hours | < 1 hour |
| 3 | Business-Important | Delays publication but work can queue | 95% | < 4 hours |
| 4 | Internal Standard | Causes inconvenience; workarounds exist | 90% | < 24 hours |
| 5 | Best Effort | Minimal impact; failure is acceptable | No target | No target |

**Understanding availability percentages**:

| Availability | Downtime Per Month | Downtime Per Year |
|--------------|-------------------|-------------------|
| 99.9% | 43 minutes | 8.7 hours |
| 99% | 7.2 hours | 3.6 days |
| 95% | 36 hours | 18 days |
| 90% | 72 hours | 36 days |

These percentages are targets, not SLAs with penalties. They guide design decisions and operational investment. Missing them triggers review, not contractual consequences.

### 1.2 Tier 1: Broadcast-Critical

**Definition**: Tools used during live broadcasts where failure is immediately visible to the audience. There are no retakes in live television; the tool must work correctly the first time, every time during broadcast windows.

**Characteristic examples**: Broadcast data visualization, live lower-thirds and graphics, real-time data feeds for on-air displays.

**Operational requirements**:

Redundancy is mandatory. No single component failure should cause complete system failure during broadcast. This typically means redundant network paths, backup data sources, and tested failover procedures. Hardware redundancy (multiple servers) is less critical when using managed cloud services like Convex, but network and data source redundancy remain important.

Pre-broadcast verification is required. Before every broadcast, operators run a verification checklist confirming connectivity to all dependencies, data freshness, and correct system state. This is not optional—it's the equivalent of a pilot's pre-flight checklist.

On-call responsibility must be assigned for every broadcast window. Someone must be available who can diagnose and fix issues within minutes, not hours. This person needs access to systems and authority to make changes without approval chains.

Graceful degradation must be designed before the primary implementation. If the live data feed fails, what does the operator see? If the database is unreachable, can cached data be displayed? These questions must have documented answers before the tool is used on air.

**Why this tier is demanding**: A 30-second outage during prime-time broadcast affects audience perception and advertiser confidence. The cost of preventing failure is almost always lower than the cost of visible failure.

### 1.3 Tier 2: Business-Critical

**Definition**: Tools essential for daily content creation where failure blocks work but doesn't create immediate public impact. Work queues rather than fails, but queued work creates pressure on downstream schedules.

**Characteristic examples**: Captions and subtitles refinement, video analytics and semantic analysis, podcast production tools, LLM-driven content enhancement.

**Operational requirements**:

Monitoring must detect failures within minutes. Alerting should notify responsible parties when error rates spike or the system becomes unreachable. The goal is human awareness before users report problems.

Work must queue safely during outages. When a Tier 2 tool is unavailable, upstream processes should be able to continue submitting work that accumulates for processing once service is restored. This requires idempotent operations (as defined in DD-17-01 §2) so retries don't create duplicates.

Recovery procedures must be documented and tested. "Restart the service" is an acceptable procedure if it actually works. The requirement is documentation and verification, not complexity.

Human review remains part of the workflow. Unlike broadcast tools operating autonomously during live events, Tier 2 tools typically have human checkpoints where quality issues can be caught before publication.

**Why this tier matters**: These tools are force multipliers—they let a small team produce more content at higher quality. Extended outages don't just create inconvenience; they reduce output capacity and may cause deadline misses.

### 1.4 Tier 3: Business-Important

**Definition**: Tools that support content workflows where failure causes delays but manual workarounds exist. Publication happens, just with more effort or reduced efficiency.

**Characteristic examples**: Article companion generators, CMS integration tools, social media formatters, print pipeline components.

**Operational requirements**:

Basic monitoring must exist. Health check endpoints, error logging, and some form of alerting (even if just email) are expected. Silent failures that accumulate for days are not acceptable.

Manual fallback procedures must be documented. When the article companion generator fails, how do editors create companion content manually? This procedure should exist and be known to users before they need it.

Recovery within a working day is the standard. If a tool breaks at 9 AM, it should be fixed by end of day—not next week. This doesn't require on-call; it requires someone checking alerts and having permission to fix things.

**Why this tier is lighter**: These tools enhance efficiency but don't create hard blocks. Manual workarounds exist because these functions were done manually before automation. The automation saves time; losing it temporarily is inconvenient, not catastrophic.

### 1.5 Tier 4: Internal Standard

**Definition**: Tools supporting internal operations that don't directly affect content production. Failure impacts convenience and efficiency but doesn't block publication.

**Characteristic examples**: File format converters, data aggregation utilities, internal dashboards, automation glue between systems.

**Operational requirements**:

Error messages must be understandable. When something fails, users should be able to determine what went wrong and whether waiting will help. "Internal Server Error" is not sufficient; "Unable to convert file: unsupported format" is.

Recovery procedures should exist, even if informal. "Restart the container" or "clear the cache and try again" counts. The requirement is that someone knows what to do, not that there's a formal runbook.

Users must know how to report issues. There should be a clear path from "this isn't working" to "someone who can fix it knows about it." This might be a Slack channel, an email address, or just "message Johan."

**The danger of Tier 4 tools**: Internal utilities often start as quick fixes and become essential infrastructure without anyone noticing. The graduation criteria (defined in STD-14-01 §1.4) help identify when a Tier 4 tool has become Tier 3 or Tier 2 and needs upgraded operational investment.

### 1.6 Tier 5: Best Effort (Exploratory)

**Definition**: Experimental tools, prototypes, and proof-of-concept implementations where failure is expected and acceptable. The goal is learning, not production use.

**Characteristic examples**: Technology evaluations, prototype features, research spikes, hackathon projects.

**Operational requirements**:

Clear labeling as experimental. Users must know this isn't a production tool. The interface should make this obvious—"PROTOTYPE: Not for production use" banners are appropriate.

No connection to production data without explicit approval. Experiments should not risk corrupting or exposing real data. Use test data, synthetic data, or explicitly approved read-only access.

Time-boxed existence. Every experiment should have a planned end date when it will be graduated to a real tier or retired. Experiments that linger become shadow infrastructure.

**What Tier 5 is NOT**: An excuse to build poorly. Even experiments benefit from basic error handling and clear code. The difference is operational investment (monitoring, redundancy, documentation), not code quality.

---

## Part 2: Per-Tier Requirements Matrix

This matrix specifies concrete requirements for each tier across four operational domains: safeguards, observability, backup, and incident response.

### 2.1 Safeguards Requirements

Safeguards are design and deployment practices that prevent failures or limit their impact.

| Requirement | Tier 1 | Tier 2 | Tier 3 | Tier 4 | Tier 5 |
|-------------|--------|--------|--------|--------|--------|
| **Redundant components** | Required | Recommended | Not required | Not required | Not required |
| **Graceful degradation design** | Required, documented | Required | Recommended | Optional | Not required |
| **Pre-deployment testing** | Load + integration + failover | Integration + unit | Unit + smoke | Basic verification | None required |
| **Manual override capability** | Required | Recommended | Optional | Not required | Not required |
| **Circuit breaker for dependencies** | Required | Required | Recommended | Optional | Not required |
| **Input validation** | Strict | Standard | Basic | Basic | Optional |
| **Rate limiting (if API exposed)** | Required | Required | Recommended | Optional | Not required |

**What "redundant components" means practically**: For broadcast tools, this means the tool can survive individual component failures—a backup data source, an alternative network path, or a cached state that can serve requests if the primary database is unreachable. For Convex-based tools, the database itself is managed and redundant, so redundancy concerns focus on data sources, network paths, and caching layers.

**What "circuit breaker" means**: When a dependency (like an external API) starts failing, the tool should stop calling it temporarily rather than timing out repeatedly. This prevents a failing dependency from cascading into tool unresponsiveness. DD-17-01 §3.4 defines the circuit breaker pattern in detail.

### 2.2 Observability Requirements

Observability is the ability to understand system state and behavior from external outputs: logs, metrics, and traces.

| Requirement | Tier 1 | Tier 2 | Tier 3 | Tier 4 | Tier 5 |
|-------------|--------|--------|--------|--------|--------|
| **Structured logging** | Required, JSON format | Required, JSON format | Required | Recommended | Optional |
| **Log retention** | 90 days minimum | 30 days minimum | 14 days minimum | 7 days minimum | Not required |
| **Health check endpoint** | Required, comprehensive | Required, basic | Required, basic | Recommended | Not required |
| **Error rate metrics** | Real-time with alerting | With alerting | Collected | Optional | Not required |
| **Latency metrics** | P50/P95/P99 tracked | P50/P95 tracked | Optional | Not required | Not required |
| **Request tracing** | Correlation IDs required | Correlation IDs required | Recommended | Optional | Not required |
| **Custom dashboards** | Required | Recommended | Optional | Not required | Not required |

**What "structured logging" means**: Logs are JSON objects with consistent fields (timestamp, level, service, message, correlation_id) that can be parsed and searched programmatically. This differs from plain text logs that require regex matching to extract information. DD-14-01 §3.3 specifies the logging standard in detail.

**What "comprehensive health check" means**: For Tier 1, the health check should verify not just "service is running" but also "dependencies are reachable" and "recent operations succeeded." A broadcast tool's health check should confirm it can reach its data sources and render test graphics.

### 2.3 Backup and Recovery Requirements

Backup ensures data can be restored after loss; recovery procedures ensure the system can return to operation after failure.

| Requirement | Tier 1 | Tier 2 | Tier 3 | Tier 4 | Tier 5 |
|-------------|--------|--------|--------|--------|--------|
| **Data backup frequency** | Continuous or < 1 hour | Daily | Daily | Weekly | Not required |
| **Backup retention** | 30 days minimum | 14 days minimum | 7 days minimum | 7 days minimum | Not required |
| **Backup verification** | Weekly restore tests | Monthly restore tests | Quarterly verification | Annual verification | Not required |
| **Recovery runbook** | Detailed, tested quarterly | Documented, tested annually | Documented | Informal OK | Not required |
| **Recovery drills** | Quarterly | Annually | Not required | Not required | Not required |
| **Point-in-time recovery** | Required | Recommended | Optional | Not required | Not required |

**Why backup verification matters**: Backups that haven't been tested are theoretical backups. A quarterly restore test for Tier 1 means actually restoring data to a test environment and verifying it's usable—not just confirming backup jobs completed.

**What Convex provides automatically**: Convex handles database backups and provides point-in-time recovery as part of the platform. The backup requirements above apply to data outside Convex (file uploads, external integrations, configuration) and to verifying that Convex's recovery actually works for your use case.

### 2.4 Incident Response Requirements

Incident response covers what happens when something goes wrong: detection, communication, resolution, and learning.

| Requirement | Tier 1 | Tier 2 | Tier 3 | Tier 4 | Tier 5 |
|-------------|--------|--------|--------|--------|--------|
| **Detection target** | < 1 minute | < 5 minutes | < 30 minutes | < 4 hours | User-reported |
| **Initial response target** | < 5 minutes | < 30 minutes | < 2 hours | < 8 hours | Best effort |
| **On-call requirement** | During broadcast windows | Business hours | None | None | None |
| **Escalation path** | Defined, with contacts | Defined | Informal OK | Informal OK | Not required |
| **Incident communication** | Real-time to stakeholders | Updates to affected users | As needed | Not required | Not required |
| **Post-incident review** | Required for all incidents | Required for extended outages | Optional | Not required | Not required |

**What "detection target" means**: How quickly does someone know there's a problem? For Tier 1, automated monitoring must detect issues within a minute and alert immediately. For Tier 4, it's acceptable if users report problems after noticing something wrong.

**What "post-incident review" is**: After resolving an incident, the team discusses what happened, why, and what could prevent recurrence. This isn't a blame exercise—it's a learning opportunity. For Tier 1, every incident gets reviewed. For Tier 2, only extended outages (>1 hour) require formal review.

---

## Part 3: Tier Assignment Criteria

Determining which tier a tool belongs to is the first step in defining its operational requirements. This section provides a framework for making that decision.

### 3.1 Decision Framework

Use these questions to determine initial tier assignment:

**Question 1: Is this tool used during live broadcasts?**
- Yes → Tier 1 (Broadcast-Critical)
- No → Continue to Question 2

**Question 2: Does failure block content creation?**
- Yes, work cannot proceed → Tier 2 (Business-Critical)
- Work can queue but backs up → Tier 2 or 3 depending on queue tolerance
- No, work proceeds with more effort → Continue to Question 3

**Question 3: Does failure delay publication?**
- Yes, publication delayed significantly → Tier 3 (Business-Important)
- Slightly delayed but manageable → Tier 3 or 4 depending on frequency
- No → Continue to Question 4

**Question 4: Is this an experiment or prototype?**
- Yes, time-boxed learning exercise → Tier 5 (Best Effort)
- No, intended for ongoing use → Tier 4 (Internal Standard)

### 3.2 Factors That Increase Tier Assignment

These factors suggest assigning a higher tier than the framework indicates:

**Downstream dependencies**: If other tools depend on this one, failure cascades. A data aggregation utility that feeds three other systems may deserve Tier 3 even if it seems like Tier 4 in isolation.

**Data sensitivity**: Tools handling competitive intelligence or financial data may need higher operational investment regardless of availability requirements. The Analytics & Intelligence archetype (DD-14-01 §1.2) has elevated security requirements even at Tier 4 availability.

**User count scaling**: A tool used by 3 people is different from one used by 30. Higher user counts mean more people affected by outages and more potential for simultaneous usage causing load issues.

**Revenue proximity**: Tools in the path between content and revenue (advertising, subscriptions) may warrant higher tiers than their direct function suggests.

### 3.3 Factors That Decrease Tier Assignment

These factors suggest a lower tier is appropriate:

**Robust manual fallback**: If the manual process is well-understood and not significantly slower, lower tier is acceptable. Article companion generation can be manual; live data visualization during broadcast cannot.

**Low usage frequency**: Tools used weekly or monthly don't need the same monitoring investment as daily-use tools. The cost of an outage is lower when the next attempted use might be days away.

**Easy rollback**: Tools that are stateless or have trivial rollback procedures need less operational investment in prevention since recovery is straightforward.

### 3.4 Override Conditions

Some conditions override the normal tier assignment:

**Security incidents**: Any tool involved in a security incident is treated as Tier 2 minimum until remediation is complete and verified.

**Regulatory requirements**: Tools handling data subject to regulatory requirements (GDPR, financial regulations) may need operational controls beyond what their availability tier suggests.

**Executive commitment**: If leadership has made specific reliability commitments for a tool, that commitment overrides the default tier assignment.

### 3.5 Re-evaluation Triggers

Tier assignments should be reviewed when:

- The tool's usage increases significantly (10x users, 10x traffic)
- The tool gains new downstream dependencies
- An incident reveals higher-than-expected impact
- The tool's scope expands materially
- Annually as part of periodic review (STD-14-01 §3.3)

---

## Part 4: Compass Reliability Target

Compass itself requires a tier assignment. Based on System Definition requirements, Compass should target **Tier 2 (Business-Critical)** with specific enhancements.

### 4.1 Why Tier 2

The System Definition (§3.8) is explicit: "Planning work is high-value. Losing work is unacceptable."

Compass handles long-running planning workflows that may span days or weeks. Losing a planning session mid-way wastes significant invested time—not just the conversation but the thinking and decisions embedded in it.

However, Compass does not operate during live broadcasts. Failure is not visible to external audiences. Work can queue (users can continue planning locally or in other tools) even if Compass is temporarily unavailable.

This positions Compass as Business-Critical: important enough to warrant serious operational investment, but not requiring the extreme measures of Broadcast-Critical.

### 4.2 Compass-Specific Requirements

Beyond standard Tier 2 requirements, Compass needs:

**Continuous state persistence**: "Conversation state saves continuously" (System Definition §3.8). Every user input and system response should be persisted within seconds. Loss of a single message is acceptable; loss of a conversation is not.

Convex's automatic persistence model supports this naturally—mutations are durable by design. The requirement is ensuring all conversation state flows through mutations, not just rendering from ephemeral client state.

**Auto-save with conflict detection**: "Documents auto-save with conflict detection" (System Definition §3.8). Artifacts being edited should save automatically without explicit user action. If two sessions modify the same artifact, conflict detection should prevent silent overwrites.

**Graceful degradation for external services**: If the LLM provider is unavailable, Compass should still allow browsing existing artifacts and decisions. If the memory/retrieval layer fails, planning continues with reduced context (no semantic search, but explicit artifact references still work).

The System Definition is explicit about this: "If memory search is down, planning continues with reduced context. If a research source is unavailable, it is skipped with visible notification."

**Safe retry for failed operations**: "Failed operations retry automatically where safe" (System Definition §3.8). Idempotent operations (as defined in DD-17-01 §2) should retry automatically. Non-idempotent operations should queue for user-initiated retry with clear status indication.

### 4.3 Compass Availability Target

**Target**: 99% availability during business hours (Monday–Friday, 8 AM–8 PM local time for EFN).

**Recovery Time Objective**: < 1 hour for full functionality; < 5 minutes for degraded mode (browsing existing content).

**Recovery Point Objective**: < 1 minute of data loss for conversation state; < 5 minutes for artifact edits.

**Why not Tier 1?** Compass is not used during live broadcasts. Planning sessions can be paused and resumed. The cost of Tier 1 requirements (redundant infrastructure, on-call during all hours, quarterly failover drills) exceeds the benefit for a tool used by 2-3 people during business hours.

---

## Part 5: Archetype-to-Tier Mapping

This section provides the definitive mapping between project archetypes (from DD-14-01) and reliability tiers.

### 5.1 Standard Mapping

| Archetype | Default Tier | Rationale |
|-----------|--------------|-----------|
| **Broadcast-Critical** | Tier 1 | Failure visible to audience; no recovery opportunity |
| **Production Pipeline** | Tier 2 | Blocks content creation but work can queue |
| **Publishing Pipeline** | Tier 3 | Delays publication; manual fallbacks exist |
| **Analytics & Intelligence** | Tier 4* | Degrades decision-making; not time-critical |
| **Internal Utility** | Tier 4 | Efficiency impact only; workarounds exist |
| **Exploratory** | Tier 5 | Failure expected and acceptable |

*Analytics & Intelligence tools default to Tier 4 for availability but have elevated security and privacy requirements regardless of tier. See DD-14-01 §2.3 for privacy profile requirements.

### 5.2 Sample Tool Classifications

| Tool | Archetype | Tier | Notes |
|------|-----------|------|-------|
| Broadcast data visualization | Broadcast-Critical | 1 | Used during live broadcasts |
| Captions/subtitles refinement | Production Pipeline | 2 | Blocks video publication workflow |
| Video analytics | Production Pipeline | 2 | Required for content planning |
| Article companion generator | Publishing Pipeline | 3 | Delays but doesn't block articles |
| Website CMS integration | Publishing Pipeline | 3 | Multiple publication paths exist |
| Viewer analytics dashboard | Analytics & Intelligence | 4 | Not time-critical; elevated privacy |
| File format converter | Internal Utility | 4 | Convenience tool with alternatives |
| Competitive intelligence tool | Analytics & Intelligence | 4 | Not time-critical; highest privacy |
| AI feature prototype | Exploratory | 5 | Time-boxed experiment |
| **Compass** | (Custom) | 2 | Business-critical planning infrastructure |

### 5.3 Tier Transition Procedures

When a tool's tier changes (up or down), follow these procedures:

**Upgrading tier (e.g., Tier 4 → Tier 3)**:

1. Complete the compliance checklist for the new tier (STD-14-01)
2. Implement required observability (§2.2) before considering upgrade complete
3. Document monitoring, alerting, and recovery procedures
4. Run at the new tier for 30 days with enhanced monitoring before considering stable

**Downgrading tier (e.g., Tier 2 → Tier 3)**:

1. Document rationale for downgrade
2. Notify users who depend on the higher tier expectations
3. Update monitoring and alerting thresholds
4. Archive (don't delete) the higher-tier operational documentation

---

## Part 6: Operational Simplicity Guidelines

The System Definition (§4.2) emphasizes that EFN's team is non-traditional developers. Operational complexity must match team capacity.

### 6.1 Keep It Debuggable

"Debuggability matters—explicit error handling, clear logs, and observable workflows" (System Definition §4.2).

For reliability implementation, this means:

**Prefer explicit over automatic**: Automated failover that fails silently is worse than manual recovery with clear instructions. If you can't explain what the system is doing, you can't debug when it misbehaves.

**Log intentions, not just actions**: Log "Starting daily backup of project artifacts" not just "Backup job started." When debugging, knowing what the system intended helps identify where it diverged.

**Test recovery, not just function**: When implementing a backup system, test the restore process. When implementing redundancy, test failover. Untested recovery procedures are theoretical.

### 6.2 Managed Services Over Self-Hosting

"Operational simplicity is essential—managed services preferred, minimal self-hosting" (System Definition §4.2).

For reliability, use managed services that handle infrastructure reliability:

| Need | Managed Approach | Self-Hosted Equivalent |
|------|------------------|------------------------|
| Database redundancy | Convex (built-in) | PostgreSQL replication configuration |
| Log aggregation | Convex dashboard, Axiom | ELK stack deployment |
| Alerting | Convex alerts, Axiom alerts | Prometheus + Alertmanager |
| Uptime monitoring | Checkly, Uptime Robot | Self-hosted Uptime Kuma |

The self-hosted alternatives require ongoing maintenance, security updates, and capacity planning. For a 2-3 person team, managed services free capacity for product work.

### 6.3 Progressive Reliability Investment

Don't implement all Tier 2 requirements on day one. Build up progressively:

**Phase 1 (Launch)**: Basic logging, error handling, health check endpoint. This is the minimum for any production use.

**Phase 2 (Month 1)**: Alerting for error spikes, documented recovery procedure, backup verification.

**Phase 3 (Month 3)**: Complete observability, tested recovery drills, refined alert thresholds based on operational experience.

This progression applies to Compass itself and to any Tier 2-3 tool EFN builds.

---

## Appendix A: Glossary

**Availability**: The percentage of time a system is operational and accessible. 99% availability = 7.2 hours downtime per month.

**Circuit breaker**: A pattern where a system stops calling a failing dependency temporarily to prevent cascade failures and allow recovery.

**Correlation ID**: A unique identifier passed through all components handling a request, enabling end-to-end tracing in logs.

**Graceful degradation**: The ability to continue providing partial service when dependencies fail, rather than failing completely.

**Health check**: An endpoint that reports whether a service is operational and, for comprehensive checks, whether its dependencies are reachable.

**Idempotent**: An operation that produces the same result whether executed once or multiple times, enabling safe retries.

**Post-incident review**: A structured discussion after resolving an incident to understand causes and prevent recurrence. Also called "blameless postmortem."

**Recovery Point Objective (RPO)**: The maximum acceptable data loss, measured in time. RPO of 5 minutes means losing at most 5 minutes of data.

**Recovery Time Objective (RTO)**: The maximum acceptable downtime. RTO of 1 hour means full service must be restored within an hour of failure.

**Redundancy**: Having backup components that can take over when primary components fail.

**Runbook**: A documented procedure for operating a system, including startup, shutdown, and recovery from common issues.

**Structured logging**: Logging in a machine-parseable format (typically JSON) with consistent fields, enabling programmatic search and analysis.

---

## Appendix B: Related Documents

- **STD-16-01**: The companion standard with enforceable requirements and checklists
- **DD-14-01**: EFN Ecosystem Requirements (archetype definitions)
- **STD-14-01**: EFN Shared Standards (compliance checklists per archetype)
- **DD-17-01**: Integration Patterns (error handling, retry strategies)
- **ADR-01-01**: Backend Selection (Convex reliability characteristics)
- **Compass System Definition**: Authoritative system specification (§3.8 Reliability, §4.2 Team Capacity)

---

*End of Reliability Tiers and Operational Standards (DD-16-01)*
