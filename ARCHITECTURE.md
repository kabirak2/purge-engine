# ARCHITECTURE

This document describes the internal architecture of **PURGE**: how narrative state is modeled, how logic flows through the system, and how responsibilities are separated.

PURGE is designed as a **deterministic narrative engine**.
Every architectural decision prioritizes **clarity, replayability, and correctness** over convenience.

---

## Architectural Overview

PURGE is divided into **three strict layers**:

1. **Core Engine** — pure narrative logic
2. **Runtime & Persistence** — state authority and disk I/O
3. **User Interface** — inspection and controlled interaction

Each layer has explicit responsibilities and enforced boundaries.

```
┌────────────────────────────┐
│        User Interface      │
│  (Streamlit panels)        │
└────────────┬───────────────┘
             │
             ▼
┌────────────────────────────┐
│   Runtime & Project Store  │
│  (Singleton state control) │
└────────────┬───────────────┘
             │
             ▼
┌────────────────────────────┐
│        Core Engine         │
│ (Canon, rules, events)    │
└────────────────────────────┘
```

No layer bypasses another.

---

## 1. Core Engine

The **core engine** contains all narrative semantics.
It is deterministic, serializable, and UI-agnostic.

### Responsibilities

The core engine is responsible for:

* defining the Canon data model
* applying events to canon
* evaluating rules and conditions
* detecting paradoxes
* validating proposed actions
* replaying narrative history
* reconstructing timeline state
* tracking structural dependencies

The core engine **never**:

* renders UI
* reads user input
* writes directly to disk
* depends on Streamlit or runtime state

---

### Canon (`core/canon.py`)

Canon is the **authoritative narrative state**.

It contains:

* metadata
* truths (boolean facts)
* rules (constraints)
* events (history)
* acts (timeline structure)
* logs, snapshots, integrity data

Canon:

* is mutated only through events
* is fully serializable to JSON
* can be reconstructed from history
* exposes read-only analysis methods (e.g. paradox detection)

Canon itself does not decide *when* it is saved.

---

### Event Model

Events are the **only mutation path**.

An event:

* belongs to an act
* declares truth mutations
* is appended immutably
* is logged for replay

All higher-level reasoning (validation, paradox detection, replay) is built on top of event history.

---

### Rule Engine

Rules are **declarative constraints**, not actions.

Rules:

* may activate conditionally based on truths
* may forbid specific truths
* have severity (`hard` or `soft`)
* never mutate canon directly

Rules are evaluated by:

* the validator (pre-action)
* the paradox engine (post-state)

---

### Paradox Engine (`core/paradox_engine.py`)

The paradox engine is a **read-only analysis system**.

A paradox exists if:

* a hard rule is active
* its conditions are met
* it forbids a truth
* that truth is currently true

Paradox detection:

* does not block events
* does not modify state
* reports contradictions only

This separation is intentional.

---

### Validation Engine (`core/validator.py`)

Validation answers a different question than paradox detection:

> “Should this action be allowed right now?”

Validation:

* runs before an event is applied
* checks rules against proposed changes
* returns structured blocked/warned results
* never mutates canon

Validation and paradox detection are separate systems by design.

---

### Replay & Timeline (`core/replay.py`, `core/timeline.py`)

Replay reconstructs canon from history.

Timeline logic:

* replays events incrementally
* captures canon state after each act
* evaluates paradoxes per step

Timeline state is **derived**, not stored.

---

## 2. Runtime & Persistence Layer

The runtime layer is the **only mutable authority** outside the core.

It answers one question:

> “Which canon is active right now, and where is it stored?”

---

### Project Store (`core/project_store.py`)

The ProjectStore:

* owns the active Canon instance
* tracks the active project file
* enforces save discipline
* prevents anonymous mutation

Only one project can be active at a time.

---

### Runtime API (`core/runtime.py`)

The runtime exposes controlled access to the ProjectStore.

It:

* enforces singleton behavior
* mediates all saves
* applies events through Canon
* prevents invalid operations (e.g. saving without a project)

No UI code bypasses the runtime.

---

### Persistence (`core/filesystem.py`)

Persistence is handled via JSON files.

Characteristics:

* explicit file boundaries
* no implicit autosave
* no database
* no background writes

All saved data is human-readable and replayable.

---

## 3. User Interface Layer

The UI layer is built using **Streamlit**.

It is intentionally thin.

---

### UI Responsibilities

The UI is responsible for:

* displaying canon state
* collecting user input
* calling runtime APIs
* rendering engine results

The UI **never**:

* implements narrative logic
* mutates canon directly
* evaluates rules
* infers meaning

---

### UI Panels

Each panel maps to one responsibility:

| Panel      | Responsibility           |
| ---------- | ------------------------ |
| Project    | lifecycle & persistence  |
| Truths     | fact editing             |
| Rules      | constraint authoring     |
| Events     | state mutation           |
| Timeline   | causal visualization     |
| Paradox    | contradiction inspection |
| Validation | rule feedback            |
| Debugger   | replay inspection        |

Panels do not communicate with each other directly.

---

## Data Flow

All operations follow the same pattern:

1. User interacts with UI
2. UI calls runtime API
3. Runtime delegates to core
4. Canon mutates (via events only)
5. Runtime persists changes
6. UI re-renders from state

There are no hidden shortcuts.

---

## Determinism & Guarantees

PURGE guarantees:

* identical events + order → identical canon
* replay produces the same result every time
* no hidden randomness
* no implicit state mutation

This enables:

* debugging
* verification
* long-form consistency
* safe future AI integration

---

## Technologies Used

Only technologies currently in use are listed.

* **Python 3**
* **Streamlit** (UI)
* **JSON** (persistence)
* Python standard library only

No databases.
No ORMs.
No AI frameworks.
No external services.

---

## Architectural Rules (Non-Negotiable)

* Core logic never imports UI
* UI never implements logic
* Runtime owns persistence
* Events are the only mutation path
* Rules never mutate canon
* Paradox detection never blocks actions

Breaking these rules is considered a bug.

---

## Architectural Intent

This architecture exists to make narratives:

* inspectable
* replayable
* debuggable
* logically constrained
* extensible without collapse

PURGE favors **explicit structure** over convenience.