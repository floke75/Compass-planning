---
id: DD-19-01
type: definition
area: 19-widget-schema
title: Widget Schema and Rendering Specification
status: draft
created: 2026-01-26
updated: 2026-02-03
author: compass-research
summary: Defines JSON schemas for all widget types with validation, interaction logging, and LLM generation guidelines
tags: [widgets, schema, json-schema, specification, zod]
related:
  - RF-02-01
  - ADR-02-01
  - RF-07-01
  - ADR-07-01
  - DD-18-01
  - STD-18-01
links:
  - rel: related
    target_id: "RF-02-01"
  - rel: related
    target_id: "ADR-02-01"
  - rel: related
    target_id: "RF-07-01"
  - rel: related
    target_id: "ADR-07-01"
  - rel: related
    target_id: "DD-18-01"
  - rel: related
    target_id: "STD-18-01"
  - rel: companion
    target_id: "STD-19-01"
  - rel: informed_by
    target_id: "RF-02-01"
  - rel: informed_by
    target_id: "RF-07-01"
  - rel: informed_by
    target_id: "ADR-02-01"
  - rel: informed_by
    target_id: "ADR-07-01"
companion: STD-19-01
informed_by: [RF-02-01, RF-07-01, ADR-02-01, ADR-07-01]
---

# Widget Schema and Rendering Specification

## Document Purpose

This document defines the JSON schemas that form the contract between LLM output and UI rendering in Compass. When the orchestration layer generates a widget specification, this schema determines what is valid. When the rendering layer receives a specification, this schema determines how to interpret it.

**Why this matters**: The widget schema is the critical boundary between two systemsthe LLM that generates specifications and the UI that renders them. A well-designed schema enables reliable generation (the LLM knows exactly what structure to produce) and consistent rendering (the UI knows exactly how to interpret the specification). A poorly designed schema leads to generation failures, rendering bugs, and debugging nightmares.

**What this document covers**:

- Complete enumeration of widget types with identifiers and categories
- Common schema fields required by every widget
- Type-specific JSON schemas for each widget in the Compass taxonomy
- Response schema for capturing user interactions
- Interaction logging format for analytics and debugging
- Validation rules for both schema compliance and semantic correctness
- Guidelines for LLM prompt construction to ensure reliable generation

**What this document does not cover**:

- Visual styling or CSS (implementation detail)
- Component library specifics (see ADR-07-01)
- Orchestration framework details (see ADR-02-01)
- Questioning arc logic (see DD-18-01)

**Audience**: Compass builders, LLM agents generating widget specifications, and developers implementing widget rendering.

---

## Part 1: Widget Type Enumeration

The Compass widget taxonomy derives from the System Definition (§2.2), which categorizes widgets by the cognitive task they support in planning conversations.

### 1.1 Complete Type Registry

The following table enumerates all widget types with their identifiers, categories, and primary use cases.

| Type Identifier | Category | Use Case | Rendering |
|-----------------|----------|----------|-----------|
| `single-select` | Choice | Select one option from a list | C1 native |
| `multi-select` | Choice | Select multiple options from a list | C1 native |
| `ranked-choice` | Choice | Order options by preference | Custom |
| `pairwise-comparison` | Choice | Compare two options repeatedly to build ranking | Custom |
| `slider` | Spectrum | Express position on a continuous scale | C1 native |
| `opposing-spectrum` | Spectrum | Position between two opposing concepts | Custom |
| `allocation` | Spectrum | Distribute a fixed budget across categories | Custom |
| `tradeoff-table` | Comparative | Evaluate options against multiple criteria | Custom |
| `ab-comparison` | Comparative | Direct comparison between two alternatives | C1 native |
| `card-sort` | Spatial | Organize items into categories | Custom |
| `sequencer` | Spatial | Arrange items in order (timeline, priority, dependency) | Custom |
| `quadrant` | Spatial | Place items on a 2D grid with labeled axes | Custom |
| `madlib` | Generative | Complete a structured template with fill-in-the-blank fields | C1 native |
| `structured-fields` | Generative | Fill required fields with structured input | C1 native |
| `decision-gate` | Meta | Checkpoint requiring explicit decision to proceed | C1 native |
| `boundary-checklist` | Meta | Verify dealbreakers and out-of-scope items | C1 native |
| `research-trigger` | Meta | Spawn a research branch for investigation | C1 native |
| `merge-gate` | Meta | Review and accept/reject branch proposals | Custom |

**Rendering column**: "C1 native" indicates the widget can render using Thesys C1's built-in components. "Custom" indicates the widget requires a custom shadcn/ui + dnd-kit implementation registered as a C1 custom component (per ADR-07-01).

### 1.2 Category Definitions

**Choice widgets** help users select from discrete options. They answer questions like "Which of these?" or "What's most important?" The cognitive task is evaluating and selecting.

**Spectrum widgets** help users express degree or magnitude. They answer questions like "How much?" or "Where on this scale?" The cognitive task is calibration and positioning.

**Comparative widgets** help users make trade-offs explicit. They answer questions like "How does A compare to B on criteria X?" The cognitive task is structured evaluation.

**Spatial widgets** help users organize and sequence. They answer questions like "What categories do these belong to?" or "What order should these be in?" The cognitive task is categorization and ordering.

**Generative widgets** help users create structured content. They answer questions like "Fill in these details" or "Complete this template." The cognitive task is constrained creation.

**Meta widgets** control workflow rather than capture content. They mark decision points, verify boundaries, trigger research, and manage branch merging. The cognitive task is process governance.

---

## Part 2: Common Schema Fields

Every widget specification includes a set of common fields that support consistent rendering and interaction handling. These fields appear in all widget types regardless of category.

### 2.1 Required Common Fields

Every widget must include these fields:

**`type`** (string, required): The widget type identifier from the registry (e.g., `"single-select"`). This determines which renderer handles the specification.

**`id`** (string, required): A unique identifier for this widget instance within the current workflow. Format: `widget-{type}-{uuid}` where uuid is a short unique string. Example: `"widget-single-select-a1b2c3"`.

**`prompt`** (string, required): The main question or instruction presented to the user. This should be clear, specific, and actionable. Maximum 500 characters.

**`required`** (boolean, required): Whether the user must respond before proceeding. Default: `true`. When `false`, the widget can be skipped.

### 2.2 Optional Common Fields

These fields are optional but recommended for better user experience:

**`helpText`** (string, optional): Additional context or explanation displayed below the prompt. Use for clarifications, examples, or constraints. Maximum 1000 characters.

**`escapeHatch`** (object, optional): Configuration for the "none of these fit" option that every widget must provide (per System Definition §2.2). When absent, a default escape hatch is rendered.

**`helpMeThink`** (object, optional): Configuration for the "help me think" support feature. When absent, a default help option is rendered.

**`researchTrigger`** (object, optional): Configuration for the "research this" action that can spawn a research branch. When absent, a default research trigger is rendered.

**`meta`** (object, optional): Additional metadata for rendering and analytics. Contains `questioningArcStage` (which stage this widget appears in), `priority` (display priority when multiple widgets are presented), and `tags` (array of strings for categorization).

### 2.3 Common Schema Definition

