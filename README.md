# PURGE — Narrative State & Timeline Engine

PURGE is a system for **building, evolving, and inspecting narrative canon** as structured state.

Instead of treating stories as text, PURGE treats them as:

* facts
* rules
* events
* time

This makes narratives **traceable, replayable, and logically inspectable**.

PURGE is not an AI storyteller.
It is the engine *underneath* one.

---

## What PURGE Does

PURGE helps you answer questions like:

* *What facts are true in the story right now?*
* *Which rules are currently active?*
* *When did a contradiction appear?*
* *Which event caused it?*
* *What did the world look like before that happened?*

It does this by modeling narratives as structured data instead of prose.

---

## Core Ideas (Plain English)

### Canon

Canon is the **current state of the story**.

It includes:

* basic metadata (title, version)
* truths (facts that are true or false)
* rules (constraints on what is allowed)
* events (things that happened)
* acts (story phases / timeline sections)

Canon is always:

* deterministic
* serializable to JSON
* reconstructible from history

---

### Truths (Facts)

Truths are simple on/off facts about the world.

Example:

```json
{
  "world_is_stable": true,
  "character_is_alive": false
}
```

Important rules:

* Truths do not change by themselves
* Truths are changed **only by events**
* Truths are checked by rules

Truths describe *what is*, not *why*.

---

### Rules (Constraints)

Rules define **what is allowed or forbidden**.

They do not change the story.
They only evaluate it.

Example:

```json
{
  "id": "no_resurrection",
  "severity": "hard",
  "conditions": {
    "all": ["world_is_stable"]
  },
  "constraint": {
    "forbid_truth": "character_is_alive"
  }
}
```

This means:

> If the world is stable, the character must not be alive.

Rules:

* may be conditional
* may be strict (`hard`) or advisory (`soft`)
* never mutate canon themselves

---

### Events (What Happens)

Events are the **only way the story changes**.

An event records:

* *what happened*
* *when it happened*
* *what facts it changed*

Example:

```json
{
  "id": "evt_revival",
  "act": 2,
  "name": "Character returns",
  "sets_truths": {
    "character_is_alive": true
  }
}
```

Events are:

* applied in order
* irreversible
* logged permanently
* replayable

Everything flows from events.

---

### Acts (Timeline Structure)

Acts divide the story into **clear phases**.

They help you:

* group events
* see progression
* inspect state at specific points
* understand causality

Acts do not enforce logic.
They provide structure and clarity.

---

## Timeline View

The Timeline shows:

* acts in order
* events inside each act
* the state of the world after each act

This lets you see:

* how facts evolved
* where rules became active
* exactly when contradictions appeared

The timeline is **derived from events**, not stored separately.

---

## Paradox Detection

A paradox means:

> The current story state violates an active hard rule.

A paradox exists only if:

1. A rule is marked `hard`
2. Its conditions are met
3. It forbids a specific truth
4. That truth is currently true

Paradox detection:

* never changes canon
* never blocks actions automatically
* only reports contradictions

It answers:

> “Is the story logically inconsistent *right now*?”

---

## Validation (Different From Paradox)

Validation checks:

> “Should this event be allowed?”

It runs **before** an event is applied.

Validation may:

* block an event
* warn about consequences

Paradox detection runs **after** events and looks at the whole state.

They serve different purposes and are kept separate intentionally.

---

## Replay & Debugging

PURGE can replay the story from history.

This allows you to:

* rebuild canon step by step
* inspect earlier states
* debug unexpected outcomes
* verify determinism

Replay always produces the same result given the same events.

---

## Projects & Persistence

Stories are stored as **projects**.

Each project:

* owns one canon
* is saved as JSON
* must be explicitly opened or created
* prevents accidental or anonymous mutation

No story changes are allowed without an active project.

---

## User Interface

The interface is built to **inspect and control**, not guess or automate.

It includes panels for:

* project management
* truths
* rules
* events
* timeline
* paradox inspection
* validation feedback
* replay debugging

The UI never contains story logic.

---

## Technologies Used

Only technologies currently in use are listed.

### Language & Runtime

* **Python 3**
* Python standard library

### UI

* **Streamlit**

  * panel-based interface
  * deterministic reruns
  * state inspection

### Data Format

* **JSON**

  * canonical storage
  * replayable structure

No databases, ORMs, AI frameworks, or external services are used at this stage.

---

## What PURGE Is (and Isn’t)

**PURGE is:**

* a narrative state engine
* a logic and timeline tool
* a debugging system for stories

**PURGE is not:**

* a text generator
* an AI storyteller
* a probabilistic system
* a black box

Those layers can be added later, *on top* of this engine.

---

## Current State

* Canon system: stable
* Event system: stable
* Timeline & acts: stable
* Paradox detection: stable
* Validation: stable

PURGE is suitable for experimentation, tooling, and extension.