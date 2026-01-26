---
id: STD-19-01
type: standard
area: 19-widget-schema
title: Widget Schema Standards
status: draft
created: 2026-01-26
updated: 2026-01-26
author: compass-research
summary: Specifies required fields, interaction logging requirements, and schema compliance rules for all Compass widgets
tags: [widgets, schema, standards, validation, compliance]
related:
  - DD-19-01
  - RF-02-01
  - ADR-02-01
  - RF-07-01
  - ADR-07-01
companion: DD-19-01
enforcement: Schema validation in orchestration layer
---

# Widget Schema Standards

## Document Purpose

This document establishes the mandatory standards for widget specifications in Compass. While DD-19-01 defines what widgets are and how they work, this document specifies what must be true for any widget specification to be considered valid and compliant.

**Why this matters**: Standards ensure consistency across all widgets regardless of who generates them or when. Without enforced standards, widget quality degrades over time as edge cases accumulate and shortcuts become normalized. These standards create a quality floor that all widget specifications must meet.

**What this document covers**:

- Required fields that every widget specification must include
- Interaction logging requirements for audit and analytics
- Schema compliance rules and validation procedures
- Quality standards for widget content
- Testing and verification procedures

**How this document is used**:

- The orchestration layer validates generated specifications against these standards
- Developers verify custom components meet logging requirements
- Quality reviews use compliance checklists to assess widget implementations

**Audience**: Compass builders, validation system implementers, and quality reviewers.

---

## Part 1: Required Fields Checklist

Every widget specification must include certain fields to be considered valid. This section defines the mandatory fields organized by their purpose.

### 1.1 Identity Fields (Required for All Widgets)

Every widget must be uniquely identifiable within a workflow. The following fields establish identity:

**`type`** is required. Must exactly match one of the 18 registered widget types defined in DD-19-01 Part 1. Case-sensitive. No aliases or abbreviations. Validation fails if the type is not recognized.

**`id`** is required. Must follow the pattern `widget-{type}-{shortId}` where `{type}` matches the type field and `{shortId}` is a unique alphanumeric string of 6-12 characters. Example: `widget-single-select-a1b2c3`. IDs must be unique within a workflow run.

### 1.2 Content Fields (Required for All Widgets)

Every widget must provide content that the user sees and responds to:

**`prompt`** is required. Must be a non-empty string between 10 and 500 characters. Must be a complete question or instruction, not a fragment or placeholder. Must not contain only whitespace, HTML tags, or markdown formatting.

**`required`** is required. Must be a boolean (`true` or `false`). Determines whether the user must respond before proceeding.

### 1.3 UX Guarantee Fields (Required Defaults)

Per the System Definition §2.2, every widget must provide escape hatch, help, and research trigger capabilities. The following standards apply:

**Escape hatch**: If `escapeHatch` field is absent, the system must render a default escape hatch with label "None of these fit / I'll describe instead" and `promptForExplanation: true`. If `escapeHatch.enabled` is explicitly `false`, no escape hatch is rendered (use only when escape truly makes no sense).

**Help me think**: If `helpMeThink` field is absent, the system must render a default help button with label "Help me think about this". Content may be generated on demand if not pre-populated.

**Research trigger**: If `researchTrigger` field is absent, the system must render a default research trigger with label "Research this". When triggered, it spawns a research branch with a brief derived from the widget prompt.

### 1.4 Type-Specific Required Fields

Beyond common fields, each widget type has additional required fields:

**Choice widgets** (`single-select`, `multi-select`): `options` array with minimum 2 items, each containing `value` and `label`.

**Ranked choice and pairwise comparison**: `items` array with minimum 3 items, each containing `value` and `label`.

**Slider**: `min`, `max`, and `labels` (with `min` and `max` labels) are required.

**Opposing spectrum**: `poles` object with `left` and `right` properties, each containing `label`.

**Allocation**: `categories` array with minimum 2 items, each containing `value` and `label`.

**Trade-off table**: `options` array (minimum 2) and `criteria` array (minimum 2), each item containing `value` and `label`.

**A/B comparison**: `optionA` and `optionB` objects, each containing `value` and `label`.

**Card sort**: `cards` array (minimum 3) and `categories` array (minimum 2), each item containing `value` and `label`.