The following JSON Schema defines the common fields. All widget-specific schemas extend this base.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "compass-widget-common",
  "title": "CommonWidgetFields",
  "type": "object",
  "properties": {
    "type": {
      "type": "string",
      "description": "The widget type identifier that determines rendering behavior"
    },
    "id": {
      "type": "string",
      "pattern": "^widget-[a-z-]+-[a-z0-9]+$",
      "description": "Unique identifier for this widget instance"
    },
    "prompt": {
      "type": "string",
      "maxLength": 500,
      "description": "The main question or instruction presented to the user"
    },
    "required": {
      "type": "boolean",
      "default": true,
      "description": "Whether the user must respond before proceeding"
    },
    "helpText": {
      "type": "string",
      "maxLength": 1000,
      "description": "Additional context displayed below the prompt"
    },
    "escapeHatch": {
      "type": "object",
      "properties": {
        "enabled": {
          "type": "boolean",
          "default": true,
          "description": "Whether escape hatch is available"
        },
        "label": {
          "type": "string",
          "default": "None of these fit / I'll describe instead",
          "description": "Text for the escape hatch option"
        },
        "promptForExplanation": {
          "type": "boolean",
          "default": true,
          "description": "Whether to show text input when escape hatch is selected"
        }
      },
      "additionalProperties": false,
      "description": "Configuration for the none-of-these option"
    },
    "helpMeThink": {
      "type": "object",
      "properties": {
        "enabled": {
          "type": "boolean",
          "default": true,
          "description": "Whether help option is available"
        },
        "label": {
          "type": "string",
          "default": "Help me think about this",
          "description": "Text for the help button"
        },
        "content": {
          "type": "string",
          "description": "Pre-written help content; if absent, generated on demand"
        }
      },
      "additionalProperties": false,
      "description": "Configuration for help/support feature"
    },
    "researchTrigger": {
      "type": "object",
      "properties": {
        "enabled": {
          "type": "boolean",
          "default": true,
          "description": "Whether research trigger is available"
        },
        "label": {
          "type": "string",
          "default": "Research this",
          "description": "Text for the research trigger button"
        },
        "defaultBrief": {
          "type": "string",
          "description": "Pre-filled research brief when triggered"
        }
      },
      "additionalProperties": false,
      "description": "Configuration for research branch trigger"
    },
    "meta": {
      "type": "object",
      "properties": {
        "questioningArcStage": {
          "type": "string",
          "enum": ["OPEN", "FOLLOW", "SHARPEN", "BOUNDARY", "GROUND"],
          "description": "Which arc stage this widget appears in"
        },
        "priority": {
          "type": "integer",
          "minimum": 1,
          "maximum": 10,
          "default": 5,
          "description": "Display priority (1=highest)"
        },
        "tags": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Tags for categorization and filtering"
        }
      },
      "additionalProperties": false,
      "description": "Additional metadata for rendering and analytics"
    }
  },
  "required": ["type", "id", "prompt", "required"],
  "additionalProperties": false
}
```

---

## Part 3: Choice Widget Schemas

Choice widgets help users select from discrete options. They range from simple single selection to complex preference ranking.

### 3.1 Single Select

Single select presents a list of options where the user chooses exactly one. This is the most common widget type, suitable for any "pick one" decision.

**When to use**: Use single select when options are mutually exclusive and no ranking is needed. Examples: "Which approach should we prioritize?" "What's the primary user type?"

**Schema**:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "compass-widget-single-select",
  "title": "SingleSelectWidget",
  "type": "object",
  "properties": {
    "type": { "const": "single-select" },
    "id": { "type": "string", "pattern": "^widget-single-select-[a-z0-9]+$" },
    "prompt": { "type": "string", "maxLength": 500 },
    "required": { "type": "boolean", "default": true },
    "helpText": { "type": "string", "maxLength": 1000 },
    "escapeHatch": { "$ref": "#/definitions/escapeHatch" },
    "helpMeThink": { "$ref": "#/definitions/helpMeThink" },
    "researchTrigger": { "$ref": "#/definitions/researchTrigger" },
    "meta": { "$ref": "#/definitions/meta" },
    "options": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "value": {
            "type": "string",
            "description": "Machine-readable identifier for this option"
          },
          "label": {
            "type": "string",
            "description": "Human-readable text displayed to user"
          },
          "description": {
            "type": "string",
            "description": "Optional additional context for this option"
          }
        },
        "required": ["value", "label"],
        "additionalProperties": false
      },
      "minItems": 2,
      "maxItems": 10,
      "description": "List of options to choose from"
    },
    "defaultValue": {
      "type": "string",
      "description": "Value of pre-selected option, if any"
    },
    "layout": {
      "type": "string",
      "enum": ["vertical", "horizontal", "grid"],
      "default": "vertical",
      "description": "How options are arranged visually"
    }
  },
  "required": ["type", "id", "prompt", "required", "options"],
  "additionalProperties": false
}
```

**Example specification**:

```json
{
  "type": "single-select",
  "id": "widget-single-select-a1b2c3",
  "prompt": "Which user type should we prioritize for the first release?",
  "required": true,
  "helpText": "Consider who would get the most value from early access.",
  "options": [
    {
      "value": "power-users",
      "label": "Power users",
      "description": "Heavy daily users who need advanced features"
    },
    {
      "value": "occasional-users",
      "label": "Occasional users",
      "description": "Infrequent users who need simplicity"
    },
    {
      "value": "new-users",
      "label": "New users",
      "description": "First-time users who need onboarding"
    }
  ],
  "meta": {
    "questioningArcStage": "SHARPEN",
    "priority": 1
  }
}
```

### 3.2 Multi Select

Multi select presents a list of options where the user can choose multiple items. The selection is unordered—if order matters, use ranked choice instead.

**When to use**: Use multi select when options are not mutually exclusive and the user may want several. Examples: "Which features are must-haves?" "What integrations do you need?"

**Schema**:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "compass-widget-multi-select",
  "title": "MultiSelectWidget",
  "type": "object",
  "properties": {
    "type": { "const": "multi-select" },
    "id": { "type": "string", "pattern": "^widget-multi-select-[a-z0-9]+$" },
    "prompt": { "type": "string", "maxLength": 500 },
    "required": { "type": "boolean", "default": true },
    "helpText": { "type": "string", "maxLength": 1000 },
    "escapeHatch": { "$ref": "#/definitions/escapeHatch" },
    "helpMeThink": { "$ref": "#/definitions/helpMeThink" },
    "researchTrigger": { "$ref": "#/definitions/researchTrigger" },
    "meta": { "$ref": "#/definitions/meta" },
    "options": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "value": { "type": "string" },
          "label": { "type": "string" },
          "description": { "type": "string" }
        },
        "required": ["value", "label"],
        "additionalProperties": false
      },
      "minItems": 2,
      "maxItems": 20,
      "description": "List of options to choose from"
    },
    "defaultValues": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Values of pre-selected options"
    },
    "minSelections": {
      "type": "integer",
      "minimum": 0,
      "default": 0,
      "description": "Minimum number of selections required"
    },
    "maxSelections": {
      "type": "integer",
      "minimum": 1,
      "description": "Maximum number of selections allowed"
    }
  },
  "required": ["type", "id", "prompt", "required", "options"],
  "additionalProperties": false
}
```

### 3.3 Ranked Choice

Ranked choice presents a list of items that the user reorders by preference. This is critical for prioritization decisions where relative order matters, not just selection.

**When to use**: Use ranked choice when you need to understand preference ordering. Examples: "Rank these features by implementation priority." "Order these user needs from most to least important."

**Schema**:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "compass-widget-ranked-choice",
  "title": "RankedChoiceWidget",
  "type": "object",
  "properties": {
    "type": { "const": "ranked-choice" },
    "id": { "type": "string", "pattern": "^widget-ranked-choice-[a-z0-9]+$" },
    "prompt": { "type": "string", "maxLength": 500 },
    "required": { "type": "boolean", "default": true },
    "helpText": { "type": "string", "maxLength": 1000 },
    "escapeHatch": { "$ref": "#/definitions/escapeHatch" },
    "helpMeThink": { "$ref": "#/definitions/helpMeThink" },
    "researchTrigger": { "$ref": "#/definitions/researchTrigger" },
    "meta": { "$ref": "#/definitions/meta" },
    "items": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "value": { "type": "string" },
          "label": { "type": "string" },
          "description": { "type": "string" }
        },
        "required": ["value", "label"],
        "additionalProperties": false
      },
      "minItems": 3,
      "maxItems": 10,
      "description": "Items to be ranked; initial order is the default ranking"
    },
    "rankingLabels": {
      "type": "object",
      "properties": {
        "top": {
          "type": "string",
          "default": "Most important",
          "description": "Label for the top position"
        },
        "bottom": {
          "type": "string",
          "default": "Least important",
          "description": "Label for the bottom position"
        }
      },
      "additionalProperties": false,
      "description": "Labels explaining what the ranking means"
    },
    "allowTies": {
      "type": "boolean",
      "default": false,
      "description": "Whether items can share the same rank"
    }
  },
  "required": ["type", "id", "prompt", "required", "items"],
  "additionalProperties": false
}
```

**Example specification**:

```json
{
  "type": "ranked-choice",
  "id": "widget-ranked-choice-d4e5f6",
  "prompt": "Rank these five features by implementation priority.",
  "required": true,
  "helpText": "Drag items to reorder. The top item will be implemented first.",
  "items": [
    { "value": "search", "label": "Full-text search" },
    { "value": "export", "label": "PDF export" },
    { "value": "collab", "label": "Real-time collaboration" },
    { "value": "mobile", "label": "Mobile app" },
    { "value": "api", "label": "Public API" }
  ],
  "rankingLabels": {
    "top": "Implement first",
    "bottom": "Implement last"
  },
  "allowTies": false,
  "meta": {
    "questioningArcStage": "SHARPEN"
  }
}
```

### 3.4 Pairwise Comparison

Pairwise comparison presents options two at a time, asking the user to choose the preferred one repeatedly. This builds a ranking through a series of simpler binary decisions, which can be more reliable for complex prioritization.

