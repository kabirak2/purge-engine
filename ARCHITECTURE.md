# ARCHITECTURE.md

## PURGE Engine

**Procedural Universe Realtime Game Engine**


## 1. Purpose and Scope

PURGE is a narrative systems engine designed to model, enforce, and evolve **story canon** under formal constraints. Unlike conventional game engines that prioritize rendering or physics, PURGE treats **narrative consistency as a first-class system concern**.

The engine is intended for:

* story-heavy games
* interactive fiction
* narrative simulations
* research into AI-assisted storytelling and canon preservation

This document defines the **architectural principles, subsystem boundaries, data flows, and extension points** of the PURGE engine.


## 2. Design Philosophy

PURGE is built on four core principles:

1. **Canon as State**
   Narrative truth is modeled explicitly and evolves over time.

2. **Rules as Constraints**
   Story progression is governed by enforceable, inspectable rules.

3. **Events as Transactions**
   Narrative changes occur through discrete, validated events.

4. **AI as Advisor, Not Authority**
   AI systems may propose changes but cannot mutate canon without validation.

These principles distinguish PURGE from free-form story generators and prevent narrative drift, paradox collapse, and incoherent timelines.


## 3. High-Level System Overview

At a macro level, PURGE is divided into three layers:

```
+-----------------------------+
|          UI Layer           |
|  (Control & Inspection)     |
+-----------------------------+
|        Core Engine          |
|  (Canon, Rules, Events)     |
+-----------------------------+
|   Persistence & Analysis    |
|  (Snapshots, Integrity)     |
+-----------------------------+
```

* **UI Layer (`ui/`)**
  Human interaction, inspection, and debugging.

* **Core Engine (`core/`)**
  Canon, validation, branching, paradox handling, AI mediation.

* **Persistence & Analysis**
  Snapshots, integrity scoring, telemetry, replay.


## 4. Canon System

### 4.1 Canon Definition

Canon represents the authoritative narrative state and is implemented in `core/canon.py`.

It consists of:

* Metadata (title, author, version)
* Truths (boolean or scalar facts)
* Rules (constraints)
* Events (historical mutations)
* Snapshots (state checkpoints)
* Integrity metrics
* Dependency graph
* Active narrative branch

Canon is **append-only in spirit**: changes occur through events rather than direct mutation.


### 4.2 Canon Lifecycle

1. Canon is initialized empty.
2. Rules are added to constrain future events.
3. Events are proposed and validated.
4. Approved events mutate canon.
5. Postconditions update truths.
6. Snapshots and integrity are recomputed.

Canon never silently changes.


## 5. Rule System and Validation

### 5.1 Rule Structure

Rules are formal constraints defined in `core/axiom.py` and enforced by `core/validator.py`.

A rule consists of:

* Scope
* Conditions (logical predicates)
* Constraint type (forbid, require, limit)
* Target and value
* Reason and metadata
* Strength and decay properties

Rules are explicit, inspectable objects—not implicit logic.


### 5.2 Validation Pipeline

When an action (e.g., event insertion) is attempted:

1. Context is constructed (e.g., act number).
2. Rule conditions are evaluated.
3. Matching constraints are collected.
4. Blocking rules prevent mutation.
5. Violations are returned with explanations.

Validation is **deterministic and explainable**.


## 6. Event and Timeline Model

### 6.1 Events

Events are discrete narrative transactions defined by:

* ID
* Name
* Description
* Act / temporal position
* Tags
* Dependencies
* Postconditions

Events are stored in canonical order and logged.


### 6.2 Timeline Semantics

The timeline is not strictly linear:

* Events may depend on others
* Branches may diverge
* Replays may reconstruct alternate histories

Temporal coherence is enforced through validation, not timestamps alone.


## 7. Branching and Paradox Handling

### 7.1 Branching Model

Implemented across:

* `core/branching.py`
* `core/branch_merge.py`
* `core/replay.py`

Each branch represents a self-consistent canon evolution.

Branches may:

* Fork
* Replay events
* Merge under constraint reconciliation


### 7.2 Paradox Detection

Paradoxes are detected via:

* Dependency conflicts
* Rule violations
* Integrity degradation

Handled in:

* `core/paradox.py`
* `core/repair.py`

Resolution strategies include:

* Event rejection
* Rule reinforcement
* Branch isolation
* Canon repair


## 8. Integrity, Analytics, and Telemetry

### 8.1 Integrity Model

Canon integrity is computed in `core/integrity.py` and reflects:

* Rule compliance
* Narrative consistency
* Dependency satisfaction

Integrity is a **quantitative signal**, not a binary flag.


### 8.2 Analytics and Telemetry

Subsystems:

* `core/analytics.py`
* `core/telemetry.py`
* `core/risk.py`
* `core/fatigue.py`

Used to:

* Measure narrative strain
* Detect overused tropes
* Identify risky story paths
* Support research analysis

These systems observe canon; they do not mutate it.


## 9. VerseMind: AI Proposal Interface

### 9.1 Role of VerseMind

VerseMind is an AI-assisted proposal engine, implemented in:

* `core/versemind.py`
* `core/versemind_prompt.py`
* `core/versemind_schema.py`

VerseMind:

* Interprets human intent
* Proposes structured changes
* Provides confidence and rationale

It **cannot** directly modify canon.


### 9.2 Human-in-the-Loop Enforcement

All AI proposals must be:

1. Presented to a human
2. Explicitly approved
3. Validated against rules

This prevents AI-driven canon collapse.


## 10. Persistence and Snapshots

### 10.1 Snapshots

Snapshots (`core/snapshot.py`) capture canon state at key points:

* After events
* Before merges
* During repair operations

Used for:

* Rollback
* Replay
* Analysis


### 10.2 Filesystem Layout

Persistence logic resides in `core/filesystem.py`.

Runtime project data is stored **outside version control** and treated as user data, not engine state.


## 11. UI Architecture

The UI layer (`ui/`) is built with Tkinter and serves as a **control surface**, not engine logic.

Panels include:

* Canon inspection
* Rule editing
* Timeline management
* Validation console
* VerseMind interface
* Debugging and paradox views

UI modules never bypass core validation.


## 12. Data Flow Summary

A typical mutation flow:

```
Human / AI Intent
        ↓
Proposal (VerseMind or Manual)
        ↓
Validation (Rules, Context)
        ↓
Event Application
        ↓
Canon Mutation
        ↓
Snapshot + Integrity Update
        ↓
Telemetry & Analytics
```

This pipeline is invariant.


## 13. Extension Points

PURGE is designed for extension at:

* Rule languages
* AI backends
* Integrity metrics
* Visualization layers
* Persistence strategies

Extensions must respect canon immutability and validation discipline.


## 14. Conclusion

PURGE formalizes narrative as a **governed system**, not a generative free-for-all.
By enforcing canon through rules, events, and explainable validation, it enables:

* long-form narrative coherence
* safe AI assistance
* reproducible story simulations
* research into narrative integrity

This architecture prioritizes **correctness, inspectability, and evolution** over convenience.