**Sequencer**: `items` array with minimum 2 items, each containing `value` and `label`.

**Quadrant**: `items` array (minimum 2) and `axes` object with `x` and `y` properties, each containing `label`, `lowLabel`, and `highLabel`.

**Mad-lib**: `template` string and `slots` array with minimum 1 item, each containing `name` and `label`.

**Structured fields**: `fields` array with minimum 1 item, each containing `name`, `label`, and `inputType`.

**Decision gate**: No additional required fields beyond common fields.

**Boundary checklist**: `checklistType` and `items` array with minimum 1 item, each containing `value` and `label`.

**Research trigger**: `researchQuestion` string is required.

**Merge gate**: `branchType`, `branchSummary`, and `proposedChanges` array are required.

### 1.5 Required Fields Verification Checklist

Use this checklist to verify a widget specification meets required field standards:

| Check | Verification |
|-------|--------------|
| Type field present | `type` exists and matches registered type |
| Type field valid | `type` is one of the 18 registered types |
| ID field present | `id` exists |
| ID format correct | `id` matches pattern `widget-{type}-{shortId}` |
| Prompt field present | `prompt` exists and is non-empty |
| Prompt length valid | `prompt` is 10-500 characters |
| Required field present | `required` exists and is boolean |
| Type-specific fields present | All required fields for this widget type exist |
| UX guarantees available | Escape hatch, help, research trigger either specified or will use defaults |

---

## Part 2: Interaction Logging Requirements

All widget interactions must be logged to support audit, analytics, and debugging. This section specifies what must be logged and how.

### 2.1 Mandatory Event Logging

The following events must be logged for every widget:

**`widget.presented`** must be logged when any widget is rendered to the user. This event establishes the baseline for measuring interaction time and confirms the widget was actually shown.

**`widget.submitted`** must be logged when the user submits a response (including escape hatch selection). This event captures the final response value.

### 2.2 Recommended Event Logging

The following events should be logged when feasible:

**`widget.interacted`** should be logged when the user makes changes before submission. This provides insight into decision-making process.

**`widget.abandoned`** should be logged when the user navigates away without responding. This identifies problematic widgets.

**`widget.help.opened`** and **`widget.help.closed`** should be logged to track help usage.

### 2.3 Required Event Fields

Every logged event must include the following fields:

| Field | Requirement |
|-------|-------------|
| `eventType` | Must be one of the defined event types |
| `timestamp` | ISO 8601 format, UTC timezone |
| `widgetId` | Must match the widget's `id` field |
| `widgetType` | Must match the widget's `type` field |
| `sessionId` | Current user session identifier |
| `workflowRunId` | Current workflow run identifier |

### 2.4 Event Payload Requirements

**`widget.presented` payload** must include the complete widget specification (so the log is self-contained for replay/debugging).

**`widget.submitted` payload** must include the complete WidgetResponse object including `value`, `responseType`, and `timestamp`.

**`widget.abandoned` payload** must include `lastKnownValue` (if any interaction occurred) and `reason` (timeout, navigation, error, etc.).

### 2.5 Logging Compliance Verification

To verify logging compliance, confirm that every widget presentation generates a `widget.presented` event, every widget submission generates a `widget.submitted` event, events contain all required fields, timestamps are valid ISO 8601 format, and event payloads contain required data.

### 2.6 Data Retention Requirements

Interaction logs must be retained for minimum 90 days for debugging and analytics. Logs older than 90 days may be archived or summarized. Personal data within logs must comply with EFN data retention policies.

---

## Part 3: Schema Compliance Rules

Widget specifications must pass schema validation before rendering. This section defines the validation rules and procedures.

### 3.1 JSON Schema Compliance

All widget specifications must validate against their declared type's JSON Schema (draft-07). Validation must be performed before rendering—invalid specifications must not be rendered.

**Strict mode**: All schemas use `additionalProperties: false`. Any field not explicitly defined in the schema causes validation failure. This prevents LLMs from adding unexpected fields that might be silently ignored.

### 3.2 Value Uniqueness Rules

Within any array of options, items, cards, categories, or fields, all `value` properties must be unique. Duplicate values cause validation failure.

**Example of failure**: 
```json
"options": [
  { "value": "opt1", "label": "Option A" },
  { "value": "opt1", "label": "Option B" }  // Fails: duplicate value
]
```