**When to use**: Use pairwise comparison when ranking many items is cognitively difficult, or when you want to validate prioritization through redundant comparisons. Examples: "Compare these approaches two at a time to determine which is most important."

**Schema**:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "compass-widget-pairwise-comparison",
  "title": "PairwiseComparisonWidget",
  "type": "object",
  "properties": {
    "type": { "const": "pairwise-comparison" },
    "id": { "type": "string", "pattern": "^widget-pairwise-comparison-[a-z0-9]+$" },
    "prompt": { "type": "string", "maxLength": 500 },
    "required": { "type": "boolean", "default": true },
    "helpText": { "type": "string", "maxLength": 1000 },
    "escapeHatch": { "$ref": "#/definitions/escapeHatch" },
    "helpMeThink": { "$ref": "#/definitions/helpMeThink" },
    "researchTrigger": { "$ref": "#/definitions/researchTrigger" },
    "meta": { "$ref": "#/definitions/meta" },
    "items": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "value": { "type": "string" },
          "label": { "type": "string" },
          "description": { "type": "string" }
        },
        "required": ["value", "label"],
        "additionalProperties": false
      },
      "minItems": 3,
      "maxItems": 8,
      "description": "Items to compare pairwise"
    },
    "comparisonQuestion": {
      "type": "string",
      "default": "Which is more important?",
      "description": "Question asked for each pair comparison"
    },
    "allowTie": {
      "type": "boolean",
      "default": true,
      "description": "Whether 'equal' is a valid response"
    },
    "algorithm": {
      "type": "string",
      "enum": ["round-robin", "swiss", "adaptive"],
      "default": "adaptive",
      "description": "How pairs are selected: round-robin shows all pairs, swiss reduces comparisons, adaptive adjusts based on responses"
    }
  },
  "required": ["type", "id", "prompt", "required", "items"],
  "additionalProperties": false
}
```

---

## Part 4: Spectrum Widget Schemas

Spectrum widgets help users express degree, magnitude, or distribution across a scale or budget.

### 4.1 Slider

Slider presents a continuous scale with labeled endpoints. The user positions a handle to indicate their preference along the spectrum.

**When to use**: Use slider when the answer is a position on a continuum rather than a discrete choice. Examples: "How important is real-time updates?" (Not important ↔ Critical) "What latency is acceptable?" (<100ms ↔ <10s)

**Schema**:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "compass-widget-slider",
  "title": "SliderWidget",
  "type": "object",
  "properties": {
    "type": { "const": "slider" },
    "id": { "type": "string", "pattern": "^widget-slider-[a-z0-9]+$" },
    "prompt": { "type": "string", "maxLength": 500 },
    "required": { "type": "boolean", "default": true },
    "helpText": { "type": "string", "maxLength": 1000 },
    "escapeHatch": { "$ref": "#/definitions/escapeHatch" },
    "helpMeThink": { "$ref": "#/definitions/helpMeThink" },
    "researchTrigger": { "$ref": "#/definitions/researchTrigger" },
    "meta": { "$ref": "#/definitions/meta" },
    "min": {
      "type": "number",
      "description": "Minimum value on the scale"
    },
    "max": {
      "type": "number",
      "description": "Maximum value on the scale"
    },
    "step": {
      "type": "number",
      "default": 1,
      "description": "Increment between valid values"
    },
    "defaultValue": {
      "type": "number",
      "description": "Initial position of the slider"
    },
    "labels": {
      "type": "object",
      "properties": {
        "min": {
          "type": "string",
          "description": "Label for minimum end"
        },
        "max": {
          "type": "string",
          "description": "Label for maximum end"
        },
        "mid": {
          "type": "string",
          "description": "Label for midpoint (optional)"
        }
      },
      "required": ["min", "max"],
      "additionalProperties": false,
      "description": "Text labels for scale positions"
    },
    "showValue": {
      "type": "boolean",
      "default": true,
      "description": "Whether to display the current numeric value"
    },
    "unit": {
      "type": "string",
      "description": "Unit suffix for the value (e.g., 'ms', '%', 'days')"
    }
  },
  "required": ["type", "id", "prompt", "required", "min", "max", "labels"],
  "additionalProperties": false
}
```

**Example specification**:

```json
{
  "type": "slider",
  "id": "widget-slider-g7h8i9",
  "prompt": "What latency is acceptable for search results?",
  "required": true,
  "min": 100,
  "max": 10000,
  "step": 100,
  "defaultValue": 500,
  "labels": {
    "min": "Instant (<100ms)",
    "max": "Slow but thorough (<10s)",
    "mid": "Balanced (~1s)"
  },
  "showValue": true,
  "unit": "ms"
}
```

### 4.2 Opposing Spectrum

Opposing spectrum presents a scale between two conceptual opposites. Unlike slider which has a numeric range, opposing spectrum captures trade-offs between qualitative poles.

**When to use**: Use opposing spectrum when the decision is between two valid but competing values. Examples: "Where on the spectrum between 'simple but limited' and 'powerful but complex'?" "Between 'move fast' and 'be thorough'?"

**Schema**:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "compass-widget-opposing-spectrum",
  "title": "OpposingSpectrumWidget",
  "type": "object",
  "properties": {
    "type": { "const": "opposing-spectrum" },
    "id": { "type": "string", "pattern": "^widget-opposing-spectrum-[a-z0-9]+$" },
    "prompt": { "type": "string", "maxLength": 500 },
    "required": { "type": "boolean", "default": true },
    "helpText": { "type": "string", "maxLength": 1000 },
    "escapeHatch": { "$ref": "#/definitions/escapeHatch" },
    "helpMeThink": { "$ref": "#/definitions/helpMeThink" },
    "researchTrigger": { "$ref": "#/definitions/researchTrigger" },
    "meta": { "$ref": "#/definitions/meta" },
    "poles": {
      "type": "object",
      "properties": {
        "left": {
          "type": "object",
          "properties": {
            "label": { "type": "string" },
            "description": { "type": "string" }
          },
          "required": ["label"],
          "additionalProperties": false
        },
        "right": {
          "type": "object",
          "properties": {
            "label": { "type": "string" },
            "description": { "type": "string" }
          },
          "required": ["label"],
          "additionalProperties": false
        }
      },
      "required": ["left", "right"],
      "additionalProperties": false,
      "description": "The two opposing concepts"
    },
    "positions": {
      "type": "integer",
      "enum": [3, 5, 7],
      "default": 5,
      "description": "Number of positions on the scale (odd number for center option)"
    },
    "defaultPosition": {
      "type": "integer",
      "description": "Initial position (0 = full left, max = full right)"
    },
    "positionLabels": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Optional labels for each position"
    }
  },
  "required": ["type", "id", "prompt", "required", "poles"],
  "additionalProperties": false
}
```

### 4.3 Allocation

Allocation presents a fixed budget (typically 100 points) that the user distributes across multiple categories. This forces explicit trade-offs—giving more to one category means less for others.

**When to use**: Use allocation when you need to understand relative priority across categories where everything matters somewhat. Examples: "Distribute 100 points across these five goals based on importance." "Allocate your time budget across these workstreams."

**Schema**:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "compass-widget-allocation",
  "title": "AllocationWidget",
  "type": "object",
  "properties": {
    "type": { "const": "allocation" },
    "id": { "type": "string", "pattern": "^widget-allocation-[a-z0-9]+$" },
    "prompt": { "type": "string", "maxLength": 500 },
    "required": { "type": "boolean", "default": true },
    "helpText": { "type": "string", "maxLength": 1000 },
    "escapeHatch": { "$ref": "#/definitions/escapeHatch" },
    "helpMeThink": { "$ref": "#/definitions/helpMeThink" },
    "researchTrigger": { "$ref": "#/definitions/researchTrigger" },
    "meta": { "$ref": "#/definitions/meta" },
    "budget": {
      "type": "integer",
      "default": 100,
      "minimum": 10,
      "maximum": 1000,
      "description": "Total points/units to distribute"
    },
    "categories": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "value": { "type": "string" },
          "label": { "type": "string" },
          "description": { "type": "string" },
          "minAllocation": {
            "type": "integer",
            "default": 0,
            "description": "Minimum points that must be allocated"
          },
          "maxAllocation": {
            "type": "integer",
            "description": "Maximum points that can be allocated"
          }
        },
        "required": ["value", "label"],
        "additionalProperties": false
      },
      "minItems": 2,
      "maxItems": 10,
      "description": "Categories to allocate budget across"
    },
    "defaultAllocations": {
      "type": "object",
      "additionalProperties": { "type": "integer" },
      "description": "Initial allocation per category (keyed by value)"
    },
    "showPercentages": {
      "type": "boolean",
      "default": true,
      "description": "Whether to display percentages alongside points"
    }
  },
  "required": ["type", "id", "prompt", "required", "categories"],
  "additionalProperties": false
}
```

