# DIAGRAMS

This document provides **visual representations** of PURGE’s architecture, data flow, and narrative mechanics.

All diagrams reflect the **current implementation**, not future plans.

---

## 1. High-Level System Architecture

This diagram shows the three-layer structure of PURGE and how data flows between them.

```
┌─────────────────────────────────────┐
│            User Interface            │
│        (Streamlit Panels)            │
│                                     │
│  Project | Truths | Rules | Events   │
│  Timeline | Paradox | Debugger       │
└───────────────┬─────────────────────┘
                │ runtime API calls
                ▼
┌─────────────────────────────────────┐
│        Runtime & Project Store       │
│     (Singleton State Authority)      │
│                                     │
│  - active project                    │
│  - active Canon instance             │
│  - save discipline                   │
└───────────────┬─────────────────────┘
                │ delegates logic
                ▼
┌─────────────────────────────────────┐
│             Core Engine              │
│                                     │
│  Canon | Rules | Events | Timeline   │
│  Paradox Engine | Validator | Replay │
└─────────────────────────────────────┘
```

Key rule:

> UI never talks directly to core logic — all access goes through the runtime.

---

## 2. Canon Data Model

Canon is the **authoritative narrative state**.

```
Canon
│
├─ meta
│   ├─ title
│   ├─ author
│   └─ version
│
├─ truths
│   ├─ fact_key → bool
│   └─ ...
│
├─ rules
│   ├─ conditions
│   ├─ constraint
│   ├─ severity
│   └─ override
│
├─ acts
│   ├─ { id, label }
│   └─ ...
│
├─ events
│   ├─ id
│   ├─ act
│   ├─ name
│   └─ sets_truths
│
├─ event_log
├─ snapshots
├─ integrity
└─ dependencies
```

Canon itself does **not** decide:

* when it is saved
* how it is displayed
* which actions are allowed

---

## 3. Event-Driven State Mutation

Events are the **only allowed mutation path**.

```
[ Event ]
   │
   ▼
Apply to Canon
   │
   ├─ mutate truths
   ├─ append to event list
   ├─ log commit
   ├─ update snapshots
   └─ update integrity
```

Nothing else mutates truths directly.

---

## 4. Act-Based Timeline Flow

Acts provide **explicit narrative time**.

```
Act 1
 ├─ Event A
 ├─ Event B
 │
 └─ Canon state after Act 1
        │
        ▼
Act 2
 ├─ Event C
 │
 └─ Canon state after Act 2
        │
        ▼
Act 3
 ├─ Event D
 └─ Event E
```

Timeline state is **reconstructed**, not stored.

---

## 5. Paradox Detection Flow

Paradox detection is **read-only**.

```
Canon State
   │
   ▼
Evaluate Rules
   │
   ├─ Are conditions satisfied?
   ├─ Is rule severity = hard?
   ├─ Does rule forbid a truth?
   └─ Is that truth currently true?
   │
   ▼
Paradox Report
```

Important:

* Paradox detection does **not** block events
* It only reports inconsistency

---

## 6. Validation vs Paradox (Critical Distinction)

```
          ┌─────────────────┐
          │  Proposed Event │
          └────────┬────────┘
                   │
                   ▼
           Validation Engine
                   │
          ┌────────┴────────┐
          │                 │
       Blocked            Allowed
                             │
                             ▼
                        Apply Event
                             │
                             ▼
                     Updated Canon
                             │
                             ▼
                     Paradox Detection
```

Validation = *Should this happen?*
Paradox = *Is the story inconsistent now?*

They are intentionally separate.

---

## 7. Replay & Reconstruction

Replay rebuilds canon from history.

```
Empty Canon
   │
   ├─ Apply Event 1
   ├─ Apply Event 2
   ├─ Apply Event 3
   │
   ▼
Reconstructed Canon
```

Given the same events in the same order, replay always produces the same result.

---

## 8. Runtime & Persistence Control

```
UI Action
   │
   ▼
Runtime API
   │
   ├─ check active project
   ├─ apply mutation
   └─ persist to disk
           │
           ▼
        JSON File
```

Rules:

* No active project → no save
* No direct disk writes from UI
* No implicit autosave

---

## 9. UI Responsibility Map

```
[ Project Panel ] ── lifecycle & persistence
[ Truths Panel ]  ── fact editing
[ Rules Panel ]   ── constraint authoring
[ Events Panel ]  ── state mutation
[ Timeline Panel ]── causal visualization
[ Paradox Panel ] ── inconsistency inspection
[ Validation ]    ── rule feedback
[ Debugger ]      ── replay & inspection
```

Each panel:

* has one responsibility
* does not perform logic
* calls runtime APIs only

---

## 10. Determinism Guarantee

```
Same Events
+ Same Order
+ Same Rules
+ Same Conditions
──────────────────
Same Canon State
```

There is:

* no randomness
* no hidden mutation
* no time-based behavior

---

## Summary

These diagrams illustrate how PURGE achieves:

* explicit narrative state
* deterministic evolution
* traceable causality
* debuggable contradictions
* clean separation of concerns

They are meant to be read alongside `ARCHITECTURE.md`.