### 3.3 Reference Validity Rules

Any field that references another field's value must reference a valid value that exists:

**`defaultValue`** must reference an existing option's `value` (for single-select, slider with discrete values).

**`defaultValues`** (array) must contain only values that exist in the options array.

**`defaultAllocations`** keys must match category `value` fields.

**`defaultAssignments`** keys must match card `value` fields, and values must match category `value` fields.

**`defaultPositions`** keys must match item `value` fields.

### 3.4 Constraint Coherence Rules

Numeric constraints must be logically consistent:

**Range constraints**: `min` must be less than `max`. `minSelections` must be less than or equal to `maxSelections`. `minItems` must be less than or equal to `maxItems`.

**Budget constraints**: For allocation widgets, the sum of all `minAllocation` values must not exceed `budget`. The sum of all `maxAllocation` values must be at least `budget`.

**Array length constraints**: `defaultValues` length must not exceed `maxSelections`. Items/options/cards arrays must have at least `minItems` (schema-defined minimum) entries.

### 3.5 Content Quality Rules

Beyond structural validation, widget content must meet quality standards:

**No placeholder content**: Labels and descriptions must not contain obvious placeholders like "[description]", "Option 1", "TODO", or "placeholder".

**No empty strings**: Any string field that is present must not be empty or whitespace-only.

**Meaningful prompts**: Prompts must be complete questions or instructions, not fragments. They should not end with ellipsis or contain "etc."

**Appropriate length**: Descriptions should provide value. Single-word descriptions are usually insufficient. Descriptions over 200 characters should be reviewed for conciseness.

### 3.6 Validation Error Handling

When validation fails, the system must:

1. **Log the error** with full context including widget ID, widget type, validation error type, error message, and the invalid specification (for debugging).

2. **Attempt recovery** if possible. For minor issues (extra field, invalid default), consider sanitizing the specification rather than failing completely.

3. **Report to orchestration** layer that generation failed, enabling retry with error feedback.

4. **Never render invalid widgets**. An invalid widget specification must not be shown to users. Fallback to a generic error state or regeneration attempt.

### 3.7 Schema Compliance Verification Checklist

| Check | Verification |
|-------|--------------|
| Schema validation passes | Specification validates against JSON Schema for declared type |
| No extra properties | No fields beyond those defined in schema |
| Value uniqueness | All `value` fields unique within their array |
| Reference validity | All references (defaults, assignments) point to existing values |
| Constraint coherence | All numeric constraints are logically consistent |
| Content quality | No placeholders, empty strings, or fragment prompts |

---

## Part 4: Widget Response Standards

Widget responses must follow consistent formats to enable reliable processing by the orchestration layer.

### 4.1 Response Structure Requirements

Every widget response must include:

| Field | Requirement |
|-------|-------------|
| `widgetId` | Must match the widget specification's `id` |
| `widgetType` | Must match the widget specification's `type` |
| `timestamp` | ISO 8601 format, capture moment of submission |
| `responseType` | One of: `submitted`, `escaped`, `helpRequested`, `researchTriggered` |
| `value` | Required when `responseType` is `submitted`; type depends on widget |

### 4.2 Response Value Type Requirements

Response values must match the expected type for each widget:

| Widget Type | Required Value Type | Validation |
|-------------|---------------------|------------|
| `single-select` | `string` | Must match an option's `value` |
| `multi-select` | `string[]` | Each must match an option's `value` |
| `ranked-choice` | `string[]` | All item values in preference order |
| `pairwise-comparison` | `string[]` | Final ranking derived from comparisons |
| `slider` | `number` | Must be within `[min, max]` range |
| `opposing-spectrum` | `number` | Integer from 0 to `positions - 1` |
| `allocation` | `object` | Keys are category values, values are integers summing to `budget` |
| `tradeoff-table` | `object` | Nested object: option → criterion → rating |
| `ab-comparison` | `string` | Must be `optionA.value` or `optionB.value` |
| `card-sort` | `object` | Keys are category values, values are arrays of card values |
| `sequencer` | `string[]` | All item values in sequence order |
| `quadrant` | `object` | Keys are item values, values are `{x, y}` (0-100) |
| `madlib` | `object` | Keys are slot names, values are strings |
| `structured-fields` | `object` | Keys are field names, values match field types |
| `decision-gate` | `string` | Either `"proceed"` or `"goBack"` |
| `boundary-checklist` | `object` | `{checked: string[], added: string[]}` |
| `research-trigger` | `object` | `{proceed: boolean, brief: string}` |
| `merge-gate` | `object` | Depends on action taken |