**Example specification**:

```json
{
  "type": "allocation",
  "id": "widget-allocation-j1k2l3",
  "prompt": "Distribute 100 points across these goals based on their importance for Phase 1.",
  "required": true,
  "budget": 100,
  "categories": [
    { "value": "speed", "label": "Development speed", "description": "Ship quickly" },
    { "value": "quality", "label": "Code quality", "description": "Maintainable, tested" },
    { "value": "features", "label": "Feature completeness", "description": "Full scope" },
    { "value": "ux", "label": "User experience", "description": "Polish and usability" }
  ],
  "defaultAllocations": {
    "speed": 25,
    "quality": 25,
    "features": 25,
    "ux": 25
  },
  "showPercentages": true
}
```

---

## Part 5: Comparative Widget Schemas

Comparative widgets help users evaluate options against criteria, making trade-offs explicit and structured.

### 5.1 Trade-off Table

Trade-off table presents a matrix of options (rows) and criteria (columns). Users score how well each option meets each criterion, producing a structured comparison.

**When to use**: Use trade-off table when choosing between options that each have different strengths and weaknesses across multiple dimensions. Examples: "Compare these three vendor options across cost, features, and support." "Evaluate these architectures against performance, maintainability, and complexity."

**Schema**:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "compass-widget-tradeoff-table",
  "title": "TradeoffTableWidget",
  "type": "object",
  "properties": {
    "type": { "const": "tradeoff-table" },
    "id": { "type": "string", "pattern": "^widget-tradeoff-table-[a-z0-9]+$" },
    "prompt": { "type": "string", "maxLength": 500 },
    "required": { "type": "boolean", "default": true },
    "helpText": { "type": "string", "maxLength": 1000 },
    "escapeHatch": { "$ref": "#/definitions/escapeHatch" },
    "helpMeThink": { "$ref": "#/definitions/helpMeThink" },
    "researchTrigger": { "$ref": "#/definitions/researchTrigger" },
    "meta": { "$ref": "#/definitions/meta" },
    "options": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "value": { "type": "string" },
          "label": { "type": "string" },
          "description": { "type": "string" }
        },
        "required": ["value", "label"],
        "additionalProperties": false
      },
      "minItems": 2,
      "maxItems": 6,
      "description": "Options being compared (rows)"
    },
    "criteria": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "value": { "type": "string" },
          "label": { "type": "string" },
          "description": { "type": "string" },
          "weight": {
            "type": "number",
            "minimum": 0,
            "maximum": 1,
            "default": 1,
            "description": "Relative importance of this criterion (for weighted scoring)"
          }
        },
        "required": ["value", "label"],
        "additionalProperties": false
      },
      "minItems": 2,
      "maxItems": 8,
      "description": "Criteria to evaluate against (columns)"
    },
    "ratingScale": {
      "type": "object",
      "properties": {
        "min": { "type": "integer", "default": 1 },
        "max": { "type": "integer", "default": 5 },
        "labels": {
          "type": "object",
          "additionalProperties": { "type": "string" },
          "description": "Labels for rating values (e.g., {1: 'Poor', 5: 'Excellent'})"
        }
      },
      "additionalProperties": false,
      "description": "Rating scale configuration"
    },
    "prefilled": {
      "type": "object",
      "additionalProperties": {
        "type": "object",
        "additionalProperties": { "type": "integer" }
      },
      "description": "Pre-filled ratings keyed by option.value then criteria.value"
    },
    "showWeightedScores": {
      "type": "boolean",
      "default": true,
      "description": "Whether to display calculated weighted scores"
    }
  },
  "required": ["type", "id", "prompt", "required", "options", "criteria"],
  "additionalProperties": false
}
```

### 5.2 A/B Comparison

A/B comparison presents two alternatives side by side for direct comparison. This is simpler than a full trade-off table and focuses attention on comparing exactly two options.

**When to use**: Use A/B comparison when the decision is between two specific alternatives. Examples: "Which of these two approaches better fits our needs?" "Compare Option A and Option B on these dimensions."

**Schema**:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "compass-widget-ab-comparison",
  "title": "ABComparisonWidget",
  "type": "object",
  "properties": {
    "type": { "const": "ab-comparison" },
    "id": { "type": "string", "pattern": "^widget-ab-comparison-[a-z0-9]+$" },
    "prompt": { "type": "string", "maxLength": 500 },
    "required": { "type": "boolean", "default": true },
    "helpText": { "type": "string", "maxLength": 1000 },
    "escapeHatch": { "$ref": "#/definitions/escapeHatch" },
    "helpMeThink": { "$ref": "#/definitions/helpMeThink" },
    "researchTrigger": { "$ref": "#/definitions/researchTrigger" },
    "meta": { "$ref": "#/definitions/meta" },
    "optionA": {
      "type": "object",
      "properties": {
        "value": { "type": "string" },
        "label": { "type": "string" },
        "description": { "type": "string" },
        "pros": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Advantages of this option"
        },
        "cons": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Disadvantages of this option"
        }
      },
      "required": ["value", "label"],
      "additionalProperties": false
    },
    "optionB": {
      "type": "object",
      "properties": {
        "value": { "type": "string" },
        "label": { "type": "string" },
        "description": { "type": "string" },
        "pros": {
          "type": "array",
          "items": { "type": "string" }
        },
        "cons": {
          "type": "array",
          "items": { "type": "string" }
        }
      },
      "required": ["value", "label"],
      "additionalProperties": false
    },
    "comparisonDimensions": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "label": { "type": "string" },
          "valueA": { "type": "string" },
          "valueB": { "type": "string" }
        },
        "required": ["label", "valueA", "valueB"],
        "additionalProperties": false
      },
      "description": "Side-by-side comparison data for specific dimensions"
    },
    "selectionRequired": {
      "type": "boolean",
      "default": true,
      "description": "Whether user must choose one (vs. just reviewing)"
    }
  },
  "required": ["type", "id", "prompt", "required", "optionA", "optionB"],
  "additionalProperties": false
}
```

---

## Part 6: Spatial Widget Schemas

Spatial widgets help users organize, categorize, and sequence items visually.

### 6.1 Card Sort

Card sort presents items as cards that the user drags into categories. This is useful for understanding how users conceptualize groupings.

**When to use**: Use card sort when you need to understand how items should be organized. Examples: "Group these features into release phases." "Categorize these requirements by stakeholder."

**Schema**:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "compass-widget-card-sort",
  "title": "CardSortWidget",
  "type": "object",
  "properties": {
    "type": { "const": "card-sort" },
    "id": { "type": "string", "pattern": "^widget-card-sort-[a-z0-9]+$" },
    "prompt": { "type": "string", "maxLength": 500 },
    "required": { "type": "boolean", "default": true },
    "helpText": { "type": "string", "maxLength": 1000 },
    "escapeHatch": { "$ref": "#/definitions/escapeHatch" },
    "helpMeThink": { "$ref": "#/definitions/helpMeThink" },
    "researchTrigger": { "$ref": "#/definitions/researchTrigger" },
    "meta": { "$ref": "#/definitions/meta" },
    "cards": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "value": { "type": "string" },
          "label": { "type": "string" },
          "description": { "type": "string" }
        },
        "required": ["value", "label"],
        "additionalProperties": false
      },
      "minItems": 3,
      "maxItems": 30,
      "description": "Items to be sorted"
    },
    "categories": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "value": { "type": "string" },
          "label": { "type": "string" },
          "description": { "type": "string" },
          "color": { "type": "string", "description": "Optional hex color for visual distinction" }
        },
        "required": ["value", "label"],
        "additionalProperties": false
      },
      "minItems": 2,
      "maxItems": 10,
      "description": "Categories to sort cards into"
    },
    "allowNewCategories": {
      "type": "boolean",
      "default": false,
      "description": "Whether user can create additional categories"
    },
    "allowUncategorized": {
      "type": "boolean",
      "default": true,
      "description": "Whether cards can remain unsorted"
    },
    "defaultAssignments": {
      "type": "object",
      "additionalProperties": { "type": "string" },
      "description": "Initial category assignments (card value → category value)"
    }
  },
  "required": ["type", "id", "prompt", "required", "cards", "categories"],
  "additionalProperties": false
}
```

### 6.2 Sequencer

Sequencer presents items that the user arranges in a specific order, representing timeline, priority, dependency, or any other sequence.

**When to use**: Use sequencer when order represents something meaningful like time, priority, or dependency. Unlike ranked choice (which is about preference), sequencer is about logical ordering. Examples: "Arrange these phases in implementation order." "Order these tasks by dependency (do first → do last)."

**Schema**:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "compass-widget-sequencer",
  "title": "SequencerWidget",
  "type": "object",
  "properties": {
    "type": { "const": "sequencer" },
    "id": { "type": "string", "pattern": "^widget-sequencer-[a-z0-9]+$" },
    "prompt": { "type": "string", "maxLength": 500 },
    "required": { "type": "boolean", "default": true },
    "helpText": { "type": "string", "maxLength": 1000 },
    "escapeHatch": { "$ref": "#/definitions/escapeHatch" },
    "helpMeThink": { "$ref": "#/definitions/helpMeThink" },
    "researchTrigger": { "$ref": "#/definitions/researchTrigger" },
    "meta": { "$ref": "#/definitions/meta" },
    "items": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "value": { "type": "string" },
          "label": { "type": "string" },
          "description": { "type": "string" },
          "constraints": {
            "type": "object",
            "properties": {
              "mustBefore": {
                "type": "array",
                "items": { "type": "string" },
                "description": "Values of items that must come after this one"
              },
              "mustAfter": {
                "type": "array",
                "items": { "type": "string" },
                "description": "Values of items that must come before this one"
              }
            },
            "additionalProperties": false,
            "description": "Ordering constraints for validation"
          }
        },
        "required": ["value", "label"],
        "additionalProperties": false
      },
      "minItems": 2,
      "maxItems": 15,
      "description": "Items to be sequenced"
    },
    "sequenceLabels": {
      "type": "object",
      "properties": {
        "start": { "type": "string", "default": "First" },
        "end": { "type": "string", "default": "Last" }
      },
      "additionalProperties": false,
      "description": "Labels for sequence endpoints"
    },
    "orientation": {
      "type": "string",
      "enum": ["horizontal", "vertical"],
      "default": "vertical",
      "description": "Visual layout direction"
    },
    "showConnectors": {
      "type": "boolean",
      "default": true,
      "description": "Whether to show arrows/lines between items"
    }
  },
  "required": ["type", "id", "prompt", "required", "items"],
  "additionalProperties": false
}
```

