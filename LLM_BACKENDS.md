## LLM Backends in the PURGE Engine

---

## 1. Purpose of This Document

This document describes how large language models (LLMs) are integrated into the PURGE engine, with a focus on **architectural boundaries**, **non-goals**, and **backend neutrality**.

PURGE does not treat LLMs as authoritative narrative agents. Instead, LLMs are optional components used to **assist human authorship** by generating structured narrative proposals.

---

## 2. Role of LLMs in PURGE

Within PURGE, LLMs are used exclusively for:

* Interpreting high-level narrative intent
* Generating structured proposals (events, rules, suggestions)
* Providing rationale and confidence estimates

LLMs **do not**:

* Mutate canon directly
* Bypass rule validation
* Resolve paradoxes autonomously
* Override human approval

All LLM output is advisory and subject to formal validation.

---

## 3. VerseMind as the Abstraction Layer

All LLM interaction is mediated through **VerseMind**, which serves as a strict abstraction layer between the engine and any specific model or runtime.

VerseMind is responsible for:

* Prompt construction
* Output schema enforcement
* Confidence annotation
* Proposal normalization

This design ensures that:

* The core engine remains model-agnostic
* LLM backends can be swapped without architectural changes
* Experimental integrations do not destabilize canon logic

---

## 4. Ollama Integration Status

Ollama is currently treated as an **experimental, optional backend**.

### Characteristics

* Local execution
* No external API dependency
* Suitable for offline experimentation
* Useful for rapid prototyping and research

### Current Position

* Ollama is **not a required dependency**
* Ollama is **not assumed to be present**
* Ollama is **not referenced by core engine logic**

Integration, when enabled, occurs entirely behind the VerseMind interface.

---

## 5. Backend Requirements

Any LLM backend used with PURGE (including Ollama) must satisfy the following constraints:

1. **Structured Output**
   Responses must conform to explicit schemas.

2. **Explainability**
   Proposals must include rationale and confidence signals.

3. **Determinism Tolerance**
   Non-deterministic outputs must be mediated by validation.

4. **Isolation**
   Backend failures must not corrupt canon or engine state.

5. **Human-in-the-Loop Enforcement**
   No proposal may be applied without explicit approval.

---

## 6. Non-Goals

PURGE explicitly does **not** aim to:

* Train LLMs
* Fine-tune narrative models
* Serve as an LLM framework
* Replace human authorship
* Optimize for maximum generation volume

LLMs are tools, not co-authors.

---

## 7. Future Directions

Future work may include:

* Additional local backends
* Remote API-based backends
* Comparative evaluation of backend behavior
* Backend-specific prompt adapters

Such extensions will not alter core engine invariants.

---

## 8. Summary

PURGE maintains a strict separation between:

* **Narrative authority** (canon, rules, validation)
* **Narrative assistance** (LLMs via VerseMind)

Ollama is acknowledged as a useful experimental backend, but the engine remains fundamentally **backend-neutral and research-oriented**.

---

### End of Document