### 4.3 Escape Response Requirements

When `responseType` is `"escaped"`:

- `value` may be absent or null
- `escapedExplanation` should contain the user's explanation if `promptForExplanation` was true
- The orchestration layer must handle escaped responses appropriately (typically by prompting for free-form input)

### 4.4 Response Validation

Before processing a widget response, validate that `widgetId` matches a known widget in the current workflow, `widgetType` matches the widget's actual type, `timestamp` is valid ISO 8601, `responseType` is one of the allowed values, `value` (if present) matches the expected type for this widget, and `value` contains valid references (option values, category values, etc.).

---

## Part 5: Testing and Verification Procedures

This section describes how to verify that widget implementations comply with these standards.

### 5.1 Schema Validation Testing

Every widget type schema must be tested with:

**Valid specification tests**: Confirm that well-formed specifications pass validation. Test with minimum required fields only. Test with all optional fields populated. Test with boundary values (min/max array lengths, string lengths).

**Invalid specification tests**: Confirm that malformed specifications fail validation. Test missing required fields (one at a time). Test invalid types for each field. Test constraint violations (min > max, etc.). Test extra properties (should fail due to `additionalProperties: false`). Test duplicate values in arrays.

### 5.2 Response Handling Testing

Every widget type must be tested for response handling:

**Submission tests**: Confirm valid responses are accepted. Test boundary values (empty selection, max selection). Confirm invalid responses are rejected with appropriate errors.

**Escape hatch tests**: Confirm escape hatch works when enabled. Confirm escape hatch is hidden when explicitly disabled. Confirm explanation prompt appears when configured.

**UX guarantee tests**: Confirm help button is present and functional. Confirm research trigger is present and spawns branch correctly.

### 5.3 Logging Compliance Testing

For each widget implementation, verify:

**Event emission**: `widget.presented` event fires on render. `widget.submitted` event fires on submission. Events contain all required fields.

**Payload completeness**: Presented event includes full specification. Submitted event includes full response.

### 5.4 Integration Testing

Test widgets in the context of actual workflows:

**Arc integration**: Test widgets at each questioning arc stage. Confirm responses correctly update workflow state. Confirm stage transitions work with widget responses.

**Branching integration**: Confirm research trigger spawns research branch. Confirm merge gate correctly handles branch proposals.

### 5.5 Compliance Certification

A widget implementation is certified compliant when:

1. All schema validation tests pass (valid and invalid cases)
2. All response handling tests pass
3. All logging compliance tests pass
4. Integration tests pass for at least one representative workflow

Document certification in the widget component's README or documentation.

---

## Part 6: Quality Standards for Widget Content

Beyond structural compliance, widget specifications should meet quality standards for the content they present.

### 6.1 Prompt Quality Standards

Prompts must be clear and actionable:

**Complete questions**: Prompts should be complete sentences ending with appropriate punctuation. Avoid fragments like "Select the option" without context.

**Specific**: Prompts should make clear what decision is being made. Avoid vague prompts like "What do you think?"

**Appropriate length**: Prompts should typically be 20-200 characters. Very short prompts lack context; very long prompts should be split with `helpText`.

**Neutral tone**: Prompts should not lead the user toward a particular answer unless intentionally designed to do so.

### 6.2 Option Quality Standards

Options presented to users must be:

**Distinct**: Each option should represent a meaningfully different choice. Overlapping options confuse users.

**Complete**: The set of options should cover the reasonable answer space. This is why escape hatch is required—but escape hatch should be rare, not common.

**Balanced**: Options should be presented fairly. Don't make one option obviously better through description length or positive language.

**Understandable**: Labels should be clear to the target user. Avoid jargon unless the context warrants it.

### 6.3 Help Content Quality Standards

When help content is provided (rather than generated on demand):

**Helpful**: Content should actually help the user think about the decision, not just restate the prompt.

**Examples**: Good help content often includes examples or scenarios.