### 6.3 Quadrant

Quadrant presents a 2D grid with labeled axes where users place items. This is useful for two-dimensional prioritization (e.g., importance vs. urgency, impact vs. effort).

**When to use**: Use quadrant when decisions benefit from two-axis thinking. Examples: "Place these features on an impact vs. effort matrix." "Position these risks by likelihood and severity."

**Schema**:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "compass-widget-quadrant",
  "title": "QuadrantWidget",
  "type": "object",
  "properties": {
    "type": { "const": "quadrant" },
    "id": { "type": "string", "pattern": "^widget-quadrant-[a-z0-9]+$" },
    "prompt": { "type": "string", "maxLength": 500 },
    "required": { "type": "boolean", "default": true },
    "helpText": { "type": "string", "maxLength": 1000 },
    "escapeHatch": { "$ref": "#/definitions/escapeHatch" },
    "helpMeThink": { "$ref": "#/definitions/helpMeThink" },
    "researchTrigger": { "$ref": "#/definitions/researchTrigger" },
    "meta": { "$ref": "#/definitions/meta" },
    "items": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "value": { "type": "string" },
          "label": { "type": "string" },
          "description": { "type": "string" }
        },
        "required": ["value", "label"],
        "additionalProperties": false
      },
      "minItems": 2,
      "maxItems": 20,
      "description": "Items to place on the quadrant"
    },
    "axes": {
      "type": "object",
      "properties": {
        "x": {
          "type": "object",
          "properties": {
            "label": { "type": "string" },
            "lowLabel": { "type": "string" },
            "highLabel": { "type": "string" }
          },
          "required": ["label", "lowLabel", "highLabel"],
          "additionalProperties": false
        },
        "y": {
          "type": "object",
          "properties": {
            "label": { "type": "string" },
            "lowLabel": { "type": "string" },
            "highLabel": { "type": "string" }
          },
          "required": ["label", "lowLabel", "highLabel"],
          "additionalProperties": false
        }
      },
      "required": ["x", "y"],
      "additionalProperties": false,
      "description": "Axis definitions"
    },
    "quadrantLabels": {
      "type": "object",
      "properties": {
        "topLeft": { "type": "string" },
        "topRight": { "type": "string" },
        "bottomLeft": { "type": "string" },
        "bottomRight": { "type": "string" }
      },
      "additionalProperties": false,
      "description": "Optional labels for each quadrant"
    },
    "defaultPositions": {
      "type": "object",
      "additionalProperties": {
        "type": "object",
        "properties": {
          "x": { "type": "number", "minimum": 0, "maximum": 100 },
          "y": { "type": "number", "minimum": 0, "maximum": 100 }
        },
        "required": ["x", "y"],
        "additionalProperties": false
      },
      "description": "Initial positions (item value → {x, y} percentage)"
    }
  },
  "required": ["type", "id", "prompt", "required", "items", "axes"],
  "additionalProperties": false
}
```

**Example specification**:

```json
{
  "type": "quadrant",
  "id": "widget-quadrant-m4n5o6",
  "prompt": "Place each feature on this impact vs. effort matrix.",
  "required": true,
  "helpText": "Drag items to position them. Top-right items are high-impact, high-effort.",
  "items": [
    { "value": "search", "label": "Full-text search" },
    { "value": "export", "label": "PDF export" },
    { "value": "collab", "label": "Real-time collaboration" },
    { "value": "mobile", "label": "Mobile app" }
  ],
  "axes": {
    "x": {
      "label": "Effort",
      "lowLabel": "Easy",
      "highLabel": "Hard"
    },
    "y": {
      "label": "Impact",
      "lowLabel": "Low impact",
      "highLabel": "High impact"
    }
  },
  "quadrantLabels": {
    "topLeft": "Quick wins",
    "topRight": "Major projects",
    "bottomLeft": "Fill-ins",
    "bottomRight": "Thankless tasks"
  }
}
```

---

## Part 7: Generative Widget Schemas

Generative widgets help users create structured content through constrained creation rather than freeform input.

### 7.1 Mad-lib

Mad-lib presents a template with fill-in-the-blank slots. The user completes the template by providing specific values for each slot.

**When to use**: Use mad-lib when you want structured input that follows a specific pattern. Examples: "Complete this user story template: As a [role], I want [capability] so that [benefit]." "Fill in this constraint statement: Must support [number] concurrent users with [latency] response time."

**Schema**:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "compass-widget-madlib",
  "title": "MadlibWidget",
  "type": "object",
  "properties": {
    "type": { "const": "madlib" },
    "id": { "type": "string", "pattern": "^widget-madlib-[a-z0-9]+$" },
    "prompt": { "type": "string", "maxLength": 500 },
    "required": { "type": "boolean", "default": true },
    "helpText": { "type": "string", "maxLength": 1000 },
    "escapeHatch": { "$ref": "#/definitions/escapeHatch" },
    "helpMeThink": { "$ref": "#/definitions/helpMeThink" },
    "researchTrigger": { "$ref": "#/definitions/researchTrigger" },
    "meta": { "$ref": "#/definitions/meta" },
    "template": {
      "type": "string",
      "description": "Template text with placeholders in {{slotName}} format"
    },
    "slots": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": {
            "type": "string",
            "description": "Slot identifier matching {{name}} in template"
          },
          "label": {
            "type": "string",
            "description": "Human-readable label for the input"
          },
          "placeholder": {
            "type": "string",
            "description": "Placeholder text shown in empty input"
          },
          "inputType": {
            "type": "string",
            "enum": ["text", "number", "select"],
            "default": "text",
            "description": "Type of input for this slot"
          },
          "options": {
            "type": "array",
            "items": { "type": "string" },
            "description": "Options for select input type"
          },
          "validation": {
            "type": "object",
            "properties": {
              "minLength": { "type": "integer" },
              "maxLength": { "type": "integer" },
              "pattern": { "type": "string", "description": "Regex pattern" },
              "min": { "type": "number" },
              "max": { "type": "number" }
            },
            "additionalProperties": false
          },
          "defaultValue": {
            "type": "string",
            "description": "Pre-filled value"
          }
        },
        "required": ["name", "label"],
        "additionalProperties": false
      },
      "minItems": 1,
      "description": "Slot definitions for template placeholders"
    }
  },
  "required": ["type", "id", "prompt", "required", "template", "slots"],
  "additionalProperties": false
}
```

**Example specification**:

