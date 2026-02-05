This document defines non-negotiable constraints for the system.
These are semantic locks, not suggestions.

If any instruction appears to conflict with this document, you must stop and report the conflict.

1. API LOCKS

Framework: FastAPI

The API must expose a public HTTP endpoint

Access must be protected using x-api-key

All responses must be deterministic JSON

JSON structure must be produced by application code, never by an LLM

Implications

LLM output may only be inserted into string fields (e.g. reply)

LLMs must never:

Create JSON

Decide response schema

Control HTTP behavior

2. FSM (FINITE STATE MACHINE) LOCKS

The system lifecycle is governed by a strict, one-way FSM.

Allowed States (fixed)
INIT
NORMAL
SUSPICIOUS
AGENT_ENGAGED
INTEL_READY
CALLBACK_SENT
TERMINATED

Global FSM Rules

State transitions are one-way only

No backward transitions are allowed

No state skipping is allowed

FSM state may only be changed by explicit lifecycle logic

FSM state must never be inferred implicitly

3. SCAM DETECTION LOCKS

Scam detection is rule-based only

Detection must be delayed (minimum turns required)

Detection logic:

Produces signals and confidence

Does not change state directly

False positives are worse than false negatives

Implications

Detection ≠ engagement

Detection ≠ response generation

Detection ≠ finalization

Detection is analysis only.

4. LLM / GPT ROLE LOCKS

LLMs are text renderers only.

LLMs may:

Generate natural language replies for the persona

Paraphrase or restate content in human-like language

LLMs must never:

Decide next actions

Change FSM state

Trigger callbacks

Extract intelligence

Control program flow

Decide when intelligence is “ready”

If an LLM suggests or implies decisions, those outputs must be ignored.

5. INTELLIGENCE EXTRACTION LOCKS

Extraction is deterministic

Extraction uses:

Regex

Validation

Deduplication

No LLM inference is allowed in extraction

Extractable Intelligence (fixed)

Bank account numbers

UPI IDs

Phishing URLs

Phone numbers

Suspicious keywords

Implications

If data does not match validation rules, it is discarded

Missing intelligence is acceptable

Hallucinated intelligence is unacceptable

6. CALLBACK LOCKS (MANDATORY)

Final callback must be sent

Callback must be sent exactly once per session

Callback must be:

Idempotent

Retried with backoff

Timed out safely

Callback Timing (critical)

Callback may only be sent after:

Scam intent is confirmed

Agent engagement is completed

Intelligence extraction is finalized

Callback must never be triggered:

During detection

During engagement

Based on timeouts alone

7. DEPLOYMENT LOCKS

Free-tier compatible

Always-on behavior

Low latency preferred over complexity