**Neutral**: Help content should not push the user toward a particular answer.

**Appropriate length**: Help content should be 50-500 characters typically.

### 6.4 Content Review Checklist

| Check | Standard |
|-------|----------|
| Prompt clarity | Is the question/instruction clear and complete? |
| Prompt specificity | Is it clear what decision is being made? |
| Option distinctness | Are options meaningfully different? |
| Option completeness | Do options cover the reasonable answer space? |
| Option balance | Are options presented fairly? |
| Help quality | Does help content actually help? |

---

## Part 7: Error Messages and Recovery

When standards violations occur, appropriate error handling ensures graceful degradation.

### 7.1 Validation Error Messages

Error messages must include:

**Error type**: What kind of validation failed (schema, uniqueness, reference, constraint, content).

**Location**: Which field or fields caused the failure.

**Expected value**: What was expected.

**Actual value**: What was received.

**Example**:
```
Schema validation error in widget-single-select-a1b2c3:
  Field: options
  Expected: array with minItems: 2
  Actual: array with 1 item
```

### 7.2 Recovery Procedures

**For minor issues** (recoverable): Extra fields can be stripped. Default values for missing optional fields can be applied. Invalid defaults can be removed (widget uses no default).

**For major issues** (not recoverable): Missing required fields, invalid type field, and invalid option references require regeneration.

### 7.3 Escalation

If recovery fails after 3 regeneration attempts, escalate by logging the full context for debugging, presenting a generic error to the user, and allowing the user to skip (if widget is not required) or enter free-form input.

---

## Appendix A: Quick Reference Tables

### A.1 Required Fields by Widget Type

| Widget Type | Type-Specific Required Fields |
|-------------|-------------------------------|
| `single-select` | `options` (min 2) |
| `multi-select` | `options` (min 2) |
| `ranked-choice` | `items` (min 3) |
| `pairwise-comparison` | `items` (min 3) |
| `slider` | `min`, `max`, `labels` |
| `opposing-spectrum` | `poles` |
| `allocation` | `categories` (min 2) |
| `tradeoff-table` | `options` (min 2), `criteria` (min 2) |
| `ab-comparison` | `optionA`, `optionB` |
| `card-sort` | `cards` (min 3), `categories` (min 2) |
| `sequencer` | `items` (min 2) |
| `quadrant` | `items` (min 2), `axes` |
| `madlib` | `template`, `slots` (min 1) |
| `structured-fields` | `fields` (min 1) |
| `decision-gate` | (none beyond common) |
| `boundary-checklist` | `checklistType`, `items` (min 1) |
| `research-trigger` | `researchQuestion` |
| `merge-gate` | `branchType`, `branchSummary`, `proposedChanges` |

### A.2 Mandatory Logging Events

| Event | When Logged | Required Payload |
|-------|-------------|------------------|
| `widget.presented` | Widget renders | Full widget specification |
| `widget.submitted` | User submits response | Full WidgetResponse object |

### A.3 Validation Priority Order

When validating, check in this order (stop on first failure):

1. Schema validation (type exists, required fields present, types correct)
2. Strict mode (no extra properties)
3. Value uniqueness
4. Reference validity
5. Constraint coherence
6. Content quality

---

## Appendix B: Glossary

**Constraint coherence**: The requirement that numeric constraints be logically consistent (e.g., min < max).

**Reference validity**: The requirement that default values and assignments reference existing option/item values.

**Schema compliance**: The requirement that widget specifications validate against their JSON Schema.

**Strict mode**: JSON Schema validation mode where `additionalProperties: false` rejects any unexpected fields.

**Value uniqueness**: The requirement that all `value` fields within an array be unique.

---

## Appendix C: Related Documents

- **DD-19-01**: Widget Schema and Rendering Specification (companion definition document)
- **RF-02-01**: LLM Orchestration Framework Research Findings
- **ADR-02-01**: Orchestration Selection
- **RF-07-01**: Widget Component Library Research Findings
- **ADR-07-01**: Widget Component Library Selection
- **DD-18-01**: Questioning Arc Definition
- **STD-18-01**: Questioning Arc Standards
- **DD-15-01**: Governance Definitions (audit logging requirements)
- **STD-15-01**: Governance Standards (audit event schema)

---

*End of Widget Schema Standards (STD-19-01)*