```json
{
  "type": "madlib",
  "id": "widget-madlib-p7q8r9",
  "prompt": "Complete this user story for the primary use case.",
  "required": true,
  "template": "As a {{role}}, I want {{capability}} so that {{benefit}}.",
  "slots": [
    {
      "name": "role",
      "label": "User role",
      "placeholder": "e.g., podcast producer",
      "inputType": "text",
      "validation": { "maxLength": 50 }
    },
    {
      "name": "capability",
      "label": "Desired capability",
      "placeholder": "e.g., to see download trends over time",
      "inputType": "text",
      "validation": { "maxLength": 200 }
    },
    {
      "name": "benefit",
      "label": "Benefit",
      "placeholder": "e.g., I can identify which episodes perform best",
      "inputType": "text",
      "validation": { "maxLength": 200 }
    }
  ]
}
```

### 7.2 Structured Fields

Structured fields presents a form with multiple fields of different types. This is more flexible than mad-lib, supporting various input types without a connecting template.

**When to use**: Use structured fields when you need multiple pieces of structured information that don't fit a template pattern. Examples: "Provide details for this integration." "Fill in the constraint parameters."

**Schema**:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "compass-widget-structured-fields",
  "title": "StructuredFieldsWidget",
  "type": "object",
  "properties": {
    "type": { "const": "structured-fields" },
    "id": { "type": "string", "pattern": "^widget-structured-fields-[a-z0-9]+$" },
    "prompt": { "type": "string", "maxLength": 500 },
    "required": { "type": "boolean", "default": true },
    "helpText": { "type": "string", "maxLength": 1000 },
    "escapeHatch": { "$ref": "#/definitions/escapeHatch" },
    "helpMeThink": { "$ref": "#/definitions/helpMeThink" },
    "researchTrigger": { "$ref": "#/definitions/researchTrigger" },
    "meta": { "$ref": "#/definitions/meta" },
    "fields": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": { "type": "string" },
          "label": { "type": "string" },
          "description": { "type": "string" },
          "inputType": {
            "type": "string",
            "enum": ["text", "textarea", "number", "select", "date", "url", "email"],
            "default": "text"
          },
          "placeholder": { "type": "string" },
          "options": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "value": { "type": "string" },
                "label": { "type": "string" }
              },
              "required": ["value", "label"],
              "additionalProperties": false
            },
            "description": "Options for select input type"
          },
          "required": { "type": "boolean", "default": false },
          "validation": {
            "type": "object",
            "properties": {
              "minLength": { "type": "integer" },
              "maxLength": { "type": "integer" },
              "pattern": { "type": "string" },
              "min": { "type": "number" },
              "max": { "type": "number" }
            },
            "additionalProperties": false
          },
          "defaultValue": { "type": "string" }
        },
        "required": ["name", "label", "inputType"],
        "additionalProperties": false
      },
      "minItems": 1,
      "description": "Field definitions"
    },
    "layout": {
      "type": "string",
      "enum": ["vertical", "two-column"],
      "default": "vertical",
      "description": "How fields are arranged"
    }
  },
  "required": ["type", "id", "prompt", "required", "fields"],
  "additionalProperties": false
}
```

---

## Part 8: Meta Widget Schemas

Meta widgets control workflow rather than capture content. They mark decision points, verify boundaries, trigger research, and manage branch merging.

### 8.1 Decision Gate

Decision gate presents a checkpoint where an explicit decision is required before proceeding. It ensures that critical choices are made consciously, not accidentally skipped.

**When to use**: Use decision gate when the workflow has a natural pause point requiring explicit commitment. Examples: "Ready to move from exploration to implementation planning?" "Confirm these requirements are complete before proceeding."

**Schema**:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "compass-widget-decision-gate",
  "title": "DecisionGateWidget",
  "type": "object",
  "properties": {
    "type": { "const": "decision-gate" },
    "id": { "type": "string", "pattern": "^widget-decision-gate-[a-z0-9]+$" },
    "prompt": { "type": "string", "maxLength": 500 },
    "required": { "type": "boolean", "default": true },
    "helpText": { "type": "string", "maxLength": 1000 },
    "escapeHatch": { "$ref": "#/definitions/escapeHatch" },
    "helpMeThink": { "$ref": "#/definitions/helpMeThink" },
    "researchTrigger": { "$ref": "#/definitions/researchTrigger" },
    "meta": { "$ref": "#/definitions/meta" },
    "summary": {
      "type": "string",
      "description": "Summary of what has been decided so far (displayed for review)"
    },
    "proceedLabel": {
      "type": "string",
      "default": "Proceed",
      "description": "Label for the proceed button"
    },
    "goBackLabel": {
      "type": "string",
      "default": "Go back and revise",
      "description": "Label for the go-back option"
    },
    "reviewItems": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "label": { "type": "string" },
          "value": { "type": "string" },
          "editable": { "type": "boolean", "default": false }
        },
        "required": ["label", "value"],
        "additionalProperties": false
      },
      "description": "Key decisions to review before proceeding"
    },
    "requiresConfirmation": {
      "type": "boolean",
      "default": true,
      "description": "Whether user must check a confirmation box"
    },
    "confirmationText": {
      "type": "string",
      "default": "I confirm these decisions are correct.",
      "description": "Text for the confirmation checkbox"
    }
  },
  "required": ["type", "id", "prompt", "required"],
  "additionalProperties": false
}
```

### 8.2 Boundary Checklist

Boundary checklist presents a list of dealbreakers or out-of-scope items that the user must verify. This ensures that constraints are consciously acknowledged.

**When to use**: Use boundary checklist during the BOUNDARY stage or when verifying constraints. Examples: "Confirm these are out of scope for Phase 1." "Verify these dealbreakers have been addressed."

**Schema**:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "compass-widget-boundary-checklist",
  "title": "BoundaryChecklistWidget",
  "type": "object",
  "properties": {
    "type": { "const": "boundary-checklist" },
    "id": { "type": "string", "pattern": "^widget-boundary-checklist-[a-z0-9]+$" },
    "prompt": { "type": "string", "maxLength": 500 },
    "required": { "type": "boolean", "default": true },
    "helpText": { "type": "string", "maxLength": 1000 },
    "escapeHatch": { "$ref": "#/definitions/escapeHatch" },
    "helpMeThink": { "$ref": "#/definitions/helpMeThink" },
    "researchTrigger": { "$ref": "#/definitions/researchTrigger" },
    "meta": { "$ref": "#/definitions/meta" },
    "checklistType": {
      "type": "string",
      "enum": ["out-of-scope", "dealbreakers", "constraints", "assumptions"],
      "description": "Type of items being checked"
    },
    "items": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "value": { "type": "string" },
          "label": { "type": "string" },
          "description": { "type": "string" },
          "severity": {
            "type": "string",
            "enum": ["critical", "important", "minor"],
            "default": "important"
          }
        },
        "required": ["value", "label"],
        "additionalProperties": false
      },
      "minItems": 1,
      "description": "Items to verify"
    },
    "requireAllChecked": {
      "type": "boolean",
      "default": true,
      "description": "Whether all items must be checked to proceed"
    },
    "allowAdditions": {
      "type": "boolean",
      "default": true,
      "description": "Whether user can add items to the list"
    }
  },
  "required": ["type", "id", "prompt", "required", "checklistType", "items"],
  "additionalProperties": false
}
```

### 8.3 Research Trigger

Research trigger presents an option to pause planning and spawn a research branch. This is the interactive form of the "Research this" action available on all widgets.

**When to use**: Use research trigger when the conversation has identified a specific uncertainty that needs investigation. Examples: "We need more information about transcription services. Want to research this?" "This decision depends on current API pricing. Research available options?"

**Schema**:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "compass-widget-research-trigger",
  "title": "ResearchTriggerWidget",
  "type": "object",
  "properties": {
    "type": { "const": "research-trigger" },
    "id": { "type": "string", "pattern": "^widget-research-trigger-[a-z0-9]+$" },
    "prompt": { "type": "string", "maxLength": 500 },
    "required": { "type": "boolean", "default": false },
    "helpText": { "type": "string", "maxLength": 1000 },
    "escapeHatch": { "$ref": "#/definitions/escapeHatch" },
    "helpMeThink": { "$ref": "#/definitions/helpMeThink" },
    "researchTrigger": { "$ref": "#/definitions/researchTrigger" },
    "meta": { "$ref": "#/definitions/meta" },
    "researchQuestion": {
      "type": "string",
      "description": "The specific question to investigate"
    },
    "suggestedBrief": {
      "type": "string",
      "description": "Pre-filled research brief (user can edit)"
    },
    "researchType": {
      "type": "string",
      "enum": ["technical", "domain", "contextual"],
      "default": "technical",
      "description": "Type of research needed"
    },
    "urgency": {
      "type": "string",
      "enum": ["blocking", "important", "nice-to-have"],
      "default": "important",
      "description": "How urgent this research is"
    },
    "skipLabel": {
      "type": "string",
      "default": "Skip research for now",
      "description": "Label for skipping research"
    },
    "proceedLabel": {
      "type": "string",
      "default": "Start research",
      "description": "Label for starting research"
    }
  },
  "required": ["type", "id", "prompt", "researchQuestion"],
  "additionalProperties": false
}
```

### 8.4 Merge Gate

Merge gate presents a proposal from a research or exploration branch for review. The user can accept, edit, or reject the proposed changes before they become canonical.

**When to use**: Use merge gate when a branch has completed and its findings need to be incorporated into the main workflow. Examples: "Research complete. Review findings and decide what to incorporate." "Exploration branch finished. Which approach do you want to continue with?"

**Schema**:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "compass-widget-merge-gate",
  "title": "MergeGateWidget",
  "type": "object",
  "properties": {
    "type": { "const": "merge-gate" },
    "id": { "type": "string", "pattern": "^widget-merge-gate-[a-z0-9]+$" },
    "prompt": { "type": "string", "maxLength": 500 },
    "required": { "type": "boolean", "default": true },
    "helpText": { "type": "string", "maxLength": 1000 },
    "escapeHatch": { "$ref": "#/definitions/escapeHatch" },
    "helpMeThink": { "$ref": "#/definitions/helpMeThink" },
    "researchTrigger": { "$ref": "#/definitions/researchTrigger" },
    "meta": { "$ref": "#/definitions/meta" },
    "branchType": {
      "type": "string",
      "enum": ["research", "exploration"],
      "description": "Type of branch being merged"
    },
    "branchSummary": {
      "type": "string",
      "description": "Summary of what the branch investigated"
    },
    "proposedChanges": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "changeId": { "type": "string" },
          "changeType": {
            "type": "string",
            "enum": ["add-requirement", "modify-requirement", "add-constraint", "modify-constraint", "add-decision", "modify-decision"],
            "description": "What kind of change is proposed"
          },
          "before": { "type": "string", "description": "Previous value (for modifications)" },
          "after": { "type": "string", "description": "Proposed new value" },
          "rationale": { "type": "string", "description": "Why this change is proposed" },
          "confidence": {
            "type": "string",
            "enum": ["high", "medium", "low"],
            "description": "Confidence in this recommendation"
          }
        },
        "required": ["changeId", "changeType", "after", "rationale"],
        "additionalProperties": false
      },
      "description": "List of proposed changes from the branch"
    },
    "sources": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "title": { "type": "string" },
          "url": { "type": "string" },
          "retrievedAt": { "type": "string", "format": "date-time" }
        },
        "required": ["title"],
        "additionalProperties": false
      },
      "description": "Sources that support the proposed changes"
    },
    "actions": {
      "type": "object",
      "properties": {
        "acceptAllLabel": { "type": "string", "default": "Accept all changes" },
        "rejectAllLabel": { "type": "string", "default": "Reject all changes" },
        "reviewIndividuallyLabel": { "type": "string", "default": "Review each change" }
      },
      "additionalProperties": false,
      "description": "Labels for action buttons"
    }
  },
  "required": ["type", "id", "prompt", "required", "branchType", "branchSummary", "proposedChanges"],
  "additionalProperties": false
}
```

---

## Part 9: Widget Response Schema

When a user interacts with a widget, their response is captured in a structured format that can be stored, analyzed, and processed by the orchestration layer.

### 9.1 Common Response Fields

Every widget response includes these fields:

**`widgetId`** (string, required): The ID of the widget that was responded to.

**`widgetType`** (string, required): The type of the widget.

**`timestamp`** (string, required): ISO 8601 timestamp of when the response was submitted.

**`responseType`** (string, required): One of `"submitted"`, `"escaped"`, `"helpRequested"`, or `"researchTriggered"`.

**`value`** (any, required for `"submitted"`): The actual response value, format depends on widget type.

**`escapedExplanation`** (string, optional): User's explanation when they used the escape hatch.

### 9.2 Response Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "compass-widget-response",
  "title": "WidgetResponse",
  "type": "object",
  "properties": {
    "widgetId": {
      "type": "string",
      "description": "ID of the widget being responded to"
    },
    "widgetType": {
      "type": "string",
      "description": "Type of the widget"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "When the response was submitted"
    },
    "responseType": {
      "type": "string",
      "enum": ["submitted", "escaped", "helpRequested", "researchTriggered"],
      "description": "How the user responded"
    },
    "value": {
      "description": "The response value (type depends on widget)"
    },
    "escapedExplanation": {
      "type": "string",
      "description": "User explanation when escape hatch was used"
    },
    "metadata": {
      "type": "object",
      "properties": {
        "interactionDurationMs": {
          "type": "integer",
          "description": "How long user spent on the widget"
        },
        "revisited": {
          "type": "boolean",
          "description": "Whether user returned to change their response"
        },
        "helpViewed": {
          "type": "boolean",
          "description": "Whether help content was viewed"
        }
      },
      "additionalProperties": false
    }
  },
  "required": ["widgetId", "widgetType", "timestamp", "responseType"],
  "additionalProperties": false
}
```

### 9.3 Type-Specific Response Values

Each widget type produces a specific value format:

| Widget Type | Value Format | Example |
|-------------|--------------|---------|
| `single-select` | `string` (selected option value) | `"power-users"` |
| `multi-select` | `string[]` (selected option values) | `["search", "export"]` |
| `ranked-choice` | `string[]` (values in ranked order) | `["search", "collab", "api"]` |
| `pairwise-comparison` | `string[]` (final ranking from comparisons) | `["search", "export", "mobile"]` |
| `slider` | `number` | `500` |
| `opposing-spectrum` | `number` (position 0 to max) | `3` |
| `allocation` | `object` (value → points) | `{"speed": 40, "quality": 30, "features": 20, "ux": 10}` |
| `tradeoff-table` | `object` (option → criterion → rating) | `{"optionA": {"cost": 4, "features": 3}, ...}` |
| `ab-comparison` | `string` (selected option value) | `"optionA"` |
| `card-sort` | `object` (category → card values) | `{"phase1": ["search"], "phase2": ["collab"]}` |
| `sequencer` | `string[]` (values in sequence order) | `["setup", "build", "test", "deploy"]` |
| `quadrant` | `object` (value → {x, y}) | `{"search": {"x": 30, "y": 80}, ...}` |
| `madlib` | `object` (slot name → value) | `{"role": "producer", "capability": "view trends"}` |
| `structured-fields` | `object` (field name → value) | `{"name": "API Integration", "priority": "high"}` |
| `decision-gate` | `string` (`"proceed"` or `"goBack"`) | `"proceed"` |
| `boundary-checklist` | `object` ({checked: string[], added: string[]}) | `{"checked": ["item1"], "added": []}` |
| `research-trigger` | `object` ({proceed: boolean, brief: string}) | `{"proceed": true, "brief": "Research APIs"}` |
| `merge-gate` | `object` ({action: string, changes: ...}) | `{"action": "acceptAll"}` or `{"action": "individual", ...}` |

---

## Part 10: Interaction Logging Format

Widget interactions are logged for analytics, debugging, and audit purposes. The logging format captures the complete interaction lifecycle.

### 10.1 Event Types

**`widget.presented`**: A widget was shown to the user. Logged when the widget renders.

**`widget.interacted`**: The user made a change to the widget (selected an option, moved a slider, etc.). Logged on each interaction, not just submission.

**`widget.submitted`**: The user submitted their response. Logged when the response is captured.

**`widget.abandoned`**: The user left without responding (navigated away, session ended). Logged when detected.

**`widget.help.opened`**: The user clicked "Help me think."

**`widget.help.closed`**: The user closed the help content.

**`widget.escape.selected`**: The user selected the escape hatch option.

**`widget.research.triggered`**: The user triggered a research branch.

### 10.2 Event Payload Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "compass-widget-event",
  "title": "WidgetInteractionEvent",
  "type": "object",
  "properties": {
    "eventType": {
      "type": "string",
      "enum": [
        "widget.presented",
        "widget.interacted",
        "widget.submitted",
        "widget.abandoned",
        "widget.help.opened",
        "widget.help.closed",
        "widget.escape.selected",
        "widget.research.triggered"
      ]
    },
    "timestamp": {
      "type": "string",
      "format": "date-time"
    },
    "widgetId": { "type": "string" },
    "widgetType": { "type": "string" },
    "sessionId": { "type": "string" },
    "workflowRunId": { "type": "string" },
    "questioningArcStage": {
      "type": "string",
      "enum": ["OPEN", "FOLLOW", "SHARPEN", "BOUNDARY", "GROUND"]
    },
    "payload": {
      "type": "object",
      "description": "Event-specific data"
    }
  },
  "required": ["eventType", "timestamp", "widgetId", "widgetType", "sessionId", "workflowRunId"],
  "additionalProperties": false
}
```

### 10.3 Event-Specific Payloads

**`widget.presented`**:
```json
{
  "widgetSpec": { /* full widget specification */ },
  "renderDurationMs": 45
}
```

**`widget.interacted`**:
```json
{
  "interactionType": "optionSelected",
  "previousValue": null,
  "newValue": "power-users"
}
```

**`widget.submitted`**:
```json
{
  "response": { /* full WidgetResponse object */ },
  "totalInteractionDurationMs": 12500
}
```

**`widget.abandoned`**:
```json
{
  "lastKnownValue": "power-users",
  "reason": "sessionTimeout",
  "timeSpentMs": 30000
}
```

---

## Part 11: Validation Rules

Widget specifications must pass both schema validation and semantic validation before rendering.

### 11.1 Schema Validation

Schema validation uses JSON Schema draft-07 and verifies that the specification matches the declared widget type's schema, all required fields are present, field values match their declared types, constraints (minItems, maxLength, etc.) are satisfied, and no additional properties are present (`additionalProperties: false` is enforced).

**Implementation note**: Use Zod for runtime validation in TypeScript. Zod schemas should be defined with `.strict()` to match JSON Schema's `additionalProperties: false` behavior.

### 11.2 Semantic Validation

Semantic validation catches logical errors that schema validation misses:

**Option uniqueness**: All `value` fields within options/items arrays must be unique.

**Reference validity**: `defaultValue` must reference an existing option value. `defaultAllocations` must reference existing category values.

**Constraint coherence**: `minSelections` must be less than or equal to `maxSelections`. `min` must be less than `max` for sliders. Allocation `minAllocation` sums must not exceed `budget`.

**Content appropriateness**: Options should not be empty strings. Prompts should be actual questions or instructions, not placeholders.

### 11.3 Error Handling

When validation fails, the system should log the error with full context (widget ID, widget type, validation error details), provide a fallback if possible (e.g., render without invalid options), notify the orchestration layer that generation failed, and consider prompting the LLM to regenerate with the error feedback (Instructor pattern).

---

## Part 12: LLM Generation Guidelines

This section provides guidance for constructing prompts that reliably generate valid widget specifications.

### 12.1 Prompt Structure

Effective prompts for widget generation follow this structure:

1. **Context**: What stage of the questioning arc? What has been decided so far?
2. **Objective**: What information are we trying to capture?
3. **Constraints**: What widget type is appropriate? What options should be included?
4. **Schema**: Include the relevant schema (or reference to it) so the LLM knows the exact format.
5. **Examples**: Include 1-2 examples of valid specifications.

### 12.2 Schema Integration with Zod

Per RF-02-01, widget schemas should use Zod with `.describe()` annotations extensively:

```typescript
const singleSelectSchema = z.object({
  type: z.literal('single-select').describe('Widget type identifier'),
  id: z.string().describe('Unique widget instance ID'),
  prompt: z.string().max(500).describe('Main question presented to user'),
  required: z.boolean().default(true).describe('Whether response is required'),
  options: z.array(
    z.object({
      value: z.string().describe('Machine-readable option identifier'),
      label: z.string().describe('Human-readable option text'),
      description: z.string().optional().describe('Additional context for this option')
    })
  ).min(2).max(10).describe('Options to choose from')
}).strict();
```

### 12.3 Common Generation Errors

**Error: Discriminated union failures**
Per RF-02-01, discriminated unions are unreliable across providers. Use separate schemas per widget type rather than a single schema with type discrimination.

**Error: Extra properties**
LLMs sometimes add helpful but unexpected fields. Always use `additionalProperties: false` in JSON Schema and `.strict()` in Zod.

**Error: Duplicate option values**
LLMs may generate options with duplicate `value` fields. Include explicit instruction: "Each option must have a unique value field."

**Error: Empty or placeholder content**
LLMs may generate placeholder text like "Option 1" or "[description]". Include explicit instruction: "Generate meaningful, specific content for all fields."

### 12.4 Validation Feedback Loop

When generation fails validation, feed the error back to the LLM:

```
The generated widget specification failed validation with the following error:
[error details]

Please regenerate the specification, fixing the error while preserving the original intent.
```

This pattern (used by Instructor) typically succeeds within 2-3 attempts.

---

## Part 13: Integration Notes

### 13.1 Integration with Orchestration (Area 02)

Widget schemas are generated by the orchestration layer (Mastra + Vercel AI SDK) and passed to the rendering layer. The orchestration layer is responsible for determining which widget type is appropriate based on conversation context, generating the widget specification using structured output, handling the widget response and updating workflow state, and logging interaction events.

The AI SDK's `Output.object()` method with Zod schemas ensures type-safe generation. Streaming via `partialOutputStream` enables progressive rendering of complex widgets.

### 13.2 Integration with Components (Area 07)

Widget specifications map to React components via the Thesys C1 rendering layer. The registration manifest (defined in ADR-07-01) pairs Zod schemas with component implementations.

**For C1 native widgets**: The specification is passed directly to the C1Component for rendering.

**For custom widgets**: The specification is passed to the registered custom component (built with shadcn/ui + dnd-kit) which handles rendering and interaction.

### 13.3 Integration with Questioning Arc (Area 18)

Widget responses feed into the questioning arc state machine. The `meta.questioningArcStage` field indicates which stage the widget belongs to. Responses update working memory and may trigger stage transitions.

The escape hatch, help, and research trigger features connect to arc operations: escape hatch may trigger free-form input handling, help may invoke LLM-generated support content, and research trigger spawns a research branch per DD-18-01.

---

## Appendix A: Complete Schema Reference

The complete JSON Schema definitions for all widget types are available in the companion file `widget-schemas.json`. This appendix provides the consolidated schema with shared definitions.

### A.1 Shared Definitions

```json
{
  "definitions": {
    "escapeHatch": {
      "type": "object",
      "properties": {
        "enabled": { "type": "boolean", "default": true },
        "label": { "type": "string", "default": "None of these fit / I'll describe instead" },
        "promptForExplanation": { "type": "boolean", "default": true }
      },
      "additionalProperties": false
    },
    "helpMeThink": {
      "type": "object",
      "properties": {
        "enabled": { "type": "boolean", "default": true },
        "label": { "type": "string", "default": "Help me think about this" },
        "content": { "type": "string" }
      },
      "additionalProperties": false
    },
    "researchTrigger": {
      "type": "object",
      "properties": {
        "enabled": { "type": "boolean", "default": true },
        "label": { "type": "string", "default": "Research this" },
        "defaultBrief": { "type": "string" }
      },
      "additionalProperties": false
    },
    "meta": {
      "type": "object",
      "properties": {
        "questioningArcStage": { "type": "string", "enum": ["OPEN", "FOLLOW", "SHARPEN", "BOUNDARY", "GROUND"] },
        "priority": { "type": "integer", "minimum": 1, "maximum": 10, "default": 5 },
        "tags": { "type": "array", "items": { "type": "string" } }
      },
      "additionalProperties": false
    }
  }
}
```

---

## Appendix B: Glossary

**C1**: Thesys's generative UI API that transforms LLM outputs into interactive React components.

**dnd-kit**: A lightweight, modular drag-and-drop library for React used for spatial widgets.

**Escape hatch**: A widget option that allows users to exit structured choices when none fit their needs.

**JSON Schema**: Standard format for describing JSON structure, used for widget specification validation.

**Meta widget**: A widget that controls workflow rather than capturing content (decision gates, research triggers, etc.).

**shadcn/ui**: A React component library used for building custom widgets.

**Widget specification**: The JSON object that defines a widget's configuration, generated by the LLM.

**Widget response**: The structured object capturing a user's interaction with a widget.

**Zod**: TypeScript-first schema validation library used for runtime validation and type inference.

---

## Appendix C: Related Documents

- **STD-19-01**: Widget Schema Standards (companion document with compliance checklists)
- **RF-02-01**: LLM Orchestration Framework Research Findings (Mastra + Vercel AI SDK selection)
- **ADR-02-01**: Orchestration Selection (formalizes orchestration decision)
- **RF-07-01**: Widget Component Library Research Findings (Thesys C1 + shadcn/ui selection)
- **ADR-07-01**: Widget Component Library Selection (formalizes component library decision)
- **DD-18-01**: Questioning Arc Definition (workflow state machine)
- **STD-18-01**: Questioning Arc Standards (stage transition rules)
- **Compass System Definition**: Authoritative system specification (§2.2 widget taxonomy, §2.1 planning workflow)

---

*End of Widget Schema and Rendering Specification (DD-19-01)*
